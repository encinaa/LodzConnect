from src.vista.Login import Login
from src.vista.Registro import Registro
from src.controlador.ControladorLogin import ControladorLogin
from src.controlador.ControladorRegistro import ControladorRegistro

class ControladorPaginaPrincipal:
    def __init__(self, vista):
        self._vista = vista

        # Conectar las señales de la vista a los métodos
        self._vista.iniciar_clicked.connect(self.abrir_login)
        self._vista.registrarse_clicked.connect(self.abrir_registro)

        # Mantener referencias para ventanas hijas
        self.ventana_login = None
        self.ventana_registro = None

    def abrir_login(self):
        self.ventana_login = Login()
        self.controlador_login = ControladorLogin(self.ventana_login)

        # Pasar la vista actual para poder volver desde el login
        self.controlador_login.set_pagina_principal(self._vista)

        self.ventana_login.show()
        self._vista.hide()

    def abrir_registro(self):
        self.ventana_registro = Registro()
        self.controlador_registro = ControladorRegistro(self.ventana_registro)

        # Permite que Registro pueda volver a esta vista
        self.controlador_registro.set_pagina_principal(self._vista)

        self.ventana_registro.show()
        self._vista.hide()
