from Pyfhel import Pyfhel, PyPtxt, PyCtxt
from flask import Flask, requests, make_response
import hashlib
import numpy as np

# Crea un objeto Pyfhel
HE = Pyfhel()

# Seteamos los parámetros para el cifrado
params = {
    'scheme': "bfv",
    'n': 1024,
    't_bits': 16,
    't': 2,
    'sec': 128,
    'scale': 1,
    'scale_bits': 30,
    'qi_sizes': [],
    'qi': []
}

# Generamos las claves pública y privada y configuramos el contexto
HE.contextGen(params['scheme'], params['n'], params['t_bits'], params['t'], params['sec'], params['scale'], params['scale_bits'], params['qi_sizes'], params['qi'])
HE.keyGen()

# Aquí debes poner el usuario y contraseña correctos.
correct_user = 'usuario_correcto'
correct_password = 'contraseña_correcta'

# Ciframos el usuario y la contraseña correctos.
encrypted_correct_user = HE.encryptInt(hashlib.sha256(correct_user.encode()).hexdigest(), encode='hex')
encrypted_correct_password = HE.encryptInt(hashlib.sha256(correct_password.encode()).hexdigest(), encode='hex')

# @app.route('/login', methods=['POST'])
def login():
    # Obtenemos el usuario y la contraseña enviados en la petición.
    user = requests.form.get('user')
    password = requests.form.get('password')

    # Ciframos el usuario y la contraseña recibidos.
    encrypted_user = HE.encryptInt(hashlib.sha256(user.encode()).hexdigest(), encode='hex')
    encrypted_password = HE.encryptInt(hashlib.sha256(password.encode()).hexdigest(), encode='hex')

    # Comparamos si el usuario y la contraseña son correctos utilizando operaciones homomórficas.
    encrypted_is_user_correct = HE.sub(encrypted_user, encrypted_correct_user)
    encrypted_is_password_correct = HE.sub(encrypted_password, encrypted_correct_password)

    # Si el resultado de las restas es 0, entonces el usuario y la contraseña son correctos.
    if HE.decryptInt(encrypted_is_user_correct) == 0 and HE.decryptInt(encrypted_is_password_correct) == 0:
        # Creamos la cookie de sesión.
        resp = make_response('Logged')
        resp.set_cookie('loggedUser', hashlib.sha256(user.encode()).hexdigest())

        return resp

    return 'Login failed', 401
