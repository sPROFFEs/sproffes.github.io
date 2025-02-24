---
title: Hacking de redes WiFi
date: 2025-02-17 11:00:00 +0000
categories: [Labs & CTF, Guía]
tags: [WiFi, WEP, WPA2, Hacking, Labs]
description: >
  Guía rápida para realizar ataques de hacking de redes WiFi
pin: false  
toc: true   
math: false 
mermaid: false 
---

> Aviso: El contenido de esta sección ha sido creado únicamente con propósitos de educación, no me hago responsable de la mala utilización de esta información.
{: .prompt-warning }


# Introducción

Para este laboratorio vamos a utilizar el sistema operativo ofrecido por la web [WiFiChallenge](https://lab.wifichallenge.com/).

Las herramientas y el procedimiento para realizar estos ataques van a ser principalmente la suite [Aircrack-ng](https://www.aircrack-ng.org/) ya que, aun existiendo otras o automatizaciones de la misma, vamos a realizar el proceso paso a paso.


## Requisitos

Suite de herramientas de [Aircrack-ng](https://www.aircrack-ng.org/)

- aircrack-ng
- airdecap-ng
- aireplay-ng
- airodump-ng
- airolib-ng
- airserv-ng
- airtun-ng
- airtun-ng-tk
- airtun-ng-tk-gtk

Sistema operativo de [WiFiChallenge](https://lab.wifichallenge.com/)

## Instalación

### Instalación de Aircrack-ng

Para instalar Aircrack-ng, vamos a utilizar el siguiente comando:

```bash
sudo apt-get install aircrack-ng
```

# Laboratorio

## Seleccionando la interfaz de red

Dentro de nuestro laboratorio vamos a establecer lo primero nuestra tarjeta de red en modo monitor. 
En este sistema vamos a encontrar diferentes interfaces. Estas interfaces simulan diferentes tipos de redes WiFi que no son reales y podemos expotar sin ninguna preocupación.

![alt text](/assets/img/posts/hackingwifi/image.png)

Para empezar vamos a quedarnos con alguna de ellas que contenga una red con WEP y una con WPA2.

### Modo monitor

Para poder ver que dispositivos y que tipo de seguridad tienen, necesitamos establecer la tarjeta de red en modo monitor.

Para ello, vamos a utilizar el siguiente comando:

```bash
airmon-ng start wlan0
```

![alt text](/assets/img/posts/hackingwifi/image-1.png)

Una vez que la tarjeta de red esté en modo monitor, podemos ver que dispositivos están disponibles y que tipo de seguridad tienen.

Es importante que tengamos en cuenta que ahora la interfaz se ha renombrado a `wlan0mon`.

### Descubrimiento de redes

Ahora que tenemos nuestra interfaz en modo monitor, podemos comenzar a descubrir las redes que están disponibles.

Vamos a utilizar el siguiente comando:

```bash
airodump-ng wlan0mon
```

![alt text](/assets/img/posts/hackingwifi/image-2.png)

Vemos diferentes redes WiFi que podemos explorar. Vamos a comenzar por la que tiene seguridad WEP.

## Ataque WEP

Este protocolo de seguridad es muy sencillo de atacar. 

El proceso de ataque consiste en capturar paquetes de red correspondientes a la misma.

Las redes con seguridad WEP mandan la clave de seguridad en el encabezado de cada paquete en forma de vector de inicializacion (IV).

Este vector se compone de 24 bits y el seed, que es la contraseña de la red. 

Debido a la corta longitud del vector de inicializacion, es posible que, capturando muchos paquetes con sus IV correspondientes se pueda obtener la clave de forma estadísitica.

Otro tipo de ataque debido a la simplicidad de la autorización de WEP es la inyección de paquetes falsos, ya que se pueden capturar paquetes legitimos y reemplazar el contenido del mensaje manteniendo las cabeceras de seguridad.

Para comprobar que tipo de ataque vamos a realizar en función de la cantidad de paquetes que se estén mandando en la red, en el mismo comando ejecutado anteriormente nos podemos fijar en la columna que indica `#Data` el número de paquetes que se están mandando.

![alt text](/assets/img/posts/hackingwifi/image-3.png)

EL tráfico es suficiente por lo que procedemos a sniffear el tráfico de la red.

Para ello, vamos a utilizar el siguiente comando:

```bash
airodump-ng --channel 3 --bssid F0:9F:C2:71:22:11 --write WEP-WifiOld wlan0mon
```

![alt text](/assets/img/posts/hackingwifi/image-4.png)

Mientras capturamos todo ese tráfico podemos ir crackeando la contraseña de la red.

Para ello, vamos a utilizar el siguiente comando:

```bash
aircrack-ng WEP-WifiOld-01.cap
```

Una vez que hemos obtenido la contraseña, podemos conectarnos a la red.

![alt text](/assets/img/posts/hackingwifi/image-5.png)

## Ataque WPA2

Para este caso nos vamos a centrar en el siguiente tipo de redes.

![alt text](/assets/img/posts/hackingwifi/image-6.png)

Como vemos aquí solo tenemos WPA2 de tipo PSK es decir, personal shared key y no enterprise como los dos WP3 que vemos justo debajo.

Para este ataque necesitamos desauntenticar a algún usuario de la red para poder obtener el handshake, por lo que necesitamos una red que tenga usuarios conectados.

Primero vamos a snifar el tráfico de la red objetivo.

```bash
airodump-ng -c 6 --bssid F0:9F:C2:71:22:12 -w wpa2 wlan0mon
```
![alt text](/assets/img/posts/hackingwifi/image-7.png)

Observamos dos equipos en la red, vamos a seleccionar a uno de ellos para lanzar el ataque de desauntenticación.

```bash
sudo aireplay-ng -0 1000 -a F0:9F:C2:71:22:12 -c 28:6C:07:6F:F9:44 wlan0mon
```
Indicamos con -0 que se trata de un detauthentication, con -a indicamos la BSSID de la red y con -c indicamos el MAC del cliente a desautentificar.

El numero 1000 indica el número de paquetes a enviar antes de que se detiene el ataque, aunque posiblemente lo paremos antes de acabar.

![alt text](/assets/img/posts/hackingwifi/image-8.png)

Vamos a dejar el comando en ejecución mientras observamos en la otra terminal con airodump a que capture el handshake. Cuando lo capture podremos saberlo cuando nos indica en la parte superior derecha lo siguiente:

![alt text](/assets/img/posts/hackingwifi/image-10.png)

Ahora que tenemos la captura con el handshake, podemos utilizar el siguiente comando para crackear la contraseña:

```bash
aircrack-ng wpa2-01.cap
```

![alt text](/assets/img/posts/hackingwifi/image-9.png)

Aunque aquí hemos usado aircrack-ng, podemos utilizar otras herramientas como john, hashcat, etc.

## Ataque WPS 

Para este ataque vamos a centrarnos en el protocolo WPS (WiFi Protected Setup). 

Este protocolo es muy sencillo de atacar ya que solo requiere de un ataque de diccionario, ya que no se necesita de una contraseña para poder conectarnos a la red sino una clave numérica predefinida.

Aunque este protocolo utiliza diferentes métodos para compartir esta clave como NFC, USB, etc la solución más extendendida es la de utilizar el método de PIN.

Actualmente este tipo de autenticación es complicada que venga establecida por defecto activa pero aun se pueden encontrar redes que no lo hacen y además que tienen versiones desactualizadas de firmware de su router.

Para el siguiente ataque vamos a utilizar un punto de acceso simulado en un punto de acceso con WPS 1.0 y una segunda tarjeta de red.

![alt text](/assets/img/posts/hackingwifi/image-11.png)

Respecto al software utilizado será wash para analizar las redes y reaver o bully para hacer el ataque.

Como consejo personal creo que lo más optimo es usar wash para detectar las redes y sus versiones de WPS y utilizar una herramienta muy potente que junta todas estas herramientas asy añade otras funciones para realizar ataques de fuerza bruta, null pin, pixieDust, etc.

Por lo tanto en este caso vamos a utilizar wash y wifite, este último simplemente para tener todos estos ataques disponibles unificados.

```bash
airmon-ng start wlan1

wash -i wlan1mon
```
Al escanear veremos las diferentes redes al alcance con WPS activado. Ahora solo nos interesa la primera.

Ahora con wifite podemos ejecutar estos ataques. Como vemos wifite si muestra todas las redes independientemente de si tienen o no WPS activado y no indica ninguna versión de WPS de forma explícita.

> Consejo: ES 100% necesario que intalemos las herramientas que nos indica wifite para que los ataques funcionen correctamente.
{: .prompt-tip }

![alt text](/assets/img/posts/hackingwifi/image-12.png)

> Nota: Para el ataque por WPS es recomendado que la intensidad de la red supere los 50/60dB. Cuanto más intesidad mas fácil será conseguir un ataque exitoso antes de que se bloquee temporalmente el punto de acceso por WPS.
{: .prompt-info }

Una vez tengamos el objetivo claro, podemos lanzar el ataque. Pulsamos CTRL + C para detener el proceso de escaneo e introducimos el numero de la red que queremos atacar.

![alt text](/assets/img/posts/hackingwifi/image-13.png)

Como vemos al tener una versión de WPS desactualizada el ataque es muy sencillo mediante pixieDust.

## Ataque Evil Twin

Este ataque posiblemente sea el más eficaz a dia de hoy ya que los nuevos protocolos de seguridad cada vez son más complejos y difíciles de atacar. 

A diferencia de atacar los protocolos de seguridad, este ataque se centra en ingienería social. Vamos a crear una red wifi clon del objetivo mientras desauntenticamos a los usuarios de la red objetivo para "obligar" a que se conecten a nuestra red evil twin.

Una vez se conecten a la red evil twin, mediante un portal web que les pide a los ususarios que ingresen la contraseña de red wifi y de esta forma conseguimos la clave de acceso.

Este ataque se puede realizar de muchas formas, manualmente o automatizado con diferentes herramientas pero existe una que es posiblemente una de las herramientas más completas para realizar auditorias de redes wifi, Airgeddon.

![alt text](/assets/img/posts/hackingwifi/image-14.png)

Una vez instalado vamos a seleccionar la interfaz de red que vamos a utilizar.

![alt text](/assets/img/posts/hackingwifi/image-15.png)

![alt text](/assets/img/posts/hackingwifi/image-16.png)

Seleccionamos el Evil Twin.

![alt text](/assets/img/posts/hackingwifi/image-17.png)

Vamos a ver diferentes opciones ya que este ataque no solo es utilizado para robar contraseñas de redes wifi, sino también para robar información de usuarios, contraseñas, etc mediante el uso de herramientas como bettercap.

En este caso nos vamos a centrar en la opción de AP con captive portal, por lo que seleccionamos 9.

Si nos fijamos estas herramientas centralizadas hacen uso de las clásicas herramientas de red como la suite Aircrack-ng, Airodump-ng, etc.

![alt text](/assets/img/posts/hackingwifi/image-18.png)

Nos centramos en nuestro punto de pruebas. Pulsamos CTRL + C para detener el proceso de escaneo e introducimos el numero de la red que queremos atacar.

![alt text](/assets/img/posts/hackingwifi/image-19.png)

Ahora nos ofrece diferentes tipos de ataques de desauntenticación, por lo que vamos a seleccionar en este caso el DDoS.

![alt text](/assets/img/posts/hackingwifi/image-20.png)

Bien, ahora el framework nos itá preguntando por la configuración del ataque. 

![alt text](/assets/img/posts/hackingwifi/image-21.png)

Nos pregunta si queremos perseguir a la red durante el DDoS ya que por norma general los router si notan que el canal en el que se encuentran está muy ocupado, irán saltando entre canales por lo que indicaremos que si.

![alt text](/assets/img/posts/hackingwifi/image-22.png)

Para este tipo de ataques necesitamos dos interfaces de red, una que tendrá el AP falso y otra que realizará el ataque de desauntenticación.

Tras unas cuantas configuraciones más que dependerán de nuestra situación.

![alt text](/assets/img/posts/hackingwifi/image-24.png)

Bien el proceso aqui es conseguir primero el PSK handshake de la red WiFi de igual forma que hicimos en el ataque WPA2 pero esto lo necesitamos para que, cuando creemos el portal web donde le pedimos la contraseña al usuario esta se compruebe con el hash y le digamos al usuario si la contraseña es o no correcta por lo que nos aseguramos de que el usuario va a introducir la contraseña correcta.

Si ya tenemos el hacndshake capturado como en este caso lo seleccionamos pero si no lo tenemos simplemente indicamos que no y hará el ataque de desautenticación de forma automática para capturarlo.

Ahora seleccionamos el idioma objetivo del portal, español en este caso. 

![alt text](/assets/img/posts/hackingwifi/image-25.png)

Ahora nos pregunta si queremos crear un portal avanzado, esto lo que hará es coger la información del fabricante del router para poder personalizar un poco el portal para hacerlo más creible.

![alt text](/assets/img/posts/hackingwifi/image-26.png)

![alt text](/assets/img/posts/hackingwifi/image-27.png)

Todas estas terminales se ocupan de crear el puntod de acceso, hacer el ataque de desautenticación, comprobar el psk introducido con el del handshake etc.

Una vez el usuario haya introducido la contraseña correcta el portal se cierra automáticamente y devuelve al usuario a su red normal y nosotros hemos conesguido la clave de acceso.

![alt text](/assets/img/posts/hackingwifi/image-28.png)

![alt text](/assets/img/posts/hackingwifi/image-29.png)

![alt text](/assets/img/posts/hackingwifi/image-30.png)

Al cerrar el proceso se genera este fichero con los intentos falidos de autenticación y el correcto.

![alt text](/assets/img/posts/hackingwifi/image-31.png)


