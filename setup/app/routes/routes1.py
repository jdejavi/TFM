from flask import Flask, Blueprint, redirect, make_response, render_template, request
from functions.functions import *
from Pyfhel import *
import numpy as np
import os
import hashlib

routes1 = Blueprint('routes1', __name__)

HE=Pyfhel()
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

@routes1.route('/register', methods=["GET","POST"])
def register():
    print("¡Pantalla de registro!")

@routes1.route('/login', methods=["GET","POST"])
def login():
    #Comprobamos si se ha seteado la cookie de sesion
    '''if(compruebaCookie()):
        return redirect('/logged/home')'''
    username = request.form.get('inputemail')
    passwdPT = request.form.get('inputpwd')
    
    #Si esta todo en blanco, lo redirige al login.html
    if(username==None or passwdPT==None):
        return render_template('login.html')
    #Si no, pasa a comprobar que el usuario está en la base de datos
    else:
        #Aqui va toda la lógica de la base de datos
        potential_user = np.array(mapear_letras(username))
        potential_pass = np.array(mapear_letras(passwdPT))
        if (not verificar_archivo(potential_user)):
            #return redirect('/register')
            return render_template('loginNoSuccess.html')
        else:
            ruta_users = f"/var/www/html/users/{convertir_vector_a_string(potential_user)}"
            potential_log = PyCtxt(pyfhel=HE, fileName=ruta_users)
            pass_input_strip_cipher = HE.encryptInt(potential_pass)
            is_correct = HE.sub(pass_input_strip_cipher, potential_log)

        if all(HE.decryptInt(is_correct) == 0):
            '''hacerle un redirect a la pagina de inicio, meterle la cookie de sesion etc
            '''
            random_string = os.urandom(16)
            hash = hashlib.sha256(random_string)  
            res = make_response(redirect('/logged/home'))
            res.set_cookie('cookie_key', hash.hexdigest(), max_age=None)
            res.set_cookie('username', convertir_vector_a_string(potential_user), max_age=None)
            return res
        else:
            '''Podria llevar una cuenta del num de intentos erroneos y a la 3 o asi envio correo.'''
            return render_template('loginNoSuccess.html')