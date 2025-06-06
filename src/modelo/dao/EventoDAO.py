from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.EventoVO import EventoVO

class EventoDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_evento(self, evento):
        sql = """
        INSERT INTO evento (nombre, descripcion, fecha, hora, ubicacion, aforoMax, aforoActual, correo_admin)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (
            evento.nombre,
            evento.descripcion,
            evento.fecha,
            evento.hora,
            evento.ubicacion,
            evento.aforoMax,
            0,  # aforoActual empieza en 0
            evento.correo_admin
        ))
        

    def obtener_todos_eventos(self):
        sql = "SELECT idEve, nombre, descripcion, fecha, hora, ubicacion, aforoMax, aforoActual, correo_admin FROM evento"
        self.cursor.execute(sql)
        resultados = self.cursor.fetchall()

        eventos = []
        for fila in resultados:
            evento = EventoVO(
                idEve=fila[0],
                nombre=fila[1],
                descripcion=fila[2],
                fecha=fila[3],
                hora=fila[4],
                ubicacion=fila[5],
                aforoMax=fila[6],
                aforoActual=fila[7],
                correo_admin=fila[8]
            )
            eventos.append(evento)
        return eventos
    
    def actualizar_aforo(self, id_evento, nuevo_aforo):
        try:
            sql = "UPDATE evento SET aforoActual = ? WHERE idEve = ?"
            self.cursor.execute(sql, (nuevo_aforo, id_evento))
            
            return True
        except Exception as e:
            print(f"Error actualizando aforo: {e}")
            return False


    def eliminar_evento(self, id_evento):
        try:
            sql = "DELETE FROM evento WHERE idEve = ?"
            self.cursor.execute(sql, (id_evento,))
            return True
        except Exception as e:
            print(f"Error eliminando evento: {e}")
            return False

    def modificar_evento(self, id_evento, nombre, descripcion, fecha, hora, ubicacion, aforo_max, correo_admin):
        try:
            sql = """
                UPDATE evento
                SET nombre=?, descripcion=?, fecha=?, hora=?, ubicacion=?, aforoMax=?, correo_admin=?
                WHERE idEve=?
            """
            self.cursor.execute(sql, (nombre, descripcion, fecha, hora, ubicacion, aforo_max, correo_admin, id_evento))

            return True
        except Exception as e:
            print(f"Error al modificar evento: {e}")
            return False
