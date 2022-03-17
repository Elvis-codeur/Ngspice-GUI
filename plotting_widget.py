from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT
from matplotlib.figure import Figure
from matplotlib.backend_bases import Event
from matplotlib.backend_bases import MouseButton 
import matplotlib.pyplot as plt

class PlottingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.figure = Figure()
        self.ax = self.figure.add_subplot(111)

        self.canvas = FigureCanvasQTAgg(self.figure)
        self.toolbar = NavigationToolbar2QT(self.canvas,self)

        self.signalWiewer = QListView()
        
        self.layoutPrincipale = QVBoxLayout()

        self.plot_dict = {}
        self.plot_dict["TRAN"] = {}
        self.plot_dict["DC"] = {}
        self.plot_dict["AC"] = {}


        self.init_UI()


    def init_UI(self):
        self.layoutPrincipale.addWidget(self.toolbar)
        self.layoutPrincipale.addWidget(self.canvas)
        self.setLayout(self.layoutPrincipale)

        #self.plot("")

    def plot(self,data):
        #print(data)
        """data is a dict 
        it contain : 
        label : the label of the data
        title : the title of the data
        data : the numerical data to plot
        time : the time if it is a transcient analysis
        type : TR,AC"""
        
        #self.ax.clear()

        if(data["type"] == "TR"):
            if data["signature"] in self.plot_dict["TRAN"].keys():
                line = self.plot_dict["TRAN"][data["signature"]].pop(0)
                line.remove()
                self.ax.legend()

            else:
                
                plot = self.ax.plot(data["time"],data["data"],label=data["label"])
                self.ax.set_xlabel("time")
                self.ax.set_ylabel(data["label"])
                self.ax.legend()

                self.plot_dict["TRAN"][data["signature"]] =  plot
                #print(self.plot_dict)
                #print(help(self.ax))

        elif data["type"] == "DC":
            if data["signature"] in self.plot_dict["DC"].keys():
                line = self.plot_dict["DC"][data["signature"]].pop(0)
                line.remove()
                self.ax.legend()

            else:
                plot = self.ax.plot(data["v-sweep"],data["data"],label=data["label"])
                self.ax.set_xlabel("v-sweep")
                self.ax.set_ylabel(data["label"])
                self.ax.legend()
                self.plot_dict["DC"][data["signature"]] = plot

            
        elif data["type"] == "AC":
            if data["signature"] in self.plot_dict["AC"].keys():
                line1,line2 = self.plot_dict["AC"][data["signature"]]

                # Remove the plots
                line1 = line1.pop(0)
                line1.remove()
                line2 = line2.pop(0)
                line2.remove()

                self.ax.legend()
            else:

                plot = self.ax.plot(data["frequency"],data["gain"],label = "gain")
                self.ax.set_ylabel("Gain")
                self.ax.set_xlabel("Fréquence")
                self.ax.set_xscale("log")
                self.ax.legend()

                self.ax2 = self.ax.twinx()
                plot2 = self.ax2.plot(data["frequency"],data["phase"],label = "phase",color="red")
                self.ax2.set_ylabel("Phase")
                self.ax2.set_xlabel("Fréquence")
                self.ax2.set_xscale("log")
                self.ax2.legend()

                self.plot_dict["AC"][data["signature"]] = plot,plot2



        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PlottingWidget()
    w.show()
    sys.exit(app.exec())