from Pyfhel import Pyfhel, PyPtxt, PyCtxt
import hashlib
import numpy as np
from functions import *
'''
def mapear_letras(texto):
    numeros = [ord(caracter) for caracter in texto]
    return numeros

def mapear_enteros(vector_enteros):
    letras = [chr(entero) for entero in vector_enteros if 0 <= entero <= 127]
    return ''.join(letras)
'''

user = 'PeP1T@'
vector_user = mapear_letras(user)

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

print(vector_user)

#numero = 33
#num_b = numero.to_bytes((numero.bit_length()+7)//8, 'big')
vector_enteros = np.array(vector_user)
print(vector_enteros)

cipher = HE.encryptInt(vector_enteros)
ciph2 = cipher.to_bytes()

#print(f"Numero cifrado: {ciph2}")
print("El tamaño del texto cifrado es de --> ", cipher.sizeof_ciphertext())
decipher = HE.decryptInt(cipher)
resultado = mapear_enteros(decipher)

print(resultado)

user_input = input("Introduce el usuario: ")
user_mapped = mapear_letras(user_input.strip())
print(user_mapped)
vector_user_mapped = np.array(user_mapped)

cipher_input = HE.encryptInt(vector_user_mapped)

encrypted_is_user_correct = HE.sub(cipher, cipher_input)

#decision = HE.decryptInt(encrypted_is_user_correct)
#print(decision)

if all(HE.decryptInt(encrypted_is_user_correct) == 0):
    print("Los usuarios coinciden suwi")
else:
    print("Revisa el codigo machote")
