from PyQt5.QtCore import QDate, QTime
from src.modelo.vo.EventoVO import EventoVO
import re
from datetime import datetime

class EventoLogica:
    def __init__(self, estudiante_dao):
        self.estudiante_dao = estudiante_dao

    def registrar_evento(self, nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin):
        # Validaciones básicas
        if not nombre.strip() or not descripcion.strip() or not ubicacion.strip():
            return False, "Todos los campos de texto deben estar completos."

        if not isinstance(fecha, QDate) or not fecha.isValid():
            return False, "Fecha inválida."

        if not isinstance(hora, QTime) or not hora.isValid():
            return False, "Hora inválida."

        if aforo <= 0:
            return False, "El aforo debe ser mayor que cero."

  
        # Convertir QDate y QTime a string
        fecha_str = fecha.toString("yyyy-MM-dd")
        hora_str = hora.toString("HH:mm:ss")

        # Crear objeto VO del evento
        evento = EventoVO(
            idEve=None,  
            nombre=nombre.strip(),
            descripcion=descripcion.strip(),
            fecha=fecha_str,
            hora=hora_str,
            ubicacion=ubicacion.strip(),
            aforoMax=aforo,
            correo_admin=correo_admin.strip()
        )

        # Insertar evento en la BD
        self.estudiante_dao.insertar_evento(evento)
        return True, "Evento registrado correctamente."

