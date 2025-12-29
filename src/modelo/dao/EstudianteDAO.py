from src.modelo.conexion.Conexion import Conexion


class EstudianteDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_estudiante(self, estudiante):
        # Insertar en Usuario
        sql = "INSERT INTO Usuario (correo, contraseña) VALUES (%s, %s)"
        self.cursor.execute(sql, (estudiante.correo, estudiante.contraseña))

        # Insertar en Estudiantes
        sql = "INSERT INTO Estudiantes (correo, nombre, edad) VALUES (%s, %s, %s)"
        self.cursor.execute(sql, (estudiante.correo, estudiante.nombre, estudiante.edad))

    def obtener_datos_estudiante(self, correo):
        cursor = self.conn.getCursor()
        try:
            cursor.execute(
                "SELECT nombre, edad FROM Estudiantes WHERE correo = %s",
                (correo,)
            )
            return cursor.fetchone()  # Devuelve (nombre, edad)
        except Exception as e:
            print(f"Error al obtener datos del estudiante: {e}")
            return None
        finally:
            cursor.close()

    def actualizar_estudiante(self, correo, nuevo_nombre, nueva_edad):
        cursor = self.conn.getCursor()
        try:
            cursor.execute(
                "UPDATE Estudiantes SET nombre = %s, edad = %s WHERE correo = %s",
                (nuevo_nombre, nueva_edad, correo)
            )
        except Exception as e:
            print(f"Error al actualizar estudiante: {e}")
        finally:
            cursor.close()

    def eliminar_estudiante(self, correo):
        try:
            cursor = self.conn.getCursor()
            cursor.execute(
                "DELETE FROM Estudiantes WHERE correo = %s",
                (correo,)
            )
            cambios = cursor.rowcount
            cursor.close()
            return cambios > 0
        except Exception as e:
            print("Error eliminando estudiante:", e)
            return False

    def obtener_todos(self):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT correo FROM Estudiantes")
            filas = cursor.fetchall()

            # Devuelve una lista de objetos simples con atributo correo
            class EstudianteSimple:
                def __init__(self, correo):
                    self.correo = correo

            return [EstudianteSimple(fila[0]) for fila in filas]
        except Exception as e:
            print(f"Error al obtener estudiantes: {e}")
            return []
        finally:
            cursor.close()
