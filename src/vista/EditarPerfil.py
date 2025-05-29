from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/EditarPerfil2.ui") 

class EditarPerfil(QMainWindow, Form):
    guardar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.BotonGuardarPerfil.clicked.connect(self.guardar_clicked)
