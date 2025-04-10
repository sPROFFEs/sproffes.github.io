---
title: Analisis Android/iOS - Caso práctico de análisis postmortem
date: 2025-04-10 11:00:00 +0000
categories: [Forense, Dispositivos moviles]
tags: [android, ios, análisis, postmortem]
image:
  path: /assets/img/posts/analisis-android-ios-postmortem/cabecera.png
  alt:  cabecera
description: >
  Ejemplo de analisis de imágenes postmortem de un dispositivo Android/iOS 
pin: false  
toc: true   
math: false 
mermaid: false 
---

Simularemos un escenario real en el que un analista forense debe extraer, preservar y examinar evidencias digitales de un dispositivo móvil, integrando tanto técnicas de volcado físico como análisis de los artefactos generados por diversas aplicaciones instaladas y configuradas en el dispositivo.

Como ya vimos en post anteriores la posibilidad de realizar un volcado "completo" en función de la situación que encontremos, en este caso vamos a utilizar dos imágenes tanto de [Android](https://drive.google.com/file/d/1AiMDFlSRHuEeAxw4mgzlISnflB_DB-D9/view) como de [IOS](https://drive.google.com/file/d/1QTc67TzenAjQU-70DHbPi4uP7VreL0zV/view) que podréis descargar.


## Análisis manual de una imágen Android

Dispositivo Android 11, basado en un Google Pixel 3, que ha sido sometido a un proceso controlado de generación de imagen forense.

### 🛠️ Detalles del Sistema y Versión de Android

El dispositivo opera con **Android 11**, utilizando una **imagen stock** proporcionada por Google.  
**Build:** `RP1A.200720.009`  
**Nivel de Parche de Seguridad:** `5 de septiembre de 2020`

#### 📱 Especificaciones del Dispositivo

- **Marca:** Google Pixel 3  
- **Modelo:** G013A  
- **Almacenamiento:** 64 GB  
- **RAM:** 4 GB  
- **Carrier:** Google Fi  
- **Número de Teléfono:** 919-579-4674  
- **Serial:** 8CEX1N716  
- **Wi-Fi MAC:** 7c:d9:5c:ac:a2:cf  
- **Bluetooth MAC:** 7c:d9:5c:ac:a2:ce  

#### 🔍 Proceso de Generación de la Imagen Forense

1. **Restablecimiento a Fábrica:**  
   Se realizó flasheo con una imagen stock limpia.

2. **Configuración Inicial:**  
   Se añadió una cuenta de Google Fi para habilitar el servicio celular.

3. **Acceso Root:**
   - Desbloqueo del bootloader  
   - Instalación de **Magisk** para obtener privilegios root

4. **Población de Datos:**  
   Se instalaron **46 aplicaciones no nativas** desde Google Play, junto a las apps stock, y se introdujeron datos mediante su uso funcional.

5. **Extracción de Datos:**  
   Se realizó una **extracción lógica** usando el software `Magnet Acquire`.

---

### 🔧 Configuración y Dispositivo

1. **Propiedades del dispositivo**  
   - Android ID, nombre y nombre Bluetooth o dispositivos enlazados 
   - 📂 `\data\system\users\%USERNUMBER%\settings_secure.xml`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-1.png)

- Bluetooth address.

A partir de Android 6.0 (Marshmallow), el acceso directo a identificadores de hardware como la dirección MAC de Bluetooth está restringido por razones de privacidad y seguridad. Esto significa que, en versiones más recientes del sistema operativo, es posible que este valor no esté disponible o esté protegido.

También podría encontrarse en el archivo `/data/misc/bluedroid/bt_config.conf`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-2.png)


```xml
 <setting id="25" name="android_id" value="630b81bde1ed068a" package="android" defaultValue="630b81bde1ed068a" defaultSysSet="true" />
 <setting id="68" name="bluetooth_name" value="Pixel 3" package="android" defaultValue="Pixel 3" defaultSysSet="true" />
```

---

### 📇 Contactos y Comunicaciones

2. **Lista de contactos**  
   - 📂 `data/com.android.providers.contacts/databases/contacts2.db`  
3. **Registro de llamadas**  
   - 📂 `data/com.android.providers.contacts/databases/calllog.db`  

- Contactos

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-5.png)

- Llamadas

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-7.png)


4. **Mensajes SMS**  
   - 📂 `/data/com.android.providers.telephony/databases/mmssms.db`  

- SMS

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-6.png)

---

### 📶 Redes y Conectividad

5. **Redes Wi-Fi utilizadas**  
   - 📂 `data/misc/apexdata/com.android.wifi/WifiConfigStore.xml`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-8.png)

6. **Dispositivos Bluetooth emparejados**  
   - 📂 `data/misc/bluedroid/bt_config.conf`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-9.png)

---

### 🖼️ Multimedia y Mensajería

7. **Fotos, documentos y multimedia**  
   - Incluye archivos de WhatsApp, Signal, Telegram, Kik, y Snapchat  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-10.png)

8. **Aplicaciones instaladas**  
   - 📂 `data/user/XXXX/com.android.vending/databases/localappstate.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-12.png)

9. **Búsquedas en Play Store**  
   - 📂 `com.android.vending/databases/suggestions.db`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-13.png)

---

### 👤 Cuentas y Actividad del Usuario

10. **Cuentas de usuario registradas**  
    - Configuradas 2 cuentas de Google  
    - 📂 `/system_ce/0/accounts_ce.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-3.png)

    - 📂 `/system_de/0/accounts_de.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-4.png)   

    - 📂 `/system_de/10/accounts_de.db` 

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-11.png)

    - 📂 `data/com.android.vending/shared_prefs/lastaccount.xml`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-14.png)

11. **Estadísticas de uso de apps**  
    - 📂 `\data\user\%USERNUMBER%\com.google.android.apps.turbo\shared_prefs\app_usage_stats.xml`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-15.png)

12. **Eventos de uso de apps y dispositivo**  
    - 📂 `\data\data\com.google.android.apps.wellbeing\databases\app_usage.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-16.png)

13. **Actividades de aplicaciones y servicios**  
    - 📂 `\data\data\com.google.android.as\databases\reflection_gel_events.db`

Esta almacena información utilizada por los Servicios de Personalización del Dispositivo (DPS), que recopilan diversas estadísticas de uso para predecir y sugerir aplicaciones y contenido al usuario.
Una característica destacada de esta base de datos es que puede conservar registros de aplicaciones que fueron eliminadas del dispositivo.
Los artefactos de reflection_gel_events.db pueden ayudar a establecer una línea de tiempo detallada de eventos en el dispositivo durante un periodo de tiempo más amplio que el que registran los datos de Digital Wellbeing.
Aunque en este caso no encontramos esta base de datos en el dispositivo.

---

### 📲 Redes Sociales y Mensajería

14. **Facebook Messenger**  
    - 📂 `data/user/0/com.facebook.orca/databases/threads_db2`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-22.png)

15. **Instagram**  
    - 📂 `data/user/0/com.instagram.android/databases/direct.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-23.png)

16. **Twitter**  
    - 📂 `data/user/0/org.Twitter.messenger/databases/xxxxxxxxxxxxxx-61.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-25.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-24.png)

17. **Telegram**  
    - 📂 `data/user/0/org.telegram.messenger/files/cache4.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-26.png)

Son mensajes cortos o los últimos que se han enviado ya que es la cache de Telegram.

18. **TikTok**  
    - 📂 `data/user/0/com.zhiliaoapp.musically/databases/xxxxxxxxxxxxxxx_im.db`  

Normalmente TikTok no guarda mensajes de forma local pero podemos encontrar multitud de cosas como imagenes, videos, etc. o incluso algunos mensajes cacheados.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-27.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-28.png)

19. **Snapchat**  
    - 📂 `data/user/0/com.snapchat.android/databases/main.db`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-29.png)

20. **Signal**  
    - 📂 `/data/user/0/org.thoughtcrime.securesms/databases/signal.db`
    - 📂 `/data/misc/keystore/user_0/10244_USRSKEY_SignalSecret`
    - 📂 `/data/user/0/org.thoughtcrime.securesms\shared_prefs\org.thoughtcrime.securesms_preferences.xml`

La base de datos de Signal se encuentra encriptada por lo que debemos seguir el siguiente proceso para poder acceder al contenido.

Signal utiliza el método de cifrado AES en modo GCM para cifrar su base de datos mediante SQLCipher.
Primero, se obtiene la clave SQLCipher, y luego se utiliza una clave AES-GCM derivada de USERKEY + IV para cifrar la base de datos.
Estos valores se almacenan en el archivo org.thoughtcrime.securesms_preferences.xml.
Para descifrar la base de datos, es necesario invertir el proceso para obtener la clave SQLCipher.

Aunque actualmente no he conseguido acceder a la base de datos de Signal.

21. **ProtonMail**  
    - 📂 `/data/user/0/ch.protonmail.android/databases/db-mail`  

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-30.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-31.png)

El contenido del mail está encriptado con GPG y la clave privada se almacena en los servicios de ProtonMail. 

22. **WhatsApp**  
       - 📂 `/data/data/com.whatsapp/databases/msgstore.db`
       - 📂 `/data/media/0/com.whatsapp/databases/msgstore.db.crypt12`
       - 📂 `/data/data/com.whatsapp/files/key`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-32.png)

Link de la herramienta [Whatsapp-Viewer](https://github.com/andreas-mausch/whatsapp-viewer/releases/tag/v1.15)

---

### 🌐 Navegación Web y Mapas

23. **Historial de Chrome**  
    - 📂 `data\data\com.android.chrome\app_chrome\default\history`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-17.png)

24. **Historial de Firefox**  
    - 📂 `data\data\org.mozilla.firefox\files\places.sqlite`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-18.png)

25. **Mensajes de Gmail y adjuntos**  
    - 📂 `data\data\com.google.android.gm\databases\bigTopDataDB`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-19.png)

26. - `data\data\com.google.android.gm\files\downloads\xxxxx\attachments\xxxxx`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-20.png)

26. **Historial de Google Maps**  
    - 📂 `data/data/com.google.android.apps.maps/databases/gmm_sync.db`

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-21.png)

---

## 🕵️‍♂️ Análisis Forense de iPhone SE con iLEAPP"

El análisis parte de un **backup lógico sin jailbreak**, generado con la utilidad `checkra1n`.

---

### 📱 Detalles del Dispositivo

- **Make:** iPhone SE  
- **Modelo:** A1662 (Rose Gold)  
- **Número de orden:** MLXL2LL/2  
- **RAM:** 2 GB  
- **Almacenamiento:** 64 GB  
- **Carrier:** Google Fi  
- **Número de teléfono:** 919-579-4674  
- **Serial:** DX3T126VH2XV  
- **Wi-Fi MAC:** A0:D7:95:79:DD:A1  
- **Bluetooth MAC:** A0:D7:95:79:DD:A2  
- **Versión iOS:** 13.4.1 (Build 17E262)  
- **Código de desbloqueo:** 0731  

---

### 🧰 Adquisición Forense

#### 📦 1. Backup lógico vía iTunes  
- ✅ **Método:** Sin jailbreak  
- 🔐 **Formato:** `.zip`  
- 🔑 **Contraseña del backup cifrado:** `mypassword123`  
- 📁 [Pulsa aquí para obtener el fichero de backup](#)

---

#### 💾 2. Imagen completa del dispositivo (Magnet Acquire)  
- 💻 **Herramienta:** Magnet Acquire  
- 🧍 **Tipo:** Volcado físico completo  
- 📁 [Pulsa aquí para obtener la imagen](#)  
- 📄 Esta imagen será utilizada para un segundo informe posterior.

---

### 🛠️ Herramientas a utilizar

#### 🧩 iLEAPP  
- **Nombre completo:** *iOS Logs, Events, and Preferences Parser*  
- **Creadores:** Alexis Brignoni & Yogesh Khatri  
- 📊 **Uso:** Permite extraer artefactos clave desde respaldos iOS/iTunes  
- 🔍 Especialmente útil para artefactos como:
  - Historial de llamadas
  - Ubicaciones
  - Preferencias de usuario

[Github](https://github.com/abrignoni/iLEAPP)

#### 🔓 iTunes Backup Explorer  
- Permite explorar y decodificar archivos de respaldo de iOS cifrados.
- Útil para convertir el contenido del `.zip` a una estructura navegable y analizable por iLEAPP.

[Github](https://github.com/MaxiHuHe04/iTunes-Backup-Explorer)

---

### 🛠️ Proceso

Descargamos las herramientas y extraemos el backup .zip del dispositivo.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-33.png)

Este zip es el backup que crea ITunes y debemos descomprimirlo.

Ahora en Itunes Backup Explorer importamos el manifest.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-34.png)

Introducimos la contraseña que se estableció durante el proceso de generación del backup. (mypassword123)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-35.png)

Seleccionamos todo y exportamos el contenido.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-36.png)

Ahora seleccionamos como entrada la carpeta que hemos extraido y creamos una nueva para el la salida.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-37.png)

Finalmente le damos a "process".

Tras el procso nos crea un html con todos los artefactos extraídos.

### 📑 Revisión del Informe iLEAPP

Al finalizar el análisis, **iLEAPP** generará un informe en formato **HTML** con múltiples pestañas organizadas por tipo de artefacto.  

---

- **🌐 Safari**  
  Historial de navegación que puede indicar hábitos, búsquedas o sitios visitados relevantes.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-38.png)

- **📍 Location Services**  
  Registros de localización GPS del dispositivo, útil para establecer presencia geográfica en fechas específicas.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-39.png)

- **💬 iMessage / SMS**  
  Conversaciones tanto de iMessage como de SMS, incluidas fechas, contactos y contenido de los mensajes.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-40.png)

- **📦 Installed Apps**  
  Lista completa de aplicaciones instaladas, incluyendo fecha de instalación y uso, útil para evaluar contexto de actividad del usuario.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-41.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-42.png)

- **📶 Network Connections**  
  Muestra redes Wi-Fi conocidas, junto con SSIDs y fechas de conexión, lo cual permite inferir ubicaciones o rutinas.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-43.png)

- **🔒 Lockdown / Device Info**  
  Información detallada del dispositivo, versión de iOS, dispositivos conectados, etc.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-44.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-45.png)


---

## Análsis sin necesidad de Itunes Backup Explorer

Si no disponemos de el backup del dispositivo, podemos realizar un análisis de la imagen completa del dispositivo, como [esta](https://drive.google.com/file/d/1j7fUmxzmk_R2fWP9v1XFPGfEef3wUAXd/view).

Esta vez seleccionaremos directamente el archivo .tar

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-46.png)

Ahora en el nuevo reporte podremos ver muchos más artefactos.

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-47.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-48.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-49.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-50.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-51.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-52.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-53.png)

![alt text](/assets/img/posts/analisis-android-ios-postmortem/image-54.png)