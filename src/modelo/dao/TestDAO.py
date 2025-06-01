from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.TestVO import TestVO
import json

class TestDAO:
    def __init__(self):
        self.conn = Conexion()
        self.cursor = self.conn.getCursor()

    def insertar_test(self, test):
        sql = """
        INSERT INTO Test (correo_admin, pregunta1, pregunta2, respuestas1, respuestas2)
        VALUES (?, ?, ?, ?, ?)
        """
        self.cursor.execute(sql, (
            test.correo_admin,
            test.pregunta1,
            test.pregunta2,
            test.respuestas1,
            test.respuestas2
        ))

    def obtener_ultimo_test(self):
        sql = """
        SELECT idTest, correo_admin, pregunta1, pregunta2, respuestas1, respuestas2
        FROM Test
        ORDER BY idTest DESC
        LIMIT 1
        """
        self.cursor.execute(sql)
        fila = self.cursor.fetchone()
        if fila:
            return TestVO(*fila)
        return None

    def guardar_respuestas(self, idTest, respuestas1, respuestas2):
        sql = """
        UPDATE Test
        SET respuestas1 = ?, respuestas2 = ?
        WHERE idTest = ?
        """
        self.cursor.execute(sql, (",".join(respuestas1), ",".join(respuestas2), idTest))
