from src.modelo.dao.EstudianteDAO import EstudianteDAO
from src.modelo.dao.PerfilDAO import PerfilDAO
from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from PyQt5.QtWidgets import QMessageBox

class ControladorEditarPerfil(ControladorBaseNavegable):
    def __init__(self, vista, usuario_vo):
        super().__init__(vista, usuario_vo.correo)
        self._vista = vista
        self.usuario_vo = usuario_vo
        self.estudiante_dao = EstudianteDAO()
        self.perfil_dao = PerfilDAO()

        self._vista.guardar_clicked.connect(self.guardar_perfil)

        # Cargar datos del estudiante
        datos_estudiante = self.estudiante_dao.obtener_datos_estudiante(usuario_vo.correo)
        if datos_estudiante:
            nombre, edad = datos_estudiante
            self._vista.EditarUsuario.setText(nombre)
            self._vista.EditarEdad.setValue(int(edad))
        else:
            self._vista.EditarUsuario.setText("Desconocido")
            self._vista.EditarEdad.setValue(0)

        # Cargar perfil
        perfil = self.perfil_dao.obtener_datos_perfil(usuario_vo.correo)
        if perfil:
            descripcion, actividades, _ = perfil
            self._vista.EditarDescripcion.setPlainText(descripcion or "")
            self._vista.EditarActividades.setPlainText(actividades or "")

    def guardar_perfil(self):
        nuevo_usuario = self._vista.EditarUsuario.text()
        nueva_edad = self._vista.EditarEdad.value()
        nueva_descripcion = self._vista.EditarDescripcion.toPlainText()
        nuevas_actividades = self._vista.EditarActividades.toPlainText()

        if not nuevo_usuario.strip():
            QMessageBox.warning(self._vista, "Error", "El nombre de usuario no puede estar vacío.")
            return

        self.estudiante_dao.actualizar_estudiante(self.usuario_vo.correo, nuevo_usuario, nueva_edad)
        self.perfil_dao.actualizar_perfil(self.usuario_vo.correo, nueva_descripcion, nuevas_actividades)

        # Volver a MiPerfil
        from src.vista.MiPerfil import MiPerfil
        from src.controlador.ControladorMiPerfil import ControladorMiPerfil

        self.vista_mi_perfil = MiPerfil()
        self.controlador_mi_perfil = ControladorMiPerfil(self.vista_mi_perfil, self.usuario_vo.correo)
        self._vista.close()
        self.vista_mi_perfil.show()