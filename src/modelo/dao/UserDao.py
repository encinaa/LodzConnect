from src.modelo.conexion.Conexion import Conexion
from src.modelo.vo.UserVo import UserVo

from typing import List

class UserDao(Conexion): #pide los datos a la bbdd con los SELECT y los almacena en VO
    SQL_SELECT = "SELECT DNI, nombre, apellido1, apellido2, email FROM usuarios"

    def __init__(self):
        super().__init__() #cuando cree objeto de userdao se va a ejecutar conexion y la ultima liena de crear conection es la q nos abre conex con bbdd

    def select(self) -> List[UserVo]:
        cursor = self.getCursor()
        usuarios = []
        try:
            cursor.execute(SQL_SELECT)
            rows = cursor.fetchall()
            for row in rows:
                idUser, nombre, apellido1, apellido2, email = row
                usuario = UserVo(idUser, nombre, apellido1, apellido2, email)
                usuarios.append(usuario)

        except Exception as e:
            print("e")  #para controlar excepciones

        return usuarios

