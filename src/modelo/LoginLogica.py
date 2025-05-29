
import re
from src.modelo.vo.LoginVO import LoginVO

class LoginLogica:
    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao

    def validar_correo(self, correo):
        return re.match(r"[^@]+@(estudiantes\.)?unileon\.es$", correo)

    def autenticar_usuario(self, correo, contraseña):
        if not self.validar_correo(correo):
            return False, "Debes usar un correo institucional válido: usuario@estudiantes.unileon.es o usuario@estudiantes.unileon.es"

        if len(correo.strip()) <= 3:
            return False, "Correo inválido."

        loginVO = LoginVO(correo, contraseña)
        if not self.usuario_dao.existe_usuario(loginVO.correo):
            return False, "El usuario no está registrado."

        contraseña_real = self.usuario_dao.obtener_contraseña(loginVO.correo)
        if not contraseña_real or contraseña_real != loginVO.contraseña:
            return False, "Contraseña incorrecta."

        # ¡¡¡¡¡Determinar si es estudiante o administrador por el correo
        if "@estudiantes.unileon.es" in correo:
            return True, "estudiante"
        elif "@unileon.es" in correo:
            return True, "administrador"
        else:
            return False, "Tipo de usuario no reconocido."
