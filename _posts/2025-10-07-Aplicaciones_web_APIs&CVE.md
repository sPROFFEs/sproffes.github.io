---
title: Aplicaciones web APIs & CVE
date: 2025-10-07 11:00:00 +0000
categories: [Web, apuntes]
tags: [HTTP, web, API, CVE]
image:
  path: /assets/img/cabeceras_genericas/banner_api.png
  alt: cabecera
description: >
  APIs & CVE

pin: false  
toc: true   
math: false 
mermaid: false 
---


## Development Frameworks & APIs

Dado que la mayoría de las aplicaciones web comparten funcionalidades comunes, como el registro de usuarios, los marcos de desarrollo web facilitan la implementación rápida de estas funcionalidades y su vinculación con los componentes front-end, lo que da como resultado una aplicación web totalmente funcional. 

Algunos de los marcos de desarrollo web más comunes son:

- **Laravel** (PHP): suele ser utilizado por startups y empresas pequeñas, ya que es potente y fácil de desarrollar. 
- **Express** (Node.JS): utilizado por PayPal, Yahoo, Uber, IBM y MySpace. 
- **Django** (Python): utilizado por Google, YouTube, Instagram, Mozilla y Pinterest. 
- **Rails** (Ruby): utilizado por GitHub, Hulu, Twitch, Airbnb e incluso Twitter en el pasado.

## APIs

Un aspecto importante del desarrollo de aplicaciones web back-end es el uso de API web y parámetros de solicitud HTTP para conectar el front-end y el back-end, con el fin de poder enviar datos entre los componentes front-end y back-end y llevar a cabo diversas funciones dentro de la aplicación web.

Para que el componente front-end interactúe con el back-end y solicite la realización de determinadas tareas, utiliza API para solicitar al componente back-end una tarea específica con una entrada específica. Los componentes back-end procesan estas solicitudes, realizan las funciones necesarias y devuelven una respuesta determinada a los componentes front-end, que finalmente representan la salida del usuario final en el lado del cliente.

#### Query Parameters

El método predeterminado para enviar argumentos específicos a una página web es a través de los parámetros de solicitud GET y POST. 

Por ejemplo, una página /search.php tomaría un parámetro de elemento, que podría utilizarse para especificar el elemento de búsqueda. El paso de un parámetro a través de una solicitud GET se realiza a través de la URL «/search.php?item=apples», mientras que los parámetros POST se pasan a través de los datos POST en la parte inferior de la solicitud HTTP POST.

```http
POST /search.php HTTP/1.1
...SNIP...

item=apples
```

#### SOAP

El estándar SOAP (Simple Objects Access) comparte datos a través de XML, donde la solicitud se realiza en XML mediante una solicitud HTTP y la respuesta también se devuelve en XML.
Los componentes front-end están diseñados para analizar correctamente esta salida XML.

```xml
<?xml version="1.0"?>

<soap:Envelope
xmlns:soap="http://www.example.com/soap/soap/"
soap:encodingStyle="http://www.w3.org/soap/soap-encoding">

<soap:Header>
</soap:Header>

<soap:Body>
  <soap:Fault>
  </soap:Fault>
</soap:Body>

</soap:Envelope>
```

SOAP es muy útil para transferir datos estructurados (es decir, un objeto de clase completo) o incluso datos binarios, y se utiliza a menudo con objetos serializados, lo que permite compartir datos complejos entre los componentes front-end y back-end y analizarlos correctamente. 

También es muy útil para compartir objetos con estado, es decir, compartir o cambiar el estado 
actual de una página web, algo cada vez más habitual en las aplicaciones web y móviles modernas.


#### REST

El estándar REST (Representational State Transfer) comparte datos a través de la ruta URL «por ejemplo, search/users/1» y, por lo general, devuelve el resultado en formato JSON «por ejemplo, userid 1».

A diferencia de los parámetros de consulta, las API REST suelen centrarse en páginas que esperan un tipo de entrada que se pasa directamente a través de la ruta URL, sin especificar su nombre o tipo. Esto suele ser útil para consultas como búsquedas, ordenaciones o filtros. 
Por eso, las API REST suelen dividir la funcionalidad de las aplicaciones web en API más pequeñas y utilizan estas solicitudes de API más pequeñas para permitir que la aplicación web realice acciones más avanzadas, lo que hace que la aplicación web sea más modular y escalable.

Las respuestas a las solicitudes de la API REST suelen realizarse en formato JSON, y los componentes front-end se desarrollan para gestionar esta respuesta y representarla correctamente. Otros formatos de salida para REST incluyen XML, x-www-form-urlencoded o incluso datos sin procesar.

REST utiliza varios métodos HTTP para realizar diferentes acciones en la aplicación web:

- Solicitud **GET** para recuperar datos 
- Solicitud **POST** para crear datos (no idempotente) 
- Solicitud **PUT** para crear o sustituir datos existentes (idempotente) 
- Solicitud **DELETE** para eliminar datos


## Vulnerabilidades web comunes

Si realizáramos una prueba de penetración en una aplicación web desarrollada internamente o no encontráramos ningún exploit público para una aplicación web pública, podríamos identificar manualmente varias vulnerabilidades. 

También podemos descubrir vulnerabilidades causadas por configuraciones incorrectas, incluso en aplicaciones web disponibles públicamente, ya que este tipo de vulnerabilidades no son causadas por la versión pública de la aplicación web, sino por una configuración incorrecta realizada por los desarrolladores. 

#### Broken Authentication/Access Control

La autenticación rota se refiere a vulnerabilidades que permiten eludir las funciones de autenticación. Por ejemplo, esto puede permitir que un atacante inicie sesión sin tener un conjunto válido de credenciales o que un usuario normal se convierta en administrador sin tener los privilegios para hacerlo.

El control de acceso defectuoso se refiere a vulnerabilidades que permiten acceder a páginas y funciones a las que no deberían tener acceso. Por ejemplo, un usuario normal que obtiene acceso al panel de administración.

Por ejemplo, College Management System 1.2 tiene una vulnerabilidad simple de omisión de autenticación que nos permite iniciar sesión sin tener una cuenta, introduciendo lo siguiente en el campo del correo electrónico: ' o 0=0 #, y utilizando cualquier contraseña con ello.


#### Malicious File Upload

Otra forma habitual de obtener control sobre las aplicaciones web es mediante la carga de scripts maliciosos. Si la aplicación web tiene una función de carga de archivos y no valida correctamente los archivos cargados, podemos cargar un script malicioso (por ejemplo, un script PHP), lo que nos permitirá ejecutar comandos en el servidor remoto.

Aunque se trata de una vulnerabilidad básica, muchos desarrolladores no son conscientes de estas amenazas, por lo que no comprueban ni validan adecuadamente los archivos cargados. Algunos desarrolladores sí realizan comprobaciones e intentan validar los archivos cargados, pero estas comprobaciones a menudo pueden eludirse, lo que nos permitiría seguir cargando scripts maliciosos.

Por ejemplo, el plugin de WordPress Responsive Thumbnail Slider 1.0 puede ser explotado para subir cualquier archivo arbitrario, incluyendo scripts maliciosos, mediante la subida de un archivo con doble extensión (por ejemplo, shell.php.jpg).


#### Command Injection

Muchas aplicaciones web ejecutan comandos locales del sistema operativo para realizar determinados procesos. 

Por ejemplo, una aplicación web puede instalar un complemento de nuestra elección ejecutando un comando del sistema operativo que descarga ese complemento, utilizando el nombre del complemento proporcionado. 

Si no se filtra adecuadamente, se puede inyectar otro comando para que se ejecute junto con el comando originalmente previsto (es decir, como el nombre del complemento), lo que permite ejecutar directamente comandos en el servidor back-end y obtener el control sobre él. 

Esta vulnerabilidad está muy extendida, ya que los desarrolladores pueden no limpiar adecuadamente las entradas de los usuarios o utilizar pruebas poco rigurosas para hacerlo, lo que permite a los atacantes eludir cualquier comprobación o filtrado establecido y ejecutar sus comandos.

Por ejemplo, el plugin de WordPress Plainview Activity Monitor 20161228 tiene una vulnerabilidad que permite a los atacantes inyectar su comando en el valor ip, simplemente añadiendo | COMMAND... después del valor ip.


#### SQL Injection (SQLi)

Al igual que la vulnerabilidad de inyección de comandos, esta vulnerabilidad puede producirse cuando la aplicación web ejecuta una consulta SQL que incluye un valor tomado de la entrada proporcionada por el usuario.

```php
$query = "select * from users where name like '%$searchInput%'";
```

Si la entrada del usuario no se filtra y valida correctamente (como ocurre con las inyecciones de comandos), podemos ejecutar otra consulta SQL junto con esta consulta, lo que eventualmente nos permitiría tomar el control de la base de datos y su servidor de alojamiento.

Por ejemplo, College Management System 1.2 sufre de una vulnerabilidad de inyección SQL, en la que podemos ejecutar otra consulta SQL que siempre devuelve verdadero, lo que significa que nos hemos autenticado correctamente, lo que nos permite iniciar sesión en la aplicación. 

Podemos utilizar la misma vulnerabilidad para recuperar datos de la base de datos o incluso obtener el control del servidor de alojamiento.


## Vulnerabilidades públicas CVE

#### Public CVE

Dado que muchas organizaciones implementan aplicaciones web de uso público, como aplicaciones web de código abierto y propietarias, estas aplicaciones web suelen ser probadas por numerosas organizaciones y expertos de todo el mundo. Esto lleva a descubrir con frecuencia un gran número de vulnerabilidades, la mayoría de las cuales se corrigen y luego se comparten públicamente y se les asigna un registro y una puntuación CVE (Common Vulnerabilities and Exposures, Vulnerabilidades y exposiciones comunes).

Muchos evaluadores de seguridad también crean exploits de prueba de concepto para comprobar si una determinada vulnerabilidad pública puede ser explotada y, por lo general, ponen estos exploits a disposición del público con fines educativos y de prueba. Esto hace que la búsqueda de exploits públicos sea el primer paso que debemos dar en el caso de las aplicaciones web.


> [!NOTE] 
> El primer paso es identificar la versión de la aplicación web. Esto se puede encontrar en muchos lugares, como el código fuente de la aplicación web. Para las aplicaciones web de código abierto, podemos consultar el repositorio de la aplicación web e identificar dónde se muestra el número de versión (por ejemplo, en la página (version.php), y luego consultar la misma página en nuestra aplicación web de destino para confirmarlo.

Una vez identificada la versión de la aplicación web, podemos buscar exploits públicos para esta versión de la aplicación web. También podemos utilizar bases de datos de exploits en línea, como Exploit DB, Rapid7 DB o Vulnerability Lab. 

Por lo general, nos interesan los exploits con una puntuación CVE de 8-10 o los exploits que permiten la ejecución remota de código.

Si una aplicación web utiliza componentes externos (por ejemplo, un complemento), también debemos buscar vulnerabilidades en estos componentes externos.


#### Common Vulnerability Scoring System (CVSS)

El Sistema Común de Puntuación de Vulnerabilidades (CVSS) es un estándar industrial de código abierto para evaluar la gravedad de las vulnerabilidades de seguridad. Este sistema de puntuación se utiliza a menudo como medida estándar para organizaciones y gobiernos que necesitan generar puntuaciones de gravedad precisas y coherentes para las vulnerabilidades de sus sistemas.

Al calcular la gravedad de una vulnerabilidad utilizando CVSS, las métricas base producen una puntuación que oscila entre 0 y 10, modificada mediante la aplicación de métricas temporales y ambientales. 

La Base de Datos Nacional de Vulnerabilidades (NVD) proporciona puntuaciones CVSS para casi todas las vulnerabilidades conocidas y divulgadas públicamente. 
En este momento, la NVD solo proporciona puntuaciones básicas basadas en las características inherentes a una vulnerabilidad determinada. 

Los sistemas de puntuación actuales son CVSS v2 y CVSS v3. 


| Calificaciones CVSS V2.0 |                          |
| :----------------------- | :----------------------- |
| Gravedad                 | Rango de puntuación base |
| Baja                     | 0,0-3,9                  |
| Media                    | 4,0-6,9                  |
| Alta                     | 7,0-10,0                 |

| Calificaciones CVSS V3.0 |                          |
| ------------------------ | ------------------------ |
| Gravedad                 | Rango de puntuación base |
| Ninguna                  | 0,0                      |
| Baja                     | 0,1-3,9                  |
| Media                    | 4,0-6,9                  |
| Alta                     | 7,0-8,9                  |
| Crítica                  | 9,0-10,0                 |

El NVD no tiene en cuenta las métricas temporales y de entorno porque las primeras pueden cambiar con el tiempo debido a acontecimientos externos. Las segundas son métricas personalizadas basadas en el impacto potencial de la vulnerabilidad en una organización determinada.
Proporciona una calculadora CVSS v2 y una calculadora CVSS v3 que las organizaciones pueden utilizar para tener en cuenta el riesgo adicional derivado de los datos temporales y de entorno que les son propios. 


#### Vulnerabilidades del servidor back-end

Las vulnerabilidades más críticas para los componentes back-end se encuentran en los servidores web, ya que son accesibles públicamente a través del protocolo TCP. Un ejemplo de una vulnerabilidad muy conocida en los servidores web es Shell-Shock, que afectó a los servidores web Apache lanzados durante y antes de 2014 y utilizaba solicitudes HTTP para obtener control remoto sobre el servidor back-end.

En cuanto a las vulnerabilidades del servidor back-end o la base de datos, suelen utilizarse tras obtener acceso local al servidor back-end o la red back-end, lo que puede lograrse a través de vulnerabilidades externas o durante pruebas de penetración internas. 
