from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.modelo.dao.EstudianteDAO import EstudianteDAO
from src.modelo.dao.PerfilDAO import PerfilDAO

class ControladorPerfilOtro:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()
        self.estudiante_dao = EstudianteDAO()
        self.perfil_dao = PerfilDAO()

        # Conectar botón de volver
        self._vista.volver_clicked.connect(self.volver_a_tablon)

        # Cargar información en la vista
        self.cargar_datos_perfil()

    def cargar_datos_perfil(self):
        try:
            usuario = self.usuario_dao.obtener_por_correo(self.correo_usuario)

            if usuario:
                datos_estudiante = self.estudiante_dao.obtener_datos_estudiante(self.correo_usuario)
                if datos_estudiante:
                    nombre, edad = datos_estudiante
                    self._vista.mostrar_nombre(nombre)
                    self._vista.mostrar_edad(edad)
                else:
                    self._vista.mostrar_nombre("Desconocido")
                    self._vista.mostrar_edad("-")

                datos_perfil = self.perfil_dao.obtener_datos_perfil(self.correo_usuario)
                if datos_perfil:
                    descripcion, actividades, _ = datos_perfil
                    self._vista.mostrar_descripcion(descripcion or "Sin descripción")
                    self._vista.mostrar_actividades(actividades or "Sin actividades")
                else:
                    self._vista.mostrar_descripcion("Sin descripción")
                    self._vista.mostrar_actividades("Sin actividades")
        except Exception as e:
            print(f"Error al cargar el perfil de otro usuario: {e}")

    def volver_a_tablon(self):
        from src.vista.Tablon import Tablon
        from src.controlador.ControladorTablon import ControladorTablon

        self.vista_tablon = Tablon()
        self.controlador_tablon = ControladorTablon(self.vista_tablon, self.correo_usuario)
        self.vista_tablon.show()
        self._vista.close()

