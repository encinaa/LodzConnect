from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PublicacionVO import PublicacionVO


class PublicacionDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_publicacion(self, publicacion):
        cursor = self.conn.getCursor()
        try:
            sql = """
                INSERT INTO Publicacion
                    (fecha, listaEtiquetados, cuentaOrigen, descripcion, url_nube, ruta_local)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(sql, (
                publicacion.fecha,
                str(publicacion.listaEtiquetados),  # Convertir lista a string
                publicacion.cuentaOrigen,
                publicacion.descripcion,
                publicacion.url_nube,
                publicacion.ruta_local
            ))
        except Exception as e:
            print("Error insertando publicación:", e)
        finally:
            cursor.close()

    def obtener_todas_publicaciones(self):
        cursor = self.conn.getCursor()
        try:
            # Ordenar por fecha descendente (más reciente primero)
            cursor.execute("""
                SELECT idPublic, fecha, listaEtiquetados, cuentaOrigen,
                       descripcion, url_nube, ruta_local 
                FROM Publicacion 
                ORDER BY fecha DESC
            """)
            filas = cursor.fetchall()
            publicaciones = []
            for fila in filas:
                publicacion = PublicacionVO(
                    idPublic=fila[0],
                    fecha=fila[1],
                    listaEtiquetados=eval(fila[2]) if fila[2] else [],
                    cuentaOrigen=fila[3],
                    descripcion=fila[4],
                    url_nube=fila[5],
                    ruta_local=fila[6]
                )
                publicaciones.append(publicacion)
            return publicaciones
        except Exception as e:
            print("Error obteniendo publicaciones:", e)
            return []
        finally:
            cursor.close()

    def eliminar_publicacion(self, id_publicacion):
        try:
            cursor = self.conn.getCursor()
            sql = "DELETE FROM Publicacion WHERE idPublic = %s"
            cursor.execute(sql, (id_publicacion,))
            cursor.close()
        except Exception as e:
            print("Error eliminando publicación:", e)
