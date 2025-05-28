from PyQt5.QtWidgets import QMessageBox
from src.vista.MiPerfil import MiPerfil
from src.vista.PáginaPrincipal import PáginaPrincipal
from src.vista.Test import Test
from src.vista.Publicacion import Publicacion
from src.vista.Eventos import Eventos
from src.controlador.ControladorMiPerfil import ControladorMiPerfil
from src.controlador.ControladorTest import ControladorTest
from src.controlador.ControladorPublicacion import ControladorPublicacion
from src.controlador.ControladorEventos import ControladorEventos
from src.modelo.dao.UsuarioDAO import UsuarioDAO




class ControladorTablon:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        # Conectar señales de la vista
        self._vista.mi_perfil_clicked.connect(self.abrir_miperfil)
        self._vista.cerrar_sesion_clicked.connect(self.cerrar_sesion)
        self._vista.test_clicked.connect(self.abrir_test)
        self._vista.publicacion_clicked.connect(self.abrir_publicacion)
        self._vista.eventos_clicked.connect(self.abrir_eventos)

        # Mantener referencias a ventanas hijas
        self.ventana_miperfil = None
        self.ventana_test = None
        self.ventana_publicacion = None
        self.ventana_eventos = None
        self.ventana_principal = None

    def abrir_miperfil(self):
        self.ventana_miperfil = MiPerfil()
        self.controlador_miperfil = ControladorMiPerfil(self.ventana_miperfil, self.correo_usuario)
        self.controlador_miperfil.set_vista_anterior(self._vista)
        self.ventana_miperfil.show()
        self._vista.hide()

    def abrir_test(self):
        self.ventana_test = Test()
        self.controlador_test = ControladorTest(self.ventana_test, self.correo_usuario)
        self.controlador_test.set_vista_anterior(self._vista)
        self.ventana_test.show()
        self._vista.hide()

    def abrir_publicacion(self):
        self.ventana_publicacion = Publicacion()
        self.controlador_publicacion = ControladorPublicacion(self.ventana_publicacion, self.correo_usuario)
        self.controlador_publicacion.set_vista_anterior(self._vista)
        self.ventana_publicacion.show()
        self._vista.hide()

    def abrir_eventos(self):
        self.ventana_eventos = Eventos()
        self.controlador_eventos = ControladorEventos(self.ventana_eventos, self.correo_usuario)
        self.controlador_eventos.set_vista_anterior(self._vista)
        self.ventana_eventos.show()
        self._vista.hide()

    def cerrar_sesion(self):
        print("Método cerrar_sesion() llamado")
        confirmacion = QMessageBox.question(
            self._vista,
            "Cerrar sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        if confirmacion == QMessageBox.Yes:
            print("Usuario confirmó cierre de sesión")

            from src.controlador.ControladorPaginaPrincipal import ControladorPaginaPrincipal


            self.ventana_principal = PáginaPrincipal()
            self.controlador_principal = ControladorPaginaPrincipal(self.ventana_principal)
            self.ventana_principal.show()
            self._vista.close()
        else:
            print("Usuario canceló cierre de sesión")


