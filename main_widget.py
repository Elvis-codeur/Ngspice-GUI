

from fileinput import filename
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from visualisation_widget import  VisualisationWidget

from text_editor import TextEditor

from ngspice.shared_ngspice import SIGNAL_SENDER

class MainWidget(QMainWindow):
    simulate = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.layoutPrincipale = QVBoxLayout()

        self.tabWidget = QTabWidget()
        self.netlistEditorWidget = TextEditor()
        self.visualisationWidget = VisualisationWidget()
        self.outputWidget = QTextEdit()

        self.toolbar = QToolBar("Editeur")
        

        self.centralW = QWidget()

        self.init_UI()

    def init_UI(self):

        self.setWindowTitle("Ngspice GUI")

        self.simulate.connect(self.visualisationWidget.process_netlist)
        SIGNAL_SENDER.signal.connect(self.set_output_text)

        # Les fichiers
        self.menuFichier = self.menuBar().addMenu("Fichier")
        self.menuSimulation = self.menuBar().addMenu("Simulation")

        self.ouvrirAction = QAction("Ouvrir un fichier")
        self.menuFichier.addAction(self.ouvrirAction)
        self.ouvrirAction.triggered.connect(self.open_file)

        self.saveAction = QAction("Enrégistrer")
        self.menuFichier.addAction(self.saveAction)
        self.saveAction.triggered.connect(self.save)

        self.saveasAction = QAction("Enrégistrer comme")
        self.menuFichier.addAction(self.saveasAction)
        self.menuFichier.addAction(self.saveasAction)

        self.actionFont = QAction("Font")
        self.actionFont.triggered.connect(self.set_font)
        

        self.runAction = QAction(QIcon("play.png"),"Simuler")
        self.runAction.setToolTip("Simuler")
        self.menuSimulation.addAction(self.runAction)
        

        self.toolbar.addAction(self.actionFont)
        self.toolbar.addAction(self.runAction)

        self.addToolBar(self.toolbar)
        
        self.tabWidget.addTab(self.netlistEditorWidget,"Editeur de netlist")
        self.tabWidget.addTab(self.visualisationWidget,"Visualisateur de signaux")
        self.layoutPrincipale.addWidget(self.tabWidget)
        self.layoutPrincipale.addWidget(self.outputWidget)

        self.centralW.setLayout(self.layoutPrincipale)
        self.setCentralWidget(self.centralW)


    def open_file(self):
        file_dialog = QFileDialog()
        file_name = file_dialog.getOpenFileName(self,"Enrégistrer le fichier",str(),"*.net *.cir *.txt")
        #print(file_name)
        f = open(file_name[0],encoding="utf-8",mode="r")
        text = f.read()
        f.close()
        self.netlistEditorWidget.setPlainText(text)
        self.simulate.emit(file_name[0])

    def set_output_text(self,message):
        self.outputWidget.setPlainText(message)

    def save(self):
        a = 0
    
    def save_as(self):
        a = 0

    def set_font(self):
        fontdialog = QFontDialog()

        font = fontdialog.getFont()
        self.netlistEditorWidget.setFont(font[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec())