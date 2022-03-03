import ngspyce.ngspyce as ngspyce 

def simulate(netlist_name,cmd):
    # Load netlist
    ngspyce.source(netlist_name)

    # Sweep both base and collector current
    ngspyce.cmd(cmd)

    return ngspyce.vector_names()
a = "C:\\Users\\Elvis\\Documents\\code-source\\Python Script\\ngspice_gui\\ngspice\\brushless_circuit.cir"
simulate(a,"tran 10u 10m uic")
