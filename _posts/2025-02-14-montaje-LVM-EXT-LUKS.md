---
title: Montaje LVM EXT LUKS - Linux
date: 2025-02-14 11:00:00 +0000
categories: [Forense, Linux]
tags: [Linux, Forense, Discos, Montaje, LVM, EXT, LUKS]
description: >
  Guía de montaje de discos EXT LUKS LVM de linux para análisis de datos.
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Introducción

Como sabemos, el sistema de almacenamiento en sistemas Windows es estructurado y manejado de forma diferente a Linux.

En linux se ha ido perfeccionando y ofreciendo al usuario diferentes opciones de almacenamiento, como LVM, ZFS, etc.

Para realizar clonados de disco y analizar su contenido efectivamente, el profesional forense necesita:

- Dominar los diferentes sistemas de archivos que usa Linux
- Saber cómo acceder y analizar la información almacenada en estos sistemas
- Estar preparado para manejar configuraciones más complejas como:

    - LVM (Logical Volume Management)
    - ZFS (Sistema de archivos avanzado)
    - LUKS (Sistema de encriptación)


El desafío aumenta cuando nos encontramos con estas configuraciones avanzadas, ya que hacen más complejo el proceso de acceder a la información almacenada. Por eso es crucial que el profesional forense tenga conocimientos profundos de estas tecnologías y sepa cómo abordar cada caso según sus características específicas.

# Conociendo los sistemas de archivos

Para poder analizar el contenido de los discos, es necesario conocer los diferentes sistemas de archivos que ofrece Linux y conocer sus diferencias con los sistemas de archivos de Windows.

Las principales diferencias entre estos sistemas de archivos y gestores de volúmenes son las sigueintes:

## NTFS (Windows)
- Desarrollado por Microsoft como sucesor de FAT32

- Características principales:
  - Soporta archivos de gran tamaño (más de 4GB)
  - Sistema de permisos básico
  - Journaling (registro de cambios para prevenir corrupción)
  - Compresión y encriptación a nivel de archivo
  - Cuota de disco
  - Enlaces simbólicos limitados

## Sistemas de archivos Linux

### EXT (Extended File System) y sus versiones

- **EXT2**: 
  - Primera versión robusta para Linux
  - Sin journaling
  - Bueno para memorias flash por menos escrituras

- **EXT3**:
  - Añade journaling
  - Compatible hacia atrás con EXT2
  - Mejor protección contra corrupción de datos

- **EXT4** (Actual estándar):
  - Mejor rendimiento y escalabilidad
  - Soporta volúmenes más grandes
  - Extents (mejor manejo de archivos grandes)
  - Asignación retrasada (mejor rendimiento)
  - Checksums en el journal
  - Timestamps con nanosegundos

### LVM (Logical Volume Management)
- No es un sistema de archivos, sino un gestor de volúmenes
- Características:
  - Permite redimensionar volúmenes en caliente
  - Snapshots (copias instantáneas)
  - Striping y mirroring
  - Agrupación flexible de discos
  - Puede usar cualquier sistema de archivos encima

### LVM Encrypted (LUKS)
- LVM con encriptación mediante LUKS
- Ventajas:
  - Encriptación completa del volumen
  - Múltiples claves posibles
  - Mayor seguridad que la encriptación de NTFS
  - Gestión flexible de claves

### ZFS
- Sistema de archivos avanzado originalmente de Sun Microsystems
- Características destacadas:
  - Integra gestión de volúmenes y sistema de archivos
  - Protección contra corrupción de datos mediante checksums
  - Compresión en tiempo real
  - Deduplicación
  - Snapshots muy eficientes
  - RAID a nivel de sistema de archivos
  - Autoreparación cuando se usa con mirrors
  - Caché en RAM y SSD (ARC y L2ARC)

## Principales diferencias

1. **Capacidad de gestión**:
   - NTFS: Gestión básica de volúmenes
   - LVM: Gestión avanzada y flexible
   - ZFS: Gestión integrada y muy avanzada

2. **Integridad de datos**:
   - NTFS: Journaling básico
   - EXT4: Journaling mejorado
   - ZFS: Checksums y autoreparación

3. **Características avanzadas**:
   - NTFS: Limitadas
   - EXT4: Moderadas
   - ZFS: Muy extensas (snapshots, compresión, deduplicación)

4. **Flexibilidad**:
   - NTFS: Limitada
   - LVM: Alta para gestión de volúmenes
   - ZFS: Alta para todo el stack de almacenamiento

5. **Escalabilidad**:
   - NTFS: Limitada
   - EXT4: Buena
   - ZFS: Excelente

6. **Recuperación de datos**:
   - NTFS: Herramientas maduras disponibles
   - EXT: Buenas herramientas disponibles
   - ZFS: Autoreparación y snapshots facilitan recuperación

7. **Rendimiento**:
   - NTFS: Bueno en Windows, limitado en Linux
   - EXT4: Muy bueno en Linux
   - ZFS: Excelente pero requiere más recursos

Esta comparación muestra cómo los sistemas de archivos Linux tienden a ofrecer más características avanzadas y flexibilidad, especialmente con soluciones como ZFS, mientras que NTFS se mantiene más simple pero efectivo para su uso principal en Windows.


# Montaje EXT4 

Se trata de un dispositivo ext4 donde sería necesario montar las particiones que se identifiquen y aplicar en ellas herramientas para la recuperación de datos borrados.

## Testdisk

```bash
testdisk imagen.dd
```

Analizamos la imagen de disco para ver las particiones.

![alt text](/assets/img/posts/lvm-ext-luks/image.png)

Observamos tres particiones donde la segunda se trata del swap, siendo la primera y tercera las del sistema de archivos principal.

![alt text](/assets/img/posts/lvm-ext-luks/image-1.png)

Si pulsamos `p` en la partición podremos ver los archivos disponibles en ella.

![alt text](/assets/img/posts/lvm-ext-luks/image-2.png)

Parecen los archivos dl sistema, configuración de red, etc.

En la tercera partición no parece haber nada interesante a primera vista.

![alt text](/assets/img/posts/lvm-ext-luks/image-3.png)

### Investigar los datos manualmente

Antes de ejecutarlo vamos a extraer las particiones que queramos analizar ya que, como hemos visto y vamos a ver ahora de nuevo, existen diferentes particiones.

Con mmls podemos ver rápidamente las particiones que tenemos en nuestro disco.

![alt text](/assets/img/posts/lvm-ext-luks/image-5.png)

Ahora las extreamos por separado.

```bash
# Extraer primera partición
dd if=datos.dd of=particion1.img bs=512 skip=2048 count=307200

# Extraer segunda partición
dd if=datos.dd of=particion3.img bs=512 skip=616448 count=407552
```

![alt text](/assets/img/posts/lvm-ext-luks/image-6.png)

```bash	
# Crear directorios para montar
sudo mkdir -p /mnt/part1
sudo mkdir -p /mnt/part3
```
```bash
# Montar primera partición
sudo mount -o ro,loop particion1.img /mnt/part1

# Montar segunda partición
sudo mount -o ro,loop particion3.img /mnt/part3
```

![alt text](/assets/img/posts/lvm-ext-luks/image-7.png)

Como vemos lo único que monta de la imagen es el directorio que con testdisk nos indicaba en blanco.

Esto es porque el resto de archivos en rojo posiblemente estuviesen eliminados.

![alt text](/assets/img/posts/lvm-ext-luks/image-8.png)

Para la partición 3 no tenemos nada.

![alt text](/assets/img/posts/lvm-ext-luks/image-9.png)

### Recuperar todos los archivos de las particiones con testdisk.

Para ello vamos a aprovechar que hemos extraido las particiones en diferentes archivos.

```bash
testdisk particion1.img
```
Ahora cuando tengamos la lista de archivos podemos seleccionar todos con `a` y luego shift + `c` para copiar todos al la ubicación de destino.

![alt text](/assets/img/posts/lvm-ext-luks/image-10.png)

![alt text](/assets/img/posts/lvm-ext-luks/image-11.png)

Ahora si podremos ver los archivos 

![alt text](/assets/img/posts/lvm-ext-luks/image-12.png)

![alt text](/assets/img/posts/lvm-ext-luks/image-13.png)

# Montaje LVM 

Con un análisis rápido de mmls vemos:

```bash	
❯ mmls lvm.dd
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000999423   0000997376   Linux (0x83)
003:  -------   0000999424   0001001471   0000002048   Unallocated
004:  Meta      0001001470   0010692607   0009691138   DOS Extended (0x05)
005:  Meta      0001001470   0001001470   0000000001   Extended Table (#1)
006:  001:000   0001001472   0010692607   0009691136   Linux Logical Volume Manager (0x8e)
007:  -------   0010692608   0010692767   0000000160   Unallocated
```
### Repaso de los datos de mmls

1. **Información General**:
- `DOS Partition Table`: Indica que usa el esquema de particionado MBR (Master Boot Record)
- `Offset Sector: 0`: El inicio de la tabla de particiones
- `Units are in 512-byte sectors`: Cada sector es de 512 bytes

2. **Columnas**:
- `Slot`: Identificador de la entrada en la tabla
- `Start`: Sector donde inicia la partición
- `End`: Sector donde termina la partición
- `Length`: Número total de sectores
- `Description`: Tipo de partición

3. **Particiones encontradas**:
```
000: Meta 0000000000-0000000000 (1 sector)
- La tabla de particiones primaria
- Ocupa el primer sector del disco

001: Unallocated 0000000000-0000002047 (2048 sectores)
- Espacio no asignado al inicio
- Típicamente reservado para el bootloader

002: Linux 0000002048-0000999423 (997,376 sectores)
- Partición Linux primaria (0x83)
- Probablemente contiene el sistema de archivos /boot

003: Unallocated 0000999424-0001001471 (2048 sectores)
- Pequeño espacio no asignado entre particiones

004: DOS Extended 0001001470-0010692607 (9,691,138 sectores)
- Partición extendida que contiene particiones lógicas
- Actúa como contenedor para particiones lógicas

005: Extended Table (#1)
- Tabla de particiones extendida
- Gestiona las particiones lógicas

006: Linux LVM 0001001472-0010692607 (9,691,136 sectores)
- Partición lógica tipo LVM (0x8e)
- Contiene los volúmenes físicos para LVM

007: Unallocated 0010692608-0010692767 (160 sectores)
- Espacio no asignado al final del disco
```

**Estructura general**:
1. Tiene una partición Linux normal al inicio (probablemente /boot)
2. Luego una partición extendida que contiene:
   - Una partición lógica LVM que ocupa casi todo el espacio
3. Pequeños espacios sin asignar al inicio y final del disco

Esta estructura es típica de una instalación Linux que usa LVM, donde:
- /boot está en una partición normal
- El resto del sistema está en LVM para flexibilidad en la gestión del espacio

La partición LVM está en el sector 1001472 y es lógica. Vamos a montarla:

Para montarla primero debemos calcular el offset en sectores.

```bash
# Calcular offset en sectores
❯ echo $((1001472 * 512))

512753664
```
Ahora creamos el loop de la partición.

```bash
sudo losetup -o 512753664 /dev/loop0 lvm.dd
```
Si hacemos un escaneo en el equipo para detectar el sistema LVM vemos que lo detecta.

```bash	
sudo pvscan --cache
  pvscan[83562] PV /dev/loop0 online.
```

Verificamos que detecta el volumen físico.

```bash
❯ sudo pvs

  PV         VG        Fmt  Attr PSize   PFree 
  /dev/loop0 debian-vg lvm2 a--   <4.62g     0 
  /dev/sda5  kali-vg   lvm2 a--  <39.52g 36.00m
```

Como vemos parece que incluso detecta el sistema del origen de la imagen.

Ahora, aunque detecte 1 solo volumen físico, dentro puede haber un grupo de volúmenes lógicos.

```bash
❯ sudo vgchange -ay
  2 logical volume(s) in volume group "kali-vg" now active
  3 logical volume(s) in volume group "debian-vg" now active
```

Como vemos ha detectado 3 volúmenes lógicos dentro de la imagen.

Para listarlos_

```bash
❯ sudo lvs

  LV     VG        Attr       LSize   Pool Origin Data%  Meta%  Move Log Cpy%Sync Convert
  home   debian-vg -wi-a-----  <1.01g                                                    
  root   debian-vg -wi-a-----  <2.66g                                                    
  swap_1 debian-vg -wi-a----- 976.00m                                                    
  root   kali-vg   -wi-ao----  38.53g                                                    
  swap_1 kali-vg   -wi-ao---- 976.00m 
```
Cabe recalcar que los que nos interesan son los etiquetados como "debian-vg" ya que el resto son del sistema nativo.

Observamos que el sistema cuenta con tres volúmenes lógicos; el home, root y swap.

Esto indica que a la hora de instalar el sistema operartivo se seleccionó la separación del sistema principal de datos del sistema y el de usuarios.

## Montado de particiones lógicas

Para montar ahora estos volúmenes lógicos hacemos los siguiene:

> Nota: Si intentamos montar el volumen /dev/loop0 esto dará error puesto que se trata de un volumen físico y no de un volumen lógico LVM y esto no es reconocido por el sistema.
{: .prompt-info }

```bash
❯ mkdir lvm_evidence
❯ sudo mount -o ro /dev/debian-vg/home /mnt/lvm_evidence
❯ sudo mkdir /mnt/lvm_root
❯ sudo mount -o ro /dev/debian-vg/root /mnt/lvm_root
```

Ahora si podemos acceder a los datos de home y root.

![alt text](/assets/img/posts/lvm-ext-luks/image-14.png)

Para desmontar y eliminar las particiones lógicas:

```bash
# Desmontar
sudo umount /mnt/evidencia

# Desactivar grupo de volúmenes
sudo vgchange -an debian-vg
  0 logical volume(s) in volume group "debian-vg" now active

# Eliminar dispositivo loop
sudo losetup -d /dev/loop0
```

# Montaje LUKS

Contamos con una imagen de disco EXT con cifrado LUKS y su contraseña.

Analizamos particiones con mmls.

```bash
❯ mmls cifrado.dd
DOS Partition Table
Offset Sector: 0
Units are in 512-byte sectors

      Slot      Start        End          Length       Description
000:  Meta      0000000000   0000000000   0000000001   Primary Table (#0)
001:  -------   0000000000   0000002047   0000002048   Unallocated
002:  000:000   0000002048   0000204799   0000202752   Linux (0x83)
```

Vemos que es una partición EXT2 sencilla.

Para comprobar que es LUKS primero creamos el loop de la partición.

```bash
sudo losetup -o $((2048 * 512)) /dev/loop0 cifrado.dd
```
En este caso el offset es 2048 * 512 bytes.

Comprobamos que es LUKS.

```bash
❯ sudo cryptsetup luksDump /dev/loop0
LUKS header information
Version:       	2
Epoch:         	3
Metadata area: 	16384 [bytes]
Keyslots area: 	16744448 [bytes]
UUID:          	e6e46028-6623-466a-b144-e8d92cb632be
Label:         	(no label)
Subsystem:     	(no subsystem)
Flags:       	(no flags)

Data segments:
  0: crypt
	offset: 16777216 [bytes]
	length: (whole device)
	cipher: aes-xts-plain64
	sector: 512 [bytes]

Keyslots:
  0: luks2
	Key:        512 bits
	Priority:   normal
	Cipher:     aes-xts-plain64
	Cipher key: 512 bits
	PBKDF:      argon2i
	Time cost:  4
	Memory:     261099
	Threads:    1
	Salt:       44 7e f4 53 61 59 5d c5 96 59 90 87 16 36 e4 bd 
	           80 cd 41 db df 5f 90 b9 05 e3 9a 36 06 7e 70 b3 
	AF stripes: 4000
	AF hash:    sha256
	Area offset:32768 [bytes]
	Area length:258048 [bytes]
	Digest ID:  0
Tokens:
Digests:
  0: pbkdf2
	Hash:       sha256
	Iterations: 86118
	Salt:       5c 3f 34 96 21 dc 8a b9 6a d9 e5 ed f9 10 d1 9a 
	           c0 cc 65 c6 4c ee 0f d3 5b 83 00 2d 3a ac 8b 17 
	Digest:     37 9e 6d b9 a3 12 55 79 60 6d 04 88 a6 10 64 3d 
	           d8 4a c4 80 b8 d7 d6 66 e2 e3 13 21 3f a8 ff 2b 
```

Efectivamente es LUKS, podemos ver las cabeceras de los datos de LUKS.

Ahora tenemos varias opciones para montar el disco LUKS.

## GUI

Si contamos con una interfaz gráfica, lo más sencillo es una vez que montamos el disco loop nos mostrará el disco indicando que es LUKS.

Simplemente damos click y nos pedirá la contraseña para poder montar el disco.

![alt text](/assets/img/posts/lvm-ext-luks/image-15.png)

## CLI

Si no contamos con una interfaz gráfica podemos montar el disco LUKS de la siguiente manera:

```bash
❯ sudo cryptsetup luksOpen /dev/loop0 luks_descifrado
Enter passphrase for /home/kali/Downloads/cifrado.dd: 
```

![alt text](/assets/img/posts/lvm-ext-luks/image-16.png)

Vemos que ahora a la izquierda en el la interfaz ya no indica que está cifrado.

Ahora si podemos montar el disco descifrado.

```bash
# Crear punto de montaje
sudo mkdir /mnt/luks_evidence

# Montar en modo solo lectura
sudo mount -o ro /dev/mapper/luks_descifrado /mnt/luks_evidence
```

![alt text](/assets/img/posts/lvm-ext-luks/image-17.png)

## Desmontar

Para desmontar y eliminar las particiones lógicas:

```bash
# Desmontar
sudo umount /mnt/luks_evidence

# Cerrar LUKS
sudo cryptsetup luksClose luks_descifrado

# Eliminar dispositivo loop
sudo losetup -d /dev/loop0
```
