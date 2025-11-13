class PublicacionVO:
    def __init__(self, idPublic, fecha, listaEtiquetados, cuentaOrigen, descripcion, url_nube=None, ruta_local=None):
        self.idPublic = idPublic
        self.fecha = fecha
        self.listaEtiquetados = listaEtiquetados
        self.cuentaOrigen = cuentaOrigen
        self.descripcion = descripcion
        self.url_nube = url_nube  # ← URL en la nube
        self.ruta_local = ruta_local  # ← Ruta local (backup)