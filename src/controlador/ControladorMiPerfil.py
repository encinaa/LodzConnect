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
            # 1. El DAO obtiene los datos de la base de datos
            self.usuario_vo = self.usuario_dao.obtener_por_correo(self.correo_usuario)
            
            if self.usuario_vo:
                # 2. Actualizar la vista con el VO
                self.vista.label_nombre.setText(self.usuario_vo.nombre)
                self.vista.label_correo.setText(self.usuario_vo.correo)
                # Puedes agregar más campos como:
                # self.vista.label_bio.setText(self.usuario_vo.biografia)
                
        except Exception as e:
            print(f"Error al cargar perfil: {e}")
            # Opcional: Mostrar QMessageBox de error

    def editar_perfil(self):
        """Maneja la navegación a editar perfil"""
        from src.controlador.ControladorEditarPerfil import ControladorEditarPerfil
        from src.vista.EditarPerfil import EditarPerfil
        
        vista_editar = EditarPerfil()
        controlador_editar = ControladorEditarPerfil(
            vista_editar, 
            self.usuario_vo  # Pasamos el VO completo
        )
        
        vista_editar.setWindowModality(2)  # Modal
        vista_editar.show()
        
        # Si EditarPerfil emite señal de actualización
        if hasattr(vista_editar, 'perfil_actualizado'):
            vista_editar.perfil_actualizado.connect(self.cargar_datos_perfil)