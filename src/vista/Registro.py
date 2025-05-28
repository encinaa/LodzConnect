# src/vista/Registro.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/Registro3.ui")

class Registro(QMainWindow, Form):
    # Señales para los botones
    registro_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar los botones a las señales personalizadas
        self.BotonRegistro.clicked.connect(self.registro_clicked)
        self.BotonAtras.clicked.connect(self.volver_clicked)
