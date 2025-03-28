---
title: Metadatos
date: 2023-06-07 00:00:00 +0000
categories: [Reconocimiento]
tags: [metadata, reconnaissance, osint]
---

## Recopilación semi-pasiva de información

Recolección de información sobre un objetivo determinado utilizando métodos que se asimilen al tráfico de red y comportamiento normal que suele recibir.

Dentro del alcance se encuentran actividades como: ⇒Consultas a servidores DNS ⇒Acceso a recursos internos de las aplicaciones web ⇒Análisis de metadatos de documentos

Quedan fuera de alcance todas las actividades que generen un comportamiento anómalo

La diferencia principal con las técnicas de reconocimiento anteriores que eran completamente pasivas es que no generábamos ningún tipo de tráfico o interacción directa con la infraestructura o servicio.

Las siguientes técnicas si que van a intercambiar cierto tráfico de red con el objetivo pero de forma no intrusiva sin generar comportamientos anómalos.

## Metadatos

### FOCA

Esta técnica se denomina extracción de metadatos, que se tratan de una serie de datos que describen otros datos como PDF, word, etc.

Estos metadatos describen cosas como el autor, el fecha de creación, software utilizado e incluso el equipo en el que se ha creado.

Esta información nos va a ser muy útil porque si conseguimos recaudar este tipo de datos que estén públicos con alguno de los métodos de recopilación antes vistos, podemos llegar a nombres de usuario, correos, versiones de sistemas y software que podemos usar para buscar entradas o vulnerabilidades de nuestro objetivo.

La herramienta que vamos a estar usando ahora se trata de FOCA. Funciona únicamente en sistemas operativos windows.

https://github.com/ElevenPaths/FOCA

Hay que tener en cuenta se necesitan las siguientes herramientas adicionales para su uso

![SQL Server Download](/assets/img/posts/reconocimiento/20241125_235017_84-1.png)
_https://www.microsoft.com/es-es/sql-server/sql-server-downloads_

![Selección Básica](/assets/img/posts/reconocimiento/20241125_235040_84-2.png)
_Seleccionamos la básica_

![Instalación](/assets/img/posts/reconocimiento/20241125_235055_84-3.png)

Una vez instalado tenemos que tener el cuenta el nombre de la instalación que por defecto es localhost.

Iniciamos FOCA y le indicamos la localización de la base de datos.

![Localización Base de Datos](/assets/img/posts/reconocimiento/20241125_235123_84-4.png)

Una vez abierto este apartado será el más interesante ya que es el que gestiona los metadatos de los ficheros que queramos.

![Gestión de Metadatos](/assets/img/posts/reconocimiento/20241125_235143_84-5.png)

Una vez tengamos el archivo que queramos analizar pulsamos click derecho en el apartado anterior y añadimos fichero.

![Añadir Fichero](/assets/img/posts/reconocimiento/20241125_235200_84-6.png)

![Selección Fichero](/assets/img/posts/reconocimiento/20241125_235233_84-7.png)

![Detalles Fichero](/assets/img/posts/reconocimiento/20241125_235240_84-8.png)

![Análisis Fichero](/assets/img/posts/reconocimiento/20241125_235256_84-9.png)

Para evitar tener que ir archivo por archivo foca nos proporciona una herramienta de proyectos.

![Herramienta Proyectos](/assets/img/posts/reconocimiento/20241125_235312_84-10.png)

![Indicar Dominio](/assets/img/posts/reconocimiento/20241125_235334_84-11.png)
_Indicamos el dominio o subdominios_

![Configurar Búsqueda](/assets/img/posts/reconocimiento/20241125_235352_84-12.png)
_Y le indicamos que tipo de ficheros y qué motores de busqueda quieres usar_

![Resultados Búsqueda](/assets/img/posts/reconocimiento/20241125_235407_84-13.png)

Seleccionamos los que nos interesen y descargamos los documentos a la máquina

![Descarga Documentos](/assets/img/posts/reconocimiento/20241125_235438_84-14.png)

![Proceso Descarga](/assets/img/posts/reconocimiento/20241125_235502_84-15.png)

![Finalización Descarga](/assets/img/posts/reconocimiento/20241125_235513_84-16.png)

## Otras herramientas

### Metagofil

Es una herramienta algo más antigua y menos completa que FOCA.

```bash
sudo apt install metagoofil
```

![Metagofil Instalación](/assets/img/posts/reconocimiento/20241125_235637_85-1.png)

```bash
metagoofil -d dominio -l 10 -t pdf,doc,txt -o Desktop/ 
```

![Metagofil Ejecución](/assets/img/posts/reconocimiento/20241125_235650_85-2.png)

### MetaShield

Su función principal es eliminar posibles metadatos sensibles de documentos que se vayan a compartir. 

https://metashieldclean-up.elevenpaths.com/

### ExifTool

```bash
sudo apt install exiftool
```

```bash
exiftool -f *.pdf | egrep -i "Author|Creator|Email|Producer|Templeate" | sort -u
```

Recorre todos los archivos pdf que tengamos y busca una serie de campos para devolver el resultado.