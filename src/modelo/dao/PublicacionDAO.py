from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.PublicacionVO import PublicacionVO

class PublicacionDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_publicacion(self, publicacion):
        cursor = self.conn.getCursor()
        try:
            sql = """INSERT INTO Publicacion 
                    (fecha, listaEtiquetados, cuentaOrigen, descripcion, url_nube, ruta_local) 
                    VALUES (?, ?, ?, ?, ?, ?)"""
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

    def obtener_todas_publicaciones(self):
        cursor = self.conn.getCursor()
        try:
            cursor.execute("SELECT idPublic, fecha, listaEtiquetados, cuentaOrigen, descripcion, url_nube, ruta_local FROM Publicacion")
            filas = cursor.fetchall()
            publicaciones = []
            for fila in filas:
                publicacion = PublicacionVO(
                    idPublic=fila[0],
                    fecha=fila[1],
                    listaEtiquetados=eval(fila[2]) if fila[2] else [],  # Convertir string a lista
                    cuentaOrigen=fila[3],
                    descripcion=fila[4],
                    url_nube=fila[5],    # ← Nuevo campo
                    ruta_local=fila[6]   # ← Nuevo campo
                )
                publicaciones.append(publicacion)
            return publicaciones
        except Exception as e:
            print("Error obteniendo publicaciones:", e)
            return []
        finally:
            cursor.close()
    
    def eliminar_publicacion(self, id_publicacion):
        sql = "DELETE FROM Publicacion WHERE idPublic = ?"
        self.cursor.execute(sql, (id_publicacion,))
        #self.conn.getConexion().commit()

