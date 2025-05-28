from PyQt5.QtWidgets import QMessageBox
from src.vista.MiPerfil import MiPerfil
from src.vista.PáginaPrincipal import PáginaPrincipal
from src.vista.Test import Test
from src.vista.Publicacion import Publicacion
from src.vista.Eventos import Eventos
from src.modelo.dao.UsuarioDAO import UsuarioDAO

class ControladorTablon:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        # Conectar señales personalizadas de la vista a los métodos
        self._vista.toggle_menu_clicked.connect(self.toggle_menu_lateral)
        self._vista.mi_perfil_clicked.connect(self.ir_a_miperfil)
        self._vista.cerrar_sesion_clicked.connect(self.cerrar_sesion)
        self._vista.test_clicked.connect(self.ir_a_test)
        self._vista.publicacion_clicked.connect(self.ir_a_publicacion)
        self._vista.eventos_clicked.connect(self.ir_a_eventos)

        # Mantener referencias a ventanas hijas
        self.ventana_miperfil = None
        self.ventana_principal = None
        self.ventana_test = None
        self.ventana_publicacion = None
        self.ventana_eventos = None

    def toggle_menu_lateral(self):
        visible = self._vista.MenuLateral.isVisible()
        self._vista.MenuLateral.setVisible(not visible)
        self._vista.MenuLateral.raise_()

    def ir_a_miperfil(self):
        self.ventana_miperfil = MiPerfil()
        self.ventana_miperfil.show()
        self._vista.hide()

    def ir_a_test(self):
        self.ventana_test = Test()
        self.ventana_test.show()
        self._vista.hide()

    def ir_a_publicacion(self):
        self.ventana_publicacion = Publicacion()
        self.ventana_publicacion.show()
        self._vista.hide()

    def ir_a_eventos(self):
        self.ventana_eventos = Eventos()
        self.ventana_eventos.show()
        self._vista.hide()

    def cerrar_sesion(self):
        confirmacion = QMessageBox.question(
            self._vista,
            "Cerrar sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            self.ventana_principal = PáginaPrincipal()
            self.ventana_principal.show()
            self._vista.close()
