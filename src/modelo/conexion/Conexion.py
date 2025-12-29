import mysql.connector
from mysql.connector import Error


class Conexion:
    def __init__(
        self,
        host="localhost",
        database="LodzConnect",
        user="root",
        password="2852",  # <-- tu contraseña de MySQL
    ):
        self._host = host
        self._database = database
        self._user = user
        self._password = password
        self.conexion = self._create_connection()

    def _create_connection(self):
        """Crea la conexión a MySQL usando mysql-connector-python."""
        try:
            conn = mysql.connector.connect(
                host=self._host,
                port=3306,
                user=self._user,
                password=self._password,
                database=self._database,
                autocommit=True,   # 🔴 IMPORTANTE: activar autocommit
            )
            if conn.is_connected():
                print("Conexión correcta a MySQL")
            return conn
        except Error as e:
            print("Error creando conexión:", e)
            return None

    def getCursor(self):
        """
        Devuelve un cursor listo para usar.
        Si la conexión se ha caído, intenta reconectar.
        """
        if self.conexion is None or not self.conexion.is_connected():
            self.conexion = self._create_connection()
            if self.conexion is None:
                raise RuntimeError("No se pudo establecer conexión con la BD.")

        # buffered=True para poder hacer fetchall() sin problemas
        return self.conexion.cursor(buffered=True)

    def commit(self):
        """Por si algún sitio quiere hacer commit manualmente."""
        if self.conexion is not None and self.conexion.is_connected():
            self.conexion.commit()

    def close(self):
        """Cierra la conexión."""
        if self.conexion is not None and self.conexion.is_connected():
            self.conexion.close()
