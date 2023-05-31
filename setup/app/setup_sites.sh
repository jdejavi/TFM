#!/bin/bash

#Script que habilita los sitios del contenedor

#Activamos el modulo de wsgi
sudo a2enmod wsgi
sudo a2enmod ssl
sudo service apache2 reload
sudo service apache2 restart

#Sacamos los sitios default que tiene el apache
sudo a2dissite 000-default.conf 0>/dev/null
#sudo a2dissite /etc/apache2/sites-enabled/default-ssl.conf

#Hacemos reload al apache2 para que saque los sites
sudo service apache2 reload

#Activamos nuestros sitios configurados
sudo a2ensite flask.conf 0>/dev/null
sudo a2ensite default-ssl.conf 0>/dev/null

#Recargamos el servicio de apache2 con la nueva configuracion y reiniciamos el servicio
sudo service apache2 reload
sudo service apache2 restart

#Damos los permisos a www-data en el directorio /var/www/html
sudo chown -R www-data:www-data /var/www/html
sudo chmod +x /var/www/html/web.wsgi
