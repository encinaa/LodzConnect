from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class ControladorEventoAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.evento_dao = EventoDAO()
        self.logica = EventoLogica(self.evento_dao)

        self._vista.anadir_evento_clicked.connect(self.on_anadir_evento_clicked)
        self.configurar_layout_eventos()
        self.mostrar_eventos()

    def on_anadir_evento_clicked(self):
        nombre, descripcion, fecha, hora, ubicacion, aforo, correo_admin = self._vista.obtener_datos_evento()

        exito, mensaje = self.logica.registrar_evento(
            nombre, descripcion, fecha, hora, ubicacion, aforo, self.correo_usuario
        )

        if exito:
            self._vista.mostrar_mensaje_exito(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

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
        if contenedor is None or contenedor.layout() is None:
            print("Error: No se encontró el contenedor de eventos o no tiene layout.")
            return

        layout = contenedor.layout()

        # Limpiar
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

        label_nombre = QLabel(f"🎊 {evento.nombre}")
        label_nombre.setStyleSheet("font-weight: bold; font-size: 16px;")

        label_fecha = QLabel(f"📅 {evento.fecha} ⏰ {evento.hora}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        fila_superior.addWidget(label_nombre)
        fila_superior.addStretch()
        fila_superior.addWidget(label_fecha)

        label_desc = QLabel(f"📝 {evento.descripcion}")
        label_desc.setWordWrap(True)

        label_ubicacion = QLabel(f"📍 {evento.ubicacion}")
        label_aforo = QLabel(f"👥 Aforo: {evento.aforoActual}/{evento.aforoMax}")

        boton_eliminar = QPushButton("❌")
        boton_eliminar.setToolTip("Eliminar evento")
        boton_eliminar.setCursor(Qt.PointingHandCursor)
        boton_eliminar.setFixedWidth(30)

        def eliminar_evento():
            confirmacion = QMessageBox.question(
                self._vista,
                "Confirmar eliminación",
                f"¿Estás seguro de que deseas eliminar el evento \"{evento.nombre}\"?",
                QMessageBox.Yes | QMessageBox.No
            )
            if confirmacion == QMessageBox.Yes:
                exito = self.evento_dao.eliminar_evento(evento.idEve)
                if exito:
                    self.mostrar_eventos()
                else:
                    QMessageBox.warning(self._vista, "Error", "No se pudo eliminar el evento.")

        boton_eliminar.clicked.connect(eliminar_evento)

        layout_botones = QHBoxLayout()
        layout_botones.addStretch()
        layout_botones.addWidget(boton_eliminar)

        layout_general.addLayout(fila_superior)
        layout_general.addWidget(label_desc)
        layout_general.addWidget(label_ubicacion)
        layout_general.addWidget(label_aforo)
        layout_general.addLayout(layout_botones)

        widget.setMaximumWidth(380)
        widget.setStyleSheet("""
            background-color: #388e3c;
            color: white;
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 5px;
            margin-bottom: 10px;
        """)

        return widget
