---
title: Volatility 2 & 3
date: 2025-01-14 11:58:38 +0000
categories: [Forense, Memoria RAM]
tags: [forense, volatility, ram, memoria, windows]
---

## Concepto

En esta sección vamos a realizar un ejemplo de uso medio/avanzado de la herramienta Volatility 2 y 3.

En el proceso vamos a ir obteniendo diferentes datos sobre el sistema a partir de un volcado de memoria ram.

## Instalación

### Volatility 2

[Github oficial de volatility 2](https://github.com/volatilityfoundation/volatility)

### Volatility 3

[Github oficial de volatility 3](https://github.com/volatilityfoundation/volatility3)

```bash
pip install volatility3
```

## Recursos

[Volcado de memoria utilizado](https://drive.google.com/file/d/1qfU9Ixqx1YqNgZFWOz548lbvK4A80md-/view?usp=sharing)

En el link anterior encontramos el volcado de memoria utilizado en esta sección.

## Perfil del sistema operativo

```bash
-Vol3

vol -f "/path/to/file" windows.info

-Vol2

vol.py -f "/path/to/file" imageinfo
vol.py -f "/path/to/file" kdbgscan
```

### Vol3

![Identifica el sistema como 7601.17514.amd64fre.win7sp1_rtm.](/assets/img/posts/volatility_2_3/20250114_172936_2025-01-14_18-29.png)
_Identifica el sistema como 7601.17514.amd64fre.win7sp1_rtm._

### Vol2

![Aqui de igual forma indica windows 7 sp1](/assets/img/posts/volatility_2_3/20250114_173006_2025-01-14_18-29_1.png)
_Aqui de igual forma indica windows 7 sp1_

## Procesos en ejecución

```bash
-Vol3

vol.py -f "/path/to/file" windows.pslist
vol.py -f "/path/to/file" windows.psscan
vol.py -f "/path/to/file" windows.pstree

-Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> pslist
vol.py -f "/path/to/file" ‑‑profile <profile> psscan
vol.py -f "/path/to/file" ‑‑profile <profile> pstree
vol.py -f "/path/to/file" ‑‑profile <profile> psxview
```

### Vol3

![Procesos en ejecución Vol3](/assets/img/posts/volatility_2_3/20250114_173530_2025-01-14_18-35.png)

### Vol2

![Procesos en ejecución Vol2](/assets/img/posts/volatility_2_3/20250114_173737_2025-01-14_18-37.png)

Total de 42 procesos

## Árbol de procesos

```bash
-Vol3

vol.py -f "/path/to/file" windows.pstree

-Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> pstree
```

### Vol3

![Vol3 árbol de procesos](/assets/img/posts/volatility_2_3/20250114_174233_2025-01-14_18-42.png)
_(Como vemos no parsea demasiado bien el contenido)_

### Vol2

![Vol2 árbol de procesos](/assets/img/posts/volatility_2_3/20250114_174111_2025-01-14_18-41.png)
_Por ejemplo podemos ver con más claridad el PPID de cada uno de los procesos._

## Registro de Windows

### Lista de hives

```bash
-Vol3

vol.py -f "/path/to/file" windows.registry.hivescan
vol.py -f "/path/to/file" windows.registry.hivelist

-Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> hivescan
vol.py -f "/path/to/file" ‑‑profile <profile> hivelist
```

### Vol3

![Hives Vol3](/assets/img/posts/volatility_2_3/20250114_174926_2025-01-14_18-49.png)

### Vol2

![Hives Vol2](/assets/img/posts/volatility_2_3/20250114_174824_2025-01-14_18-48.png)

En ambos coincide que existen 12 hives en el registro

### Claves de registro

```bash
-Vol3

vol.py -f "/path/to/file" windows.registry.printkey
vol.py -f "/path/to/file" windows.registry.printkey ‑‑key "Software\Microsoft\Windows\CurrentVersion"

-Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> printkey
vol.py -f "/path/to/file" ‑‑profile <profile> printkey -K "Software\Microsoft\Windows\CurrentVersion"
```

### Vol3

![Claves Vol3](/assets/img/posts/volatility_2_3/20250114_175955_2025-01-14_18-59.png)
_Por ejemplo vemos que en SYSTEM existen 9 claves incluyendo las volátiles_

### Vol2

![Claves Vol2](/assets/img/posts/volatility_2_3/20250114_182452_2025-01-14_19-08.png)

### Claves especificas

```bash
-Vol3

vol.py -f "/path/to/file" windows.registry.printkey ‑‑key"Software\Microsoft\Windows\CurrentVersion"

- Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> printkey -K "Software\Microsoft\Windows\CurrentVersion"
```

### Vol3

![Claves específicas Vol3](/assets/img/posts/volatility_2_3/20250114_182705_2025-01-14_19-26.png)

### Vol2

![Claves específicas Vol2](/assets/img/posts/volatility_2_3/20250114_182831_2025-01-14_19-28.png)

## Hash de contraseñas

```bash
-Vol3

vol.py -f <ruta_a_la_imagen> windows.hashdump

- Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> hashdump
```

### Vol3

![Hash Vol3](/assets/img/posts/volatility_2_3/20250114_183705_2025-01-14_19-36.png)

### Vol2

![Hash Vol2](/assets/img/posts/volatility_2_3/20250114_183748_2025-01-14_19-37.png)

![Hash cracked](/assets/img/posts/volatility_2_3/20250114_183849_2025-01-14_19-38.png)
_En este caso la contraseña es sencilla_

## Conexiones externas

```bash
-Vol3

vol.py -f <ruta_a_la_imagen> windows.netstat

- Vol2

vol.py  -f <ruta_a_la_imagen> --profile=<perfil_de_sistema> netscan
```

### Vol3

![Conexiones Vol3](/assets/img/posts/volatility_2_3/20250114_184327_2025-01-14_19-43.png)

### Vol2

![Conexiones Vol2](/assets/img/posts/volatility_2_3/20250114_184547_2025-01-14_19-45.png)
_En este caso volatility 2 es más capaz_

## Estructuras FILE_OBJECT

```bash
-Vol3

vol.py -f <ruta_a_la_imagen> windows.filescan

- Vol2

vol.py  -f <ruta_a_la_imagen> --profile=<perfil_de_sistema> filescan
```

### Vol3

![Estructuras Vol3](/assets/img/posts/volatility_2_3/20250114_185140_2025-01-14_19-51.png)
_Extrae 3420 resultados_

### Vol2

![Estructuras Vol2](/assets/img/posts/volatility_2_3/20250114_184947_2025-01-14_19-49.png)
_Extrae 3423 resultados_

## Extracción de ficheros

```bash
-Vol3

vol.py -f [ImageName] -o "dump" windows.dumpfile --pid 1328 --virtaddr 0xbf0f6abe9740

- Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> dumpfiles ‑‑dump-dir="/path/to/dir" -p <PID>
```

### Localizar un fichero

![Localizar fichero](/assets/img/posts/volatility_2_3/20250114_192053_2025-01-14_20-20.png)
_Localizamos el proceso_

### Vol3

![Extracción Vol3](/assets/img/posts/volatility_2_3/20250114_192211_2025-01-14_20-22.png)

### Vol2

![Extracción Vol2](/assets/img/posts/volatility_2_3/20250114_192739_2025-01-14_20-27.png)

## Rutas de ficheros

```bash
-Vol3

vol.py -f "/path/to/file" windows.filescan

- Vol2

vol.py -f "/path/to/file" ‑‑profile <profile> filescan
```

### Vol3

![Rutas Vol3](/assets/img/posts/volatility_2_3/20250114_193320_2025-01-14_20-33.png)

### Vol2

![Rutas Vol2](/assets/img/posts/volatility_2_3/20250114_193208_2025-01-14_20-31.png)

## Tabla MFT

```bash
-Vol3

vol.py -f <ruta_a_la_imagen> windows.mftscan.MFTScan

- Vol2

vol.py -f <ruta_a_la_imagen> --profile=<perfil_de_sistema> mftparser
```

### Vol3

![MFT Vol3](/assets/img/posts/volatility_2_3/20250114_195210_2025-01-14_20-52.png)

### Vol2

![MFT Vol2](/assets/img/posts/volatility_2_3/20250114_193922_2025-01-14_20-38.png)

Aqui podemos ver las fechas de acceso, modificacion, etc de los archivos de los que tengamos interés

## URLs en memoria

```bash
-Vol3

vol.py -f "/path/to/file" windows.vadyarascan --yara-rules "https://" | grep -A 5 -B 5 "Process firefox"

- Vol2

vol.py -f <imagen_memoria> --profile=<perfil> yarascan -Y "https://" | grep -A 5 -B 5 "Process firefox"
```

### Vol2

![URLs en memoria](/assets/img/posts/volatility_2_3/20250114_220227_2025-01-14_23-02.png)
_Podemos ver diferentes URL almacenadas en la memoria_

## Fechas de ejecución

```bash
-Vol3

vol.py -f <imagen_memoria> windows.registry.printkey --key "Software\\Mozilla\\Firefox"

- Vol2

vol.py -f <imagen_memoria> --profile=<perfil> printkey -K "Software\\Mozilla\\Firefox"
```

### Vol3

![Fechas Vol3](/assets/img/posts/volatility_2_3/20250114_222508_2025-01-14_23-25.png)

### Vol2

![Fechas Vol2](/assets/img/posts/volatility_2_3/20250114_222136_2025-01-14_23-19.png)

Mas o menos podemos deducir las ultimas fechas en función de las ultimas modificaciones de las llaves en el registro de windows

### Fechas de navegación a URLs

Si necesitamos visualizar la fecha y hora en la que se visualizó una URL podemos acceder a la base de datos sqlite que genera el navegador.

En este caso firefox genera varias bases de datos en las que almacena cookies, bookmarks, historiales, etc por lo que deberían estar en memoria ya que el proceso está en ejecución.

![Proceso Firefox](/assets/img/posts/volatility_2_3/20250116_214047_2025-01-16_22-40.png)
_Localizamos el proceso principal del navegador_

![Volcado Firefox](/assets/img/posts/volatility_2_3/20250116_214139_2025-01-16_22-41.png)
_Volcamos toda los datos del proceso. En este caso se ha usado volatility 2 pero es indiferente_

Podemos verificar que en el volcado podemos encontrar estas bases de datos gestionadas por el navegador

![Bases de datos](/assets/img/posts/volatility_2_3/20250116_214549_2025-01-16_22-44.png)

Ahora que sabemos que los documentos están en uso por el proceso vamos a volcar toda los datos en memoria cargados pero de forma individual

![Volcado individual](/assets/img/posts/volatility_2_3/20250116_214711_2025-01-16_22-47.png)
_Esto nos va a generar muchos archivos que tendremos que filtrar ahora_

Por ejemplo podemos filtrar los archivos por tipo ya que el nombre que le asigna volatility es la dirección de memoria que ocupa y el proceso del que viene.

En este caso simplemente con un explorador de archivos organizamos por tipo de fichero y nos quedamos los sqlite.

Vamos a tener que comprobar el contenido a mano de cada uno pero lo más normal es que el fichero sqlite más grande sea el que contiene el historial, bookmarks y otros datos.

![Renombrar SQLite](/assets/img/posts/volatility_2_3/20250116_215021_2025-01-16_22-48.png)
_Le podemos cambiar el nombre para que sea más fácil de referenciar_

Ahora que tenemos el documento podemos abrir la base de datos con sqlite y acceder a los datos

![SQLite datos](/assets/img/posts/volatility_2_3/20250116_215208_2025-01-16_22-52.png)
_En este caso podemos la URL que vimos anteriormente mediante YARA_

La fecha de visita es el número en la tercera columna pero no es visible. Esto es por cómo son almacenadas las fechas en sqlite pero es un cálculo sencillo.

![Fecha SQLite](/assets/img/posts/volatility_2_3/20250116_215448_2025-01-16_22-54.png)
_2020-06-12 14:18:23_

## Bonus

### Contexto

En esta sección bonus vamos a realizar un analisis más profundo sobre un proceso en concreto.

El objetivo es sencillo; anteriormente conseguimos encontrar un fichero 7z en memoria, el problema es que viene conmprimido con contraseña por lo que tenenmos dos opciones.

1- Intentar crackear el fichero
2- Buscar en el dump de memoria si la contraseña puede estar en algún proceso abierto

Podemos proceder de la siguiente forma:

Mientras dejamos algun software de crackeo intentar descifrar el archivo vamos a indagar en el dump.

En este apartado vamos a estar utilizando únicamente volatility 3.

### Listar procesos

```bash
vol.py -f <imagen_memoria> windows.pslist
```

![Procesos de interés](/assets/img/posts/volatility_2_3/20250115_084259_2025-01-15_09-42.png)
_Vemos los dos procesos que nos pueden interesar, de uno ya tenemos el 7z y ahora podemos ver que hay contenido en el proceso del notepad_

Para este proceso existen numerosos comandos que nos pueden dar más información sobre el contenido en memoria del proceso notepad.exe

```bash
vol -f dump.raw windows.memmap --pid <PID_notepad> --dump

vol -f dump.raw windows.vadinfo --pid <PID_notepad>
```

Estos comandos nos proporcionarán bastante información e incluso es posible que el contenido del fichero que estuviese editando el usuario en el momento de la captura pero analizar el dump puede ser tedioso y alargarse demasiado, es por eso que existen plugins ya hechos por la comunidad para ciertas tareas y es lo que vamos a estar utilizando aquí.

### Enlace al plugin

[Github](https://github.com/spitfirerxf/vol3-plugins/blob/main/notepad.py)

Este plugin lo debemos mover a la ruta donde tengamos localizado nuestro volatility.

En este caso como lo instalamos mediante pip y en linux la ruta debería ser:

```bash
/home/kali/.local/lib/python3.12/site-packages/volatility3/framework/plugins/windows/
```

Ahora si podemos ejecutar el plugin de la siguiente forma

```bash
vol.py -f dump.raw windows.notepad
```

![Plugin notepad](/assets/img/posts/volatility_2_3/20250115_085006_2025-01-15_09-49.png)

Aunque el contenido es algo lioso quizás la mejor manera de proceder es identificar la zona que el usuario podría estar viendo en pantalla, es decir la interfaz de usuario.

Cuando identifiquemos el posible texto que necesitamos podemos proceder a intentar descifrar el fichero obtenido anteriormente.

![Extracción archivos](/assets/img/posts/volatility_2_3/20250115_085402_Peek_2025-01-15_09-53.gif)
_En este caso vamos 4 ficheros porque anteriormente realizamos la extración con volatility 2 y 3_