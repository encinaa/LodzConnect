from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# AQUI CARGAMOS TODAS LAS INTERFACES
Form, Window = uic.loadUiType("./src/vista/Ui/PáginaPrincipal2.ui")

class PáginaPrincipal(QMainWindow, Form):
    iniciar_clicked = pyqtSignal()
    registrarse_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self) 

        self.BotonIniciar.clicked.connect(self.iniciar_clicked)
        self.BotonRegistrarse.clicked.connect(self.registrarse_clicked)
