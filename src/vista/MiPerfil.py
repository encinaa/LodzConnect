# src/vista/MiPerfil.py
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

Form, Window = uic.loadUiType("./src/vista/Ui/MiPerfil2.ui")  # Asegúrate del nombre correcto del archivo

class MiPerfil(QMainWindow, Form):
    # Señales personalizadas para comunicación con el controlador
    volver_clicked = pyqtSignal()
    editar_perfil_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Conectar botones a señales personalizadas
        self.BotonTablon.clicked.connect(self.volver_clicked)
        self.BotonEditarPerfil.clicked.connect(self.editar_perfil_clicked)

        # A partir de aquí, puedes acceder a widgets como:
        # self.Usuario, self.Edad, self.Descripcion, self.ListaActividades
