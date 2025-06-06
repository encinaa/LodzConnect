from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from datetime import datetime


class ControladorEventoAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)

        self._vista.anadir_evento_clicked.connect(self.on_anadir_evento_clicked)
        self._vista.eliminar_evento_solicitado.connect(self.eliminar_evento)
        self.mostrar_eventos()

    def on_anadir_evento_clicked(self):
        datos = self._vista.obtener_datos_evento()
        exito, mensaje = self.logica.registrar_evento(*datos[:-1], self.correo_usuario)

        if exito:
            self._vista.mostrar_mensaje_exito(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

    def eliminar_evento(self, id_evento, nombre_evento):
        confirmacion = self._vista.pedir_confirmacion_eliminacion(nombre_evento)
        if confirmacion:
            exito = self.evento_dao.eliminar_evento(id_evento)
            exito, mensaje = self.logica.eliminar_evento_y_notificar(id_evento, nombre_evento)
            if exito:
                self._vista.mostrar_mensaje_exito(mensaje)
                self.mostrar_eventos()
            else:
                self._vista.mostrar_mensaje_error("No se pudo eliminar el evento.")

    def mostrar_eventos(self):
        eventos = self.evento_dao.obtener_todos_eventos()
        eventos_ordenados = sorted(eventos, key=lambda e: (
            datetime.strptime(e.fecha, "%Y-%m-%d").date(),
            datetime.strptime(e.hora, "%H:%M:%S").time()
        ))

        self._vista.mostrar_eventos(eventos_ordenados)