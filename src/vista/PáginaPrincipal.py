from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/PáginaPrincipal2.ui")

class PáginaPrincipal(QMainWindow, Form):
    # Definimos señales que emitirán cuando se pulse un botón
    iniciar_clicked = pyqtSignal()
    registrarse_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar los botones a las señales personalizadas
        self.BotonIniciar.clicked.connect(self.iniciar_clicked)
        self.BotonRegistrarse.clicked.connect(self.registrarse_clicked)
