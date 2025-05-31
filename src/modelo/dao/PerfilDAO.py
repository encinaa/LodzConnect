from src.modelo.conexion.Conexion import Conexion

class PerfilDAO:
    def __init__(self):
        self.conn = Conexion()
    
    def obtener_datos_perfil(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT descripcion, listaActividades, correo FROM perfil WHERE correo = ?", (correo,))
            return cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener datos del perfil: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_perfil(self, correo, nueva_descripcion, nuevas_actividades):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("UPDATE perfil SET descripcion = ?, listaActividades = ? WHERE correo = ?", (nueva_descripcion, nuevas_actividades, correo))
        except Exception as e:
            print(f"Error al actualizar perfil: {e}")
        finally:
            cursor.close()