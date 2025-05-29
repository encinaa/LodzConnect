# clase padre
from abc import ABC
from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.UsuarioDAO import UsuarioDAO

class ControladorBaseNavegable(ABC):
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        self._vista.mi_perfil_clicked.connect(self.abrir_miperfil)
        self._vista.cerrar_sesion_clicked.connect(self.cerrar_sesion)
        self._vista.test_clicked.connect(self.abrir_test)
        self._vista.publicacion_clicked.connect(self.abrir_publicacion)
        self._vista.eventos_clicked.connect(self.abrir_eventos)
        self._vista.tablon_clicked.connect(self.abrir_tablon)

        self.ventana_miperfil = None
        self.ventana_test = None
        self.ventana_publicacion = None
        self.ventana_eventos = None
        self.ventana_tablon = None
        self.ventana_principal = None

    def abrir_miperfil(self):
        from src.vista.MiPerfil import MiPerfil
        from src.controlador.ControladorMiPerfil import ControladorMiPerfil
        self.ventana_miperfil = MiPerfil()
        ControladorMiPerfil(self.ventana_miperfil, self.correo_usuario)
        self.ventana_miperfil.show()
        self._vista.hide()

    def abrir_test(self):
        from src.vista.Test import Test
        from src.controlador.ControladorTest import ControladorTest
        self.ventana_test = Test()
        ControladorTest(self.ventana_test, self.correo_usuario)
        self.ventana_test.show()
        self._vista.hide()

    def abrir_publicacion(self):
        from src.vista.PublicacionPopup import PublicacionPopup
        from src.controlador.ControladorPopupPublicacion import ControladorPopupPublicacion
        popup = PublicacionPopup()
        ControladorPopupPublicacion(popup, self.correo_usuario)
        popup.exec_()

    def abrir_eventos(self):
        from src.vista.Eventos import Eventos
        from src.controlador.ControladorEventos import ControladorEventos
        self.ventana_eventos = Eventos()
        ControladorEventos(self.ventana_eventos, self.correo_usuario)
        self.ventana_eventos.show()
        self._vista.hide()

    def abrir_tablon(self):
        from src.vista.Tablon import Tablon
        from src.controlador.ControladorTablon import ControladorTablon
        self.ventana_tablon = Tablon()
        ControladorTablon(self.ventana_tablon, self.correo_usuario)
        self.ventana_tablon.show()
        self._vista.hide()

    def cerrar_sesion(self):
        from src.vista.PáginaPrincipal import PáginaPrincipal
        from src.controlador.ControladorPaginaPrincipal import ControladorPaginaPrincipal

        confirmacion = QMessageBox.question(
            self._vista,
            "Cerrar sesión",
            "¿Estás seguro de que deseas cerrar sesión?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if confirmacion == QMessageBox.Yes:
            self.ventana_principal = PáginaPrincipal()
            ControladorPaginaPrincipal(self.ventana_principal)
            self.ventana_principal.show()
            self._vista.close()
