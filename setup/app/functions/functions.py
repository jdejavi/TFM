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

def compruebaCookie():
    '''if(email is None): return False'''
    prueba = request.cookies.get('cookie_key')
    email = request.cookies.get('email_user')
    
    if(usuario_registrado(prueba,email)): return True
    else: return False

def verificar_archivo(archivo):
    ruta = f"/home/javier/scripts_homomorfica/users/{archivo}"
    if os.path.isfile(archivo):
        return True
    else:
        return False