from src.modelo.conexion.Conexion import Conexion
from src.utils.singleton import singleton
import datetime


@singleton
class RefreshTokenDAO:
    def __init__(self):
        self.conn = Conexion()

    def insertar_refresh(self, token, correo, expires_at):
        cursor = self.conn.getCursor()
        try:
            # Convertir datetime a string en formato MySQL
            expires_at_str = expires_at.strftime('%Y-%m-%d %H:%M:%S')

            sql = """
                INSERT INTO RefreshToken (token, correo, expires_at, revoked)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql, (token, correo, expires_at_str, False))
        except Exception as e:
            print("Error insertando refresh token:", e)
        finally:
            cursor.close()

    def existe_token(self, token):
        cursor = self.conn.getCursor()
        try:
            sql = "SELECT revoked, expires_at FROM RefreshToken WHERE token = %s"
            cursor.execute(sql, (token,))
            resultado = cursor.fetchone()
            if resultado:
                revoked, expires_at = resultado
                return revoked, expires_at
            return None
        except Exception as e:
            print("Error comprobando refresh token:", e)
            return None
        finally:
            cursor.close()

    def revocar_token(self, token):
        cursor = self.conn.getCursor()
        try:
            sql = "UPDATE RefreshToken SET revoked = %s WHERE token = %s"
            cursor.execute(sql, (True, token))
        except Exception as e:
            print("Error revocando token:", e)
        finally:
            cursor.close()

    def revocar_todos_tokens_usuario(self, correo):
        """Revoca todos los tokens de un usuario (útil para logout)"""
        cursor = self.conn.getCursor()
        try:
            sql = "UPDATE RefreshToken SET revoked = %s WHERE correo = %s"
            cursor.execute(sql, (True, correo))
            print(f"✓ Every token of {correo} revocked")
        except Exception as e:
            print("Error revocando tokens por correo:", e)
        finally:
            cursor.close()
