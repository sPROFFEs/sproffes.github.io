---
title: Creación de mapas de memoria RAM en linux
date: 2025-02-05 14:00:00 -0000
categories: [Forense, Linux]
tags: [Forense, memoria ram, linux, dump, memdump, volatility]
description: >
  Guía rápida de como crear mapas de memoria RAM en linux para Volatility 2 y 3.
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Introducción

Como vimos en el post de [Análisis básico de memoria RAM en linux](https://sproffes.github.io/posts/analisismemorialinux/), para analizar los dumps de memoria RAM en Linux es necesario tener el mapa correspondiente a la versión de linux que sse estaba utilizando en el momento de la captura.

Para ello he creado este post donde explico como crear los mapas de memoria RAM en linux.

# Preparación

## Instalación de Volatility 2 y 3

En el post mencionado anteriormente he explicado como instalar Volatility 2 y 3.

## Extraer la versión de Linux exacta del dump de memoria RAM

Vamos a extraer la versión de linux que estaba utilizando en el momento de la captura.

### Strings

```bash
❯ strings ram.lime| grep "Linux version"
        /* Used for emulating ABI behavior of previous Linux versions: */
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
00000] Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
MESSAGE=Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
MESSAGE=Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
```

### Volatility 2

No cuenta con funcionalidad especial para extraer los banners del dump de memoria RAM.

### Volatility 3

```bash
❯ python3 vol.py -f ram.lime banners
Volatility 3 Framework 2.20.0
Progress:  100.00               PDB scanning finished                  
Offset  Banner

0x9687160       Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x9a379e4       Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3788f624      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3942e7df      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3a300264      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3b2037a8      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3c275ea4      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3d895ae4      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
0x3da173e8      Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
```


# Creación de perfil para Volatility 2

Para crear el perfil para Volatility 2 primeramente necesitamos una maquina virtual con el sistema operativo exacto a las cabeceras de la memoria RAM.

Una vez tengamos el sistema, vamos a descargar desde el repositorio de Volatility 2 las herramientas para crear el perfil de datos dwarf.

[Github](https://github.com/volatilityfoundation/volatility)

Una vez descargados los archivos, vamos a crear el perfil de datos dwarf, pero para ello vamos a necesitar instalar lo siguiente:

```bash
sudo apt install build-essential
sudo apt install linux-headers-$(uname -r)
sudo apt install linux-image-$(uname -r) && sudo apt install linux-image-$(uname -r)-dbg
```

#### Modificar el código

Si a la hora de compilar el código nos aparece el siguiente error:

```bash
/home/kali/Desktop/volatility/tools/linux/module.c:136:9: warning: "__rcu" redefined
  136 | #define __rcu
      |         ^~~~~
In file included from <command-line>:
/usr/src/linux-headers-6.11.2-common/include/linux/compiler_types.h:61:10: note: this is the location of the previous definition
   61 | # define __rcu          BTF_TYPE_TAG(rcu)
      |          ^~~~~
```
Vamos a modificar el código de module.c para que no se genere el error.

```bash
nano volatility/tools/linux/module.c
```
Cambias el siguiente código:

```bash
#define __rcu
```
Por:

```bash
#define __rcu BTF_TYPE_TAG(rcu)
```

O

```bash
#ifndef __rcu
#define __rcu
#endif
```
Al final del archivo agregaremos:

```bash
MODULE_LICENSE("GPL");
```

Ahora si podemos ejecutar el siguiente comando:

```bash
cd volatility/tools/linux
make
```

Esto nos generará un archivo llamado `module.dwarf` que será el perfil de datos.

Ahora simplemente vamos a copiar el contenido de la carpeta /usr/lib/debug/boot y vamos a crear un fichero zip de la carpeta boot y el perfil de datos.

```bash
cp -r /usr/lib/debug/boot .
mv /volatility/tools/linux/module.dwarf .
zip -r debian-XXXX-memmap.zip boot
```

Ahora si como hicimos en el post de analisis de memoria RAM en linux, copiamos el zip en la carpeta volatility/volatility/plugins/overlays/linuxdebian-XXXX-memmap.zip y ejecutamos el vol.py



# Creación de perfil para Volatility 3

Para crear el perfil para Volatility 3 vamos a seguir los mismos pasos que para Volatility 2 pero en este caso no es estrictamente necesario estar en una maquina con el mismo kernel que el que estaba utilizando en la captura de memoria RAM.

A pesar de ser recomendado, no es necesario tener una maquina virtual con el mismo kernel que el que estaba utilizando en la captura de memoria RAM.

La diferencia es que en el caso de no contar con una maquina que se base en el mismo kernel que el que estaba utilizando en la captura de memoria RAM, es necesario descargar el kernel del mismo kernel que estaba utilizando en la captura de memoria RAM.

```bash
sudo apt install linux-image-<version-kernel> && sudo apt install linux-image-<version-kernel-dbg
```

[Dwarf2json](https://github.com/volatilityfoundation/dwarf2json)

Para poder compilar el código es necesario instalar el lenguaje de programación Golang.

```bash
sudo apt install golang
```

Una vez instalado el lenguaje de programación, vamos a descargar el código fuente del proyecto.

```bash
git clone https://github.com/volatilityfoundation/dwarf2json.git 
cd dwarf2json
go build
```

Se nos creará un binario llamado `dwarf2json` que será el ejecutable para poder generar los perfiles de datos formato json.xz que utiliza Volatility 3.

```bash
./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-XXXX | xz -9 linux-image-XXXX-memmap.json.xz
./dwarf2json linux --elf /usr/lib/debug/boot/vmlinux-XXXX --system-map /usr/lib/debug/boot/system.map-XXXX | xz -9 linux-image-XXXX-memmap.json.xz
```

Ahora movemos los mapas de memoria RAM a la carpeta /volatility3/volatility3/symbols/linux

# Creación de perfil para Volatility 2 y 3 de forma automática

Para esta tarea he creado un script que se encarga de crear los perfiles de datos de forma automática.

Aunque es funcional en los sistemas basados en debian no ha sido probado en otros sistemas operativos.

A pesar de esto aqui dejo el script para que puedas verlo y modificarlo si lo necesitas.

[Linux Memory Mapper](https://github.com/sPROFFEs/LinuxMemMapper)

En el repositorio se encuentra el script junto con la herramienta utilizada por volatility 2 para crear los perfiles de datos y necesita ser compilada con el mismo kernel que el que estaba utilizando en la captura de memoria RAM y el binario dwarf2json ya compilado y listo para usar ya que no necesita ser compilado con el kernel del sistema operativo que estaba utilizando en la captura de memoria RAM.

![alt text](/assets/img/posts/linuxmemorymaps/image.png)

![alt text](/assets/img/posts/linuxmemorymaps/image-1.png)
