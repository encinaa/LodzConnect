from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UsuarioVO import UsuarioVO
from src.utils.singleton import singleton


@singleton
class UsuarioDAO:
    def __init__(self):
        self.conn = Conexion()  # Conexión a la base de datos

    def existe_usuario(self, correo):
        cursor = self.conn.getCursor()
        try:
            sql = "SELECT 1 FROM Usuario WHERE correo = %s"
            cursor.execute(sql, (correo,))
            return cursor.fetchone() is not None
        except Exception as e:
            print("Error comprobando existencia de usuario:", e)
            return False
        finally:
            cursor.close()

    def insertar_usuario(self, correo, contraseña):
        cursor = self.conn.getCursor()
        try:
            sql = "INSERT INTO Usuario (correo, contraseña) VALUES (%s, %s)"
            cursor.execute(sql, (correo, contraseña))
        except Exception as e:
            print("Error insertando usuario:", e)
        finally:
            cursor.close()

    def obtener_contraseña(self, correo):
        cursor = self.conn.getCursor()
        try:
            sql = "SELECT contraseña FROM Usuario WHERE correo = %s"
            cursor.execute(sql, (correo,))
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
            sql = "SELECT correo, contraseña FROM Usuario WHERE correo = %s"
            cursor.execute(sql, (correo,))
            fila = cursor.fetchone()
            if fila:
                return UsuarioVO(correo=fila[0], contraseña=fila[1])
            return None
        except Exception as e:
            print(f"Error al obtener usuario por correo: {e}")
            return None
        finally:
            cursor.close()

    def eliminar_usuario(self, correo):
        try:
            cursor = self.conn.getCursor()
            sql = "DELETE FROM Usuario WHERE correo = %s"
            cursor.execute(sql, (correo,))
            cursor.close()
        except Exception as e:
            print("Error eliminando usuario:", e)
