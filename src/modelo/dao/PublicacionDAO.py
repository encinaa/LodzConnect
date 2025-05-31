from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PublicacionVO import PublicacionVO

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

    def obtener_todas_publicaciones(self):
        sql = "SELECT idPublic, fecha, listaEtiquetados, cuentaOrigen, descripcion FROM Publicacion ORDER BY fecha DESC"
        self.cursor.execute(sql)
        filas = self.cursor.fetchall()

        publicaciones = []
        for fila in filas:
            lista_etiquetados = fila[2].split(',') if fila[2] else []
            publicacion = PublicacionVO(
                idPublic=fila[0],
                fecha=fila[1],
                listaEtiquetados=lista_etiquetados,
                cuentaOrigen=fila[3],
                descripcion=fila[4]
            )
            publicaciones.append(publicacion)

        return publicaciones
