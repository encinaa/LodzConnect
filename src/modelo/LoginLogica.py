
import re
from src.utils.singleton import singleton
from src.modelo.vo.LoginVO import LoginVO
from src.utils.seguridad_utils import verificar_contraseña

@singleton #utils
class LoginLogica:
    def __init__(self, usuario_dao):
        self.usuario_dao = usuario_dao

    def validar_correo(self, correo):
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', correo) 

    def autenticar_usuario(self, correo, contraseña):
        if not self.validar_correo(correo):
            return False, "Please use a valid email"

        if len(correo.strip()) <= 3:
            return False, "Invaled email."

        loginVO = LoginVO(correo, contraseña)
        if not self.usuario_dao.existe_usuario(loginVO.correo):
            return False, "User not registred."

        contraseña_hash = self.usuario_dao.obtener_contraseña(correo)
        if not contraseña_hash or not verificar_contraseña(contraseña, contraseña_hash):
            return False, "Wrong password."
        
        # ¡¡¡¡¡Determinar si es estudiante o administrador por el correo
        if "@gmail.com" in correo or "@outlook.com" in correo or "@hotmail.com" in correo:
            return True, "estudiante"
        elif "@unileon.es" in correo:
            return True, "administrador"
        else:
            return False, "Tipo de usuario no reconocido."
