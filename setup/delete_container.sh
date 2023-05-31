#!/bin/bash

################################################################################
# Autores: Javier Matilla Martín (aka m4t1) y Juan Camilo Muñoz Salazar
# Script para eliminar todos los contenedores en una máquina
################################################################################

# Detectar todos los contenedores y eliminarlos
docker rm -f $(docker ps -a -q)
