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
