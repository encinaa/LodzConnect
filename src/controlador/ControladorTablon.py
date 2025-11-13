from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware

class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario, access_token):
        super().__init__(vista, correo_usuario)
        self.access_token = access_token
        self.auth_middleware = AuthMiddleware()
        self.publicacion_dao = PublicacionDAO()

        # configurar layout y mostrar publicaciones al iniciar (si procede)
        try:
            if hasattr(self._vista, "configurar_layout_publicaciones"):
                self._vista.configurar_layout_publicaciones()
        except Exception:
            pass

        try:
            self.mostrar_publicaciones()
        except Exception:
            pass

        try:
            if hasattr(self._vista, "actualizar_publicaciones_clicked"):
                self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)
        except Exception:
            pass

        try:
            if hasattr(self._vista, "confirmar_eliminacion"):
                self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)
        except Exception:
            pass

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, self.abrir_perfil_otro, self._vista.emitir_confirmacion_eliminacion)

    def mostrar_mis_publicaciones(self):
        """Carga sólo las publicaciones del usuario autenticado y las muestra."""
        publicaciones = self.publicacion_dao.obtener_publicaciones_por_usuario(self.correo_usuario)
        self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, self.abrir_perfil_otro, self._vista.emitir_confirmacion_eliminacion)

    def eliminar_publicacion(self, publicacion):
        try:
            self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
            self.mostrar_publicaciones()
            try:
                self._vista.mostrar_mensaje_info("Eliminado", "La publicación ha sido eliminada correctamente.")
            except Exception:
                pass
        except Exception as e:
            print("ERROR eliminar_publicacion:", e)

    def abrir_perfil_otro(self, correo):
        from src.vista.PerfilOtro import PerfilOtro
        from src.controlador.ControladorPerfilOtro import ControladorPerfilOtro
        vista_otro = PerfilOtro()
        ControladorPerfilOtro(vista_otro, correo)
        vista_otro.show()
        self._vista.close()