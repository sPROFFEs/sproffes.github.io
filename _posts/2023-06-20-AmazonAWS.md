---
title: Amazon AWS
date: 2024-06-20 
categories: [Cloud, AWS]
tags: [aws, cloud, deployment, web-application]
---

## Despliegue de un entorno real en la nube (AWS)

### Escenario de despliegue

Aplicación web para el despliegue: [https://github.com/aws-samples/simple-phonebook-web-application](https://github.com/aws-samples/simple-phonebook-web-application)

![](/assets/img/posts/amazonaws/20241125_211851_72-1.png)

### Pasos para el despliegue

1. Creación y configuración de la VPC

2. Creación y configuración de la subred privada

3. Creación y configuración de las subredes públicas

4. Creación y configuración del Internet Gateway

5. Creación y configuración de una Route Table para la subred privada. Asociación de la nueva route table a la subred privada. No debe añadirse ninguna ruta adicional a las que se crean por defecto (ten en cuenta que la ruta por defecto que indica que el tráfico destinado a 10.0.0.0/16 será enrutado localmente es lo que permite que exista conectividad entre todas las subredes que se encuentran en la VPC).

6. Creación y configuración de un Route Table para las subredes públicas. Asociación de la nueva route table a la subred pública. Creación de una nueva ruta que redireccione el tráfico dirigido a 0.0.0.0 hacia el Internet Gateway.

7. Creación y configuración de Security Groups: Creación de dos Security Groups que controlarán las conexiones entrantes y salientes hacia la aplicación web y el servidor de base de datos.

8. Security Group para la aplicación web:
   - Crear regla de entrada para permitir tráfico HTTP desde cualquier dirección IPv4
   - Crear regla de entrada para permitir tráfico SSH desde cualquier dirección IPv4

9. Security Group para la base de datos:
   - Crear regla de entrada para permitir el tráfico MySQL desde el Security Group de la aplicación web

10. Creación y configuración de los servidores de aplicación en EC2:
    Script user data para crear las instancias:

```bash
#!/bin/bash
yum -y install httpd php mysql php-mysql

case $(ps -p 1 -o comm | tail -1) in
systemd) systemctl enable --now httpd ;;
init) chkconfig httpd on; service httpd start ;;
*) echo "Error starting httpd (OS not using init or systemd)." 2>&1
esac

if [ ! -f /var/www/html/bootcamp-app.tar.gz ]; then
cd /var/www/html
wget https://s3.amazonaws.com/immersionday-labs/bootcamp-app.tar
tar xvf bootcamp-app.tar
chown apache:root /var/www/html/rds.conf.php
fi
yum -y update
```

11. Creación y configuración del Target Group

12. Creación y configuración del Application Load Balancer

13. Creación y configuración del servidor de base de datos MySQL