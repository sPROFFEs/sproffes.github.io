---
title: Clonado en caliente y con cifrado
date: 2024-11-01 11:58:38 +0000
categories: [Forense, Discos]
tags: [forensics, clonado, bitlocker, tpm]
---

## Tabla de Contenidos
1. [Configuración TPM](#configuración-tpm)
2. [Clonación de Disco con DD y FTK](#clonación-de-disco-con-dd-y-ftk)
3. [Clonación de Directorio con FTK Imager](#clonación-de-directorio-con-ftk-imager)
4. [Proceso de Cifrado](#proceso-de-cifrado)
5. [Clonado del disco cifrado](#proceso-de-clonado-en-disco-con-bitlocker)
6. [Clonado del directorio dentro del disco cifrado](#clonado-directorio-cifrado-dentro-de-disco-con-bitlocker)

## Configuración TPM

### Configuración en Máquina Virtual
Para máquinas virtuales, es necesario realizar una configuración especial del TPM antes de poder activar BitLocker.

> La simulación del chip TPM es necesaria en entornos virtuales.
{: .prompt-warning }

![Configuración TPM](/assets/img/posts/evidencias_en_caliente/tpm-config.png)
![Configuración TPM](/assets/img/posts/evidencias_en_caliente/tmp1.png)
_Configuración del TPM en entorno virtual_

## Clonación de Disco con DD y FTK

### Paso 1: Preparación del Entorno
Asegúrese de tener en cuenta el tamaño de los discos para el sistema operativo Windows 10 Pro y abra CMD como administrador.

> Siempre verifique los requisitos de espacio en disco antes de comenzar el proceso de clonación.
{: .prompt-tip }

![Listado de discos en CMD](/assets/img/posts/evidencias_en_caliente/disk-listing.png)
_Listado de discos físicos en CMD_

![Comando de clonado DD](/assets/img/posts/evidencias_en_caliente/clonado-dd.png)
_Comando de clonado DD_

![montado en FTK](/assets/img/posts/evidencias_en_caliente/montaje3.png)
![montado en FTK](/assets/img/posts/evidencias_en_caliente/montaje2.png)
![montado en FTK](/assets/img/posts/evidencias_en_caliente/montaje1.png)
_Montado en FTK Imager_

## Clonación de Directorio con FTK Imager

> Nota: Este proceso excluye archivos eliminados, metadatos y archivos del sistema.
{: .prompt-warning }

![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir1.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir2.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir3.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir4.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir5.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir6.png)
![Clonación de directorio en FTK](/assets/img/posts/evidencias_en_caliente/dir7.png)
_Proceso de clonación de directorio_

## Proceso de Cifrado

### Cifrado con Bitlocker
El proceso requiere modificar una política de BitLocker para permitir el uso en dispositivos TPM no compatibles.

> Guarde la clave de recuperación en un lugar seguro.
{: .prompt-tip }

![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif1.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif2.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif3.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif4.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif5.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif6.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif7.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif8.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif9.png)
_Proceso de configuración de BitLocker_

### Proceso de Cifrado
El cifrado del disco se realizará al reiniciar el equipo.

![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif10.png)
![Configuración de BitLocker](/assets/img/posts/evidencias_en_caliente/cif11.png)
_Progreso del proceso de cifrado_

## Proceso de clonado en disco con BitLocker

### FTK Imager
Ahora hacemos una imagen de clonado del disco completo con FTK.

> Clonará el disco completo encriptado
{: .prompt-tip }

![Verificación de hash](/assets/img/posts/evidencias_en_caliente/cloncif1.png)
_Verificación de integridad mediante hash_

### Acceso al Contenido Clonado
Ahora si montamos la imagen veremos como de las tres particiones que hay en el disco únicamente la de boot y recuperación de windows son visibles. Sin embargo vemos como la partición del disco principal de sistema no es reconocida.

![Verificación de contenido](/assets/img/posts/evidencias_en_caliente/cloncif2.png)
_Verificación de acceso al contenido encriptado clonado_

## Clonado directorio cifrado dentro de disco con BitLocker

Si de igual forma hacemos un clonado únicamente del directorio users del disco C.

> En este caso vemos que el clonado si es accesible debido a que el clonado es únicamente del directorio y no del disco completo por lo que los datos son obtenidos ya descifrados.
{: .prompt-tip }

![Verificación de hash](/assets/img/posts/evidencias_en_caliente/cifdir1.png)
_Directorio dentro del disco cifrado clonado_