---
title: Análisis forense en servicios de almacenamiento SaaS
date: 2025-02-20 11:00:00 +0000
categories: [Forense, Cloud]
tags: [Cloud, Forense, Almacenamiento, nube]
description: >
  Guía rapida sobre el análisis forense en servicios de almacenamiento SaaS.
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Introcucción

### ¿Qué es el análisis forense de la nube?  

El análisis forense de la nube es la aplicación de principios y procedimientos de ciencia forense digital en entornos de computación en la nube. Este tipo de análisis implica la recolección, identificación, preservación, examen e interpretación de evidencia digital almacenada tanto en dispositivos locales (endpoints) como en los servidores de los proveedores de servicios en la nube. Según el documento, el análisis forense de la nube abarca enfoques híbridos como forenses virtuales, de red y en tiempo real, y requiere la colaboración de actores clave como proveedores de servicios, consumidores y auditores. 

Además, enfrenta desafíos legales derivados de características como la multi-jurisdicción y la multi-inquilinato propias de la nube. 


### ¿Cuáles son las fuentes de evidencias digitales que nos encontramos específicamente cuando trabajamos en la nube?  

En el contexto del análisis forense de la nube, las principales fuentes de evidencia digital incluyen: 

    Dispositivos Locales (Endpoints):  

        Archivos y Carpetas Sincronizados:  Archivos y carpetas sincronizadas entre el dispositivo local y la nube.
        Papelera de Reciclaje:  Contiene archivos eliminados que pueden ser recuperados.
        Registros del Sistema:  Event logs, registros de aplicaciones y seguridad.
        Archivos de Prefetch:  Información sobre aplicaciones ejecutadas recientemente.
        Archivos DLL y LNK:  Archivos de biblioteca dinámica y atajos que pueden revelar información sobre programas ejecutados.
        Caché y Cookies del Navegador:  Datos temporales y credenciales almacenadas por navegadores web.
        Historial del Navegador:  Registros de sitios visitados y actividades relacionadas con servicios en la nube.
        Memoria Volátil (RAM):  Procesos activos y datos en uso durante la ejecución de aplicaciones de la nube.
         

    Proveedores de Servicios en la Nube:  

        APIs de los Proveedores:  Permiten acceder a metadatos y contenido de archivos directamente desde la nube.
        Registros de Actividad:  Logs de operaciones realizadas por el usuario, como subidas, descargas, ediciones y eliminaciones.
        Revisiones y Metadatos:  Historial de versiones y detalles técnicos sobre los archivos.
         
### ¿Qué posibilidades nos ofrece explotar las API que nos ofrecen los proveedores de servicios en la nube?

Las APIs de los proveedores de servicios en la nube ofrecen varias posibilidades para la recolección de evidencia forense: 

    Acceso Directo a Datos en la Nube:  

        Las APIs permiten a los investigadores acceder a datos almacenados en la nube sin necesidad de depender únicamente de copias locales.
         

    Recolección de Metadatos:  

        Contenido de Archivos:  Se puede obtener el contenido específico de archivos almacenados en la nube.
        Metadatos de Archivos:  Incluyen nombre, tamaño, ID, hash, tipo MIME, fecha y hora de creación/modificación, ubicación, etc.
        Historial de Revisiones:  Registra cambios realizados en un archivo, permitiendo analizar versiones anteriores.
        Logs de Operaciones:  Registros de actividades como subidas, descargas, compartición, edición y eliminación de archivos.
        Notificaciones Especiales:  Información sobre eventos importantes relacionados con los archivos o carpetas.

### Clientes más utilizados a la hora de acceder a servicios en la nube 

| Software Cliente | Servicios en la Nube Soportados | Plataformas Soportadas |
|------------------|--------------------------------|------------------------|
| **Dropbox Client** | Dropbox | Windows, macOS, Linux, Móviles (iOS/Android) |
| **Google Drive Client** | Google Drive | Windows, macOS, Móviles (iOS/Android) |
| **OneDrive Client** | Microsoft OneDrive | Windows, macOS, Móviles (iOS/Android) |
| **iCloud App** | iCloud | macOS, iOS, Windows |
| **Box Client** | Box | Windows, macOS, Móviles (iOS/Android) |
| **Amazon Cloud Drive Client** | Amazon Cloud Drive | Windows, macOS, Móviles (iOS/Android) |
| **ownCloud Client** | ownCloud | Windows, macOS, Linux, Móviles (iOS/Android) |
| **Mega Client** | Mega | Windows, macOS, Linux, Móviles (iOS/Android) |
| **SkyDrive Client** (ahora OneDrive) | Microsoft SkyDrive/OneDrive | Windows, Móviles (iOS/Android) |
| **IDrive Client** | IDrive | Windows, macOS, Linux, Móviles (iOS/Android) |
| **hubiC Client** | hubiC | Windows, macOS, Linux, Móviles (iOS/Android) |
| **Web Browsers** | Cualquier servicio en la nube accesible vía web | Windows, macOS, Linux, Móviles (a través de navegadores móviles) |


## Google Drive

| Artefacto                  | Ubicación                                                                                   |
|----------------------------|---------------------------------------------------------------------------------------------|
| Almacenamiento Local de Google Drive | `%UserProfile%\Google Drive\` (si la sincronización sin conexión está habilitada)       |
| Base de Datos de Metadatos | `%UserProfile%\AppData\Local\Google\DriveFS\<ID de cuenta>\metadata_sqlite_db`              |
| Caché de Archivos (Archivos Almacenados Localmente) | `%UserProfile%\AppData\Local\Google\DriveFS\<ID de cuenta>\content_cache\`               |
| Claves del Registro *(Seguimiento de la letra de unidad montada)* | `NTUSER\Software\Google\DriveFS\Share`                                                   |
| Registros en la Nube de Google Workspace | Informes de Administración de Google Workspace (para usuarios empresariales)            |

https://www.cyberengage.org/post/investigating-google-drive-for-desktop-a-forensic-guide

### Ruta de instalación del servicio y configuración

En el caso de Google Drive, el cliente estandar instalará la versión de Drive File Steam, que es la versión gratuita de Drive.

Su ubicación de instalación y su configuración como serivicio se realiza en C:\Program Files\Google\Drive File Stream.

![alt text](/assets/img/posts/cloud-forense-saas/image.png)

Aquí encontramos el servicio de Google Drive File Stream como ejecutable y toda la configuración del mismo.

### Rutas de directorios sincronizados

Esto dependerá de las que el usuario haya seleccionado en su configuración de Google Drive para que se sincronicen con el servicio pero estas opciones pueden ser encontradas.

Pero por defecto sea cual sea la carpeta seleccionada siempre se crea un disco virtual en windows donde se guarda la información de la carpeta de Google Drive sincronizadas.

![alt text](/assets/img/posts/cloud-forense-saas/image-1.png)

Si existen otros ordenadores conectados a drive aparecerán en la lista de equipos, es por eso que en este caso se nombra como MyPC1.

Podemos acceder a las claves de registro para para ver estas ubicaciones en un análisis postmortem.

Mediante Registry Explorer realizamos la busqueda en el registro 

![alt text](/assets/img/posts/cloud-forense-saas/image-2.png)

Podemos ver que la carpeta que sicroniza el usuario es Documents.

También podemos encontrar estas rutas en la carpeta de configuración del usuario en AppData\Local\Google\DriveFS\root_preference_sqlite.db

![alt text](/assets/img/posts/cloud-forense-saas/image-3.png)

![alt text](/assets/img/posts/cloud-forense-saas/image-4.png)

### Metadatos de Google Drive

Esta base de datos se encuentra en appdata/local/google/drivefs/metadata_sqlite_db

![alt text](/assets/img/posts/cloud-forense-saas/image-5.png)

Dentro de estab base de datos encontramos la tabla items.

| Columna           | Descripción                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| stable_id         | Identificador único del archivo                                                               |
| id                | Identificador del archivo en la nube (puede cruzarse con URLs de Google Drive y registros de auditoría) |
| trashed           | Indica si el archivo está en la Papelera de Google Drive (1 = Sí)                             |
| is_owner          | Muestra si el usuario es el propietario del archivo (1 = Sí)                                  |
| is_folder         | Distingue entre archivos (0) y carpetas (1)                                                   |
| local_title       | Nombre real del archivo                                                                       |
| file_size         | Tamaño del archivo en bytes                                                                   |
| modified_date     | Última fecha de modificación (formato Unix Epoch)                                             |
| viewed_by_me_date | Última vez que el usuario interactuó con el archivo                                           |
| shared_with_me_date | Indica si el archivo fue compartido (1 = Sí)                                                 |
| proto             | Datos binarios que contienen el hash MD5 del archivo (almacenados en formato protocol buffer) |

![alt text](/assets/img/posts/cloud-forense-saas/image-6.png)

### Caché de Archivos y datos eliminados

Estos datos se encuentran en AppData\Local\Google\DriveFS\ID de usuario\content_cache\

![alt text](/assets/img/posts/cloud-forense-saas/image-7.png)

En este caso por ejemplo se ha abierto un fichero txt que estaba compartido por lo que podemos ver en caché el respaldo sin modificar del mismo.

- Estos archivos temporales pueden persistir incluso después de ser eliminados de la nube.  
- Si un archivo fue abierto pero no guardado, es posible que aún exista en la caché.  
- Los archivos en caché carecen de los nombres de archivo originales, pero pueden ser emparejados mediante metadatos.

En la tabla items_properties podemos encontrar:

| Columna               | Descripción                                                                                   |
|-----------------------|-----------------------------------------------------------------------------------------------|
| pinned                | Indica si el archivo se almacenó offline (1 = Sí)                                             |
| trashed_locally       | Indica si el archivo fue eliminado localmente                                                 |
| trashed_locally_name  | Nombre original del archivo eliminado localmente (se encuentra en `$Recycle.Bin`)             |
| content-entry         | Confirma si el archivo está en caché local                                                    |
| drivefs.Zone.Identifier | Proporciona detalles sobre el origen del archivo (útil para identificar descargas)          |
| version-counter       | Registra modificaciones y revisiones del archivo                                              |
| Modified-date         | Hora de modificación del archivo reportada desde el sistema de archivos local                 |
| Local-title           | Nombre del archivo o carpeta                                                                  |

![alt text](/assets/img/posts/cloud-forense-saas/image-8.png)

Incluso si se han eliminado en la nube quedan registros del ID del archivo eliminado y algunos datos como su nombre.

![alt text](/assets/img/posts/cloud-forense-saas/image-9.png)

Utilizando web como [ProtoBuffer](https://protobuf-decoder.netlify.app/) podemos intentar ordenar un poco el contenido de estos buffers de datos que quedan tras la eliminación.

![alt text](/assets/img/posts/cloud-forense-saas/image-10.png)

### Flujo de Trabajo Forense: Investigando Google Drive para Escritorio

🔹 **Paso 1: Identificar el Uso de Google Drive en el Sistema**  
    - Verifica las claves del registro (`NTUSER\Software\Google\DriveFS\Share`).  
    - Identifica el punto de montaje de Google Drive y la letra de unidad asignada.  

🔹 **Paso 2: Extraer Metadatos y Listados de Archivos**  
    - Analiza `metadata_sqlite_db` para enumerar todos los archivos de Google Drive, incluidos los archivos solo en la nube.  
    - Revisa `item_properties` para archivos en caché y eliminados.  

🔹 **Paso 3: Recuperar Archivos Almacenados o Eliminados Localmente**  
    - Extrae archivos almacenados en caché localmente desde `content_cache`.  
    - Busca archivos eliminados en `$Recycle.Bin` y en la Papelera de Google Drive.  

🔹 **Paso 4: Investigar Compartición Externa y Fuga de Datos**  
    - Cruza los IDs de archivo con los registros de administración de Google Workspace.  
    - Rastrea descargas y eventos de compartición de archivos para detectar fugas de datos.  

🔹 **Paso 5: Correlacionar con Otros Artefactos Forenses**  
    - Compara la actividad de Google Drive con el historial del navegador, los Registros de Eventos de Windows y los datos de Prefetch.  
    - Busca accesos no autorizados desde direcciones IP sospechosas o inusuales.

### Bonus herramientas automáticas

Podemos encontrar multitud de herramientas creadas por la comunidad que nos pueden aportar alguna forma más ordenada u obtener datos que no encontramos manualmente.

[Enlace DriveFS-Sleuth](https://github.com/AmgdGocha/DriveFS-Sleuth)

![alt text](/assets/img/posts/cloud-forense-saas/image-11.png)

## OneDrive

### Ruta de instalación del servicio y configuración

Normalmente la ruta de instalación se encuentra en C:\Program Files\Microsoft OneDrive. 

![alt text](/assets/img/posts/cloud-forense-saas/image-12.png)

Aunque también es posible que en algunos equipos se encuentre en C:\Users\username\%AppData%\Local\Microsoft\OneDrive

En este caso como si se encuentra en archvos de programa, en appdata se guardan los datos correspondientes a la instalación, configuración, etc. 

![alt text](/assets/img/posts/cloud-forense-saas/image-13.png)

La mayoría de configuraciones y datos personales los encontramos en appdata\local\Microsoft\OneDrive\logs

![alt text](/assets/img/posts/cloud-forense-saas/image-14.png)

### Rutas de directorios sincronizados

En las claves de registro almacenadas en NTUSER.dat podemos extraer la siguiente información:

![alt text](/assets/img/posts/cloud-forense-saas/image-16.png)

| Columna           | Descripción                                                                                   |
|-------------------|-----------------------------------------------------------------------------------------------|
| UserFolder        | La ubicación actual de la carpeta de sincronización de OneDrive                               |
| cid/UserCid       | Un ID en nube de Microsoft único                                                              |
| UserEmail         | El correo electrónico utilizado para la cuenta de Microsoft                                  |
| LastSignInTime    | Timestamp de la última autenticación (formato Unix epoch)                                     |

![alt text](/assets/img/posts/cloud-forense-saas/image-17.png)

Si OneDrive está habilitado, esta clave del registro debe existir, por lo que se puede rastrear la actividad del usuario incluso si los archivos de OneDrive han sido movidos o eliminados.

### Metadatos y sincornización

%UserProfile%\AppData\Local\Microsoft\OneDrive\settings

En este directorio podemos encontrar algunos artefactos como:

- Rastrea tanto archivos locales como archivos solo en la nube.  
- Enumera nombres de archivos, estructura de carpetas y metadatos.  
- Proporciona marca de tiempo para las operaciones de sincronización de archivos.

En la base de datos de sincronización podemos encontrar las carpetas y los archivos que se encuentran sincronizados. 

![alt text](/assets/img/posts/cloud-forense-saas/image-19.png)

![alt text](/assets/img/posts/cloud-forense-saas/image-18.png)

Incluso los archivos solo en la nube (que no están almacenados localmente) se registran aquí, por lo que se pueden rastrear archivos eliminados o movidos que ya no existen en el dispositivo.

### Logs de actividad

%UserProfile%\AppData\Local\Microsoft\OneDrive\logs

Estos registros almacenan hasta 30 días de datos y registran:  
- Subidas y descargas de archivos  
- Renombrados y eliminaciones de archivos  
- Eventos de acceso a archivos compartidos

![alt text](/assets/img/posts/cloud-forense-saas/image-20.png)

Los archivos de registro pueden revelar la actividad de los archivos, incluso si el usuario eliminó las copias locales.  

Las marcas de tiempo en los registros .odl pueden correlacionar las transferencias de archivos con otras actividades del sistema.

![alt text](/assets/img/posts/cloud-forense-saas/image-21.png)

### OneDrive Business Microsoft 365

Si OneDrive Business está habilitado, esta clave del registro debe existir.

NTUSER\Software\Microsoft\OneDrive\Accounts\Business1

![alt text](/assets/img/posts/cloud-forense-saas/image-22.png)

- **UserFolder**: Ubicación de la carpeta raíz del almacenamiento local de archivos de OneDrive.  
- **UserEmail**: Correo electrónico asociado a la cuenta de Microsoft en la nube.  
- **LastSignInTime**: Fecha y hora de la última autenticación (tiempo en formato Unix epoch).  
- **ClientFirstSignInTimestamp**: Hora de la primera autenticación de la cuenta (tiempo en formato Unix epoch).  
- **SPOResourceID**: URL de SharePoint para la instancia de OneDrive.

![alt text](/assets/img/posts/cloud-forense-saas/5fb032_41ccc25bacff4cb09c9ac5b46844662b~mv2.png)

OneDrive permite compartir archivos y sincronizar carpetas entre múltiples cuentas. Las carpetas compartidas se rastrean bajo:

NTUSER\Software\Microsoft\OneDrive\Accounts\Personal\Tenants

NTUSER\Software\Microsoft\OneDrive\Accounts\Business1\Tenants

![alt text](/assets/img/posts/cloud-forense-saas/5fb032_cffb158b5b264d99b5ce77d11a90b955~mv2.png)

![alt text](/assets/img/posts/cloud-forense-saas/5fb032_097865a98a4946dbb1418827bc095251~mv2.png)

Esta clave registra las carpetas compartidas sincronizadas con OneDrive, rastrea archivos compartidos a través de Microsoft Teams y SharePoint.

Las carpetas compartidas pueden no almacenarse en la carpeta de OneDrive predeterminada.  

## Dropbox

### Ruta de instalación del servicio y configuración

La ruta de instalación por defecto la podemos encontrar en program files x86/dropbox

![alt text](/assets/img/posts/cloud-forense-saas/image-23.png)

### Artefactos principales

| Artefacto          | Ubicación                                               | Propósito                                                                 |
|--------------------|---------------------------------------------------------|---------------------------------------------------------------------------|
| Carpeta Local de Dropbox | `%UserProfile%\Dropbox\`                             | Almacena archivos sincronizados                                           |
| Archivos de Configuración | `%UserProfile%\AppData\Local\Dropbox\info.json`      | Contiene configuraciones de Dropbox y la ruta de sincronización           |
| Carpeta de Caché   | `%UserProfile%\Dropbox\.dropbox.cache\`                | Almacena archivos recientemente eliminados y archivos solo en la nube     |
| Bases de Datos de Sincronización | `%UserProfile%\AppData\Local\Dropbox\instance1\` | Registra la actividad de sincronización de archivos                       |
| Claves del Registro | `SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\SyncRootManager\Dropbox` | Identifica la ubicación y configuraciones de sincronización               |

### Detalles de configuración 

%UserProfile%\AppData\Local\Dropbox\

![alt text](/assets/img/posts/cloud-forense-saas/image-24.png)

Este archivo JSON almacena:  
- Ruta de la carpeta de sincronización (ubicación de almacenamiento personalizada)  
- Información del equipo de Dropbox (cuentas empresariales)  
- Tipo de suscripción (Básica, Plus, Business, Enterprise)

### Recuperación de archivos 

%UserProfile%\Dropbox\.dropbox.cache\

![alt text](/assets/img/posts/cloud-forense-saas/image-25.png)
 
- Una carpeta oculta presente en la raíz de la carpeta de archivos de Dropbox del usuario. Puede contener copias de archivos eliminados que aún no han sido purgados del almacén local de archivos.  
- Almacena en caché archivos solo en la nube que se han accedido recientemente.  
- Se limpia automáticamente cada 3 días.  

### Sincronización de archivos e historiales de modificación

%UserProfile%\AppData\Local\Dropbox\instance1\

En las bases de dato home.db y sync_history.db

![alt text](/assets/img/posts/cloud-forense-saas/image-26.png)

| Tabla           | Campo                          | Propósito                                                                 |
|-----------------|--------------------------------|---------------------------------------------------------------------------|
| recents         | server_path, timestamp         | Archivos actualizados recientemente, con su ruta en el servidor y marca de tiempo. |
| starred_items   | server_path, is_starred, timestamp | Archivos marcados como "importantes", con su ruta en el servidor, estado de marcado y marca de tiempo. |
| sfj_resources   | server_path, server_fetch_timestamp | Rastrea la última sincronización desde la nube, con la ruta del archivo en el servidor y la marca de tiempo de sincronización. |


![alt text](/assets/img/posts/cloud-forense-saas/image-27.png)

| Campo          | Propósito                                                                 |
|----------------|---------------------------------------------------------------------------|
| file_event_type | Tipo de acción realizada (agregar, eliminar, editar)                      |
| direction       | Dirección de la transferencia: Carga = Local → Nube, Descarga = Nube → Local |
| local_path      | Ruta completa del archivo en el sistema local                            |
| timestamp       | Hora de la última actividad relacionada con el archivo                   |
| other_user      | "1" indica que el archivo pertenece a otro usuario                       |


### Recuperación de archivos ocultos y bases de datos encriptadas

En Dropbox podemos encontrar varias bases de datos con información importante pero que se encuentran encriptadas.

Hace unos años atrás estas bases de datos utilizaban el sistema DPAPI de windows para encriptar los datos. Estas llaves se almacenaban en el registro de windows perteneciente a los usuarios de Dropbox.

Podíamos obtener esta clave del archivo NTUSER.DAT.

Anteriormente gran parte de las bases de datos que hemos observado en los apartados anteriores se encontraban encriptadas, lo que actualmente no es así por lo que quizás hayan cambiado la forma en la que se almacenan estos datos.

Si nos fijamos en la base de datos config.dbx la cual contiene la información de la cuenta de Dropbox esta si se encuentra cifrada. 

Igualemente a continuación adjunto un programa para poder descifrar los archivos DBX de dropbox.

[Data Protecton Decryptor](https://www.nirsoft.net/utils/dpapi_data_decryptor.html)

Los archivos DBX  son archivos SQLite cifrados utilizando la extensión de cifrado SQLite Encryption Extension (SEE) para SQLite.

No todos los archivos DBX son SQLite cifrados: algunos son simples archivos SQLite, otros pueden ser archivos Base64, etc. Como profesionales de DFIR (Digital Forensics and Incident Response), no debemos confiar en las extensiones de archivo , ¿verdad? Antes de intentar descifrarlos, echemos un vistazo crudo a los archivos.   

Existen dos claves del registro (valores)  que contienen las claves de los usuarios de Dropbox, no solo una.

Estas dos claves del registro son blobs de DPAPI, por lo que necesitarás la contraseña de inicio de sesión del usuario (o su hash SHA1, véase "¡Happy DPAPI!") para poder descifrarlos.
Los valores del registro que contienen los blobs de DPAPI tienen datos antes (versión, longitud) y después (HMAC) de ellos.   

La seguridad de los archivos DBX  se basa únicamente en la seguridad de DPAPI (que, por cierto, es bastante robusta).
Los blobs de DPAPI utilizan una entropía fija (un secreto): d114a55212655f74bd772e37e64aee9b .   

Cuando se descifran, los blobs de DPAPI proporcionarán las llamadas Claves de Usuario , pero estas no descifrarán directamente los archivos DBX .
Las claves de descifrado de DBX se derivan de las Claves de Usuario utilizando PBKDF2 con 1066 iteraciones y una sal fija: 0D638C092E8B82FC452883F95F355B8E .   





