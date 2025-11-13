from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
from datetime import datetime
import os
import shutil
import uuid
from src.api.nube_api import CloudStorageAPI 
from src.api.nube_api_mock import CloudStorageAPIMock

class ControladorPopupPublicacion:
    def __init__(self, vista, correo_usuario, access_token=None):
        self.vista = vista
        self.correo_usuario = correo_usuario
        self.access_token = access_token
        self.dao = PublicacionDAO()
        self.auth_middleware = AuthMiddleware()


        #MODIFICACION CON NUBE---------------------------------------------
        # INTEGRACIÓN CON NUBE - API del compañero2
        """
        self.cloud_api = CloudStorageAPI(
            base_url="https://tu-contenedor.ejemplo.com",  # URL que te dé tu compañero???
            api_key="tu_api_key"  # Si necesita autenticación???
        )
        """
#-------#PRUEBAS:
        self.cloud_api = CloudStorageAPIMock()
        print("🔧 MOCK API activado - Modo testing")
#-------#FIN RPUEBAS.
        #MODIFICACION CON NUBE---------------------------------------------

        # support both button names that may exist on different popup implementations
        boton = getattr(self.vista, "boton_publicar", None)
        if boton:
            boton.clicked.connect(self.publicar)

    def _verificar_autenticacion(self):
        """Verifica que el usuario esté autenticado antes de publicar"""
        if not self.access_token:
            self.vista.mostrar_mensaje("error", "Error", "Sesión no válida")
            return False
        
        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        if not valido:
            self.vista.mostrar_mensaje("error", "Sesión expirada", "Por favor, inicie sesión nuevamente")
            return False
        return True


    def publicar(self):
        #Versión MEJORADA que sube a la nube y guarda en BD
        if not self._verificar_autenticacion():
            return

        # 1) Manejo de archivos (PDFs)
        if hasattr(self.vista, "obtener_rutas"):
            rutas = self.vista.obtener_rutas()
            if not rutas:
                self.vista.mostrar_mensaje("Information", "No files", "No selected files to upload.")
                return

            uploads_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(uploads_dir, exist_ok=True)

            errores = []
            exitos = []
            
            for ruta in rutas:
                try:
                    nombre_original = os.path.basename(ruta)
                    """
                    # 1. Subir a la nube
                    url_nube = self._subir_a_nube(ruta, nombre_original)
                    if not url_nube:
                        errores.append(f"{nombre_original}: Error uploading to cloud")
                        continue
                    """

#-------------------#PRUEBAS:
                    # ✅ 1. Subir a nube MOCK
                    print(f"🔄 Intentando subir a nube mock: {nombre_original}")
                    resultado = self.cloud_api.upload_file(ruta, nombre_original, self.access_token)
                    
                    if not resultado['success']:
                        errores.append(f"{nombre_original}: {resultado.get('error', 'Error desconocido')}")
                        continue
                    
                    url_nube = resultado['url']
                    print(f"✅ Subido a nube mock: {url_nube}")
#-------------------#FIN RPUEBAS.

                    # 2. Guardar localmente (backup)
                    nombre_local = f"{uuid.uuid4().hex}_{nombre_original}"
                    destino_local = os.path.join(uploads_dir, nombre_local)
                    shutil.copy2(ruta, destino_local)

                    # 3. Guardar en BD con URL de la nube
                    nueva_publicacion = PublicacionVO(
                        idPublic=None,
                        fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        listaEtiquetados=[],
                        cuentaOrigen=self.correo_usuario,
                        descripcion=nombre_original,
                        url_nube=url_nube,  # ← NUEVO CAMPO
                        ruta_local=destino_local  # ← NUEVO CAMPO
                    )
                    
                    self.dao.insertar_publicacion(nueva_publicacion)
                    exitos.append(nombre_original)
                    
                except Exception as e:
                    errores.append(f"{ruta}: {e}")

            # Mostrar resultados
            self._mostrar_resultados_upload(exitos, errores)
            return


        # 2) Fallback to original text-based behavior for backward compatibility
        if hasattr(self.vista, "texto"):
            texto = self.vista.texto.toPlainText().strip()

            if not texto:
                self.vista.mostrar_mensaje("error", "Error", "Text must be fullfilled.")
                return

            if len(texto) > 500:
                self.vista.mostrar_mensaje("error", "Error", "Publication can't exceed 500 carachteres.")
                return

            nueva_publicacion = PublicacionVO(
                idPublic=None,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                listaEtiquetados=[],
                cuentaOrigen=self.correo_usuario,
                descripcion=texto
            )

            self.dao.insertar_publicacion(nueva_publicacion)
            self.vista.mostrar_mensaje("information", "Posted", "Your post has been saved.")
            try:
                self.vista.accept()
            except Exception:
                pass
            return

        # If neither API is present on the view, show a helpful error
        try:
            self.vista.mostrar_mensaje("error", "Error", "Incompatible view: no 'texto' or 'obtener_rutas' found.")
        except Exception:
            pass

    def _subir_a_nube(self, ruta_archivo, nombre_archivo):
        """Sube archivo a la nube usando la API del compañero2"""
        try:
            # Usar el access_token JWT para autenticación
            response = self.cloud_api.upload_file(
                file_path=ruta_archivo,
                destination_name=nombre_archivo,
                access_token=self.access_token  # ← Tu token JWT
            )
            
            if response and response.get('success'):
                return response.get('url')  # URL del archivo en la nube
            else:
                print(f"Error uploading to cloud: {response}")
                return None
                
        except Exception as e:
            print(f"Exception uploading to cloud: {e}")
            return None

    def _mostrar_resultados_upload(self, exitos, errores):
        """Muestra resultados de la subida"""
        if exitos:
            mensaje = f"Subidos {len(exitos)} archivos a la nube"
            self.vista.mostrar_mensaje("Information", "Éxito", mensaje)
            self.vista.accept()
        
        if errores:
            self.vista.mostrar_mensaje("error", "Errores", "\n".join(errores))

    # Método extra para debugging
    def ver_estadisticas_mock(self):
        """Muestra estadísticas del mock (útil para testing)"""
        stats = self.cloud_api.get_upload_stats()
        print("ESTADÍSTICAS MOCK:")
        print(f"   Total subidas: {stats['total_uploads']}")
        if stats['last_upload']:
            print(f"   Última subida: {stats['last_upload']['original_name']}")
            print(f"   URL mock: {stats['last_upload']['mock_url']}")