from src.modelo.conexion.Conexion import Conexion

class UsuarioDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def existe_usuario(self, correo):
        self.cursor.execute("SELECT 1 FROM Usuario WHERE correo = ?", (correo,))
        return self.cursor.fetchone() is not None

    def insertar_usuario(self, correo, contraseña):
        self.cursor.execute("INSERT INTO Usuario (correo, contraseña) VALUES (%s, %s)", (correo, contraseña))
        self.conn.commit()

    """
    def insertar_estudiante(self, correo, nombre):
        self.cursor.execute("INSERT INTO Estudiantes (correo, nombre) VALUES (%s, %s)", (correo, nombre))
        self.conn.commit()
    """
    def insertar_admin(self, correo, permisos="Y"):
        self.cursor.execute("INSERT INTO Administrador (correo, permisos) VALUES (%s, %s)", (correo, permisos))
        self.conn.commit()

    def obtener_contraseña(self, correo):
        self.cursor.execute("SELECT contraseña FROM Usuario WHERE correo = ?", (correo,))
        resultado = self.cursor.fetchone()
        return resultado[0] if resultado else None

