from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware


class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario, access_token):
        super().__init__(vista, correo_usuario)
        self.access_token = access_token
        self.auth_middleware = AuthMiddleware()
        #self.publicacion_dao = PublicacionDAO()
        #self.mostrar_publicaciones()
        #self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)
        #self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)
    """
    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, self.abrir_perfil_otro, self._vista.emitir_confirmacion_eliminacion)

    def eliminar_publicacion(self, publicacion):
        self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
        self.mostrar_publicaciones()
        self._vista.mostrar_mensaje_info("Eliminated", "Your post has been eliminated")
    """
    def abrir_perfil_otro(self, correo):
        from src.vista.PerfilOtro import PerfilOtro
        from src.controlador.ControladorPerfilOtro import ControladorPerfilOtro
        vista_otro = PerfilOtro()
        ControladorPerfilOtro(vista_otro, correo)
        vista_otro.show()
        self._vista.close()



    def _verificar_autenticacion(self):
        """Método interno para verificar autenticación"""
        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        
        if not valido:
            # En una app real, aquí obtendrías el refresh_token de tu almacenamiento
            self._vista.mostrar_mensaje_error("Sesión expirada", "Por favor, inicie sesión nuevamente")
            return False
        return True

    # En cada método que haga requests a la API:
    def cargar_publicaciones(self):
        if not self._verificar_autenticacion():
            return
        
        # Headers con el token para tu API
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }