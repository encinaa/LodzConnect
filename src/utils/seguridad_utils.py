#para hashear la contraseña y eso
import bcrypt

def hashear_contraseña(contraseña_plana):
    contraseña_bytes = contraseña_plana.encode('utf-8')
    sal = bcrypt.gensalt()
    hash = bcrypt.hashpw(contraseña_bytes, sal)
    return hash.decode('utf-8')

import bcrypt

def verificar_contraseña(contraseña_ingresada, hash_almacenado):
    try:
        if hash_almacenado.startswith("$2b$") or hash_almacenado.startswith("$2a$"):
            return bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), hash_almacenado.encode('utf-8'))
        else:
            # Comparación directa si no está hasheado (me daba error al entrar el master)
            return contraseña_ingresada == hash_almacenado
    except Exception as e:
        print(f"Error al verificar contraseña: {e}")
        return False
