from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.vista.PerfilOtro import PerfilOtro
from src.controlador.ControladorPerfilOtroAdmin import ControladorPerfilOtroAdmin
from PyQt5.QtWidgets import QWidget, QVBoxLayout

class ControladorTablonAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.publicacion_dao = PublicacionDAO()
        self.configurar_layout_publicaciones()
        self.mostrar_publicaciones()
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)

    def configurar_layout_publicaciones(self):
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor is None:
            print("No se encontró el widget 'contenedorPublicaciones'")
            return

        if contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)
            print("Layout asignado manualmente a 'contenedorPublicaciones'")

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor is None or contenedor.layout() is None:
            print("Error con el contenedor de publicaciones.")
            return

        layout = contenedor.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for pub in publicaciones:
            widget = self._vista.crear_widget_publicacion(pub, self.abrir_perfil_otro, self.confirmar_eliminacion)
            layout.addWidget(widget)

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
