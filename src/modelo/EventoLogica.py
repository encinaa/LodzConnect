from src.modelo.vo.EventoVO import EventoVO
from src.modelo.dao.EstudianteDAO import EstudianteDAO
from PyQt5.QtCore import QDate, QTime
import re
from src.utils.email_utils import enviar_correo

class EventoLogica:
    def __init__(self, evento_dao):
        self.evento_dao = evento_dao
        self.estudiante_dao = EstudianteDAO()

    def registrar_evento(self, nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin):
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        ubicacion = ubicacion.strip()
        correo_admin = correo_admin.strip()

        if not nombre or not descripcion or not ubicacion:
            return False, "Todos los campos deben estar completos."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo_admin):
            return False, "El correo del administrador no es válido."

        if isinstance(fecha, str):
            fecha = QDate.fromString(fecha, "yyyy-MM-dd")

        if not isinstance(fecha, QDate) or not fecha.isValid():
            return False, "La fecha no es válida."

        if fecha < QDate.currentDate():
            return False, "La fecha del evento no puede ser anterior a hoy."

        if isinstance(hora, str):
            hora = QTime.fromString(hora, "HH:mm:ss")

        if not isinstance(hora, QTime) or not hora.isValid():
            return False, "La hora no es válida."

        if aforo <= 0:
            return False, "El aforo debe ser mayor que cero."

        evento = EventoVO(
            idEve=None,
            nombre=nombre,
            descripcion=descripcion,
            fecha=fecha.toString("yyyy-MM-dd"),
            hora=hora.toString("HH:mm:ss"),
            ubicacion=ubicacion,
            aforoMax=aforo,
            aforoActual=0,
            correo_admin=correo_admin
        )

        self.evento_dao.insertar_evento(evento)

        # Preparar asunto y cuerpo (puedes usar el que ya tienes)
        asunto = f"Nuevo evento registrado: {nombre}"
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Nuevo evento en UniConecta</h2>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Descripción:</strong> {descripcion}</p>
            <p><strong>Fecha:</strong> {fecha.toString("dd/MM/yyyy")}</p>
            <p><strong>Hora:</strong> {hora.toString("HH:mm")}</p>
            <p><strong>Ubicación:</strong> {ubicacion}</p>
            <p><strong>Aforo máximo:</strong> {aforo}</p>
            <br>
            <p>¡No te lo pierdas!</p>
        </body>
        </html>
        """

        # Obtener todos los estudiantes hice funcion nueva un poco rara pero funciona
        estudiantes = self.estudiante_dao.obtener_todos() 

        for estudiante in estudiantes:
            try:
                enviar_correo(estudiante.correo, asunto, cuerpo)
            except Exception as e:
                print(f"Error enviando correo a {estudiante.correo}: {e}")


        return True, "Evento registrado correctamente."


    def apuntarse(self, evento):
        if evento.aforoActual >= evento.aforoMax:
            return False, "El evento ya está lleno."

        nuevo_aforo = evento.aforoActual + 1
        exito = self.evento_dao.actualizar_aforo(evento.idEve, nuevo_aforo)

        if exito:
            evento.aforoActual = nuevo_aforo  # actualizar también en el objeto
            return True, "Te has apuntado correctamente al evento."
        else:
            return False, "No se pudo completar la inscripción al evento."

    def desapuntarse(self, evento):
        if evento.aforoActual <= 0:
            return False, "No hay inscritos que eliminar."

        nuevo_aforo = evento.aforoActual - 1
        exito = self.evento_dao.actualizar_aforo(evento.idEve, nuevo_aforo)

        if exito:
            evento.aforoActual = nuevo_aforo
            return True, "Te has desapuntado correctamente del evento."
        else:
            return False, "No se pudo cancelar tu inscripción al evento."


    def eliminar_evento_y_notificar(self, id_evento, nombre_evento):
        exito = self.evento_dao.eliminar_evento(id_evento)
        if not exito:
            return False, "No se pudo eliminar el evento."

        asunto = f"Evento eliminado: {nombre_evento}"
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Evento eliminado en UniConecta</h2>
            <p>El evento <strong>{nombre_evento}</strong> ha sido cancelado.</p>
            <p>Disculpa las molestias.</p>
        </body>
        </html>
        """

        estudiantes = self.estudiante_dao.obtener_todos()
        for estudiante in estudiantes:
            try:
                enviar_correo(estudiante.correo, asunto, cuerpo)
            except Exception as e:
                print(f"Error enviando correo a {estudiante.correo}: {e}")

        return True, "Evento eliminado y notificaciones enviadas."


    def modificar_evento(self, id_evento, nombre, descripcion, fecha, hora, ubicacion, aforo_max, correo_admin):
        exito = self.evento_dao.modificar_evento(id_evento, nombre, descripcion, fecha, hora, ubicacion, aforo_max, correo_admin)

        if not exito:
            return False, "No se pudo modificar el evento."

        # Preparar asunto y cuerpo del correo
        asunto = f"Evento modificado: {nombre}"
        cuerpo = f"""
        <html>
        <body style="font-family: Arial, sans-serif;">
            <h2>Evento actualizado en UniConecta</h2>
            <p><strong>Nombre:</strong> {nombre}</p>
            <p><strong>Descripción:</strong> {descripcion}</p>
            <p><strong>Fecha:</strong> {QDate.fromString(fecha, "yyyy-MM-dd").toString("dd/MM/yyyy")}</p>
            <p><strong>Hora:</strong> {hora[:5]}</p>
            <p><strong>Ubicación:</strong> {ubicacion}</p>
            <p><strong>Aforo máximo:</strong> {aforo_max}</p>
            <br>
            <p>¡Revisa los detalles del evento actualizado!</p>
        </body>
        </html>
        """

        estudiantes = self.estudiante_dao.obtener_todos()
        for estudiante in estudiantes:
            try:
                enviar_correo(estudiante.correo, asunto, cuerpo)
            except Exception as e:
                print(f"Error enviando correo a {estudiante.correo}: {e}")

        return True, "Evento actualizado y notificaciones enviadas."
