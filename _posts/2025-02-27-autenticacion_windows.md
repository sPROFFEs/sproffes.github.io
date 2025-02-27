---
title: Autenticación y autorización en Windows
date: 2025-02-27 11:00:00 +0000
categories: [Teoría, Active Directory, Windows]
tags: [Guía, Auditoria, Active Directory, Windows, Kerberos, NTLM, Hash, Pass-the-Hash, Pass-the-Ticket, AS-REP Roasting, Golden Ticket, Silver Ticket, Silver Ticket]
description: >
  TÉCNICAS COMO SUPLANTACIÓN DE USUARIOS, MOVIMIENTOS LATERALES, ETC
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Esquema de autenticación

![alt text](/assets/img/posts/autenticacion_windows/34-1.png)

Este esquema representa el proceso de autenticación del sistema que se realiza en windows. 

Cuando se intenta autenticar como un usuario tenemos nuestra interfaz en la que introducimos nuestras credenciales.
Este proceso se comunica con el LocalSecurityAutority que recibe las credenciales y el paquete de autenticación a utilizar. 

Si nos encontramos en una infraestructura de dominio el paquete será *kerberos* pero a nivel local el paquete será *NTLM*, por tanto el **LSA** llamará a la librería correspondiente.
A nivel local el sistema comprueba las credenciales contra una base de datos local manejada por el **SAM**.

Si en nuestra máquina queremos iniciar sesión con un usuario a nivel local, seleccionamos otro usuario e indicamos que el usuario está registrado a nivel local del la siguiente manera:

![alt text](/assets/img/posts/autenticacion_windows/34-2.png)

## LSA Logon Sessions

Cuando un usuario se autentica correctamente, el paquete de autenticación (*kerberos.dll o ntlm.dll*) crea una **logon session** y devuelve información a la autoridad local **LSA**

El módulo **LSA** usa esta información para crear un *Access Token* en el que se incluye un identificador local único (**LUID**) para la logon session que se denomina como un identificador de inicio de sesión (**SID**).

[Documentación Microsoft](https://learn.microsoft.com/en-us/windows-server/security/windows-authentication/credentials-processes-in-windows-authentication#BKMK_CrentialInputForUserLogon)

## Interactive Authentication

La autenticación es interactiva cuando se solicita al usuario que proporcione información de inicio de sesión como con un UI.

La **LSA** realiza una autenticación interactiva cuando un usuario inicia sesión a traves de la interfaz de usuario *GINA*.
Si se realiza de manera correcta la autenticación, comienza la *logon session* del usuario y se **guarda** un conjunto de **credenciales** de inicio de sesión para futuras referencias. Esto se guarda en el módulo **LSA** para implementar el *SingleSignON*

[Documentación Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthn/interactive-authentication)

## Non interactive Authentication

Al no ser interactiva solo se puede usar después de que se haya realizado una autenticación interactiva, es decir; es posterior.

El usuario no introduce ningun tipo de dato de inicio de sesión; en su lugar se usan las credenciales **establecidas** y **almacenadas** en el módulo **LSA** previamente.
Esto se utiliza para consumir servicios en red y conectar máquinas sin tener que volver a introducir credenciales.

[Documentación Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthn/noninteractive-authentication)



De forma práctica podemos ver esto en nuestra WS01 ya que como tenemos una sesión iniciada de forma local, hemos pasado esa autenticación interactiva y ahora podemos ver esa logon session y el access token asociados.

Microsoft ofrece una serie de herramientas de administración entre las que se encuentra una para visualizar las Loggonsessions.

[LogonSessions](https://learn.microsoft.com/en-us/sysinternals/downloads/logonsessions)

Para esta herramienta se necesitan privilegios de administración, como este usuario es a nivel local, se encuentra dentro del grupo administradores porque es el que se creó inicialmente con la máquina.

![alt text](/assets/img/posts/autenticacion_windows/34-5.png)

![alt text](/assets/img/posts/autenticacion_windows/34-6.png)

En una powershell como administrador:

![alt text](/assets/img/posts/autenticacion_windows/34-8.png)

![alt text](/assets/img/posts/autenticacion_windows/34-9.png)

Si nos fijamos este usuario local tiene dos **LogonSession** creadas al mismo tiempo, ya que van asociadas a un *AccessToken*. Lo normal al autenticarse se crean dos sesiones para ese usuario, una con los privilegios que tiene el usuario y otra con privilegios elevados ya que al iniciar el sistema algunos servicios necesitan de estos para ser ejecutados.

```powershell
.\logonsessions.exe -p
```

Si ejecutamos ese parámetro veremos los procesos que hay asociados a cada una de esas LogonSessions.

![alt text](/assets/img/posts/autenticacion_windows/34-10.png)

Esta sesion ejecuta los procesos que necesitan de privilegios elevados.

![alt text](/assets/img/posts/autenticacion_windows/34-11.png)

Esta otra los demas procesos que no son necesarios de privilegios elevados.


Hemos visto antes estas dos sesiones tienen un token de acceso o AccessToken que les permite autorizar el acceso a diferentes objetos.

Vamos a ver una cosa curiosa, vamos a iniciar sesión de nuevo en un usuario de dominio.

Iniciamos un powershell como administrador del dominio.

![alt text](/assets/img/posts/autenticacion_windows/34-12.png)

Ejecutamos loggonsessions.exe

![alt text](/assets/img/posts/autenticacion_windows/34-13.png)

Si nos fijamos en las dos últimas sesiones.

![alt text](/assets/img/posts/autenticacion_windows/34-14.png)

Son las dos sesiones que acabamos de crear, la de *empleado1* de forma interactiva y la de *administrador* de forma interactiva pero se observa que es otro tipo de interacción debido a que ha sido un prompt de ejecución de permisos y no un inicio de sesión como el de *empleado1*. Como igualmente hemos interactuado, ya que hemos introducido las credenciales de administrador es interactivo. 

Ahora bien, si vamos al DC01 y accedemos desde un powershell a el disco de WS01.

![alt text](/assets/img/posts/autenticacion_windows/34-15.png)

Hemos solicitado sus archivos pero no nos hemos autenticado por lo que si vemos de nuevo las **logon sessions** en WS01.

![alt text](/assets/img/posts/autenticacion_windows/34-16.png)

En último lugar veremos un acceso de administrador al equipo pero su tipo de inicio ha sido network y no interactivo.
Esto es importante porque cuando tenemos un logon interactivo en algún lugar de la memoria RAM, las credenciales de los usuarios que han interactuado se encuentran almacenadas como pueden ser *empleado1* o *administrador*, al iniciar el powershell ambas credenciales han quedado almacenadas en el **LSA**.

Sin embargo en las sesiones de network o red no se almacenan las credenciales en la RAM o **LSA** del equipo.

## Access Tokens

Cuando un usuario inicia sesión, el sistema comprueba la contaseña con la base de datos de seguridad. Si se autentica correctamente, el sistema genera un *AccessToken* y cada proceso ejecutado en nombre de ese usuario tiene una **copia** de ese **token de acceso**.

Un **token de acceso** es en si un objeto que describe el contexto de seguridad de un proceso o subproceso, donde se incluye la identidad y los privilegios de la cuenta de usuario asociada con el proceso.

El sistema usa un token para identificar el usuario cuando un subproceso interactúa con un *securable object* o intenta realizar una tarea del sistema que requiere privilegios.

Cada proceso tiene un token principal asociado que describe el contexto de seguridad asociado al proceso. De forma predeterminada el sistema usa el token principal cuando un *subproceso* del *proceso* interactúa con un *securable object*, además un subproceso puede suplantar una cuenta de cliente lo que permite que el subproceso interactúe con el securable object mediante el contexto de seguridad del cliente.

Este subproceso que suplanta a un cliente tiene un token principal y un token de suplantación.

Por tanto de todo esto sacamos que existen dos tipos de tokens:

- **Principal**: el que tiene por defecto el proceso y todo subproceso (a no ser que se esté suplantando)

- **Suplantación**: que suplanta al usuario y que suele utilizar en arquitecturas cliente-servidor.

[Documentación Microsoft](https://learn.microsoft.com/en-us/windows/win32/secauthz/access-tokens)


Volviendo a nuestra estación de trabajo vamos a utilizar [ProccessExplorer](https://learn.microsoft.com/en-us/sysinternals/downloads/process-explorer) para ver los procesos que se están ejecutando en nuestra máquina.

Abrimos un powershell como adminstrador y otro como empleado1 y con el processexplorer vemos dos procesos powershell.

![alt text](/assets/img/posts/autenticacion_windows/34-17.png)

![alt text](/assets/img/posts/autenticacion_windows/34-18.png)

Aquí observamos las diferencias de privilegios, las diferentes logonsessions que usan y los usuarios relacionados con estos procesos.

Estos tokens de acceso son los que validan cuando la ejecución puede o no puede hacer algo según sus privilegios.

