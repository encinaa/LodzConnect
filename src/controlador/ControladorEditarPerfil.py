"""














INUTIL


























"""
from src.modelo.dao.EstudianteDAO import EstudianteDAO
from src.modelo.dao.PerfilDAO import PerfilDAO
from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable


class ControladorEditarPerfil(ControladorBaseNavegable):
    def __init__(self, vista, usuario_vo):
        super().__init__(vista, usuario_vo.correo)
        self.usuario_vo = usuario_vo
        self.estudiante_dao = EstudianteDAO()
        self.perfil_dao = PerfilDAO()

        self._vista.guardar_clicked.connect(self.guardar_perfil)

        # Cargar datos del estudiante
        datos_estudiante = self.estudiante_dao.obtener_datos_estudiante(usuario_vo.correo)
        if datos_estudiante:
            nombre, edad = datos_estudiante
            self._vista.establecer_nombre(nombre)
            self._vista.establecer_edad(int(edad))
        else:
            self._vista.establecer_nombre("Desconocido")
            self._vista.establecer_edad(0)

        # Cargar datos del perfil
        perfil = self.perfil_dao.obtener_datos_perfil(usuario_vo.correo)
        if perfil:
            descripcion, actividades, _ = perfil
            self._vista.establecer_descripcion(descripcion or "")
            #self._vista.establecer_actividades(actividades or "")


    def guardar_perfil(self):
        nuevo_usuario = self._vista.obtener_nombre()
        nueva_edad = self._vista.obtener_edad()
        nueva_descripcion = self._vista.obtener_descripcion()
        #nuevas_actividades = self._vista.obtener_actividades()

        if not nuevo_usuario.strip():
            self._vista.mostrar_mensaje_error("User name must be fullfilled.")
            return

        self.estudiante_dao.actualizar_estudiante(self.usuario_vo.correo, nuevo_usuario, nueva_edad)
        self.perfil_dao.actualizar_perfil(self.usuario_vo.correo, nueva_descripcion)

        # Volver a MiPerfil
        from src.vista.MiPerfil import MiPerfil
        from src.controlador.ControladorMiPerfil import ControladorMiPerfil

        self.vista_mi_perfil = MiPerfil()
        self.controlador_mi_perfil = ControladorMiPerfil(self.vista_mi_perfil, self.usuario_vo.correo)
        self._vista.close()
        self.vista_mi_perfil.show()
