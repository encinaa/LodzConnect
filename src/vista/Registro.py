from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import uic
from PyQt5.QtCore import pyqtSignal

Form, Window = uic.loadUiType("./src/vista/Ui/Registro3.ui")

class Registro(QMainWindow, Form):
    registro_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.BotonRegistro.clicked.connect(self.registro_clicked)
        self.BotonAtras.clicked.connect(self.volver_clicked)

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        msg = QMessageBox(self)
        if tipo == "error":
            msg.setIcon(QMessageBox.Warning)
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
        elif tipo == "informacion":
            msg.setIcon(QMessageBox.Information)
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
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)
        msg.exec_()
