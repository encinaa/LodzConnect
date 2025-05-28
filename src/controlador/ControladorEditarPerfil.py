# src/controlador/ControladorEditarPerfil.py
class ControladorEditarPerfil:
    def __init__(self, vista, correo_usuario):
        self._vista = vista
        self.correo_usuario = correo_usuario
        self.vista_anterior = None

        # Conectar la señal del botón guardar
        self._vista.guardar_clicked.connect(self.guardar_perfil)

        # Simulación: cargar datos actuales (puedes sustituirlo por lógica real con DAO)
        self._vista.EditarUsuario.setText("Aroa García")
        self._vista.EditarEdad.setValue(22)
        self._vista.EditarDescripcion.setPlainText("Estudiante de Ingeniería de Software")
        self._vista.EditarActividades.setPlainText("• Participar en eventos\n• Realizar publicaciones")

    def set_vista_anterior(self, vista_anterior):
        self.vista_anterior = vista_anterior

    def guardar_perfil(self):
        # Obtener los datos desde la vista
        nombre = self._vista.EditarUsuario.text()
        edad = self._vista.EditarEdad.value()
        descripcion = self._vista.EditarDescripcion.toPlainText()
        actividades = self._vista.EditarActividades.toPlainText()

        # Simular guardar (en una app real: usar UsuarioDAO aquí)
        print("Perfil guardado:")
        print(f"Nombre: {nombre}")
        print(f"Edad: {edad}")
        print(f"Descripción: {descripcion}")
        print(f"Actividades: {actividades}")

        # Volver a la vista anterior (MiPerfil)
        if self.vista_anterior:
            self.vista_anterior.show()
        self._vista.close()
