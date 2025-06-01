from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QVBoxLayout, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from src.modelo.vo.TestVO import TestVO
from src.modelo.dao.TestDAO import TestDAO

class CrearTestPopup(QDialog):
    def __init__(self, correo_admin, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Crear Nuevo Test")
        self.setFixedSize(400, 250)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        self.correo_admin = correo_admin
        self.test_dao = TestDAO()

        self.pregunta1_input = QLineEdit(self)
        self.pregunta2_input = QLineEdit(self)
        self.boton_guardar = QPushButton("Guardar", self)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Pregunta 1:"))
        layout.addWidget(self.pregunta1_input)
        layout.addWidget(QLabel("Pregunta 2:"))
        layout.addWidget(self.pregunta2_input)
        layout.addWidget(self.boton_guardar)
        self.setLayout(layout)

        self.boton_guardar.clicked.connect(self.guardar_test)

    def guardar_test(self):
        pregunta1 = self.pregunta1_input.text().strip()
        pregunta2 = self.pregunta2_input.text().strip()

        if not pregunta1 or not pregunta2:
            QMessageBox.warning(self, "Error", "Ambas preguntas deben ser rellenadas.")
            return

        nuevo_test = TestVO(
            idTest=None,
            correo_admin=self.correo_admin,
            pregunta1=pregunta1,
            pregunta2=pregunta2,
            respuestas1="[]",  # '??????
            respuestas2="[]"
        )

        self.test_dao.insertar_test(nuevo_test)
        QMessageBox.information(self, "Éxito", "Test guardado correctamente.")
        self.accept()
