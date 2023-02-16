"""
Ejemplo para hashear y comprobar
contraseñas largas en Python usando bcrypt
@author parzibyte
"""
import bcrypt, hashlib, base64
# Esta puede venir de un formulario, ser leída con input o cualquier cosa
pass_texto_plano = "hunter2" * 500 # Muy larga, es hunter2 500 veces

# Debemos tenerla como bytes
pass_texto_plano = pass_texto_plano.encode()

# Y ahora la "acortamos"
pass_texto_plano = base64.b64encode(hashlib.sha256(pass_texto_plano).digest())

# La sal, necesaria para preparar nuestra contraseña
sal = bcrypt.gensalt()

# Hashear
pass_hasheada = bcrypt.hashpw(pass_texto_plano, sal)

#Nota: en casos reales no imprimas ni guardes en un log las contraseñas ni la sal
print("La contraseña en texto plano es '{}', la sal es '{}' y la hasheada es '{}'".format(pass_texto_plano, sal, pass_hasheada))

# Ahora vamos a comprobarla, recuerda que pass_hasheada puede provenir de tu base de datos o un lugar en donde la guardaste
print("Comprobando contraseñas...")
if bcrypt.checkpw(pass_texto_plano, pass_hasheada):
	print("Ok, las contraseñas coinciden")
else:
	print("Contraseña incorrecta")
