from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/Tablón4.ui")

class Tablon(VistaNavegable, Form):
    actualizar_publicaciones_clicked = pyqtSignal()
    confirmar_eliminacion = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        boton_actualizar = self.findChild(QPushButton, "BotonActualizar")
        if boton_actualizar:
            boton_actualizar.clicked.connect(self.actualizar_publicaciones_clicked)

    def mostrar_lista_publicaciones(self, publicaciones, correo_usuario, callback_perfil, callback_eliminar):
        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if not contenedor:
            return

        layout = contenedor.layout()
        if layout is None:
            return

        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for pub in publicaciones:
            widget = self.crear_widget_publicacion(pub, correo_usuario, callback_perfil, callback_eliminar)
            layout.addWidget(widget)

    def crear_widget_publicacion(self, publicacion, correo_usuario, callback_perfil, callback_eliminar):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()

        if publicacion.cuentaOrigen == correo_usuario:
            boton_eliminar = QPushButton("❌")
            boton_eliminar.setFixedSize(40, 40)
            boton_eliminar.setStyleSheet("color: red; border: none; font-weight: bold; padding-bottom: 3px;")
            boton_eliminar.setCursor(Qt.PointingHandCursor)
            boton_eliminar.clicked.connect(lambda _, pub=publicacion: callback_eliminar(pub))
            fila_superior.addWidget(boton_eliminar)
        else:
            fila_superior.addSpacing(30)

        boton_origen = QPushButton(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("border: none; color: #007acc; text-align: left;")
        boton_origen.setCursor(Qt.PointingHandCursor)
        boton_origen.clicked.connect(lambda _, correo=publicacion.cuentaOrigen: callback_perfil(correo))
        fila_superior.addWidget(boton_origen)

        fila_superior.addStretch()

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
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

    def emitir_confirmacion_eliminacion(self, publicacion):
        respuesta = QMessageBox.question(
            self,
            "Eliminar publicación",
            "¿Estás seguro de que deseas eliminar esta publicación?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.confirmar_eliminacion.emit(publicacion)

    def mostrar_mensaje_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)
