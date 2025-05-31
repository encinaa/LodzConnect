from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout
from src.modelo.dao.PublicacionDAO import PublicacionDAO


from PyQt5.QtWidgets import QVBoxLayout, QWidget

class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.publicacion_dao = PublicacionDAO()
        self.configurar_layout_publicaciones()  # ← NUEVO
        self.mostrar_publicaciones()

    def configurar_layout_publicaciones(self):
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor and contenedor.layout() is None:
            layout = QVBoxLayout(contenedor)
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
        elif not contenedor:
            print("⚠ No se encontró el widget 'contenedorPublicaciones'")

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if not contenedor:
            print("⚠ No se encontró el widget 'contenedorPublicaciones'")
            return

        layout = contenedor.layout()
        if not layout:
            print("⚠ El widget 'contenedorPublicaciones' no tiene un layout asignado")
            return

        # Limpiar publicaciones anteriores (opcional)
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for pub in publicaciones:
            widget = self.crear_widget_publicacion(pub)
            layout.addWidget(widget)

    def crear_widget_publicacion(self, publicacion):
        widget = QWidget()
        layout = QVBoxLayout()
        widget.setLayout(layout)

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_origen = QLabel(f"👤 {publicacion.cuentaOrigen}")
        label_desc = QLabel(f"📝 {publicacion.descripcion}")

        layout.addWidget(label_fecha)
        layout.addWidget(label_origen)
        layout.addWidget(label_desc)

        widget.setStyleSheet("border: 1px solid gray; padding: 10px; margin-bottom: 10px;")
        return widget

