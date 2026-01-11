from src.api.nube_api import CloudStorageAPI
from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
import os
import webbrowser
from urllib.parse import unquote

class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario, access_token):
        super().__init__(vista, correo_usuario, access_token)
        self.access_token = access_token
        self.auth_middleware = AuthMiddleware()
        self.publicacion_dao = PublicacionDAO() 

        # 1. TOKEN SAS
        self.sas_token = "sp=racwdli&st=2026-01-11T18:17:14Z&se=2026-06-30T01:32:14Z&spr=https&sv=2024-11-04&sr=c&sig=LA9iSkwjWL4LOunrbj3D%2BXGmqEwEb2bJuNp4KImdWg0%3D"
        
        base_url = "https://uniconnection.blob.core.windows.net/files"
        self.nube_api = CloudStorageAPI(f"{base_url}?{self.sas_token}")

        self.mostrar_publicaciones()
        
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)
        self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)
        
        if hasattr(self._vista, 'item_double_clicked'):
            self._vista.item_double_clicked.connect(self.abrir_archivo)

    def mostrar_publicaciones(self):
        """
        Carga publicaciones, OMITIENDO los .zip (limpiando tokens de la URL).
        """
        if not self._verificar_autenticacion():
            return
            
        try:
            print("🔄 Sincronizando con la nube...")
            publicaciones_locales = self.publicacion_dao.obtener_todas_publicaciones()
            
            nombres_en_bd = set()
            for p in publicaciones_locales:
                if p.url_nube:
                    # Limpiamos para el set de control
                    nombre_limpio = p.url_nube.split('/')[-1].split('?')[0]
                    nombres_en_bd.add(nombre_limpio)

            res_nube = self.nube_api.list_files()
            lista_final = []

            # ---------------------------------------------------------
            # 1. Procesar archivos de la Base de Datos
            # ---------------------------------------------------------
            for p in publicaciones_locales:
                if p.url_nube:
                    # ### CORRECCIÓN CRÍTICA AQUÍ ###
                    # 1. Quitamos los parámetros del token (?sv=...)
                    url_sin_token = p.url_nube.split('?')[0].lower()
                    
                    # 2. Ahora sí comprobamos la extensión
                    if url_sin_token.endswith('.zip'):
                        print(f"🚫 Ocultando ZIP de BD: {p.titulo}")
                        continue 
                    # ###############################

                    p.tipo = "nube"
                    p.url = p.url_nube
                    lista_final.append(p)

            # ---------------------------------------------------------
            # 2. Procesar archivos encontrados en Azure (Descomprimidos)
            # ---------------------------------------------------------
            if res_nube["success"]:
                import datetime
                
                for archivo_nube in res_nube["files"]:
                    nombre = archivo_nube["nombre"] 
                    
                    if "__MACOSX" in nombre or nombre.startswith("."):
                        continue
                    
                    # También filtramos ZIPs que vengan directos de Azure
                    if nombre.lower().endswith('.zip'):
                        continue
                    
                    if nombre not in nombres_en_bd:
                        nueva_p = type('Publicacion', (), {})() 
                        nueva_p.idPublic = None 
                        
                        nombre_solo_archivo = nombre.split('/')[-1]
                        nueva_p.titulo = nombre_solo_archivo 
                        
                        # Descripción con la ruta completa
                        nueva_p.descripcion = nombre
                        
                        nueva_p.url = archivo_nube["url"]
                        nueva_p.url_nube = archivo_nube["url"]
                        nueva_p.tipo = "nube"
                        
                        nueva_p.cuentaOrigen = self.correo_usuario 
                        nueva_p.usuario_correo = self.correo_usuario
                        nueva_p.fecha = datetime.datetime.now().strftime("%Y-%m-%d")

                        lista_final.append(nueva_p)

            self._vista.mostrar_lista_publicaciones(
                lista_final, 
                self.correo_usuario, 
                self.abrir_perfil_otro, 
                self._vista.emitir_confirmacion_eliminacion
            )
            print(f"✅ Mostrando {len(lista_final)} archivos (ZIPs ocultos)")
                                                
        except Exception as e:
            print(f"❌ Error en mostrar_publicaciones: {e}")
            import traceback
            traceback.print_exc()

    def abrir_archivo(self, publicacion):
        try:
            url_limpia = publicacion.url.split('?')[0]
            url_final = f"{url_limpia}?{self.sas_token}"
            print(f"🌐 Abriendo archivo: {url_limpia}") 
            webbrowser.open(url_final)
        except Exception as e:
            print(f"Error al abrir: {e}")
            self._vista.mostrar_mensaje_error("Error", "No se pudo abrir el archivo.")

    def eliminar_publicacion(self, publicacion):
        if not self._verificar_autenticacion(): return
        try:
            url_limpia = publicacion.url.split('?')[0]
            if "/files/" in url_limpia:
                blob_name = url_limpia.split("/files/")[-1]
            else:
                blob_name = url_limpia.split('/')[-1]
            blob_name = unquote(blob_name)
            
            print(f"🗑️ Intentando eliminar blob: '{blob_name}'")
            res_nube = self.nube_api.delete_file(blob_name)
            
            exito = res_nube["success"] or "BlobNotFound" in str(res_nube.get("error", ""))
            
            if exito:
                if hasattr(publicacion, 'idPublic') and publicacion.idPublic:
                    self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
                self._vista.mostrar_mensaje_info("Eliminated", f"File '{blob_name}' deleted.")
                self.mostrar_publicaciones()
            else:
                print(f"❌ Error Azure: {res_nube.get('error')}")
                self._vista.mostrar_mensaje_error("Error", f"Cloud error: {res_nube.get('error')}")
        except Exception as e:
            print(f"❌ Error crítico al eliminar: {e}")
            self._vista.mostrar_mensaje_error("Error", f"Exception: {str(e)}")

    def abrir_perfil_otro(self, correo): pass
    def _verificar_autenticacion(self): return True