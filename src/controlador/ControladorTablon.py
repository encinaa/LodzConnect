from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO


class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)

        # DAO para obtener/eliminar publicaciones
        self.publicacion_dao = PublicacionDAO()

        # Conectar señales de la vista
        # La vista emite actualizar_publicaciones_clicked al pulsar el botón de refresh
        if hasattr(self._vista, "actualizar_publicaciones_clicked"):
            self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)

        # La vista emite confirmar_eliminacion(publicacion) cuando el usuario confirma
        if hasattr(self._vista, "confirmar_eliminacion"):
            self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)

        # Exponer un método con nombre que otros controladores/popups puedan llamar
        # (ControladorPopupPublicacion busca parent.cargar_publicaciones())
        # y cargar las publicaciones inicialmente
        try:
            self.cargar_publicaciones()
        except Exception:
            # si falla la carga inicial no romper la inicialización
            pass

    def mostrar_publicaciones(self):
        """
        Carga las publicaciones desde el DAO y delega la renderización a la vista.
        callback_perfil: función para abrir el perfil de otro usuario.
        callback_eliminar: delega a la vista la acción de pedir confirmación de eliminación.
        """
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        # La vista espera: mostrar_lista_publicaciones(publicaciones, correo_usuario, callback_perfil, callback_eliminar)
        self._vista.mostrar_lista_publicaciones(
            publicaciones,
            self.correo_usuario,
            self.abrir_perfil_otro,
            self._vista.emitir_confirmacion_eliminacion
        )

    # Alias público que puede ser llamado por otros componentes (p. ej. popup)
    def cargar_publicaciones(self):
        self.mostrar_publicaciones()

    def eliminar_publicacion(self, publicacion):
        """
        Elimina la publicación (recibida desde la vista tras confirmación)
        y actualiza la lista en pantalla.
        """
        try:
            self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
            # recargar lista
            self.mostrar_publicaciones()
            # informar al usuario
            if hasattr(self._vista, "mostrar_mensaje_info"):
                self._vista.mostrar_mensaje_info("Eliminated", "Your post has been eliminated")
        except Exception as e:
            # si ocurre un error, mostrarlo si la vista tiene el método
            if hasattr(self._vista, "mostrar_mensaje_info"):
                self._vista.mostrar_mensaje_info("Error", f"No se pudo eliminar la publicación: {e}")

    def abrir_perfil_otro(self, correo):
        from src.vista.PerfilOtro import PerfilOtro
        from src.controlador.ControladorPerfilOtro import ControladorPerfilOtro
        vista_otro = PerfilOtro()
        ControladorPerfilOtro(vista_otro, correo)
        vista_otro.show()
        self._vista.close()