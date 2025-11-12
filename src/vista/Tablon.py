from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable
import os
import subprocess
import sys

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

        # Configuración del layout del contenedor de publicaciones
        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if contenedor and contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)

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

        layout_general.addLayout(fila_superior)

        # Check whether the publication description represents or refers to a file
        descripcion = (publicacion.descripcion or "").strip()

        file_path = None
        # 1) If descripcion is an absolute or relative path that exists, use it.
        if descripcion:
            # treat both absolute and relative paths
            try_path = descripcion
            if not os.path.isabs(try_path):
                # try relative to cwd and to an "uploads" folder
                rel_cwd = os.path.join(os.getcwd(), try_path)
                if os.path.exists(rel_cwd):
                    try_path = rel_cwd
            if os.path.exists(try_path):
                file_path = os.path.abspath(try_path)

        # 2) If descripcion is just a filename (e.g. "foo.pdf"), try to find it in ./uploads
        if not file_path and descripcion:
            uploads_dir = os.path.join(os.getcwd(), "uploads")
            if os.path.isdir(uploads_dir):
                for f in os.listdir(uploads_dir):
                    if f == descripcion or f.endswith("_" + descripcion) or descripcion in f:
                        file_path = os.path.join(uploads_dir, f)
                        break

        # Render file publication differently (clickable/openable)
        if file_path and os.path.exists(file_path):
            fila_archivo = QHBoxLayout()
            nombre_archivo = os.path.basename(file_path)
            label_file = QLabel(f"📎 {nombre_archivo}")
            label_file.setWordWrap(True)
            fila_archivo.addWidget(label_file)

            btn_abrir = QPushButton("Abrir")
            btn_abrir.setCursor(Qt.PointingHandCursor)
            btn_abrir.setStyleSheet("color: #007acc; border: none; text-decoration: underline; background: transparent;")
            # capture path in default arg
            btn_abrir.clicked.connect(lambda _, p=file_path: self._abrir_archivo(p))
            fila_archivo.addWidget(btn_abrir)

            fila_archivo.addStretch()
            layout_general.addLayout(fila_archivo)
        else:
            # default: show description as plain text
            label_desc = QLabel(f"📝 {descripcion}")
            label_desc.setWordWrap(True)
            layout_general.addWidget(label_desc)

        widget.setStyleSheet("""
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 10px;
        """)
        return widget

    def _abrir_archivo(self, ruta):
        try:
            if sys.platform.startswith("darwin"):
                subprocess.call(["open", ruta])
            elif sys.platform.startswith("win"):
                os.startfile(ruta)
            else:
                # assume linux / unix-like
                subprocess.call(["xdg-open", ruta])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{e}")

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