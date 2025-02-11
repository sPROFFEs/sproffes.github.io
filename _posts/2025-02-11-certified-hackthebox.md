---
title: Certified - Hackthebox - Season7
date: 2025-02-11 11:00:00 +0000
categories: [Labs & CTF, Write Up, Hackthebox]
tags: [Windows, CTF, Active Directory] 
image:
  path: /assets/img/posts/certified_htb/cabecera.png
  alt: Certified
description: >
  Certified - Hackthebox - Season7 - Guía en español
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Escaneo de puertos

```bash
❯ nmap -sC -O -n 10.10.11.41
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-11 12:19 CET
Stats: 0:01:02 elapsed; 0 hosts completed (1 up), 1 undergoing Script Scan
NSE Timing: About 95.50% done; ETC: 12:20 (0:00:01 remaining)
Nmap scan report for 10.10.11.41
Host is up (0.086s latency).
Not shown: 988 filtered tcp ports (no-response)
PORT     STATE SERVICE
53/tcp   open  domain
88/tcp   open  kerberos-sec
135/tcp  open  msrpc
139/tcp  open  netbios-ssn
389/tcp  open  ldap
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
|_ssl-date: 2025-02-11T18:20:23+00:00; +7h00m01s from scanner time.
445/tcp  open  microsoft-ds
464/tcp  open  kpasswd5
593/tcp  open  http-rpc-epmap
636/tcp  open  ldapssl
|_ssl-date: 2025-02-11T18:19:51+00:00; +7h00m00s from scanner time.
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
3268/tcp open  globalcatLDAP
3269/tcp open  globalcatLDAPssl
| ssl-cert: Subject: commonName=DC01.certified.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1:<unsupported>, DNS:DC01.certified.htb
| Not valid before: 2024-05-13T15:49:36
|_Not valid after:  2025-05-13T15:49:36
|_ssl-date: 2025-02-11T18:19:51+00:00; +7h00m00s from scanner time.
5985/tcp open  wsman
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2019|10 (97%)
OS CPE: cpe:/o:microsoft:windows_server_2019 cpe:/o:microsoft:windows_10
Aggressive OS guesses: Windows Server 2019 (97%), Microsoft Windows 10 1903 - 21H1 (91%)
No exact OS matches for host (test conditions non-ideal).

Host script results:
|_clock-skew: mean: 7h00m00s, deviation: 0s, median: 6h59m59s
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
| smb2-time: 
|   date: 2025-02-11T18:19:53
|_  start_date: N/A

OS detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 74.01 seconds
```
## Puntos clave

Indicadores de Active Directory: Los puertos 88 (Kerberos), 389 (LDAP) y 445 (SMB) sugieren la presencia de un controlador de dominio de Windows.

Certificados SSL: Los detalles del certificado revelaron el nombre de host DC01.certified.htb y información adicional del dominio, lo que confirma el rol del objetivo como autoridad certificadora.

Firma SMB: Los scripts de Nmap indicaron que la firma SMB está habilitada y es obligatoria, lo que puede limitar algunos vectores de ataque SMB.

## Comprobación de credenciales en SMB

```bash
❯ nxc smb certified.htb -u 'judith.mader' -p 'judith09'
SMB         10.10.11.41     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:certified.htb) (signing:True) (SMBv1:False)
SMB         10.10.11.41     445    DC01             [+] certified.htb\judith.mader:judith09
```
Las credenciales parecen ser válidas por lo que de primeras tenemos acceso de bajo nivel.

## Comprobación de credenciales en LDAP y mapeo para BloodHound

```bash
❯ nxc ldap dc01.certified.htb -u judith.mader -p judith09 --bloodhound --collection All --dns-tcp --dns-server 10.10.11.41
SMB         10.10.11.41     445    DC01             [*] Windows 10 / Server 2019 Build 17763 x64 (name:DC01) (domain:certified.htb) (signing:True) (SMBv1:False)
LDAP        10.10.11.41     389    DC01             [+] certified.htb\judith.mader:judith09 
LDAP        10.10.11.41     389    DC01             Resolved collection methods: rdp, container, psremote, acl, group, objectprops, session, localadmin, dcom, trusts
LDAP        10.10.11.41     389    DC01             Done in 00M 14S
LDAP        10.10.11.41     389    DC01             Compressing output into /home/kali/.nxc/logs/DC01_10.10.11.41_2025-02-11_123007_bloodhound.zip
```
Importamos el `zip` a BloodHound para obtener el posible camino de entrada al AD.

# Análisis con BloodHound

![alt text](/assets/img/posts/certified_htb/image.png)

- Permisos de Judith Mader:  
  - Judith Mader tiene permisos de WriteOwner sobre el grupo de Gestión.  

- Cuenta de Servicio (Management_SVC):  
  - La cuenta Management_SVC tiene permisos de GenericWrite sobre el grupo de Gestión.  

- Privilegios de CA_Operator:  
  - La cuenta Management_SVC tiene permisos de GenericAll sobre el usuario CA_Operator.

Sabiendo esto y teniendo nuestro punto de entrada claro vamos a explotar estas realciones para poder escalar privilegios de usuario.

# Escalando privilegios de usuario

## Estableciendo la Propiedad

> Utilizamos **bloodyAD** para establecer a **judith.mader** como la propietaria del grupo "Management".

![alt text](/assets/img/posts/certified_htb/image-1.png)

## Concediendo Permisos de Escritura

> Haciendo uso de imapacket-dacledit modificamos los permisos del grupo.

![alt text](/assets/img/posts/certified_htb/image-2.png)

## Añadiendo a Judith al grupo

> Añadimos al usuario `judith.mader` al grupo `Management`.

![alt text](/assets/img/posts/certified_htb/image-3.png)

## Explotando KeyCredentialLink

Como la cuenta de servicio management_svc es parte del grupo management podemos explotar esta vulnerabilidad que nos permite modificar o crear certificados en nombre de una cuenta de la que no tenemos sus credenciales, es decir impersonar.

> Usamos `pwhysker` para crear un certificado de `management_svc`

![alt text](/assets/img/posts/certified_htb/image-4.png)

## Obtención del Ticket Granting Ticket

Para realizar la obtención del TGT necesitaremos [este script python](https://github.com/dirkjanm/PKINITtools)

Ahora que disponemos de un certificado que nos permite impersonar al `management_svc` podemos obtener un TGT para hacer uso de los servicios en su nombre.

Para esto hay que tener en cuenta que es posible no estar sincronizados con el AD de forma suficiente para que el TGS nos genere un TGT válido.

Recomiento preparar bien los siguientes comandos para realizarlos lo más rapido posibles uno detrás de otro o mediante un pipe.

> Sincronizamos nuestro equipo con el servidor NTP del AD.

```bash 
sudo ntpdate -s 10.10.11.41
```

> Creamos el TGT en nombre de `management_svc`

![alt text](/assets/img/posts/certified_htb/image-5.png)

Si todo ha ido bien nos genera una key y un fichero .ccache con el TGT 

## Recuperando el HASH NT

Ahora que disponemos de un TGT a nombre de `management_svc` podemos utilizarlo para extraer su NT hash desde la base de datos LDAP.

Antes de ejecutar el script es necesario indicar la ruta a nuestro fichero .ccache mediante la variable $KRB5CCNAME  

![alt text](/assets/img/posts/certified_htb/image-6.png)

> Extraemos el NT hash de `management_svc` usando `gettgtpkinit.py`

![alt text](/assets/img/posts/certified_htb/image-7.png)

Recordad indicar la key del TGT

# Aceso por WinRM 

Ahora que tenemos el hash de `management_svc` podemos acceder a WinRM

![alt text](/assets/img/posts/certified_htb/image-8.png)

# Escalando privilegios - movimiento lateral

Teniendo acceso al usuario `management_svc`, como vimos en Bloodhound este usuario tiene permisos GenericAll sobre el CA_Operator por lo que podemos modificar cualquier cosa de este usuario.

## Modificamos las credenciales del CA_OPERATOR

> Utilizamos `certipy-ad` para modificar la keyCredential de `ca_operator`

![alt text](/assets/img/posts/certified_htb/image-9.png)

## Actualizamos el UserPrincipalName de ca_operator

Para explotar el hecho de poder crear certificados en nombre de otros usuario vamos a modificar como el AD identifica a ca_operator para que crea que es administrator y así poder generar un certificado en su nombre.

> Actualizamos el UPN (UserPrincipalName) de `ca_operator` a `administrator`

![alt text](/assets/img/posts/certified_htb/image-10.png)

## Generamos el certificado en nombre de administrator

> Usamos de nuevo certipy-ad para generar el certificado

![alt text](/assets/img/posts/certified_htb/image-11.png)

## Volvemos a actualizar el UPN a su estado anterior

Para evitar que impersonemos al usuario ca_operator con el UPN modificado, debemos actualizar de nuevo este a su anterior estado.

![alt text](/assets/img/posts/certified_htb/image-12.png)

## Impersonamos a administrator para obtener su NT hash

![alt text](/assets/img/posts/certified_htb/image-13.png)

# Acceso WinRM como administrator

![alt text](/assets/img/posts/certified_htb/image-14.png)