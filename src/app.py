class App:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(App, cls).__new__(cls)
            cls._instance.access_token = None
            cls._instance.refresh_token = None
            cls._instance.correo_usuario = None  # ← AÑADE ESTO
        return cls._instance
    
    def set_tokens(self, access_token, refresh_token, correo_usuario=None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        if correo_usuario:
            self.correo_usuario = correo_usuario
    
    def get_access_token(self):
        return self.access_token
    
    def get_refresh_token(self):
        return self.refresh_token
    
    def get_correo_usuario(self):
        return self.correo_usuario
    
    def limpiar_sesion(self):
        """Limpia toda la sesión - útil para logout"""
        self.access_token = None
        self.refresh_token = None
        self.correo_usuario = None
        print("✓ Sesión limpiada en App")