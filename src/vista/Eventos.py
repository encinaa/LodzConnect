from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal


Form, _ = uic.loadUiType("./src/vista/Ui/Eventos.ui")

class Eventos(VistaNavegable, Form):
    actualizar_eventos_clicked = pyqtSignal()


    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

