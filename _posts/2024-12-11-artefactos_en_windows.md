---
title: Análisis Post-mortem - Artefactos en Windows
date: 2024-11-12 11:58:38 +0000
categories: [Forense, Windows]
tags: [forense, windows, analisis, artefactos]
img_path: /assets/img/posts/artefactos_en_windows
---


## Prefetch

### ¿Qué son?

Un prefetch o precarga es una característica de windows que mejora el rendimiento del sistema operativo. Al inicio, el sistema operativo realiza un seguimiento de los programas que se abren habitualmente, guarda la información y aprende del uso para que el sistema haga un pre-inicio del software de uso habitual por lo que se dice que se realiza un "prefetch"

### ¿Cómo se almacena?

Para almacenar esta información windows crea una ruta de precarga donde almacena estos archivos con extensión "pf" y podemos encontrarlos en %WINDIR%\prefetch. Para cada programa ejecutado se genera un archivo prefetch que contiene información sobre el programa, como son el path, la fecha y hora de modificación creación y última vez que se ejecutó, así como una lista de las dependencias cargadas por la aplicación en los primeros 30 segundos de su ejecución.

### ¿Qué información es util desde un punto de vista forense?

Estos archivos también almacenan información sobre el disco, GUID y marcas de creación de la unidad. Se almacena para todos los volúmenes y es util para poder identificar GUIDs de unidades externas. En algunas periciales es interesante este dato y se puede comparar con las unidades externas utilizadas para poner en marcha las aplicaciones o para descubrir los archivos que han sido abiertos desde el propio dispositivo o disco duro externo y puede ser importante reflejar esto en el análisis pericial.

## LOGs

### ¿Que són?

Es un registro de eventos durante un rango de tiempo en particular. Se utiliza para registrar datos o información sobre quién, qué, cuándo, dónde y por qué un evento ocurre para un dispositivo en particular o para una aplicación concreta.

### Los más importantes por su contenido

A pesar de que existen numerosos registros que windows realiza, dentro de los más interesantes por su valor o contenido pericial podemos encontrar los siguientes:

#### `%WINDIR%\setupact.log`

Contiene información acerca de las acciones de instalación durante la misma.

**EVIDENCIAS**: Podemos ver fechas de instalación, propiedades de programas instalados, rutas de acceso, copias legales, discos de instalación…

#### `%WINDIR%\Debug\mrt.log`

Resultados del programa de eliminación de software malintencionado de Windows.

**EVIDENCIAS**: Fechas, Versión del motor, firmas y resumen de actividad.

#### `%WINDIR%\Logs\CBS\CBS.log`

Ficheros pertenecientes a "Windows Resource Protection" y que no se han podido restaurar.

**EVIDENCIAS**: Proveedor de almacenamiento, PID de procesos, fechas, rutas…

#### `%AppData%\setupapi.log`

Contiene información de unidades, services pack y hotfixes.

**EVIDENCIAS**: Unidades locales y extraibles, programas de instalación, programas instalados, actualizaciones de seguridad, reconocimiento de dispositivos conectados…

#### `%WINDIR%\INF\setupapi.dev.log`

Contiene información de unidades Plug and Play y la instalación de drivers.

**EVIDENCIAS**: Versión de SO, Kernel, Service Pack, arquitectura, modo de inicio, fechas, rutas, lista de drivers, dispositivos conectados, dispositivos iniciados o parados…

#### `%WINDIR%\Performance\Winsat\winsat.log`

Contiene trazas de utilización de la aplicación WINSAT que miden el rendimiento del sistema.

**EVIDENCIA**: Fechas, valores sobre la tarjeta gráfica, CPU, velocidades, puertos USB…

#### `*.INI`

Contiene configuraciones de programas

**EVIDENCIA**: Rutas, secciones, parámetros de usuarios…

#### `%WINDIR%\Memory.dmp`

Contiene información sobre los volcados de memoria.

**EVIDENCIA**: Rutas, programas, accesos, direcciones de memoria, listado de usuarios, contraseñas, conexiones…

#### `%WINDIR%\System32\config%WINDIR%\System32\winevt\Logs`

Contiene los logs de Windows accesibles desde el visor de eventos.

**EVIDENCIAS**: Casi todas. Entradas, fechas, accesos, permisos, programas, usuario, etc…

#### `%PROGRAMDATA%\Microsoft\Microsoft Antimalware\Support %PROGRAMDATA%\Microsoft\Microsoft Security Client\Support`

Logs del motor de antimalware

**EVIDENCIAS**: Fechas, versión del motor, programas analizados, actividad del malware…

## Fichero de hibernación en Windows

### ¿Qué es?

El archivo *hiberfil.sys* es un fichero especial que almacena el estado completo de la memoria RAM de una sistema cuando esta entra en modo de hibernación.

Su tamaño es igual a la cantidad total de memoria RAM instalada en el equipo y contiene una versión comprimida de los datos en memoria.

Su creación es posible solo si el hardware de la máquina cumple con los estándares *ACPI* y *Plug-and-Play*.

Para interactuar con este archivo o analizarlo, generalmente se requieren herramientas especializadas debido a su formato comprimido.

### ¿Cómo ver su contenido?

Por ejemplo, el WindowsMemory Toolkit de Moonsols (ahora conocido como Comae) incluye herramientas como hibr2bin, que permiten extraer y mostrar los datos almacenados en el archivo hiberfil.sys.

Esta herramienta convierte la información comprimida del archivo en un formato legible para su análisis.

También se puede transformar archivos de hibernación en una imagen sin procesar utilizando el framework *Volatility*, que incluye un módulo especializado para crear una imagen legible a partir del archivo de hibernación. Una vez que se obtiene esta imagen lineal, resulta muy fácil examinar su contenido. Otra herramienta práctica es *Strings*, que permite localizar cadenas de texto dentro del archivo de hibernación. Esto facilita una evaluación rápida de su contenido sin necesidad de generar una imagen completamente legible.

### Importancia

La información contenida en el archivo hiberfil.sys puede ser extremadamente importante, dependiendo del contexto en el que se analice.

En investigaciones digitales puede proporcionar una instantánea del estado de la memoria en el momento en que el sistema entró en hibernación. Esto incluye programas abiertos, documentos en uso, conexiones activas y datos sensibles que estaban cargados en la RAM.

Puede ser útil para recuperar información perdida o no guardada, como el contenido de un archivo que estaba siendo editado pero no fue almacenado antes de la hibernación.

Los desarrolladores y técnicos pueden usar el contenido del archivo para analizar errores del sistema, depurar aplicaciones o identificar conflictos de hardware o software.

Puede contener información sensible, como contraseñas, claves de cifrado o datos personales. Por ello, es crucial protegerlo en sistemas críticos, ya que puede representar un riesgo de seguridad si cae en manos equivocadas.

## Volume shadow copies service (VSS)

El Shadow Copy, también conocido como Volume Snapshot Service, Volume Shadow Copy Service o simplemente VSS, es una tecnología integrada en Microsoft Windows que permite crear copias de seguridad, ya sea de forma automática o manual, de archivos o volúmenes, incluso si están en uso. Este servicio funciona directamente sobre el sistema de archivos, garantizando que se puedan realizar snapshots consistentes sin interrumpir las operaciones normales del sistema.

Esta tecnología necesita que el sistema de archivos sea NTFS para poder crear y almacenar las copias que pueden ser creadas en local y en dispositivos externos, bien en dispositivos en red o dispositivos locales.

### ¿Viene activada por defecto o la tiene que activar el usuario?

El servicio Volume Shadow Copy (VSS) está habilitado de forma predeterminada en sistemas Windows para funciones específicas, como la Restauración del Sistema y Copias de Seguridad de Windows, pero no siempre está configurado para realizar snapshots automáticos de todos los volúmenes.

### ¿Cada cuánto tiempo se realizan?

Depende de cómo esté configurado el sistema y el propósito para el cual se usa el servicio Volume Shadow Copy (VSS).

**Restauración del Sistema**

En Windows, los puntos de restauración del sistema, que utilizan VSS, suelen crearse automáticamente una vez al día o cuando se produce un evento significativo, como:

- La instalación de una actualización del sistema.
- Cambios en el software o configuración importantes.
- Instalación de controladores.

**Copias de Sombra para Volúmenes Específicos**

Si se configura manualmente VSS para un volumen, la frecuencia de las copias dependerá de la programación establecida. Por ejemplo:

En un entorno empresarial con servidores Windows, las copias de sombra a menudo se programan para realizarse varias veces al día, como cada 4 o 6 horas, según las necesidades.

En sistemas no configurados explícitamente, no se realizan copias periódicas, y el usuario debe iniciarlas manualmente.

### Ejemplos

#### Recuperación de Archivos Modificados o Eliminados Accidentalmente

**Contexto:**
Un empleado está trabajando en un archivo importante y accidentalmente borra o sobrescribe información crítica. El archivo se encuentra almacenado en una carpeta compartida de la red.

**Utilidad de las Copias de Sombra:**
Si las copias de sombra están habilitadas en el servidor o sistema donde se almacena el archivo, se puede acceder a versiones anteriores del documento. Esto permite restaurar una versión específica del archivo desde el Explorador de Windows, evitando la pérdida de datos críticos sin necesidad de recurrir a una copia de seguridad completa.

#### Diagnóstico y Mitigación de Ransomware

**Contexto:**
Una computadora o servidor es infectado por ransomware, y el malware cifra los archivos del sistema, haciéndolos inaccesibles.

**Utilidad de las Copias de Sombra:**
Si las copias de sombra están configuradas en el sistema antes del ataque, el administrador puede intentar recuperar versiones anteriores de los archivos desde las copias de sombra, lo que puede mitigar parcialmente el impacto del ransomware. Aunque algunos ransomware también intentan eliminar estas copias, si se han protegido correctamente, pueden servir como una línea de defensa adicional.

## Registro de Windows

El registro de Windows es una base de datos organizada de manera jerárquica que se utiliza para guardar configuraciones y opciones de los sistemas operativos Microsoft Windows.

En esta base de datos se almacena la configuración de componentes fundamentales del sistema operativo, así como la de las aplicaciones que funcionan en él. Entre los elementos que usan el registro están el kernel, los controladores de dispositivo, los servicios del sistema, el Administrador de Cuentas de Seguridad (SAM), la interfaz gráfica de usuario (GUI) y las aplicaciones de terceros.

Además, el registro permite que los controladores accedan a información que puede ser usada para generar un perfil del rendimiento del sistema.

### Cómo importar y exportar claves de registro en CLI y GUI

#### En el entorno GUI

- Exportar claves: Abre el Editor del Registro (regedit) como administrador, navega hasta la clave deseada, haz clic derecho, selecciona "Exportar" y guarda el archivo .reg
- Importar claves: Haz doble clic en un archivo .reg previamente exportado o selecciona "Archivo > Importar" dentro del Editor del Registro y elige el archivo.

#### En el entorno CLI

- Exportar: Usa el comando reg export [KeyPath] [FileName.reg], donde [KeyPath] es la ruta completa de la clave y [FileName.reg] el archivo de destino.
- Importar: Utiliza el comando reg import [FileName.reg], donde [FileName.reg] es el archivo que contiene las claves a importar​

### Claves interesantes desde el punto de vista forense

#### HKLM\SYSTEM:

Revela: Configuración del sistema, información sobre dispositivos conectados, y detalles de inicio y apagado. Útil para identificar patrones de actividad en un dispositivo.

#### HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run:

Revela: Programas configurados para ejecutarse al inicio del sistema. Puede ayudar a detectar malware o programas sospechosos.

#### HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs:

Revela: Archivos abiertos recientemente por el usuario, lo que aporta información sobre su actividad reciente.

#### HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings:

Revela: Configuración de navegación, como proxys y preferencias de red, que pueden mostrar comportamientos de navegación.

#### HKLM\SAM:

Revela: Base de datos de cuentas locales del sistema. Útil para analizar usuarios y contraseñas en investigaciones de acceso no autorizado.

#### HKLM\SYSTEM\CurrentControlSet\Enum\USBSTOR:

Revela: Dispositivos USB conectados históricamente, incluyendo nombres y marcas. Es clave para rastrear dispositivos externos conectados al sistema​

## Eventos EVTX

Los registros de eventos son archivos que almacenan información sobre eventos importantes que ocurren en el sistema, como cuando un usuario inicia sesión, se produce un error en un programa, o se realiza alguna acción clave en el sistema. Cada vez que ocurre uno de estos eventos, Windows lo registra en un archivo especial. Esta información puede ser consultada usando una herramienta llamada Visor de eventos.

Para los usuarios avanzados, los registros de eventos son muy útiles para solucionar problemas o investigar el comportamiento del sistema operativo y de otras aplicaciones.

Los registros de aplicaciones y servicios en Windows varían según el programa o servicio que se esté ejecutando. Estos registros incluyen información específica sobre las aplicaciones del sistema y registros más detallados relacionados con servicios particulares de Windows, proporcionando un panorama más granular del funcionamiento del sistema y sus componentes.

El formato EVTX fue introducido por Microsoft en Windows Vista y Server 2008, reemplazando el antiguo formato EVT que se utilizaba desde Windows NT 4.0. La principal razón de este cambio fue que el formato EVT original no podía adaptarse fácilmente a las crecientes demandas de complejidad del sistema moderno.

El nuevo formato EVTX incluye mejoras como:

- Nuevas características y propiedades de los eventos.
- El uso de canales para la publicación de eventos, lo que permite una mayor organización y filtrado.
- Un formato basado en XML, lo que facilita la interpretación y la integración con otros sistemas.
- Un nuevo Visor de eventos y un servicio de registro de eventos, que mejoran la forma en que se gestionan y visualizan los registros.

### ¿Cuáles pueden ser interesantes?

Desde un punto de vista forense, ciertos tipos de eventos son cruciales para la investigación, ya que pueden proporcionar detalles importantes sobre actividades sospechosas o incidentes de seguridad.

#### Eventos de seguridad (Auditoría)

Los eventos que indican intentos de inicio de sesión, especialmente aquellos que muestran errores de inicio de sesión o múltiples intentos fallidos, pueden ser indicativos de intentos de acceso no autorizado. Los registros de auditoría también incluyen eventos como cambios en las contraseñas o modificaciones en las cuentas de usuario.

Estos eventos permiten identificar acciones sospechosas o no autorizadas, como ataques de fuerza bruta o elevación de privilegios. Además, pueden mostrar si un atacante consiguió acceder a una cuenta de usuario o administrador.

#### Eventos del sistema

Los eventos de error del sistema, como caídas de servicios críticos o problemas con controladores de dispositivos, son relevantes. En particular, los errores que indican que un servicio del sistema (como el servicio de red o el servicio de autenticación) no se ha iniciado correctamente pueden ser señales de manipulación maliciosa.

Pueden ayudar a identificar problemas con la estabilidad del sistema o ataques que intentan desactivar servicios esenciales para ocultar actividades maliciosas. También pueden dar pistas sobre un malfuncionamiento de hardware que podría estar relacionado con un ataque físico.

## Herramientas a utilizar para análisis de artefactos

### FTK Imager

Es una herramienta esencial para la creación de imágenes forenses de discos, permitiendo trabajar con artefactos como ficheros de hibernación, Shadow Copies, y otros archivos del sistema.

También permite ver y exportar registros de eventos, ficheros eliminados y contenido en memoria, lo que la convierte en una herramienta clave en análisis forenses​.

### Arsenal Image Mounter

Esta herramienta permite montar imágenes de disco forenses en el sistema operativo como si fueran discos físicos.

Es útil para analizar contenido de imágenes de disco, incluyendo los artefactos relacionados con la caché, prefetch, y otros archivos del sistema. También es importante cuando se quiere acceder a archivos de Shadow Copies o registros de eventos sin alterar la imagen original​.

### Registry Explorer

Especializada en el análisis del registro de Windows, Registry Explorer permite a los investigadores examinar las claves del registro, lo que es esencial para encontrar detalles sobre configuraciones del sistema, actividades de usuarios, y rastrear posibles eventos de seguridad.

Es muy útil para la investigación forense de accesos y modificaciones en el sistema.

### RegRipper

RegRipper es una herramienta diseñada para extraer e interpretar los datos del registro de Windows.

Permite a los forenses obtener información detallada sobre el sistema, como el historial de programas ejecutados, la actividad de usuarios y las conexiones USB, lo que es útil para identificar actividades sospechosas o no autorizadas​.

### WRR (Windows Registry Recovery)

Esta herramienta está orientada a la recuperación de datos del registro de Windows.

Es útil para restaurar información del registro dañada o incompleta y obtener detalles importantes en situaciones donde el sistema haya sufrido daños o pérdida de datos​.

### LinkParser

Se especializa en analizar los registros de enlaces (Jump Lists) de Windows.

Esta herramienta es valiosa cuando se necesita rastrear las aplicaciones recientemente usadas por un usuario, identificando accesos a archivos o programas específicos, y obteniendo una línea de tiempo sobre el comportamiento del usuario.

### JumpListExplorer

Similar a LinkParser, facilita el análisis de Jump Lists en Windows.

Estas listas contienen información sobre los archivos y programas recientemente abiertos por el usuario, lo que puede ayudar a reconstruir la actividad reciente de un individuo, especialmente en investigaciones forenses sobre el uso de aplicaciones y documentos​.

### ShellbagExplorer

Esta herramienta permite a los forenses examinar los datos de Shellbags, que guardan información sobre las carpetas y archivos que un usuario ha abierto o visualizado en el sistema, incluso si han sido eliminados.

Es útil para rastrear la actividad en directorios específicos o archivos eliminados.

### USB Detective

Es una herramienta esencial para rastrear la actividad relacionada con dispositivos USB en un sistema Windows.

Puede revelar información sobre cuándo se conectaron dispositivos USB, qué archivos se copiaron o accedieron, y si hubo alguna manipulación de datos en un dispositivo de almacenamiento externo, lo cual es clave en investigaciones relacionadas con exfiltración de datos o accesos no autorizados​.

## Extraer evidencias de los artefactos

Antes de comenzar indicar que estamos utilizando el software FTK Imager para acceder a estas ubicaciones para extraer cada uno de los artefactos que se van a ir mostrando a continuación.

Cabe a destacar además que este proceso de ejemplo se está realizando en una máquina virtual activa y no sobre una imágen de disco extraida, pero el proceso es casi identico.

### Extraer archivos de registro

Para agilizar el proceso vamos a extraer el directorio donde vamos a encontrar la mayoria de registros del sistema interesantes.

Usando FTK extraemos el directorio completo.

```
C:\windows\system32\conf
```

![Extraer archivos de registro](/assets/img/posts/artefactos_en_windows/20241210_182435_Peek_2024-12-10_19-24.gif)

### Herramientas útiles

- [Registry Explorer](https://www.sans.org/tools/registry-explorer/)
- [RegRipper](https://github.com/keydet89/RegRipper4.0)
- [Windows Registry Recovery](https://www.mitec.cz/wrr.html)

### Versión del sistema, nombre de la máquina y zona horaria

```
Software\Microsoft\Windows NT\CurrentVersion
```

![Versión del sistema](/assets/img/posts/artefactos_en_windows/20241210_185749_Peek_2024-12-10_19-25.gif)

### Fecha de último acceso y Hora de apagado

```
System\ControlSet001\Control\Filesystem

System\ControlSet001\Control\Windows
```

![Fecha último acceso 1](/assets/img/posts/artefactos_en_windows/20241211_132918_Peek_2024-12-10_21-16.gif)

![Fecha último acceso 2](/assets/img/posts/artefactos_en_windows/20241211_132929_Peek_2024-12-10_21-17.gif)

Si vemos el resultado anterior es debido a que esta política viene desactivada por defecto en las últimas versiones de windows para mejorar el rendimiento del sistema.

Ahora vamos a comprobar el tiempo de apagado.

![Hora de apagado](/assets/img/posts/artefactos_en_windows/20241211_133223_Peek_2024-12-11_14-32.gif)

### Interfaces de red

```
System\ControlSet001\Services\Tcpip\Parameters\Interfaces\{GUID_INTERFACE}
```

![Interfaces de red](/assets/img/posts/artefactos_en_windows/20241211_171143_Peek_2024-12-11_18-11.gif)

### Histórico de redes

```
Software\Microsoft\Windows NT\CurrentVersion\NetworkList\

Software\Microsoft\Windows NT\CurrentVersion\NetworkList\Nla\Cache
```

![Histórico de redes](/assets/img/posts/artefactos_en_windows/20241211_171456_Peek_2024-12-11_18-14.gif)

### Cuándo se conectó a una red

```
Software\Microsoft\Windows NT\CurrentVersion\NetworkList\Profiles
```

![Conexiones a red](/assets/img/posts/artefactos_en_windows/20241211_171717_Peek_2024-12-11_18-17.gif)

### Carpetas compartidas

```
System\ControlSet001\Services\lanmanserver\Shares\
```

![Carpetas compartidas](/assets/img/posts/artefactos_en_windows/20241211_171907_Peek_2024-12-11_18-18.gif)

### Programas de inicio

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Run
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\RunOnce
Software\Microsoft\Windows\CurrentVersion\Runonce
Software\Microsoft\Windows\CurrentVersion\Policies\Explorer\Run
Software\Microsoft\Windows\CurrentVersion\Run
```

![Acceso NTUSER.DAT](/assets/img/posts/artefactos_en_windows/20241211_172712_Peek_2024-12-11_18-26.gif)
_Para acceder a NTUSER.DAT primero hay que extraerlo del disco de evidencia_

Una vez hecho ahora si podemos visualizar todas las rutas

![Ruta SOFTWARE](/assets/img/posts/artefactos_en_windows/20241211_172910_Peek_2024-12-11_18-28.gif)
_En este caso es la ruta en SOFTWARE_

![Ruta NTUSER.DAT](/assets/img/posts/artefactos_en_windows/20241211_174155_Peek_2024-12-11_18-41.gif)
_En este caso es la ruta NTUSER.DAT_

### Búsquedas en la barra de búsqueda

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\WordWheelQuery
```

![Búsquedas](/assets/img/posts/artefactos_en_windows/20241211_174351_Peek_2024-12-11_18-43.gif)
_En este caso el sistema no tiene activada la barra de busqueda por lo que no hay registros_

### Rutas en Inicio o Explorer

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\TypedPaths
```

![Rutas Explorer](/assets/img/posts/artefactos_en_windows/20241211_174440_Peek_2024-12-11_18-44.gif)
_Igualmente no aparece nada porque es inexistente en la máquina_

### Documentos recientes

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RecentDocs
```

![Documentos recientes](/assets/img/posts/artefactos_en_windows/20241211_174602_Peek_2024-12-11_18-45.gif)

### Documentos ofimáticos recientes

```
NTUSER.DAT\Software\Microsoft\Office\{Version}\{Excel|Word}\UserMRU
```

En este caso no vemos ni siquiera la carpeta office porque no tiene instalado el software

![Documentos ofimáticos](/assets/img/posts/artefactos_en_windows/20241211_174815_Peek_2024-12-11_18-48.gif)

### Posición de lectura sobre el último documento abierto

```
NTUSER.DAT\Software\Microsoft\Office\Word\Reading Locations\Document X.
```

Igualmente omitimos por no tener el software instalado

### Ficheros ofimáticos autoguardados

```
C:\Usuarios\\AppData\Roaming\Microsoft\{Excel|Word|Powerpoint}\
```

En este caso podemos acceder directamente desde FTK y de nuevo omitimos por no tener el software

### OpenSaveMRU: Ficheros que han sido abiertos o guardados dentro de una ventana Windows

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\ComDlg32\OpenSaved
PidlMRU
```

![OpenSaveMRU](/assets/img/posts/artefactos_en_windows/20241211_175228_Peek_2024-12-11_18-52.gif)

### Últimos comandos ejecutados

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\RunMRU
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\Policies\RunMRU
```

![Últimos comandos](/assets/img/posts/artefactos_en_windows/20241211_175508_Peek_2024-12-11_18-54.gif)

### UserAssistKey: Programas ejecutados desde el Escritorio

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\UserAssist\{GUID}\Count
```

![UserAssistKey](/assets/img/posts/artefactos_en_windows/20241211_175728_Peek_2024-12-11_18-57.gif)

### Eventos asociados a la barra de tareas

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\FeatureUsage
```

![Eventos barra tareas](/assets/img/posts/artefactos_en_windows/20241211_175939_Peek_2024-12-11_18-59.gif)

### Aplicaciones recientes

```
Software\Microsoft\Windows\Current Version\Search\RecentApps
```

En el caso de esta máquina no se encuentra porque puede que no esté activado

### Dispositivos MTP

```
C:\users\Appdata\Local\Temp\WPDNSE\{GUID}
```

![Dispositivos MTP](/assets/img/posts/artefactos_en_windows/20241211_180926_Peek_2024-12-11_19-09.gif)
_En este caso vemos que no existe ya que en la máquina no existía ningún dispositivo MTP conectado_

### Almacenamiento USB. Identificadores de fabricante(VID) y de producto (PID)

```
SYSTEM\ControlSet001\Enum\USBSTOR
```

![USB VID PID](/assets/img/posts/artefactos_en_windows/20241211_181233_Peek_2024-12-11_19-12.gif)

### Nombres de volúmenes USB

```
SOFTWARE\Microsoft\Windows Portable Devices\Devices
```

![Volúmenes USB](/assets/img/posts/artefactos_en_windows/20241211_181433_Peek_2024-12-11_19-14.gif)

### Localizar el usuario que ha utilizado el USB

```
NTUSER.DAT\Software\Microsoft\Windows\CurrentVersion\Explorer\Mountpoints2
```

![Usuario USB](/assets/img/posts/artefactos_en_windows/20241211_181645_Peek_2024-12-11_19-16.gif)

### Número de serie de volumen lógico

```
Software\Microsoft\Windows NT\CurrentVersion\EMDMgmt
```

![Número serie volumen](/assets/img/posts/artefactos_en_windows/20241211_181935_Peek_2024-12-11_19-18.gif)
_Hay que tener en cuenta que todos estos datos solo existen si se han utilizado dispositivos de almacenamiento externos_

### Primera y última vez que se conectó el dispositivo

```
System\ControlSet001\Enum\USBSTOR\{VEN_PROD_VERSION}\{USBserial}\Properties\{83da6326-97a6-4088-9453-a1923f573b29}\
```

![Conexiones dispositivo](/assets/img/posts/artefactos_en_windows/20241211_182342_Peek_2024-12-11_19-23.gif)

### Servicios

```
SYSTEM\ControlSet001\Services
```

![Servicios](/assets/img/posts/artefactos_en_windows/20241211_185333_Peek_2024-12-11_19-53.gif)

### Histórico de PowerShell

```
C:Users\{User}\AppData\Roaming\Microsoft\Windows\PowerShell\PSReadline\ConsoleHost_history.txt
```

![Histórico PowerShell](/assets/img/posts/artefactos_en_windows/20241211_185645_Peek_2024-12-11_19-56.gif)

### Tareas programadas

```
C:\Windows\Tasks
C:\Windows\System32\Tasks
```

![Tareas programadas](/assets/img/posts/artefactos_en_windows/20241211_190049_Peek_2024-12-11_20-00.gif)

## Otros artefactos

### Documentos recientes (LinkParses o LeCMD)

- [LinkParser](https://github.com/ravisorg/LinkParser)
- [LeCMD](https://github.com/EricZimmerman/LECmd)

```
C:\Users\\AppData\Roaming\Microsoft\Windows\Recent
```

![Documentos recientes](/assets/img/posts/artefactos_en_windows/20241211_184824_Peek_2024-12-11_19-25.gif)

### Windows PREFETCH (LeCMD)

```
C:\Windows\Prefetch
```

![Windows PREFETCH](/assets/img/posts/artefactos_en_windows/20241211_185136_Peek_2024-12-11_19-51.gif)

### Automatic & Custom destinations (JumpListExplorer)

- [JumpList Explorer](https://github.com/EricZimmerman/JumpList)

```
C:\Users\\AppData\Roaming\Microsoft\Windows\Recent\AutomaticDestinations
C:\Users\\AppData\Roaming\Microsoft\Windows\Recent\CustomDestinations
```

Ubicamos y descargamos las rutas con FTK

![AutomaticDestinations](/assets/img/posts/artefactos_en_windows/20241211_192717_Peek_2024-12-11_20-27.gif)

![CustomDestinations 1](/assets/img/posts/artefactos_en_windows/20241211_192857_Peek_2024-12-11_20-28.gif)

![CustomDestinations 2](/assets/img/posts/artefactos_en_windows/20241211_193044_Peek_2024-12-11_20-30.gif)
_Estas parecen estar vacías_

### Acceso y tiempos MAC a directorios (ShellbagExplorer)

```
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\Bags
USRCLASS.DAT\Local Settings\Software\Microsoft\Windows\Shell\BagMRU Desktop
NTUSER.DAT\Software\Microsoft\Windows\Shell\BagMRU
```

![USRCLASS.DAT](/assets/img/posts/artefactos_en_windows/20241211_194442_Peek_2024-12-11_20-44.gif)
_Extraemos el directorio donde se encuentra USRCLASS.DAT_

Para verlas en crudo con el registro

![Registro crudo](/assets/img/posts/artefactos_en_windows/20241211_195222_Peek_2024-12-11_20-52.gif)

Pero para poder interpretar el contenido de las ShellBags hacemos uso del siguiente software

![ShellBags software](/assets/img/posts/artefactos_en_windows/20241211_195352_Peek_2024-12-11_20-53.gif)

### Base de datos Cortana en versiones anteriores a Windows 10.0.17763.55 (Sqlite studio)

```
\Users\user_name\AppData\Local\Packages\Microsoft.Windows.Cortana_xxxx\LocalState\ESEDatabase_CortanaCoreInstance\CortanaCireDb.dat
```

Omitimos este artefacto porque estamos usando Windows 11

### Notificaciones de Windows

```
C:\Users\{user_name}\AppData\Local\Microsoft\Windows\Notifications\wpndatabase.db
```

![Notificaciones Windows](/assets/img/posts/artefactos_en_windows/20241211_200329_Peek_2024-12-11_21-02.gif)

### Windows Store

```
C:\ProgramData\Microsoft\Windows\AppRepository\StateRepositoryDeployment.srd
Software\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Applications\
Software\Microsoft\Windows\CurrentVersion\Appx\AppxAllUserStore\Deleted\
```

![Windows Store 1](/assets/img/posts/artefactos_en_windows/20241211_200918_Peek_2024-12-11_21-09.gif)

![Windows Store 2](/assets/img/posts/artefactos_en_windows/20241211_201218_Peek_2024-12-11_21-12.gif)

### Thumbnails (thumbviewer) & Thumbcaché (thumbcacheviewer)

- [Thumbs Viewer](https://thumbsviewer.github.io/)
- [Thumbcache Viewer](https://thumbcacheviewer.github.io/)

```
Ficheros "thumbs.db"
C:\Users\user\AppData\Local\Microsoft\Windows\Explorer
```

![Thumbnails](/assets/img/posts/artefactos_en_windows/20241211_202211_Peek_2024-12-11_21-21.gif)
_Puede que no encontremos ningún archivo thumb.db pero si caches_

### Papelera de reciclaje (Rifiuti)

- [Rifiuti](https://abelcheung.github.io/rifiuti2/)

El concepto de esta herramienta es que como se observa a continuación el visualizado de los nombres de los archivos existentes en las papeleras de los diferentes usuarios es modificado por windows al ser enviados a la papelera.
Este software se encarga de recuperar el nombre de ese archivo.

![Papelera reciclaje](/assets/img/posts/artefactos_en_windows/20241212_085524_Peek_2024-12-12_09-53.gif)

### OfficeFileCache & OfficeBacktage

En ambos casos se trata de extraer metadatos de los documentos creados con el paquete office por lo que en esta ocasión vamos a saltar estos artefactos ya que no lo tenemos en nuestra máquina

#### OfficeFileCacheParser

```
\Users\(Username)\AppData\Local\Microsoft\Office\(Office Version)\OfficeFileCache
```

#### OfficeBackstageParser

```
\{Users}\AppData\Local\Microsoft\Office\16.0\BackstageinAppNavCache
```

### IP Pública

- [ETLParser](https://github.com/forensiclunch/ETLParser)

```
C:\Windows\ServiceProfiles\NetworkService\AppData\Local\Microsoft\Windows\DeliveryOptimization\Logs\
```

![IP Pública 1](/assets/img/posts/artefactos_en_windows/20241212_090852_Peek_2024-12-12_10-08.gif)

![IP Pública 2](/assets/img/posts/artefactos_en_windows/20241212_092501_Peek_2024-12-12_10-24.gif)
_Podemos abrirlo con algun editor de hojas de cálculo igualmente_

Nota* Esa no es mi IP pública real, la he modificado por supuesto

### Windows SuperFetch

```
C:\Windows\Prefetch\Ag*.db
```

- [PECmd](https://www.sans.org/tools/pecmd/)

![Windows SuperFetch](/assets/img/posts/artefactos_en_windows/20241212_103306_Peek_2024-12-12_11-32.gif)

### ShimCache

- [AppCompatCacheParser](https://github.com/EricZimmerman/AppCompatCacheParser)

```
SYSTEM\CurrentControlSet\Control\SessionManager\AppcompatCache\AppCompatCache
```

![ShimCache](/assets/img/posts/artefactos_en_windows/20241212_111928_Peek_2024-12-12_12-19.gif)

### AmCache

```
C:\Windows\AppCompat\Programas\Amcache.hve
```

![AmCache](/assets/img/posts/artefactos_en_windows/20241212_112750_Peek_2024-12-12_12-26.gif)

### BAM

```
SYSTEM\CurrentControlSet\Services\bam\UserSettings\{SID}
SYSTEM\CurrentControlSet\Services\bam\state\UserSettings\{SID}
```

![BAM](/assets/img/posts/artefactos_en_windows/20241212_113603_Peek_2024-12-12_12-35.gif)

### Eventos

```
C:\Windows\system32\winevt\Logs
```

- [EventLog Explorer](https://eventlogxp.com/downloads/)

![Eventos](/assets/img/posts/artefactos_en_windows/20241212_115024_Peek_2024-12-12_12-49.gif)

### SRUM

- [Network usage view](https://www.nirsoft.net/utils/network_usage_view.html)

```
C:\Windows\System32\sru\SRUDB.dat
```

![SRUM](/assets/img/posts/artefactos_en_windows/20241212_181806_Peek_2024-12-12_19-16.gif)