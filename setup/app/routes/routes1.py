from flask import Flask, Blueprint, redirect, make_response, render_template, request
from functions.functions import *

routes1 = Blueprint('routes1', __name__)


@routes1.route('/login')
def login():
    return '¡Ruta de login!'


@routes1.route('/login', methods=["GET","POST"])
def login():
    #Comprobamos si se ha seteado la cookie de sesion
    if(compruebaCookie()):
        return redirect('/logged/home')
    email = request.form.get('inputemail')
    passwdPT = request.form.get('inputpwd')
    
    #Si esta todo en blanco, lo redirige al login.html
    if(email==None or passwdPT==None):
        return render_template('login.html')
    #Si no, pasa a comprobar que el usuario está en la base de datos
    else:
        #Aqui va toda la lógica de la base de datos
        bytes=passwdPT.encode()
        hash=hashlib.sha256(bytes)
        existe=controlador_db.hashEmailUsuarioYConfirmado(hash.hexdigest(),email)
        if(existe):
            '''hacerle un redirect a la pagina de inicio, meterle la cookie de sesion etc
            '''
            print ('Existe el hash')
            
            res = make_response(redirect('/logged/home'))
            res.set_cookie('cookie_key', hash.hexdigest(), max_age=None)
            res.set_cookie('email_user', email, max_age=None)
            return res
        else:
            '''Podria llevar una cuenta del num de intentos erroneos y a la 3 o asi envio correo.'''
            print('No existe el hash')
            
            return render_template('loginNoSuccess.html')