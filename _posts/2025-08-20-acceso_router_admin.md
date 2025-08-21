---
title: ¿Tu router te está espiando? La verdad sobre TR-069 y la privacidad
date: 2025-08-20 11:00:00 +0000
categories: [Pentesting, firmware]
tags: [TR-069, privacy, router, penetration-testing]
image: 
    path: /assets/img/posts/acceso_router_admin/banner.jpg 
    alt:  cabecera
description: >
  ¿Sabías que tu proveedor de Internet puede acceder y configurar tu router sin que tú lo sepas? Esto es posible gracias al protocolo TR-069, también conocido como CPE WAN Management Protocol (CWMP). Aunque diseñado para facilitar la gestión remota de dispositivos, plantea serias preocupaciones sobre la privacidad y el control del usuario.

  El autor no se hace responsable de cualquier daño que puedan sufrir tus dispositivos o tu red o consecuencias legales de seguir este post.
pin: false  
toc: true   
math: false 
mermaid: false 
---

## ¿Qué es TR-069?

TR-069 es un estándar técnico que permite a los proveedores de servicios de Internet (ISP) gestionar y configurar remotamente los dispositivos del usuario final, como routers, módems y set-top boxes. A través de un servidor de configuración automática (ACS), el ISP puede:

- Configurar parámetros del dispositivo.
- Actualizar el firmware.
- Monitorear el rendimiento y estado del dispositivo.
- Realizar diagnósticos y solucionar problemas de forma remota.

Aunque estas funciones pueden mejorar la experiencia del usuario al facilitar la resolución de problemas y la actualización de dispositivos, también implican que el ISP tiene acceso a tu red doméstica.

---


## Implicaciones para la privacidad

El acceso remoto que ofrece TR-069 permite a los ISP obtener información detallada sobre tu red, incluyendo:

- Direcciones IP internas.
- Dispositivos conectados y sus configuraciones.
- Historial de actividad y uso de la red.

Aunque esta información puede ser utilizada para mejorar el servicio, también puede ser explotada con fines comerciales o incluso para vulnerar tu privacidad y no solo por el ISP sino cualquera con acceso a esos logs o servidores.



---

## ¿Qué sucede si desactivo TR-069?

Desactivar TR-069 en tu dispositivo puede limitar ciertas funcionalidades, como:

- Actualizaciones automáticas de firmware.
- Soporte remoto del ISP.
- Configuraciones automáticas de parámetros.

Sin embargo, esto también te otorga un mayor control sobre tu dispositivo y tu red, reduciendo el acceso remoto no deseado.

> Nota : Desactivar el acceso remoto puede ser mal visto por parte de tu ISP, lo que puede llevar a una tarifa más alta o incluso a la cancelación de tu servicio.
{: .prompt-warning}

---

Dicho esto vamos a lo que nos interesa que, principalmente (al menos en mi caso) es conseguir esas funcionalidades de administración extra que suelen ofrecer los routers pero que no están habilitadas por defecto ya que muchos ISP instalan configuraciones para evitar que los usuarios accedan a ellas.

---

## Desbloqueo de acceso elevado

### Dispositivo y acceso inicial

En este caso vamos a estar viendo un dispositivo de Huawei modelo EG8145V5.

![Router](/assets/img/posts/acceso_router_admin/imagens-produto-site-02-2.webp)

No vamos a compartir ni datos sobre el ISP ni el usuario en cuestión para evitar posibles violaciones de datos.

En función de la operadora estas modifican o no configuraciones en estos dispositivos, a veces puede que las credenciales de acceso al panel de administración sean las del dispositivo por defecto aunque en otras pueden cambiarse, como es este caso.

Aquí vamos a partir de que conocemos las credenciales del usuario normal de acceso, ya sean las que encontramos en la pegatina del dispositivo o las que nos hayan dado por parte del la operadora.

Para acceder al panel de administración normalmente basta con saber la IP del router que suele ser 192.168.x.1 y el puerto 80 que es el por defecto. El valor x puede variar dependiendo de la subred que configure el router por defecto. Si estamos conectados podemos escanear con nmap o hacer un simple arp -a para ver las IPs que están en nuestra red.

Si escaneamos con nmap veremos de forma más clara como tiene el puerto 80 abierto y quizá otros más.

![nmap](/assets/img/posts/acceso_router_admin/image.png)

---

### Investigando el panel de administración

En este post no vamos a explicar todo el proceso de reconocimiento por lo que vamos a ir directos en cada uno de los pasos, pero recomendamos encarecidamente que para este tipo de reconomientos utilicemos herramientas como Burp Suite, Zap, Caido, etc.

![panel-admin](/assets/img/posts/acceso_router_admin/image-1.png)

Una vez en el login podemos inciar sesión con las credenciales que tengamos disponibles. No os dejeis engañar si vuestro operador os da un nombre de usuario como `root`o `admin` ya que esto se cambia sin problema y no tiene nada que ver con los privilegios del usuario.

Una vez dentro para saber si nuestro usuario tiene o no todos os privilegios podemos simplemente buscar la opción para modificar los parametros WAN. 

#### ¿Qué son las WAN en un router?

En el firmware de tu router seguramente verás varias interfaces llamadas **WAN**. WAN significa **Wide Area Network** (Red de Área Amplia) y es el término que usamos para describir la conexión que tu router tiene hacia Internet o hacia otra red externa.

La WAN actúa como la “puerta de salida” de tu red doméstica o de oficina. Todo el tráfico que sale hacia Internet pasa por esta interfaz, mientras que el resto de tu red (LAN) permanece privada.

##### Tipos de conexión WAN
Los routers suelen soportar varios tipos de conexiones WAN según tu proveedor de Internet:

- **DHCP**: El router recibe automáticamente una IP pública del ISP.
- **PPPoE**: Requiere usuario y contraseña proporcionados por tu proveedor (muy común en ADSL o fibra).
- **IP estática**: Configuras manualmente una IP pública que te asigna tu ISP.
- **Trunk / VLAN**: Para conexiones de fibra óptica que usan etiquetas de VLAN para diferenciar servicios.

##### WAN y TR-069
En muchos routers, la WAN está directamente relacionada con TR-069. El servidor ACS del ISP utiliza esta interfaz para enviar configuraciones, actualizaciones de firmware y diagnosticar problemas de forma remota.

Es por esto que si nuestro operador ha sido inteligente, habrá deshabilitado la posibilidad de que el usuario pueda modificar estos parámetros o incluso verlos.

Todo esto es dependiente completamente del dispositivo y de la configuración del operador, por lo que es muy difícil de predecir.

![wan-info](/assets/img/posts/acceso_router_admin/image-2.png)

En este caso podemos ver pero datos básico y no podemos modificar nada.

![wan-config](/assets/img/posts/acceso_router_admin/image-3.png)

En la zona de configuración no vemos nada de las WAN, eso nos indica que no tenemos todos los privilegios disponibles en el panel de administración.

---

#### GPON vs EPON: Diferencias en tu router

Otra cosa que podemos observar es la versión del firmware de tu router.

Cuando revisamos el firmware, especialmente en redes de fibra óptica, es común encontrar opciones relacionadas con **GPON** y **EPON**. Ambos son estándares de tecnología de acceso de fibra, pero presentan diferencias clave:

##### 1. GPON (Gigabit Passive Optical Network)
- **Velocidad**: Hasta 2.488 Gbps de bajada y 1.244 Gbps de subida por puerto.
- **Eficiencia**: Usa multiplexación por división de tiempo (TDM) para enviar datos a múltiples usuarios.
- **Uso**: Muy común en proveedores de telecomunicaciones (ISP) que buscan entregar servicios de alta velocidad con calidad garantizada.
- **Ventaja**: Mejor eficiencia para transmisión de video y servicios convergentes (voz, video, datos).

##### 2. EPON (Ethernet Passive Optical Network)
- **Velocidad**: Normalmente hasta 1 Gbps simétrico (aunque existen variantes de 10G-EPON).
- **Eficiencia**: Basado en Ethernet, transmite tramas de datos directamente usando TDM o TDMA.
- **Uso**: Popular en redes metropolitanas y entornos donde la infraestructura Ethernet ya está presente.
- **Ventaja**: Fácil integración con redes Ethernet existentes y administración más simple.

##### 3. Diferencias clave
| Característica      | GPON                       | EPON                          |
|---------------------|----------------------------|-------------------------------|
| Estándar            | ITU-T G.984                | IEEE 802.3ah                  |
| Velocidad máxima    | 2.488 Gbps / 1.244 Gbps    | 1 Gbps simétrico (10G opc.)   |
| Transporte          | Frame TDM                  | Tramas Ethernet               |
| Uso principal       | ISP y triple play          | Redes metropolitanas, empresas|
| Costo del equipo    | Más alto                   | Generalmente más bajo         |

Esto es importante tenerlo en cuenta porque a veces pensamos que cambiar el firmware de nuestro router puede resolver problemas, pero no siempre es así. A parte de que podemos perder los datos de configuración para poder tener acceso a internet, también podemos encontrarnos con una situación incómoda con nuestra operadora e incluso perder el contrato y por ende el servicio.

![firmware](/assets/img/posts/acceso_router_admin/image-4.png)

---

## Vamos a la acción

En el caso de este dispotivo nos vamos a ir directamente a la parte donde podemos guardar la configuración del router.

![config-empty](/assets/img/posts/acceso_router_admin/image-5.png)

En este caso nos deja guardar o guardar y reiniciar. No nos sirve de nada ninguna de ellas, si acaso la de guardar.

Lo normal es que suelan dejar guardar los datos y descargar el archivo de configuración para poder tenerlo en un lugar seguro pero con este usuario no tenemos los privilegios necesarios para hacerlo.

O si. En este caso parece que los roles de los usuarios dentro del sistema del dispositivo lo único que hace es mostrar o no ciertos datos y dar posibilidad de modificarlos, por lo que si somos curiosos vemos que estamos ante un iframe que va haciendo llamadas a diferentes peticiones a scripts `.asp`.

---


#### Que son los scripts .asp?

`.asp` viene de Active Server Pages, una tecnología clásica de Microsoft para generar páginas web dinámicas.

En el caso de los routers, no suele ser un ASP “puro de Microsoft”, sino una implementación muy ligera adaptada al firmware. Funcionan como plantillas HTML + etiquetas especiales que el firmware interpreta para mostrar información dinámica.

El firmware tiene un mini-servidor web embebido (ej. Boa, GoAhead, mini_httpd).

Ese servidor carga los archivos .asp, que contienen código y variables que se rellenan dinámicamente desde la configuración interna del router.

Basicamente un sistema de plantilas HTML + etiquetas especiales que el firmware interpreta para mostrar información dinámica.


Usando esto a nuestro favor y sabiendo que pocas veces se hacen las cosas bien, es tan sencillo como revisar el codigo en las devtools del navegador.

### Si, solo es editar una etiqueta csl

![devtools](/assets/img/posts/acceso_router_admin/image-6.png)

Eliminamos el display none y tenemos las opciones que queremos completamente disponibles.

Si se diera el caso de que aun siendo visibles no funcionan, si nos fijamos también podemos ver la petición que realiza en el propio codigo.

![botones-visibles](/assets/img/posts/acceso_router_admin/image-7.png)

Descargamos el xml con la configuración del router y lo analizamos con un editor de texto.


## Entendiendo la configuración

En este archivo xml vamos a ver absolutamente toda la configuración actual del router, incluyendo los nombres de los usuarios, contraseñas, WAN, LAN, etc.

Hay muchos datos interesantes en el archivo pero no queremos hacer cosas que no deberíamos hacer, verdad? Por lo que vamos a revisar los datos que nos interesan.


Como nuestro objetivo es desbloquear el usuario con los permisos de administración mas elevados, simplemente buscamos la sección que diga algo como `user interface` o `web user interface`.

![users](/assets/img/posts/acceso_router_admin/image-8.png)

Vamos a encontrar en este caso los usuarios configurados y la contraseña anterior del mismo (para cuando dentro del panel pide la contraseña anterior). 

las contraseñas estan encriptadas hashes con salt, y el PassMode=3 indica probablemente un algoritmo seguro tipo SHA-256 o bcrypt e incluso con este no es reversible entonces quedaría la posibilidad de crackear la contraseña mediante fuerza bruta con diccionario y no es rentable.

Pensando en ser más eficiente... y si sencillamente modificamos la contraseña y cargamos el archivo nuevamente? 

![passmode](/assets/img/posts/acceso_router_admin/image-9.png)

Vamos a modificar el parámetro `PassMode` a `0` lo que hace que la contraseña se pueda escribir en texto plano y no se encripte. Podemos también cambiar el valor Userlevel del usuario que tenemos a `0` para que sea administrador y poder acceder a todas las opciones del panel de administración o podemos cambiar la contraseña del usuario `telecomadmin` de igual forma.

En el caso actual es indiferente lo que hagamos porque todo lo que implique la modificación del usuario telecomadmin o el userlevel del usuario root será revertido al valor original gracias al TR-069.

### Modificando la administración ACS

Esto es sencillo de evitar, es no permitir que nuestro dispositivo sea administrado de forma remota por el ACS del ISP.

Buscamos la línea donde diga algo parecido a `ManagementServer` y desactivamos el reporte de estado y desabilitamos el acceso remoto.

![management](/assets/img/posts/acceso_router_admin/image-10.png)

Como vemos tenemos la dirección del servidor ACS, el puerto, nombre de usuario y contraseña. Solo lo vamos a desactivar.

También podemos hacer que ni siquiera se autentique en el WAN (`enable = 0`) aunque teniendo deshabilitado el acceso remoto, el servidor no podría resetear la configuración del router.

![WAN](/assets/img/posts/acceso_router_admin/image-11.png)

### Activando acceso por SSH/Telnet

Si el dispositivo tiene SSH o Telnet activado, podemos hacer que este sea accesible desde este archivo, pero teniendo cuidado ya que podemos activarlo para que sea accesible desde internet y nadie quiere eso.

![SSH](/assets/img/posts/acceso_router_admin/image-12.png)

Debemos habilitar los puertos en algunas opciones más pero esto ya depende de cada dispositivo. Lo curioso es que estas opciones de habilitar Telnet o SSH no salen en ninguna opción dentro del panel de administración incluso con los privilegios más elevados.

### Acceso por SSH 

Llegados a este punto ya hemos accedido al panel con todas las opciones (o la gran mayoría) disponibles dentro del router, como por ejemplo establecer nuestra propia dirección DNS, crear VLANs, modificar parámetros WAN, captura de tráfico, etc. Esto depende completamente del dispositvo.

Pero vamos a llegar hasta el final, acceso por SSH. 

Tras modificar algunos parámetros que solo parecen estar visibles en el archivo pero no en la interfaz, hemos conseguido habilitar el acceso por SSH. 

Aquí hay dos cosas importantes en el caso de este dispositivo:

- Tenemos que deshabilitar el firewall para que el SSH funcione.
- En la parte de usuario encontramos uno llamado cli-user, en este caso es root. Debemos simplemente cambiar el hash de la contraseña que tiene actualmente y sustituirlo por el hash que tenemos en nuestro usuario normal cuya contraseña ya sabemos y su salt, importante.

![cli-user](/assets/img/posts/acceso_router_admin/image-13.png)

Tras subir la configuración de nuevo vemos que el firewall está deshabilitado y el SSH está habilitado.

![ssh](/assets/img/posts/acceso_router_admin/image-14.png)

Como se ve, el comando es:

```bash
ssh -oHostKeyAlgorithms=+ssh-rsa -oPubkeyAcceptedKeyTypes=+ssh-rsa root1@192.168.100.1
```

Esto se debe a que el sistema utiliza un tipo de clave ssh-rsa antigua que los clientes actuales no soportan pero que podemos forzar a utilizar con el parámetro -oHostKeyAlgorithms=+ssh-rsa.

Una vez dentro vemos de primeras que no tenemos una terminal normal sino propietaria... nos toca explorar un poco más.


## Dentro del router

![comandos](/assets/img/posts/acceso_router_admin/image-15.png)

Lo que encontramos es un CLI modificado, no deja de ser un linux pero han modificado ciertas llamdas, en este caso ls o ps pasan a ser llamados como wap list o wap ps.

Si mandamos el comando ? o help, vemos una lista de comandos disponibles.

- *ifconfig* → muestra interfaces de red (clásico de Linux).

- *netstat -na* → conexiones abiertas.

- *ping*, *traceroute*, *nslookup* → pruebas de red.

- *display current-configuration* → probablemente te suelte TODO el config activo (como el config.xml).

- *set userpasswd* → cambiar contraseñas de usuarios del sistema.

- *su* → eleva los privilegios a superusuario wap

- *session cli* → suena a que abre otra sesión dentro del sistema.

- *load ssh-pubkey* → parece que permite cargar claves públicas (interesante para acceso SSH persistente).

- *wap ps* y *wap top* → muestran procesos corriendo, lo cual indica que sí estamos encima de un Linux embebido.

- *shell* → nos abre una shell de comandos.


Ejecutamos `shell` lo que significa que estamos en un shell BusyBox embebido sobre Dopra Linux (Huawei/HG-series suelen llevar este fork de Linux).

En este punto deberíamos tener una shell busybox completa pero en este caso concreto parece que ha sido modificada únicamente para ejecutar un archivo.


## Disclaimer

El autor no se hace responsable de cualquier daño que puedan sufrir tus dispositivos o tu red o consecuencias legales de seguir este post.