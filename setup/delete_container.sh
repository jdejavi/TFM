#!/bin/bash

############################################################################################
# Autores: Javier Matilla Martín (aka m4t1) y Juan Camilo Muñoz Salazar                    #
# Script de borrado de contenedores para el TFM Criptografía homomórfica, estado del arte  #
############################################################################################

# Detectar todos los contenedores y eliminarlos
docker rm -f $(docker ps -a -q)
