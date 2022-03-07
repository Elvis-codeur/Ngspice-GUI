
from fileinput import filename
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from constante import *

from visualisation_widget import  VisualisationWidget

from text_editor import TextEditor

from ngspice.shared_ngspice import SIGNAL_SENDER

class MainWidget(QMainWindow):
    simulate_file = pyqtSignal(str)
    simulate_netlist = pyqtSignal(str)
    process_raw = pyqtSignal(str)
    def __init__(self):
        super().__init__()

        self.layoutPrincipale = QVBoxLayout()

        self.tabWidget = QTabWidget()
        self.netlistEditorWidget = TextEditor()
        self.visualisationWidget = VisualisationWidget()
        self.outputWidget = QTextEdit()

        self.file_name = ""
        self.netlist_text = ""

        self.toolbar = QToolBar("Editeur")
        self.centralW = QWidget()

        self.init_UI()

    def init_UI(self):

        self.setWindowTitle("Ngspice GUI")

        self.simulate_file.connect(self.visualisationWidget.process_netlist_file)
        self.simulate_netlist.connect(self.visualisationWidget.process_netlist_text)

        SIGNAL_SENDER.signal.connect(self.set_output_text)

        # Les fichiers
        self.menuFichier = self.menuBar().addMenu("Fichier")
        self.menuSimulation = self.menuBar().addMenu("Simulation")

        self.ouvrirAction = QAction("Ouvrir un fichier")
        self.ouvrirAction.setShortcut(QKeySequence("Ctrl+O"))
        self.menuFichier.addAction(self.ouvrirAction)
        self.ouvrirAction.triggered.connect(self.open_file)

        self.saveAction = QAction(QIcon("save.png"),"Enrégistrer")
        self.saveAction.setShortcut(QKeySequence("Ctrl+S"))
        self.menuFichier.addAction(self.saveAction)
        self.saveAction.triggered.connect(self.save)

        self.saveasAction = QAction(QIcon("save_as.png"), "Enrégistrer comme")
        self.saveasAction.setShortcut(QKeySequence("Ctrl+Shift+S"))
        self.menuFichier.addAction(self.saveasAction)
        self.saveAction.triggered.connect(self.save_as)

        self.actionFont = QAction(QIcon("font.png"),"Font")
        self.actionFont.triggered.connect(self.set_font)
        

        self.runAction = QAction(QIcon("play.png"),"Simuler")
        self.runAction.setToolTip("Simuler")
        self.runAction.triggered.connect(self.run_simulation)
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

        self.set_title()

    def open_file(self):
        file_dialog = QFileDialog()
        file_name = file_dialog.getOpenFileName(self,"Enrégistrer le fichier",str(),"*.net *.cir *.txt")
        
        if(file_name[0]):
            self.file_name = file_name[0]
            self.set_title()
            #print(file_name)
            f = open(file_name[0],encoding="utf-8",mode="r")
            text = f.read()
            f.close()
            self.netlistEditorWidget.setPlainText(text)
            #self.simulate.emit(file_name[0])


    def run_simulation(self):
        if(self.file_name):
            print("ion-filename")
            self.save()
            self.simulate_file.emit(self.file_name)
        else:
            print("cation-filename")
            self.netlist_text = self.netlistEditorWidget.toPlainText()
            if(self.netlist_text):
                self.save()
                self.simulate_netlist.emit(self.netlist_text)
            else:
                QMessageBox(self.centralW,"Erreur","Rien à simuler").show()


    def set_output_text(self,message):
        self.outputWidget.setPlainText(message)

    def set_title(self):
        if(self.file_name):
            self.setWindowTitle(SOFTWARE_NAME +" " + SOFTWARE_VERSION +" ->" +self.file_name)
        else:
            self.setWindowTitle(SOFTWARE_NAME +" " + SOFTWARE_VERSION)


    def __save(self,text):

        self.set_title()

        f = open(self.file_name,mode = "w",encoding="utf-8")
        if(f.writable()):
            f.write(text)
        else:
            b = QMessageBox(self,"Erreur","Impossible d'écrire le fichier")
            b.show()

    def save(self):
        text = self.netlistEditorWidget.toPlainText()

        if(self.file_name):
            self.__save(text)
                
        else:
            filedialog = QFileDialog()
            filename = filedialog.getSaveFileName(self,"Enrégister un fichier",str(),"*.net *.cir *.model")
            if filename:
                self.file_name = filename[0]
                if(self.file_name):
                    self.__save(text)


    
    def save_as(self):
        text = self.netlistEditorWidget.toPlainText()

        filedialog = QFileDialog()
        filename = filedialog.getSaveFileName(self,"Enrégister un fichier",str(),"*.net *.cir *.model")
        if filename:
            self.file_name = filename[0]
            if(self.file_name):
                self.__save(text)

    def set_font(self):
        fontdialog = QFontDialog()

        font = fontdialog.getFont()
        self.netlistEditorWidget.setFont(font[0])

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWidget()
    w.show()
    sys.exit(app.exec())