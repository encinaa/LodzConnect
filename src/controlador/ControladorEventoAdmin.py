# src/controlador/ControladorEventoAdmin.py
from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica

class ControladorEventoAdmin:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)
        self.vista_principal = None

        self._vista.anadir_evento_clicked.connect(self.on_anadir_evento_clicked)

    def set_pagina_principal(self, vista_principal):
        self.vista_principal = vista_principal

    def on_anadir_evento_clicked(self):
        nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin = self._vista.obtener_datos_evento()

        exito, mensaje = self.logica.registrar_evento(nombre, descripcion, fecha, hora, ubicacion, aforo, self.correo_usuario)

        if exito:
            self._vista.mostrar_mensaje_exito(mensaje)
            self._vista.limpiar_formulario()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

