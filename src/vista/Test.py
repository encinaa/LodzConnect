from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox
from src.vista.VistaNavegable import VistaNavegable
from src.modelo.dao.TestDAO import TestDAO

Form, _ = uic.loadUiType("./src/vista/Ui/Test.ui")

class Test(VistaNavegable, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        self.test_dao = TestDAO()
        self.test_actual = None

        # Cargar última pregunta
        self.cargar_ultimo_test()

        # Conectar botón
        self.BotonGuardarMiRespuesta.clicked.connect(self.guardar_respuestas)

    def cargar_ultimo_test(self):
        self.test_actual = self.test_dao.obtener_ultimo_test()
        if self.test_actual:
            self.campoPregunta1.setText(self.test_actual.pregunta1)
            self.campoPregunta2.setText(self.test_actual.pregunta2)
        else:
            self.campoPregunta1.setText("No hay tests disponibles.")
            self.campoPregunta2.setText("")

    def guardar_respuestas(self):
        if not self.test_actual:
            QMessageBox.warning(self, "Error", "No hay test cargado.")
            return

        nueva_respuesta1 = self.campoRespuesta1.toPlainText().strip()
        nueva_respuesta2 = self.campoRespuesta2.toPlainText().strip()

        if not nueva_respuesta1 or not nueva_respuesta2:
            QMessageBox.warning(self, "Campos vacíos", "Debes escribir ambas respuestas.")
            return

        # Obtener las respuestas anteriores (pueden ser None si aún no hay)
        respuestas1 = self.test_actual.respuestas1.split(",") if self.test_actual.respuestas1 else []
        respuestas2 = self.test_actual.respuestas2.split(",") if self.test_actual.respuestas2 else []

        # Agregar las nuevas
        respuestas1.append(nueva_respuesta1)
        respuestas2.append(nueva_respuesta2)

        # Guardar en la base de datos
        self.test_dao.guardar_respuestas(self.test_actual.idTest, respuestas1, respuestas2)

        QMessageBox.information(self, "Guardado", "Respuestas guardadas correctamente.")

        # Limpiar los campos de entrada
        self.campoRespuesta1.clear()
        self.campoRespuesta2.clear()

        # Actualizar los datos en el objeto en memoria
        self.test_actual.respuestas1 = ",".join(respuestas1)
        self.test_actual.respuestas2 = ",".join(respuestas2)



