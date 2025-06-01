from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin
from src.modelo.GestionLogica import GestionLogica
from PyQt5 import uic

Form, _ = uic.loadUiType("./src/vista/Ui/Gestión.ui")

class GestionAdmin(VistaNavegableAdmin, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        self.logica = GestionLogica()

        # Conectar validación en tiempo real
        self.EmailAdmin.textChanged.connect(self.validar_admin_live)

        # Conectar botones
        self.BotonAnadirAdmin.clicked.connect(self.anadir_admin)
        self.BotonEliminarAdmin.clicked.connect(self.confirmar_eliminar_admin)


    def validar_admin_live(self):
        correo = self.EmailAdmin.text()
        if self.logica.validar_correo_admin(correo):
            self.colorear_line_edit(self.EmailAdmin, True)
        else:
            self.colorear_line_edit(self.EmailAdmin, False)

    def colorear_line_edit(self, line_edit, valido):
        palette = line_edit.palette()
        color = QColor("white") if valido else QColor(255, 200, 200)
        palette.setColor(QPalette.Base, color)
        line_edit.setPalette(palette)

    def anadir_admin(self):
        correo = self.EmailAdmin.text()
        ok, mensaje = self.logica.anadir_admin(correo)
        QMessageBox.information(self, "Resultado", mensaje)

    def confirmar_eliminar_admin(self):
        correo = self.EmailAdmin.text()
        if not self.logica.validar_correo_admin(correo):
            QMessageBox.warning(self, "Error", "Introduce un correo válido de administrador.")
            return
        respuesta = QMessageBox.question(self, "Confirmar eliminación",
                                         f"¿Estás seguro de que quieres eliminar al administrador {correo}?",
                                         QMessageBox.Yes | QMessageBox.No)
        if respuesta == QMessageBox.Yes:
            ok, mensaje = self.logica.eliminar_admin(correo)
            QMessageBox.information(self, "Resultado", mensaje)


