from tkinter.tix import Tree
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import sys


class TextEditor(QTextEdit):
    def __init__(self):
        super().__init__()

        self.init_UI()

    def init_UI(self):
        self.setFont(QFont("Consolas",15,5,True))