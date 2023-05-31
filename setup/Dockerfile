FROM ubuntu:latest

# Actualizar la lista de paquetes e instalar las dependencias necesarias
RUN apt update && \
    apt install -y python3 python3-pip mariadb-server libmariadbclient-dev-compat && \
    apt install -y apache2 && \
    apt install -y build-essential && \
    apt install -y cmake && \
    apt install -y git && \
    apt install -y nano && \
    pip3 install flask Pyfhel && \
    apt clean && \
    apt install -y sudo && \
    apt install -y net-tools && \
    apt install -y libapache2-mod-wsgi-py3 && \
    rm -rf /var/lib/apt/lists/*

EXPOSE 80
EXPOSE 443

# Crear un usuario llamado "tfm" y agregarlo al grupo de sudoers
RUN useradd -ms /bin/bash tfm && \
    echo "tfm ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER tfm

COPY app/web.py /var/www/html/
COPY app/web.wsgi /var/www/html/
COPY app/cert.pem /var/www/html/
COPY app/key.pem /var/www/html/
COPY app/setup_sites.sh /home/tfm/
COPY sites/flask.conf /etc/apache2/sites-available/
COPY sites/default-ssl.conf /etc/apache2/sites-available/
COPY app/static/ /var/www/html/static/
COPY app/templates/ /var/www/html/templates/
COPY certificate/certificate.crt /etc/apache2/certificate/
COPY certificate/private.key /etc/apache2/certificate/

# Establecer el directorio de trabajo como el directorio principal del usuario
WORKDIR /home/tfm

