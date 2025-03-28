---
title: Recopilación Activa
date: 2023-07-06
categories: [Reconocimiento]
tags: [recon, dns, subdominios, tecnologias, content-discovery]
---

## Recopilación activa de información

Recolección de información sobre un objetivo determinado utilizando métodos que interactúan de manera directa con la organización, normalmente mediante el envío de tráfico de red.

- Escaneo de hosts
- Escaneo de puertos
- Escaneo de servicios

En muchas ocasiones la actividad de este tipo de técnicas suele ser detectada como actividad sospechosa o maliciosa.

Esto es importante tenerlo en cuenta porque si nosotros estamos realizando un ejercicio de hacking ético a una organización y no podemos ser identificados o detectados por esas herramientas de detección, pues porque estamos también verificando esa capacidad de detección, entonces tendremos que tener cuidado con qué técnicas de recopilación activa estamos utilizando y centrarnos únicamente en aquellas que sean menos intrusivas.

## DNSrecoon y transferencia de zona

Anteriormente veíamos como consultar datos de forma pasiva sobre diferentes dominios.

Estas consultas se realizaban en medida al fichero de zona de estos DNS servers pero no eran el fichero como tal.

Vamos ver como poder descargar ese fichero de zona en un DNS server mal configurado.

### Transferencia de zona

Es una capacidad que nos proporcionan los DNS server para copiar ese fichero de zona a otro DNS server y no tener que volver a crearlo.

Esto a veces está mal configurado y nos permite realizar esta transferencia de zona a un DNS server no autorizado.

Vamos a utilizar un dominio de pruebas para ver ese fichero de zonas. https://dnsdumpster.com/

Buscamos "zonetransfer.me"

Vemos alguna información pero vamos a ver como con el fichero tendremos mucha más información.

Existen algunas herramientas de terminal que permiten sacar información como DNS dumpster.

```bash
sudo apt install dnsutils
```

Hay varias herramientas como por ejemplo:

```bash
nslookup
set type=ns
zonetransfer.me
```

![](/assets/img/posts/reconocimiento/20241126_003102_95-1.png)

Podemos comprobar si nos envía el fichero de transferencia de zona

```bash
set type=any
ls -d zonetransfer.me
```

![](/assets/img/posts/reconocimiento/20241126_003137_95-2.png)

Dice que el comando no está implementado por que realmente le estamos pidiendo que transfiera este archivo a una máquina host Kali Linux y esto no tendría sentido por motivos de seguridad.

Esto mismo podemos intentarlo desde una máquina windows y nos saldrá el mismo error.

Esto es por el mismo motivo que antes, estamos intentando iniciar una transferencia del fichero hacia ningún sitio porque el host o destino de la transferencia debería ser o está entendido para el DNS server que debe de ser otro DNS server y no cualquier máquina que le haga la petición.

```bash
set type=any
server nsztml.digi.ninja
ls -d zonetransfer.me
```

Una de las cosas interesantes de estos ficheros de zona es que en muchas ocasiones, cuando ese DNS server está compartido entre la red interna y redes externas, podemos también tener algún tipo de configuración de servidores y direcciones internas.

### Otra herramienta en Linux DNSrecon

```bash
dnsrecon -d zonetrasfer.me -t axfr
```

## Identificando Subdominios

### Fase de reconocimiento sobre la superficie de ataque

Hay que tener en cuenta que normalmente la superficie de ataque a una aplicación web no se reduce a un solo dominio, sino a todos los subdominios que tenga asociados ya que se encuentran alojados juntos.

Es muy común que en los subdominios haya menos medias de seguridad ya que las inversiones de mantenimiento y blindaje suelen ir dirigidas a webs principales o de acceso masivo ya que todo tiene un coste.

O incluso la posibilidad de olvidar la existencia de uno por parte de la empresa.

### SubFinder

https://github.com/projectdiscovery/subfinder

Descubre subdominios validos de una web utilizando fuentes pasivas de información.

```bash
sudo apt install subfinder
```

Vamos a probarla contra una web diseñada para eso.

```bash
subfinder -d hackthissite.org > output_subfinder.txt
```

![](/assets/img/posts/reconocimiento/20241126_003420_49-1.png)

### SubLister

https://github.com/aboul3la/Sublist3r

Utiliza python para recopilar información de subdominios utilizando OSINT, fuentes publicas de información.

También implementa subbrute que enumera subdominios haciendo peticiones a nameServers públicos. Aunque es una herramienta más activa esta implementa OpenResolvers que permite hacer bypass a los rate limits de un name servers y proporciona un poco de "anonimato"

```bash
sudo apt install sublist3r
sublist3r -d hackthissite.org -v
```

![sublister -d hackthissite.org -v -b -o subbrute.txt](/assets/img/posts/reconocimiento/20241126_003508_49-2.png)

Se le puede indicar que haga un escaneo de los subdominios y además que indique cuales tienen ciertos puertos abiertos:

```bash
sublister -d hackthissite.org -v -p 80,443
```

El problema es el ruido que genera.

## Identificando tecnologías

### Tipo de aplicaciones, tecnologías, servidores, lenguajes de programación detrás de cada subdominio

### WhatWeb

https://github.com/urbanadventurer/WhatWeb

Escaner de aplicaciones web que analiza un dominio o subdominio y analiza sus tecnologías, librerías, versiones, direcciones de correo, errores sql, id de cuentas, wp-content. Vamos a analizar una web de la maquina VPLE

Para listar los plugins

```bash
whatweb -l
```

No suele generar mucho tráfico de red y tiene opciones para controlarlo.

![whatweb -v http://192.168.20.133:8080](/assets/img/posts/reconocimiento/20241126_003901_50-1.png)

![Va dando información mediante los plugins, etc.](/assets/img/posts/reconocimiento/20241126_003908_50-2.png)

Si usamos esta aplicación, al analizar las peticiones y las cabeceras de los paquetes no debería haber problema a la hora de usarlo contra una web con balanceador de carga.

El balanceador se encargar de repartir las cargas de peticiones entre varios servidores o regiones.

![Diferentes modos](/assets/img/posts/reconocimiento/20241126_003931_50-3.png)

### WebAnalyze

https://github.com/rverton/webanalyze

Es algo más sencilla y rápida que WhatWeb, menos conocida pero da menos detalle.

```bash
go install -v github.com/rverton/webanalyze/cmd/webanalyze@latest
webanalyze -update
```

![](/assets/img/posts/reconocimiento/20241126_004003_50-4.png)

## Content Discovery

Si en las anteriores técnicas aun no hemos encontrado nada demasiado útil podemos analizar los contenidos.

Se puede realizar de forma manual como un usuario pero normalmente esto que está de cara al público suele estar más securizado.

Pero si hacemos un análisis más profundo puede haber archivos que se pueden estar sirviendo aunque no se referencien de cara al público y pueden ser más interesantes.

Una cosa a tener en cuenta es que esta técnica es que claramente es más intrusiva porque interactuamos directamente con la aplicación y por tanto generamos tráfico.

### Dirbuster

https://github.com/KajanM/DirBuster

Viene instalada por defecto en Kali. Trata de hacer fuerza bruta en un dominio que le indiquemos mediante un diccionario. Por defecto los diccionarios se encuentran en 

```bash
/usr/share/wordlists/dirbuster
```

![](/assets/img/posts/reconocimiento/20241126_004206_51-1.png)

![](/assets/img/posts/reconocimiento/20241126_004214_51-2.png)

### Gobuster y seclists

Es una herramienta similar, más reciente y escrita en go.

https://github.com/OJ/gobuster

También incorpora fuerza bruta sobre subdominios, virtual hosts o buckets en amazon.

```bash
sudo apt install gobuster
```

Añadimos también mejores diccionarios

```bash
git clone https://github.com/danielmiessler/SecLists
gobuster -h
```

![](/assets/img/posts/reconocimiento/20241126_004359_51-3.png)

```bash
gobuster dir -u http://192.168.20.133:8080 -w /home/kali/Desktop/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt
```

También podemos buscar ficheros concretos por extensión

```bash
gobuster dir -u http://192.168.20.133:8080 -w /home/kali/Desktop/SecLists/Discovery/Web-Content/directory-list-2.3-small.txt -x pdf
```