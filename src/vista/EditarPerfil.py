# src/vista/EditarPerfil.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/EditarPerfil.ui")  # Asegúrate de que el archivo .ui se llama así

class EditarPerfil(QMainWindow, Form):
    # Señales personalizadas
    guardar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar el botón de guardar a la señal personalizada
        self.BotonGuardarPerfil.clicked.connect(self.guardar_clicked)
