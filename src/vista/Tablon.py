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

        # Buscar botones por nombre globalmente (sin depender de MenuLateral)
        self.boton_miperfil = self.findChild(QPushButton, "BotonMiPerfil")
        self.boton_cerrarsesion = self.findChild(QPushButton, "BotonCerrarSesion")
        self.boton_test = self.findChild(QPushButton, "BotonTest")
        self.boton_publicacion = self.findChild(QPushButton, "BotonPublicacion")
        self.boton_eventos = self.findChild(QPushButton, "BotonEventos")
        self.boton_tablon = self.findChild(QPushButton, "BotonTablon")

        # Conectar botones a señales personalizadas
        if self.boton_miperfil:
            self.boton_miperfil.clicked.connect(self.mi_perfil_clicked)

        if self.boton_cerrarsesion:
            print("✅ BotonCerrarSesion encontrado")  # Debug
            self.boton_cerrarsesion.clicked.connect(lambda: print("Botón cerrar sesión pulsado"))  # Debug
            self.boton_cerrarsesion.clicked.connect(self.cerrar_sesion_clicked)

        if self.boton_test:
            self.boton_test.clicked.connect(self.test_clicked)

        if self.boton_publicacion:
            self.boton_publicacion.clicked.connect(self.publicacion_clicked)

        if self.boton_eventos:
            self.boton_eventos.clicked.connect(self.eventos_clicked)

        if self.boton_tablon:
            self.boton_tablon.clicked.connect(self.tablon_clicked)
