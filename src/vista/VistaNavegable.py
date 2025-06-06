# ESTA ES LA PADRE DE TODA LA COLUMNA DE LA IZQDA EN TABLON DEL ESTUDIANTE (esq pa copiar codigo heredamos mejor)
from PyQt5.QtWidgets import QMainWindow, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSignal

class VistaNavegable(QMainWindow):
    # todos los botones s ellaman igual asiq
    mi_perfil_clicked = pyqtSignal()
    cerrar_sesion_clicked = pyqtSignal()
    test_clicked = pyqtSignal()
    publicacion_clicked = pyqtSignal()
    eventos_clicked = pyqtSignal()
    tablon_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

    def conectar_botones_navegacion(self):
        botones = {
            "BotonMiPerfil": self.mi_perfil_clicked,
            "BotonCerrarSesion": self.cerrar_sesion_clicked,
            "BotonTest": self.test_clicked,
            "BotonPublicacion": self.publicacion_clicked,
            "BotonEventos": self.eventos_clicked,
            "BotonTablon": self.tablon_clicked,
        }

        for nombre_boton, señal in botones.items():
            boton = self.findChild(QPushButton, nombre_boton)
            if boton:
                boton.clicked.connect(señal)

    def confirmar_cierre_sesion(self):
        respuesta = QMessageBox.question(
            self,
            "Cerrar sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        return respuesta == QMessageBox.Yes
