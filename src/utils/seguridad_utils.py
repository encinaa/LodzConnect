#para hashear la contraseña y eso
import bcrypt

def hashear_contraseña(contraseña_plana):
    contraseña_bytes = contraseña_plana.encode('utf-8')
    sal = bcrypt.gensalt()
    hash = bcrypt.hashpw(contraseña_bytes, sal)
    return hash.decode('utf-8')

def verificar_contraseña(contraseña_ingresada, hash_almacenado):
    return bcrypt.checkpw(contraseña_ingresada.encode('utf-8'), hash_almacenado.encode('utf-8'))
