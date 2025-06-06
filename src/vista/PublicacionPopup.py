from PyQt5.QtWidgets import QDialog, QTextEdit, QPushButton, QVBoxLayout, QMessageBox
from PyQt5.QtCore import Qt

class PublicacionPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Nueva Publicación")
        self.setFixedSize(400, 300)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.texto = QTextEdit(self)
        self.boton_publicar = QPushButton("Publicar", self)

        layout = QVBoxLayout()
        layout.addWidget(self.texto)
        layout.addWidget(self.boton_publicar)
        self.setLayout(layout)

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        if tipo == "error":
            QMessageBox.warning(self, titulo, mensaje)
        elif tipo == "informacion":
            QMessageBox.information(self, titulo, mensaje)
