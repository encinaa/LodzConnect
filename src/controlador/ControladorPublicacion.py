from src.modelo.dao.PublicacionDAO import PublicacionDAO
from src.vista.PopupPublicacion import PopupPublicacion

class ControladorPublicacion:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.dao = PublicacionDAO()

        self._vista.publicar_clicked.connect(self.publicar)
        self._vista.volver_clicked.connect(self.volver)

        self.vista_anterior = None

    def set_vista_anterior(self, vista_anterior):
        self.vista_anterior = vista_anterior

    def publicar(self):
        texto = self._vista.get_texto_publicacion()
        if texto:
            from datetime import datetime
            from src.modelo.vo.PublicacionVO import PublicacionVO
            publicacion = PublicacionVO(
                idPublic=None,
                fecha=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                listaEtiquetados=[],
                cuentaOrigen=self.correo_usuario
            )
            self.dao.insertar_publicacion(publicacion)

    def volver(self):
        if self.vista_anterior:
            self.vista_anterior.show()
        self._vista.close()
