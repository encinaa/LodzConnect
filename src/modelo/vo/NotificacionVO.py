class NotificacionVO():
    def __init__(self, idNot, titulo, mensaje, tipo, destinatarios, fecha, correo_admin):
        self.idNot = idNot
        self.titulo = titulo
        self.mensaje = mensaje
        self.tipo = tipo
        self.destinatarios = destinatarios
        self.fecha = fecha
        self.correo_admin = correo_admin