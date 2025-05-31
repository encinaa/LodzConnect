from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class ControladorTablon(ControladorBaseNavegable):
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
        else:
            print("Layout ya existente en 'contenedorPublicaciones'")

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor is None:
            print("No se encontró el widget 'contenedorPublicaciones'")
            return

        layout = contenedor.layout()
        if layout is None:
            print("El widget 'contenedorPublicaciones' no tiene un layout asignado")
            return

        # Limpiar publicaciones anteriores
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for pub in publicaciones:
            widget = self.crear_widget_publicacion(pub)
            layout.addWidget(widget)

    #PARA Q SALGAN LAS PUBLICACIONES HAY Q HACERLO SI O SI DESDE CODIGO
    def crear_widget_publicacion(self, publicacion):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        # cuentaOrigen (izquierda) + fecha (derecha)
        fila_superior = QHBoxLayout()
        label_origen = QLabel(f"👤 {publicacion.cuentaOrigen}")
        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        fila_superior.addWidget(label_origen)
        fila_superior.addStretch()  # empuja la fecha a la derecha
        fila_superior.addWidget(label_fecha)

        # el texto
        label_desc = QLabel(f"📝 {publicacion.descripcion}")
        label_desc.setWordWrap(True)  # ajusta el texto si es largo

        layout_general.addLayout(fila_superior)
        layout_general.addWidget(label_desc)

        widget.setStyleSheet("""
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        """)
        return widget
