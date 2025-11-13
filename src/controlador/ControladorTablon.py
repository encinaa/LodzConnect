from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
import os  # ← AÑADE ESTA IMPORTACIÓN


class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario, access_token):
        super().__init__(vista, correo_usuario, access_token)
        self.access_token = access_token
        self.auth_middleware = AuthMiddleware()
        self.publicacion_dao = PublicacionDAO()  # ← DESCOMENTA ESTO
        self.mostrar_publicaciones()  # ← DESCOMENTA ESTO
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)
        self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)


    def mostrar_publicaciones(self):
        """Carga y muestra las publicaciones desde la BD"""
        if not self._verificar_autenticacion():
            return
            
        try:
            print("🔄 Actualizando publicaciones...")
            
            publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
            
            
            # ✅ SIMPLIFICADO: Solo marcar tipo para nube
            for publicacion in publicaciones:
                if hasattr(publicacion, 'url_nube') and publicacion.url_nube:
                    publicacion.tipo = "nube"
                    publicacion.url = publicacion.url_nube
                # Los demás serán tratados como texto automáticamente
            
            self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, 
                                                self.abrir_perfil_otro, 
                                                self._vista.emitir_confirmacion_eliminacion)
            
            print(f"✅ Publicaciones actualizadas: {len(publicaciones)} encontradas")
                                                
        except Exception as e:
            print(f"Error cargando publicaciones: {e}")
            self._vista.mostrar_mensaje_error("Error", "No se pudieron cargar las publicaciones")


    def eliminar_publicacion(self, publicacion):
        if not self._verificar_autenticacion():
            return
            
        self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
        self.mostrar_publicaciones()
        self._vista.mostrar_mensaje_info("Eliminated", "Your post has been eliminated")

    def abrir_perfil_otro(self, correo):
        pass

    def _verificar_autenticacion(self):
        """Método interno para verificar autenticación"""
        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        
        if not valido:
            self._vista.mostrar_mensaje_error("Expired session", "Please, log in again.")
            return False
        return True

    # En cada método que haga requests a la API:
    def cargar_publicaciones(self):
        if not self._verificar_autenticacion():
            return
        
        try:
            # 1. Obtener publicaciones de la BD
            publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
            
            # 2. Para cada publicación, verificar si tiene archivo en nube
            for publicacion in publicaciones:
                if publicacion.url_nube:
                    # Mostrar como enlace a la nube
                    publicacion.tipo = "nube"
                    publicacion.url = publicacion.url_nube
                elif publicacion.ruta_local and os.path.exists(publicacion.ruta_local):
                    # Mostrar archivo local
                    publicacion.tipo = "local" 
                    publicacion.url = publicacion.ruta_local
                else:
                    # Es texto plano
                    publicacion.tipo = "texto"
            
            # 3. Pasar a la vista
            self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, 
                                                self.abrir_perfil_otro, 
                                                self._vista.emitir_confirmacion_eliminacion)
                                                
        except Exception as e:
            print(f"Error cargando publicaciones: {e}")
            self._vista.mostrar_mensaje_error("Error", "No se pudieron cargar las publicaciones")