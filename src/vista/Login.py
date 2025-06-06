from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

Form, Window = uic.loadUiType("./src/vista/Ui/IniciarSesion2.ui")

class Login(QMainWindow, Form):
    aceptar_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()
    recuperar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self) 

        self.BotonAceptar.clicked.connect(self.aceptar_clicked)
        self.BotonVolver.clicked.connect(self.volver_clicked)
        self.BotonRecuperar.clicked.connect(self.recuperar_clicked)

    def mostrar_mensaje_advertencia(self, titulo, mensaje):
        msg = QMessageBox(self)
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

    def mostrar_mensaje_error(self, titulo, mensaje):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Critical)
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
