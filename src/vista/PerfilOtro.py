from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/PerfilOtro.ui")  # UI diferente

class PerfilOtro(VistaNavegable, Form):
    volver_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
        self._conectar_boton_volver()

    def _conectar_boton_volver(self):
        boton_volver = self.findChild(QPushButton, "BotonVolver")
        if boton_volver:
            boton_volver.clicked.connect(self.volver_clicked)

    def mostrar_nombre(self, nombre):
        self.label_Usuario.setText(nombre)

    def mostrar_edad(self, edad):
        self.label_Edad.setText(str(edad))

    def mostrar_descripcion(self, descripcion):
        self.label_Descripcion.setText(descripcion)

    def mostrar_actividades(self, actividades):
        self.ListaActividades.setText(actividades)
