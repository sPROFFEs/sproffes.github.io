---
title: Recopilación pasiva
date: 2024-01-19
categories: [Reconocimiento]
tags: [passive-recon, google-dorks, shodan, censys, whois, maltego]
---

## Google Hacking/Dorking

Se usarán motores de búsqueda como Google, Bing, DuckGo, etc mediante el uso de una serie de comandos y operaciones booleanas para encontrar información específica que los motores indexan pero no es tan pública.

### Comandos específicos para google
https://gist.github.com/zachbrowne/489762a6852abb24f9e3

https://www.exploit-db.com/google-hacking-database

Restringir la búsqueda unicamente al sitio web indicado, nada de webs donde se le haga referencia:

```
site:website.com
```

Apuntar a un tipo de archivo concreto o contenido:

```
site:website.com filetype:pdf
```

### Google dorks
Tipo de archivo

```
filetype:sql "MySQL dump"
filetype:sql "MySQL dump" (pass|password|passwd|pwd)
```

Buscar parámetros en la url

```
inurl:index.php?id=
```

Comandos principales que podemos utilizar con Google. Hay que tener en cuenta que todos ellos deben ir seguidos (sin espacios) de la consulta que quiere realizarse:

```
define:término
```

Se muestran definiciones procedentes de páginas web para el término buscado.

```
filetype:término
```

Las búsquedas se restringen a páginas cuyos nombres acaben en el término especificado. Sobretodo se utiliza para determinar la extensión de los ficheros requeridos. Nota: el comando ext:término se usa de manera equivalente.

```
site:sitio/dominio
```

Los resultados se restringen a los contenidos en el sitio o dominio especificado. Muy útil para realizar búsquedas en sitios que no tienen buscadores internos propios.

```
link:url
```

Muestra páginas que apuntan a la definida por dicha url. La cantidad (y calidad) de los enlaces a una página determina su relevancia para los buscadores. Nota: sólo presenta aquellas páginas con pagerank 5 o más.

```
cache:url
```

Se mostrará la versión de la página definida por url que Google tiene en su memoria, es decir, la copia que hizo el robot de Google la última vez que pasó por dicha página.

```
info:url
```

Google presentará información sobre la página web que corresponde con la url.

```
related:url
```

Google mostrará páginas similares a la que especifica la url. Nota: Es difícil entender que tipo de relación tiene en cuenta Google para mostrar dichas páginas. Muchas veces carece de utilidad.

```
allinanchor:términos
```

Google restringe las búsquedas a aquellas páginas apuntadas por enlaces donde el texto contiene los términos buscados.

```
inanchor:término
```

Las búsquedas se restringen a aquellas apuntadas por enlaces donde el texto contiene el término especificado. A diferencia de allinanchor se puede combinar con la búsqueda habitual.

```
allintext:términos
```

Se restringen las búsquedas a los resultados que contienen los términos en el texto de la página.

```
intext:término
```

Restringe los resultados a aquellos textos que contienen término en el texto. A diferencia de allintext se puede combinar con la búsqueda habitual de términos.

```
allinurl:términos
```

Sólo se presentan los resultados que contienen los términos buscados en la url.

```
inurl:término
```

Los resultados se restringen a aquellos que contienen término en la url. A diferencia de allinurl se puede combinar con la búsqueda habitual de términos.

```
allintitle:términos
```

Restringe los resultados a aquellos que contienen los términos en el título.

```
intitle:término
```

Restringe los resultados a aquellos documentos que contienen término en el título. A diferencia de allintitle se puede combinar con la búsqueda habitual de términos.

### Operadores Booleanos Google Hacking
Google hace uso de los operadores booleanos para realizar búsquedas combinadas de varios términos. Esos operadores son una serie de símbolos que Google reconoce y modifican la búsqueda realizada:

```
" " - Busca las palabras exactas.

- - Excluye una palabra de la búsqueda. (Ej: gmail -hotmail, busca páginas en las que aparezca la palabra gmail y no aparezca la palabra hotmail)

OR (|) - Busca páginas que contengan un término u otro.

+ - Permite incluir palabras que Google por defecto no tiene en cuenta al ser muy comunes (en español: "de", "el", "la".....). También se usa para que Google distinga acentos, diéresis y la letra ñ, que normalmente son elementos que no distingue.

* - Comodín. Utilizado para sustituir una palabra. Suele combinarse con el operador de literalidad (" ").
```

## Shodan

Surgió en 2009 y en este caso no indexa las palabras como hace el motor de google u otros motores de búsqueda sino que recorre todo internet buscando información sobre el dominio que busquemos o las ip que indiquemos.

Esta herramienta consigue los datos en gran parte de los banners de los dispositivos que se encuentran conectados a internet, analiza sus puertos y servicios que posteriormente shodan indexa esta información.

Es importante tener en cuenta que en este momento no buscamos webs ni archivos indexados sino información en los banners que generan los servicios al intentar comunicarte con ellos. Shodan cuenta con algunos comandos propios.

### Filtros más relevantes para el uso de Shodan

```
after: Only show results after the given date (dd/mm/yyyy) string
asn: Autonomous system number string
before: Only show results before the given date (dd/mm/yyyy) string
category: Available categories: ics, malwarestring
city: Name of the city string
country: 2-letter country code string
geo: Accepts between 2 and 4 parameters. If 2 parameters: latitude, longitude. If 3 parameters: latitude, longitude, range. If 4 parameters: top left latitude, top left longitude, bottom right latitude, bottom right longitude.
hash: Hash of the data property integer
has_ipv6: True/False boolean
has_screenshot: True/False boolean
server: Devices or servers that contain a specific server header flag string
hostname: Full host name for the device string
ip: Alias for net filter string
isp: ISP managing the netblock string
net: Network range in CIDR notation (ex.199.4.1.0/24) string
org: Organization assigned the netblock string
os: Operating system string
port: Port number for the service integer
postal: Postal code (US-only) string
product: Name of the software/product providing the banner string
region: Name of the region/state string
state: Alias for region string
version: Version for the product string
vuln: CVE ID for a vulnerability string
```

### Ejemplo de comandos shodan en una búsqueda

```
ftp anonymous login ok country:"US" port:"21"
```

### Repositorio
https://github.com/jakejarvis/awesome-shodan-queries

## Censys

Herramienta similar a Shodan. La diferencia es la manera en la que indexa los datos. Censys escanea diariamente internet con Zmap y Zgrab lo que permite realizar una indexación de diferente manera y normalmente más actualizada.

https://search.censys.io/

## Whois

Las organizaciones y usuarios dan de alta todos los años diferentes nombres de dominio para servir los servicios.

Cuando se da de alta un dominio se deben dar datos personales que se almacenan en una base de datos que se denominan "WhoIS"

No es un base de datos centralizada, son varias y son gestionadas por las entidades que registran los nombres de dominios que se adquieren.

Para realizar estas consultas se pueden usar varias herramientas.

```bash
whois -h
```

A día de hoy estas bases de datos no son de mucha utilidad porque los datos pueden ser privados y los que se muestran no son los correctos.

## Archive

Cuando se encuentra información sensible publicada en internet y se reporta la información, lo más común es que la empresa retire los datos aunque no siempre cambian las credenciales por lo que si se puede acceder al histórico de, por ejemplo github, podremos volver a tener esas credenciales.

Para esto podemos utilizar la aplicación web

https://archive.org/

Se trata de un frontend a una base de datos muy extensa que contiene muchos datos como archivos, sistemas, etc así como snapshots de páginas web.

Recorre internet recopilando los estados actuales de las webs y los recopila en un diagrama temporal.

## TheHarvester

https://github.com/laramies/theHarvester

```bash
theHarvester -h
```

![Cuando se realizan muchas peticiones a un servicio concreto de motor de búsqueda lo que ocurre es que bloquean nuestra ip pública durante un tiempo.](/assets/img/posts/reconocimiento/20241125_233450_80-1.png)

```bash
theHarvester -d domain.com -b SOURCE -l 100 -f results
theHarvester -d domain.com -b all -l 100 -f results
```

## Maltego

Una de las herramientas más amplias y profesionales de recopilación de información pasiva.

### Instalación en Kali Linux

```bash
sudo apt install maltego
```

Nos pedirá registrar una cuenta en su web, es gratis no hay problema así que una vez configurado todo tenemos algo como esto

![](/assets/img/posts/reconocimiento/20241125_233627_81-1.png)

![Vamos a revisar actualizaciones](/assets/img/posts/reconocimiento/20241125_233646_81-2.png)

Vamos a comenzar entendiendo un par de conceptos

### Transformador

Todas las consultas hacen una query a una base de datos y ejecutan unos comandos que indexan la información. Estas consultas se denominan "transforms" que se ejecutan sobre diferentes bases de datos y que podemos asociar a diferentes entidades.

Empresas de terceros pueden hacer sus propios transformers para hacer querys a sus bases de datos.

![Instalamos algunas que nos interesen teniendo en cuenta que algunas como shodan, virustotal, etc pueden pedir API keys.](/assets/img/posts/reconocimiento/20241125_233817_81-3.png)

![](/assets/img/posts/reconocimiento/20241125_233828_81-4.png)

Creamos un nuevo grafo

### Grafos

Se trata un lienzo en el podremos arrastrar entidades que se tratan de diferentes tipos de información sobre los que podremos buscar en fuentes públicas haciendo uso de los transformadores.

![](/assets/img/posts/reconocimiento/20241125_233917_81-5.png)

Podemos ejecutar un análisis utilizando estos transformadores para recaudar datos de un nombre concreto o una entidad, incluso asociar una persona o serie de personas a una entidad y realizar una busqueda más concreta, etc.

![Podemos exportar el reporte](/assets/img/posts/reconocimiento/20241125_233946_81-6.png)

## Recon-Ng

https://github.com/lanmaster53/recon-ng

Es una herramienta basada en una interfaz de consola a la que se van accediendo a diferentes módulos.

https://github.com/lanmaster53/recon-ng-marketplace

### Uso

```bash
recon-ng
```

![](/assets/img/posts/reconocimiento/20241125_234110_82-1.png)

```bash
modules search
```

![Vamos a instalar algunos](/assets/img/posts/reconocimiento/20241125_234141_82-2.png)

```bash
marketplace search
```

![](/assets/img/posts/reconocimiento/20241125_234205_82-3.png)

![](/assets/img/posts/reconocimiento/20241125_234214_82-4.png)

![](/assets/img/posts/reconocimiento/20241125_234223_82-5.png)

![](/assets/img/posts/reconocimiento/20241125_234250_82-6.png)

![Si pulsamos tab veremos diferentes opciones del módulo](/assets/img/posts/reconocimiento/20241125_234323_82-7.png)

```bash
run
```

![](/assets/img/posts/reconocimiento/20241125_234407_82-8.png)