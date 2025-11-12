from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable
from src.modelo.dao.EventoDAO import EventoDAO
from src.modelo.EventoLogica import EventoLogica
from src.utils.auth_middleware import AuthMiddleware
from datetime import datetime

class ControladorEventos(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario, access_token=None):
        # Llama al constructor del padre pasando TODOS los parámetros
        super().__init__(vista, correo_usuario, access_token)
        
        # Inicializa el middleware de autenticación
        self.auth_middleware = AuthMiddleware()
        
        #self.evento_dao = EventoDAO()
        #self.logica = EventoLogica(self.evento_dao)

        #self._vista.apuntarse_solicitado.connect(self.apuntarse_evento)
        #self._vista.desapuntarse_solicitado.connect(self.desapuntarse_evento)
        #self.mostrar_eventos()

    def _verificar_autenticacion(self):
        """Verifica que el usuario esté autenticado"""
        if not self.access_token:
            self._vista.mostrar_mensaje_error("Error", "No hay token de acceso")
            return False
        
        valido, datos = self.auth_middleware.verificar_token(self.access_token)
        if not valido:
            self._vista.mostrar_mensaje_error("Sesión expirada", "Por favor, inicie sesión nuevamente")
            return False
        return True

    # Tus métodos comentados aquí...
    """
    def apuntarse_evento(self, evento):
        # Verificar autenticación primero
        if not self._verificar_autenticacion():
            return
            
        exito, mensaje = self.logica.apuntarse(evento)
        if exito:
            self._vista.mostrar_mensaje_info(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

    def desapuntarse_evento(self, evento):
        # Verificar autenticación primero
        if not self._verificar_autenticacion():
            return
            
        exito, mensaje = self.logica.desapuntarse(evento)
        if exito:
            self._vista.mostrar_mensaje_info(mensaje)
            self.mostrar_eventos()
        else:
            self._vista.mostrar_mensaje_error(mensaje)

    def mostrar_eventos(self):
        # Verificar autenticación primero
        if not self._verificar_autenticacion():
            return
            
        eventos = self.evento_dao.obtener_todos_eventos()
        eventos_ordenados = sorted(eventos, key=lambda e: (
            datetime.strptime(e.fecha, "%Y-%m-%d").date(),
            datetime.strptime(e.hora, "%H:%M:%S").time()
        ))
        self._vista.mostrar_eventos(eventos_ordenados)
    """