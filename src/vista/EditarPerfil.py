from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, Window = uic.loadUiType("./src/vista/Ui/EditarPerfil2.ui") 

class EditarPerfil(VistaNavegable, Form):
    guardar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
        self.BotonGuardarPerfil.clicked.connect(self.guardar_clicked)
