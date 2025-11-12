from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.utils.seguridad_utils import verificar_contraseña
from src.utils.token_utils import create_access_token, create_refresh_token
from src.modelo.dao.RefreshTokenDAO import RefreshTokenDAO
from src.modelo.vo.LoginVO import LoginVO
import datetime
import re

class LoginLogica:
    def __init__(self, usuario_dao):
        self.usuario_dao = UsuarioDAO()

    def validar_correo(self, correo):
        return re.match(r"[^@]+@(estudiantes\.)?unileon\.es$", correo)

    def autenticar_usuario(self, correo, contraseña):
        if not self.validar_correo(correo):
            return False, "Debes usar un correo institucional válido: usuario@estudiantes.unileon.es o usuario@unileon.es"

        if len(correo.strip()) <= 3:
            return False, "Correo inválido."

        loginVO = LoginVO(correo, contraseña)
        if not self.usuario_dao.existe_usuario(loginVO.correo):
            return False, "El usuario no está registrado."

        contraseña_hash = self.usuario_dao.obtener_contraseña(correo)
        if not contraseña_hash or not verificar_contraseña(contraseña, contraseña_hash):
            return False, "Contraseña incorrecta."
        
        # ¡¡¡¡¡Determinar si es estudiante o administrador por el correo
        if "@estudiantes.unileon.es" in correo:
            return True, "estudiante"
        elif "@unileon.es" in correo:
            return True, "administrador"
        else:
            return False, "Tipo de usuario no reconocido."

    def login(self, correo, contraseña):
        user = self.usuario_dao.obtener_usuario_por_correo(correo)
        if not user:
            return False, "Usuario no encontrado"

        if verificar_contraseña(contraseña, user[1]):
            # Generar tokens
            payload = {"sub": correo}
            access_token = create_access_token(payload)
            refresh_token = create_refresh_token(payload)

            # Guardar refresh token
            dao = RefreshTokenDAO()
            expires = datetime.datetime.utcnow() + datetime.timedelta(days=7)
            dao.insertar_refresh(refresh_token, correo, expires)

            # Retornar tokens
            return True, {"access_token": access_token, "refresh_token": refresh_token}
        else:
            return False, "Contraseña incorrecta"