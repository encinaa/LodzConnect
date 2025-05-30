from PyQt5 import uic
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin

Form, _ = uic.loadUiType("./src/vista/Ui/EventoAdmin.ui")

class EventoAdmin(VistaNavegableAdmin, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
