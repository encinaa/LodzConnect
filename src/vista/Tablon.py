# src/vista/Tablon.py
from PyQt5.QtWidgets import QMainWindow, QPushButton
from PyQt5.QtCore import pyqtSignal
from PyQt5 import uic

Form, Window = uic.loadUiType("./src/vista/Ui/Tablón3.ui")

class Tablon(QMainWindow, Form):
    # Señales personalizadas
    mi_perfil_clicked = pyqtSignal()
    cerrar_sesion_clicked = pyqtSignal()
    test_clicked = pyqtSignal()
    publicacion_clicked = pyqtSignal()
    eventos_clicked = pyqtSignal()
    tablon_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Buscar botones por nombre dentro de MenuLateral
        boton_miperfil = self.findChild(QPushButton, "BotonMiPerfil")
        boton_cerrarsesion = self.findChild(QPushButton, "BotonCerrarSesion")
        boton_test = self.findChild(QPushButton, "BotonTest")
        boton_publicacion = self.findChild(QPushButton, "BotonPublicacion")
        boton_eventos = self.findChild(QPushButton, "BotonEventos")
        boton_tablon = self.findChild(QPushButton, "BotonTablon")

        # Conectar señales
        if boton_miperfil:
            boton_miperfil.clicked.connect(self.mi_perfil_clicked)
        if boton_cerrarsesion:
            boton_cerrarsesion.clicked.connect(self.cerrar_sesion_clicked)
        if boton_test:
            boton_test.clicked.connect(self.test_clicked)
        if boton_publicacion:
            boton_publicacion.clicked.connect(self.publicacion_clicked)
        if boton_eventos:
            boton_eventos.clicked.connect(self.eventos_clicked)
        if boton_tablon:
            boton_tablon.clicked.connect(self.tablon_clicked)
