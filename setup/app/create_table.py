#!/usr/bin/env python3

import pymysql

# Datos de conexión a la base de datos
host = '172.18.0.3'
usuario = 'root'
passwd = 'root'

# Conexión a la base de datos
conexion = pymysql.connect(host=host, user=usuario, password=passwd)

# Crear un cursor para ejecutar consultas
cursor = conexion.cursor()

# Crear una base de datos
base_datos = 'usuarios'  # Reemplaza con el nombre deseado para la base de datos
sql_crear_base_datos = f'CREATE DATABASE {base_datos}'
cursor.execute(sql_crear_base_datos)

# Seleccionar la base de datos recién creada
cursor.execute(f'USE {base_datos}')

# Crear una tabla
sql_crear_tabla = f'''
CREATE TABLE usuarios(
    id BIGINT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    apellidos VARCHAR(150) NOT NULL,
    mail VARCHAR(150) NOT NULL,
    nickname VARCHAR(150) NOT NULL,
    passwd VARCHAR(150) NOT NULL,
    )
'''
cursor.execute(sql_crear_tabla)

# Confirmar los cambios en la base de datos
conexion.commit()

# Cerrar la conexión
conexion.close()

print("Base de datos y tabla creadas exitosamente.")
