---
title: Dump de memoria RAM y disco en Proxmox VE
date: 2025-03-03 14:00:00 +0000
categories: [Forense, Proxmox VE]
tags: [Proxmox VE, Memory Dump, Disk Dump, Proxmox VE, Memory Dump, Disk Dump, Proxmox VE, Memory Dump, Disk Dump, Proxmox VE, Memory Dump, Disk Dump]
image:
  path: /assets/img/cabeceras_genericas/proxmoxlogo.png
  alt:  Proxmox logo
description: >
  Guía para volcado de memoria y disco en Proxmox VE
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Introducción 

En esta sección vamos a ver como podemos realizar una extracción de datos en caliente o post mortem de una máquina virtual dentro de un servidor administrado por Proxmox VE.

Para realizar la extracción de estos datos es necesario tener en cuenta que debemos tener acceso a un usuario administrador de Proxmox VE, ya que los comandos que vamos a ver a continuación son ejecutados con privilegios elevados.

En el entorno de virtualización de Proxmox VE, las máquinas o contenedores virtuales son administrador por QEMU por lo que para el caso del volcado de memoria RAM es necesario que el sistema operativo de la máquina virtual tenga instalado el agente QEMU (qemu-guest-agent) para que este pueda ser monitoreado por QEMU.

Aunque los siguientes comandos son ejecutados directamente sobre el servidor Proxmox VE, vamos a tomar en consideración que la salida de los datos vamos a realizarla sobre nuestro equipo local.

## Memory Dump o volcado de memoria RAM

Primero vamos a localizar el ID de la máquina virtual que queremos realizar el volcado de memoria RAM.

Dentro de nuestra shell SSH del usuario administrador de Proxmox VE, vamos a utilizar el comando:

```bash
qm list
```

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image.png)

Una vez localizado el ID de la máquina virtual que queremos realizar el volcado de memoria RAM, vamos a realizar el volcado de memoria RAM con el siguiente comando:

```bash
qm monitor <ID de la máquina virtual> 
```

Dentro del interprete 

```bash
dump-guest-memory -d /tmp/<ID de la máquina virtual>_mem.dump
```

Creado el dump de memoria RAM ahora debemos comprobar que se encuentra en el directorio /tmp/ y que está completo.

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-1.png)

Ahora desde una terminal en nuestra máquina local, vamos a utilizar el comando:

```bash
scp -C -p root@100.104.163.41:/tmp/118_mem.dump ./118_mem.dump
```

Indicamos `-p` para que mantenga la fecha de acceso y modificación y `-C` para forzar la compresión del archivo en la transferencia y que sea más rápido.

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-2.png)

Al encontrase el dump en el directorio tmp dentro del servidor Proxmox VE podemos eliminarlo manualmente o esperar a que se elimine automáticamente.

## Volcado de disco

Para este proceso necesitamos el mismo ID de la máquina virtual que hemos encontrado anteriormente y ver en qué ubicación se encuentra el disco duro de la máquina virtual.

```bash
qm config 118
```

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-3.png)

En este caso solo tiene un disco que se encuentra en local-lvm.

Para verficar que se encuentra en dicha ubicación podemos utilizar el comando:

```bash
pvesm list local-lvm
```

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-4.png)

Para saber la ubicación exacta del disco:

```bash
pvesm path local-lvm:vm-118-disk-0
```

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-5.png)

Ahora tenemos dos opciones, si la máquina está encendida y no podemos apagarla o si por el contrario la máquina está apagada.

### En caso de que la máquina está encendida

Creamos una snapshot de la máquina virtual:

```bash
sudo lvcreate -L 12G -s -n vm-118-disk-snap /dev/pve/vm-118-disk-0
```
> Aviso : Hay que tener en cuenta que el tamaño del snapshot tiene que ser el mismo que el del disco duro de la máquina virtual que podemos ver en el comando `qm config <ID de la máquina virtual>`.
{: .prompt-warning}

Pasamos el snapshot a formato raw:

```bash
sudo qemu-img convert -O raw /dev/pve/vm-118-disk-snap /tmp/vm-118-disk.raw
```

Ahora podemos eliminar el snapshot:

```bash
sudo lvremove -f /dev/pve/vm-118-disk-snap
```
![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-6.png)

### En caso de que la máquina está apagada

En este caso es más sencillo crear un snapshot de la máquina virtual.

```bash
sudo qemu-img convert -O raw /dev/pve/vm-118-disk-0 /tmp/vm-118-disk.raw
```

![alt text](/assets/img/posts/proxmox_volcado_disco_ram/image-7.png)

Ahora podemos copiar el archivo a nuestro equipo local:

```bash
scp -C -p root@100.104.163.41:/tmp/vm-118-disk.raw ./vm-118-disk.raw
```

## Conclusiones

Finalmente con el dump de memoria RAM y el volcado de disco podemos realizar una extracción de datos en caliente o post mortem de estas imágenes para su análisis e investigación mediante FTK, Autopsy, Volatility, etc.

