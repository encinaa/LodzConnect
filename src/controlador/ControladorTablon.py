from src.api.nube_api import CloudStorageAPI
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
        self.nube_api = CloudStorageAPI("https://lodzconnect.blob.core.windows.net/files?sp=racwd&st=2025-12-29T13:36:04Z&se=2026-04-29T20:51:04Z&spr=https&sv=2024-11-04&sr=c&sig=CBGhQx9dfPr8zSlE5JLy65Qv3PkkfLKBOv%2BJND870tc%3D")


    def mostrar_publicaciones(self):
            """Carga y muestra publicaciones combinando BD local y archivos en la nube"""
            if not self._verificar_autenticacion():
                return
                
            try:
                print("🔄 Sincronizando con la nube...")
                
                # 1. Obtener lo que tenemos en BD local
                publicaciones_locales = self.publicacion_dao.obtener_todas_publicaciones()
                # Crear un set de nombres de archivos que ya conocemos para evitar duplicados
                nombres_en_bd = {p.url_nube.split('/')[-1].split('?')[0] for p in publicaciones_locales if p.url_nube}

                # 2. Obtener la lista real de la nube (donde están las de otros)
                res_nube = self.nube_api.list_files()
                
                lista_final = []

                # 3. Procesar publicaciones de la BD local
                for p in publicaciones_locales:
                    if p.url_nube:
                        p.tipo = "nube"
                        p.url = p.url_nube
                    lista_final.append(p)

                # 4. Añadir archivos de la nube que NO están en nuestra BD (de otros usuarios)
                if res_nube["success"]:
                    for archivo_nube in res_nube["files"]:
                        if archivo_nube["nombre"] not in nombres_en_bd:
                            # Creamos un objeto genérico que la vista pueda entender
                            # (Asegúrate de que este objeto tenga los atributos que tu vista requiere)
                            nueva_p = type('Publicacion', (), {})() 
                            nueva_p.idPublic = None # O un ID generado
                            nueva_p.titulo = f"Archivo compartido: {archivo_nube['nombre']}"
                            nueva_p.descripcion = "Subido por otro usuario"
                            nueva_p.url = archivo_nube["url"]
                            nueva_p.url_nube = archivo_nube["url"]
                            nueva_p.tipo = "nube"
                            nueva_p.usuario_correo = "Global" # Identificador para archivos ajenos
                            lista_final.append(nueva_p)

                # 5. Enviar a la vista
                self._vista.mostrar_lista_publicaciones(
                    lista_final, 
                    self.correo_usuario, 
                    self.abrir_perfil_otro, 
                    self._vista.emitir_confirmacion_eliminacion
                )
                
                print(f"✅ Mostrando {len(lista_final)} elementos (Local + Nube)")
                                                    
            except Exception as e:
                print(f"Error sincronizando: {e}")
                self._vista.mostrar_mensaje_error("Error", "It could not be synchronized with the cloud")

    def eliminar_publicacion(self, publicacion):
        """
        Maneja la eliminación tanto de archivos locales+nube como 
        de archivos que solo existen en la nube (de otros).
        """
        if not self._verificar_autenticacion():
            return
            
        try:
            # 1. Extraer el nombre del blob desde la URL
            # La URL tiene formato: .../contenedor/nombre_archivo?token_sas
            blob_name = publicacion.url.split('/')[-1].split('?')[0]

            # 2. Si la publicación tiene ID, existe en nuestra BD local
            if hasattr(publicacion, 'idPublic') and publicacion.idPublic is not None:
                print(f"🗑️ Eliminando publicación {publicacion.idPublic} y su archivo: {blob_name}")
                # Borramos de la nube
                res_nube = self.nube_api.delete_file(blob_name)
                # Borramos de la BD
                self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
            else:
                # 3. Si no tiene ID, es un archivo "fantasma" que solo está en la nube
                print(f"🗑️ Eliminando archivo externo de la nube: {blob_name}")
                res_nube = self.nube_api.delete_file(blob_name)

            if res_nube["success"]:
                self._vista.mostrar_mensaje_info("Eliminated", f"File '{blob_name}' has been deleted.")
            else:
                self._vista.mostrar_mensaje_error("Cloud Error", f"Could not delete from cloud: {res_nube['error']}")

            # Refrescar la lista para que desaparezca
            self.mostrar_publicaciones()

        except Exception as e:
            print(f"❌ Error en proceso de eliminación: {e}")
            self._vista.mostrar_mensaje_error("Error", "An error occurred during deletion.")


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


def eliminar_publicacion_con_archivo(self, publicacion_id):
        """
        Elimina una publicación y su archivo asociado, tanto de la nube como de la base de datos.
        """
        publicacion = self.publicacion_dao.obtener_publicacion_por_id(publicacion_id)
        if not publicacion:
            return {"success": False, "error": "Publicación no encontrada"}

        # 1. Eliminar archivo en Azure
        if hasattr(publicacion, "url_archivo") and publicacion.url_archivo:
            blob_name = publicacion.url_archivo.split("/")[-1]
            res_nube = self.nube_api.delete_file(blob_name)
            if not res_nube["success"]:
                # Si falla, puedes decidir abortar o continuar
                print(f" No se pudo borrar el archivo en la nube: {res_nube['error']}")

        # 2. Eliminar registro en base de datos
        try:
            self.publicacion_dao.eliminar_publicacion(publicacion_id)
            return {"success": True, "deleted_id": publicacion_id}
        except Exception as e:
            return {"success": False, "error": f"Error al eliminar en BD: {e}"}