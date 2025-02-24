---
title: Protocolo Kerberos en Active Directory
date: 2025-02-23 11:00:00 +0000
categories: [Teoría, Active Directory]
tags: [Guía, Auditoria, Active Directory, Windows, Kerberos, NTLM, Hash, Pass-the-Hash, Pass-the-Ticket, AS-REP Roasting, Golden Ticket, Silver Ticket, Silver Ticket]
description: >
  Funcionamiento de Kerberos en Active Directory
pin: false  
toc: true   
math: false 
mermaid: false 
---

## ¿QUÉ ES KERBEROS?

Se trata de un protocolo de autenticación desarrollado originalmente en el MIT en 1983 para el proyecto ATHENA cuyos objetivos incluían la integración de:

- SSO (Single sign-on)
- Soporte para sistemas de archivos en red
- Entorno gráfico unificado (X Windows)
- Servicio de convención de nombres (como DNS)

## KERBEROS Y MICROSOFT WINDOWS

En este sistema la autenticación de usuarios y hosts basada en dominio se realiza a través de Kerberos.

Kerberos v5 (RFC1510) se implementó en windows server 2000 y sustituyó a NTLM (Windows NT LAN Manager) como opción de autenticación por defecto.

Actualmente NTLM se sigue utilizando como mecanismo de autenticación a nivel local de la máquina (no unidos a un domino).

Este protocolo Kerberos es el más antiguo y de uso común en la actualidad.

En la web del MIT podemos encontrar un diálogo entre dos personas Athena y Eurípides escrita por las personas que diseñaron este protocolo en el que discuten cómo ponerle solución a un problema siendo la solución final el protocolo Kerberos.

[Diálogo](http://web.mit.edu/kerberos/www/dialogue.html)

## ¿CÓMO FUNCIONA KERBEROS?

El usuario manda un paquete plano con su **USUARIO** al servicio de autenticación normalmente acompañado de otro paquete con un **timestap** cifrado con la clave del usuario,

El servicio de autenticación comprueba si existe el usuario, si es así coge su **password** de la base de datos, genera una nueva clave de sesión y coge también la clave del **ticket Granting ticket service**.

`TICKET GRANTING TIKET -  {sessionkey:username:address:servicename:lifespan:timestamp}`

Cifra esta cadena de texto con la clave del **ticket Granting ticket service**, una clave privada del propio servicio que el usuario no conoce. Además, simultáneamente crea otro paquete adicional con **SessionKey1**, lo cifra con la clave privada del usuario y todo esto lo envía al **usuario**.

El usuario recibe la información, desencripta el paquete con su clave privada. Ahora tiene la clave de sesión, el **ticket granting ticket** encriptado por la clave privada del **ticket Granting ticket service** y su clave privada personal.

El usuario usa el **ticket granting ticket** para interactuar con el **ticket Granting ticket service** pero para que no pueda ser interceptado sin más primero se crea un *Autenticator*

`AUTHENTICATOR - {username:address} encrypted with session key}`

Y esto lo cifra con la **SessionKey1**.

Esto previene que, si alguien intercepta el **ticket granting ticket** no pueda interactuar con el **ticket Granting ticket service** porque no podría componer el *Autenticator*, ya que para esto se necesita la *SessionKey* que iba anteriormente incluida en un paquete cifrado con la clave personal del usuario.

Ahora el usuario envía al **ticket Granting ticket service** el *Autenticator* cifrado y el *ticket granting ticket*.

El **ticket Granting ticket service** utiliza su **clave privada de servicio** para descifrar el **ticket granting ticket**, conseguir la *SessionKey* y así descifrar el *Autenticator*, comprueba que el usuario que aparece en el **ticket granting ticket** es el mismo que el del *Autenticator* coinciden y si es así pasa la validación. 

Ahora el **ticket Granting ticket service** crea un **ticket de servicio para el sistema de ficheros**. Para ello crea una nueva *SessionKey2* que incluye en el **ticket de servicio ficheros** y este lo cifra con la **clave privada del servicio de ficheros.**.

Esta nueva *SessionKey2* la mete en otro paquete y lo cifra con la *SessionKey1* que obtuvo del ticket granting ticket y que el usuario ya tiene.

Envía pues el **ticket de servicio para el sistema de ficheros** y el paquete *SessionKey2* cifrado al usuario.

El usuario descifra la *SessionKey2* con la *SessionKey1*, crea un nuevo *Autenticator 2* e igual que antes lo cifra con la *SessionKey2* que acaba de obtener. 

Envia el *Autenticator 2*  y el **ticket de servicio para el sistema de ficheros** a el **servicio de ficheros**.

El **servicio de ficheros** descifra el **ticket de servicio para el sistema de ficheros** en el que está contenida la *SessionKey2* con la que a su vez descifra el *Autenticator 2*, compara la información del **ticket** con la del *Autenticator 2* y si coinciden puede validar el usuario.

Ahora si le envía los datos correspondientes al usuario.

A todo esto se le añade un paso adicional en la comunicación con el sistema de archivos ya que el servicio puede autenticar al usuario pero el usuario no puede autenticar a el servicio por lo que puede ser suplantado por un servicio falso.

En la **autenticación** mutua:

- El usuario antes de mandar el comando para obtener el fichero del servicio, únicamente manda el *Autenticator 2*  y el **ticket de servicio para el sistema de ficheros**. 

- El servicio realiza todo el proceso anterior, autentica a el usuario y procede a autenticarse a si mismo. Crea un paquete con un **timestamp**, lo cifra con la *SessionKey2* (ya que si fuese un servicio falso no podría haber obtenido esa clave) y lo envía al usuario.

- El usuario descifra el paquete con el **timestamp** y si lo hace correctamente este verifica que el **servicio es el auténtico** y no un suplantador, ahora si le envía el comando para realizar uso del servicio.

- Todo esto es necesario de saber porque se pueden realizar ataques a ciertos pasos y aprovechar para obtener ciertos datos, explotar el uso de los tickets, utilizarlos en nombre de otros usuarios, etc...

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image.png)

## ¿CÓMO SE IMPLEMENTA ESTE PROTOCOLO EN ACTIVE DIRECTORY?

Durante el proceso de autenticación de Kerberos se utilizan ciertos nombres que están asociados con AD.

A la hora de arrancar nuestra máquina WS01,WS02,... cualquiera dentro del dominio, en el prompt del login inicial es donde comienza todo este proceso y donde el usuario consigue su **TicketGrantingTicket(TGT)**.

Abrimos Wireshark y lo ponemos a capturar en la red privada del domino.

Iniciamos sesión en el WS01

En wireshark filtramos por Kerberos y vemos:

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-1.png)

Este primer paquete envía el usuario para pedir el servicio de autenticación (Autentication service request).

Si desplegamos los datos del paquete vemos que envía el nombre del usuario y los servicios que está solicitando

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-2.png)

Todos los servicios de ActiveDirectory vienen identificados por el Service Principal Name (SPN).

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-3.png)

Si nos fijamos el siguiente paquete es un error por parte del servicio de autenticación que indica la necesidad de una pre-autenticación y esto es porque en la nueva implementación de Kerberos v5 se añadió la comprobación de usuario necesitando un TimeStamp cifrado con el password del usuario.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-4.png)

El usuario manda otra petición pero esta vez con un timestamp cifrado.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-5.png)

El servicio responde con un paquete Autentication service replay (AS-REP)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-6.png)

En su contenido vemos que adjunta el ticket que veíamos previamente y otro dato encriptado que se trata de sessionkey cifrada con el password del usuario.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-7.png)

Esta información se descifra en el usuario y el usuario envía un paquete TGS-REQ (ticket granting service request)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-8.png)

Como veíamos antes esto contiene el TGT que recibió antes y un autenticator

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-9.png)

Del servicio recibimos un TGS-REP (ticket granting service replay)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-10.png)

Este paquete contiene el ticket de servicio con el nombre del mismo y el equipo desde el que solicita y unos datos cifrados que son la SessionKey para luego interactuar con el servicio del host.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-11.png)

Si nos fijamos el usuario hace otra petición para un nuevo ticket para el servicio de LDAP en el host del controlador del dominio.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-12.png)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-13.png)

El servicio responde con el nuevo ticket

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-14.png)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-15.png)

A partir de aqui se observa el tráfico con los servicios que ya se están solicitando del host

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-16.png)

En el primer paquete vemos 

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-17.png)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-18.png)

Le envía el ticket de servicio para LDAP y el autenticator.

El servicio envía un paquete de autenticación mutua.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-19.png)

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-20.png)

Que si recordamos son datos como un timestamp cifrados con la sessionkey que el usuario ya posee.

## Lo importante a tener en cuenta

Todo esto se lleva a cabo por un usuario en el controlador de dominio. Este está creado por defecto y se llama krbtgt.

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-21.png)

El KDC o KeyDistributionCenter engloba a los servicios de authentication y el ticket gratnting service. 

Este usuario es el que se encarga de cifrar estos paquetes y tickets porque la clave de este usuario se trata de la clave del TGS.

La clave por defecto de este usuario es muy larga y compleja por lo que obviamente no se debería cambiar nunca a algo muy sencillo de crackear.

Si queremos ver el ServicePrincipalNames SPN, se puede observar qué servicios ofrece cada ordenador de la infraestructura y que SPN tiene asociados.

```powershell
Get-NetComputer -Identity WS01
```

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-22.png)

```powershell
Get-NetComputer -Identity DC01
```

![alt text](/assets/img/posts/teoria-protocolo-kerberos/image-23.png)
