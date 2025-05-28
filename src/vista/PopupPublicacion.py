# src/vista/PopupPublicacion.py
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton
from PyQt5.QtCore import pyqtSignal

class PopupPublicacion(QDialog):
    publicar_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nueva Publicación")
        self.setFixedSize(400, 300)

        layout = QVBoxLayout()

        self.texto_publicacion = QTextEdit()
        self.boton_publicar = QPushButton("Publicar")
        self.boton_volver = QPushButton("Volver")

        layout.addWidget(self.texto_publicacion)
        layout.addWidget(self.boton_publicar)
        layout.addWidget(self.boton_volver)
        self.setLayout(layout)

        # Conectar botones a señales
        self.boton_publicar.clicked.connect(self.publicar_clicked.emit)
        self.boton_volver.clicked.connect(self.volver_clicked.emit)

    def get_texto_publicacion(self):
        return self.texto_publicacion.toPlainText()
