#!/usr/bin/env python3

import pymysql
import hashlib
'''
   connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')'''
ip ='172.18.0.3'
usuario='root'
passwd='root'
database ='web_tfm'

def usuario_registrado(hash,email):
   connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')
   cursor=connection.cursor()
   if(cursor):
       print('DB Connected')
       busqueda = "SELECT * FROM usuarios WHERE passwd=%s AND mail=%s"
       fila=cursor.execute(busqueda,(hash,email,))
       if(fila==1):
           connection.close()
           return True
       else:
           connection.close()
           return False

def comprueba_user(cookie_key, mail):
     connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')
     cursor=connection.cursor()
     if(cursor):
       print('DB Connected')
       busqueda = "SELECT * FROM usuarios WHERE passwd=%s AND mail=%s"
       fila=cursor.execute(busqueda,(cookie_key,mail,))
       if(fila==1):
           connection.close()
           return True
       else:
           connection.close()
           return False

def insertaVariables(nombre,apellidos,email,nickname,passwd):
    connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')

    cursor=connection.cursor()

    if(cursor):
        bytes = passwd.encode()
        hashPwd = hashlib.sha256(bytes)
        insercion = "INSERT INTO usuarios (nombre,apellidos,mail,nickname,passwd) VALUES (%s, %s, %s, %s, %s);"
        cursor.execute(insercion,(nombre,apellidos,email,nickname,hashPwd.hexdigest()))
        connection.commit()
        connection.close()

        print("Inserción tabla variable exitosa")
        return True
    else:
        print("No se conecto a la DB")
        return False