import mysql.connector


class LoginBD:

    def __init__(self, bbdd):
        ##self.conn =  Conexion bbdd
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Zepolitte00.:)',  # Sustituye '--' por tu contraseña real
            database= 'UniConecta'
        )
        self.cursor = self.conn.cursor()

    def get_cursor(self):
        return self.cursor

    def validar_email(self, email):
        self.cursor.execute("SELECT correo FROM Usuario WHERE correo = ?", (email,))
        result = self.cursor.fetchone()
        return result is not None

    def encontrar_contraseña(self, email, contraseña):
        self.cursor.execute("SELECT contraseña FROM Usuario WHERE correo = ? AND contraseña = ?", (email, contraseña))
        result = self.cursor.fetchone()
        return result is not None
    
    def registrar_usuario(self, correo, contraseña):
        # Validar si ya existe el correo
        if self.validar_email(correo):
            print("El usuario ya existe")
            return

        # Validar correo de la uni

        ##verificamos los estudiantes
        if "@estudiantes.unileon.es" in correo:
            if len(contraseña) > 8 and re.search(r"\d", contraseña):
                cursor.execute("INSERT INTO Usuario (correo, contraseña) VALUES (?, ?)", (correo, contraseña))
                nombre = correo.split('@')[0]  #Extraemos el nombre del correo 
                cursor.execute("INSERT INTO Estudiantes (correo, nombre) VALUES (?, ?)", (correo, nombre))
                conn.commit()
                print("Estudiante registrado correctamente")
            else:
                print("Contraseña no válida")
        ##admins
        elif "@unileon.es" in correo:
            if len(contraseña) > 8 and re.search(r"\d", contraseña):
                cursor.execute("INSERT INTO Usuario (correo, contraseña) VALUES (?, ?)", (correo, contraseña))
                permisos = "Y"
                cursor.execute("INSERT INTO Administrador (correo, permisos) VALUES (?, ?)", (correo, permisos))
                conn.commit()
                print("Administrador registrado correctamente")
            else:
                print("Contraseña no válida")

        else:
            print("Correo no válido")


