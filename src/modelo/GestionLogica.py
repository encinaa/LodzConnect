import re
import random
import string
from src.modelo.dao.UsuarioDAO import UsuarioDAO
from src.modelo.dao.AdminDAO import AdminDAO
from src.modelo.dao.EstudianteDAO import EstudianteDAO

class GestionLogica:
    def __init__(self):
        self.usuario_dao = UsuarioDAO()
        self.admin_dao = AdminDAO()
        self.estudiante_dao = EstudianteDAO()

    def validar_correo_admin(self, correo):
        return re.match(r"[^@]+@unileon\.es$", correo) is not None

    def anadir_admin(self, correo):
        if not self.validar_correo_admin(correo):
            return False, "Correo inválido. Debe ser de dominio @unileon.es"
        if self.usuario_dao.existe_usuario(correo):
            return False, "El usuario ya existe en la base de datos."

        contraseña = self.generar_contraseña_segura()
        self.usuario_dao.insertar_usuario(correo, contraseña)
        self.admin_dao.insertar_admin(correo)
        return True, f"Administrador añadido correctamente.\nLa nueva contraseña es: {contraseña}"

    def eliminar_admin(self, correo):
        if correo == "master@unileon.es":
            return False, "No se puede eliminar al administrador principal (master)."
        if not self.validar_correo_admin(correo):
            return False, "Correo inválido. Debe ser de dominio @unileon.es"
        if not self.usuario_dao.existe_usuario(correo):
            return False, "El administrador no existe en la base de datos."
        
        eliminado_admin = self.admin_dao.eliminar_admin(correo)
        if eliminado_admin:
            self.usuario_dao.eliminar_usuario(correo)
            return True, "Administrador eliminado correctamente."
        else:
            return False, "No se encontró el administrador en la tabla correspondiente."


    #esq si el master añade los admins les tiene q dar una contraseña claro
    def generar_contraseña_segura(self, longitud=8):
        while True:
            contraseña = ''.join(random.choices(string.ascii_letters + string.digits, k=longitud))
            if (any(c.isupper() for c in contraseña) and any(c.islower() for c in contraseña)):
                return contraseña