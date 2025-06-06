from PyQt5 import uic
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin
from PyQt5.QtCore import pyqtSignal, Qt
from datetime import datetime  
from PyQt5.QtWidgets import QMessageBox, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QWidget

Form, _ = uic.loadUiType("./src/vista/Ui/EventoAdmin.ui")

class EventoAdmin(VistaNavegableAdmin, Form):
    anadir_evento_clicked = pyqtSignal()
    eliminar_evento_solicitado = pyqtSignal(int, str)
    modificar_evento_solicitado = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()
        self.BotonAnadirEvento.clicked.connect(self.anadir_evento_clicked)

    def obtener_datos_evento(self):
        return (
            self.NombreEvento.toPlainText(),
            self.DescripcionEvento.toPlainText(),
            self.FechaEvento.date(),
            self.HoraEvento.time(),
            self.UbicacionEvento.toPlainText(),
            self.AforoMax.value(),
            self.CorreoAdmin.text() if hasattr(self, "CorreoAdmin") else ""
        )

    def mostrar_mensaje_exito(self, mensaje):
        QMessageBox.information(self, "Éxito", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.warning(self, "Error", mensaje)

    def pedir_confirmacion_eliminacion(self, nombre_evento):
        respuesta = QMessageBox.question(
            self, "Confirmar eliminación",
            f"¿Estás seguro de que deseas eliminar el evento \"{nombre_evento}\"?",
            QMessageBox.Yes | QMessageBox.No
        )
        return respuesta == QMessageBox.Yes

    def mostrar_eventos(self, lista_eventos):
        contenedor = self.findChild(QWidget, "contenedorEventos")
        if contenedor.layout() is None:
            contenedor.setLayout(QVBoxLayout())

        layout = contenedor.layout()

        # Limpiar widgets previos
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for evento in lista_eventos:
            widget_evento = self._crear_widget_evento(evento)
            layout.addWidget(widget_evento)

    def _crear_widget_evento(self, evento):
        widget = QWidget()
        layout_general = QVBoxLayout(widget)

        fila_superior = QHBoxLayout()
        fila_superior.addWidget(QLabel(f"🎊 {evento.nombre}"))
        fila_superior.addStretch()
        fila_superior.addWidget(QLabel(f"📅 {evento.fecha} ⏰ {evento.hora}"))

        layout_general.addLayout(fila_superior)
        layout_general.addWidget(QLabel(f"📝 {evento.descripcion}"))
        layout_general.addWidget(QLabel(f"📍 {evento.ubicacion}"))
        layout_general.addWidget(QLabel(f"👥 Aforo: {evento.aforoActual}/{evento.aforoMax}"))

        boton_eliminar = QPushButton("❌")
        boton_eliminar.setToolTip("Eliminar evento")
        boton_eliminar.setFixedWidth(30)
        boton_eliminar.setCursor(Qt.PointingHandCursor)
        boton_eliminar.clicked.connect(
            lambda _, eid=evento.idEve, enombre=evento.nombre: self.eliminar_evento_solicitado.emit(eid, enombre)
        )

        boton_modificar = QPushButton("✏️ Modificar")
        boton_modificar.setCursor(Qt.PointingHandCursor)
        boton_modificar.clicked.connect(lambda _, e=evento: self.modificar_evento_solicitado.emit(e))


        fila_botones = QHBoxLayout()
        fila_botones.addWidget(boton_modificar) 
        fila_botones.addStretch()
        fila_botones.addWidget(boton_eliminar)
        layout_general.addLayout(fila_botones)

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
    

    def rellenar_campos_evento(self, evento):
        self.NombreEvento.setPlainText(evento.nombre)
        self.DescripcionEvento.setPlainText(evento.descripcion)
        self.FechaEvento.setDate(datetime.strptime(evento.fecha, "%Y-%m-%d").date())
        self.HoraEvento.setTime(datetime.strptime(evento.hora, "%H:%M:%S").time())
        self.UbicacionEvento.setPlainText(evento.ubicacion)
        self.AforoMax.setValue(int(evento.aforoMax))
