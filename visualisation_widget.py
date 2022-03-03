
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from plotting_widget import PlottingWidget
from ngspice.process_raw import ProcessRaw
from ngspice.simulator import NgspiceSimulator

""" This widget will do the process works"""

class VisualisationWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.signalViewer = QListView()
        self.signalViewerModel = QStandardItemModel()
        
        self.plottingW = PlottingWidget()
        self.layoutPrincipale = QHBoxLayout()


        self.init_UI()

    def init_UI(self):
        self.signalViewer.setMaximumWidth(200)

        self.signalViewerModel.appendRow(QStandardItem("Elvis"))

        self.signalViewer.setModel(self.signalViewerModel)

        self.layoutPrincipale.addWidget(self.signalViewer)
        self.layoutPrincipale.addWidget(self.plottingW)
        self.setLayout(self.layoutPrincipale)

        self.process_raw("")
        self.init_visualisation()

    def erase_list_view(self):
        for i in range(self.signalViewerModel.rowCount()):
            self.signalViewerModel.removeRow(i)

    def add_rows(self,labels):
        for i in labels:
            self.signalViewerModel.appendRow(QStandardItem(i))

    def process_netlist(self,text):
        try:
            self.netlistProcessor = NgspiceSimulator()
            #print(text)
            self.datas = self.netlistProcessor.simulate(text,"tran 10n 1m uic")
            self.datas = self.datas["tran1"]
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
        self.add_rows(list(self.datas.keys())[1:])

        self.plottingW.plot({"label":list(self.datas.keys())[1],
                            "data":self.datas[list(self.datas.keys())[1]],
                            "time":self.datas[list(self.datas.keys())[0]],
                             "type":"TR"})

    def plot_signal(self,signal_name):
        self.plottingW.plot({
            "label":signal_name,
            "data" : self.datas[signal_name]
        })




if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = VisualisationWidget()
    w.show()
    sys.exit(app.exec())