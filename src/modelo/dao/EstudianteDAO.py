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
