from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

# Cargar la interfaz generada desde el archivo .ui
Form, Window = uic.loadUiType("./src/vista/Ui/IniciarSesion2.ui")

class Login(QMainWindow, Form):
    # Señales para los botones
    aceptar_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()
    recuperar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)  # Inicializa los widgets

        # Conectar los botones a las señales personalizadas
        self.BotonAceptar.clicked.connect(self.aceptar_clicked)
        self.BotonVolver.clicked.connect(self.volver_clicked)
        self.BotonRecuperar.clicked.connect(self.recuperar_clicked)
