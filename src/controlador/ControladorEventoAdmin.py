from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from datetime import datetime
from PyQt5.QtCore import QDate, QTime

class ControladorEventoAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)

        self._vista.anadir_evento_clicked.connect(self.on_anadir_evento_clicked)
        self._vista.eliminar_evento_solicitado.connect(self.eliminar_evento)
        self._vista.modificar_evento_solicitado.connect(self.preparar_modificacion_evento)

        self.id_evento_a_modificar = None  # Para saber si estamos modificando

        self.mostrar_eventos()

    def on_anadir_evento_clicked(self):
        datos = self._vista.obtener_datos_evento()

        # Convertir QDate y QTime si es necesario
        fecha = datos[2]
        hora = datos[3]
        if isinstance(fecha, QDate):
            fecha = fecha.toString("yyyy-MM-dd")
        if isinstance(hora, QTime):
            hora = hora.toString("HH:mm:ss")

        # Construir nueva tupla con los datos corregidos
        datos_convertidos = (
            datos[0],  # nombre
            datos[1],  # descripcion
            fecha,
            hora,
            datos[4],  # ubicacion
            datos[5]   # aforoMax
        )

        if self.id_evento_a_modificar is None:
            # Alta normal
            exito, mensaje = self.logica.registrar_evento(*datos_convertidos, self.correo_usuario)
        else:
            # Modificación
            exito, mensaje = self.logica.modificar_evento(
                self.id_evento_a_modificar,
                *datos_convertidos,
                self.correo_usuario
            )

        if exito:
            self._vista.mostrar_mensaje_exito(mensaje)
            self.id_evento_a_modificar = None  # Limpiar modo edición
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)



    def eliminar_evento(self, id_evento, nombre_evento):
        confirmacion = self._vista.pedir_confirmacion_eliminacion(nombre_evento)
        if confirmacion:
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

    def preparar_modificacion_evento(self, evento):
        """Este slot se activa al pulsar el botón de 'Modificar' en la vista"""
        self.id_evento_a_modificar = evento.idEve
        self._vista.rellenar_campos_evento(evento)
