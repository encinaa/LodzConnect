from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/MiPerfil2.ui")

class MiPerfil(VistaNavegable, Form):
    editar_perfil_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
        self._conectar_botones_especificos()

    def _conectar_botones_especificos(self):
        boton_editar = self.findChild(QPushButton, "BotonEditarPerfil")
        if boton_editar:
            boton_editar.clicked.connect(self.editar_perfil_clicked)

    def mostrar_nombre(self, nombre):
        self.label_Usuario.setText(nombre)

    def mostrar_edad(self, edad):
        self.label_Edad.setText(str(edad))

    def mostrar_descripcion(self, descripcion):
        self.label_Descripcion.setText(descripcion)
    """
    def mostrar_actividades(self, actividades):
        self.ListaActividades.setText(actividades)
    """
