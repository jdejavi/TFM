#!/bin/bash

################################################################################################################
# Autores: Javier Matilla Martín (aka m4t1) y Juan Camilo Muñoz Salazar			 		       #
# Script de creacion de tabla y configuracion de Apache para el TFM Criptografía homomórfica, estado del arte  #
################################################################################################################

#Asigno los permisos correctos
sudo chown tfm:tfm create_table.py

#Configuro el apache y creo la tabla
sudo ./setup_sites.sh
sudo python3 create_table.py
