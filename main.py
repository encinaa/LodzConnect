"""como no me iba PyQt5, puse PyQt6. si no va. Cambios:
- sustituir PyQt6 por PyQt5
- añadir _ al exec del main: app.exec_
"""
#holi
from PyQt5.QtWidgets import QApplication, QMainWindow 
from PyQt5 import uic
from src.vista.Login import Login
from src.modelo.vo.LoginBBDD import LoginBD
from src.vista.PáginaPrincipal import PáginaPrincipal
from src.controlador.ControladorPaginaPrincipal import ControladorPaginaPrincipal


if __name__ == "__main__":
    app = QApplication([])

    vista_principal = PáginaPrincipal()                      # Crear la vista
    controlador = ControladorPaginaPrincipal(vista_principal)  # Pasarla al controlador
    vista_principal.show()                                    # Mostrar la vista

    app.exec_()