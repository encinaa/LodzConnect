from PyQt5 import uic
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, pyqtSignal
from src.vista.VistaNavegable import VistaNavegable
import os
import subprocess
import sys

Form, _ = uic.loadUiType("./src/vista/Ui/Eventos.ui")

class Eventos(VistaNavegable, Form):
    # Señal que solicita la eliminación de una publicación (emite el objeto PublicacionVO)
    eliminar_publicacion_solicitada = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

    def mostrar_publicaciones(self, lista_publicaciones, correo_usuario):
        """
        Muestra una lista de PublicacionVO en el contenedor de la UI.
        lista_publicaciones: lista de objetos con atributos idPublic, fecha, cuentaOrigen, descripcion
        correo_usuario: email del usuario actual, usado para mostrar el botón eliminar cuando corresponde.
        """
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

        # Añadir publicaciones
        for pub in lista_publicaciones:
            widget_pub = self.crear_widget_publicacion(pub, correo_usuario)
            layout.addWidget(widget_pub)

    def crear_widget_publicacion(self, publicacion, correo_usuario):
        widget = QWidget()
        layout_general = QVBoxLayout(widget)

        fila_superior = QHBoxLayout()
        # Mostrar botón eliminar si la publicación pertenece al usuario actual
        if publicacion.cuentaOrigen == correo_usuario:
            boton_eliminar = QPushButton("❌")
            boton_eliminar.setFixedSize(40, 40)
            boton_eliminar.setStyleSheet("color: red; border: none; font-weight: bold; padding-bottom: 3px;")
            boton_eliminar.setCursor(Qt.PointingHandCursor)
            boton_eliminar.clicked.connect(lambda _, pub=publicacion: self.eliminar_publicacion_solicitada.emit(pub))
            fila_superior.addWidget(boton_eliminar)
        else:
            fila_superior.addSpacing(30)

        boton_origen = QLabel(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("color: #007acc;")
        fila_superior.addWidget(boton_origen)

        fila_superior.addStretch()

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila_superior.addWidget(label_fecha)

        layout_general.addLayout(fila_superior)

        # Descripción / nombre del fichero: usar publicacion.descripcion (nombre limpio)
        descripcion = (publicacion.descripcion or "").strip()

        file_path = None
        # 1) Si descripcion apunta a una ruta existente (absolute o relative)
        if descripcion:
            try_path = descripcion
            if not os.path.isabs(try_path):
                rel_cwd = os.path.join(os.getcwd(), try_path)
                if os.path.exists(rel_cwd):
                    try_path = rel_cwd
            if os.path.exists(try_path):
                file_path = os.path.abspath(try_path)

        # 2) Si no, buscar en ./uploads por coincidencia
        if not file_path and descripcion:
            uploads_dir = os.path.join(os.getcwd(), "uploads")
            if os.path.isdir(uploads_dir):
                for f in os.listdir(uploads_dir):
                    if f == descripcion or f.endswith("_" + descripcion) or descripcion in f:
                        file_path = os.path.join(uploads_dir, f)
                        break

        # Render archivo (nombre "limpio" mostrado; botón Abrir usa file_path real)
        if file_path and os.path.exists(file_path):
            fila_archivo = QHBoxLayout()
            nombre_archivo = descripcion if descripcion else os.path.basename(file_path)
            label_file = QLabel(f"📎 {nombre_archivo}")
            label_file.setWordWrap(True)
            fila_archivo.addWidget(label_file)

            btn_abrir = QPushButton("Abrir")
            btn_abrir.setCursor(Qt.PointingHandCursor)
            btn_abrir.setStyleSheet("color: #007acc; border: none; text-decoration: underline; background: transparent;")
            btn_abrir.clicked.connect(lambda _, p=file_path: self._abrir_archivo(p))
            fila_archivo.addWidget(btn_abrir)

            fila_archivo.addStretch()
            layout_general.addLayout(fila_archivo)
        else:
            # default: show description as plain text
            label_desc = QLabel(f"📝 {descripcion}")
            label_desc.setWordWrap(True)
            layout_general.addWidget(label_desc)

        widget.setMaximumWidth(820)
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
                subprocess.call(["xdg-open", ruta])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir el archivo:\n{e}")

    def mostrar_mensaje_info(self, mensaje):
        QMessageBox.information(self, "Información", mensaje)

    def mostrar_mensaje_error(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)