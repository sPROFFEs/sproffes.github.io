---
title: Guía de Procedimiento - Adquisición de Evidencias (Cold Clone)
date: 2024-10-10 11:58:38 +0000
categories: [Forense, Discos]
tags: [forense, clonado, evidencias]
---

## Descripción General

### Paso 1: Configuración de la Máquina Virtual

Descarga el archivo proporcionado y configura el segundo disco en el programa de virtualización.

#### Instrucciones Detalladas

Añade el disco descargado con la opción "add" y arranca la máquina con un live ISO de Kali Linux. Selecciona la opción "forensic" para evitar contaminación del disco.

![Configuración inicial del disco](/assets/img/posts/clonado_de_disco/disco1.png)
_Configuración inicial del disco_

![Selección de disco virtual](/assets/img/posts/clonado_de_disco/disco2.png)
_Selección de disco virtual_

![Configuración completada](/assets/img/posts/clonado_de_disco/disco3.png)
_Configuración completada_

![Arranque en modo forense](/assets/img/posts/clonado_de_disco/arranque.png)
_Arranque en modo forense_

### Paso 2: Verificación de Discos

En Kali Linux, usa el siguiente comando para listar los discos disponibles:

```bash
fdisk -l
```

#### Instrucciones Detalladas

Verifica que puedes ver el disco de evidencia y el disco contenedor. Asegúrate de que hay espacio suficiente en el disco contenedor.

![Resultado del comando fdisk -l](/assets/img/posts/clonado_de_disco/fdisk.png)
_Resultado del comando fdisk -l_

### Paso 3: Cálculo del Hash de la Evidencia

Antes de empezar con el clonado o la creación de una imagen, calcula el hash del disco de evidencia:

```bash
sha512sum /dev/sdX    # Reemplaza /dev/sdX con el dispositivo adecuado
```

![Hash calculado de la evidencia original](/assets/img/posts/clonado_de_disco/hashevidencia.png)
_Hash calculado de la evidencia original_

### Paso 4: Clonado del Disco

Ejecuta el comando de clonado:

```bash
dd if=/dev/sdX of=/dev/sdY bs=4M
```

Verifica el hash del disco clonado:

```bash
sha512sum /dev/sdY
```

![Proceso de clonado en ejecución](/assets/img/posts/clonado_de_disco/clonado.png)
_Proceso de clonado en ejecución_

![Verificación del hash del clonado](/assets/img/posts/clonado_de_disco/hashclonado.png)
_Verificación del hash del clonado_

### Paso 5: Creación de Imagen del Disco

Crea una imagen del disco de evidencia:

```bash
dd if=/dev/sdX of=/ruta/a/imagen.img bs=4M
```

Verifica el hash de la imagen:

```bash
sha512sum /ruta/a/imagen.img
```

![Inicio del proceso de imagen](/assets/img/posts/clonado_de_disco/imagen1.png)
_Inicio del proceso de imagen_

![Progreso de la imagen](/assets/img/posts/clonado_de_disco/imagen2.png)
_Progreso de la imagen_

![Verificación de la imagen](/assets/img/posts/clonado_de_disco/imagen3.png)
_Verificación de la imagen_

![Comprobación final](/assets/img/posts/clonado_de_disco/imagen4.png)
_Comprobación final_

![Proceso completado](/assets/img/posts/clonado_de_disco/imagen5.png)
_Proceso completado_