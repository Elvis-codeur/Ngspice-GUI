from ctypes import (CDLL, CFUNCTYPE, Structure, c_int, c_char_p, c_void_p,
                    c_bool, c_double, POINTER, c_short)

from ctypes.util import find_library
import encodings
from importlib.resources import path

import os 
import logging
from signal import signal
from sys import prefix
from django.dispatch import Signal
import numpy as np
import pathlib 
logger = logging.getLogger(__name__)

#print("\n\n\n",os.path.join(os.getcwd(),"ngspice.dll"))

spice = CDLL(os.path.join(os.getcwd(),"bin/ngspice.dll"))

# typedef struct vecvalues {
# char* name; /* name of a specific vector */
# double creal; /* actual data value */
# double cimag; /* actual data value */
# bool is_scale;/* if 'name' is the scale vector */
# bool is_complex;/* if the data are complex numbers */
# } vecvalues, *pvecvalues;


class vecvalues(Structure):
    _fields_ = [
        ('name', c_char_p),
        ('creal', c_double),
        ('cimag', c_double),
        ('is_scale', c_bool),
        ('is_complex', c_bool)]


# typedef struct vecvaluesall {
# int veccount; /* number of vectors in plot */
# int vecindex; /* index of actual set of vectors. i.e. the number of accepted data points */
# pvecvalues *vecsa; /* values of actual set of vectors, indexed from 0 to veccount - 1 */
# } vecvaluesall, *pvecvaluesall;


class vecvaluesall(Structure):
    _fields_ = [
        ('veccount', c_int),
        ('vecindex', c_int),
        ('vecsa', POINTER(POINTER(vecvalues)))]


# struct ngcomplex {
#    double cx_real;
#    double cx_imag;
# } ;

class ngcomplex(Structure):
    _fields_ = [
        ('cx_real', c_double),
        ('cx_imag', c_double)]


# /* Dvec flags. */
# enum dvec_flags {
#   VF_REAL = (1 << 0),       /* The data is real. */
#   VF_COMPLEX = (1 << 1),    /* The data is complex. */
#   VF_ACCUM = (1 << 2),      /* writedata should save this vector. */
#   VF_PLOT = (1 << 3),       /* writedata should incrementally plot it. */
#   VF_PRINT = (1 << 4),      /* writedata should print this vector. */
#   VF_MINGIVEN = (1 << 5),   /* The v_minsignal value is valid. */
#   VF_MAXGIVEN = (1 << 6),   /* The v_maxsignal value is valid. */
#   VF_PERMANENT = (1 << 7)   /* Don't garbage collect this vector. */
# };


class dvec_flags(object):
    vf_real = (1 << 0)  # The data is real.
    vf_complex = (1 << 1)  # The data is complex.
    vf_accum = (1 << 2)  # writedata should save this vector.
    vf_plot = (1 << 3)  # writedata should incrementally plot it.
    vf_print = (1 << 4)  # writedata should print this vector.
    vf_mingiven = (1 << 5)  # The v_minsignal value is valid.
    vf_maxgiven = (1 << 6)  # The v_maxsignal value is valid.
    vf_permanent = (1 << 7)  # Don't garbage collect this vector.


# /* vector info obtained from any vector in ngspice.dll.
# Allows direct access to the ngspice internal vector structure,
# as defined in include/ngspice/devc.h .*/
# typedef struct vector_info {
#    char *v_name;		/* Same as so_vname. */
#    int v_type;			/* Same as so_vtype. */
#    short v_flags;		/* Flags (a combination of VF_*). */
#    double *v_realdata;		/* Real data. */
#    ngcomplex_t *v_compdata;	/* Complex data. */
#    int v_length;		/* Length of the vector. */
# } vector_info, *pvector_info;

class vector_info(Structure):
    _fields_ = [
        ('v_name', c_char_p),
        ('v_type', c_int),
        ('v_flags', c_short),
        ('v_realdata', POINTER(c_double)),
        ('v_compdata', POINTER(ngcomplex)),
        ('v_length', c_int)]


# int  ngSpice_Command(char* command);
spice.ngSpice_Command.argtypes = [c_char_p]

# int ngSpice_Circ(char**)
spice.ngSpice_Circ.argtypes = [POINTER(c_char_p)]
spice.ngSpice_AllPlots.restype = POINTER(c_char_p)

spice.ngSpice_AllVecs.argtypes = [c_char_p]
spice.ngSpice_AllVecs.restype = POINTER(c_char_p)
spice.ngSpice_CurPlot.restype = c_char_p

spice.ngGet_Vec_Info.restype = POINTER(vector_info)
spice.ngGet_Vec_Info.argtypes = [c_char_p]

captured_output = []


# Unit names for use with pint or other unit libraries
vector_type = [
    'dimensionless',  # notype = 0
    'second',  # time = 1
    'hertz',  # frequency = 2
    'volt',  # voltage = 3
    'ampere',  # current = 4
    'NotImplemented',  # output_n_dens = 5
    'NotImplemented',  # output_noise = 6
    'NotImplemented',  # input_n_dens = 7
    'NotImplemented',  # input_noise = 8
    'NotImplemented',  # pole = 9
    'NotImplemented',  # zero = 10
    'NotImplemented',  # sparam = 11
    'NotImplemented',  # temp = 12
    'ohm',  # res = 13
    'ohm',  # impedance = 14
    'siemens',  # admittance = 15
    'watt',  # power = 16
    'dimensionless'  # phase = 17
    'NotImplemented',  # db = 18
    'farad'  # capacitance = 19
    'coulomb'  # charge = 21
]


#
# enum simulation_types {
#   ...
# };
class simulation_type(object):
    notype = 0
    time = 1
    frequency = 2
    voltage = 3
    current = 4
    output_n_dens = 5
    output_noise = 6
    input_n_dens = 7
    input_noise = 8
    pole = 9
    zero = 10
    sparam = 11
    temp = 12
    res = 13
    impedance = 14
    admittance = 15
    power = 16
    phase = 17
    db = 18
    capacitance = 19
    charge = 20


from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class SignalSender(QObject):
    signal = pyqtSignal(str)

SIGNAL_SENDER = SignalSender()

@CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
def printfcn(output, _id, _ret):

    
    """Callback for libngspice to print a message"""
    global captured_output
    print(output)
    prefix, _, content = output.decode('ascii').partition(' ')
    if prefix == 'stderr':
        
        logger.error(content)
        a =1
    else:
        captured_output.append(content)
        SIGNAL_SENDER.signal.emit("\n".join(captured_output))
    return 0


@CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
def statfcn(status, _id, _ret):
    """
    Callback for libngspice to report simulation status like 'tran 5%'
    """
    #logger.debug(status.decode('ascii'))
    return 0


@CFUNCTYPE(c_int, c_int, c_bool, c_bool, c_int, c_void_p)
def controlled_exit(exit_status, immediate_unloading, requested_exit,
                    libngspice_id, ret):
    logger.debug('ControlledExit',
                 dict(exit_status=exit_status,
                      immediate_unloading=immediate_unloading,
                      requested_exit=requested_exit,
                      libngspice_id=libngspice_id, ret=ret))

@CFUNCTYPE(c_int, POINTER(vecvaluesall), c_int, c_int, c_void_p)
def send_data(vecvaluesall_, num_structs, libngspice_id, ret):
    logger.debug('SendData', dict(vecvaluesall=vecvaluesall_,
                                  num_structs=num_structs,
                                  libngspice_id=libngspice_id,
                                  ret=ret))


def cmd(command):
    """
    Send a command to the ngspice engine

    Parameters
    ----------
    command : str
        An ngspice command

    Returns
    -------
    list of str
        Lines of the captured output

    Examples
    --------

    Print all default variables

    >>> ns.cmd('print all')
    ['false = 0.000000e+00',
     'true = 1.000000e+00',
     'boltz = 1.380620e-23',
     'c = 2.997925e+08',
     'e = 2.718282e+00',
     'echarge = 1.602190e-19',
     'i = 0.000000e+00,1.000000e+00',
     'kelvin = -2.73150e+02',
     'no = 0.000000e+00',
     'pi = 3.141593e+00',
     'planck = 6.626200e-34',
     'yes = 1.000000e+00']

    """
    max_length = 1023
    if len(command) > max_length:
        raise ValueError('Command length', len(command), 'greater than',
                         max_length)
    del captured_output[:]
    spice.ngSpice_Command(command.encode('ascii'))
    logger.debug('Command %s returned %s', command, captured_output)
    return captured_output

def circ(netlist_lines):
    """
    Load a netlist

    Parameters
    ----------

    netlist_lines : str or list of str
        Netlist, either as a list of lines, or a
        single multi-line string.  Indentation and white
        space don't matter. Unlike a netlist file, the
        first line doesn't need to be a comment, and you
        don't need to provide the `.end`.

    Returns
    -------
    int
        `1` upon error, otherwise `0`.

    Examples
    --------

    Using a sequence of lines:

    >>> ns.circ(['va a 0 dc 1', 'r a 0 2'])
    0

    Using a single string:

    >>> ns.circ('''va a 0 dc 1
    ...         r a 0 2''')
    0

    """
    if issubclass(type(netlist_lines), str):
        netlist_lines = netlist_lines.split('\n')
    netlist_lines = [line.encode('ascii') for line in netlist_lines]
    # First line is ignored by the engine
    netlist_lines.insert(0, b'* ngspyce-created netlist')
    # Add netlist end
    netlist_lines.append(b'.end')
    # Add list terminator
    netlist_lines.append(None)
    array = (c_char_p * len(netlist_lines))(*netlist_lines)
    return spice.ngSpice_Circ(array)

def plots():
    """
    List available plots (result sets)

    Each plot is a collection of vector results

    Returns
    -------
    list of str
        List of existing plot names

    Examples
    --------

    Each analysis creates a new plot

    >>> ns.circ(['v1 a 0 dc 1', 'r1 a 0 1k']); ns.plots()
    ['const']
    >>> ns.operating_point(); ns.plots()
    ['op1', 'const']
    >>> ns.dc('v1', 0, 5, 1); ns.plots()
    ['dc1', 'op1', 'const']

    Get lists of vectors available in different plots:

    >>> ns.vectors(plot='const').keys()
    dict_keys(['echarge', 'e', 'TRUE', 'FALSE', 'no', 'i', ... 'c', 'boltz'])
    >>> ns.vectors(plot='ac1').keys()
    dict_keys(['V(1)', 'vout', 'v1#branch', 'frequency'])
    """
    ret = []
    plotlist = spice.ngSpice_AllPlots()
    ii = 0
    while True:
        if not plotlist[ii]:
            return ret
        ret.append(plotlist[ii].decode('ascii'))
        ii += 1


def vector_names(plot=None):
    """
    Names of vectors present in the specified plot

    Names of the voltages, currents, etc present in the specified plot.
    Defaults to the current plot.

    Parameters
    ----------
    plot : str, optional
        Plot name. Defaults to the current plot.

    Returns
    -------
    list of str
        Names of vectors in the plot

    Examples
    --------

    List built-in constants

    >>> ns.vector_names('const')
    ['planck', 'boltz', 'echarge', 'kelvin', 'i', 'c', 'e', 'pi', 'FALSE', 'no', 'TRUE', 'yes']

    Vectors produced by last analysis

    >>> ns.circ('v1 a 0 dc 2');
    >>> ns.operating_point();
    >>> ns.vector_names()
    ['v1#branch', 'a']

    """
    names = []
    if plot is None:
        plot = spice.ngSpice_CurPlot().decode('ascii')
    veclist = spice.ngSpice_AllVecs(plot.encode('ascii'))
    ii = 0
    while True:
        if not veclist[ii]:
            return names
        names.append(veclist[ii].decode('ascii'))
        ii += 1

def vector(name, plot=None):
    """
    Return a numpy.ndarray with the specified vector

    Uses the current plot by default.

    Parameters
    ----------
    name : str
        Name of vector
    plot : str, optional
        Which plot the vector is in. Defaults to current plot.

    Returns
    -------
    ndarray
        Value of the vector

    Examples
    --------

    Run an analysis and retrieve a vector

    >>> ns.circ(['v1 a 0 dc 2', 'r1 a 0 1k']);
    >>> ns.dc('v1', 0, 2, 1);
    >>> ns.vector('v1#branch')
    array([ 0.   , -0.001, -0.002])

    """
    if plot is not None:
        name = plot + '.' + name
        
    vec = spice.ngGet_Vec_Info(name.encode('ascii'))
    #print(vec)
    if not vec:
        raise RuntimeError('Vector {} not found'.format(name))
    vec = vec[0]
    if vec.v_length == 0:
        array = np.array([])
    elif vec.v_flags & dvec_flags.vf_real:
        array = np.ctypeslib.as_array(vec.v_realdata, shape=(vec.v_length,))
    elif vec.v_flags & dvec_flags.vf_complex:
        components = np.ctypeslib.as_array(vec.v_compdata,
                                           shape=(vec.v_length, 2))
        array = np.ndarray(shape=(vec.v_length,), dtype=complex,
                           buffer=components)
    else:
        raise RuntimeError('No valid data in vector')
    logger.debug('Fetched vector {} type {}'.format(name, vec.v_type))
    array.setflags(write=False)
    if name == 'frequency':
        return array.real
    return array



def initialize_ngspice():
    spice.ngSpice_Init(printfcn, statfcn, controlled_exit, send_data, None, None,
                       None)
    # Prevent paging output of commands (hangs)
    cmd('set nomoremode')

"""
initialize_ngspice()
cmd("source sim3.cir")
cmd("tran 10n 1m uic")
print(vector_names("tran1"))
print(plots())

import matplotlib.pyplot as plt

time,in1 = vector("time"),vector("in2")

plt.plot(time,in1)
plt.show()
"""