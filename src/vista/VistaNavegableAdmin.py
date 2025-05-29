from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import pyqtSignal

class VistaNavegableAdmin(QMainWindow):
    tablon_clicked = pyqtSignal()
    eventos_clicked = pyqtSignal()
    gestion_clicked = pyqtSignal()
    test_clicked = pyqtSignal()
    cerrar_sesion_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

    def conectar_botones_navegacion(self):
        botones = {
            "BotonTablon": self.tablon_clicked,
            "BotonAnadirEventos": self.eventos_clicked,
            "BotonGestion": self.gestion_clicked,
            "BotonCrearTest": self.test_clicked,
            "BotonCerrarSesion": self.cerrar_sesion_clicked,
        }

        for nombre_boton, señal in botones.items():
            boton = self.findChild(QPushButton, nombre_boton)
            if boton:
                boton.clicked.connect(señal)
