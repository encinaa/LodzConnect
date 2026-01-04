# src/controlador/ControladorPopupPublicacion.py

from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
from datetime import datetime
import os
import shutil
import uuid
import traceback

from src.api.nube_api import CloudStorageAPI

# ⚠️ URL SAS COMPLETA DEL CONTENEDOR (NO LA SUBAS A UN REPO PÚBLICO)
AZURE_SAS_URL = (
    "https://lodzconnect.blob.core.windows.net/files"
    "?sp=racwd&st=2025-12-29T13:36:04Z&se=2026-04-29T20:51:04Z"
    "&spr=https&sv=2024-11-04&sr=c"
    "&sig=CBGhQx9dfPr8zSlE5JLy65Qv3PkkfLKBOv%2BJND870tc%3D"
)


class ControladorPopupPublicacion:
    def __init__(self, vista, correo_usuario, access_token=None):
        self.vista = vista
        self.correo_usuario = correo_usuario
        self.access_token = access_token
        self.dao = PublicacionDAO()
        self.auth_middleware = AuthMiddleware()

        # ----- INTEGRACIÓN CON NUBE (Azure REAL) -----
        self.cloud_api = CloudStorageAPI(AZURE_SAS_URL)
        print("🌐 Azure REAL activado")
        # ----------------------------------------------

        # Botón publicar (distintos nombres posibles según la vista)
        boton = getattr(self.vista, "boton_publicar", None)
        if boton:
            boton.clicked.connect(self.publicar)

    # ------------------------------------------------------------------
    #  AUTENTICACIÓN (comprobamos que el token JWT es válido)
    # ------------------------------------------------------------------
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

    # ------------------------------------------------------------------
    #  PUBLICAR (con subida a Azure + guardado en BD)
    # ------------------------------------------------------------------
    def publicar(self):
        # Versión mejorada que sube a la nube y guarda en BD
        if not self._verificar_autenticacion():
            return

        # 1) Si la vista tiene selector de archivos (PDFs)
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

                    # 1. Subir a Azure

                    es_zip = nombre_original.lower().endswith('.zip')
                    # Si es ZIP, se descomprime antes de subirse
                    if es_zip:
                        print(f"📦 Detectado ZIP. Extrayendo en Azure: {nombre_original}")
                        # Llamamos a la función de extracción
                        resultado = self.cloud_api.upload_and_extract_zip(ruta, self.access_token)
                    else:
                        print(f"🔄 Subiendo archivo normal a Azure: {nombre_original}")
                        # Subida estándar para PDFs u otros archivos
                        resultado = self.cloud_api.upload_file(ruta, nombre_original, self.access_token)


                    if not resultado["success"]:
                        errores.append(f"{nombre_original}: {resultado.get('error', 'Error desconocido')}")
                        continue

                    url_nube = resultado["url"]
                    print(f"✅ Subido a Azure: {url_nube}")

                    # 2. Guardar una copia local (backup)
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
                        url_nube=url_nube,
                        ruta_local=destino_local
                    )

                    self.dao.insertar_publicacion(nueva_publicacion)
                    exitos.append(nombre_original)

                except Exception as e:
                    errores.append(f"{ruta}: {e}")

            # Mostrar resultados
            self._mostrar_resultados_upload(exitos, errores)
            return

        # 2) Fallback: publicación de solo texto (por compatibilidad)
        if hasattr(self.vista, "texto"):
            texto = self.vista.texto.toPlainText().strip()

            if not texto:
                self.vista.mostrar_mensaje("error", "Error", "Text must be fullfilled.")
                return

            if len(texto) > 500:
                self.vista.mostrar_mensaje("error", "Error", "Publication can't exceed 500 characters.")
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

        # Si la vista no tiene ni archivos ni texto
        try:
            self.vista.mostrar_mensaje("error", "Error", "Incompatible view: no 'texto' or 'obtener_rutas' found.")
        except Exception:
            pass


    def eliminar_publicacion(self, publicacion_id, url_nube=None, ruta_local=None):
        """
        Elimina una publicación de:
        - la nube (Azure),
        - la base de datos,
        - y el archivo local dentro de 'uploads',
        incluso si el directorio de ejecución cambió.
        """
        import os, traceback

        try:
            # 1️⃣ Eliminar de la nube (Azure)
            if url_nube:
                print(f"☁️ Eliminando en la nube: {url_nube}")
                try:
                    resultado = self.cloud_api.delete_file(url_nube, self.access_token)
                    if not resultado.get("success", False):
                        print("⚠️ No se pudo eliminar de Azure:", resultado.get("error"))
                    else:
                        print("✅ Archivo eliminado de Azure.")
                except Exception as e:
                    print("⚠️ Error al contactar Azure:", e)

            # 2️⃣ Eliminar archivo local
            archivo_encontrado = None
            if ruta_local:
                ruta_absoluta = os.path.abspath(ruta_local)
                print(f"📂 Intentando eliminar archivo local: {ruta_absoluta}")

                if os.path.exists(ruta_absoluta):
                    archivo_encontrado = ruta_absoluta
                else:
                    # Intentar en carpeta uploads relativa al cwd
                    uploads_dir = os.path.join(os.getcwd(), "uploads")
                    posible = os.path.join(uploads_dir, os.path.basename(ruta_local))
                    if os.path.exists(posible):
                        archivo_encontrado = posible
                    else:
                        # Buscar dentro de todo el proyecto por nombre del archivo
                        for root, dirs, files in os.walk(os.getcwd()):
                            if os.path.basename(ruta_local) in files:
                                archivo_encontrado = os.path.join(root, os.path.basename(ruta_local))
                                break

                if archivo_encontrado:
                    try:
                        os.remove(archivo_encontrado)
                        print(f"🧹 Archivo local eliminado correctamente: {archivo_encontrado}")
                    except Exception as e:
                        print(f"⚠️ No se pudo eliminar el archivo local ({archivo_encontrado}): {e}")
                else:
                    print("ℹ️ No se encontró el archivo local para eliminar.")
            else:
                print("ℹ️ No se proporcionó ruta_local.")

            # 3️⃣ Eliminar registro de la base de datos
            print(f"🗑 Eliminando publicación con ID {publicacion_id}...")
            filas_afectadas = self.dao.eliminar_publicacion(publicacion_id)

            if filas_afectadas == 0:
                self.vista.mostrar_mensaje("error", "No encontrado", "No se encontró la publicación en la base de datos.")
                return

            # 4️⃣ Mostrar mensaje de éxito
            self.vista.mostrar_mensaje("information", "Eliminado", "La publicación y su archivo se eliminaron correctamente.")
            if hasattr(self.vista, "actualizar_lista_publicaciones"):
                self.vista.actualizar_lista_publicaciones()

        except Exception as e:
            print("❌ Error al eliminar publicación:", e)
            print(traceback.format_exc())
            self.vista.mostrar_mensaje("error", "Error interno", str(e))


    # ------------------------------------------------------------------
    #  AUXILIARES
    # ------------------------------------------------------------------
    def _subir_a_nube(self, ruta_archivo, nombre_archivo):
        """
        Mantengo este método por si alguien lo llama en otro sitio,
        pero realmente ya lo hacemos directo en publicar().
        """
        try:
            response = self.cloud_api.upload_file(
                file_path=ruta_archivo,
                destination_name=nombre_archivo,
                access_token=self.access_token
            )

            if response and response.get("success"):
                return response.get("url")
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
            try:
                self.vista.accept()
            except Exception:
                pass

        if errores:
            self.vista.mostrar_mensaje("error", "Errores", "\n".join(errores))
