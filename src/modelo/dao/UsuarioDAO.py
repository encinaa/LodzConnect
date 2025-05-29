from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO

class UsuarioDAO:
    def __init__(self):
        self.conn = Conexion()  # Conexión a la base de datos

    def existe_usuario(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT 1 FROM Usuario WHERE correo = ?", (correo,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error comprobando existencia de usuario:", e)
            return False
        finally:
            cursor.close()

    def insertar_usuario(self, correo, contraseña):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("INSERT INTO Usuario (correo, contraseña) VALUES (?, ?)", (correo, contraseña))
            self.conn.conexion.commit()
        except Exception as e:
            print("Error insertando usuario:", e)
        finally:
            cursor.close()

    def insertar_admin(self, correo, permisos="Y"):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("INSERT INTO Administrador (correo, permisos) VALUES (?, ?)", (correo, permisos))
            self.conn.conexion.commit()
        except Exception as e:
            print("Error insertando admin:", e)
        finally:
            cursor.close()

    def obtener_contraseña(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT contraseña FROM Usuario WHERE correo = ?", (correo,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except Exception as e:
            print("Error obteniendo contraseña:", e)
            return None
        finally:
            cursor.close()

    def obtener_por_correo(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT correo, contraseña FROM Usuario WHERE correo = ?", (correo,))
            fila = cursor.fetchone()
            if fila:
                return UsuarioVO(correo=fila[0], contraseña=fila[1])
            return None
        except Exception as e:
            print(f"Error al obtener usuario por correo: {e}")
            return None
        finally:
            cursor.close()

