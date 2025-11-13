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
            print("✅ Botón 'Actualizar' encontrado, conectando señal...")
            boton_actualizar.clicked.connect(self._on_actualizar_clicked)
        else:
            print("❌ Botón 'Actualizar' NO encontrado - revisa el nombre en el .ui")

        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if contenedor and contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)

    def _on_actualizar_clicked(self):
        """Método interno que emite la señal cuando se hace click"""
        print("🔄 clicked - emitiendo señal...")
        self.actualizar_publicaciones_clicked.emit()

    def mostrar_lista_publicaciones(self, publicaciones, correo_usuario, callback_perfil, callback_eliminar):
        contenedor = self.findChild(QWidget, "contenedorPublicaciones")
        if not contenedor:
            print("❌ Contenedor de publicaciones no encontrado")
            return

        layout = contenedor.layout()
        if layout is None:
            print("❌ Layout del contenedor no encontrado")
            return

        # Limpiar publicaciones anteriores
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        print(f"📝 Mostrando {len(publicaciones)} publicaciones...")

        if not publicaciones:
            label_vacio = QLabel("No uploads yet")
            label_vacio.setAlignment(Qt.AlignCenter)
            label_vacio.setStyleSheet("color: #666; font-style: italic; padding: 20px;")
            layout.addWidget(label_vacio)
            return

        for pub in publicaciones:
            widget = self.crear_widget_publicacion(pub, correo_usuario, callback_perfil, callback_eliminar)
            layout.addWidget(widget)

    def crear_widget_publicacion(self, publicacion, correo_usuario, callback_perfil, callback_eliminar):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()

        # Botón eliminar (solo para publicaciones propias)
        if publicacion.cuentaOrigen == correo_usuario:
            boton_eliminar = QPushButton("❌")
            boton_eliminar.setFixedSize(40, 40)
            boton_eliminar.setStyleSheet("color: red; border: none; font-weight: bold; padding-bottom: 3px;")
            boton_eliminar.setCursor(Qt.PointingHandCursor)
            boton_eliminar.clicked.connect(lambda _, pub=publicacion: callback_eliminar(pub))
            fila_superior.addWidget(boton_eliminar)
        else:
            fila_superior.addSpacing(30)

        # Botón del usuario origen
        boton_origen = QPushButton(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("border: none; color: #007acc; text-align: left;")
        boton_origen.setCursor(Qt.PointingHandCursor)
        boton_origen.clicked.connect(lambda _, correo=publicacion.cuentaOrigen: callback_perfil(correo))
        fila_superior.addWidget(boton_origen)

        fila_superior.addStretch()

        # Fecha
        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila_superior.addWidget(label_fecha)

        layout_general.addLayout(fila_superior)

        descripcion = (publicacion.descripcion or "").strip()
        
        # ✅ SIMPLIFICADO: Solo manejar nube y texto
        if hasattr(publicacion, 'tipo') and publicacion.tipo == "nube":
            # Archivo en la nube - mostrar como enlace clickeable
            fila_archivo = QHBoxLayout()
            nombre_archivo = os.path.basename(descripcion)
            
            # Botón que funciona como enlace
            btn_archivo = QPushButton(f" {nombre_archivo}")
            btn_archivo.setCursor(Qt.PointingHandCursor)
            btn_archivo.setStyleSheet("""
                color: #007acc; 
                border: none; 
                text-decoration: underline; 
                background: transparent;
                text-align: left;
                padding: 0px;
            """)
            btn_archivo.clicked.connect(lambda _, url=publicacion.url: self._abrir_url_nube(url))
            fila_archivo.addWidget(btn_archivo)
            
            fila_archivo.addStretch()
            layout_general.addLayout(fila_archivo)
            
        else:
            # Texto plano
            label_desc = QLabel(f" {descripcion}")
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




    def _abrir_url_nube(self, url):
        """Abre URL de archivo en la nube en el navegador"""
        try:
            print(f"🌐 Abriendo URL de nube: {url}")
            if sys.platform.startswith("darwin"):
                subprocess.call(["open", url])
            elif sys.platform.startswith("win"):
                subprocess.call(["start", url], shell=True)
            else:
                subprocess.call(["xdg-open", url])
        except Exception as e:
            QMessageBox.warning(self, "Error", f"No se pudo abrir la URL:\n{e}")

    def emitir_confirmacion_eliminacion(self, publicacion):
        respuesta = QMessageBox.question(
            self,
            "Delete post",
            "Are you sure you want to delete this post permanently?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.confirmar_eliminacion.emit(publicacion)

    def mostrar_mensaje_info(self, titulo, mensaje):
        QMessageBox.information(self, titulo, mensaje)

    def mostrar_mensaje_error(self, titulo, mensaje):
        QMessageBox.critical(self, titulo, mensaje)