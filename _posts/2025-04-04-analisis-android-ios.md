---
title: Analisis Android/iOS
date: 2025-04-04 11:00:00 +0000
categories: [Forense, Dispositivos moviles]
tags: [android, ios, análisis, mobileedit, avillaForensics]
image:
  path: /assets/img/posts/analisis-android-ios/cabecera.png
  alt:  cabecera
description: >
  Ejemplo de analisis de un dispositivo Android/iOS con avillaForensics y mobileedit
pin: false  
toc: true   
math: false 
mermaid: false 
---

---

## Introducción

En el ámbito del análisis forense digital, contar con herramientas especializadas y actualizadas es fundamental para obtener evidencia precisa y confiable. En este post, exploramos dos soluciones destacadas en el análisis forense de dispositivos móviles: **Avilla Forensics** y **MOBILedit**. Ambas herramientas, aunque con enfoques y características diferentes, han ganado reconocimiento por su efectividad y versatilidad en investigaciones criminales, auditorías internas y procesos judiciales.

**Avilla Forensics**, desarrollada por el investigador brasileño Daniel Avilla, es una herramienta gratuita que ha revolucionado el análisis lógico de dispositivos Android. Compatible con Windows y con soporte para versiones recientes de Android (hasta la 15), permite la recolección segura de datos sin necesidad de acceso root, gracias a módulos como APK Downgrade y App Full Extraction. Su sistema de integridad y cifrado de evidencias ofrece garantías esenciales para mantener la cadena de custodia digital.

Por otro lado, **MOBILedit** es una solución comercial ampliamente utilizada en entornos profesionales. Ofrece funcionalidades avanzadas para la extracción, análisis y visualización de datos de dispositivos móviles, con soporte para una amplia gama de marcas y modelos. Su interfaz intuitiva y compatibilidad con herramientas forenses reconocidas lo convierten en una opción sólida para peritos, fuerzas de seguridad y analistas forenses.

--- 

## MobileEdit

Antes de comenzar decir que la versión utilizada en este post es la versión de pago por lo que debemos activar la licencia antes de utilizarla.

A día de realizar este post, Compelson ofrece una versión de MobileEdit gratuita que dejaré a continuación aunque sus características son más limitadas que las de la versión comercial.

- [Versión gratuita](https://www.mobiledit.com/forensic-express-personal)

### Activación y actualización

![alt text](/assets/img/posts/analisis-android-ios/image.png)

![alt text](/assets/img/posts/analisis-android-ios/image-1.png)

![alt text](/assets/img/posts/analisis-android-ios/image-2.png)

Una vez activado vamos a actualizar los componentes de MobileEdit a la versión más reciente.

![alt text](/assets/img/posts/analisis-android-ios/image-3.png)

![alt text](/assets/img/posts/analisis-android-ios/image-4.png)

![alt text](/assets/img/posts/analisis-android-ios/image-5.png)

Tras esperar un rato podemos ver todos los componentes actualizados.

![alt text](/assets/img/posts/analisis-android-ios/image-6.png)

### Ejemplo de uso en Android
Antes de empezar vamos a reiniciar la aplicación para que se actualicen los componentes.

Al conectar nuestro dispositvo el software lo reconocerá y si no tenemos activado el modo depuración nos perdrirá que lo activemos ya que es necesario para poder que el software funcione correctamente.

![alt text](/assets/img/posts/analisis-android-ios/image-7.png)

Una vez hecho esto en nuestro dispositivo, podemos ver como el software reconocerá el mismo.

![alt text](/assets/img/posts/analisis-android-ios/image-8.png)

Si hacemos click en el icono "i" vemos información general sobre el dispositivo.

![alt text](/assets/img/posts/analisis-android-ios/image-9.png)

Ahora vamos a hacer click en el apartado que hay justo debajo del dispositivo "Phone data preview".

Nos preguntará si queremos instalar la aplicación de MobileEdit en nuestro dispositivo.

![alt text](/assets/img/posts/analisis-android-ios/image-10.png)

Seleccionamos instalar y esto instalará la aplicación automáticamente y reconectará el dispositivo.

Tras un escaneo nos preguntará si queremos empezar la extracción de datos.

![alt text](/assets/img/posts/analisis-android-ios/image-11.png)

Al terminar nos abre los registros de llamadas, mensajes, contactos, etc.

En este ejemplo no veremos nada ya que el teléfono es de pruebas y no tiene ninguna información personal.

![alt text](/assets/img/posts/analisis-android-ios/image-12.png)

Vamos ahora con la opción de saltar la seguridad del dispositivo.

![alt text](/assets/img/posts/analisis-android-ios/image-13.png)

Podremos seleccionar en función del modelo, chipset o método.

![alt text](/assets/img/posts/analisis-android-ios/image-14.png)

![alt text](/assets/img/posts/analisis-android-ios/image-15.png)

Para este modelo vemos que nos ofrecen las siguientes opciones.

![alt text](/assets/img/posts/analisis-android-ios/image-16.png)

Vamos a probar a tener acceso root de forma temporal.

Nos muestra las vulnerabilidades que puede aprovechar para obtener acceso root.

![alt text](/assets/img/posts/analisis-android-ios/image-17.png)

Nos indica lo que necesitamos para hacer el proceso.

![alt text](/assets/img/posts/analisis-android-ios/image-18.png)

Al detectar el dispositivo veremos el proceso que se está ejecutando.

![alt text](/assets/img/posts/analisis-android-ios/image-19.png)

En este caso el proceso no ha sido posible.

![alt text](/assets/img/posts/analisis-android-ios/image-20.png)

Aunque no hayamos conseguido acceso root podemos ver contenido del dispositivo.

Seleccionamos navegar contenido.

![alt text](/assets/img/posts/analisis-android-ios/image-21.png)

En este navegador de archivos podemos explorar y analizar el contenido del dispositivo conectado.

![alt text](/assets/img/posts/analisis-android-ios/image-22.png)

![alt text](/assets/img/posts/analisis-android-ios/image-23.png)

Para ver más opciones vamos doble click sobre el dispositivo.

![alt text](/assets/img/posts/analisis-android-ios/image-24.png)

#### Logical extraction

![alt text](/assets/img/posts/analisis-android-ios/image-25.png)

Esta opcíón nos permite extraer información útil del dispositivo. Aunque es posible usarla sin rootear el dispositivo, es más recomendable hacerlo con root ya que conseguiremos toda la información posible.

Es por eso que una de las opciones más abajo es rootear el dispositivo como intentamos antes aunque nos ofrece opciones más generales que podemos usar.

![alt text](/assets/img/posts/analisis-android-ios/image-26.png)

Como en este caso el dispositivo no es vulnerable vamos a tener únicamente acceso a cierta información.

![alt text](/assets/img/posts/analisis-android-ios/image-27.png)

Podemos extraer información filtrando, completa, analizar las aplicaciones, información del dispositivo, etc.

Por ejemplo en el análisis de aplicaciones...

![alt text](/assets/img/posts/analisis-android-ios/image-28.png)

Tras unas cuentas preguntas sobre los datos del analista y el formato que queremos en la salida nos hará un informe sobre el contenido de la aplicación seleccionada.

![alt text](/assets/img/posts/analisis-android-ios/image-29.png)

En el reporte podemos observar los datos extraídos.

![alt text](/assets/img/posts/analisis-android-ios/image-30.png)

![alt text](/assets/img/posts/analisis-android-ios/image-31.png)

### Ejemplo de uso en iOS

Para IOS neesitaremos los drivers, damos en instalar.

![alt text](/assets/img/posts/analisis-android-ios/image-32.png)

Tras confirmar y confiar en el dispositivo, podremos ver la información del mismo igual que en Android.

![alt text](/assets/img/posts/analisis-android-ios/image-33.png)

En este caso IOS por defecto trae menos opciones que Android.

![alt text](/assets/img/posts/analisis-android-ios/image-34.png)

En iOS lo más recomendable es hacer un backup completo y luego interpretar los datos mediantes otras herramientas.

![alt text](/assets/img/posts/analisis-android-ios/image-35.png)

Igualmente podemos navegar por el contenido del dispositivo de forma manual.

![alt text](/assets/img/posts/analisis-android-ios/image-36.png)

## Avilla Forensics

Avilla Forensics es una herramienta de código abierto desarrollada por Daniel Avilla, con el objetivo de facilitar la extracción de datos de dispositivos Android. 

[Github Oficial](https://github.com/AvillaDaniel/AvillaForensics/releases/tag/3.8)

Una vez instalada encontraremos la aplicación en `C:\Forensics-3-8`

Ejecutada la aplicación nos encontramos ante una interfaz algo compleja pero muy completa.

![alt text](/assets/img/posts/analisis-android-ios/image-37.png)

Tenemos multitud de opciones para analizar el dispositivo.

#### Capturar pantalla

![alt text](/assets/img/posts/analisis-android-ios/image-38.png)

#### Explorar ficheros

![alt text](/assets/img/posts/analisis-android-ios/image-39.png)

#### Grabar y compartir pantalla

![alt text](/assets/img/posts/analisis-android-ios/image-40.png)

#### Datos y contenidos especiales del dispositivo

![alt text](/assets/img/posts/analisis-android-ios/image-41.png)

#### Otras opciones

- Backup ADB
- Extracción de datos según aplicación
- Extraer, desecndear y analizar datos de whatsapp
- Instalar y desinstalar aplicaciones
- Hacer downgrade de aplicaciones
- Obtener una copia completa del sistema de archivos
- etc...

### iOS

Para iOS también dispone de algunas opciones aunque algo más limitadas.

![alt text](/assets/img/posts/analisis-android-ios/image-42.png)



## Conclusiones y recomendaciones

Estas aplicaciones ofrecen un abanico de funcionalidades para analizar dispositivos Android y iOS y permiten obtener evidencias de los mismos.

Aunque no hemos explorado al 100% todas las funcionalidades de estas herramientas, nos han servido de ejemplo para entender cómo funcionan y cómo podemos utilizarlas para obtener evidencias de dispositivos Android y iOS.

En un entorno de investigación forense, es importante tener en cuenta que la información que obtengamos de estas herramientas puede ser utilizada para investigar y resolver casos de robos, robo de identidad, etc por lo que es fundamental e manejo de la información con cuidado así como la validez de los datos y, aunque estas herramientas son versátiles e importantes, existen mutitud de opciones (principalmente comerciales) que pueden ser utilizadas para obtener evidencias de dispositivos Android y iOS.

Tras una investigación exhaustiva de las soluciones disponibles podemos tener en cuenta la adquisición de las siguientes herramientas:

1. **MOBILedit Forensic Express**: Esta solución integral ofrece extracción de datos tanto físicos como lógicos, análisis avanzado de aplicaciones y recuperación de datos eliminados. Es compatible con una amplia gama de dispositivos, incluyendo teléfonos móviles y smartwatches. Además, cuenta con funciones de bypass de seguridad y generación de informes detallados, facilitando el proceso de análisis forense.

2. **Avilla Forensics**: Desarrollada por Daniel Avilla, esta herramienta gratuita se especializa en la extracción lógica de datos de dispositivos Android. Su módulo APK Downgrade permite la recopilación de datos de más de 15 aplicaciones sin necesidad de acceso root, lo que es esencial para investigaciones forenses. Además, se integra automáticamente con herramientas como IPED y Cellebrite Physical Analyzer, ampliando sus capacidades de análisis. citeturn0search2

3. **Cellebrite UFED**: Reconocida mundialmente, esta herramienta permite la extracción y análisis de datos de una amplia variedad de dispositivos móviles. Ofrece capacidades avanzadas para acceder a datos protegidos y recuperar información eliminada, siendo una opción preferida por agencias de aplicación de la ley.

4. **Magnet AXIOM**: Esta plataforma permite la adquisición y análisis de datos de múltiples fuentes, incluyendo dispositivos móviles, computadoras y servicios en la nube. Su capacidad para recuperar datos eliminados y analizar aplicaciones populares la convierte en una herramienta valiosa para investigaciones digitales.

5. **Oxygen Forensic Detective**: Ofrece una solución completa para la extracción, análisis y generación de informes de datos de dispositivos móviles. Es especialmente eficaz en el análisis de datos de aplicaciones y servicios en la nube, proporcionando una visión detallada de la actividad del usuario.

Además de esto hemos de tener en cuenta que no siempre será sencillo o 100% posible la obtención de evidencias de cualquier dispositivo móvil. Todo dependerá de la situación ya que no es lo mismo encontrarnos ante un peritaje donde el dispositivo se proporciona de forma voluntario y por tanto se tiene acceso a las claves/pin/contraseña del usuario, a un peritaje donde el usuario no aporta o ayuda de forma voluntaria (o a fallecido) y por tanto no tenemos acceso a estos pines/contraseñas.

Otra cosa a tener en cuenta es la marca del dispositivo ya que por ejemplo Samsung cuenta con software como KNOX que corre a nivel de firmware y encripta y separa ciertas particiones del sistema y otras características varias. Todo ha de tenerse en cuenta a la hora de analizar dispositivos móviles en general.

## Viabilidad de realizar un peritaje forense en Android.

En un peritaje sobre dispositivos Linux, Windows, Mac, etc... es usual tener en cuenta un volcado de RAM si el dispositivo se encontraba encendido, pero en Android/IOS no es así.

La complejidad de realizar un dump de memoria RAM en Android es muy alta, ya que no se suele contar con los headers/herramientas de compilación necesarias para por ejemplo utilizar herramientas como LIME, Volatility, etc... y todo ello incluso teniendo acceso root al dispositivo(en el mejor de los casos).

### ¿Cúal es la situación ideal que permitiría un perfecto análisis forense a un dispositivo Android?

Supone disponer, sin interferencias ni alteraciones, de:

-  **Clonado de la memoria interna**: Se tendría una imagen bit a bit (forense y sin alteración) del almacenamiento persistente del dispositivo. Esto implica capturar de forma íntegra todas las   particiones relevantes (por ejemplo, sistema, datos, recuperación, cache, etc.) sin comprometer la integridad de la evidencia. El proceso debería ejecutarse sin alterar el estado original del dispositivo y sin dependencias de métodos invasivos que puedan modificar los datos almacenados.

- **Volcado de la memoria volátil**: Se lograría una extracción completa y sin pérdida del contenido de la RAM en vivo, preservando toda la información transitoria (procesos en ejecución, conexiones de red, claves de cifrado, etc.). Esto es especialmente relevante porque la evidencia volatile se borra al apagar o reiniciar el dispositivo. La idealidad incluye el uso de herramientas como LiME configuradas de tal manera que puedan adquirir todas las áreas de memoria sin interrupciones ni errores (por ejemplo, sin que la eliminación de algún segmento crítico comprometa el análisis) .

- **Acceso sin restricciones**: El dispositivo debe estar en un estado en que se pueda interactuar con él sin trabas, es decir, con el bootloader desbloqueado, ADB habilitado (o algún otro método de comunicación) y sin que estén activos mecanismos de bloqueo que impidan el acceso a la memoria (como cifrado sin clave accesible, bloqueo de pantalla, OEM lock o protecciones específicas como Knox).

- **Disponibilidad de herramientas compatibles**: Debe existir soporte (en forma de fuentes del kernel, perfiles de Volatility y módulos de LiME) que permitan la adquisición completa y correcta tanto de la memoria interna como de la volátil sin necesidad de intervenciones que modifiquen el dispositivo.

- **No pérdida de RAM por reinicio**: La captura de la memoria volátil debe ocurrir sin reiniciar el sistema, de modo que se evite perder datos críticos, lo cual exige métodos de adquisición “en caliente” (live forensics) que sean plenamente fiables.

### Situación real en un dispositivo Android genérico y posibles soluciones

En dispositivos Android comerciales (como Samsung, Xiaomi, etc.), la realidad es muy distinta de la ideal por una serie de desafíos técnicos y legales:

- **Rooteo sin pérdida de datos**

  La mayoría de los métodos de rooteo requieren reiniciar el dispositivo o incluso desbloquear el bootloader, lo que necesariamente borra la memoria volátil. De hecho, para poder instalar y activar herramientas como LiME, se necesitan permisos de superusuario, los cuales suelen obtenerse mediante un proceso que implica un reinicio (o cambio de estado) del dispositivo. Existen métodos que buscan lograr un “root sin reinicio”, como el exploit “Rage Against The Cage” aplicado en algunos dispositivos. Sin embargo, estos métodos son muy específicos, dependen del modelo y versión del sistema, y en general no garantizan la preservación completa de la RAM.

- **Mecanismos de seguridad de Android**

Los dispositivos modernos incorporan múltiples barreras para impedir accesos no autorizados:

  - El bloqueo de pantalla (PIN, patrón, contraseña) y la desactivación por defecto del USB debugging dificultan la conexión y el control del dispositivo sin la intervención del usuario.
  - Características como el cifrado de los datos y la protección del cargador de arranque (OEM Lock) y, en algunos casos, soluciones propietarias como Knox en dispositivos Samsung, impiden o limitan modificaciones y accesos profundos que se necesitan para la adquisición forense.

  Como resultado, para poder acceder a la memoria volátil se requiere desactivar o sortear estas funciones, lo que en muchos casos involucra interacciones manuales o el uso de exploits – acciones que pueden alterar la evidencia o ser difíciles de defender en un contexto legal. Este riesgo se expone al tener que explotar vulnerabilidades para activar funcionalidades (por ejemplo, habilitar USB debugging sin la interacción del usuario) que son justamente medidas de protección de la plataforma.

- **Variabilidad del hardware y software**

  Cada dispositivo Android es una combinación única de hardware, particiones y configuración de kernel. Para poder utilizar herramientas de extracción (como LiME) y análisis (como Volatility), es indispensable contar con:

  - Un módulo de kernel (LKM) compatible, lo cual generalmente requiere disponer de las fuentes y la configuración exacta del kernel, y
  - Un perfil específico de Volatility para interpretar correctamente el volcado de RAM.

  Esta diversidad obliga a los investigadores a compilar de forma específica el módulo de adquisición y a generar un perfil de análisis adaptado a cada dispositivo. La imposibilidad de disponer siempre de las fuentes o la configuración correcta impide estandarizar el proceso y genera una gran carga de trabajo para cada caso, reduciendo la reproducibilidad y confiabilidad del análisis.

- **Limitaciones técnicas y legales**

Finalmente, aunque se logre realizar el volcado de memoria, el uso de herramientas como Volatility en entornos Android aún conlleva dificultades, debido a la enorme cantidad de variantes de kernel y la falta de soporte pleno comparado con sistemas Windows. Además, la utilización de métodos no estandarizados (como algunos exploits de rooteo) puede poner en duda la integridad de la evidencia. Cualquier alteración que se produzca durante el proceso de adquisición (por ejemplo, la pérdida de la memoria volátil al reiniciar el dispositivo) o la imposición de métodos no validados puede afectar la admisibilidad de la evidencia en un juicio, incrementando además los riesgos legales para el perito forense.

