---
title: Android - Analisis forense
date: 2025-03-20 11:00:00 +0000
categories: [Forense, Android]
tags: [Forense, Android, Analisis forense]
image:
  path: /assets/img/cabeceras_genericas/android-forense.png
  alt:  Android
description: >
  Guía para analisis forense en Android 
pin: false  
toc: true   
math: false 
mermaid: false 
---

## 🔍 Análisis Forense en Android: Retos y Claves para Investigaciones Digitales  

Los smartphones son herramientas esenciales en la sociedad europea, usados desde consumidores hasta altos cargos gubernamentales y empresas. Su versatilidad los convierte en monederos digitales, sistemas de navegación, sensores de salud (como monitorización cardíaca remota) y más. Sin embargo, esta riqueza de datos los convierte en fuentes críticas para el **análisis forense móvil**, que busca recuperar evidencia digital bajo condiciones forenses rigurosas.  

### 🔑 Aspectos Clave en el Análisis Forense Móvil:  
1. **Adquisición de Datos Compleja**:  
   - Los dispositivos suelen analizarse *encendidos* (live acquisition), ya que acceder a la memoria interna puede ser técnicamente limitado.  
   - Tarjetas SD y memorias externas pueden contener información vital, pero requieren manejo cuidadoso para preservar pruebas.  

2. **Cadena de Custodia (CoC) Frágil**:  
   - Instalar aplicaciones forenses en el dispositivo puede alterar su estado original.  
   - La falta de sistemas de archivos de *solo lectura* aumenta el riesgo de modificar datos, comprometiendo su validez legal.  

3. **Riesgo de Pérdida de Integridad**:  
   - Entornos de prueba o herramientas no especializadas pueden activar mecanismos de defensa del dispositivo (como malware) y borrar pruebas.  
   - Cualquier error técnico puede invalidar la evidencia en juicios.  

## Uso de Android Studio para Análisis Forense

Para analizar datos forenses en Android, se puede utilizar [Android Studio](https://developer.android.com/studio) ya que cuenta con un emulador de dispositivos Google Pixel.

En este caso estaremos usando Android Studio en un sistema host Windows 11. 

Instalado el software vamos a crear un emulador.

![alt text](/assets/img/posts/android_forense/image.png)

![alt text](/assets/img/posts/android_forense/image-1.png)

Si nos pide instalar el hypervisor para el emulador de Android, nosotros lo instalamos.

![alt text](/assets/img/posts/android_forense/image-2.png)

Como queremos un equipo en el que podamos trabajar como usuario root seleccionaremos el modelo más reciente que no cuente con el soporte de google.

![alt text](/assets/img/posts/android_forense/image-3.png)

Seleccionamos la API de Google compatible con el sistema host y ajustamos las características del emulador a necesidad.

![alt text](/assets/img/posts/android_forense/image-4.png)

Una vez iniciado puede que veamos un mensaje como este.

![alt text](/assets/img/posts/android_forense/image-5.png)

Si es el caso significa que tendremos que descargar el Android Debug Bridge (adb) para poder conectarnos al emulador de forma manual.

Para descargarel paquete de herramientas SDK de Android podemos usar el siguiente enlace y seleccionar el que corresponda a nuestro sistema host. 

[SDK Tools](https://developer.android.com/tools/releases/platform-tools?hl=es-419)

Una vez descagado y extraido, en el emulador haremos lo siguiente.

![alt text](/assets/img/posts/android_forense/image-6.png)

Colocamos la ruta al ejecutable de adb.

### Activar el modo depuración USB en el emulador

Es igual a un teléfono Android convencional. Iremos a ajustes, información sobre el dispositivo y pulsaremos varias veces sobre el numero de compilación del dispositivo hasta que se nos que hemos activado las opciones de desarrollador.

![alt text](/assets/img/posts/android_forense/image-7.png)

Ahora en sistema buscaremos las opciones de desarrollador y activamos el modo depuración USB.

![alt text](/assets/img/posts/android_forense/image-8.png)


### Algunos comandos de ADB

#### 1. **`adb devices`**
   - **Uso**: Lista todos los dispositivos Android conectados a la computadora y que tienen el modo de depuración USB activado.
   - **Ejemplo**:  
     ```bash
     adb devices
     ```
   - **Resultado**: Muestra una lista de dispositivos conectados con sus identificadores únicos (serial numbers) y su estado (por ejemplo, `device` si está listo para usar o `unauthorized` si no se ha autorizado la depuración USB).

![alt text](/assets/img/posts/android_forense/image-10.png)

#### 2. **`adb shell`**
   - **Uso**: Inicia una sesión de terminal (shell) en el dispositivo Android, permitiendo ejecutar comandos directamente en el sistema operativo del dispositivo.
   - **Ejemplo**:  
     ```bash
     adb shell
     ```
   - **Resultado**: Entras en una línea de comandos dentro del dispositivo, donde puedes ejecutar comandos de Linux (como `ls`, `cd`, `rm`, etc.) para navegar por el sistema de archivos o realizar tareas avanzadas.

![alt text](/assets/img/posts/android_forense/image-9.png)

#### 3. **`adb root`**
   - **Uso**: Reinicia el servicio ADB con permisos de superusuario (root) en el dispositivo. Esto es útil para acceder a partes restringidas del sistema.
   - **Ejemplo**:  
     ```bash
     adb root
     ```
   - **Nota**: Solo funciona si el dispositivo tiene permisos root habilitados. Si no, el comando no tendrá efecto.

![alt text](/assets/img/posts/android_forense/image-11.png)

#### 4. **`adb pull`**
   - **Uso**: Copia archivos o directorios desde el dispositivo Android a la computadora.
   - **Sintaxis**:  
     ```bash
     adb pull <ruta_en_dispositivo> <ruta_en_pc>
     ```
   - **Ejemplo**:  
     ```bash
     adb pull /sdcard/Download/mi_archivo.txt ~/Desktop/
     ```
   - **Resultado**: Copia el archivo `test.png` desde la carpeta `Download` del dispositivo al escritorio del equipo.

![alt text](/assets/img/posts/android_forense/image-12.png)

### 5. **`adb push`**
   - **Uso**: Copia archivos o directorios desde la computadora al dispositivo Android.
   - **Sintaxis**:  
     ```bash
     adb push <ruta_en_pc> <ruta_en_dispositivo>
     ```
   - **Ejemplo**:  
     ```bash
     adb push ~/Desktop/mi_archivo.txt /sdcard/Download/
     ```
   - **Resultado**: Copia el archivo `test.txt` desde el escritorio de la computadora a la carpeta `Download` del dispositivo.

![alt text](/assets/img/posts/android_forense/image-13.png)

## Crear una maquina virtual Android en un entorno de virtualización (Proxmox)

Como alternativa a android studio, podemos utilizar un entorno de virtualización como proxmox para crear una maquina virtual con el sistema operativo android.

> Nota : Se podría utilizar cualquier otro virtualizados como VMWare o VirtualBox, pero en este caso vamos a utilizar proxmox.
{: .prompt-notice}

Para descargar una versión del sistema android compatible con arquitectura x86 podemos utilizar el siguiente enlace.

[Android x86 System Image](https://www.android-x86.org/?ref=benheater.com)

Una vez creada la maquina virtual, arrancamos y procedemos a instalar el sistema operativo android.

![alt text](/assets/img/posts/android_forense/image-14.png)

Detectamos y creamos las particiones del sistema.

![alt text](/assets/img/posts/android_forense/image-15.png)

Si queremos indicamos que use GPT. En principio seleccionaremos que no.

![alt text](/assets/img/posts/android_forense/image-16.png)

Creamos una nueva. 

![alt text](/assets/img/posts/android_forense/image-17.png)

Seleccionamos primaria y damos enter para dejar el tamaño por defecto del disco.

![alt text](/assets/img/posts/android_forense/image-14-1.png)

Hacemos la partición booteable.

![alt text](/assets/img/posts/android_forense/image-15-1.png)

Escribimos los cambios y seleccionamos `QUIT` para salir del modo de particionado.

![alt text](/assets/img/posts/android_forense/image-18.png)

Ya nos debería salir la partición correcta por lo que damos en OK.

![alt text](/assets/img/posts/android_forense/image-19.png)

Formateamos la partición en EXT4.

![alt text](/assets/img/posts/android_forense/image-20.png)

Indicamos que si.

![alt text](/assets/img/posts/android_forense/image-21.png)

Instalamos el bootloader GRUB.

![alt text](/assets/img/posts/android_forense/image-22.png)

Hacemos la que se pueda escribir en /system.

![alt text](/assets/img/posts/android_forense/image-23.png)

Reiniciamos el sistema y hacemos la configuración inicial.

En la red WiFi seleccionamos más redes y la red virtualizada.

![alt text](/assets/img/posts/android_forense/image-24.png)

Finalizada la configuración tipica de android ahora activamos como antes el modo depuración USB.

![alt text](/assets/img/posts/android_forense/image-25.png)

## Extracción de datos mediante AFLogical OSE

Ahora que tenemos nuestros posibles entornos de prueba vamos a empezar utilizando una herramienta para extraer datos de los dispositivos Android como registros de llamadas, contanctos, SMS, etc.

[AFLogical OSE](https://github.com/nowsecure/android-forensics)

Debido a que el software ya es antiguo posiblemente sea dificil encontrar el apk necesario para que funcione aunque a continuación dejo el enlace del apk oficial que encontré y subí a Internet Archive.

[AFLogical OSE APK](https://archive.org/details/aflogical-ose-1.5.2)

Una vez descargado el archivo, lo instalamos en nuestro dispositivo Android.

Para ello vamos a utilizar adb por lo que en nuestra máquina windows donde tenemos descargado ADB descargaremos el apk a esta.

> Nota : Para saber la IP de la máquina android y poder conectarnos por ADB podemos utilziar el terminal integrade que viene con el sistema operativo android y el comando `ip a`
{: .prompt-advice}

```bash
adb connect 192.168.1.10:5555
adb devices
adb install aflogical-ose-1.5.2.apk
```

![alt text](/assets/img/posts/android_forense/image-26.png)

Una vez instalada veremos la aplicación instalada en nuestro dispositivo. Aunque es algo antigua no viene mal probarla.

![alt text](/assets/img/posts/android_forense/image-27.png)

Una vez ejecutemos la aplicación los datos extraidos deben aparecer en la ruta `/sdcard/forensics/`

Mediante adb pull podemos extraer los datos.

![alt text](/assets/img/posts/android_forense/image-28.png)

## Extracción de datos mediante Andriller

Andriller es una herramienta de software que ofrece una colección de herramientas forenses para smartphones. Realiza adquisiciones de solo lectura, forenses, seguras y no destructivas desde dispositivos Android. Incluye características como el desbloqueo de pantallas de bloqueo (Patrón, PIN o Contraseña), decodificadores personalizados para datos de aplicaciones desde bases de datos de Android (algunas de Apple iOS y Windows) para decodificar comunicaciones. La extracción y los decodificadores generan informes en formatos HTML y Excel.

Es una herramienta escrita en python por lo que necesitamos este lenguaje para poder utilizarla.

[GitHub](https://github.com/den4uk/andriller)

En Windows:

- Descargamos el codigo de gitihub y navegamos a su carpeta.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install andriller -U 
```

Una vez instalado para ejecutarlo simplemente `python -m andriller`.

![alt text](/assets/img/posts/android_forense/image-29.png)

Este software detecta el dispositvo mediante USB por lo que en este caso para que detecte nuestra máquina virtual android debemos hacer lo siguiente. 

En el adb que utiliza este software vamos a conectarnos a la máquina virtual android de forma remota manualmente.

![alt text](/assets/img/posts/android_forense/image-30.png)

Ahora nos detectará la máquina virtual y podremos utilizarla.

Esta herramienta nos permite extraer los datos básicos que se pueden extraer de los dispositivos Android sin permisos de root y los directorios compartidos, sin embargo si somos usuario root dentro del dispositivo podemos extraer información más detallada haciendo uso de un backup del dispositivo.

![alt text](/assets/img/posts/android_forense/image-31.png)

Si damos en esta última opción nos mostrará un mensaje de aviso indicando que debemos aceptar el backup del dispositivo de forma manual.

![alt text](/assets/img/posts/android_forense/image-32.png)

![alt text](/assets/img/posts/android_forense/image-33.png)

Una vez completado tendremos un pequeño resumen de los datos estos dentro de la carpeta de salida que seleccionamos anteriormente.

![alt text](/assets/img/posts/android_forense/image-34.png)

## Peritajes sobre WhatsApp

### Introducción para un Peritaje sobre WhatsApp

Actualmente, las aplicaciones de mensajería instantánea como WhatsApp se han convertido en herramientas esenciales tanto para la comunicación personal como para las interacciones comerciales. Con más de **2.000 millones de usuarios en todo el mundo**, WhatsApp no solo facilita el intercambio de mensajes, sino también la transmisión de archivos multimedia, la realización de llamadas de voz y video, y el uso de funcionalidades avanzadas como la geolocalización en tiempo real. Sin embargo, este amplio uso también ha convertido a WhatsApp en una fuente crítica de **evidencias digitales** en investigaciones judiciales, casos de ciberseguridad y procesos legales.

El **análisis forense de WhatsApp** tiene como objetivo extraer, preservar y analizar los datos almacenados en la aplicación para responder a preguntas clave, como:
- ¿Quién participó en una conversación?
- ¿Cuándo y cómo se envió o recibió un mensaje?
- ¿Es posible recuperar mensajes borrados?
- ¿Se puede determinar la procedencia de un mensaje (desde un dispositivo móvil o WhatsApp Web)?
- ¿Qué información adicional (metadatos, ubicaciones, archivos) puede ser relevante para el caso?

Este tipo de análisis es especialmente relevante en casos de **acoso, fraude, suplantación de identidad, ciberdelitos** y otros escenarios donde las conversaciones de WhatsApp pueden ser pruebas fundamentales. Sin embargo, el proceso de peritaje no está exento de desafíos, como el cifrado de los datos, la constante actualización de la aplicación y la necesidad de preservar la integridad de las evidencias para garantizar su validez en un procedimiento judicial.

En este contexto, el peritaje se enfoca en el **análisis forense de WhatsApp**, abordando tanto las plataformas **iOS** como **Android**, y explorando las técnicas y herramientas disponibles para la extracción y análisis de datos. Además, se examinarán las diferencias entre los modelos de datos de ambas plataformas, las funcionalidades de interés forense y las limitaciones técnicas que pueden surgir durante el proceso.


### Diferencias entre un peritaje consensuado y un peritaje no consensuado

- **Consensuado**: El profesional cuenta con el permiso del titular de la cuenta y acceso completo al terminal (claves de desbloqueo, datos de la cuenta). Esto permite métodos menos invasivos, como extraer la base de datos mediante copias de seguridad (iTunes en iOS o Google Cloud en Android) o usar herramientas comerciales con el token de WhatsApp Web.

- **No consensuado**: Se realiza sin acceso al terminal, generalmente por orden judicial. Requiere evadir medidas de seguridad (root/jailbreak) para acceder a la memoria interna. En Android, implica obtener la clave de cifrado ubicada en `/data/data/com.whatsapp/files/key`. En iOS, puede ser imposible si el dispositivo está cifrado, a menos que se realice un jailbreak.

### Algunas técnicas para peritar conversaciones de WhatsApp

1. **Capturas de pantalla**: Menos fiable, pero válida si se verifica la integridad del dispositivo.

2. **Extracción mediante token**: Usar WhatsApp Web para simular una sesión y extraer mensajes (no accede a datos borrados o completos).

3. **Acceso a la base de datos**:
   - **iOS**: Extraer copias de seguridad con iTunes y analizar archivos como `ChatStorage.sqlite`.
   - **Android**: Acceder a `/data/data/com.whatsapp/databases/msgstore.db` (requiere root) o descifrar copias de seguridad en la nube usando la clave local.

4. **Herramientas forenses comerciales**: Oxygen Forensics, MobilEdit o Magnet Axiom para extraer y analizar datos.

5. **Análisis de registros y metadatos**: Revisar logs de llamadas (`call_history.sqlite`), ubicaciones (`location.db`) o mensajes borrados mediante técnicas de recuperación de datos.

### Ubicación y extracción de claves y bases de datos

- **Clave de cifrado (Android)**:
  - Ruta: `/data/data/com.whatsapp/files/key`.
  - Extracción: Requiere acceso root (por ejemplo, mediante ADB) o downgrade de la versión de WhatsApp para evitar cifrado.

- **Bases de datos**:
  - **iOS**:
    - Ubicación: `/private/var/mobile/Applications/group.net.whatsapp.WhatsApp.shared/`.
    - Extracción: Copia de seguridad con iTunes y uso de herramientas como Oxygen Forensics.
  - **Android**:
    - Ubicación: `/data/data/com.whatsapp/databases/` (ej: `msgstore.db`, `wa.db`).
    - Extracción: Root del dispositivo o uso de máquinas virtuales para evitar alterar el original.

- **Métodos alternativos**:
  - **WhatsApp Web**: Simular sesiones para extraer mensajes activos (no incluye datos borrados).
  - **Copia de seguridad en la nube (Android)**: Descargar desde Google Drive usando la clave local almacenada en el dispositivo.


> Nota : La extracción de datos en iOS es más estructurada pero menos informativa, mientras que Android permite comprobaciones cruzadas debido a redundancia en tablas. Ambos requieren preservar la integridad de los artefactos para su validez judicial.
{: .prompt-notice}

### Ejemplo de análisis forense de WhatsApp en Android

Para este caso tenemos diferentes opciones y es que actualmente las bases de datos de WhatsApp están cifradas siempre y cuando en el dispositivo donde se ha instalado la aplicación tenga una tarjeta SIM insertada. De lo contrario las bases de datos no están cifradas y no existe una clave de cifrado.

Esto podría ocurrir por ejemplo si utilizamos la máquina virtual configurada anteriormente o el emulador por lo que para este caso (si disponemos de ello) lo mejor es realizarlo sobre un terminal con acceso root real, con posibilidad de insetar una tarjeta SIM.

![alt text](/assets/img/posts/android_forense/image-35.png)

Como vemos ya tenemos nuestro dispositivo listo, en este caso está rooteado por lo que tenemos acceso a la memoria interna y podemos extraer la base de datos de WhatsApp.

1. Accedemos al dispositivo como root

Conectamos el dispositivo al PC y permitimos el acceso por adb (previamente activado en las opciones de desarrollador).

![alt text](/assets/img/posts/android_forense/image-41.png)

```bash
adb root
```

Si por algún motivo tenemos un mensaje de error indidcando que el modo root no está disponible en versiones de producción es porque la versión de nuestro dispositivo, aun estando rooteado, es de producción y no de desarrollo, por lo que el modo root mediante ADB no estará disponible.

- Error 

```bash
sdksdk@uwuntu:~$ adb root
adbd cannot run as root in production builds
```

Es por esto que una vez tenemos el dispositivo rooteado podemos hacer lo siguiente.

Vamos a iniciar una shell en nuestro dispositivo y podemos ver que el usuario no es root sino shell, por lo que no tenemos privilegios.

![alt text](/assets/img/posts/android_forense/image-36.png)

Una vez dentro de la shell ejecutamos `su root` para elevar nuestro privilegios a superusuario y, en la pantalla de nuestro dispositivo veremos un aviso de nuestra aplicación que gestiona el acceso root (en este caso Magisk) preguntando si queremos permitirle el acceso.

Si no apareciese el mensaje siempre podemos acceder a nuestra aplicación y permitir el acceso root manualmente.

![alt text](/assets/img/posts/android_forense/image-42.png)

![alt text](/assets/img/posts/android_forense/image-37.png)

2. Extraer la Clave de Cifrado

```bash
cd /data/data/com.whatsapp/files/
adb pull /data/data/com.whatsapp/files/key /ruta/destino/
```
El comando `pull` solo funcionará si podemos establecer adb como root, en este caso necesitamos acceder como root una vez dentro de la shell por lo que nos indicará que no tenemos permisos para acceder a ese archivo.

Como solución podemos simplemente copiar el contenido.

```bash
adb exec-out "su -c 'cat /data/data/com.whatsapp/files/key'" > ./key
```

![alt text](/assets/img/posts/android_forense/image-38.png)

3. Extraer la base de datos

Para este caso el proceso es similar.

```bash
cd /data/data/com.whatsapp/databases/
adb pull /data/data/com.whatsapp/databases/msgstore.db /ruta/destino/
adb pull /data/data/com.whatsapp/databases/wa.db /ruta/destino/
```
   Los archivos principales son:
   - `msgstore.db`: Contiene los mensajes.
   - `wa.db`: Contiene información de contactos.
   - `chatsettings.db`: Almacena configuraciones de chats.

![alt text](/assets/img/posts/android_forense/image-39.png)

Como tenemos el mismo error de permisos que antes hacemos lo siguiente.

```bash
adb exec-out "su -c 'cat /data/data/com.whatsapp/databases/msgstore.db'" > ./msgstore.db
adb exec-out "su -c 'cat /data/data/com.whatsapp/databases/wa.db'" > ./wa.db
```

![alt text](/assets/img/posts/android_forense/image-40.png)

Con todo esto ya tenemos nuestros archivos de bases de datos y clave de cifrado para analizar.

#### Analizar los datos extraídos con Andriller u otras herramientas forenses.

Para utilizar Andriller hacemos lo mismo que en el apartado de la extracción de datos aunque como en este caso estamos trabajando sobre un ubuntu, los pasos son los siguientes.

```bash
git clone https://github.com/den4uk/andriller.git
cd andriller
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 andriller-gui.py
```
Primero vamos a decodificar las bases de datos con la key.

Seleccionamos en la pestaña `app utils` la opción `WhatsApp Crypt`.

![alt text](/assets/img/posts/android_forense/image-45.png)

Indicamos el directorio donde tenemos las bases de datos y la clave de cifrado, y damos click en `Decrypt all`.

Si no tenemos encriptadas las bases no es necesario.

Seleccionamos decodificadores.

![alt text](/assets/img/posts/android_forense/image-43.png)

1. Contactos de WhatsApp

![alt text](/assets/img/posts/android_forense/image-44.png)

Una vez abrimos el reporte podremos ver todos los contactos de WhatsApp.

![alt text](/assets/img/posts/android_forense/image-46.png)

2. Chats de WhatsApp

Como es de esperar la estructura de los datos en la base de datos puede cambiar a lo largo del tiempo y actualizaciones por lo que ahora si intentamos extraer los chats de WhatsApp tendremos un error porque la tabla de `chat_list` no existe.

Para solucionar esto podemos abrir la base de datos con `SQLiteBrowser` y ver el nombre actual de la tabla.
Una vez hemos encontrado la tabla que necesitamos podemos cambiar en el código de Andriller para que la tabla se llame `chat` ya que a fecha de escribir este artículo la tabla `chat_list` ahora es llamada `chat`.

El archivo `decoders.py` será el que tendremos que modificar. 

![alt text](/assets/img/posts/android_forense/image-48.png)

Para los mensajes es similar, buscamos como se llama actualmente la tabla `messages` y cambiamos el nombre a `message` en el código.

![alt text](/assets/img/posts/android_forense/image-47.png)

En esta aplicación solo he conseguido sacar los contactos por lo que para poder visualizar los chats vamos a utilizar otra herramienta que tendremos que modificar.

####  Whatsapp Msgstore Viewer

[Github Oficial](https://github.com/absadiki/whatsapp-msgstore-viewer)

Esta herramienta es algo menos conocida e interpreta la información de forma bastante clara simulando la intergaz de un usuario de WhatsApp.

Una vez tengamos la herramienta descargada y funcionando debemos añadir una nueva estructura de datos ya que la que trae por defecto no es compatible con la actual (a fecha de escribir este artículo).

```bash
git clone https://github.com/absadiki/whatsapp-msgstore-viewer.git
cd whatsapp-msgstore-viewer
mkdir /db/v2
nano /db/v2/db.py
```

```python
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from dbs.abstract_db import AbstractDatabase


class Database(AbstractDatabase):

    def __init__(self, msgstore, wa):
        # Updated schema to match current WhatsApp database structure
        schema = {
            'chat_view': {
                'name': 'chat_view',
                'attributes': [
                    '_id',
                    'jid_row_id',
                    'hidden',
                    'subject',
                    'created_timestamp',
                    'display_message_row_id',
                    'last_message_row_id',
                    'last_read_message_row_id',
                    'last_read_receipt_sent_message_row_id',
                    'last_important_message_row_id',
                    'archived',
                    'sort_timestamp',
                    'mod_tag',
                    'gen',
                    'spam_detection',
                    'unseen_earliest_message_received_time',
                    'unseen_message_count',
                    'unseen_missed_calls_count',
                    'unseen_row_count',
                    'plaintext_disabled',
                    'vcard_ui_dismissed',
                    'change_number_notified_message_row_id',
                    'show_group_description',
                    'ephemeral_expiration',
                    'last_read_ephemeral_message_row_id',
                    'ephemeral_setting_timestamp',
                    'ephemeral_displayed_exemptions',
                    'ephemeral_disappearing_messages_initiator',
                    'unseen_important_message_count',
                    'group_type',
                    'last_message_reaction_row_id',
                    'last_seen_message_reaction_row_id',
                    'unseen_message_reaction_count',
                    'unseen_comment_message_count',
                    'growth_lock_level',
                    'growth_lock_expiration_ts',
                    'last_read_message_sort_id',
                    'display_message_sort_id',
                    'last_message_sort_id',
                    'last_read_receipt_sent_message_sort_id',
                    'has_new_community_admin_dialog_been_acknowledged',
                    'history_sync_progress'
                ]
            },
            'message': {
                'name': 'message',
                'attributes': [
                    '_id',
                    'chat_row_id',
                    'key_id',
                    'from_me',
                    'timestamp',
                    'text_data',
                    'sort_id'  # Added new field
                ]
            },
            'message_media': {
                'name': 'message_media',
                'attributes': [
                    'message_row_id',
                    'file_path',
                ]
            },
            'message_quoted': {
                'name': 'message_quoted',
                'attributes': [
                    'message_row_id',
                    'text_data',
                    'from_me',
                    'key_id'
                ]
            },
            'jid': {  # Added jid table as it's referenced in the queries
                'name': 'jid',
                'attributes': [
                    '_id',
                    'user',
                    'raw_string'
                ]
            },
            'call_log': {  # Added call_log table for fetch_calls method
                'name': 'call_log',
                'attributes': [
                    '_id',
                    'from_me',
                    'timestamp',
                    'video_call',
                    'duration',
                    'jid_row_id'
                ]
            }
        }
        super(Database, self).__init__(msgstore, wa, schema=schema)

    def fetch_contact_chats(self):
        sql_query = """
        SELECT 
            chat_view._id, 
            jid.user,
            jid.raw_string as jid_row_id,
            message.text_data, 
            DATETIME(ROUND(chat_view.sort_timestamp / 1000), 'unixepoch') as timestamp

        FROM chat_view 
        INNER JOIN jid ON chat_view.jid_row_id = jid._id 
        INNER JOIN message ON chat_view.last_message_row_id = message._id

        WHERE jid.raw_string NOT LIKE '%g.us'
        
        ORDER BY timestamp DESC
        """
        return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_group_chats(self):
        sql_query = """
        SELECT 
            chat_view._id, 
            chat_view.subject as user,
            jid.raw_string as jid_row_id,
            message.text_data, 
            DATETIME(ROUND(chat_view.sort_timestamp / 1000), 'unixepoch') as timestamp

        FROM chat_view 
        INNER JOIN jid ON chat_view.jid_row_id = jid._id 
        INNER JOIN message ON chat_view.last_message_row_id = message._id

        WHERE jid.raw_string LIKE '%g.us'
        
        ORDER BY timestamp DESC
        """
        return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_calls(self, how_many=None):
        sql_query = """
        SELECT 
            call_log._id, 
            call_log.from_me, 
            DATETIME(ROUND(call_log.timestamp / 1000), 'unixepoch') as timestamp, 
            call_log.video_call,
            Time(call_log.duration, 'unixepoch') as duration,
            jid.user, 
            jid.raw_string as jid_row_id

        FROM call_log 
        LEFT JOIN jid ON call_log.jid_row_id = jid._id
        
        ORDER BY timestamp DESC
        """
        if how_many:
            return self.msgstore_cursor.execute(sql_query).fetchmany(how_many)
        else:
            return self.msgstore_cursor.execute(sql_query).fetchall()

    def fetch_chat(self, chat_view_id):
        sql_query = f"""
        SELECT  
            message._id, 
            message.key_id, 
            message.from_me, 
            DATETIME(ROUND(message.timestamp / 1000), 'unixepoch') as timestamp,  
            ifnull(message.text_data, '') as text_data,
            message_media.file_path,
            message_quoted.text_data as message_quoted_text_data,
            message_quoted.from_me as message_quoted_from_me,
            message_quoted.key_id as message_quoted_key_id,
            message.sort_id
        
        FROM message 
        LEFT JOIN message_media ON message._id = message_media.message_row_id
        LEFT JOIN message_quoted ON message._id = message_quoted.message_row_id
        
        WHERE message.chat_row_id = {chat_view_id}
        
        ORDER BY message.sort_id ASC
        """
        return self.msgstore_cursor.execute(sql_query).fetchall()
        
    def fetch_unread_messages(self, chat_view_id):
        """
        Fetch unread messages based on last_read_message_row_id or sort_id
        """
        sql_query = f"""
        SELECT  
            message._id, 
            message.key_id, 
            message.from_me, 
            DATETIME(ROUND(message.timestamp / 1000), 'unixepoch') as timestamp,  
            ifnull(message.text_data, '') as text_data,
            message.sort_id
            
        FROM message 
        JOIN chat_view ON message.chat_row_id = chat_view._id
        
        WHERE 
            chat_view._id = {chat_view_id}
            AND (
                (chat_view.last_read_message_sort_id IS NOT NULL AND message.sort_id > chat_view.last_read_message_sort_id)
                OR
                (chat_view.last_read_message_row_id IS NOT NULL AND message._id > chat_view.last_read_message_row_id)
            )
            
        ORDER BY message.sort_id ASC
        """
        return self.msgstore_cursor.execute(sql_query).fetchall()
        
    def fetch_important_messages(self, chat_view_id):
        """
        Fetch important messages from a chat
        """
        sql_query = f"""
        SELECT  
            message._id, 
            message.key_id, 
            message.from_me, 
            DATETIME(ROUND(message.timestamp / 1000), 'unixepoch') as timestamp,  
            ifnull(message.text_data, '') as text_data
            
        FROM message 
        WHERE 
            message.chat_row_id = {chat_view_id}
            AND message._id IN (
                SELECT last_important_message_row_id 
                FROM chat_view 
                WHERE _id = {chat_view_id} AND last_important_message_row_id IS NOT NULL
            )
        """
        return self.msgstore_cursor.execute(sql_query).fetchall()
```

Si tenemos un fallo en el main_screen podremos arreglarlo modificando lo siguiete.

```bash
nano view/MainScreen/main_screen.py
```

Aquí reemplazamos todos los `raw_string_jid` por `jid_row_id`.

Ahora podemos ejecutarlo y ver los chats de WhatsApp aunque hasta ahora solo he podido listar los chats sin los nombre de contacto ya que existe un error al leer la base de datos WA.db.

![alt text](/assets/img/posts/android_forense/image-49.png)

- Chats 

![alt text](/assets/img/posts/android_forense/image-50.png)

- Grupos

![alt text](/assets/img/posts/android_forense/image-51.png)

- Llamadas

![alt text](/assets/img/posts/android_forense/image-52.png)

