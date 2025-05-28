from src.vista.EditarPerfil import EditarPerfil
from src.controlador.ControladorEditarPerfil import ControladorEditarPerfil




class ControladorMiPerfil:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.vista_anterior = None

        # Conectar señales
        self._vista.volver_clicked.connect(self.volver_a_tablon)
        self._vista.editar_perfil_clicked.connect(self.editar_perfil)

    def set_vista_anterior(self, vista_anterior):
        self.vista_anterior = vista_anterior

    def volver_a_tablon(self):
        if self.vista_anterior:
            self.vista_anterior.show()
        self._vista.close()

    def editar_perfil(self):
        self.ventana_editar = EditarPerfil()
        self.controlador_editar = ControladorEditarPerfil(self.ventana_editar, self.correo_usuario)
        self.controlador_editar.set_vista_anterior(self._vista)
        self.ventana_editar.show()
        self._vista.hide()
