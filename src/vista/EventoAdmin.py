from PyQt5 import uic
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMessageBox

Form, _ = uic.loadUiType("./src/vista/Ui/EventoAdmin.ui")

class EventoAdmin(VistaNavegableAdmin, Form):
    anadir_evento_clicked = pyqtSignal()  # Señal para el botón

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        # Conectar el click del botón a emitir la señal
        self.BotonAnadirEvento.clicked.connect(self.anadir_evento_clicked)

    # Métodos para obtener datos del formulario
    def obtener_datos_evento(self):
        nombre = self.NombreEvento.toPlainText()
        descripcion = self.DescripcionEvento.toPlainText()
        fecha = self.FechaEvento.date()
        hora = self.HoraEvento.time()
        ubicacion = self.UbicacionEvento.toPlainText()
        aforo = self.AforoMax.value()
        correo_admin = self.CorreoAdmin.text() if hasattr(self, "CorreoAdmin") else ""
        return nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin

    # Métodos para mostrar mensajes
    def mostrar_mensaje_exito(self, mensaje):
        QMessageBox.information(self, "Éxito", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    def limpiar_formulario(self):
        self.NombreEvento.clear()
        self.DescripcionEvento.clear()
        self.FechaEvento.setDate(self.FechaEvento.minimumDate())
        self.HoraEvento.setTime(self.HoraEvento.minimumTime())
        self.UbicacionEvento.clear()
        self.AforoMax.setValue(0)
        if hasattr(self, "CorreoAdmin"):
            self.CorreoAdmin.clear()
