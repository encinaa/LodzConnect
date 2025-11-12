from abc import ABC
from src.modelo.dao.UsuarioDAO import UsuarioDAO


class ControladorBaseNavegable(ABC):
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()

        # Para guardar referencias
        self._controladores = {}

        # ESTAN TODOS AQUI PERO IGUAL HABIA Q PONERLOS EN LA VISTA
        #self._vista.mi_perfil_clicked.connect(self.abrir_miperfil)
        self._vista.cerrar_sesion_clicked.connect(self.cerrar_sesion)
        #self._vista.test_clicked.connect(self.abrir_test)
        self._vista.publicacion_clicked.connect(self.abrir_publicacion)
        self._vista.eventos_clicked.connect(self.abrir_eventos)
        self._vista.tablon_clicked.connect(self.abrir_tablon)
    """
    def abrir_miperfil(self):
        from src.vista.MiPerfil import MiPerfil
        from src.controlador.ControladorMiPerfil import ControladorMiPerfil
        vista = MiPerfil()
        self._controladores["mi_perfil"] = ControladorMiPerfil(vista, self.correo_usuario)
        vista.show()
        self._vista.close()
    
    def abrir_test(self):
        from src.vista.Test import Test
        from src.controlador.ControladorTest import ControladorTest
        vista = Test()
        self._controladores["test"] = ControladorTest(vista, self.correo_usuario)
        vista.show()
        self._vista.close()
    """
    def abrir_publicacion(self):
        from src.vista.PublicacionPopup import PublicacionPopup
        from src.controlador.ControladorPopupPublicacion import ControladorPopupPublicacion
        popup = PublicacionPopup()
        self._controladores["popup"] = ControladorPopupPublicacion(popup, self.correo_usuario)
        popup.exec_()

    def abrir_eventos(self):
        from src.vista.Eventos import Eventos
        from src.controlador.ControladorEventos import ControladorEventos
        vista = Eventos()
        self._controladores["eventos"] = ControladorEventos(vista, self.correo_usuario)
        vista.show()
        self._vista.close()

    def abrir_tablon(self):
        from src.vista.Tablon import Tablon
        from src.controlador.ControladorTablon import ControladorTablon
        vista = Tablon()
        self._controladores["tablon"] = ControladorTablon(vista, self.correo_usuario)
        vista.show()
        self._vista.close()

    def cerrar_sesion(self):
        from src.vista.PáginaPrincipal import PáginaPrincipal
        from src.controlador.ControladorPaginaPrincipal import ControladorPaginaPrincipal

        confirmacion = self._vista.confirmar_cierre_sesion()
        if confirmacion:
            vista = PáginaPrincipal()
            self._controladores["principal"] = ControladorPaginaPrincipal(vista)
            vista.show()
            self._vista.close()

