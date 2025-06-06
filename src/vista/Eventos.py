from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/Eventos.ui")

class Eventos(VistaNavegable, Form):
    apuntarse_solicitado = pyqtSignal(object)
    desapuntarse_solicitado = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

    def mostrar_eventos(self, lista_eventos):
        contenedor = self.findChild(QWidget, "contenedorEventos")
        if contenedor is None:
            return

        layout = contenedor.layout()
        if layout is None:
            layout = QVBoxLayout()
            contenedor.setLayout(layout)

        # Limpiar layout
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Añadir eventos
        for evento in lista_eventos:
            widget_evento = self.crear_widget_evento(evento)
            layout.addWidget(widget_evento)

    def crear_widget_evento(self, evento):
        widget = QWidget()
        layout_general = QVBoxLayout(widget)

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
        boton_apuntarse.clicked.connect(lambda: self.apuntarse_solicitado.emit(evento))

        boton_desapuntarse = QPushButton("❌ Desapuntarse")
        boton_desapuntarse.setCursor(Qt.PointingHandCursor)
        boton_desapuntarse.clicked.connect(lambda: self.desapuntarse_solicitado.emit(evento))

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

    def mostrar_mensaje_info(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)
