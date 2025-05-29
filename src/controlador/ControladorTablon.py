from src.controlador.ControladorBaseNavegable import ControladorBaseNavegable

class ControladorTablon(ControladorBaseNavegable):
    def __init__(self, vista, correo_usuario):
        super().__init__(vista, correo_usuario)
