---
title: Web fuzzing
date: 2025-10-08 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, fuzzing]
image:
  path: /assets/img/cabeceras_genericas/web-fuzzing-banner.png
  alt: cabecera
description: >
  Reconocimiento web 

pin: false  
toc: true   
math: false 
mermaid: false 
---

### Fuzzing vs. Brute-forcing

- El fuzzing involucra una red más amplia. La finalidad es forzar la aplicación con inputs mal formados, carácteres inválidos o combianciones sin sentido, todo para ver como responde la aplicación ante estos inputs. 
- La fuerza bruta o brute-forzing es algo más objetivo, ya que se enfoca en intentar de forma repetida un valor o valores específicos como usuarios o contraseñas. 



> [!NOTE] analogía
> El fuzzing sería como intentar abrir una puerta cerrada lanzando todo lo que tengamos a mano, mientras el brute-forcing sería tener un manojo de llaves e ir probando una a una hasta que se abra.

#### ¿Para qué se hace el fuzzing?

Cada vez las aplicaciones web son más grandes y complejas haciendo que manejen gran cantidad de datos, por lo que el fuzzing permite:

- **Descubrir vulnerabilidades ocultas:**

El _fuzzing_ puede descubrir vulnerabilidades que los métodos tradicionales de pruebas de seguridad podrían pasar por alto. Al bombardear una aplicación web con entradas inesperadas o inválidas, puede provocar comportamientos no previstos que revelen fallos ocultos en el código.

- **Automatización de pruebas de seguridad:**

El _fuzzing_ automatiza la generación y el envío de entradas de prueba, lo que ahorra tiempo y recursos valiosos. Esto permite que los equipos de seguridad se centren en analizar los resultados y corregir las vulnerabilidades detectadas.

- **Simulación de ataques reales:**

Los _fuzzers_ pueden imitar técnicas utilizadas por atacantes, ayudando a identificar debilidades antes de que sean explotadas por actores maliciosos. Este enfoque proactivo puede reducir significativamente el riesgo de un ataque exitoso.

- **Fortalecimiento de la validación de entradas:**

El _fuzzing_ permite detectar debilidades en los mecanismos de validación de datos, fundamentales para prevenir vulnerabilidades comunes como **inyecciones SQL** y **cross-site scripting (XSS)**.

- **Mejora de la calidad del código:**

Además de mejorar la seguridad, el _fuzzing_ ayuda a descubrir errores y fallos, lo que contribuye a un código más robusto y confiable. Los desarrolladores pueden usar el feedback del _fuzzing_ para escribir código más sólido.

- **Seguridad continua:**

El _fuzzing_ puede integrarse en el ciclo de vida del desarrollo de software (SDLC) como parte de los procesos de **integración continua** y **despliegue continuo** (CI/CD), garantizando que las pruebas de seguridad se realicen regularmente y que las vulnerabilidades se detecten desde las primeras etapas del desarrollo.


## Herramientas

pipx es una herramienta de línea de comandos diseñada para simplificar la instalación y gestión de aplicaciones Python. Agiliza el proceso creando entornos virtuales aislados para cada aplicación, lo que garantiza que las dependencias no entren en conflicto. Esto significa que puedes instalar y ejecutar múltiples aplicaciones Python sin preocuparte por problemas de compatibilidad. pipx también facilita la actualización o desinstalación de aplicaciones, manteniendo tu sistema organizado y libre de desorden.


    
            shellsession
    `$ sudo apt update`
    

    
            shellsession
    `$ sudo apt install -y golang`
    

    
            shellsession
    `$ sudo apt install -y python3 python3-pip`
    

    
            shellsession
		$ sudo apt install pipx pr0ff3@htb[/htb]$ pipx ensurepath 
		$ sudo pipx ensurepath --global`
    

    
            shellsession
    `$ go version pr0ff3@htb[/htb]$ python3 --version`

#### FFUF

FFUF (Fuzz Faster U Fool) es un fuzzer web rápido escrito en Go. Destaca por su capacidad para enumerar rápidamente directorios, archivos y parámetros dentro de aplicaciones web. Su flexibilidad, velocidad y facilidad de uso lo convierten en uno de los favoritos.

```
$ go install github.com/ffuf/ffuf/v2@latest
```

#### Gobuster

Gobuster es otro popular directorio web y fuzzer de archivos. Es conocido por su velocidad y simplicidad, lo que lo convierte en una excelente opción.

```
$ go install github.com/OJ/gobuster/v3@latest
```

### Feroxbuster

FeroxBuster es una herramienta rápida y recursiva para descubrir contenido, escrita en Rust. Está diseñada para descubrir por fuerza bruta contenido sin enlaces en aplicaciones web, lo que la hace especialmente útil para identificar directorios y archivos ocultos. Es más una herramienta de «navegación forzada» que un fuzzer como ffuf.

```
$ curl -sL https://raw.githubusercontent.com/epi052/feroxbuster/main/install-nix.sh | sudo bash -s $HOME/.local/bin
```

#### wfuzz/wenum

wenum es una bifurcación de wfuzz que se mantiene activamente, una herramienta de fuzzing de línea de comandos muy versátil y potente, conocida por su flexibilidad y opciones de personalización. Es especialmente adecuada para el fuzzing de parámetros, ya que permite probar una amplia gama de valores de entrada en aplicaciones web y descubrir posibles vulnerabilidades en la forma en que procesan esos parámetros.

```
$ pipx install git+https://github.com/WebFuzzForge/wenum
$ pipx runpip wenum install setuptools
```

```
$ ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -u http://IP:PORT/FUZZ


        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : GET
 :: URL              : http://IP:PORT/FUZZ
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200-399
________________________________________________

[...]

w2ksvrus                [Status: 301, Size: 0, Words: 1, Lines: 1, Duration: 0ms]
:: Progress: [220559/220559] :: Job [1/1] :: 100000 req/sec :: Duration: [0:00:03] :: Errors: 0 ::
```
```
pr0ff3@htb[/htb]$ ffuf -w /usr/share/seclists/Discovery/Web-Content/common.txt -u http://IP:PORT/w2ksvrus/FUZZ.html -e .php,.html,.txt,.bak,.js -v
```

### Recursive fuzzing

```
$ ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -ic -v -u http://IP:PORT/FUZZ -e .html -recursion
```

El indicador **-recursion**. le indica a ffuf que realice fuzzing en cualquier directorio que encuentre de forma recursiva. 
Por ejemplo, si ffuf descubre un directorio admin, iniciará automáticamente un nuevo proceso de fuzzing en http://localhost/admin/FUZZ. 

En escenarios de fuzzing en los que las listas de palabras contienen comentarios (líneas que comienzan con #), la opción ffuf -ic resulta muy valiosa. Al habilitar esta opción, ffuf ignora de forma inteligente las líneas comentadas durante el fuzzing, evitando que se traten como entradas válidas.

Puede consumir muchos recursos, especialmente en aplicaciones web grandes. Las solicitudes excesivas pueden sobrecargar el servidor objetivo, causando potenciales problemas de rendimiento o activando mecanismos de seguridad.

Para mitigar estos riesgos, ffuf ofrece opciones para afinar el proceso de fuzzing recursivo:

- `-recursion-depth`: Este parámetro te permite establecer una profundidad máxima para la exploración recursiva. Por ejemplo, `-recursion-depth 2` limita el fuzzing a dos niveles de profundidad (el directorio inicial y sus subdirectorios inmediatos).
    
- `-rate`: Puedes controlar la tasa a la que ffuf envía solicitudes por segundo, evitando sobrecargar el servidor.
    
- `-timeout`: Esta opción establece el tiempo de espera para solicitudes individuales, ayudando a prevenir que el fuzzer se quede colgado en objetivos que no responden.
```
$ ffuf -w /usr/share/seclists/Discovery/Web-Content/directory-list-2.3-medium.txt -ic -u http://IP:PORT/FUZZ -e .html -recursion -recursion-depth 2 -rate 500
```


### Fuzzing de parámetros

#### GET
```http
https://example.com/search?query=fuzzing&category=security
```

En esta URL:

- query es un parámetro con el valor «fuzzing»

- category es otro parámetro con el valor «security»

#### POST 

```html
POST /login HTTP/1.1 Host: example.com Content-Type: application/x-www-form-urlencoded username=your_username&password=your_password
```

Cuando envías un formulario o interactúas con una página web que utiliza solicitudes POST, ocurre lo siguiente:


	**Recopilación de datos**: la información introducida en los campos del formulario se recopila y se prepara para su transmisión.
	
	**Codificación**: Estos datos se codifican en un formato específico, normalmente application/x-www-form-urlencoded o multipart/form-data:
	
	**application/x-www-form-urlencoded**: Este formato codifica los datos como pares clave-valor separados por el símbolo «&», de forma similar a los parámetros GET, pero colocados dentro del cuerpo de la solicitud en lugar de en la URL.
	
	**multipart/form-data**: este formato se utiliza cuando se envían archivos junto con otros datos. Divide el cuerpo de la solicitud en varias partes, cada una de las cuales contiene un dato específico o un archivo.
	
	S**olicitud HTTP**: los datos codificados se colocan dentro del cuerpo de una solicitud HTTP POST y se envían al servidor web.
	
	**Procesamiento del lado del servidor**: el servidor recibe la solicitud POST, decodifica los datos y los procesa de acuerdo con la lógica de la aplicación.


### Wenum

```
$ pipx install git+https://github.com/WebFuzzForge/wenum 
$ pipx runpip wenum install setuptools
```

```
$ wenum -w /usr/share/seclists/Discovery/Web-Content/common.txt --hc 404 -u "http://IP:PORT/get.php?x=FUZZ"

...
 Code    Lines     Words        Size  Method   URL 
...
 200       1 L       1 W        25 B  GET      http://IP:PORT/get.php?x=OA... 

Total time: 0:00:02
Processed Requests: 4731
Filtered Requests: 4730
Requests/s: 1681
```

```
$ ffuf -u http://IP:PORT/post.php -X POST -H "Content-Type: application/x-www-form-urlencoded" -d "y=FUZZ" -w /usr/share/seclists/Discovery/Web-Content/common.txt -mc 200 -v

        /'___\  /'___\           /'___\       
       /\ \__/ /\ \__/  __  __  /\ \__/       
       \ \ ,__\\ \ ,__\/\ \/\ \ \ \ ,__\      
        \ \ \_/ \ \ \_/\ \ \_\ \ \ \ \_/      
         \ \_\   \ \_\  \ \____/  \ \_\       
          \/_/    \/_/   \/___/    \/_/       

       v2.1.0-dev
________________________________________________

 :: Method           : POST
 :: URL              : http://IP:PORT/post.php
 :: Wordlist         : FUZZ: /usr/share/seclists/Discovery/Web-Content/common.txt
 :: Header           : Content-Type: application/x-www-form-urlencoded
 :: Data             : y=FUZZ
 :: Follow redirects : false
 :: Calibration      : false
 :: Timeout          : 10
 :: Threads          : 40
 :: Matcher          : Response status: 200
________________________________________________

[Status: 200, Size: 26, Words: 1, Lines: 2, Duration: 7ms]
| URL | http://IP:PORT/post.php
    * FUZZ: SU...

:: Progress: [4730/4730] :: Job [1/1] :: 5555 req/sec :: Duration: [0:00:01] :: Errors: 0 ::
```


### Virtual host fuzzing

```
$ echo "IP inlanefreight.htb" | sudo tee -a /etc/hosts
```

```
$ gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/Web-Content/common.txt --append-domain
```

`gobuster vhost`: Esta bandera activa el modo de fuzzing de vhosts de Gobuster, indicándole que se enfoque en descubrir hosts virtuales en lugar de directorios o archivos.  

`-u http://inlanefreight.htb:81`: Especifica la URL base del servidor objetivo. Gobuster usará esta URL como base para construir las peticiones con diferentes nombres de vhost. En este ejemplo, el servidor objetivo está en `inlanefreight.htb` y escucha en el puerto `81`.  

`-w /usr/share/seclists/Discovery/Web-Content/common.txt`: Señala el archivo de wordlist que Gobuster usará para generar nombres potenciales de vhost. La wordlist `common.txt` de SecLists contiene una colección de nombres de vhost y subdominios comúnmente usados.  

`--append-domain`: Esta bandera crucial indica a Gobuster que añada el dominio base (`inlanefreight.htb`) a cada palabra de la wordlist. Esto asegura que la cabecera `Host` en cada petición incluya un nombre de dominio completo (por ejemplo, `admin.inlanefreight.htb`), lo cual es esencial para la detección de vhosts.

```
$ gobuster vhost -u http://inlanefreight.htb:81 -w /usr/share/seclists/Discovery/Web-Content/common.txt --append-domain

===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:             http://inlanefreight.htb:81
[+] Method:          GET
[+] Threads:         10
[+] Wordlist:        /usr/share/SecLists/Discovery/Web-Content/common.txt
[+] User Agent:      gobuster/3.6
[+] Timeout:         10s
[+] Append Domain:   true
===============================================================
Starting gobuster in VHOST enumeration mode
===============================================================
Found: .git/logs/.inlanefreight.htb:81 Status: 400 [Size: 157]
...
Found: admin.inlanefreight.htb:81 Status: 200 [Size: 100]
Found: android/config.inlanefreight.htb:81 Status: 400 [Size: 157]
...
Progress: 4730 / 4730 (100.00%)
===============================================================
Finished
===============================================================
```


### Fuzzing de subdominios

```
$ gobuster dns -d inlanefreight.com -w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt
```

`gobuster dns`: Activa el modo de fuzzing DNS de Gobuster, indicándole que se enfoque en el descubrimiento de subdominios.  

`-d inlanefreight.com`: Especifica el dominio objetivo (por ejemplo, `inlanefreight.com`) para el que quieres descubrir subdominios.  

`-w /usr/share/seclists/Discovery/DNS/subdomains-top1million-5000.txt`: Señala el archivo de wordlist que Gobuster usará para generar nombres potenciales de subdominios. En este ejemplo usamos una wordlist que contiene las 5000 subdominios más comunes.


### Identificar API endpoints

##### REST

Las API REST se basan en el concepto de recursos, que se identifican mediante URL únicas denominadas «endpoints». Estos endpoints son los destinos de las solicitudes de los clientes y suelen incluir parámetros para proporcionar contexto adicional o control sobre la operación solicitada.

/users: representa una colección de recursos de usuario.

/users/123: representa un usuario específico con el ID 123.

/products: representa una colección de recursos de productos.

/products/456: representa un producto específico con el ID 456.

|Tipo de Parámetro|Descripción|Ejemplo|
|---|---|---|
|Parámetros de consulta|Se añaden a la URL del endpoint después de un signo de interrogación (?). Se usan para filtrar, ordenar o paginar.|`/users?limit=10&sort=name`|
|Parámetros de ruta|Empotrados directamente en la URL del endpoint. Se usan para identificar recursos específicos.|`/products/{id}pen_spark`|
|Parámetros en el cuerpo de la petición|Se envían en el cuerpo de peticiones POST, PUT o PATCH. Se usan para crear o actualizar recursos.|`{ "name": "New Product", "price": 99.99 }`|

#### SOAP (simple object access protocol)

Las API SOAP (Simple Object Access Protocol) tienen una estructura diferente a las API REST. Se basan en mensajes XML y archivos WSDL (Web Services Description Language) para definir sus interfaces y operaciones.

Las API SOAP suelen exponer un único punto final. Este punto final es una URL en la que el servidor SOAP escucha las solicitudes entrantes. El contenido del mensaje SOAP determina la operación específica que se desea realizar.

Los parámetros SOAP se definen dentro del cuerpo del mensaje SOAP, un documento XML. Estos parámetros se organizan en elementos y atributos, formando una estructura jerárquica. 

La estructura específica de los parámetros depende de la operación que se invoque. 
Los parámetros se definen en el archivo Web Services Description Language (WSDL), un documento basado en XML que describe la interfaz, las operaciones y los formatos de mensaje del servicio web.

Para identificar los puntos finales (operaciones) y parámetros disponibles para una API SOAP, puede utilizar los siguientes métodos:

Análisis WSDL: el archivo WSDL es el recurso más valioso para comprender una API SOAP. Describe:

- Operaciones disponibles (puntos finales)

- Parámetros de entrada para cada operación (tipos de mensajes, elementos y atributos)

- Parámetros de salida para cada operación (tipos de mensajes de respuesta)

- Tipos de datos utilizados para los parámetros (por ejemplo, cadenas, enteros, tipos complejos)

- La ubicación (URL) del punto final SOAP


#### GraphQL Queries

Las consultas están diseñadas para recuperar datos del servidor GraphQL. Identifican con precisión los campos, las relaciones y los objetos anidados que desea el cliente, lo que elimina el problema de la recuperación excesiva o insuficiente de datos, habitual en las API REST. Los argumentos dentro de las consultas permiten un mayor refinamiento, como el filtrado o la paginación.

|Componente|Descripción|Ejemplo|
|---|---|---|
|**Campo (Field)**|Representa una pieza específica de datos que deseas recuperar (por ejemplo, nombre, correo electrónico).|`name`, `email`|
|**Relación (Relationship)**|Indica una conexión entre diferentes tipos de datos (por ejemplo, las publicaciones de un usuario).|`posts`|
|**Objeto anidado (Nested Object)**|Un campo que devuelve otro objeto, permitiéndote profundizar más en el grafo de datos.|`posts { title, body }`|
|**Argumento (Argument)**|Modifica el comportamiento de una consulta o campo (por ejemplo, filtrado, ordenamiento, paginación).|`posts(limit: 5)` (recupera las primeras 5 publicaciones de un usuario)|
Las mutaciones son el equivalente a las consultas diseñadas para modificar datos en el servidor. Abarcan operaciones para crear, actualizar o eliminar datos. Al igual que las consultas, las mutaciones también pueden aceptar argumentos para definir los valores de entrada para estas operaciones.

|Componente|Descripción|Ejemplo|
|---|---|---|
|**Operación (Operation)**|La acción que se desea realizar (por ejemplo, crear una publicación, actualizar un usuario, eliminar un comentario).|`createPost`|
|**Argumento (Argument)**|Datos de entrada necesarios para la operación (por ejemplo, título y contenido de una nueva publicación).|`title: "New Post", body: "This is the content of the new post"`|
|**Selección (Selection)**|Campos que deseas recuperar en la respuesta después de que se complete la mutación.|`id`, `title`|
```
mutation {
  createPost(title: "New Post", body: "This is the content of the new post") {
    id
    title
  }
}
```

			