from src.modelo.conexion.Conexion import Conexion
from src.utils.singleton import singleton

@singleton
class AdminDAO:
    def __init__(self):
        self.conn = Conexion()

    def insertar_admin(self, correo, permisos="Y"):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("INSERT INTO Administrador (correo, permisos) VALUES (?, ?)", (correo, permisos))
     
        except Exception as e:
            print("Error insertando admin:", e)
        finally:
            cursor.close()

    def eliminar_admin(self, correo):
        try:
            cursor = self.conn.getCursor()
            cursor.execute("DELETE FROM Administrador WHERE correo = ?", (correo,))
            cambios = cursor.rowcount
            cursor.close()
            return cambios > 0
        except Exception as e:
            print("Error eliminando admin:", e)
            return False

