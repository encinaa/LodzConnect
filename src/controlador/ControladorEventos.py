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

        boton_apuntarse = QPushButton("✅ Apuntarse")
        boton_apuntarse.setCursor(Qt.PointingHandCursor)

        boton_desapuntarse = QPushButton("❌ Desapuntarse")
        boton_desapuntarse.setCursor(Qt.PointingHandCursor)

        def marcar_interes():
            if evento.aforoActual < evento.aforoMax:
                nuevo_aforo = evento.aforoActual + 1
                exito = self.evento_dao.actualizar_aforo(evento.idEve, nuevo_aforo)
                if exito:
                    evento.aforoActual = nuevo_aforo
                    label_aforo.setText(f"👥 Aforo: {nuevo_aforo}/{evento.aforoMax}")
                else:
                    QMessageBox.warning(self._vista, "Error", "No se pudo actualizar el aforo.")
            else:
                QMessageBox.information(self._vista, "Aforo completo", "El evento ya ha alcanzado el aforo máximo.")

        def desapuntarse():
            if evento.aforoActual > 0:
                nuevo_aforo = evento.aforoActual - 1
                exito = self.evento_dao.actualizar_aforo(evento.idEve, nuevo_aforo)
                if exito:
                    evento.aforoActual = nuevo_aforo
                    label_aforo.setText(f"👥 Aforo: {nuevo_aforo}/{evento.aforoMax}")
                else:
                    QMessageBox.warning(self._vista, "Error", "No se pudo actualizar el aforo.")
            else:
                QMessageBox.information(self._vista, "Aforo mínimo", "No hay nadie apuntado al evento.")

        boton_apuntarse.clicked.connect(marcar_interes)
        boton_desapuntarse.clicked.connect(desapuntarse)

        layout_botones = QHBoxLayout()
        layout_botones.addWidget(boton_apuntarse)
        layout_botones.addWidget(boton_desapuntarse)

        layout_general.addLayout(fila_superior)
        layout_general.addWidget(label_desc)
        layout_general.addWidget(label_ubicacion)
        layout_general.addWidget(label_aforo)
        layout_general.addLayout(layout_botones)

        widget.setMaximumWidth(620)
        widget.setStyleSheet("""
            background-color: #388e3c;
            color: white;
            border: 1px solid #90caf9;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        """)

        return widget
