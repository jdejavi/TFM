#!/bin/bash

#Asigno los permisos correctos
sudo chown tfm:tfm create_table.py

#Configuro el apache y creo la tabla
sudo ./setup_sites.sh
sudo python3 create_table.py
