---
title: Volume Shadow Copy
date: 2025-01-04 11:58:38 +0000
categories: [Forense, Windows]
tags: [windows, forense, shadow-copy, backup]
pin: false
math: false
mermaid: false
---

Shadow Copy, también conocido como Volume Snapshot Service o VSS, es una tecnología de Microsoft Windows que permite crear copias de seguridad, ya sean manuales, automáticas o instantáneas, de archivos o volúmenes, incluso si están en uso. Funciona a través del servicio Volume Shadow Copy y requiere el sistema de archivos NTFS para generar y almacenar las instantáneas. Estas pueden realizarse tanto en volúmenes locales como externos utilizando cualquier componente de Windows compatible con esta tecnología.

Las instantáneas pueden ofrecer a los investigadores forenses acceso a archivos eliminados entre el momento en que se creó la instantánea y el inicio de la investigación, pero solo muestran versiones anteriores de los archivos. No revelan cambios realizados antes de la creación de la instantánea. 

Dado que las instantáneas se generan a nivel de bloque y no de archivo, es posible que modificaciones en archivos individuales no sean suficientes para que Windows registre esos cambios en la instantánea correspondiente.

## Añadir almacenamiento

Debido a que estamos utilizando una VM vamos a crear un segundo disco de almacenamiento para poder almacenar estas imagenes sin tener problemas de almacenamiento.

![Añadir almacenamiento](/assets/img/posts/shadow_copy/20250104_155528_2025-01-04_16-55.png)

### Habilitar el servicio SCV

![Habilitar SCV](/assets/img/posts/shadow_copy/20250104_155819_2025-01-04_16-57.png)
_Creamos el punto de restauración_

![Configuración 1](/assets/img/posts/shadow_copy/20250104_160118_2025-01-04_16-58.png)

![Configuración 2](/assets/img/posts/shadow_copy/20250104_160132_2025-01-04_16-59.png)
_Activamos proteccion, seleccionamos la capacidad completa del disco y aplicamos los cambios_

Con esto tenemos la posibilidad de ir creando puntos de restauración de forma manual pero podemos configurarlo para que se realice de forma automática.

## Programar las copias

Abrimos el programador de tareas de windows y creamos la nueva tarea para que se ejecute cuando indiquemos

![Programar copias](/assets/img/posts/shadow_copy/20250104_162003_Peek_2025-01-04_17-17.gif)

```powershell
-Command "Checkpoint-Computer -Description 'Punto de restauración automático' -RestorePointType MODIFY_SETTINGS"
```

Ahora podemos verificar que está activada además de poder ejecutarla de forma manual

![Verificar tarea](/assets/img/posts/shadow_copy/20250104_162128_Peek_2025-01-04_17-19.gif)

## Crear puntos de restauración

En este caso voy a crear varios puntos de restauración de forma manual para que podamos ver el funcionamiento de forma más dinámica con un ejemplo.

## Comprobar versiones

Se han creado tres puntos de restauración en el equipo donde se han creado documentos, instalado programas, etc...

Ahora vamos a comprobar desde el mismo sistema si existien versiones anteriores de dichos ficheros haciendo uso del explorador de archivos 

![Comprobar versiones](/assets/img/posts/shadow_copy/20250104_164616_Peek_2025-01-04_17-46.gif)
_Si como en este caso no vemos posibles versiones anteriores es posible que no sean cambios lo suficientemente sustanciales como para que windows nos indique que existen versiones anteriores_

## Crear imagen del disco con FTK

Para poder comprobar que también podemos acceder a la información de las shadow copy en un análisis post-mortem vamos a crear una imagen del disco C en el otro disco creado antes.

![Crear imagen FTK](/assets/img/posts/shadow_copy/20250104_165610_Peek_2025-01-04_17-56.gif)

![Montar imagen](/assets/img/posts/shadow_copy/20250104_171722_Peek_2025-01-04_18-17.gif)
_Montamos el disco donde hemos creado la imagen del disco C_

## Shadow Copy View

### Montar la imagen del disco

![Montar imagen disco](/assets/img/posts/shadow_copy/20250104_172649_Peek_2025-01-04_18-25.gif)

### Descarga y uso de ShadowCopyView

[shadow_copy_view](https://www.nirsoft.net/utils/shadow_copy_view.html#google_vignette)

Mediante este software podremos visualizar todos los cambios que existen entre las diferentes imagenes de restauración creadas

![ShadowCopyView uso](/assets/img/posts/shadow_copy/20250104_173045_Peek_2025-01-04_18-30.gif)
_En este caso solo nos interesan las del disco F que es la evidencia mientras que las del C son las creadas por el sistema. En un análisis esas no saldrían disponibles_

Ahora podemos comparar por ejemplo las diferencias entre los documentos del escritorio entre la imagen más antigua y la más reciente

![Imagen antigua](/assets/img/posts/shadow_copy/20250104_173511_Peek_2025-01-04_18-33.gif)
_La más antigua_

![Imagen reciente](/assets/img/posts/shadow_copy/20250104_173531_Peek_2025-01-04_18-34.gif)
_La más reciente_

## Comprobación en línea de comandos

Si queremos listar las copias creadas en el sistema podemos bien hacerlo desde la herramienta de creación dando en "Restaurar" o mediante powershell

![Comprobación GUI](/assets/img/posts/shadow_copy/20250104_174029_Peek_2025-01-04_18-40.gif)

![Comprobación PowerShell](/assets/img/posts/shadow_copy/20250104_174229_Peek_2025-01-04_18-42.gif)