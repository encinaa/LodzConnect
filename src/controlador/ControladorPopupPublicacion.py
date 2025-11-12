from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware
from datetime import datetime
import os
import shutil
import uuid

class ControladorPopupPublicacion:
    def __init__(self, vista, correo_usuario, access_token=None):
        self.vista = vista
        self.correo_usuario = correo_usuario
        self.access_token = access_token
        self.dao = PublicacionDAO()
        self.auth_middleware = AuthMiddleware()

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
        """
        The popup used by the UI may be either:
        - the original text-based PublicacionPopup (providing `texto` QTextEdit), or
        - the file-upload popup (providing `obtener_rutas()`).
        This method detects which one is present and performs the appropriate action:
        - For text posts: keep previous behavior (validate text, create PublicacionVO and insert).
        - For file uploads: copy the selected files into a local uploads folder and create a PublicacionVO
          record for each uploaded file (description = filename). Adjust if you prefer storing full path
          or other metadata.
        """
        # Verificar autenticación primero
        if not self._verificar_autenticacion():
            return

        # 1) File-upload path (new popup)
        if hasattr(self.vista, "obtener_rutas"):
            rutas = self.vista.obtener_rutas()
            if not rutas:
                # keep message type consistent with vista.mostrar_mensaje implementation
                try:
                    self.vista.mostrar_mensaje("Information", "No files", "No selected files to upload.")
                except Exception:
                    # fallback to a no-op if vista doesn't implement mostrar_mensaje
                    pass
                return

            # Prepare uploads directory inside current working dir; you can change this path
            uploads_dir = os.path.join(os.getcwd(), "uploads")
            os.makedirs(uploads_dir, exist_ok=True)

            errores = []
            exitos = []
            for ruta in rutas:
                try:
                    nombre = os.path.basename(ruta)
                    # prefix with uuid to avoid collisions
                    destino_nombre = f"{uuid.uuid4().hex}_{nombre}"
                    destino_path = os.path.join(uploads_dir, destino_nombre)
                    shutil.copy2(ruta, destino_path)

                    # create a PublicacionVO record referring to the uploaded file (descripcion holds original filename)
                    nueva_publicacion = PublicacionVO(
                        idPublic=None,
                        fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        listaEtiquetados=[],
                        cuentaOrigen=self.correo_usuario,
                        descripcion=nombre
                    )
                    # insert into DB
                    self.dao.insertar_publicacion(nueva_publicacion)

                    exitos.append(nombre)
                except Exception as e:
                    errores.append(f"{ruta}: {e}")

            # Report result to user
            if exitos:
                try:
                    self.vista.mostrar_mensaje("Information", "Uploaded", f"The file(s) {len(exitos)} has been uploaded.")
                except Exception:
                    pass
                # close popup
                try:
                    self.vista.accept()
                except Exception:
                    pass

            if errores:
                # show errors as well (non-blocking)
                try:
                    self.vista.mostrar_mensaje("error", "Upload error", "\n".join(errores))
                except Exception:
                    pass

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