from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.EventoDAO import EventoDAO
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class ControladorEventos(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.configurar_layout_eventos()
        self.mostrar_eventos()
        self._vista.actualizar_eventos_clicked.connect(self.mostrar_eventos)

    def configurar_layout_eventos(self):
        contenedor = self._vista.findChild(QWidget, "contenedorEventos")
        if contenedor and contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)

    def mostrar_eventos(self):
        eventos = self.evento_dao.obtener_todos_eventos()
        contenedor = self._vista.findChild(QWidget, "contenedorEventos")
        if contenedor is None:
            print("No se encontró el widget 'contenedorEventos'")
            return

        layout = contenedor.layout()
        if layout is None:
            print("El widget 'contenedorEventos' no tiene layout")
            return

        # limpiar
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for evento in eventos:
            widget = self.crear_widget_evento(evento)
            layout.addWidget(widget)

    def crear_widget_evento(self, evento):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()

        label_nombre = QLabel(f"🎉 {evento.nombre}")
        label_nombre.setStyleSheet("font-weight: bold; font-size: 16px;")

        label_fecha = QLabel(f"📅 {evento.fecha} ⏰ {evento.hora}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        fila_superior.addWidget(label_nombre)
        fila_superior.addStretch()
        fila_superior.addWidget(label_fecha)

        label_desc = QLabel(f"📝 {evento.descripcion}")
        label_desc.setWordWrap(True)

        label_ubicacion = QLabel(f"📍 {evento.ubicacion}")
        label_aforo = QLabel(f"👥 Aforo máximo: {evento.aforoMax}")

        boton_apuntarse = QPushButton("✅ Apuntarse")
        boton_apuntarse.setCursor(Qt.PointingHandCursor)
        boton_apuntarse.clicked.connect(lambda _, e=evento: self.apuntarse_evento(e))

        layout_general.addLayout(fila_superior)
        layout_general.addWidget(label_desc)
        layout_general.addWidget(label_ubicacion)
        layout_general.addWidget(label_aforo)
        layout_general.addWidget(boton_apuntarse)

        widget.setStyleSheet("""
            background-color: #f1f8ff;
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        """)

        return widget

    def apuntarse_evento(self, evento):
        # Lógica para apuntarse (esto se adaptaría a tu DAO o sistema)
        if self.evento_dao.apuntar_usuario(evento.idEvento, self.correo_usuario):
            QMessageBox.information(self._vista, "Apuntado", "Te has apuntado al evento con éxito.")
        else:
            QMessageBox.warning(self._vista, "Error", "Ya estás apuntado o ha ocurrido un error.")
