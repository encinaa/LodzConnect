from src.modelo.vo.PublicacionVO import PublicacionVO
from src.modelo.dao.PublicacionDAO import PublicacionDAO
from datetime import datetime

class ControladorPopupPublicacion:
    def __init__(self, vista, correo_usuario):
        self.vista = vista
        self.correo_usuario = correo_usuario
        self.dao = PublicacionDAO()

        self.vista.boton_publicar.clicked.connect(self.publicar)

    def publicar(self):
        texto = self.vista.texto.toPlainText().strip()

        if not texto:
            self.vista.mostrar_mensaje("error", "Error", "Text must be fullfilled.")
            return

        if len(texto) > 500:
            self.vista.mostrar_mensaje("error", "Error", "Publication can't exceed 500 carachteres.")
            return

        nueva_publicacion = PublicacionVO(
            idPublic=None, 
            fecha=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            listaEtiquetados=[], 
            cuentaOrigen=self.correo_usuario,
            descripcion=texto    
        )

        self.dao.insertar_publicacion(nueva_publicacion)
        self.vista.mostrar_mensaje("Information", "Posted", "Your post has been saved.")
        self.vista.accept()
