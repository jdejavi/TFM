#!/usr/bin/env python3

from Pyfhel import Pyfhel, PyPtxt, PyCtxt

import numpy as np
import os

#Funciones que despues iran en el functions
def convertir_vector_a_string(vector):
    vector_str = [str(elemento) for elemento in vector]
    return ','.join(vector_str)

def mapear_letras(texto):
    numeros = [ord(caracter) for caracter in texto]
    return numeros

def mapear_enteros(vector_enteros):
    letras = [chr(entero) for entero in vector_enteros if 0 <= entero <= 127]
    return ''.join(letras)

def verificar_archivo(archivo):
    ruta = f"/home/javier/scripts_homomorfica/users/{archivo}"
    if os.path.isfile(archivo):
        return True
    else:
        return False

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

user = input("Introduce el nombre del usuario a registrar --> ")
passwd = input("Introduce la pass del usuario --> ")

#Quitamos el salto de linea del final
user_strip = user.strip()
passwd_strip = passwd.strip()

#Generamos el vector de enteros para el usuario y la contraseña
vector_user = np.array(mapear_letras(user_strip))
vector_pass = np.array(mapear_letras(passwd_strip))

print(f"El valor del vector_user es --> {vector_user}")
print(f"El valor del vector_pass es --> {vector_pass}")
print(convertir_vector_a_string(vector_user))

ruta_users = f"/home/javier/scripts_pruebas/users/{convertir_vector_a_string(vector_user)}"

if (verificar_archivo(ruta_users)):
    print("Lo siento, este nombre de usuario ya ha sido elegido, pruebe otro...")
else:
    print("Nombre de usuario válido, procediendo con el registro...")
    cipher_pass = HE.encryptInt(vector_pass)
    print(cipher_pass)
    cipher_pass.save(ruta_users)

#Ahora vamos a intentar cargar el contenido del archivo que hemos guardado y a intentar hacer el login propio, aver si lo recupera bien
potential_user = PyCtxt(pyfhel=HE, fileName=ruta_users)

if (verificar_archivo(ruta_users)):

#    potential_user.load(ruta_users, HE)

    print(f"Tenemos el archivo cifrado --> {potential_user}")
    pass_input = input("Introduce la contraseña para el user: ")

    pass_input_strip = pass_input.strip()
    vector_pass_input = np.array(mapear_letras(pass_input_strip))
    pass_input_strip_cipher = HE.encryptInt(vector_pass_input)
    is_correct = HE.sub(pass_input_strip_cipher, potential_user)

    if all(HE.decryptInt(is_correct) == 0):
        print("Las contraseñas coinciden suwi")
    else:
        print("Mu mal")
else:
    print("El usuario no esta registrado...")
