# -*- coding: utf-8 -*-
import os
import shutil
import uuid
from datetime import datetime

from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.utils.auth_middleware import AuthMiddleware

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
            # keep for backward-compatibility, but prefer reacting to archivos_subidos signal
            boton.clicked.connect(self.publicar)

        # Prefer connecting to the popup's archivos_subidos signal (emitted AFTER the popup
        # has populated its internal rutas/_rutas). This avoids a race where controlador.publicar
        # runs before the popup updates its rutas.
        if hasattr(self.vista, "archivos_subidos"):
            try:
                self.vista.archivos_subidos.connect(self._on_archivos_subidos)
            except Exception:
                # do not break if the signal exists but connection fails
                pass

    def _verificar_autenticacion(self):
        """Verifica que el usuario esté autenticado antes de publicar"""
        if not self.access_token:
            try:
                self.vista.mostrar_mensaje("error", "Error", "Sesión no válida")
            except Exception:
                pass
            return False

        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        if not valido:
            try:
                self.vista.mostrar_mensaje("error", "Sesión expirada", "Por favor, inicie sesión nuevamente")
            except Exception:
                pass
            return False
        return True

# (Muestra solo la función modificada / relevante)
# ... importa lo que ya tengas arriba en el archivo ...

    def _on_archivos_subidos(self, rutas):
        """Handler conectado a PublicacionPopup.archivos_subidos(list_of_paths)."""
        if not self._verificar_autenticacion():
            return

        if not rutas:
            try:
                self.vista.mostrar_mensaje("Information", "No files", "No selected files to upload.")
            except Exception:
                pass
            return

        uploads_dir = os.path.join(os.getcwd(), "uploads")
        os.makedirs(uploads_dir, exist_ok=True)

        errores = []
        exitos = []
        for ruta in rutas:
            try:
                nombre = os.path.basename(ruta)
                destino_nombre = f"{uuid.uuid4().hex}_{nombre}"
                destino_path = os.path.join(uploads_dir, destino_nombre)
                shutil.copy2(ruta, destino_path)

                nueva_publicacion = PublicacionVO(
                    idPublic=None,
                    fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    listaEtiquetados=[],
                    cuentaOrigen=self.correo_usuario,
                    descripcion=nombre
                )
                self.dao.insertar_publicacion(nueva_publicacion)
                exitos.append(nombre)
            except Exception as e:
                errores.append(f"{ruta}: {e}")

        if exitos:
            try:
                self.vista.mostrar_mensaje("Information", "Uploaded", f"The file(s) {len(exitos)} has been uploaded.")
            except Exception:
                pass
            # Intentar cerrar popup
            try:
                self.vista.accept()
            except Exception:
                pass

            # NOTIFICAR: recorrer ancestros para emitir la señal de recarga si existe
            try:
                parent_widget = (self.vista.parent() if callable(getattr(self.vista, "parent", None)) else None) or getattr(self.vista, "parentWidget", lambda: None)()
                # si parent_widget es None, intentamos fallback con vista.parent()
                if parent_widget is None:
                    try:
                        parent_widget = self.vista.parent()
                    except Exception:
                        parent_widget = None

                # subir por los ancestros hasta encontrar un widget que exponga 'actualizar_publicaciones_clicked'
                while parent_widget:
                    if hasattr(parent_widget, "actualizar_publicaciones_clicked"):
                        try:
                            parent_widget.actualizar_publicaciones_clicked.emit()
                        except Exception:
                            # si no es un pyqtSignal o falla, ignorar
                            pass
                        break
                    # avanzar al siguiente ancestro
                    next_parent = None
                    try:
                        next_parent = parent_widget.parentWidget()
                    except Exception:
                        pass
                    if next_parent is None:
                        try:
                            next_parent = parent_widget.parent()
                        except Exception:
                            next_parent = None
                    parent_widget = next_parent
            except Exception:
                pass

        if errores:
            try:
                self.vista.mostrar_mensaje("error", "Upload error", "\n".join(errores))
            except Exception:
                pass
            
    def publicar(self):
        """
        Mantengo publicar() para compatibilidad con la ruta de texto antigua y
        para el caso en que el popup no exponga la señal archivos_subidos.
        """
        # Verificar autenticación primero
        if not self._verificar_autenticacion():
            return

        # 1) File-upload path (legacy): try obtener_rutas() if present
        if hasattr(self.vista, "obtener_rutas"):
            rutas = self.vista.obtener_rutas()
            if rutas is None:
                try:
                    self.vista.mostrar_mensaje("Information", "No files", "No selected files to upload.")
                except Exception:
                    pass
                return

            # Reuse the same handler logic to avoid duplicating behavior
            return self._on_archivos_subidos(rutas)


        # 2) Fallback to original text-based behavior for backward compatibility
        if hasattr(self.vista, "texto"):
            texto = self.vista.texto.toPlainText().strip()

            if not texto:
                try:
                    self.vista.mostrar_mensaje("error", "Error", "Text must be fullfilled.")
                except Exception:
                    pass
                return

            if len(texto) > 500:
                try:
                    self.vista.mostrar_mensaje("error", "Error", "Publication can't exceed 500 carachteres.")
                except Exception:
                    pass
                return

            nueva_publicacion = PublicacionVO(
                idPublic=None,
                fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                listaEtiquetados=[],
                cuentaOrigen=self.correo_usuario,
                descripcion=texto
            )
            try:
                self.dao.insertar_publicacion(nueva_publicacion)
                try:
                    self.vista.mostrar_mensaje("information", "Posted", "Your post has been saved.")
                except Exception:
                    pass
                try:
                    self.vista.accept()
                except Exception:
                    pass
            except Exception:
                try:
                    self.vista.mostrar_mensaje("error", "Error", "Incompatible view: operation failed.")
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