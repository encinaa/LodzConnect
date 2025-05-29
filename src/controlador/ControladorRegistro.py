
from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.modelo.dao.EstudianteDAO import EstudianteDAO
from src.modelo.RegistroLogica import RegistroLogica

class ControladorRegistro:
    def __init__(self, vista):
        self._vista = vista
        self.usuario_dao = UsuarioDAO()
        self.estudiante_dao = EstudianteDAO()
        self.logica = RegistroLogica(self.usuario_dao, self.estudiante_dao)
        self.vista_principal = None

        self._vista.registro_clicked.connect(self.on_register_clicked)
        self._vista.volver_clicked.connect(self.on_volver_clicked)

    def set_pagina_principal(self, vista_principal):
        self.vista_principal = vista_principal

    def on_register_clicked(self):
        correo = self._vista.registro_correo.text()
        contraseña = self._vista.registro_contrasena.text()
        confirmar = self._vista.registro_confirmContrasena.text()
        nombre = self._vista.registro_nombre.text()
        edad = self._vista.registro_edad.text()

        exito, mensaje = self.logica.registrar_usuario(correo, contraseña, confirmar, nombre, edad)

        if exito:
            self.mostrar_mensaje_info("Registro exitoso", mensaje)
            if self.vista_principal:
                self.vista_principal.show()
            self._vista.close()
        else:
            self.mostrar_mensaje_error("Error de registro", mensaje)

    def on_volver_clicked(self):
        if self.vista_principal is not None:
            self.vista_principal.show()
        self._vista.close()

    def mostrar_mensaje_error(self, titulo, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 13px;
            }
            QPushButton {
                background-color: #d32f2f;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #b71c1c;
            }
        """)
        msg.exec_()

    def mostrar_mensaje_info(self, titulo, mensaje):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.setStyleSheet("""
            QMessageBox {
                background-color: white;
            }
            QLabel {
                color: black;
                font-size: 13px;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
                padding: 5px 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0d47a1;
            }
        """)
        msg.exec_()
