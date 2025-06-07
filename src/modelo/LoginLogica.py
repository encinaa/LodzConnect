
import re
from src.utils.singleton import singleton
from src.modelo.vo.LoginVO import LoginVO
from src.utils.seguridad_utils import verificar_contraseña

@singleton #utils
class LoginLogica:
    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao

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
