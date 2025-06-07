from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO


class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.publicacion_dao = PublicacionDAO()
        self.mostrar_publicaciones()
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)
        self._vista.confirmar_eliminacion.connect(self.eliminar_publicacion)
 
    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        self._vista.mostrar_lista_publicaciones(publicaciones, self.correo_usuario, self.abrir_perfil_otro, self._vista.emitir_confirmacion_eliminacion)

    def eliminar_publicacion(self, publicacion):
        self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
        self.mostrar_publicaciones()
        self._vista.mostrar_mensaje_info("Eliminado", "La publicación ha sido eliminada correctamente.")

    def abrir_perfil_otro(self, correo):
        from src.vista.PerfilOtro import PerfilOtro
        from src.controlador.ControladorPerfilOtro import ControladorPerfilOtro
        vista_otro = PerfilOtro()
        ControladorPerfilOtro(vista_otro, correo)
        vista_otro.show()
        self._vista.close()
