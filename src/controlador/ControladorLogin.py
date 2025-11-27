from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.modelo.LoginLogica import LoginLogica
from src.vista.Tablon import Tablon
from src.controlador.ControladorTablon import ControladorTablon
from src.utils.token_utils import create_access_token, create_refresh_token
from src.modelo.dao.RefreshTokenDAO import RefreshTokenDAO
import datetime
from src.app import App


class ControladorLogin:
    def __init__(self, vista):
        self._vista = vista
        self.vista_principal = None
        self.ventana_tablon = None
        self.usuario_dao = UsuarioDAO()
        self.logica = LoginLogica(self.usuario_dao)

        # Conectar las señales de la vista
        self._vista.aceptar_clicked.connect(self.on_login_clicked)
        self._vista.volver_clicked.connect(self.on_volver_clicked)
        #self._vista.recuperar_clicked.connect(self.on_recuperar_clicked)

    def set_pagina_principal(self, vista_principal):
        self.vista_principal = vista_principal

    def on_login_clicked(self):
        correo = self._vista.iniciarSesion_correo.text()
        contraseña = self._vista.iniciarSesion_contrasena.text()

        # Primero autenticar para determinar tipo de usuario
        exito, tipo_usuario = self.logica.autenticar_usuario(correo, contraseña)
        
        if exito:
            # Ahora hacer login completo para obtener tokens
            exito_login, tokens = self.logica.login(correo, contraseña)
            
            if exito_login:
                print("✓ TOKENS GENERADOS:")
                print(f"Access: {tokens['access_token']}")
                print(f"Refresh: {tokens['refresh_token']}")
                
                # Guardar tokens
                self._guardar_tokens(tokens['access_token'], tokens['refresh_token'])
                
                # Verificar que se guardaron en App
                print(f"✓ En App - Access: {App().get_access_token() is not None}")
                print(f"✓ En App - Refresh: {App().get_refresh_token() is not None}")
                
                # Redirigir según tipo de usuario
                if tipo_usuario == "estudiante":
                    self.ventana_tablon = Tablon()
                    # Pasar el access_token al controlador
                    self.controlador_tablon = ControladorTablon(self.ventana_tablon, correo, tokens['access_token'])
                    self.ventana_tablon.show()
                else:
                    self._vista.mostrar_mensaje_error("Error", "User type unknown.")
                    return
                self._vista.close()
            else:
                self._vista.mostrar_mensaje_error("Login Error", tokens)  # tokens contiene el mensaje de error
        else:
            self._vista.mostrar_mensaje_error("Authentication error", tipo_usuario)

    def on_volver_clicked(self):
        if self.vista_principal is not None:
            self.vista_principal.show()
        self._vista.close()

    """
    def on_recuperar_clicked(self):
        correo = self._vista.iniciarSesion_correo.text()
        print(f"Recuperar contraseña para: {correo}")
        self._vista.mostrar_mensaje_advertencia(
            "Recuperación de contraseña",
            f"Para recuperar su contraseña asociada a {correo}, por favor pase por secretaría."
        )
    """

    def _guardar_tokens(self, access_token, refresh_token):
        """Guarda los tokens en el almacenamiento de la aplicación"""
        # Opción 1: Guardar en variables de instancia (simple)
        self.access_token = access_token
        self.refresh_token = refresh_token
        
        # Opción 2: Guardar en sesión si estás usando web.py
        try:
            import web
            web.ctx.session.access_token = access_token
            web.ctx.session.refresh_token = refresh_token
        except:
            pass
        
        # Opción 3: Guardar en configuración global de la app
        App().set_tokens(access_token, refresh_token)
        
        print(f"Tokens guardados - Access: {access_token[:20]}... Refresh: {refresh_token[:20]}...")

    def _generar_tokens(self, correo):
        """Genera access y refresh tokens para el usuario"""
        payload = {"sub": correo}
        access_token = create_access_token(payload)
        refresh_token = create_refresh_token(payload)
        
        # Guardar refresh token en la base de datos
        dao = RefreshTokenDAO()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
        dao.insertar_refresh(refresh_token, correo, expires)
        
        return access_token, refresh_token

    def get_access_token(self):
        """Obtiene el access token actual"""
        try:
            return getattr(self, 'access_token', None)
        except:
            return getattr(self, 'access_token', None)

    def get_refresh_token(self):
        """Obtiene el refresh token actual"""
        try:
            return getattr(self, 'refresh_token', None)
        except:
            return getattr(self, 'refresh_token', None)