from flask import request
import os
from functions.controlador_db import *
from phe.paillier import EncryptedNumber, PaillierPrivateKey, PaillierPublicKey
from phe import paillier
import json

KEY_FILE = '/var/www/html/functions/key.json'

def generate_or_load_keypair():
    
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            #print('Existe el par de claves')
            keys = json.load(f)
            public_key = PaillierPublicKey(n=int(keys['public_key']))
            private_key = PaillierPrivateKey(public_key=public_key,
                                             p=int(keys['private_key']['p']),
                                             q=int(keys['private_key']['q']))
    else:
        #print('Generando el par de claves')
        public_key, private_key = paillier.generate_paillier_keypair()
        keys = {
            'public_key': str(public_key.n),
            'private_key': {
                'p': str(private_key.p),
                'q': str(private_key.q)
            }
        }
        with open(KEY_FILE, 'w') as f:
            json.dump(keys, f)
    return public_key, private_key

def mapear_letras(texto):
    numeros = [ord(caracter) for caracter in texto]
    return numeros

def mapear_enteros(vector_enteros):
    letras = [chr(entero) for entero in vector_enteros if 0 <= entero <= 127]
    return ''.join(letras)

def compruebaCookie():
    '''if(email is None): return False'''
    prueba = request.cookies.get('cookie_key')
    email = request.cookies.get('email_user')
    
    if(comprueba_user(prueba,email)): return True
    else: return False

def verificar_archivo(archivo):
    ruta = f"/home/javier/scripts_homomorfica/users/{archivo}"
    if os.path.isfile(archivo):
        return True
    else:
        return False
    
def convertir_vector_a_string(vector):
    vector_str = [str(elemento) for elemento in vector]
    return ','.join(vector_str)
'''
def añadeVotoAOpcion(opcion):
    
    public_key, private_key = generate_or_load_keypair()
    
    voto_que_es = public_key.encrypt(1 if opcion == 'que_es' else 0)
    voto_base_matematica = public_key.encrypt(1 if opcion == 'base_matematica' else 0)
    voto_aplicaciones = public_key.encrypt(1 if opcion == 'aplicaciones' else 0)

    total_que_es = obtieneVotosOpcion('que es') + voto_que_es
    total_base_matematica = obtieneVotosOpcion('base matematica') + voto_base_matematica
    total_aplicaciones = obtieneVotosOpcion('aplicaciones') + voto_aplicaciones

    votoFinal_ques = private_key.decrypt(total_que_es)
    votoFinal_base = private_key.decrypt(total_base_matematica)
    votoFinal_app = private_key.decrypt(total_aplicaciones)

    print(f'Votos que es --> {votoFinal_ques}')
    print(f'Votos base --> {votoFinal_base}')
    print(f'Votos app--> {votoFinal_app}')

    actualizaVotosOpcion('que es', total_que_es)
    actualizaVotosOpcion('base matematica', total_base_matematica)
    actualizaVotosOpcion('aplicaciones', total_aplicaciones)

    mail = request.cookies.get('email_user')
    actualizaEstadoVotante(mail)


'''