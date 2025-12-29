# src/controlador/ControladorPopupPublicacion.py

from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
from datetime import datetime
import os
import shutil
import uuid

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
                    print(f"🔄 Subiendo a Azure: {nombre_original}")
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
