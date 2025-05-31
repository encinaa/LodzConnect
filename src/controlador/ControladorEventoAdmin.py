from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.EventoLogica import EventoLogica
from PyQt5.QtCore import QDate, QTime

class ControladorEventoAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario, estudiante_dao):
        super().__init__(vista, correo_usuario)
        self.vista = vista
        self.correo_usuario = correo_usuario

        # Instancia la lógica del evento
        self.logica_evento = EventoLogica(estudiante_dao)

        # Conectar la señal del botón "Añadir Evento" con el método manejador
        self.vista.conectar_boton_anadir_evento(self.anadir_evento)

    def anadir_evento(self):
        # Obtener datos de la vista
        nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin = self.vista.obtener_datos_evento()

        # Validar y registrar evento usando la lógica
        exito, mensaje = self.logica_evento.registrar_evento(
            nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin or self.correo_usuario
        )

        # Mostrar mensajes según el resultado
        if exito:
            self.vista.mostrar_mensaje_exito(mensaje)
            self.vista.limpiar_formulario()
        else:
            self.vista.mostrar_mensaje_error(mensaje)
