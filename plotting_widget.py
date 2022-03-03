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
        if(data["type"] == "TR"):
            self.ax.plot(data["time"],data["data"],label=data["label"])
            self.ax.set_xlabel("time")
            self.ax.set_ylabel(data["label"])
            self.ax.legend()



        self.canvas.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = PlottingWidget()
    w.show()
    sys.exit(app.exec())