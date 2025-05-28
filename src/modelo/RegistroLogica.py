
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from src.modelo.vo.EstudianteVO import EstudianteVO

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

        estudiante = EstudianteVO(correo, contraseña, nombre, edad)
        self.estudiante_dao.insertar_estudiante(estudiante)

        codigo = self.generar_codigoVerf()
        self.enviar_correo_confirmacion(correo, codigo)

        return True, "Usuario registrado correctamente. Revisa tu correo."

    def validar_correo(self, correo):
        return re.match(r"[^@]+@estudiantes\.unileon\.es$", correo)

    def validar_contraseña(self, contraseña):
        return (
            len(contraseña) >= 8 and
            re.search(r"[A-Z]", contraseña) and
            re.search(r"\d", contraseña)
        )

    def generar_codigoVerf(self, longitud=6):
        return ''.join(str(random.randint(0, 9)) for _ in range(longitud))

    def enviar_correo_confirmacion(self, destinatario, codigo):
        remitente = "uniconectaule@gmail.com"
        contraseña = "Asdfghj1"

        asunto = "Confirmación de cuenta"
        cuerpo = f"""
        ¡Hola!
        Gracias por registrarte. Tu código de confirmación es: {codigo}
        """

        mensaje = MIMEMultipart()
        mensaje['From'] = remitente
        mensaje['To'] = destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo, 'plain'))

        try:
            with smtplib.SMTP('smtp.gmail.com', 587) as servidor:
                servidor.starttls()
                servidor.login(remitente, contraseña)
                servidor.send_message(mensaje)
                print("Correo enviado correctamente.")
        except Exception as e:
            print(f"Error al enviar correo: {e}")
