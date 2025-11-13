from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PublicacionVO import PublicacionVO

class PublicacionDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_publicacion(self, publicacion):
        sql = "INSERT INTO Publicacion (fecha, listaEtiquetados, cuentaOrigen, descripcion) VALUES (?, ?, ?, ?)"
        try:
            self.cursor.execute(sql, (
                publicacion.fecha,
                ",".join(publicacion.listaEtiquetados),
                publicacion.cuentaOrigen,
                publicacion.descripcion  
            ))
            # commit controlado ya implementado en tu versión (o comportamiento de autocommit)
            # asumiendo que la conexión maneja autocommit o commit ya realizado
        except Exception as e:
            print("ERROR en insertar_publicacion:", e)
            raise

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

    def obtener_publicaciones_por_usuario(self, correo):
        """Devuelve publicaciones cuyo cuentaOrigen == correo (más recientes primero)."""
        sql = "SELECT idPublic, fecha, listaEtiquetados, cuentaOrigen, descripcion FROM Publicacion WHERE cuentaOrigen = ? ORDER BY fecha DESC"
        try:
            self.cursor.execute(sql, (correo,))
            filas = self.cursor.fetchall()
        except Exception as e:
            print("ERROR en obtener_publicaciones_por_usuario:", e)
            raise

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
    
    def eliminar_publicacion(self, id_publicacion):
        sql = "DELETE FROM Publicacion WHERE idPublic = ?"
        try:
            self.cursor.execute(sql, (id_publicacion,))
            # commit controlado
        except Exception as e:
            print("ERROR en eliminar_publicacion:", e)
            raise