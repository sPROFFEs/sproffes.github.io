---
title: Sysmon en Windows
date: 2024-12-20 11:58:38 +0000
categories: [Forense, Windows]
tags: [sysmon, windows, monitorización, seguridad]
pin: false
math: false
mermaid: false
---

## ¿Qué es sysmon?

Sysmon (System Monitor) es una herramienta avanzada de la suite Sysinternals de Microsoft que proporciona monitoreo detallado de actividades del sistema en tiempo real. Sysmon captura eventos clave, como cambios en el registro, creación de procesos, conexiones de red, y manipulación de archivos, entre otros. Estos eventos se registran en los logs de eventos de Windows, permitiendo a los administradores y analistas de seguridad identificar comportamientos sospechosos, investigar incidentes y realizar análisis forenses. Es altamente configurable mediante un archivo de configuración XML que define qué eventos deben ser monitoreados y cómo.

Monitoriza:
- Procesos que se crean
- Conexiones de red
- Cambios en el registro
- Comandos que se ejecutan

## Instalación

### Sistema operativo

Windows 10 Pro 22H2 19045.3803

### Descarga

- [Sysmon Windows](https://download.sysinternals.com/files/Sysmon.zip)
- [Sysmon Linux](https://github.com/Sysinternals/SysmonForLinux)

### Instalación

Una vez descargado y extraido en la ruta del ejcutable abrimos un terminal como administrador y ejecutamos:

```bash
sysmon -accepteula -i
```

### Configuración por defecto

![Configuración por defecto](/assets/img/posts/sysmon_windows/20241220_104128_2024-12-20_11-40.png)
_Esto instalará el sofware con una configuración por defecto_

### Configuración personalizada

[Archivo de configuración](https://github.com/SwiftOnSecurity/sysmon-config/blob/master/sysmonconfig-export.xml)

```bash
sysmon -accepteula -i c:\ruta\config.xml # Si es la primera instalación

sysmon -c c:\ruta\config.xml # Si quieres asignar una configuración al software ya instalado
```

![Configuración personalizada](/assets/img/posts/sysmon_windows/20241220_105625_2024-12-20_11-56.png)

## Visualización de logs

### Visor de eventos

Para ver el contenido que crea este software podemos consultar la documentación oficial de Microsoft.

Para ver los registros que crea debemos utilizar el visualizador de eventos de windows, simplemente en el inicio escribimos eventos e iniciamos el visualizador.

![Visor de eventos](/assets/img/posts/sysmon_windows/20241220_105026_Peek_2024-12-20_11-49.gif)

### Archivo de configuración

En el anterior apartado veremos todos los registros que nosotros hayamos configurado en el archivo de configuración cargado en el programa.

Si abrimos el archivo xml veremos la estructura en la que este indica que patrones debe tomar para monitorizar según que procesos y crear registros sobre los mismos

![Configuración de registros](/assets/img/posts/sysmon_windows/20241220_110034_2024-12-20_12-00.png)
_Crea registros de los servicios de red, el svchosts para registrar los servicios creados y en ejecución..._

![Configuración de conexiones](/assets/img/posts/sysmon_windows/20241220_110229_2024-12-20_12-02.png)
_Se puede añadir que registre cualquier conexión mediante Tor, ssh, proxy socks5/4, conexiónes SSH, Telnet, etc..._

### Ejemplo

Como en este caso indicamos el cambio de configuración después de la instalación, esto tambien queda registrado.

![Ejemplo de registro](/assets/img/posts/sysmon_windows/20241220_110639_2024-12-20_12-06.png)

## Ejemplo práctico - Cargar el registro

En este caso se han realizado una serie de actividades en el equipo que iremos averiguando gracias a los registros creados por sysmon.

Antes de comenzar con la visualización de los mismos debemos localizar su ubicación en el sistema de archivos y, además usaremos un software para facilitar la visualización de los mismos.

### Ubicación de registros

```plaintext
C:\Windows\System32\winevt\Logs\Microsoft-Windows-Sysmon%4Operational
```

### SysmonViewer

[SysmonTools - dentro buscamos SysmonViewer](https://github.com/nshalabi/SysmonTools)

### Extraer los registros

![Extracción de registros](/assets/img/posts/sysmon_windows/20241220_122941_Peek_2024-12-20_13-29.gif)

### Importar el registro en SysmonView

![Importar registro](/assets/img/posts/sysmon_windows/20241220_123129_Peek_2024-12-20_13-31.gif)

## Ejemplo práctico - Analizar los resultados

En SysmonView tendremos a la izquierda los ejecutables que han sido registrados por sysmon.

Si seleccionamos alguno nos indicará la ruta del binario y además las sesiones que ha tenido abiertas y su rastro.

Suponiendo que vamos a investigar lo que ha pasado en este equipo por ejemplo podemos empezar con el binario del explorador de archivos windows.

![Análisis de binarios](/assets/img/posts/sysmon_windows/20241220_124108_Peek_2024-12-20_13-40.gif)

Vemos varias entradas sobre un fichero llamado "SAMFW.COM_SM-G990B" que corresponde con el firmware de un telefono samsung.

El fichero parece ser grande porque cuenta con varios registros de creación y file stream ya que al estár el archivo descargando este se va modificando.

Poco más abajo vemos dos modificaciones en el registro, un par de creaciones de archivos más y lo que parece una ejecución de SysmonView.exe ya que al ejecutar el binario se actualiza la fecha de último uso.

![Correlación de binarios](/assets/img/posts/sysmon_windows/20241220_125253_Peek_2024-12-20_13-52.gif)
_Si buscamos algunos binarios más ahora que sabemos lo del firmware samsung vemos que hay correlaciones con algunos de los binarios ejecutados_

Si por ejemplo abrimos el registro de un binario llamado "Samsung USB driver" vemos que ha sido llamado desde el explorer.exe, se ha creado un proceso nuevo y se han creado 381 archivos y ha cambiado las fechas apertura de 594.

Si segumos el rastro parece que está creando varios archivos dll y por el nombre del ejecutable deducimos que es un driver para la comunciación entre el pc y el telefono samsung.

![Análisis de drivers](/assets/img/posts/sysmon_windows/20241220_125856_Peek_2024-12-20_13-54.gif)

Si vamos al binario llamado ODIN vemos que ha sido ejecutado 3 veces desde el explorador de archivos en un corto periodo de tiempo.

![Ejecuciones de ODIN](/assets/img/posts/sysmon_windows/20241220_130213_Peek_2024-12-20_14-02.gif)

Ahora que sabemos todo esto podemos comprobar si realmente el usuario finalmente conectó el dispositivo al ordenador.

Para ello como sabemos que ha instalado unos drivers propietarios y que son samsung podemos ir al binario que se encarga de ejecutar los controladores en windows en modo usuario.

![Conexiones de dispositivo](/assets/img/posts/sysmon_windows/20241220_130756_Peek_2024-12-20_14-07.gif)
_Aqui vemos como se cargaron varias veces lo que puede indicar las veces que se conectó el dispositivo al pc_

### Conclusión

Con estos datos que no son muy extensos ya que es un entorno de pruebas, vemos que el usuario descargó el firmware de un dispositivo Samsung modelo G990B, descargó o se transfirió un archivo llamado magisk_... que se trata de algun archivo del firmware del dispositivo modificado para tener acceso root, ejecutó el software odin varias veces, lo que puede ser indicativo de algun fallo en el proceso, al igual que las veces que conectó y desconectó el dispositivo al ordenador.

Con estas pruebas mas o menos podemos deducir que se trata de un rooteo a un dispositivo movil Samsung.

Esto es solo una muestra ya que como hemos visto registra cada paso que realiza cada binario, de donde viene, que hace y cuando acaba.

Además no se limita a los proceos internos unicamente sino que también podemos ver las llamadas que hace fuera del equipo.

![Llamadas DNS](/assets/img/posts/sysmon_windows/20241220_131655_Peek_2024-12-20_14-16.gif)
_Vemos llamdas DNS_

Aqui podemos ver como el buscador de windows por defecto al traer ciertos softwares pre instalados o esperando a serlo hace varias llamadas a lo que parecen varias api de microsoft.