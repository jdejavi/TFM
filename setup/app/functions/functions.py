from flask import request
import os
from functions.controlador_db import *
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

'''def compruebaCookie():
    if(email is None): return False
    prueba = request.cookies.get('cookie_key')
    email = request.cookies.get('email_user')

    #Compruebo que la cookie seteada es de un usuario de la base de datos
    if(controlador_db.hashEmailUsuarioYConfirmado(prueba,email)): return True
    else: return False'''

def verificar_archivo(archivo):
    ruta = f"/home/javier/scripts_homomorfica/users/{archivo}"
    if os.path.isfile(archivo):
        return True
    else:
        return False
    
def convertir_vector_a_string(vector):
    vector_str = [str(elemento) for elemento in vector]
    return ','.join(vector_str)