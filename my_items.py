from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys

from sympy import arg

class StandardItem(QStandardItem):
    def __init__(self,text):
        super().__init__()
        self.setText(text)
        a = 0

        #self.doubleClicked.connect(self.p)

    def p(self):
        print("Elvis est un enfant de Dieu")

    def mouseDoubleClickEvent(self,event):
        print(self.accessibleText())





if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = StandardItem()
    w.show()
    sys.exit(app.exec())