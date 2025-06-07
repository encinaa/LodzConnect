from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.vista.PerfilOtro import PerfilOtro
from src.controlador.ControladorPerfilOtroAdmin import ControladorPerfilOtroAdmin

class ControladorTablonAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.publicacion_dao = PublicacionDAO()
        self._vista.configurar_layout_publicaciones()
        self.mostrar_publicaciones()
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        self._vista.mostrar_lista_publicaciones(publicaciones, self.abrir_perfil_otro, self.confirmar_eliminacion)

    def confirmar_eliminacion(self, publicacion):
        self._vista.mostrar_confirmacion_eliminacion(
            lambda: self.eliminar_publicacion(publicacion)
        )

    def eliminar_publicacion(self, publicacion):
        self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
        self.mostrar_publicaciones()
        self._vista.mostrar_mensaje_info("Eliminado", "La publicación ha sido eliminada correctamente.")

    def abrir_perfil_otro(self, correo):
        self.vista_otro = PerfilOtro()
        self.controlador_otro = ControladorPerfilOtroAdmin(self.vista_otro, correo)
        self.vista_otro.show()
        self._vista.close()
