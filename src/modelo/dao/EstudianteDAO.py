from src.modelo.conexion.Conexion import Conexion

class EstudianteDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_estudiante(self, estudiante):
        sql = "INSERT INTO Usuario (correo, contraseña) VALUES (?, ?)"
        self.cursor.execute(sql, (estudiante.correo, estudiante.contraseña))
        #self.cursor.commit()
        sql = "INSERT INTO Estudiantes (correo, nombre, edad) VALUES (?, ?, ?)"
        self.cursor.execute(sql, (estudiante.correo, estudiante.nombre, estudiante.edad))
        #self.cursor.commit()
    
    def obtener_datos_estudiante(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT nombre, edad FROM Estudiantes WHERE correo = ?", (correo,))
            return cursor.fetchone()  # Devuelve (nombre, edad)
        except Exception as e:
            print(f"Error al obtener datos del estudiante: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_estudiante(self, correo, nuevo_nombre, nueva_edad):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("UPDATE Estudiantes SET nombre = ?, edad = ? WHERE correo = ?", (nuevo_nombre, nueva_edad, correo))
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
        finally:
            cursor.close()
