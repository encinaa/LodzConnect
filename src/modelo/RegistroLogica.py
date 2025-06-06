import re
from src.modelo.vo.EstudianteVO import EstudianteVO
from src.utils.email_utils import enviar_correo 
import os
from src.utils.seguridad_utils import hashear_contraseña


class RegistroLogica:
    def __init__(self, usuario_dao, estudiante_dao):
        self.usuario_dao = usuario_dao
        self.estudiante_dao = estudiante_dao

    def registrar_usuario(self, correo, contraseña, confirmar, nombre, edad):
        if not nombre.strip() or not edad.strip():
            return False, "Por favor, complete el nombre y la edad."

        if not edad.isdigit() or int(edad) <= 0:
            return False, "Por favor, introduzca una edad válida."

        if contraseña != confirmar:
            return False, "Las contraseñas no coinciden."

        if not self.validar_correo(correo):
            return False, "Por favor introduzca un correo institucional de estudiante (@estudiantes.unileon.es)."

        if not self.validar_contraseña(contraseña):
            return False, "Por favor introduzca una contraseña válida (mínimo 8 caracteres, una mayúscula y al menos un número)."

        if self.usuario_dao.existe_usuario(correo):
            return False, "El usuario ya está registrado."

        contraseña_hash = hashear_contraseña(contraseña)
        estudiante = EstudianteVO(correo, contraseña_hash, nombre, edad)
        self.estudiante_dao.insertar_estudiante(estudiante)

        self.enviar_correo_confirmacion(correo)

        return True, "Usuario registrado correctamente. Revisa tu correo."

    def validar_correo(self, correo):
        return re.match(r"[^@]+@estudiantes\.unileon\.es$", correo)

    def validar_contraseña(self, contraseña):
        return (
            len(contraseña) >= 8 and
            re.search(r"[A-Z]", contraseña) and
            re.search(r"\d", contraseña)
        )

    def enviar_correo_confirmacion(self, destinatario):
        api_key = os.environ.get("SENDGRID_API_KEY")
        print(f"API KEY: {api_key}")
        asunto = "Confirmación de cuenta"
        cuerpo = f"""
<html>
  <body style="font-family: Arial, sans-serif; color: #333;">
    <div style="max-width: 600px; margin: auto;">
      <h2 style="color: #0066cc;">¡Bienvenido a UniConecta!</h2>
      <p>Gracias por registrarte. Tu cuenta ha sido creada con éxito.</p>
      <p>Estamos encantados de tenerte con nosotros.</p>
      <br>
      <p>El equipo de UniConecta</p>
    </div>
  </body>
</html>
"""

        try:
            status = enviar_correo(destinatario, asunto, cuerpo)
            return status
        except Exception as e:
            print(f"Error al enviar correo: {e}")
            return None
