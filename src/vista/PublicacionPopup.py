from PyQt5.QtWidgets import (
    QDialog, QListWidget, QListWidgetItem, QFileDialog,
    QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QMessageBox
)
from PyQt5.QtCore import pyqtSignal, Qt
import os

class PublicacionPopup(QDialog):
    """
    Popup to select files (default: PDFs), preview them in a list, remove selections,
    and "publish" (emits `archivos_subidos(list_of_paths)` and/or calls parent.on_archivos_subidos).
    """
    archivos_subidos = pyqtSignal(list)        # emitted when files are published
    archivos_actualizados = pyqtSignal(list)   # emitted when selection changes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("New Post")
        self.setModal(True)
        # remove context help button
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(560, 420)

        self.label_titulo = QLabel("New Post")
        self.label_titulo.setStyleSheet("font: 14pt 'Century'; color: #2e7d32;")

        self.lista = QListWidget()
        self.lista.setSelectionMode(QListWidget.ExtendedSelection)

        self.boton_subir = QPushButton("Select files")
        self.boton_publicar = QPushButton("Upload and publish")
        self.boton_eliminar = QPushButton("Delete selected")
        self.boton_cerrar = QPushButton("Close")

        # Layouts
        h_top = QHBoxLayout()
        h_top.addWidget(self.boton_subir)
        h_top.addWidget(self.boton_eliminar)
        h_top.addStretch()
        h_top.addWidget(self.boton_publicar)
        h_top.addWidget(self.boton_cerrar)

        layout = QVBoxLayout()
        layout.addWidget(self.label_titulo)
        layout.addLayout(h_top)
        layout.addWidget(self.lista)
        self.setLayout(layout)

        # State
        self._rutas = []

        # Connections
        self.boton_subir.clicked.connect(self.select_files)
        self.boton_eliminar.clicked.connect(self.delete_selected)
        self.boton_cerrar.clicked.connect(self.reject)
        self.boton_publicar.clicked.connect(self.publish)

        # Cursors
        for b in (self.boton_subir, self.boton_publicar, self.boton_eliminar, self.boton_cerrar):
            b.setCursor(Qt.PointingHandCursor)

    def mostrar_mensaje(self, tipo, titulo, mensaje):
        """tipo: 'error' or 'information' (case-insensitive)"""
        t = (tipo or "").lower()
        if t == "error":
            QMessageBox.critical(self, titulo, mensaje)
        else:
            QMessageBox.information(self, titulo, mensaje)

    def select_files(self):
        archivos, _ = QFileDialog.getOpenFileNames(
            self, "Select files (PDF)", os.getcwd(),
            "PDF Files (*.pdf);;All Files (*)"
        )
        if not archivos:
            return
        añadidos = []
        for ruta in archivos:
            if ruta not in self._rutas:
                self._rutas.append(ruta)
                self.add_to_list(ruta)
                añadidos.append(ruta)
        if añadidos:
            self.archivos_actualizados.emit(self._rutas.copy())

    def add_to_list(self, ruta):
        nombre = os.path.basename(ruta)
        item = QListWidgetItem(nombre)
        item.setData(Qt.UserRole, ruta)
        self.lista.addItem(item)

    def delete_selected(self):
        seleccion = self.lista.selectedItems()
        if not seleccion:
            return
        # Iterate over a snapshot of selected items and remove them safely
        for item in seleccion:
            ruta = item.data(Qt.UserRole)
            row = self.lista.row(item)
            # remove the item from the widget; returned item can be discarded
            self.lista.takeItem(row)
            if ruta in self._rutas:
                self._rutas.remove(ruta)
        self.archivos_actualizados.emit(self._rutas.copy())

    def cargar_lista(self, rutas):
        """Replace current list with provided rutas (list of file paths)."""
        self.lista.clear()
        self._rutas = []
        for r in rutas:
            if r not in self._rutas:
                self._rutas.append(r)
                self.add_to_list(r)
        self.archivos_actualizados.emit(self._rutas.copy())

    def obtener_rutas(self):
        return self._rutas.copy()

    def publish(self):
        rutas_a_publicar = list(self._rutas)  # defensive copy

        if not rutas_a_publicar:
            QMessageBox.information(self, "No files", "No selected files to publish")
            return

        # Emit a signal for other parts of the app to react
        self.archivos_subidos.emit(rutas_a_publicar)

        # Try calling a parent callback if available (keeps behavior compatible
        # with code that used the commented implementation)
        parent = self.parent()
        if parent and hasattr(parent, "on_archivos_subidos"):
            try:
                parent.on_archivos_subidos(rutas_a_publicar)
            except Exception:
                # Don't block UI if parent handler fails
                pass

        # Close popup after publishing
        self.accept()