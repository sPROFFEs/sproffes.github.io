---
title: Recopilación y análisis de datos en caliente Windows
date: 2025-01-08 11:58:38 +0000
categories: [Forense, Windows]
tags: [forense, windows, memoria, volatility, ram, dfir]
---

En este caso vamos a realizar una obtención de datos en caliente, es decir mientras el equipo sigue encendido.

Estos tipos de análisis son muy delicados ya que el objetivo se trata de recolectar todos los datos posibles de la máquina en su estado actual pero, como bien sabemos estos datos están en constante cambio si esta se encuentra encendida.

En casos así podemos encontrar discos cifrados a los que si no accedemos en caliente posiblemente sea imposible o muy complejo realizarlo en un análisis post-mortem sin la clave de cifrado.

Es por eso que es importante o bien realizar la extracción de evidencias de forma lógica con el sistema arrancado (evitando lo máximo posible la modificación de cualquier parámetro o fichero del mismo) y además extraer el estado actual de la máquina; procesos, conexiones, caché, RAM, etc.

## Herramientas

En este tipo de análisis lo mejor es utilizar herramientas externas que no necesiten instalción o modificación de ficheros dentro de la máquina ya que evitamos modificar lo máximo posible los datos de la misma.

Con esto en mente vamos a utilizar herramientas que se pueden ejecutar desde una memoria USB o similar.

## Extracción de datos automatizada

Para este tipo de extracción vamos a utilizar comandos que ofrece el propio sistema Windows aunque ciertos datos es mejor o unicamente se pueden extraer con herramientas externas.

Podemos hacer la extracción de forma manual con cada software y comando pero existen scripts automatizados que realizan esto rápidamente y guardan los datos en archivos para su posterior análisis.

En internet existen distintos scripts e incluso puedes crear el tuyo propio como en este caso.

### DFIR Forensic Script

[Github](https://github.com/sPROFFEs/DFIR-Forensic-Script)

Este script esta creado con varios comandos incluidos en el sistema así como algunos ejecutables de terceros y es capaz de extraer esos datos y almacenarlos en formato txt, json o csv.

En el enlace esta el repositorio para poder descargarlo y saber más sobre como funciona.

### Ejemplo de uso

![Descargamos el repositorio y lo guardamos en un USB](/assets/img/posts/dfirscript_volatility/20250108_124534_2025-01-08_13-45.png)
_Descargamos el repositorio y lo guardamos en un USB_

![Dentro encontramos dos scripts .bat y .ps1](/assets/img/posts/dfirscript_volatility/20250108_124718_2025-01-08_13-47.png)
_Dentro encontramos dos scripts .bat y .ps1_

Estos scripts ejecutan los mismos comandos en el sistema pero tienen un formato de salida diferente.

El más recomendado es el script powershell porque nos permite seleccionar json y csv de salida a diferente del batch que solo nos permite txt.

Para ejecutar ciertos comandos de ambos scripts hay que tener en cuenta que debemos tener privilegios elevados, además para poder ejecutar scripts en powershell debemos tener la política de ejecución de scripts configurada para que lo permita.

```powershell
Set-ExecutionPolicy Unrestricted
```

### Powershell

![Ejecución del script Powershell](/assets/img/posts/dfirscript_volatility/20250108_125403_Peek_2025-01-08_13-53.gif)

![Resultado del script Powershell](/assets/img/posts/dfirscript_volatility/Peek%202025-01-08%2023-14.gif)

### Batch

![Ejecución del script Batch](/assets/img/posts/dfirscript_volatility/20250108_125942_Peek_2025-01-08_13-59.gif)

## Volcado de memoria RAM

Otro banco de datos que podemos sacar de la máquina objetivo es la memoria RAM, para extraerla existen numerosos software aunque en este caso utilizaremos FTK imager portable.

![Proceso de volcado de memoria con FTK Imager](/assets/img/posts/dfirscript_volatility/20250108_130400_Peek_2025-01-08_14-03.gif)

### Volatility

[Github](https://github.com/volatilityfoundation/volatility)

En este caso vamos a utilizar la version para linux por lo que podemos instalarla o usar el binario standalone que se proporciona.

Utilizando el standalone tenemos los siguiente:

![Volatility standalone](/assets/img/posts/dfirscript_volatility/20250108_155718_2025-01-08_16-57.png)

Ahora vamos los siguientes datos del dump de memoria.

```plaintext
- Perfil del sistema operativo
- Listado de procesos
- Historial de comandos
- Información detallada del sistema operativo
- Ficheros cargados en memoria
- Conexiones activas
```

### Perfil del sistema operativo

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw imageinfo
```

![Perfiles de sistema operativo](/assets/img/posts/dfirscript_volatility/20250108_160415_2025-01-08_17-04.png)
_Observamos las posibles versiones del sistema operativo_

### Listado de procesos

Una vez identificado el perfil, usa pslist o pstree para listar los procesos:

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 pslist

./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 pstree
```

![Listado de procesos](/assets/img/posts/dfirscript_volatility/20250108_161611_Peek_2025-01-08_17-16.gif)

### Historial de comandos

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 cmdscan

./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 consoles
```

![Historial de comandos](/assets/img/posts/dfirscript_volatility/20250108_162758_2025-01-08_17-27.png)
_Es posible no encontrar cierta información ya que o no hay registro o no se almacena de forma predeterminada_

### Información detallada del sistema operativo

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 kdbgscan
```

![Información del sistema](/assets/img/posts/dfirscript_volatility/20250108_163038_2025-01-08_17-30.png)

### Ficheros cargados en memoria

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 modules
```

![Ficheros en memoria](/assets/img/posts/dfirscript_volatility/20250108_163203_Peek_2025-01-08_17-31.gif)

### Conexiones activas

```bash
./volatility_2.6_lin64_standalone  -f /home/kali/Desktop/practica1.raw --profile=Win7SP1x86 netscan
```

![Conexiones activas](/assets/img/posts/dfirscript_volatility/20250108_163324_Peek_2025-01-08_17-33.gif)

> **NOTA**: Si estás analizando una imagen de memoria de Linux, el procedimiento es similar, pero el perfil debe coincidir con el kernel y la distribución del sistema.