#!/usr/bin/env python3

from Pyfhel import Pyfhel, PyPtxt, PyCtxt
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

texto = PyPtxt()

valor_1 = 1302
valor_2 = 2531

print(f'Vamos a cifrar un {valor_1} y un {valor_2} y vamos a sumar ambos valores...\n')

num_0 = HE.encryptInt(np.array([valor_1], dtype=np.int64))
num_1 = HE.encryptInt(np.array([valor_2], dtype=np.int64))

suma = num_0 + num_1
print(f'El valor de la variable es --> {suma}\n')

resultado_desc = HE.decryptInt(suma)

print(f'El valor de la variable descifrada es --> {resultado_desc[0]}\n')
