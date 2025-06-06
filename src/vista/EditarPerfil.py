from PyQt5.QtWidgets import QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/EditarPerfil2.ui")

class EditarPerfil(VistaNavegable, Form):
    guardar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
        self._conectar_botones_especificos()

    def _conectar_botones_especificos(self):
        boton_guardar = self.findChild(QPushButton, "BotonGuardarPerfil")
        if boton_guardar:
            boton_guardar.clicked.connect(self.guardar_clicked)

    # Métodos para obtener y mostrar datos
    def establecer_nombre(self, nombre):
        self.EditarUsuario.setText(nombre)

    def obtener_nombre(self):
        return self.EditarUsuario.text()

    def establecer_edad(self, edad):
        self.EditarEdad.setValue(edad)

    def obtener_edad(self):
        return self.EditarEdad.value()

    def establecer_descripcion(self, descripcion):
        self.EditarDescripcion.setPlainText(descripcion)

    def obtener_descripcion(self):
        return self.EditarDescripcion.toPlainText()

    def establecer_actividades(self, actividades):
        self.EditarActividades.setPlainText(actividades)

    def obtener_actividades(self):
        return self.EditarActividades.toPlainText()

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)