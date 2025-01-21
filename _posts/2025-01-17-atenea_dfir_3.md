---
title: Reto DFIR 3 - Atenea CCN
date: 2025-01-17 18:16:41 +0100
categories: [Labs & CTF, Walkthrough, DFIR]
tags: [dfir, forensics, malware analysis, memory analysis, volatility, cobalt strike]
---

## Recursos

### Volcado de memoria utilizado

[Google Drive](https://drive.google.com/file/d/1jUG9Wj4sHuZUpwvqCVLOlbYcwsbxt67I/view?usp=sharing)

## Análisis de procesos

![Árbol de procesos](/assets/img/posts/atenea_dfir_3/20250117_181641_2025-01-17_19-16.png)
_./vol2 -f Hell.img --profile=Win7SP1x64 pstree_

Hay una cadena de anidamiento sospechosa de cmd.exe -> powershell.exe que se repite varias veces:
cmd.exe (2680)
 └─ powershell.exe (700)
    └─ cmd.exe (1876)
       └─ powershell.exe (2532)
          └─ cmd.exe (2236)
             └─ powershell.exe (2696)
                └─ cmd.exe (2632)

Procesos sospechosos relacionados con inyección:

- inject.exe (PID 2648) con un proceso hijo inject.tmp (PID 2812)
- La presencia de archivos .tmp es sospechosa en este contexto

MSI_v1.0.3.exe (PID 880) lo tenemos en cuenta para el siguiente punto.

Procesos con nombres sospechosos:

- PZ.exe y PZshl.exe
- NM34_x86.exe que inicia wscript.exe
- diec.exe

Varios procesos que podrían estar relacionados con la instalación de malware:

- tsetup.exe con su archivo temporal tsetup.tmp
- Múltiples instancias de notepad.exe que podrían estar siendo usadas para inyección de código

## Análisis de conexiones

![Análisis de conexiones de red](/assets/img/posts/atenea_dfir_3/20250117_183529_2025-01-17_19-34.png)
_./vol2 -f Hell.img --profile=Win7SP1x64 netscan_

MSI_v1.0.3.exe (PID 880) muestra un comportamiento inusual:

- Tiene múltiples conexiones UDP en puerto 0
- Realiza varios intentos de conexión al puerto 80 y 8080 de 10.0.0.200
- Este patrón podría indicar actividad de malware o intentos de comunicación con un servidor de comando y control

Hay dos conexiones TCP CLOSED con propietarios sospechosos:

- PID 424 conectando a 152.18.134.4 (sin nombre de proceso)
- PID 2 conectando a 56.43.118.4 con un nombre de proceso corrupto "??y????"

Hay una conexión CLOSED desde el PID 197507 (identificado como "f?") al puerto 8080, lo cual es sospechoso por:

- El PID es inusualmente alto
- El nombre del proceso está corrupto/incompleto
- El puerto 8080 es comúnmente usado para proxies y servidores web alternativos

Hay un proceso con PID 88224 (identificado como "L?") escuchando en el puerto UDP 60092

## Análisis de autoruns

![Análisis de autoruns](/assets/img/posts/atenea_dfir_3/20250117_184222_2025-01-17_19-42.png)
_vol -f Hell.img windows.autorun_

Hay dos instancias de mctadmin.exe configuradas para ejecutarse en RunOnce para diferentes perfiles de servicio (LocalService y NetworkService). Esto podría ser sospechoso porque:

- Está configurado para ejecutarse una sola vez
- Afecta a múltiples perfiles de servicio
- No es un componente estándar de Windows

La presencia de múltiples entradas de registro en diferentes hives (SOFTWARE, NTUSER.DAT) que ejecutan programas al inicio podría indicar persistencia de software potencialmente malicioso.

## Malfind

```bash
./vol2 -f Hell.img --profile=Win7SP1x64 malfind -D ./malfind/ 

foremost *

clamscan *
```

![Análisis con malfind](/assets/img/posts/atenea_dfir_3/20250117_185547_2025-01-17_19-55.png)

Hemos exportado los procesos que el plugin malfind encuentra para posteriormente analizarlos con el antivirus ClamAV que es opensource y gratuito.

Encontramos dos archivos .dll que parecen estar infectados con Cobalt Strike es una herramienta de post-explotación comercial comúnmente usada en ataques dirigidos.

Si en vez de volcar los datos simplemente los listamos veremos que entre los procesos infectados se encuentra en efecto el proceso MSI_v1.0.3.exe

Si lo extraemos y lo analizamos veremos el mismo tipo de infección

![Análisis adicional](/assets/img/posts/atenea_dfir_3/20250117_192049_2025-01-17_20-20.png)

En las conexiones de red vimos que MSI_v1.0.3.exe intentaba conectarse a 10.0.0.200 en los puertos 80 y 8080
Estos probablemente son los intentos de conexión al servidor de comando y control

## Análisis de conexiones en los procesos infectados

Mediante malfind encontramos varios procesos infectados entre los que se encuentran varios svchosts.

Tras identificar el PID de cada uno hemos llegado a la conclusión de que uno de ellos fue la infección inicial, ya que como veremos ahora realiza varias conexiones para descargar software malicioso.

![Análisis de URLs](/assets/img/posts/atenea_dfir_3/20250117_192513_2025-01-17_20-24.png)
_./vol2 -f Hell.img --profile=Win7SP1x64 yarascan -Y "http" | grep -A 17 "Owner: Process svchost.exe"_

Encontramos en la memoria del proceso svchost.exe (PID 744) lo que parece ser el origen real de la infección:

URLs de descarga del malware:

- http://update.qyule.com/setup.exe
- http://218.204.253.145/setup.exe

Hay referencias a "Zlob.ANA" en la memoria, lo que sugiere que podría haber una infección previa de un troyano Zlob

El malware parece mostrar un mensaje de alerta: "the computer has been infected!!"

Hay una URL sospechosa adicional: "myfirstgaysex.com" que probablemente sea parte del vector de infección inicial

El User-Agent que se está usando es "mozilla/4.0 (compatible; msie 6." lo que sugiere que está intentando parecer Internet Explorer 6

Por lo tanto, parece que:

- La máquina fue inicialmente infectada por una variante del troyano Zlob

- Este troyano probablemente descargó el Cobalt Strike (MSI_v1.0.3.exe) como una infección secundaria

- Aunque el Cobalt Strike está intentando conectarse a 10.0.0.200, la infección inicial vino de estos dominios maliciosos

## Analisis de CMD

![Análisis de consolas](/assets/img/posts/atenea_dfir_3/20250117_194218_2025-01-17_20-42.png)
_./vol2 -f Hell.img --profile=Win7SP1x64 consoles_

Se confirma la existencia de un archivo "SHellb0t.zip" que fue descomprimido en el directorio temporal C:\Users\Baphomet\AppData\Local\Temp\Temp1_SHellb0t.zip\diec.exe

El diec.exe que vimos anteriormente en el árbol de procesos (PID 2208) proviene de este archivo zip, lo que sugiere que:

- No es el DIE-Engine legítimo, sino malware que se hace pasar por él
- El nombre "SHellb0t" sugiere que es algún tipo de bot o backdoor

Vemos de nuevo la cadena de procesos cmd.exe/powershell.exe que identificamos antes, pero ahora con más detalles:

cmd.exe (2680)
 └─ powershell.exe (700)
    └─ cmd.exe (1876)
       └─ powershell.exe (2532)
          └─ cmd.exe (2236)
             └─ powershell.exe (2696)
                └─ cmd.exe (2632)

## Análisis con Yara rules

![Análisis con Yara](/assets/img/posts/atenea_dfir_3/20250117_195429_2025-01-17_20-53.png)

Insta11Strings

    Se encontraron múltiples coincidencias en las siguientes direcciones de memoria:
        0xf8a003910961
        0xf8a0039155b9
        0xf8a00391a9e9
        0xf8a003922631
    Cada coincidencia incluye un valor hexadecimal (ejemplo: 42 31 32 41 45...) que parece ser un identificador o un conjunto de datos codificados.

Ponmocup

    Dirección de memoria: 0xfa8003ff3000
    Bytes coincidentes: 4d 5a 90 00 03 00 00 00 04 00 08 00...
    Regla relacionada: Coincide con Ponmocup, un malware conocido por actividades de robo de 
información.

## Identificación del beacon

Ahora que sabemos todo esto e investigamos el malware cobalt strike podemos intentar identificar el beacon o el punto de conexión princiapal con el servidor C&2.

Cuando el malware esta en ejecución este establece una conexión en el equipo de tipo beacon, esto signfica que por ejemplo al igual que un punto de acceso wifi, este está continuamente mandando paquetes (esta vez dirigidos al C&2) para indicarle que está en línea y activo para recibir comandos.

Los "beacons" (balizas) son el componente principal de comunicación que:

- Establece un canal de comunicación encriptado entre el sistema comprometido y el servidor de comando y control
- Puede operar sobre HTTP, HTTPS o DNS para evitar detección
- Permite ejecutar comandos remotamente en el sistema infectado
- Puede permanecer inactivo por períodos configurables para dificultar su detección

### Herramientas para identificar los paquetes beacon

[Enlace github](https://github.com/XD-bot/ToolsFromDidierStevensSuite/blob/master/1768.py)

Este proceso de identificación se puede realizar de forma manual o tras una pequeña investigación podemos encontrar scripts o herramientas que nos ayudan a identificar los paquetes beacon.

#### Uso de la herramienta

```bash
python3 1768.py hell.img
```

![Python](/assets/img/posts/atenea_dfir_3/2025-01-21_19-48.png)

## Conclusión

Tomando en cuenta todo lo analizado podemos intentar deducir que se trata de una infección por inyección de dll.

Todo lo encontrado en los autoruns, lo exportado de los procesos infectados y la interacción con procesos a nivel de kernel indican que puede ser un rootkit de control remoto e incluso pertenecer a una antigua y conocida botnet.

El hecho de encontrar múltiples DLLs infectadas sugiere que el malware está usando la técnica de "DLL injection", que es una técnica común usada por Cobalt Strike para:

- Mantener persistencia
- Evadir detección
- Ejecutar código malicioso en el contexto de otros procesos legítimos

Esto encaja con el patrón completo que hemos visto:

- La infección inicial probablemente vino por las URLs que encontramos en svchost.exe
- El malware se propagó usando inyección de DLLs
- MSI_v1.0.3.exe parece ser el payload principal de Cobalt Strike
- La cadena de cmd/powershell probablemente fue usada para realizar la inyección de las DLLs

![Proceso de escaneo](/assets/img/posts/atenea_dfir_3/20250117_201123_Peek_2025-01-17_21-08.gif)

Posiblemente parte de los procesos infectados hacen uso o provinen de otros procesos que hacen uso de estas dll.