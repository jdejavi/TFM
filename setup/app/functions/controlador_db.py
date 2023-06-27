#!/usr/bin/env python3
import pymysql
import pymysql.cursors
import hashlib
from phe.paillier import EncryptedNumber
from phe import paillier

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
        
        consulta = "SELECT COUNT(*) FROM usuarios WHERE nickname = %s;"
        cursor.execute(consulta, (nickname,))
        resultado = cursor.fetchone()
        if resultado[0] > 0:
            print("El valor ya existe en la base de datos.")
            connection.close()
            return False

        insercion = "INSERT INTO usuarios (nombre,apellidos,mail,nickname,haVotado,passwd) VALUES (%s, %s, %s, %s, %s, %s);"
        cursor.execute(insercion,(nombre,apellidos,email,nickname,'NO',hashPwd.hexdigest()))
        connection.commit()
        connection.close()

        print("Inserción tabla variable exitosa")
        return True
    else:
        print("No se conecto a la DB")
        return False

def annade_voto(option):
    from functions.functions import generate_or_load_keypair

    public_key, private_key = generate_or_load_keypair()
    options = ['que_es', 'base_matematica', 'aplicaciones']

    connection = pymysql.connect(host='172.18.0.3',
                                 user='root',
                                 password='root',
                                 db='web_tfm',
                                 cursorclass=pymysql.cursors.DictCursor)

    cursor=connection.cursor()

    if(cursor):
        with connection.cursor() as cursor:
            # Cifrar un 1 para la opción seleccionada y un 0 para las demás
            for i in options:
                if i == option:
                    #print(f'cifrando un 1 para {i}')
                    vote = public_key.encrypt(1)
                else:
                    #print(f'cifrando un 0 para {i}')
                    vote = public_key.encrypt(0)
                #vote = public_key.encrypt(1) if i == option else public_key.encrypt(0)
                sql = "SELECT recuento FROM votos WHERE opcion = %s"
                cursor.execute(sql, (i,))
                result = cursor.fetchone()
                current_vote = EncryptedNumber(public_key, int(result['recuento']))
                new_vote = current_vote + vote
                sql = "UPDATE votos SET recuento = %s WHERE opcion = %s"
                cursor.execute(sql, (str(new_vote.ciphertext()), i))
        connection.commit()
    else:
        connection.close()

'''
def obtieneVotosOpcion(opcion):
    public_key, private_key = generate_or_load_keypair()

    connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')

    cursor=connection.cursor()

    if(cursor):
        busqueda = "SELECT recuento FROM votos WHERE opcion = %s"
        fila=cursor.execute(busqueda,(opcion,))

        if(fila==1):
           connection.close()
           return fila
        else:
            connection.close()
            return False

def actualizaVotosOpcion(opcion, nuevoValor):
    connection=pymysql.connect(host='172.18.0.3',
                           user='root',
                           password='root',
                           db='web_tfm')

    cursor=connection.cursor()

    if(cursor):
        actualizacion = "UPDATE votos SET votos=%s WHERE opcion=%s"
        cursor.execute(actualizacion, (nuevoValor, opcion))
        connection.commit()
        connection.close()

        if cursor.rowcount > 0:
            return True  # Actualización exitosa
        else:
            return False'''

def get_results():
    from functions.functions import generate_or_load_keypair

    public_key, private_key = generate_or_load_keypair()
    options = ['que_es', 'base_matematica', 'aplicaciones']
    results = []
    connection = pymysql.connect(host='172.18.0.3',
                                 user='root',
                                 password='root',
                                 db='web_tfm',
                                 cursorclass=pymysql.cursors.DictCursor)  # Utiliza DictCursor para obtener resultados como diccionarios

    cursor = connection.cursor()

    if cursor:
        with connection.cursor() as cursor:
            # Descifrar el total de votos para cada opción
            for option in options:
                sql = "SELECT recuento FROM votos WHERE opcion = %s"
                cursor.execute(sql, (option,))
                result = cursor.fetchone()
                encrypted_vote = EncryptedNumber(public_key, int(result['recuento']))
                decrypted_vote = private_key.decrypt(encrypted_vote)
                results.append(decrypted_vote)
    else:
        connection.close()
    return results


def actualizaEstadoVotante(mail):
    connection = pymysql.connect(host='172.18.0.3',
                                 user='root',
                                 password='root',
                                 db='web_tfm')

    cursor = connection.cursor()

    if cursor:
        actualizacion = "UPDATE usuarios SET haVotado=%s WHERE mail=%s"
        cursor.execute(actualizacion, ('SI', mail))
        connection.commit()
        connection.close()

        if cursor.rowcount > 0:
            return True  # Actualización exitosa
        else:
            return False  # No se encontró ninguna fila para actualizar
        
def compruebaSiHaVotado(mail):
    connection = pymysql.connect(host='172.18.0.3',
                                 user='root',
                                 password='root',
                                 db='web_tfm')

    cursor = connection.cursor()

    if cursor:
        busqueda = "SELECT haVotado from usuarios WHERE mail=%s"
        cursor.execute(busqueda, (mail,))
        connection.commit()
        haVotado = cursor.fetchall()
        #print(haVotado[0][0])
        if haVotado[0][0] == 'SI':
            connection.close()
            return True
        else:
            connection.close()
            return False