---
title: Javascript deobfuscation
date: 2025-10-12 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, javascript, cifrado]
image:
  path: /assets/img/posts/javascript-deofuscado/js_banner.png
  alt: cabecera
description: >
   Javascript deobfuscation

pin: false  
toc: true   
math: false 
mermaid: false 
---


## Código fuente

El código javascript puede estar incluido dentro del propio HTML entre etiquetas `<script>` o referenciado en un archivo externo.

## Ofuscación

Es una técnica utilizada para dificultar la lectura de un script por parte de los seres humanos, pero que permite que funcione igual desde un punto de vista técnico, aunque el rendimiento pueda ser más lento. Esto se consigue normalmente de forma automática mediante el uso de una herramienta de ofuscación, que toma el código como entrada e intenta reescribirlo de una forma mucho más difícil de leer, dependiendo de su diseño.

Por ejemplo, los ofuscadores de código suelen convertir el código en un diccionario con todas las palabras y símbolos utilizados en él y, a continuación, intentan reconstruir el código original durante la ejecución consultando cada palabra y símbolo del diccionario. A continuación se muestra un ejemplo de un código JavaScript sencillo que se ha ofuscado:

![image](/assets/img/posts/javascript-deofuscado/20251012124137.png)

### Minimizar código JavaScript

Una forma habitual de reducir la legibilidad de un fragmento de código JavaScript sin afectar a su funcionalidad. Consiste en colocar todo el código en una sola línea (a menudo muy larga). 
La minificación de código es más útil para códigos largos, ya que si nuestro código solo constara de una sola línea, no se vería muy diferente una vez minificado.

https://javascript-minifier.com/
### Empaquetado de código JavaScript

http://beautifytools.com/javascript-obfuscator.php

![image](/assets/img/posts/javascript-deofuscado/20251012124836.png)

El tipo de ofuscación anterior se conoce como «empaquetado», que suele reconocerse por los seis argumentos de función utilizados en la función inicial «function(p,a,c,k,e,d)».

Una herramienta de ofuscación de empaquetadores suele intentar convertir todas las palabras y símbolos del código en una lista o un diccionario y, a continuación, hacer referencia a ellos utilizando la función (p,a,c,k,e,d) para reconstruir el código original durante la ejecución. 

La función (p,a,c,k,e,d) puede ser diferente de un empaquetador a otro. Sin embargo, suele contener un orden determinado en el que se empaquetaron las palabras y los símbolos del código original para saber cómo ordenarlos durante la ejecución.

  Aunque un empaquetador hace un gran trabajo reduciendo la legibilidad del código, aún podemos ver sus cadenas principales escritas en texto claro, lo que puede revelar algunas de sus funciones.

### Obfuscator

https://obfuscator.io/

![image](/assets/img/posts/javascript-deofuscado/20251012125315.png)

Code: javascript

```javascript
var _0x1ec6=['Bg9N','sfrciePHDMfty3jPChqGrgvVyMz1C2nHDgLVBIbnB2r1Bgu='];(function(_0x13249d,_0x1ec6e5){var _0x14f83b=function(_0x3f720f){while(--_0x3f720f){_0x13249d['push'](_0x13249d['shift']());}};_0x14f83b(++_0x1ec6e5);}(_0x1ec6,0xb4));var _0x14f8=function(_0x13249d,_0x1ec6e5){_0x13249d=_0x13249d-0x0;var _0x14f83b=_0x1ec6[_0x13249d];if(_0x14f8['eOTqeL']===undefined){var _0x3f720f=function(_0x32fbfd){var _0x523045='abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/=',_0x4f8a49=String(_0x32fbfd)['replace'](/=+$/,'');var _0x1171d4='';for(var _0x44920a=0x0,_0x2a30c5,_0x443b2f,_0xcdf142=0x0;_0x443b2f=_0x4f8a49['charAt'](_0xcdf142++);~_0x443b2f&&(_0x2a30c5=_0x44920a%0x4?_0x2a30c5*0x40+_0x443b2f:_0x443b2f,_0x44920a++%0x4)?_0x1171d4+=String['fromCharCode'](0xff&_0x2a30c5>>(-0x2*_0x44920a&0x6)):0x0){_0x443b2f=_0x523045['indexOf'](_0x443b2f);}return _0x1171d4;};_0x14f8['oZlYBE']=function(_0x8f2071){var _0x49af5e=_0x3f720f(_0x8f2071);var _0x52e65f=[];for(var _0x1ed1cf=0x0,_0x79942e=_0x49af5e['length'];_0x1ed1cf<_0x79942e;_0x1ed1cf++){_0x52e65f+='%'+('00'+_0x49af5e['charCodeAt'](_0x1ed1cf)['toString'](0x10))['slice'](-0x2);}return decodeURIComponent(_0x52e65f);},_0x14f8['qHtbNC']={},_0x14f8['eOTqeL']=!![];}var _0x20247c=_0x14f8['qHtbNC'][_0x13249d];return _0x20247c===undefined?(_0x14f83b=_0x14f8['oZlYBE'](_0x14f83b),_0x14f8['qHtbNC'][_0x13249d]=_0x14f83b):_0x14f83b=_0x20247c,_0x14f83b;};console[_0x14f8('0x0')](_0x14f8('0x1'));
```

Ahora deberíamos tener una idea clara de cómo funciona la ofuscación de código. Todavía hay muchas variaciones de herramientas de ofuscación de código, cada una de las cuales ofusca el código de manera diferente. 

![image](/assets/img/posts/javascript-deofuscado/20251012125508.png)

http://www.jsfuck.com/

Existen muchos otros ofuscadores de JavaScript, como [JJ Encode](https://utf-8.jp/public/jjencode.html) o [AA Encode](https://utf-8.jp/public/aaencode.html). Sin embargo, estos ofuscadores suelen ralentizar considerablemente la ejecución y compilación del código, por lo que no se recomienda su uso a menos que exista una razón obvia, como eludir filtros o restricciones web.


### Desofuscación

#### Beautify

Si estuviéramos utilizando Firefox, podemos abrir el depurador del navegador con [ CTRL+MAYÚS+Z ] y, a continuación, hacer clic en nuestro script secret.js. Esto mostrará el script con su formato original, pero podemos hacer clic en el botón «{ }» situado en la parte inferior, que imprimirá el script con el formato JavaScript adecuado.

Además, podemos utilizar muchas herramientas en línea o complementos de editores de código, como [Prettier](https://prettier.io/playground/) o [Beautifier](https://beautifier.io/). Copiemos el script secret.js:

![image](/assets/img/posts/javascript-deofuscado/20251012130340.png)

Podemos encontrar muchas herramientas online útiles para desofuscar código JavaScript y convertirlo en algo que podamos entender. Una buena herramienta es [UnPacker](https://matthewfl.com/unPacker.html). 

![image](/assets/img/posts/javascript-deofuscado/20251012130613.png)

El método de ofuscación utilizado anteriormente es el empaquetado. Otra forma de desempaquetar dicho código es encontrar el valor de retorno al final y utilizar console.log para imprimirlo en lugar de ejecutarlo.

Una vez que el código se vuelve más confuso y codificado, resulta mucho más difícil limpiarlo con herramientas automatizadas. Esto es especialmente diícil si el código se ha ocultado utilizando una herramienta de ocultación personalizada.


### Análisis de código

```javascript
'use strict';
function generateSerial() {
  ...SNIP...
  var xhr = new XMLHttpRequest;
  var url = "/serial.php";
  xhr.open("POST", url, true);
  xhr.send(null);
};
```

Vemos que el archivo secret.js contiene solo una función, generateSerial.

##### Variables

Se define una variable xhr que crea un objeto XMLHttpRequest que maneja peticiones web.

La segunda variable URL contiene una ruta /serial.php que debe estar en el mismo dominio.

##### Funciones

- xhr.open:
Utiliza la función xhr para crear una petición POST  a la URL.

- xhr.send:
Envía esa petición creada sin contenido adicional.

Basicamente envía la petición POST a /serial.php sin datos en el body por lo tanto no recibe nada de vuelta.


##### Replicado

Sabiendo el proceso que intenta ejecutar el código podemos intentar imitarlo para probar si tenemos respuesta del backend.

```shell-session
$ curl -s http://SERVER_IP:PORT/ -X POST -d "param1=sample"
```


### Decodificación

![image](/assets/img/posts/javascript-deofuscado/20251012133216.png)

Por ese motivo, es muy frecuente encontrar código ofuscado que contiene bloques de texto codificados que se descodifican durante la ejecución. 

##### Base64

Se utiliza para reducir el uso de carácteres espciales ya que estos se codifícan utilizando carácteres alpha-numeric junto con + y /. 

Las cadenas codificadas con base64 se reconocen rápidamente ya que solo contienen carácteres alpha-numericos y que su padding se realiza con los carácteres =. 

La longitud de las cadenas codificadas en base 64 tienden a ser múltipos de 4; por ejemplo si la salida es una cadena de 3 carácteres, se añade = al final para que sean 4.

```shell-session
$ echo https://www.example.com/ | base64

aHR0cHM6Ly93d3cuZXhhbXBsZS5jb20vCg==
```

```shell-session
$ echo aHR0cHM6Ly93d3cuZXhhbXBsZS5jb20vCg== | base64 -d

https://www.example.com/
```

##### Hexadecimal

Este tipo de codificación convierte cada carácter en su orden relativo en la tabla ASCII.

Por ejemplo a=61, b=62, c=63, etc...

Estas cadenas se pueden reconocer facilmente ya que solo utilizan 16 carácteres 0-9 a-f.

```shell-session
echo https://www.example.com/ | xxd -p

68747470733a2f2f7777772e6578616d706c652e636f6d2f0a
```

```shell-session
$ echo 68747470733a2f2f7777772e6578616d706c652e636f6d2f0a | xxd -p -r

https://www.example.com/
```

##### Cesar/Rot13

Es una técnica muy antigua que consiste en rotar cada letra x veces; por ejemplo:

Rotamos a 3 veces pasaría a ser d, b pasa a ser e, etc...

Hay muchas variaciones de este cifrado pero una de las más comunes es rot13.

Aunque este método de codificación hace que cualquier texto parezca aleatorio, sigue siendo posible detectarlo porque cada carácter se asigna a un carácter específico. Por ejemplo, en rot13, http://www se convierte en uggc://jjj, que sigue teniendo algunas similitudes y puede reconocerse como tal.

```shell-session
$ echo https://www.example.com/ | tr 'A-Za-z' 'N-ZA-Mn-za-m'
uggcf://jjj.rknzcyr.pbz/
```
```shell-session
echo uggcf://jjj.rknzcyr.pbz/ | tr 'A-Za-z' 'N-ZA-Mn-za-m'
https://www.example.com/
```
