from PyQt5 import uic
from src.vista.VistaNavegable import VistaNavegable

Form, _ = uic.loadUiType("./src/vista/Ui/TablónAdmin.ui")

class TablonAdmin(VistaNavegable, Form):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.conectar_botones_navegacion()



    aceptar_clicked = pyqtSignal()
    volver_clicked = pyqtSignal()
    recuperar_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setupUi(self) 

        self.Boton.clicked.connect(self.aceptar_clicked)
        self.BotonVolver.clicked.connect(self.volver_clicked)
        self.BotonRecuperar.clicked.connect(self.recuperar_clicked)
