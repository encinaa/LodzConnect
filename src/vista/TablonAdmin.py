from PyQt5 import uic
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtSignal

Form, _ = uic.loadUiType("./src/vista/Ui/TablónAdmin.ui")

class TablonAdmin(VistaNavegableAdmin, Form):
    actualizar_publicaciones_clicked = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()


        boton_actualizar = self.findChild(QPushButton, "BotonActualizar")
        if boton_actualizar:
            boton_actualizar.clicked.connect(self.actualizar_publicaciones_clicked)
