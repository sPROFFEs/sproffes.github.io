---
categories:
- Forense
- Navegadores
date: 2024-12-20 11:58:38 +0000
lang: es
tags:
- forense
- browsers
- chrome
- firefox
- edge
title: Evidencias en los Navegadores Web
---

Los navegadores web son herramientas que se utilizan en diversos dispositivos, como teléfonos móviles, tabletas, netbooks y ordenadores de escritorio. Además de permitir la navegación por internet, también pueden emplearse para explorar los archivos almacenados en el propio dispositivo.

La memoria caché del navegador puede guardar diversos tipos de contenido descargado, como imágenes, videos, documentos, programas ejecutables y scripts. Asimismo, los navegadores pueden almacenar datos introducidos por los usuarios en formularios, como búsquedas, nombres de usuario, contraseñas para correos electrónicos, redes sociales, sitios web y datos financieros, incluidos números de tarjetas de crédito.

Los marcadores y el historial de búsquedas también pueden proporcionar información sobre los intereses o actividades del propietario del dispositivo, lo que puede ser útil en investigaciones.

Cada navegador web deja sus propios artefactos individuales en el sistema operativo. Los tipos de artefactos del navegador web pueden variar según la versión del navegador web. Normalmente, al investigar artefactos de navegadores web, puede extraer los siguientes tipos de artefactos:

* Historial de navegación
* Ficheros en el directorio cache
* Cookies
* URL escritas
* Sesiones
* Sitios más visitados
* Capturas de pantalla
* Valores de formulario (búsquedas, autocompletar)
* Archivos descargados (Descargas)
* Favoritos

## Recolección de evidencias

### Microsoft Edge

```plaintext
Historial de navegación - %localappdata%\Microsoft\Edge\User Data\Default\History

Caché - %localappdata%\Microsoft\Edge\User Data\Default\Cache

Cookies - %localappdata%\Microsoft\Edge\User Data\Default\Cookies

Thumbnails - %localappdata%\Microsoft\Edge\User Data\Default\Cache\Cache_Data

Sesiones - %localappdata%\Microsoft\Edge\User Data\Default\Sessions

Valores de formulario - %localappdata%\Microsoft\Edge\User Data\Default\Web Data

Historial de descargas - %localappdata%\Microsoft\Edge\User Data\Default\History

Favoritos - %localappdata%\Microsoft\Edge\User Data\Default\Bookmarks
```

### Firefox

```plaintext
Historial de navegación - %appdata%\Mozilla\Firefox\Profiles\[Perfil]\places.sqlite

Ficheros en el directorio caché - %localappdata%\Mozilla\Firefox\Profiles\[Perfil]\cache2

Cookies - %appdata%\Mozilla\Firefox\Profiles\[Perfil]\cookies.sqlite

Thumbnails - %appdata%\Local\Mozilla\Firefox\Profiles\eqainsr.default-release\cache2\entries

Sesiones - %appdata%\Roaming\Mozilla\Firefox\Profiles\[nombre del perfil]\

Valores de formulario - %appdata%\Mozilla\Firefox\Profiles\[Perfil]\formhistory.sqlite

Archivos descargados (Descargas) - %appdata%\Mozilla\Firefox\Profiles\[Perfil]\places.sqlite

Favoritos - %appdata%\Mozilla\Firefox\Profiles\[Perfil]\places.sqlite
```

### Google Chrome

```plaintext
Historial de navegación - %localappdata%\Google\Chrome\User Data\Default\History

Ficheros en el directorio caché - %localappdata%\Google\Chrome\User Data\Default\Cache

Cookies - %localappdata%\Google\Chrome\User Data\Default\Cookies

Sesiones - %localappdata%\Google\Chrome\User Data\Default\Sessions

Thumbnails - %localappdata%\Google\Chrome\User Data\Default\Cache\Cache_Data

Valores de formulario - %localappdata%\Google\Chrome\User Data\Default\Web Data

Archivos descargados (Descargas) - %localappdata%\Google\Chrome\User Data\Default\History

Favoritos - %localappdata%\Google\Chrome\User Data\Default\Bookmarks
```

### Nota

Tanto en chrome como firefox podemos tener varios usuarios.

El nombre de la carpeta que contenga los datos varía en función de esto, por ejemplo:

Firefox - los perfiles se almacenan en carpetas con nombre generados de forma nombre.default, etc...

Chrome - los prefiles se almacenan en carpetas según el número del perfil, si no se ha creado ninguno nuevo será Default.

![Firefox](/assets/img/posts/artefactos_en_los_navegadores/20241220_164956_2024-12-20_17-49.png)
_Firefox_

![Chrome](/assets/img/posts/artefactos_en_los_navegadores/20241220_165007_2024-12-20_17-49_1.png)
_Chrome_

## Historial de navegación

[Browsing History View](https://www.nirsoft.net/utils/browsing_history_view.html)

### Edge, Chrome y Firefox

![Browsing History](/assets/img/posts/artefactos_en_los_navegadores/20241220_170817_2024-12-20_18-08.png)

![Browsing History Demo](/assets/img/posts/artefactos_en_los_navegadores/20241220_171104_Peek_2024-12-20_18-10.gif)

## Caché

[Mozilla cache viewer (GECKO)](https://www.nirsoft.net/utils/mzcacheview.zip)

[Chrome caché viewer (CHROMIUM)](https://www.nirsoft.net/utils/chromecacheview.zip)

### Chrome

![Chrome Cache](/assets/img/posts/artefactos_en_los_navegadores/20241220_171915_Peek_2024-12-20_18-19.gif)

### Edge

![Edge Cache](/assets/img/posts/artefactos_en_los_navegadores/20241220_172024_Peek_2024-12-20_18-20.gif)

### Firefox

![Firefox Cache](/assets/img/posts/artefactos_en_los_navegadores/20241220_172153_Peek_2024-12-20_18-21.gif)

## Cookies

[MZCookiesView](https://www.nirsoft.net/utils/mzcv-x64.zip)

[ChromeCookiesView](https://www.nirsoft.net/utils/chromecookiesview-x64.zip)

### Nota

Antes de acceder a los archivos de las cookies es necesario finalizar por completo los procesos del navegador ya que si no bloquea estos archivos

### Edge

![Edge Cookies](/assets/img/posts/artefactos_en_los_navegadores/20241220_173806_Peek_2024-12-20_18-38.gif)

### Chrome

![Chrome Cookies](/assets/img/posts/artefactos_en_los_navegadores/20241220_173815_Peek_2024-12-20_18-37.gif)

### Firefox

![Firefox Cookies](/assets/img/posts/artefactos_en_los_navegadores/20241220_174935_Peek_2024-12-20_18-49.gif)

## Thumbnails

[ImageCaché viewer](https://www.nirsoft.net/utils/imagecacheviewer.zip)

### Edge

![Edge Thumbnails](/assets/img/posts/artefactos_en_los_navegadores/20241220_182919_Peek_2024-12-20_19-29.gif)

### Chrome

![Chrome Thumbnails](/assets/img/posts/artefactos_en_los_navegadores/20241220_183024_Peek_2024-12-20_19-30.gif)

### Firefox

![Firefox Thumbnails](/assets/img/posts/artefactos_en_los_navegadores/20241220_183113_Peek_2024-12-20_19-31.gif)

## Favoritos

[WebBookmarks view](https://www.nirsoft.net/utils/webbrowserbookmarksview.zip)

![Bookmarks](/assets/img/posts/artefactos_en_los_navegadores/20241220_184827_Peek_2024-12-20_19-48.gif)

## Archivos descargados

[BrowserDownloads viewer](https://www.nirsoft.net/utils/browserdownloadsview.zip)

![Downloads](/assets/img/posts/artefactos_en_los_navegadores/20241220_185321_Peek_2024-12-20_19-53.gif)

## Valores de formulario

[Web Browser pass view - password (wbpv28821@)](https://www.nirsoft.net/toolsdownload/webbrowserpassview.zip)

[Browser AutoFill view](https://www.nirsoft.net/utils/browserautofillview.zip)

![BrowserAutoFillView](/assets/img/posts/artefactos_en_los_navegadores/20241220_190429_Peek_2024-12-20_20-04.gif)
_BrowserAutoFillView_

![WebBrowserPassView](/assets/img/posts/artefactos_en_los_navegadores/20241220_190627_Peek_2024-12-20_20-05.gif)
_WebBrowserPassView_

## Bonus - Búsquedas

[MyLastSearch](https://www.nirsoft.net/utils/mylastsearch.zip)

![Search History](/assets/img/posts/artefactos_en_los_navegadores/20241220_191529_Peek_2024-12-20_20-15.gif)