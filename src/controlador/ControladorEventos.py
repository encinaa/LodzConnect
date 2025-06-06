from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from datetime import datetime

class ControladorEventos(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)

        self._vista.apuntarse_solicitado.connect(self.apuntarse_evento)
        self._vista.desapuntarse_solicitado.connect(self.desapuntarse_evento)
        self.mostrar_eventos()

    def apuntarse_evento(self, evento):
        exito, mensaje = self.logica.apuntarse(evento)
        if exito:
            self._vista.mostrar_mensaje_info(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

    def desapuntarse_evento(self, evento):
        exito, mensaje = self.logica.desapuntarse(evento)
        if exito:
            self._vista.mostrar_mensaje_info(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

    def mostrar_eventos(self):
        eventos = self.evento_dao.obtener_todos_eventos()
        eventos_ordenados = sorted(eventos, key=lambda e: (
            datetime.strptime(e.fecha, "%Y-%m-%d").date(),
            datetime.strptime(e.hora, "%H:%M:%S").time()
        ))
        self._vista.mostrar_eventos(eventos_ordenados)

