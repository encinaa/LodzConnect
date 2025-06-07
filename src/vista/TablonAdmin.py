from PyQt5 import uic
from PyQt5.QtWidgets import QPushButton, QMessageBox, QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, Qt
from src.vista.VistaNavegableAdmin import VistaNavegableAdmin

Form, _ = uic.loadUiType("./src/vista/Ui/TablónAdmin.ui")

class TablonAdmin(VistaNavegableAdmin, Form):
    actualizar_publicaciones_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        boton_actualizar = self.findChild(QPushButton, "BotonActualizar")
        if boton_actualizar:
            boton_actualizar.clicked.connect(self.actualizar_publicaciones_clicked)

    def configurar_layout_publicaciones(self):
        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if contenedor and contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)

    def mostrar_lista_publicaciones(self, publicaciones, callback_perfil, callback_eliminar):
        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if not contenedor or contenedor.layout() is None:
            return

        layout = contenedor.layout()
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for publicacion in publicaciones:
            widget = self.crear_widget_publicacion(publicacion, callback_perfil, callback_eliminar)
            layout.addWidget(widget)

    def crear_widget_publicacion(self, publicacion, callback_perfil, callback_eliminar):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()

        boton_eliminar = QPushButton("❌")
        boton_eliminar.setFixedSize(40, 40)
        boton_eliminar.setStyleSheet("color: red; border: none; font-weight: bold; padding-bottom: 3px;")
        boton_eliminar.setCursor(Qt.PointingHandCursor)
        boton_eliminar.clicked.connect(lambda _, pub=publicacion: callback_eliminar(pub))
        fila_superior.addWidget(boton_eliminar)

        boton_origen = QPushButton(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("border: none; color: #007acc; text-align: left;")
        boton_origen.setCursor(Qt.PointingHandCursor)
        boton_origen.clicked.connect(lambda _, correo=publicacion.cuentaOrigen: callback_perfil(correo))
        fila_superior.addWidget(boton_origen)

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila_superior.addStretch()
        fila_superior.addWidget(label_fecha)

        label_desc = QLabel(f"📝 {publicacion.descripcion}")
        label_desc.setWordWrap(True)

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

    def mostrar_confirmacion_eliminacion(self, on_accept_callback):
        respuesta = QMessageBox.question(
            self,
            "Eliminar publicación",
            "¿Estás seguro de que deseas eliminar esta publicación?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            on_accept_callback()

    def mostrar_mensaje_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)
