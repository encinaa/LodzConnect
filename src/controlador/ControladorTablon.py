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

        # Al pulsar el botón ☰ mostramos/ocultamos menú lateral
        self._vista.BotonMenu.clicked.connect(self.toggle_menu_lateral)

        # Conectar botones del menú lateral a sus funciones
        self._vista.MenuLateral.BotonMiPerfil.clicked.connect(self.ir_a_miperfil)
        self._vista.MenuLateral.BotonCerrarSesion.clicked.connect(self.cerrar_sesion)
        self._vista.MenuLateral.BotonTest.clicked.connect(self.ir_a_test)
        self._vista.MenuLateral.BotonPublicacion.clicked.connect(self.ir_a_publicacion)
        self._vista.MenuLateral.BotonEventos.clicked.connect(self.ir_a_eventos)

        # Mantener referencias para evitar que las ventanas se destruyan
        self.ventana_miperfil = None
        self.ventana_principal = None
        self.ventana_test = None
        self.ventana_publicacion = None
        self.ventana_eventos = None

    def toggle_menu_lateral(self):
        print("Toggle menu activado")
        visible = self._vista.MenuLateral.isVisible()
        self._vista.MenuLateral.setVisible(not visible)
        self._vista.MenuLateral.raise_()

    def ir_a_miperfil(self):
        print("Ir a Mi Perfil")
        self.ventana_miperfil = MiPerfil()
        # Si quieres pasar el correo_usuario o algo similar, aquí puedes
        self.ventana_miperfil.show()
        self._vista.hide()

    def ir_a_test(self):
        print("Ir a Test")
        self.ventana_test = Test()
        self.ventana_test.show()
        self._vista.hide()

    def ir_a_publicacion(self):
        print("Ir a Publicacion")
        self.ventana_publicacion = Publicacion()
        self.ventana_publicacion.show()
        self._vista.hide()

    def ir_a_eventos(self):
        print("Ir a Eventos")
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
            print("Cerrar sesión confirmada")
            self.ventana_principal = PáginaPrincipal()
            self.ventana_principal.show()
            self._vista.close()
