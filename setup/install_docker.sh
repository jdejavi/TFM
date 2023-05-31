#!/bin/bash

##########################################################################################
# Autores: Javier Matilla Martín (aka m4t1) y Juan Camilo Muñoz Salazar			 #
# Script de instalación de Docker para el TFM Criptografía homomórfica, estado del arte  #
##########################################################################################



# Actualizar la lista de paquetes e instalar dependencias
sudo apt-get update
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common -y

# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

# Agregar el repositorio de Docker a las fuentes de APT
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

# Actualizar la lista de paquetes nuevamente
sudo apt-get update

# Instalar Docker
sudo apt-get install docker-ce -y

# Comprobar que Docker esté en ejecución
sudo systemctl status docker

# Agregar el usuario actual al grupo "docker"
sudo usermod -aG docker $USER

