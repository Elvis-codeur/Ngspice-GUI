
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

import numpy as np

from plotting_widget import PlottingWidget
from ngspice.process_raw import ProcessRaw
from ngspice.simulator import NgspiceSimulator
from my_items import StandardItem

""" This widget will do the process works"""

class VisualisationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.signalViewer = QTreeView()
        self.signalViewerModel = QStandardItemModel()
        
        self.plottingW = PlottingWidget()
        self.layoutPrincipale = QHBoxLayout()

        self.default_command = ["run","save all","set filetype = ascii"]


        self.init_UI()

    def init_UI(self):
        self.signalViewer.setMaximumWidth(200)

        """
        el = QStandardItem("Elvis")
        el.appendRow([QStandardItem("Elvis1"),QStandardItem("Elvis2")])
        self.signalViewerModel.appendRow(el)
        """
        self.signalViewer.setModel(self.signalViewerModel)

        self.layoutPrincipale.addWidget(self.signalViewer)
        self.layoutPrincipale.addWidget(self.plottingW)
        self.setLayout(self.layoutPrincipale)

        #self.process_raw("")
        #self.init_visualisation()

        self.signalViewer.clicked.connect(self.plot)

    def plot(self,kl):
        try:

            a = self.signalViewerModel.itemFromIndex(kl)
            parent = a.parent()
            #print("detected ==",a.text(),"parent ==",parent.text())
            self.plot_signal(parent.text(),a.text())
        except Exception as e:
            print(e)

    def erase_list_view(self):
        for i in range(self.signalViewerModel.rowCount()):
            self.signalViewerModel.removeRow(i)

    def add_rows(self,labels):
        self.signalViewerModel = QStandardItemModel()

        #print("old signal removed")
        #print("\n",self.datas.keys(),"\n")
        for i in self.datas.keys():
            #print("==={}===".format(i))
            k = QStandardItem(i)
            k.setEditable(False)

            l = []
            #print("signal name =====",self.datas[i].keys())
            for u in self.datas[i].keys():
                p = QStandardItem(u)
                p.setEditable(False)
                l.append(p)

            k.appendRows(l)

            self.signalViewerModel.appendRow(k)
            self.signalViewer.setModel(self.signalViewerModel)
        print("new signals added")


    def p(self):
        print("kommm")

    def process_netlist_text(self,text):
        try:
            self.netlistProcessor = NgspiceSimulator()
            self.datas = self.netlistProcessor.simulate_netlist(text,self.default_command)
            self.init_visualisation()
        except Exception as e:
            print(e)

    def process_netlist_file(self,file_name):
        try:
            self.netlistProcessor = NgspiceSimulator()
            #print(text)
            self.datas = self.netlistProcessor.simulate_file(file_name,self.default_command)
            #print(self.datas.keys())
            self.init_visualisation()
        except Exception as e:
            print(e)

    def process_raw(self,filename):
        try:
            self.rawProcessor = ProcessRaw("cc.raw")
            self.datas = self.rawProcessor.args
        except Exception as e:
            print(e)

    def init_visualisation(self):
        self.add_rows(self.datas)

        """
        self.plottingW.plot({"label":list(self.datas.keys())[1],
                            "data":self.datas[list(self.datas.keys())[1]],
                            "time":self.datas[list(self.datas.keys())[0]],
                             "type":"TR"})
        """

    def plot_signal(self,parent_name,signal_name):
        #print(self.datas)
        print("len === ",len(self.datas[parent_name][signal_name]))
        try:
            primary_key = self.datas.keys()
            if(parent_name in primary_key):
                if(signal_name in self.datas[parent_name]):
                    if("v-sweep" in self.datas[parent_name]):

                        #print("data = ",self.datas[parent_name][signal_name])
                        self.plottingW.plot({
                            "label" :parent_name + " # " + signal_name,
                            "data" : self.datas[parent_name][signal_name],
                            "v-sweep" : self.datas[parent_name]["v-sweep"],
                            "type" :"DC"
                            })

                    elif ("frequency" in self.datas[parent_name]):
                        d = self.datas[parent_name][signal_name]
                        if(d):
                            for i in d:
                                print("d == ",d)
                                gains = []
                                args = []

                                gain = np.sqrt(i.imag**2 + i.real**2)
                                gains.append(gain)

                                arg = np.arccos(i.real/gain)

                                if(np.imag > 0):
                                    args.append(arg)
                                else:
                                    args.append(-arg)

                            self.plottingW.plot({
                            "title" : parent_name + " # " + signal_name,
                            "gain" : gains,
                            "phase" : args,
                            "frequency":self.datas[parent_name]["frequency"],
                            "type" :"AC"
                            })

                        else:
                            print("Unable to plot signal")



                    elif "time" in self.datas[parent_name]:
                        print("data = ",self.datas[parent_name][signal_name])


        except Exception as e:
            print("Execption = ",e)

        
        """try:
            if signal_name not in self.datas.keys():
                print("Signal inexistant")
            else:
                
                self.plottingW.plot({
                    "label":signal_name,
                    "data" : self.datas[signal_name],
                    "time" : self.datas["time"],
                    "type" :"TR"
                    })

        except Exception as e:
            print("Exception" ,e," ",signal_name not in self.datas.keys())
        """




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VisualisationWidget()
    w.show()
    sys.exit(app.exec())