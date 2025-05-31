from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.modelo.dao.EstudianteDAO import EstudianteDAO
from src.modelo.dao.PerfilDAO import PerfilDAO
from src.modelo.vo.UsuarioVO import UsuarioVO


class ControladorMiPerfil(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()
        self.estudiante_dao = EstudianteDAO()
        self.perfil_dao = PerfilDAO()
        self.usuario_vo = None

        # Conectar señales
        self._vista.editar_perfil_clicked.connect(self.editar_perfil)
        self.cargar_datos_perfil()

    def cargar_datos_perfil(self):
        """Carga los datos del usuario usando los DAOs"""
        try:
            self.usuario_vo = self.usuario_dao.obtener_por_correo(self.correo_usuario)

            if self.usuario_vo:
                # Obtener nombre y edad desde Estudiantes
                datos_estudiante = self.estudiante_dao.obtener_datos_estudiante(self.correo_usuario)
                if datos_estudiante:
                    nombre, edad = datos_estudiante
                    self._vista.label_Usuario.setText(nombre)
                    self._vista.label_Edad.setText(str(edad))
                else:
                    self._vista.label_Usuario.setText("Desconocido")
                    self._vista.label_Edad.setText("-")

                # Obtener descripción y actividades desde perfil
                datos_perfil = self.perfil_dao.obtener_datos_perfil(self.correo_usuario)
                if datos_perfil:
                    descripcion, lista_actividades, _ = datos_perfil
                    self._vista.label_Descripcion.setText(descripcion or "Sin descripción")
                    self._vista.ListaActividades.setText(lista_actividades or "Sin actividades")
                else:
                    self._vista.label_Descripcion.setText("Sin descripción")
                    self._vista.ListaActividades.setText("Sin actividades")

        except Exception as e:
            print(f"Error al cargar perfil: {e}")

    def editar_perfil(self):
        """Maneja la navegación a editar perfil"""
        from src.controlador.ControladorEditarPerfil import ControladorEditarPerfil
        from src.vista.EditarPerfil import EditarPerfil

        self.vista_editar = EditarPerfil()
        self.controlador_editar = ControladorEditarPerfil(
            self.vista_editar,
            self.usuario_vo
        )

        self.vista_editar.setWindowModality(2)
        self.vista_editar.show()
        self._vista.close()
