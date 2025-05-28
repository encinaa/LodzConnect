from src.modelo.dao.UserDao import UserDao

class BussinessObject():
    def pruebaconsulta(self):
        userdao = UserDao()
        usuarios = userdao.select() #pide los datos al dao, ya tengo toda la info de los usuarios q esta en la bbd





