# Crear un nuevo archivo: src/utils/auth_middleware.py
from src.utils.token_utils import verify_access_token, verify_refresh_token
from src.modelo.dao.RefreshTokenDAO import RefreshTokenDAO
import datetime


class AuthMiddleware:
    @staticmethod
    def verificar_token(access_token):
        """Verifica si el access token es válido"""
        if not access_token:
            return False, "Token requerido"
        
        valido, datos = verify_access_token(access_token)
        if not valido:
            return False, f"Token inválido: {datos}"
        
        return True, datos
    
    @staticmethod
    def renovar_token(refresh_token):
        """Renueva el access token usando refresh token"""
        # Verificar que el refresh token existe y no está revocado
        dao = RefreshTokenDAO()
        token_info = dao.existe_token(refresh_token)
        
        if not token_info:
            return False, "Refresh token no encontrado"
        
        revoked, expires_at = token_info
        if revoked:
            return False, "Refresh token revocado"
        
        # Verificar expiración
        if datetime.datetime.utcnow() > expires_at:
            return False, "Refresh token expirado"
        
        # Verificar firma del token
        valido, datos = verify_refresh_token(refresh_token)
        if not valido:
            return False, f"Refresh token inválido: {datos}"
        
        # Generar nuevo access token
        from src.utils.token_utils import create_access_token
        nuevo_access_token = create_access_token({"sub": datos["sub"]})
        
        return True, nuevo_access_token