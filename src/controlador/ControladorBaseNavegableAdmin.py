from abc import ABC
from PyQt5.QtWidgets import QMessageBox
from src.modelo.dao.UsuarioDAO import UsuarioDAO

class ControladorBaseNavegableAdmin(ABC):
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        # Para guardar referencias
        self._controladores = {}

        # Conectar señales de botones del admin
        self._vista.tablon_clicked.connect(self.abrir_tablon)
        self._vista.eventos_clicked.connect(self.abrir_eventos)
        self._vista.gestion_clicked.connect(self.abrir_gestion)
        self._vista.test_clicked.connect(self.abrir_test)
        self._vista.cerrar_sesion_clicked.connect(self.cerrar_sesion)

    def abrir_tablon(self):
        from src.vista.TablonAdmin import TablonAdmin
        from src.controlador.ControladorTablonAdmin import ControladorTablonAdmin
        vista = TablonAdmin()
        self._controladores["tablon_admin"] = ControladorTablonAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()

    def abrir_eventos(self):
        pass
        #OTRO POPUP?
        """
        from src.vista.EventosAdmin import EventosAdmin
        from src.controlador.ControladorEventosAdmin import ControladorEventosAdmin
        vista = EventosAdmin()
        self._controladores["eventos_admin"] = ControladorEventosAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()
        """

    def abrir_gestion(self):
        pass
        #FALTA VISTA
        """
        from src.vista.GestionAdmin import GestionAdmin
        from src.controlador.ControladorGestionAdmin import ControladorGestionAdmin
        vista = GestionAdmin()
        self._controladores["gestion_admin"] = ControladorGestionAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()
        """

    def abrir_test(self):
        #CREO Q ES UN POPUP
        pass
        """
        from src.vista.TestAdmin import TestAdmin
        from src.controlador.ControladorTestAdmin import ControladorTestAdmin
        vista = TestAdmin()
        self._controladores["test_admin"] = ControladorTestAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()
        """

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
            vista = PáginaPrincipal()
            self._controladores["principal"] = ControladorPaginaPrincipal(vista)
            vista.show()
            self._vista.close()
