#!/bin/bash

################################################################################
# Autores: Javier Matilla Martín (aka m4t1) y Juan Camilo Muñoz Salazar
# Script para crear un contenedor de Docker con los paquetes necesarios
################################################################################

# Construir la imagen de Docker
docker build -t web_tfm .

# Crear un contenedor de Docker
docker run -d -it -p 443:443 --name container_tfm -v /var/lib/mysqlTFM:/var/lib/mysql web_tfm

#Cambiamos la primera linea del archivo de /etc/hosts para acceder con un dominio personalizado

sed -i '1s/.*/127.0.0.1 homomorphicEncrypt.he localhost/' /etc/hosts

#Entramos dentro del contenedor de docker

docker exec -it $(docker ps -a | awk 'NR==2 {print $1}') bash
