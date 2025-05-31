from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.UsuarioDAO import UsuarioDAO  # Acceso a datos
from src.modelo.vo.UsuarioVO import UsuarioVO  # Objeto de valor

class ControladorMiPerfil(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
        self.correo_usuario = correo_usuario
        self.usuario_dao = UsuarioDAO()  # Instancia del DAO
        self.usuario_vo = None  # Objeto de valor del usuario
        
        # Conectar señales
        self._vista.editar_perfil_clicked.connect(self.editar_perfil)
        self.cargar_datos_perfil()

    def cargar_datos_perfil(self):
        """Carga los datos del usuario usando el DAO"""
        try:
            # Obtener el VO del usuario desde la tabla Usuario
            self.usuario_vo = self.usuario_dao.obtener_por_correo(self.correo_usuario)

            if self.usuario_vo:
                #self._vista.label_correo.setText(self.usuario_vo.correo)

                # Obtener nombre y edad desde la tabla Estudiantes
                datos_estudiante = self.usuario_dao.obtener_datos_estudiante(self.correo_usuario)
                if datos_estudiante:
                    nombre, edad = datos_estudiante
                    self._vista.label_Usuario.setText(nombre)
                    self._vista.label_Edad.setText(str(edad))
                else:
                    self._vista.label_Usuario.setText("Desconocido")
                    self._vista.label_Edad.setText("-")
        except Exception as e:
            print(f"Error al cargar perfil: {e}")
            # QMessageBox de error si quieres

    def editar_perfil(self):
        """Maneja la navegación a editar perfil"""
        from src.controlador.ControladorEditarPerfil import ControladorEditarPerfil
        from src.vista.EditarPerfil import EditarPerfil
        
        vista_editar = EditarPerfil()
        controlador_editar = ControladorEditarPerfil(
            vista_editar, 
            self.usuario_vo.correo 
        )
        
        vista_editar.setWindowModality(2)  # Modal
        vista_editar.show()
        self._vista.close()
      
        '''if hasattr(vista_editar, 'perfil_actualizado'):
            vista_editar.perfil_actualizado.connect(self.cargar_datos_perfil)'''
