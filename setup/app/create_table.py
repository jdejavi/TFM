#!/usr/bin/env python3

import pymysql
from phe.paillier import EncryptedNumber, PaillierPrivateKey, PaillierPublicKey
from phe import paillier
import os
import json


KEY_FILE = '/var/www/html/functions/key.json'

def generate_or_load_keypair():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            print('Existe el par de claves')
            keys = json.load(f)
            public_key = PaillierPublicKey(n=int(keys['public_key']))
            private_key = PaillierPrivateKey(public_key=public_key,
                                             p=int(keys['private_key']['p']),
                                             q=int(keys['private_key']['q']))
    else:
        print('Generando el par de claves')
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

public_key, private_key = generate_or_load_keypair()

que_es = public_key.encrypt(0)
base_matematica = public_key.encrypt(0)
aplicaciones = public_key.encrypt(0)

serialized_que_es = str(que_es)
serialized_base_matematica = str(base_matematica)
serialized_aplicaciones = str(aplicaciones)

options = ['que_es', 'base_matematica', 'aplicaciones']

# Datos de conexión a la base de datos
host = '172.18.0.3'
usuario = 'root'
passwd = 'root'

# Conexión a la base de datos
conexion = pymysql.connect(host='172.18.0.3', user='root', password='root')

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Crear una base de datos
base_datos = 'web_tfm'  # Reemplaza con el nombre deseado para la base de datos
sql_crear_base_datos = f'CREATE DATABASE {base_datos}'
cursor.execute(sql_crear_base_datos)

# Seleccionar la base de datos recién creada
cursor.execute(f'USE {base_datos}')

# Crear una tabla
sql_crear_tabla_users = f'''
CREATE TABLE usuarios(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    mail VARCHAR(150) NOT NULL,
    nickname VARCHAR(150) NOT NULL,
    haVotado VARCHAR(20) NOT NULL,
    passwd VARCHAR(150) NOT NULL
    )
'''

sql_crear_tabla_votaciones = f'''
CREATE TABLE votos(
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    opcion TEXT,
    recuento TEXT)
'''

cursor.execute(sql_crear_tabla_users)
cursor.execute(sql_crear_tabla_votaciones)
#"INSERT INTO usuarios (nombre,apellidos,mail,nickname,passwd) VALUES (%s, %s, %s, %s, %s);"
for option in options:
    sql = "INSERT INTO votos (opcion, recuento) VALUES (%s, %s)"
    encrypted_zero = public_key.encrypt(0)
    cursor.execute(sql, (option, str(encrypted_zero.ciphertext())))

# Confirmar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión
conexion.close()

print("Base de datos y tabla creadas exitosamente.")
