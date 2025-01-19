---
title: Naabu y Netcat
date: 2023-06-07 00:00:00 +0000
categories: [Reconocimiento, Naabu & Netcat]
tags: [network, scanning, naabu, netcat]
---

## Naabu

Es posible que al ser NMAP la herramienta de reconocimiento de redes más usada y potente algunas IDS y sistemas de seguridad estén bien orientados hacia los métodos que usa y evitar así posibles intrusiones por lo que a veces es recomendado utilizar otras opciones

```
https://github.com/projectdiscovery
```

Esta herramienta pertenece a ProjectDiscovery que tienen varias soluciones y herramientas opensource muy interesantes. Naabu es una herramienta de escaneo de puertos escrita en Go que te permite enumerar de manera rápida y confiable los puertos válidos para hosts. Es una herramienta bastante simple que realiza escaneos rápidos de SYN/CONNECT/UDP en el host o lista de hosts y enumera todos los puertos que devuelven una respuesta.

```bash
sudo apt-get install naabu

naabu 192.168.20.0/24
```

Es una herramienta menos completa que NMAP pero que igualmente es útil y es conveniente tenerla en cuenta

## Netcat

De igual manera también podemos hacer un escaneo manual de los puertos con NETCAT. Netcat es la "navaja suiza" en herramientas de hacking porque permite recibir conexiones de red y establecer conexión de red con un nodo en la misma red.

```bash
netcat -nv 192.168.20.130 80 

-n → no resolución DNS 

-v → verbose 
```

De esta forma podemos manualmente emitir pequeños paquetes a direcciones concretas en puertos concretos. Podemos realizar un escaneo de puertos de forma activa ya sabiendo el HOST objetivo pero con ciertas precauciones.

```bash
netcat -nvw2 192.168.20.128 1-100

-w2 → timetout para las conexiones 
```

De nuevo escanear de forma mas comedida levantará menos alertas. Para extraer el servicio del puerto en concreto:

```bash
netcat -nv 192.168.20.128 21
```

Esto no alertará porque es un request normal y no es sospechoso. De igual forma podemos reconocer que host están activos de la siguiente forma:

```bash
netcat -nv 192.168.20.128 90
```

En este caso el puerto no esta activo por lo que no existe pero si ejecutamos el comando y capturamos con wireshark veremos que:

![Wireshark Capture](/assets/img/posts/reconocimiento/20241127_211647_4-3.png)

El host responderá de vuelta con un reset indicando que en ese puerto no está activo pero si hace un reset del TCP significa que el host está activo.