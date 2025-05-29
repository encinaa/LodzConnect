# src/vista/Eventos.py
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/Test.ui")

class Test(VistaNavegable, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
