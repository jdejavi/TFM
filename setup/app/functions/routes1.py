from flask import Flask, Blueprint, redirect, make_response, render_template, request
from functions.functions import *
import numpy as np
import os
import hashlib
from functions.controlador_db import *

routes1 = Blueprint('routes1', __name__)

@routes1.route('/register', methods=["GET","POST"])
def register():
      
    nombre=request.form.get('inputName')
    apellidos = request.form.get('inputSurnames')
    email = request.form.get('inputEmail')
    nickname = request.form.get('inputNick')
    passwd = request.form.get('inputPwd')

    if(nombre==None or apellidos==None or email==None or nickname==None or passwd==None):
        return render_template('register.html')
    else:
            insertaVariables(nombre,apellidos,email,nickname,passwd)

            res = make_response(redirect('/login'))
            res.set_cookie('email_user', email, max_age=None)
            return res
            

@routes1.route('/login', methods=["GET","POST"])
def login():
    email = request.form.get('inputemail')
    passwdPT = request.form.get('inputpwd')
    
    if(email==None or passwdPT==None):
        return render_template('login.html')
    else:
        bytes=passwdPT.encode()
        hash=hashlib.sha256(bytes)
        existe= usuario_registrado(hash.hexdigest(),email)
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

@routes1.route('/logged/home', methods=["GET","POST"])
def logged():
    if(compruebaCookie()):
        return render_template('indexLog.html')
    else:
        return redirect('/login')