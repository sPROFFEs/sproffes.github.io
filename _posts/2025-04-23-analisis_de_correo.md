---
title: Análisis forense de correos electrónicos
date: 2025-04-23 11:00:00 +0000
categories: [Forense, Correo electrónico]
tags: [SMTP, IMAP, POP3]
image:
  path: /assets/img/posts/analisis-correo-electronico/cabecera.png
  alt:  cabecera
description: >
  Ejemplo de analisis de correo electrónico
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Contexto

El correo electrónico es uno de los métodos de comunicación más comunes en la actualidad, aunque las redes sociales están ganando terreno, especialmente en comunicaciones privadas. A pesar de esto, las empresas siguen utilizando el correo electrónico para interactuar con clientes actuales, futuros y pasados, ofreciendo soporte, servicio al cliente y actualizaciones sobre productos o políticas. Además, se usa para iniciar tickets de problemas en aplicaciones de asistencia y para alertas administrativas de sistemas.

Sin embargo, el correo electrónico no fue diseñado con la seguridad en mente, lo que lo convierte en un medio vulnerable.

Originalmente creado para enviar mensajes de texto entre máquinas y redes simples, el diseño permite que personas malintencionadas redirijan o modifiquen los correos electrónicos. Además, cualquiera con acceso a redes u ordenadores donde se procesan los correos electrónicos puede leerlos, ya que no existe un mecanismo integrado para garantizar la confidencialidad (como el cifrado), ni para verificar la integridad o el remitente del correo.

El problema radica en que el correo electrónico no tiene métodos de verificación de identidad del remitente, lo que facilita el envío de correos fraudulentos con direcciones falsas. Aunque algunos proveedores intentan mitigar este problema con configuraciones especiales, muchas plataformas no cuentan con estas medidas.

Además, el texto del correo electrónico se transmite de forma clara, lo que significa que puede ser fácilmente interceptado por herramientas de monitoreo de red.

A pesar de estas vulnerabilidades, existen herramientas disponibles que pueden mejorar la seguridad del correo electrónico, como métodos de cifrado y autenticación. El objetivo es tomar conciencia de los riesgos asociados con el uso del correo electrónico y aprender a estudiar las evidencias forenses en las cabeceras de los correos electrónicos para detectar posibles fraudes o alteraciones.

Para ello, se recomienda utilizar herramientas como Webmail, clientes de correo como Thunderbird y Outlook, y herramientas online especializadas.

## Análsis de cabeceras y validación de DKIM

Para poder visualizar un correo electrónico en texto plano depende de nuestra aplicación, en este caso Gmail.

![alt text](/assets/img/posts/analisis-correo-electronico/image.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-1.png)

La información se podría interpretar de forma manual aunque al estar en texto es algo difícil de leer. Para esto, se utilizan herramientas de análisis forense como [Google Admin Toolbox](https://toolbox.googleapps.com/apps/messageheader/analyzeheader).

Esta herramienta nos permite visualizar de forma más clara y ordenada la información del correo electrónico.

![alt text](/assets/img/posts/analisis-correo-electronico/image-2.png)

### Análisis de las cabeceras

1. **Delivered-To**: 
   - Indica la dirección de correo electrónico a la que se entregó el mensaje. En este caso, el correo fue entregado a **XXXXXX@gmail.com**.

2. **Received**:
   - Muestra la información sobre los servidores que han procesado el correo electrónico. Es útil para rastrear el camino del mensaje a través de diferentes servidores. Cada entrada "Received" representa un salto entre servidores.
   - Por ejemplo, uno de los servidores indica que el mensaje fue recibido por **2002:a05:622a:188c** con el identificador SMTP **v12csp224888qtc** y la fecha y hora en que se recibió.

3. **X-Forwarded-Encrypted**:
   - Este campo muestra información sobre el estado de cifrado de los correos. En este caso, la dirección encriptada está asociada a una versión segura del correo, indicando que la información fue cifrada antes de ser transmitida.

4. **ARC-Seal** y **ARC-Message-Signature**:
   - Estas son firmas que ayudan a verificar que el mensaje no ha sido alterado durante su tránsito a través de múltiples servidores.
   - **ARC-Seal** garantiza que el mensaje pasó por una autenticación en un servidor y no ha sido modificado.
   - **ARC-Message-Signature** es una firma que verifica la integridad del mensaje en su totalidad.

5. **ARC-Authentication-Results**:
   - Este campo muestra los resultados de las verificaciones de seguridad, como **DKIM** (DomainKeys Identified Mail), **SPF** (Sender Policy Framework) y **DMARC**. Estos son mecanismos utilizados para verificar la autenticidad del remitente y prevenir el fraude:
     - **DKIM**: Verifica que el contenido del correo no haya sido alterado.
     - **SPF**: Verifica si el correo proviene de una dirección IP autorizada.
     - **DMARC**: Combinación de DKIM y SPF para asegurar que el mensaje proviene de un dominio legítimo.

6. **Return-Path**:
   - Indica la dirección a la que deben enviarse las respuestas o los rebotes (errores) del mensaje, en este caso **xxxxx@axxxxxxada.com**.

7. **DKIM-Signature**:
   - Es una firma digital que asegura que el contenido del mensaje proviene realmente del dominio **xxxxxxxx.com** y que no ha sido alterado.

8. **X-Google-DKIM-Signature**:
   - Es una firma similar a **DKIM-Signature**, pero específica de Google, que también asegura la autenticidad del mensaje enviado a través de los servidores de Google.

9. **X-Received**:
   - Similar a **Received**, pero en este caso se incluye el identificador único del servidor y la fecha exacta en la que se procesó el mensaje.

10. **MIME-Version**:
    - Especifica la versión del formato de correo electrónico. En este caso, la versión es **1.0**, lo que indica que el correo usa el estándar MIME (Multipurpose Internet Mail Extensions) para soportar contenidos no textuales, como archivos adjuntos o formatos especiales.

11. **From**:
    - Muestra quién envió el correo electrónico. En este caso, el correo proviene de **XXX xxxxx <XXXXX@aXXXXXda.com>**.

12. **Date**:
    - Es la fecha y hora en que el correo fue enviado. En este caso, el correo fue enviado el **7 de febrero de 2025 a las 13:26:36 (hora +0100)**.

13. **Message-ID**:
    - Es un identificador único asignado al correo electrónico para distinguirlo de otros mensajes. En este caso, el ID es **<CAP0rW9cv7-YH=r2f0JzsgbvPhPrRmULF5WT9z_r0JMhaZaCS6w@mail.gmail.com>**.

14. **Subject**:
    - El asunto del correo electrónico, que en este caso es **"Certificado disponible + Encuesta de satisfacción y vídeo resumen"**.

15. **To** y **Bcc**:
    - **To** (Para): Muestra a quién fue enviado el correo. En este caso, es a **undisclosed-recipients** (sin destinatarios visibles).
    - **Bcc** (Copia oculta): En este caso, el destinatario oculto es **xxxxxxxx@gmail.com**.

16. **Content-Type**:
    - Indica el tipo de contenido del correo. En este caso, el correo es **multipart/related**, lo que significa que contiene múltiples partes, como texto y archivos adjuntos, que están relacionados entre sí.

Estas cabeceras ayudan a realizar una auditoría y análisis forense del correo electrónico para verificar su autenticidad, detectar posibles fraudes y rastrear el origen del mensaje. También son útiles para asegurarse de que el correo ha sido entregado de forma segura y sin modificaciones maliciosas.

### Comprobar validez del DKIM

Para verificar el **DKIM** (DomainKeys Identified Mail), necesitamos identificar dos componentes clave: el selector y el dominio. Estos se encuentran en la cabecera DKIM-Signature.

1. **Dominio**: Se encuentra en el campo `d=`, que en este caso es:
   ```
   d=xxxxxxxx.com
   ```
   - Este es el dominio que ha firmado el correo.

2. **Selector**: Se encuentra en el campo `s=`, que en este caso es:
   ```
   s=google
   ```
   - Este es el selector utilizado para la firma DKIM, que generalmente corresponde a un registro específico en el DNS del dominio que contiene la clave pública.

#### Cómo verificar el DKIM:

1. **Accedemos al DNS del dominio** `xxxxxxx.com`.
2. Buscamos un **registro TXT** para el selector `google`.

    El registro TXT debería tener la siguiente forma:

    google._domainkey.XXXXXX.com

3. Verifica que el registro TXT contenga la clave pública correspondiente para comprobar la firma DKIM. Esto se utiliza para validar que el correo electrónico no ha sido modificado y que realmente proviene del dominio legítimo. 

Podemos buscarlo de forma manual con herramientas como DomainDossier o NsLookup.

![alt text](/assets/img/posts/analisis-correo-electronico/image-3.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-4.png)

Y buscamos directamente el contenido.

![alt text](/assets/img/posts/analisis-correo-electronico/image-7.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-5.png)

O podemos usar herramientas como [DKIM Validator](https://dkimcore.org/tools/)

![alt text](/assets/img/posts/analisis-correo-electronico/image-6.png)

## Simulación de un spoofing

Podemos simular un correo malicioso que se hace pasar por otro dominio para ver como se comportan las validaciones de DKIM, etc.

Utilizando [Emkei`s Fake Mailer](https://emkei.cz/) y [Yopmail](https://yopmail.com/) hacemos la prueba.

![alt text](/assets/img/posts/analisis-correo-electronico/image-8.png)

Como vemos ya nos indica que google no parece ser el dominio desde el que se envía el correo pero podemos comprobar el contenido del correo completo.

![alt text](/assets/img/posts/analisis-correo-electronico/image-9.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-10.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-11.png)

También podemos analizar el contenido con [DKIM Validator](https://dkimvalidator.com/)

![alt text](/assets/img/posts/analisis-correo-electronico/image-12.png)

Si probamos a enviar estos correos de spoofing a proveedores oficiales tienen filtros muy estrictos de autenticación para evitar este tipo de ataques.

Si analizamos la imagen veremos lo siguiente:

**SPF: SoftFail**
El SPF (Sender Policy Framework) indica **qué servidores están autorizados a enviar correos en nombre de un dominio**. En tu caso:

- **From (aparente)**: `gmail.com`
- **Tu IP de envío**: `114.29.236.247` (emkei.cz)
- **Resultado SPF**: `SoftFail`

Eso significa: *“la IP **no** está en la lista de servidores permitidos para enviar correos desde gmail.com, pero el dominio no solicita un rechazo directo (solo marca como sospechoso).”*

Esto **no bloquea el correo automáticamente**, pero sí lo marca como **sospechoso** y ayuda a otros mecanismos a tomar la decisión de rechazarlo o enviarlo a spam.

Esto ocurre en Yopmail pero en grandes proveedores de correo como Gmail, Hotmail, etc. directamente **bloquean los correos que no pasan los filtros**.

---

**DKIM: None**
El DKIM (DomainKeys Identified Mail) es un sistema donde el servidor legítimo del dominio **firma criptográficamente** los mensajes.

- El mensaje **no incluye ninguna firma DKIM**, lo que **confirma que no proviene realmente de Gmail**, ya que todos sus correos reales **sí** llevan esa firma.
- Resultado: **Fallo total de autenticación**.

---

**DMARC: Fail**
El DMARC (Domain-based Message Authentication, Reporting and Conformance) combina SPF y DKIM para **decidir qué hacer con correos no auténticos**.

- Gmail tiene esta política DMARC:
  ```
  v=DMARC1; p=none; sp=quarantine;
  ```

  Lo cual dice: *"Si ni SPF ni DKIM pasan, marca el mensaje como sospechoso o potencialmente envíalo a cuarentena."*

- Como aquí **falló en SPF y no tiene DKIM**, el mensaje **no tiene ninguna autenticación válida** y por tanto, bajo DMARC, puede:
  - Ir a **Spam**
  - Ser **rechazado** (especialmente si el proveedor receptor lo decide así)

---

### ¿Por qué no llega a Gmail o Hotmail?

Gmail, Outlook y otros servicios tienen **capas extra de protección**, como:

| Capa de Seguridad | ¿Qué hace?                                                                      |
|-------------------|---------------------------------------------------------------------------------|
| SPF               | Verifica si la IP puede enviar correos en nombre del dominio                    |
| DKIM              | Verifica si el mensaje fue firmado por el dominio legítimo                      |
| DMARC             | Verifica alineación entre el dominio SPF/DKIM y el `From`                       |
| Filtros internos  | Heurísticas, listas negras, reputación del servidor, patrones de spam, contenido|

En este caso, **emkei.cz** es una herramienta pública muy usada para spoofing, por lo que **su IP ya está en listas negras y tiene pésima reputación**. Muchos servicios directamente **bloquean sus correos antes de que lleguen al buzón**.

---

## Evidencias dentro de clientes de correo (Outlook, Thunderbird, etc.)

Normalmente cuando se realiza un peritaje en algún equipo de empresa o algún particular que maneja numerosas cuentas de correo, se suelen encontrar clientes de gestión de correo como Thunderbird u Outlook que unifican todas estas cuentas en una sola interfaz.

Vamos a analizar un par de ejemplos en lo que simularemos un correo configurado en Outlook y otro en Thunderbird. Luego visualizaremos que evidencias podríamos extraer de los clientes.

### Configuración de los clientes

En el caso de Outlook la configuración inicial es sencilla, simplemente vamos a crear una cuenta de microsoft y posteriormente la añadimos en thunderbird.

![alt text](/assets/img/posts/analisis-correo-electronico/image-13.png)

En ambos clientes hemos añadido una segunda cuenta de gmail como ejemplo adicional y aunque la configuración es sencilla ya que son grandes proveedores y la sincroinización se realiza de forma transaparente, si deseamos añadir una cuenta de un dominio nuestro deberíamos hacerlo de forma manual indicando los datos necesarios.

Se recomienda usar el protocolo IMAP siempre y cuando queramos que nuestros emails se almacenen en el servidor.

- IMAP sincroniza los correos directamente con el servidor.

- Ideal para mantener copias exactas en varios dispositivos.

- A diferencia de POP3, no descarga y borra los mensajes del servidor (a menos que lo configures así).

Por ejemplo datos comunes para configurar el servidor de gmail:

```yaml
Servidor IMAP: imap.gmail.com
Puerto IMAP: 993
Seguridad: SSL/TLS
Servidor SMTP: smtp.gmail.com
Puerto SMTP: 465 o 587
Seguridad: SSL/TLS
```

En el caso de la cuenta de outlook es necesario verificar la cuenta y activar el acceso IMAP y forwarding. 

![alt text](/assets/img/posts/analisis-correo-electronico/image-14.png)

Si necesitamos o queremos introducir los datos del servidore de correo de forma manual son los siguientes:

```yaml
IMAP Server: imap-mail.outlook.com
IMAP Port: 993
SSL: Yes
SMTP Server: smtp-mail.outlook.com
SMTP Port: 587
TLS: Yes
```

### Ficheros de almacenamiento donde pueden quedar evidencias forenses

#### Thunderbird

Thunderbird guarda todos los datos del correo en una carpeta de perfil:

- **Ruta en Windows**:

`C:\Users\<TU_USUARIO>\AppData\Roaming\Thunderbird\Profiles\<nombre>.default-release\`

![alt text](/assets/img/posts/analisis-correo-electronico/image-15.png)

- Archivos importantes

| Archivo / Carpeta         | Contenido                               |
|---------------------------|-----------------------------------------|
| `Inbox`                   | Correo recibido (sin extensión)         |
| `Sent`                    | Correos enviados                        |
| `Trash`                   | Papelera                                |
| `.msf`                    | Archivos índice (no contienen mensajes) |
| `prefs.js`                | Configuración de cuentas                |
| `key4.db` / `logins.json` | Contraseñas almacenadas                 |
| `ImapMail/`               | Contiene carpetas IMAP sincronizadas    |
| `Mail/`                   | Carpetas POP o locales                  |

> Los archivos tipo `Inbox`, `Sent`, etc., están en **formato MBOX**, es decir, un archivo de texto plano con todos los correos concatenados.

Por ejemplo tenemos un correo de ejemplo que enviamos desde la cuenta forensetest@outlook.com a la cuenta gmail.

![alt text](/assets/img/posts/analisis-correo-electronico/image-16.png)

Y los correos recibidos en la cuenta outlook aunque la estructura de archivos es algo diferente.

![alt text](/assets/img/posts/analisis-correo-electronico/image-17.png)

#### Outlook

Outlook almacena los correos en archivos con extensiones propias.

Esto dependerá de la versión de Outlook que estemos analizando por lo que analizamos en este caso la versión Outlook classic.

---

##### Según la versión:

- **Outlook con cuentas IMAP o Exchange (Office 365, Outlook.com, etc.)**

- Los correos se guardan en archivos **.OST** (Offline Storage Table).
- Ubicación típica:
  ```
  C:\Users\<TuUsuario>\AppData\Local\Microsoft\Outlook\
  ```

- **Outlook con cuentas POP3**

- Usa archivos **.PST** (Personal Storage Table), que pueden estar en:
  ```
  C:\Users\<TuUsuario>\Documents\Outlook Files\
  ```

#### 🧾 Archivos:
| Archivo / Extensión | Descripción |
|----------------------|-------------|
| `.pst` (Personal Storage Table) | Almacén local de correos, contactos, calendarios (POP o exportación IMAP) |
| `.ost` (Offline Storage Table)  | Almacén en caché de cuentas IMAP/Exchange |

> Para análisis forense, los `.pst` son los más comunes, ya que contienen toda la información exportada.

![alt text](/assets/img/posts/analisis-correo-electronico/image-18.png)

---

### Herramientas para análisis forense / visualización de archivos de correo

#### Para MBOX (Thunderbird)

Herramientas genéricas para visualizar y analizar archivos `mbox`:

| Herramienta             | Descripción                                                                                                                 |
|-------------------------|-----------------------------------------------------------------------------------------------------------------------------|
| **MBox Viewer**         | Gratuito, permite leer correos desde archivos MBOX en Windows. [MBOX Viewer](https://sourceforge.net/projects/mbox-viewer/) |
| **Mozilla Thunderbird** | Se puede usar para abrir perfiles antiguos manualmente                                                                      |                                       
| **Aid4Mail Viewer**     | Gratuito, más avanzado. [Aid4Mail](https://www.aid4mail.com/free-viewer/)                      |
| **MailRider / Klammer** | Visores en Mac                                                                                                              |
| **Python + mailbox**    | Si sabes programar, puedes automatizar extracción de datos de MBOX                                                          |

##### Ejemplo con MBOX Viewer

Primero extraemos las carpetas correspondientes donde se encuentras los ficheros mbox con los correos de cada uno de los IMAP de outlook y gmail.

![alt text](/assets/img/posts/analisis-correo-electronico/image-19.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-20.png)

En el caso de gmail como hemos visto justo en la imagen anterior solo se visualizan los correos en la bandeja de entrada. Para visualizarlos todos debemos importar la carpeta `[Gmail].sbd`.

![alt text](/assets/img/posts/analisis-correo-electronico/image-22.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-21.png)

#### Para PST / OST (Outlook)

Herramientas para abrir `.pst` y `.ost` sin Outlook:

| Herramienta               | Descripción                                                                                                             |
|---------------------------|-------------------------------------------------------------------------------------------------------------------------|
| **Kernel PST Viewer**     | Gratis para ver correos, no requiere Outlook instalado                                                                  |
| **MFCMAPI**               | Herramienta avanzada de Microsoft para analizar archivos PST/OST [Github](https://github.com/microsoft/mfcmapi/releases)|
| **FreeViewer PST/OST Viewer** | Herramienta gráfica y gratuita                                                                                          |                                
| **PstWalker**             | Análisis forense de archivos PST                                                                                        | 
| **readpst** (Linux)       | Herramienta de línea de comandos para convertir `.pst` a formato MBOX                                                   |

##### Ejemplo con MFCMAPI

Esta herramienta es muy versatil y permite analizar los diferentes perfiles con todas sus configuraciones y datos aunque desde un punto de vista de análisis forense post-mortem no es muy útil ya que requiere que el cliente Outlook esté instalado y tenga los perfiles configurados.

Podemos seleccionar los diferentes perfiles.

![alt text](/assets/img/posts/analisis-correo-electronico/image-23.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-24.png)

Para ver el inbox damos click en **QuickStart** -> **Open Folder** y seleccionamos la carpeta **Inbox**.

![alt text](/assets/img/posts/analisis-correo-electronico/image-25.png)

##### EJemplo con FreeViewer PST/OST Viewer

![alt text](/assets/img/posts/analisis-correo-electronico/image-26.png)

![alt text](/assets/img/posts/analisis-correo-electronico/image-27.png)

Este software cuenta con una interfaz más amigable e incluso muestra de forma destacada los mensajes eliminados, errores de sincronización, etc.

![alt text](/assets/img/posts/analisis-correo-electronico/image-28.png)

