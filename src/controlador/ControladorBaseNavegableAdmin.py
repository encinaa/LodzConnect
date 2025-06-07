from abc import ABC
from src.modelo.dao.UsuarioDAO import UsuarioDAO

class ControladorBaseNavegableAdmin(ABC):
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        # Para guardar referencias para poder volver a las vistas sin q se cierren pestañas
        self._controladores = {}

        # Conecta señales de botones del admin
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
        from src.vista.EventoAdmin import EventoAdmin
        from src.controlador.ControladorEventoAdmin import ControladorEventoAdmin
        vista = EventoAdmin()
        self._controladores["eventos_admin"] = ControladorEventoAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()

    def abrir_gestion(self):
        from src.vista.GestionAdmin import GestionAdmin
        from src.controlador.ControladorGestionAdmin import ControladorGestionAdmin
        vista = GestionAdmin()
        self._controladores["gestion_admin"] = ControladorGestionAdmin(vista, self.correo_usuario)
        vista.show()
        self._vista.close()


    def abrir_test(self):
        from src.vista.CrearTestPopup import CrearTestPopup
        popup = CrearTestPopup(self.correo_usuario)
        popup.exec_()

    def cerrar_sesion(self):
        from src.vista.PáginaPrincipal import PáginaPrincipal
        from src.controlador.ControladorPaginaPrincipal import ControladorPaginaPrincipal

        confirmacion = self._vista.confirmar_cierre_sesion()
        if confirmacion:
            vista = PáginaPrincipal()
            self._controladores["principal"] = ControladorPaginaPrincipal(vista)
            vista.show()
            self._vista.close()

