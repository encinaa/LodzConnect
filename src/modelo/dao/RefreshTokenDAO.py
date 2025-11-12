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
            
            sql = "INSERT INTO RefreshToken (token, correo, expires_at, revoked) VALUES (?, ?, ?, ?)"
            cursor.execute(sql, (token, correo, expires_at_str, False))
        except Exception as e:
            print("Error insertando refresh token:", e)
        finally:
            cursor.close()

    def existe_token(self, token):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT revoked, expires_at FROM RefreshToken WHERE token = ?", (token,))
            resultado = cursor.fetchone()
            if resultado:
                # Convertir string de MySQL a datetime si es necesario
                revoked, expires_at_str = resultado
                # Si quieres usar como datetime: expires_at = datetime.datetime.strptime(expires_at_str, '%Y-%m-%d %H:%M:%S')
                return revoked, expires_at_str
            return None
        except Exception as e:
            print("Error comprobando refresh token:", e)
            return None
        finally:
            cursor.close()

    def revocar_token(self, token):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("UPDATE RefreshToken SET revoked = ? WHERE token = ?", (True, token))
        except Exception as e:
            print("Error revocando token:", e)
        finally:
            cursor.close()