---
title: Code - HackTheBox Season 7
date: 2025-03-27 20:30:00 +0000
layout: post
permalink: /writeups/HTB/LABS/code-htb-season7
description: >
  Guía en español para Code - HackTheBox Season 7
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Escaneo de puertos

```bash
❯ nmap -sC -sV --min-rate 5000 -O 10.10.11.62
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-27 00:15 CET
Nmap scan report for 10.10.11.62
Host is up (0.097s latency).
Not shown: 998 closed tcp ports (reset)
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 b5:b9:7c:c4:50:32:95:bc:c2:65:17:df:51:a2:7a:bd (RSA)
|   256 94:b5:25:54:9b:68:af:be:40:e1:1d:a8:6b:85:0d:01 (ECDSA)
|_  256 12:8c:dc:97:ad:86:00:b4:88:e2:29:cf:69:b5:65:96 (ED25519)
5000/tcp open  http    Gunicorn 20.0.4
|_http-title: Python Code Editor
|_http-server-header: gunicorn/20.0.4
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Web

En el servicio web tenemos lo que parece un sandbox de python para crear y probar scripts online.

Explorando el WSGI (Web Server Gateway Interface) que utiliza la web encontramos que es un servidor web de python llamado gunicorn y algunas vulnerabilias que podemos explotar.

[Gunicorn](https://security.snyk.io/package/pip/gunicorn/20.0.4)

Aprovechando esto podemos intentar exfiltrar datos.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-17.png)

Observamos que se exfiltran dos usuarios de la base de datos con sus claves en md5.

### Crackeando las contraseñas

Para crackear las contraseñas podemos usar hashcat.

```bash
hashcat -m 0 -a 0 hashes.txt /usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-21.png)

## Acceso por SSH

Probando las claves conseguimos acceder por ssh con la cuenta de martin.

Una vez dentro probamos `sudo -l` para ver que podemos ejecutar comandos como root.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-29.png)

Tenemos capacidad para ejecutar un script que se llama backy.sh.

Es un script que hace uso de un archivo task.json para realizar lo que parece un backup del directorio que contiene la app web.

Si nos dirigimos a la carpeta backups encontramos los archivos.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-28.png)

### Obteniendo la user flag

Para esto vamos a aprovechar que podemos ejecutar el backup como root.

La flag del usuario se encuentra el el directorio del developer llamada `app-production`.

Lo que vamos a hacer es crear un archivo task.json en /tmp para que ejecute el backup completo de toda la carpeta del usuario incluida la flag.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-29_1.png)

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-31.png)

Despues nos dirigimos de nuevo a la carpeta backups para encontrar el archivo .tar.bz2 que contiene la flag.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-37.png)

### Obteniendo el root flag

Probando exactamente el mismo proceso pero con el directorio de root vemos que tenemos error ya que el script tiene un filtro para evitar copiar datos de este directorio.

El script filtra `/root` por lo que no podemos usar la ruta absoluta, en alternativa usaremo una ruta relativa.

Creamos un task.json en /tmp pero indicando que la ruta a /root es `/var/../root/`.

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-43.png)

![alt text](/assets/img/writeups/hackthebox/code-htb-s7/2025-03-27_00-53.png)