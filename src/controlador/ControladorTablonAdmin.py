from src.controlador.ControladorBaseNavegableAdmin import ControladorBaseNavegableAdmin
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

class ControladorTablonAdmin(ControladorBaseNavegableAdmin):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        #self._correo_usuario = correo_usuario #tengo q renombrarlo pq me daba error
        self.publicacion_dao = PublicacionDAO()
        self.configurar_layout_publicaciones()
        self.mostrar_publicaciones()
        self._vista.actualizar_publicaciones_clicked.connect(self.mostrar_publicaciones)


    def configurar_layout_publicaciones(self):
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor is None:
            print("No se encontró el widget 'contenedorPublicaciones'")
            return

        if contenedor.layout() is None:
            layout = QVBoxLayout()
            layout.setContentsMargins(10, 10, 10, 10)
            layout.setSpacing(10)
            contenedor.setLayout(layout)
            print("Layout asignado manualmente a 'contenedorPublicaciones'")
        

    def mostrar_publicaciones(self):
        publicaciones = self.publicacion_dao.obtener_todas_publicaciones()
        contenedor = self._vista.findChild(QWidget, "contenedorPublicaciones")
        if contenedor is None:
            print("No se encontró el widget 'contenedorPublicaciones'")
            return

        layout = contenedor.layout()
        if layout is None:
            print("El widget 'contenedorPublicaciones' no tiene un layout asignado")
            return

        # Limpiar publicaciones anteriores
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for pub in publicaciones:
            widget = self.crear_widget_publicacion(pub)
            layout.addWidget(widget)

    #PARA Q SALGA ELIMINAR TODAS
    def crear_widget_publicacion(self, publicacion):
        widget = QWidget()
        layout_general = QVBoxLayout()
        widget.setLayout(layout_general)

        fila_superior = QHBoxLayout()

        # Admin puede eliminar cualquier publicación
        boton_eliminar = QPushButton("❌")
        boton_eliminar.setFixedSize(40, 40)
        boton_eliminar.setStyleSheet("""
            color: red; 
            border: none; 
            font-weight: bold; 
            padding-bottom: 3px;
        """)
        boton_eliminar.setCursor(Qt.PointingHandCursor)
        boton_eliminar.clicked.connect(lambda _, pub=publicacion: self.confirmar_eliminacion(pub))
        fila_superior.addWidget(boton_eliminar)

        boton_origen = QPushButton(f"👤 {publicacion.cuentaOrigen}")
        boton_origen.setStyleSheet("border: none; color: #007acc; text-align: left;")
        boton_origen.setCursor(Qt.PointingHandCursor)

        label_fecha = QLabel(f"📅 {publicacion.fecha}")
        label_fecha.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

        fila_superior.addWidget(boton_origen)
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
 



    #popup para confirmar eliminacion
    def confirmar_eliminacion(self, publicacion):
        respuesta = QMessageBox.question(
            self._vista,
            "Eliminar publicación",
            "¿Estás seguro de que deseas eliminar esta publicación?",
            QMessageBox.Yes | QMessageBox.No
        )
        if respuesta == QMessageBox.Yes:
            self.publicacion_dao.eliminar_publicacion(publicacion.idPublic)
            self.mostrar_publicaciones()
            QMessageBox.information(
                self._vista,
                "Eliminado",
                "La publicación ha sido eliminada correctamente."
            )


"""
    def abrir_perfil_usuario(self, correo):
        from src.vista.MiPerfil import MiPerfil  # importa la vista
        from src.controlador.ControladorMiPerfil import ControladorMiPerfil  # importa el controlador

        vista_perfil = MiPerfil()
        controlador_perfil = ControladorMiPerfil(vista_perfil, correo)

        self.navegar_a(vista_perfil)

"""