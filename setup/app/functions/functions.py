from flask import request

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

    #Compruebo que la cookie seteada es de un usuario de la base de datos
    if(controlador_db.hashEmailUsuarioYConfirmado(prueba,email)): return True
    else: return False