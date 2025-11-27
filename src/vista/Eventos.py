from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import pyqtSignal, Qt, QUrl
from PyQt5 import uic
from PyQt5.QtGui import QDesktopServices
from src.vista.VistaNavegable import VistaNavegable
import os
import sys
import logging

# Use an absolute path or ensure the working directory is correct when loading .ui
Form, _ = uic.loadUiType(os.path.join("src", "vista", "Ui", "Eventos.ui"))

logger = logging.getLogger(__name__)

class Eventos(VistaNavegable, Form):
    actualizar_publicaciones_clicked = pyqtSignal()
    confirmar_eliminacion = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

        boton_actualizar = self.findChild(QPushButton, "BotonActualizar")
        if boton_actualizar:
            logger.debug("Botón 'Actualizar' encontrado, conectando señal...")
            boton_actualizar.clicked.connect(self._on_actualizar_clicked)
        else:
            logger.warning("Botón 'Actualizar' NO encontrado - revisa el nombre en el .ui")

        # Buscar el contenedor y layout por sus nombres exactos
        self.contenedor_publicaciones = self.findChild(QWidget, "contenedorEventos")
        if self.contenedor_publicaciones:
            logger.debug("Contenedor 'contenedorEventos' encontrado")
            # Prefer container.layout() as layouts can be tricky to find by name
            self.layout_publicaciones = getattr(self, "layoutPublicaciones", None) or self.contenedor_publicaciones.layout()
            if self.layout_publicaciones:
                logger.debug("Layout de publicaciones obtenido")
            else:
                logger.debug("No se pudo obtener el layout, creando uno nuevo")
                self.layout_publicaciones = QVBoxLayout()
                self.layout_publicaciones.setContentsMargins(10, 10, 10, 10)
                self.layout_publicaciones.setSpacing(10)
                self.contenedor_publicaciones.setLayout(self.layout_publicaciones)
        else:
            logger.error("Contenedor 'contenedorEventos' NO encontrado")
            self.layout_publicaciones = None

    def _on_actualizar_clicked(self):
        """Emitir señal cuando se haga click"""
        logger.debug("_on_actualizar_clicked called")
        self.actualizar_publicaciones_clicked.emit()

    def mostrar_lista_publicaciones(self, publicaciones, correo_usuario, callback_perfil, callback_eliminar):
        logger.debug("mostrar_lista_publicaciones: %d publicaciones, usuario=%s", len(publicaciones), correo_usuario)

        layout = self.layout_publicaciones
        if not layout:
            logger.warning("Layout no disponible, abortando mostrar lista")
            return

        # Limpiar publicaciones anteriores
        self._limpiar_layout(layout)

        publicaciones_propias = [pub for pub in publicaciones if pub.cuentaOrigen == correo_usuario]
        logger.debug("Publicaciones propias: %d", len(publicaciones_propias))

        if not publicaciones_propias:
            label_vacio = QLabel("You haven't made any posts yet")
            label_vacio.setAlignment(Qt.AlignCenter)
            label_vacio.setStyleSheet("""
                QLabel {
                    color: #666; 
                    font-style: italic; 
                    padding: 40px; 
                    font-size: 16px;
                    background-color: transparent;
                    border: 2px dashed #ccc;
                    border-radius: 8px;
                    margin: 20px;
                }
            """)
            label_vacio.setMinimumHeight(200)
            label_vacio.setMinimumWidth(400)
            layout.addWidget(label_vacio)
            label_vacio.show()
            if self.contenedor_publicaciones:
                self.contenedor_publicaciones.show()
        else:
            for pub in publicaciones_propias:
                widget = self.crear_widget_publicacion(pub, correo_usuario, callback_perfil, callback_eliminar)
                layout.addWidget(widget)

        # Force redraw
        layout.update()
        if self.contenedor_publicaciones:
            self.contenedor_publicaciones.update()
        self.update()
        logger.debug("UI actualizada")

    def _limpiar_layout(self, layout):
        """Remove all items/widgets from layout safely using takeAt."""
        count = layout.count()
        logger.debug("Limpieza de layout, items=%d", count)
        for i in range(count - 1, -1, -1):
            item = layout.takeAt(i)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                logger.debug("Eliminando widget: %s", widget)
                widget.setParent(None)
                widget.deleteLater()
            else:
                # item could be a nested layout or spacer
                logger.debug("Eliminando item no-widget")
                # If nested layout, try deleting its children too
                child_layout = item.layout()
                if child_layout:
                    self._limpiar_layout(child_layout)
                # no explicit delete needed for spacer

    def crear_widget_publicacion(self, publicacion, correo_usuario, callback_perfil, callback_eliminar):
        widget = QWidget()
        layout_general = QVBoxLayout(widget)

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

        fila_superior.addStretch()

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila_superior.addWidget(label_fecha)

        layout_general.addLayout(fila_superior)

        descripcion = (publicacion.descripcion or "").strip()

        if getattr(publicacion, 'tipo', None) == "nube":
            fila_archivo = QHBoxLayout()
            nombre_archivo = os.path.basename(descripcion or "")
            btn_archivo = QPushButton(f"📎 {nombre_archivo}")
            btn_archivo.setCursor(Qt.PointingHandCursor)
            btn_archivo.setStyleSheet("""
                QPushButton {
                    color: #007acc; 
                    border: none; 
                    text-decoration: underline; 
                    background: transparent;
                    text-align: left;
                    padding: 0px;
                }
                QPushButton:hover {
                    color: #005a9e;
                }
            """)
            # Use QDesktopServices for opening URLs (cross-platform)
            btn_archivo.clicked.connect(lambda _, url=publicacion.url: self._abrir_url_nube(url))
            fila_archivo.addWidget(btn_archivo)
            fila_archivo.addStretch()
            layout_general.addLayout(fila_archivo)
        else:
            label_desc = QLabel(f"💬 {descripcion}")
            label_desc.setWordWrap(True)
            label_desc.setStyleSheet("margin-top: 5px;")
            layout_general.addWidget(label_desc)

        widget.setStyleSheet("""
            QWidget {
                background-color: #f9f9f9;
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 10px;
                margin-bottom: 10px;
            }
        """)
        return widget

    def _abrir_url_nube(self, url):
        """Open cloud URL cross-platform via Qt (safer than subprocess)."""
        try:
            logger.debug("Abriendo URL: %s", url)
            if not url:
                raise ValueError("Empty URL")
            QDesktopServices.openUrl(QUrl(url))
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