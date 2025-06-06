from src.modelo.vo.EventoVO import EventoVO
from PyQt5.QtCore import QDate, QTime
import re

class EventoLogica:
    def __init__(self, evento_dao):
        self.evento_dao = evento_dao

    def registrar_evento(self, nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin):
        nombre = nombre.strip()
        descripcion = descripcion.strip()
        ubicacion = ubicacion.strip()
        correo_admin = correo_admin.strip()

        if not nombre or not descripcion or not ubicacion:
            return False, "Todos los campos deben estar completos."

        if not re.match(r"[^@]+@[^@]+\.[^@]+", correo_admin):
            return False, "El correo del administrador no es válido."

        if not isinstance(fecha, QDate) or not fecha.isValid():
            return False, "La fecha no es válida."

        if fecha < QDate.currentDate():
            return False, "La fecha del evento no puede ser anterior a hoy."

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
