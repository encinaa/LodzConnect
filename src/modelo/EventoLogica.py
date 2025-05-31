# src/modelo/EventoLogica.py
from src.modelo.vo.EventoVO import EventoVO
from PyQt5.QtCore import QDate, QTime
import re

class EventoLogica:
    def __init__(self, evento_dao):
        self.evento_dao = evento_dao

    def registrar_evento(self, nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin):
        if not nombre.strip() or not descripcion.strip() or not ubicacion.strip():
            return False, "Todos los campos deben estar completos."

        if not isinstance(fecha, QDate) or not fecha.isValid():
            return False, "La fecha no es válida."

        # Validación de fecha pasada
        hoy = QDate.currentDate()
        if fecha < hoy:
            return False, "La fecha del evento no puede ser anterior a hoy."


        if not isinstance(hora, QTime) or not hora.isValid():
            return False, "La hora no es válida."

        if aforo <= 0:
            return False, "El aforo debe ser mayor que cero."

        evento = EventoVO(
            idEve=None,
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha=fecha.toString("yyyy-MM-dd"),
            hora=hora.toString("HH:mm:ss"),
            ubicacion=ubicacion.strip(),
            aforoMax=aforo,
            correo_admin=correo_admin.strip()
        )

        self.evento_dao.insertar_evento(evento)
        return True, "Evento registrado correctamente."
