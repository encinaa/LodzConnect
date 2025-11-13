from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware

class ControladorEventos(ControladorBaseNavegable):
    """
    Este controlador antes gestionaba 'eventos'. Lo reutilizamos para la pestaña 'My posts':
    - carga las publicaciones del usuario y las muestra en la vista Eventos (renombrada mentalmente a My posts)
    - permite eliminar publicaciones del usuario
    """
    def __init__(self, vista, correo_usuario, access_token=None):
        super().__init__(vista, correo_usuario, access_token)
        self.auth_middleware = AuthMiddleware()
        self.publicacion_dao = PublicacionDAO()

        # conectar la señal de la vista para eliminar publicaciones
        try:
            if hasattr(self._vista, "eliminar_publicacion_solicitada"):
                self._vista.eliminar_publicacion_solicitada.connect(self.eliminar_publicacion)
        except Exception:
            pass

        # mostrar las publicaciones del usuario al inicializar
        try:
            self.mostrar_mis_publicaciones()
        except Exception:
            pass

    def _verificar_autenticacion(self):
        """Verifica token si es necesario (mantener consistencia con otros controladores)."""
        if not self.access_token:
            try:
                self._vista.mostrar_mensaje_error("Sesión no válida")
            except Exception:
                pass
            return False

        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        if not valido:
            try:
                self._vista.mostrar_mensaje_error("Sesión expirada")
            except Exception:
                pass
            return False
        return True

    def mostrar_mis_publicaciones(self):
        """Carga publicaciones cuyo cuentaOrigen == correo_usuario y pide a la vista mostrarlas."""
        # opcional: verificar autenticación (si tu flujo requiere token válido para leer)
        # if not self._verificar_autenticacion():
        #     return

        publicaciones = self.publicacion_dao.obtener_publicaciones_por_usuario(self.correo_usuario)
        try:
            # la vista implementa mostrar_publicaciones(lista, correo_usuario)
            self._vista.mostrar_publicaciones(publicaciones, self.correo_usuario)
        except Exception as e:
            print("ERROR mostrar_mis_publicaciones:", e)

    def eliminar_publicacion(self, publicacion):
        # eliminar y recargar
        try:
            self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
            # recargar la lista
            self.mostrar_mis_publicaciones()
            try:
                self._vista.mostrar_mensaje_info("La publicación ha sido eliminada.")
            except Exception:
                pass
        except Exception as e:
            print("ERROR eliminar_publicacion:", e)
            try:
                self._vista.mostrar_mensaje_error("No se pudo eliminar la publicación.")
            except Exception:
                pass