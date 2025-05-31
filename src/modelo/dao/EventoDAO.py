from src.modelo.conexion.Conexion import Conexion

class EventoDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_evento(self, evento):
        sql = """
        INSERT INTO evento (idEve, nombre, descripcion, fecha, hora, ubicacion, aforoMax, correo_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (
            evento.idEve,
            evento.nombre,
            evento.descripcion,
            evento.fecha,
            evento.hora,
            evento.ubicacion,
            evento.aforoMax,
            evento.correo_admin
        ))
        #self.conn.getConexion().commit()
