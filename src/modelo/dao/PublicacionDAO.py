from src.modelo.conexion.Conexion import Conexion

class PublicacionDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_publicacion(self, publicacion):
        sql = "INSERT INTO Publicacion (fecha, listaEtiquetados, cuentaOrigen, descripcion) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (
            publicacion.fecha,
            ",".join(publicacion.listaEtiquetados),
            publicacion.cuentaOrigen,
            publicacion.descripcion  # ✅ ahora hay 4 valores
        ))

