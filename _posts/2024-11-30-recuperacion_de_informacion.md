---
title: Recuperación de información
date: 2024-11-30 11:58:38 +0000
categories: [Forense, Discos]
tags: [windows, linux, mbr, testdisk, autopsy, recuperción de información]
---

## 1. Identificar el disco

Partimos de que tenemos una imagen de disco que queremos restaurar ya que se encuentra dañada. Lo primero es intentar identificar que tipo de sistema de particiones utiliza y para ello vamos a intentar identificarlo a bajo nivel.

![Automáticamente vemos como detecta el tipo MBR](/assets/img/posts/recuperacion_de_informacion/20241130_102548_Screenshot_from_2024-11-30_11-25-28.png)
_Automáticamente vemos como detecta el tipo MBR_

Ahora sabiendo esta información tenemos dos opciones:

- Restaurar la tabla de particiones para poder montar la imagen
- Intentar extraer los datos del disco con programas especializados

## 2. Restaurar la tabla MBR

### Testdisk

Primero vamos a tomar la opción de restaurar la tabla de particiones para poder montar la imagen y acceder al contenido.
Para esto vamos a hacer uso del siguiente software.

[TestDisk](https://www.cgsecurity.org/wiki/TestDisk_Download){:target="_blank"}

### Montar la imagen de disco con FTK

Para facilitar el trabajo vamos a montar la imagen a recuperar usando FTK y activar la escritura en el mismo

![Activar la escritura en el disco](/assets/img/posts/recuperacion_de_informacion/20241130_104507_Screenshot_from_2024-11-30_11-45-04.png)
_Activar la escritura en el disco_

### Ejecutar TestDisk

Ahora podemos ejecutar Testdisk_win que encontramos en la carpeta descargada

![Veremos que si nos muestra el disco montado, lo seleccionamos](/assets/img/posts/recuperacion_de_informacion/20241130_103635_Screenshot_from_2024-11-30_11-36-19.png)
_Veremos que si nos muestra el disco montado, lo seleccionamos_

Debemos tener en cuenta que al tratarse del sistema MBR debemos seleccionar la opcion INTEL/PC

![Intel PC](/assets/img/posts/recuperacion_de_informacion/20241130_103918_Screenshot_from_2024-11-30_11-38-58.png)

![Analizamos el disco en busca de particiones](/assets/img/posts/recuperacion_de_informacion/20241130_103940_Screenshot_from_2024-11-30_11-39-38.png)
_Analizamos el disco en busca de particiones_

![No detecta particiones a simple vista, damos en busqueda rápida](/assets/img/posts/recuperacion_de_informacion/20241130_104013_Screenshot_from_2024-11-30_11-40-11.png)
_No detecta particiones a simple vista, damos en busqueda rápida_

![Rápidamente detecta una partición NTFS, la seleccionamos](/assets/img/posts/recuperacion_de_informacion/20241130_104048_Screenshot_from_2024-11-30_11-40-46.png)
_Rápidamente detecta una partición NTFS, la seleccionamos_

![Escribimos los cambios](/assets/img/posts/recuperacion_de_informacion/20241130_104134_Screenshot_from_2024-11-30_11-41-29.png)
_Escribimos los cambios_

### Comprobación

Listo, en principio debemos tener recuperado el sistema de archivos y ser accesible desde FTK.

Aprovechamos que tenemos el disco montado con el mismo y vamos a comprobar que podemos acceder.

![Acceso completo a los archivos del disco](/assets/img/posts/recuperacion_de_informacion/20241130_104829_Screenshot_from_2024-11-30_11-48-27.png)
_Acceso completo a los archivos del disco_

### Información adicional

Adicionalmente ahora podemos verificar que sistemas de archivos tiene el disco mediante la comprobación del disco nuevamente con Active disk editor

![Ahora si detecta la partición correcta](/assets/img/posts/recuperacion_de_informacion/20241130_105959_Screenshot_from_2024-11-30_11-59-44.png)
_Ahora si detecta la partición correcta_

![Información adicional](/assets/img/posts/recuperacion_de_informacion/20241130_110032_Screenshot_from_2024-11-30_12-00-13.png)

## 3. Extracción de datos sin recuperar MBR

Para este método vamos a ver tres programas de extracción de datos

### Bulk Extractor

[Version 1.5.0 graphical installer with Windows GUI](https://digitalcorpora.s3.amazonaws.com/downloads/bulk_extractor/bulk_extractor-1.5.0-windowsinstaller.exe){:target="_blank"}

[Version 2.0 command-line EXE](https://digitalcorpora.s3.amazonaws.com/downloads/bulk_extractor/bulk_extractor-2.0.0-windows.zip){:target="_blank"}

Importamos la imagen del disco dañada y añadir un directorio de salida

![En el icono del engranaje podemos importar](/assets/img/posts/recuperacion_de_informacion/20241130_110925_Screenshot_from_2024-11-30_12-09-14.png)
_En el icono del engranaje podemos importar_

Una vez haya extraido los datos los muestra como un registro de tareas que se han realizado, url visitadas, emails, archivos zip, etc...

![También podemos ver los datos raw de los archivos del disco](/assets/img/posts/recuperacion_de_informacion/20241130_111214_Screenshot_from_2024-11-30_12-12-11.png)
_También podemos ver los datos raw de los archivos del disco_

### Autopsy

[Autopsy Forensics](https://www.autopsy.com/){:target="_blank"}

Este software es uno de los más conocidos y utilizados debido a su versatilidad.

Vamos a ver que datos consigue extraer del disco.

![Creamos un caso de prueba](/assets/img/posts/recuperacion_de_informacion/20241130_111512_Screenshot_from_2024-11-30_12-15-05.png)
_Creamos un caso de prueba_

![Seleccionamos la imagen del disco y dejamos el resto por defecto hasta ejecutar](/assets/img/posts/recuperacion_de_informacion/20241130_111631_Screenshot_from_2024-11-30_12-16-25.png)
_Seleccionamos la imagen del disco y dejamos el resto por defecto hasta ejecutar_

![Análisis en proceso](/assets/img/posts/recuperacion_de_informacion/20241130_111941_Screenshot_from_2024-11-30_12-19-20.png)

Si analizamos el contenido vemos que realmente si a completado la extracción de los archivos que hay en el disco.

Si hacemos click derecho en cualquiera de los documentos o ficheros podremos extraerlos.

![Vemos que tambíen nos extrae metadatos de ciertos rastros que pueden ser interesantes](/assets/img/posts/recuperacion_de_informacion/20241130_112135_Screenshot_from_2024-11-30_12-21-29.png)
_Vemos que tambíen nos extrae metadatos de ciertos rastros que pueden ser interesantes_

### Photorec Testdisk

Por último vamos a usar la extensión photorec del software anteriormente utilizado Testdisk.

Aunque inicialmente fue pensado para recuperar imágenes es capaz de recuperar cualquier tipo de archivo y es muy intuitivo.

Lo tenemos disponible en la misma carpeta que descargamos de testdisk.

Ejecutamos qphotorec_win

![Importamos la imagen del disco dañado y seleccionamos el directorio de salida](/assets/img/posts/recuperacion_de_informacion/20241130_112515_Screenshot_from_2024-11-30_12-25-08.png)
_Importamos la imagen del disco dañado y seleccionamos el directorio de salida_

![Como ya sabemos con anterioridad que es sistema NTFS lo seleccionamos](/assets/img/posts/recuperacion_de_informacion/20241130_112656_Screenshot_from_2024-11-30_12-26-53.png)
_Como ya sabemos con anterioridad que es sistema NTFS lo seleccionamos_

Ejecutamos y sin más pasos simplemente indica los archivos que ha recuperado.

Si vamos al directorio de salida los podremos encontrar.

![Resultados de la recuperación](/assets/img/posts/recuperacion_de_informacion/20241130_112840_Screenshot_from_2024-11-30_12-28-33.png)

Se trata de una herramienta sencilla pero potente aunque como su enfoque no es de análisis forense no proporciona tanta información como los anteriores programas.

## 4. Recuperación de arranque windows XP

Para esta sección vamos a intentar recuperar el arranque dañado de una máquina windows XP mediante testdisk.

El software de virtualización es virtualbox

![Versión de windows xp funcionando](/assets/img/posts/recuperacion_de_informacion/20241130_170236_Screenshot_from_2024-11-30_18-02-25.png)
_Versión de windows xp funcionando_

### Dañar el arranque

En este caso vamos a usar una imagen live de kali linux para poder dañar el disco de arranque de windows. 
Simplemente añadimos la imagen a la máquina y arrancamos desde linux

Una vez en kali 

```bash
sudo fdisk -l
```

![Identificamos el disco del sistema windows /dev/sda1](/assets/img/posts/recuperacion_de_informacion/20241130_171206_Screenshot_from_2024-11-30_18-11-52.png)
_Identificamos el disco del sistema windows /dev/sda1_

```bash
sudo dd if=/dev/zero of=/dev/sda1 bs=512 count=1
```

![Escribe ceros en los primeros 512 bytes](/assets/img/posts/recuperacion_de_informacion/20241130_171438_Screenshot_from_2024-11-30_18-14-33.png)
_Escribe ceros en los primeros 512 bytes_

![Podemos comprobar que el daño es correcto](/assets/img/posts/recuperacion_de_informacion/20241130_171551_Screenshot_from_2024-11-30_18-15-46.png)
_Podemos comprobar que el daño es correcto_

### Reparación con Testdisk

Ahora vamos a intentar reparar el sistema haciendo uso de testdisk. 

Hemos usado kali linux porque contamos con la ventaja de que viene preinstalado por lo que será más rápido.

```bash
sudo testdisk /dev/sda1
```

![Inicio de TestDisk](/assets/img/posts/recuperacion_de_informacion/20241130_171850_Screenshot_from_2024-11-30_18-18-45.png)

![Seleccionamos que no existen particiones](/assets/img/posts/recuperacion_de_informacion/20241130_172014_Screenshot_from_2024-11-30_18-20-09.png)
_Seleccionamos que no existen particiones_

![Análisis de particiones](/assets/img/posts/recuperacion_de_informacion/20241130_172048_Screenshot_from_2024-11-30_18-20-43.png)

![Indica que el sector de arranque está dañado pero el de respaldo es válido](/assets/img/posts/recuperacion_de_informacion/20241130_172123_Screenshot_from_2024-11-30_18-21-15.png)
_Indica que el sector de arranque está dañado pero el de respaldo es válido_

Elegimos la opción de backup boot sector

![Backup boot sector](/assets/img/posts/recuperacion_de_informacion/20241130_181526_Screenshot_from_2024-11-30_19-15-21.png)

![Si comprobamos de nuevo la integridad veremos que indica el sector de arranque correctamente](/assets/img/posts/recuperacion_de_informacion/20241130_172431_Screenshot_from_2024-11-30_18-24-23.png)
_Si comprobamos de nuevo la integridad veremos que indica el sector de arranque correctamente_

### Reparación con windows

Si no conseguimos arrancar de nuevo el sistema windows XP podemos intentar recuperar el arranque con el disco de instalación de windows

![Presionamos R](/assets/img/posts/recuperacion_de_informacion/20241130_173028_Screenshot_from_2024-11-30_18-29-27.png)
_Presionamos R_

![Dentro del sistema hacemos lo siguiente](/assets/img/posts/recuperacion_de_informacion/20241130_173402_Screenshot_from_2024-11-30_18-33-49.png)
_Dentro del sistema hacemos lo siguiente_

```bash
fixmbr
fixboot
bootcfg /rebuild
```

![Primeros pasos de recuperación](/assets/img/posts/recuperacion_de_informacion/Screenshot%20from%202024-12-05%2011-17-38.png)

Escribimos fixmbr y aceptamos con s

![Ejecutando fixmbr](/assets/img/posts/recuperacion_de_informacion/Screenshot%20from%202024-12-05%2011-20-11.png)

Escribimos fixboot y aceptamos con s

![Ejecutando fixboot](/assets/img/posts/recuperacion_de_informacion/Screenshot%20from%202024-12-05%2011-22-08.png)

Escribimos bootcfg /rebuild, aceptamos con s y presionamos enter dos veces.

Ahora reiniciamos escribiendo exit y al reiniciar ya tendremos el sistema de arranque arreglado.

## 5. Recuperación de arranque windows 7

Ahora vamos a realizar el mismo proceso pero de un sistema windows 7 en dualboot con debian

![Sistema inicial](/assets/img/posts/recuperacion_de_informacion/20241130_174918_Screenshot_from_2024-11-30_18-47-42.png)

### Comprobación

![Vemos que el sistema windows es funcional](/assets/img/posts/recuperacion_de_informacion/20241130_175004_Screenshot_from_2024-11-30_18-49-58.png)
_Vemos que el sistema windows es funcional_

### Proceso de dañar el arranque

Este proceso es exactamente igual que el anterior, arrancaremos kali live ya que el debian existente está desactualizado y tiene problemas de repositorios.

![Visualizamos las particiones del disco](/assets/img/posts/recuperacion_de_informacion/20241130_175806_Screenshot_from_2024-11-30_18-58-00.png)
_Visualizamos las particiones del disco_

En la primera partición donde indica boot es la que neceistamos modificar

![Modificación del boot](/assets/img/posts/recuperacion_de_informacion/20241130_180118_Screenshot_from_2024-11-30_19-01-11.png)

### Comprobación de arranque

![El sistema de arranque no funciona para windows 7](/assets/img/posts/recuperacion_de_informacion/20241130_180227_Screenshot_from_2024-11-30_19-02-07.png)
_El sistema de arranque no funciona para windows 7_

### Reparación con Testdisk

De nuevo arrancamos kali linux para reparar el sistema de arranque

```bash
sudo testdisk /dev/sda1
```

![Inicio de TestDisk](/assets/img/posts/recuperacion_de_informacion/20241130_180523_Screenshot_from_2024-11-30_19-05-17.png)

![Selección None](/assets/img/posts/recuperacion_de_informacion/20241130_180810_Screenshot_from_2024-11-30_19-08-04.png)
_None_

![Boot option](/assets/img/posts/recuperacion_de_informacion/20241130_180843_Screenshot_from_2024-11-30_19-08-32.png)
_Boot_

![Backup BS](/assets/img/posts/recuperacion_de_informacion/20241130_180918_Screenshot_from_2024-11-30_19-09-01.png)
_Backup BS_

![Ahora reiniciamos para comprobar el arranque de windows](/assets/img/posts/recuperacion_de_informacion/20241130_181001_Screenshot_from_2024-11-30_19-09-46.png)
_Ahora reiniciamos para comprobar el arranque de windows_

### Comprobación de arranque reparado

Ahora al reiniciar y arrancar desde la partición de windows 7 todo funcionará correctamente

![Sistema Windows 7 arrancado correctamente](/assets/img/posts/recuperacion_de_informacion/20241130_181206_Screenshot_from_2024-11-30_19-11-30.png)