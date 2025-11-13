from PyQt5.QtWidgets import QPushButton, QMessageBox, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QScrollArea
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable
import os
import subprocess
import sys

Form, _ = uic.loadUiType("./src/vista/Ui/Eventos.ui")

class Eventos(VistaNavegable, Form):
<<<<<<< HEAD
    # Señal que solicita la eliminación de una publicación (emite el objeto PublicacionVO)
    eliminar_publicacion_solicitada = pyqtSignal(object)
=======
    actualizar_publicaciones_clicked = pyqtSignal()
    confirmar_eliminacion = pyqtSignal(object)
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()

<<<<<<< HEAD
    def mostrar_publicaciones(self, lista_publicaciones, correo_usuario):
        """
        Muestra una lista de PublicacionVO en el contenedor de la UI.
        lista_publicaciones: lista de objetos con atributos idPublic, fecha, cuentaOrigen, descripcion
        correo_usuario: email del usuario actual, usado para mostrar el botón eliminar cuando corresponde.
        """
        contenedor = self.findChild(QWidget, "contenedorEventos")
        if contenedor is None:
=======
        boton_actualizar = self.findChild(QPushButton, "BotonActualizar")
        if boton_actualizar:
            print("✅ Botón 'Actualizar' encontrado, conectando señal...")
            boton_actualizar.clicked.connect(self._on_actualizar_clicked)
        else:
            print("❌ Botón 'Actualizar' NO encontrado - revisa el nombre en el .ui")

        # Buscar el contenedor y layout por sus nombres exactos
        self.contenedor_publicaciones = self.findChild(QWidget, "contenedorEventos")
        if self.contenedor_publicaciones:
            print("✅ Contenedor 'contenedorEventos' encontrado")
            
            # Buscar el layout por su nombre
            self.layout_publicaciones = self.findChild(QVBoxLayout, "layoutPublicaciones")
            if self.layout_publicaciones:
                print("✅ Layout 'layoutPublicaciones' encontrado directamente")
            else:
                # Si no se encuentra por nombre, usar el layout del contenedor
                self.layout_publicaciones = self.contenedor_publicaciones.layout()
                if self.layout_publicaciones:
                    print("✅ Layout obtenido del contenedor")
                else:
                    print("❌ No se pudo obtener el layout, creando uno nuevo")
                    self.layout_publicaciones = QVBoxLayout()
                    self.layout_publicaciones.setContentsMargins(10, 10, 10, 10)
                    self.layout_publicaciones.setSpacing(10)
                    self.contenedor_publicaciones.setLayout(self.layout_publicaciones)
        else:
            print("❌❌❌ Contenedor 'contenedorEventos' NO encontrado")

    def _on_actualizar_clicked(self):
        """Método interno que emite la señal cuando se hace click"""
        print("🔄 clicked - emitiendo señal...")
        self.actualizar_publicaciones_clicked.emit()

    def mostrar_lista_publicaciones(self, publicaciones, correo_usuario, callback_perfil, callback_eliminar):
        print(f"🎯 ENTRANDO a mostrar_lista_publicaciones")
        print(f"   - Publicaciones recibidas: {len(publicaciones)}")
        print(f"   - Correo usuario: {correo_usuario}")
        
        if not hasattr(self, 'layout_publicaciones') or not self.layout_publicaciones:
            print("❌❌❌ Layout no disponible")
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca
            return

        layout = self.layout_publicaciones
        print(f"📦 Estado inicial del layout: {layout.count()} elementos")

        # Limpiar publicaciones anteriores
        self._limpiar_layout(layout)

<<<<<<< HEAD
        # Añadir publicaciones
        for pub in lista_publicaciones:
            widget_pub = self.crear_widget_publicacion(pub, correo_usuario)
            layout.addWidget(widget_pub)

    def crear_widget_publicacion(self, publicacion, correo_usuario):
=======
        # Filtrar solo publicaciones propias
        publicaciones_propias = [pub for pub in publicaciones if pub.cuentaOrigen == correo_usuario]
        
        print(f"📝 Mostrando {len(publicaciones_propias)} publicaciones propias de {correo_usuario}")

        if not publicaciones_propias:
            print("👀 No hay publicaciones propias, mostrando mensaje vacío")
            
            # Crear y configurar el label
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
            
            print(f"📋 Antes de agregar label - elementos en layout: {layout.count()}")
            
            # Agregar al layout
            layout.addWidget(label_vacio)
            
            print(f"📋 Después de agregar label - elementos en layout: {layout.count()}")
            
            # Forzar visualización
            label_vacio.show()
            if hasattr(self, 'contenedor_publicaciones'):
                self.contenedor_publicaciones.show()
            
            print("✅ Label de vacío agregado y mostrado")
            
        else:
            print(f"📋 Hay {len(publicaciones_propias)} publicaciones, creando widgets...")
            for i, pub in enumerate(publicaciones_propias):
                print(f"  📄 Creando widget {i+1} para: {pub.cuentaOrigen}")
                widget = self.crear_widget_publicacion(pub, correo_usuario, callback_perfil, callback_eliminar)
                layout.addWidget(widget)

        # Forzar actualización
        layout.update()
        if hasattr(self, 'contenedor_publicaciones'):
            self.contenedor_publicaciones.update()
        self.update()
        
        print("🔄 Actualización de UI forzada")

    def _limpiar_layout(self, layout):
        """Limpia todos los widgets de un layout"""
        print(f"🧹 Limpiando layout con {layout.count()} elementos")
        
        # Remover todos los widgets
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item:
                widget = item.widget()
                if widget:
                    print(f"  🗑️ Eliminando widget: {widget}")
                    widget.setParent(None)
                    widget.deleteLater()
                else:
                    # Es un spacer o layout
                    layout.removeItem(item)
                    print(f"  🗑️ Eliminando item no-widget")

    def crear_widget_publicacion(self, publicacion, correo_usuario, callback_perfil, callback_eliminar):
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()
<<<<<<< HEAD
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

=======

        # Botón eliminar (siempre visible ya que son publicaciones propias)
        boton_eliminar = QPushButton("❌")
        boton_eliminar.setFixedSize(40, 40)
        boton_eliminar.setStyleSheet("color: red; border: none; font-weight: bold; padding-bottom: 3px;")
        boton_eliminar.setCursor(Qt.PointingHandCursor)
        boton_eliminar.clicked.connect(lambda _, pub=publicacion: callback_eliminar(pub))
        fila_superior.addWidget(boton_eliminar)

        # Botón del usuario origen (siempre será el usuario actual)
        boton_origen = QPushButton(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("border: none; color: #007acc; text-align: left;")
        boton_origen.setCursor(Qt.PointingHandCursor)
        boton_origen.clicked.connect(lambda _, correo=publicacion.cuentaOrigen: callback_perfil(correo))
        fila_superior.addWidget(boton_origen)

        fila_superior.addStretch()

        # Fecha
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca
        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        fila_superior.addWidget(label_fecha)

        layout_general.addLayout(fila_superior)

<<<<<<< HEAD
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
=======
        descripcion = (publicacion.descripcion or "").strip()
        
        # ✅ SIMPLIFICADO: Solo manejar nube y texto
        if hasattr(publicacion, 'tipo') and publicacion.tipo == "nube":
            # Archivo en la nube - mostrar como enlace clickeable
            fila_archivo = QHBoxLayout()
            nombre_archivo = os.path.basename(descripcion)
            
            # Botón que funciona como enlace
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
            btn_archivo.clicked.connect(lambda _, url=publicacion.url: self._abrir_url_nube(url))
            fila_archivo.addWidget(btn_archivo)
            
            fila_archivo.addStretch()
            layout_general.addLayout(fila_archivo)
            
        else:
            # Texto plano
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
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca
        """)
        return widget

<<<<<<< HEAD
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
=======
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
>>>>>>> facd77cd000b329d3d92f38676fc45344c8572ca
