# src/controlador/ControladorEventoAdmin.py
from PyQt5.QtWidgets import QApplication
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.vista.Eventos import Eventos
from src.controlador.ControladorEventos import ControladorEventos

class ControladorEventoAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)

        self._vista.anadir_evento_clicked.connect(self.on_anadir_evento_clicked)

    def on_anadir_evento_clicked(self):
        nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin = self._vista.obtener_datos_evento()

        exito, mensaje = self.logica.registrar_evento(nombre, descripcion, fecha, hora, ubicacion, aforo, self.correo_usuario)

        if exito:
            self._vista.mostrar_mensaje_exito(mensaje)
            self.abrir_eventos()

        else:
            self._vista.mostrar_mensaje_error(mensaje)

