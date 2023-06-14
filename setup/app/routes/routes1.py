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
    print("Pantalla de registro")

@routes1.route('/login', methods=["GET","POST"])
def login():
    print("Pantalla de login")