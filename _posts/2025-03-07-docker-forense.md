---
title: Docker - Analisis forense
date: 2025-03-07 11:00:00 +0000
categories: [Forense, Proxmox VE, Docker]
tags: [Proxmox VE, Forense, Docker, Analisis forense]
image:
  path: /assets/img/cabeceras_genericas/docker.jpg
  alt:  Docker
description: >
  Guía para analisis forense en Docker 
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Introducción

Docker es una herramienta que facilita a los desarrolladores crear, probar e implementar aplicaciones de manera ágil mediante el uso de contenedores . Estos contenedores actúan como entornos aislados, asegurando que las aplicaciones funcionen de manera consistente en cualquier sistema, sin importar las diferencias técnicas del entorno.

Entre sus beneficios destacan:

- Consistencia entre entornos : Permite replicar configuraciones idénticas en desarrollo, pruebas y producción, reduciendo errores.

- Despliegue ágil : Integra procesos de integración y entrega continuos (CI/CD), acelerando la puesta en marcha de actualizaciones sin interrumpir servicios.

- Eficiencia : Los contenedores son ligeros y se inician o detienen en segundos, optimizando el tiempo de desarrollo y depuración.

Sin embargo, presenta desafíos:

- Curva de aprendizaje : Su configuración y manejo pueden resultar complejos para quienes no están familiarizados con la tecnología.

- Rendimiento : En escenarios de alta exigencia, la capa de virtualización de los contenedores podría afectar el desempeño comparado con entornos tradicionales.

En resumen, Docker simplifica la gestión de aplicaciones con contenedores, pero requiere familiaridad técnica y puede tener limitaciones en entornos críticos de rendimiento.

## Instalación de Docker en Proxmox VE

Existen diferentes formas de instalar Docker en cualquier sistema operativo, pero en este caso vamos a hacer uso de una herramienta muy útil para desplegar diferentes servicios en un entorno de virtualización, Proxmox VE.

[Docker script para Proxmox VE](https://community-scripts.github.io/ProxmoxVE/scripts?id=docker-vm)

Para instalarlo ejecutamos el siguiente comando en nuestro servidor Proxmox VE:

```bash
bash -c "$(wget -qLO - https://github.com/community-scripts/ProxmoxVE/raw/main/vm/docker-vm.sh)"
```

Cuando finalize tendremos nuestro servidor Docker instalado y listo para usar.

![alt text](/assets/img/posts/docker-forense/image.png)

## Uso básico de Docker

Vamos a hacer un recorrido básico sobre algunos comandos de Docker.

### Versión de Docker

```bash
docker --version
```

![alt text](/assets/img/posts/docker-forense/image-1.png)

### Información del host Docker

```bash
docker info
```

![alt text](/assets/img/posts/docker-forense/image-2.png)

### Descarfar una imagen Docker

Descarga la imagen desde Docker Hub si no existe localmente, en este caso la imagen de `nginx`.

```bash
docker pull nginx:latest
```

![alt text](/assets/img/posts/docker-forense/image-3.png)

### Listar las imágenes de Docker localmente

Muestra todas las imágenes almacenadas en tu máquina.

```bash
docker images
# o
docker image ls
```

![alt text](/assets/img/posts/docker-forense/image-4.png)

### Ejecutar una imagen Docker en segundo plano

```bash
docker run -d --name my-nginx nginx:latest
```
    -d: Modo "detached" (segundo plano).
    --name: Asigna un nombre al contenedor.

![alt text](/assets/img/posts/docker-forense/image-5.png)

### Ejecutar una imagen Docker en modo interactivo

```bash
docker run -it --name my-nginx-interactive nginx:latest
```
    -it: Modo interactivo.

> Nota: Este comando iniciará el contenedor, pero como la imagen de NGINX no incluye una shell por defecto, el contenedor se detendrá al no tener un proceso interactivo. Para acceder a una shell, usa el paso 12.
{: prompt-info}

### Listar los contenedores Docker en ejecución

```bash
docker ps
```
Para ver todos los contenedores (incluidos los detenidos):

```bash
docker ps -a
```

![alt text](/assets/img/posts/docker-forense/image-6.png)

### Inspeccionar un contenedor

```bash
docker inspect <ID_o_nombre_contenedor>
```

![alt text](/assets/img/posts/docker-forense/image-7.png)

### Listar las redes de Docker

```bash
docker network ls
```

![alt text](/assets/img/posts/docker-forense/image-8.png)

### Adjuntar una consola a un contenedor 

```bash
docker attach <ID_o_nombre_contenedor>
```

Para salir sin detener el contenedor: Presiona Ctrl+P seguido de Ctrl+Q.

![alt text](/assets/img/posts/docker-forense/image-9.png)

En este caso no abre un shell ya que esta imagen de nginx no tiene un shell.

### Ejecutar /bin/bash en un contenedor

Para esto vamos a descargar una imagen con shell como debian por ejemplo.

```bash
docker exec -it <ID_o_nombre_contenedor> /bin/bash
```

![alt text](/assets/img/posts/docker-forense/image-10.png)

### Detener un contenedor

```bash
docker stop <ID_o_nombre_contenedor>
```

![alt text](/assets/img/posts/docker-forense/image-11.png)

### Iniciad un contenedor detenido

```bash
docker start <ID_o_nombre_contenedor>
```

![alt text](/assets/img/posts/docker-forense/image-12.png)

### Borrar un contenedor

```bash
docker rm <ID_o_nombre_contenedor>
# o si está en ejecución
docker rm -f <ID_o_nombre_contenedor>
```

![alt text](/assets/img/posts/docker-forense/image-13.png)

### Crear un dockerfile para un contenedor

Creamos el dockerfile en el directorio actual:

```bash
# Usar la imagen oficial de Kali Linux
FROM kalilinux/kali-rolling

# Copiar el archivo 'script' al contenedor (asegúrate de que exista en tu directorio local)
COPY script /file

# Dar permisos de ejecución al archivo
RUN chmod +x /file
```

![alt text](/assets/img/posts/docker-forense/image-14.png)

> Nota: Como se trata de una prueba el archivo que se copia en el contenedor es `script` y estará vacío en el directorio actual.
{: prompt-info}

Ahora contriubimos la imagen:

```bash
docker build -t my-kali-image .
```
![alt text](/assets/img/posts/docker-forense/image-15.png)

![alt text](/assets/img/posts/docker-forense/image-16.png)

### Crear una imagen Docker desde un contenedor

Para esto debemos crear una shell interactiva dentro del contenedor que queramos convertir en una imagen Docker.

Por ejemplo dentro de el contenedor debian.

![alt text](/assets/img/posts/docker-forense/image-17.png)

Realizamos los cambios pertinentes y salimos del contenedor.

Ahora creamos una imagen del contenedor con los cambios realizados.

```bash
docker commit <ID_o_nombre_contenedor> <nombre_imagen>
```

![alt text](/assets/img/posts/docker-forense/image-18.png)

### Exportar la imagen como un fichero

Ahora para convertir esa imagen personalizada en un dockerfile podemos usar el siguiente comando:

```bash
docker save -o <nombre_fichero.tar> <ID_o_nombre_imagen>
```

![alt text](/assets/img/posts/docker-forense/image-19.png)

### Exportar un contenedor como un fichero

```bash
docker export <ID_o_nombre_contenedor> -o <nombre_fichero.tar>
```

![alt text](/assets/img/posts/docker-forense/image-20.png)

### Eliminar una imagen Docker

Al igual que podemos eliminar contenedores, también podemos eliminar imágenes.

```bash
docker rmi <ID_o_nombre_imagen>
```

![alt text](/assets/img/posts/docker-forense/image-21.png)


## Contexto forense en Docker

1. **Evidencia fragmentada y componentes clave:**  
   - Los contenedores no tienen una función de "snapshot" integrada. La obtención de evidencia requiere capturar **componentes separados**:  
     - **Sistema de archivos**: Usar el sistema *copy-on-write* de runtimes como Docker para identificar cambios desde la imagen base (ej. `docker commit`).  
     - **Memoria**: Dumper la memoria de procesos individuales con herramientas como `gcore` o `memfetch`, aprovechando el aislamiento de *namespaces*.  
     - **Volúmenes compartidos**: Inspeccionar montajes de volúmenes persistentes (ej. en `/var/lib/docker/volumes`), pero evitar alterar metadatos accediéndolos en modo *read-only*.  

2. **Arquitecturas distribuidas y microservicios:**  
   - Los incidentes pueden involucrar múltiples contenedores y hosts. Es crítico:  
     - Mapear interacciones entre servicios (redes, APIs, almacenamiento).  
     - Capturar evidencia de todos los contenedores relacionados, incluso si no muestran actividad sospechosa inicialmente.  

3. **Aislamiento imperfecto y escapes de contenedores:**  
   - Los contenedores comparten el kernel del host, lo que introduce riesgos:  
     - **Escapes**: Investigar si el contenedor usó flags peligrosos (`--privileged`, `--cap-add`, etc.) o accedió a dispositivos del host.  
     - **Volúmenes**: Malware puede persistir en volúmenes externos (ej. S3, GlusterFS), requiriendo análisis específico del backend.  

4. **Entorno forense adaptado a contenedores:**  
   - **Ephemeralidad**: Los contenedores son efímeros. Para preservar evidencia:  
     - **Pausar** el contenedor (ej. `docker pause`) para congelar procesos y memoria.  
     - **Aislar** redes o limitar syscalls para evitar contaminación.  
   - **Herramientas específicas**: Usar plataformas como **StackRox** para:  
     - Monitorear tráfico entre contenedores y detectar movimientos laterales.  
     - Automatizar respuestas (cuarentena, bloqueo de comandos).  

5. **Diferencias con entornos tradicionales (VMs):**  
   - A diferencia de las VMs, no hay aislamiento hardware. Esto implica:  
     - Mayor complejidad para capturar estados completos (ej. memoria + procesos).  
     - Mayor dependencia de herramientas especializadas en contenedores.  

6. **Recomendaciones clave:**  
   - **Priorizar la inmutabilidad**: Evitar reiniciar/eliminar contenedores sospechosos hasta capturar evidencia.  
   - **Automatizar la auditoría**: Implementar políticas con herramientas como StackRox para alertar sobre privilegios excesivos o comportamientos anómalos.  
   - **Preservar contexto**: Registrar metadatos (ej. redes, etiquetas de Kubernetes) para reconstruir la cadena de eventos.  


### **Modificadores Docker y su utilidad en forensia informática**  

#### **1. `docker diff`**  
**¿Qué hace?**  
Muestra los cambios realizados en el sistema de archivos de un contenedor comparado con su imagen base.  
**Utilidad forense:**  
- Identificar archivos añadidos, modificados o eliminados en un contenedor sospechoso.  
- Detectar malware, backdoors, o configuraciones no autorizadas.  

**Ejemplo:**  
```bash
docker diff <ID_contenedor>
```  
**Salida típica:**  
```
C /etc/passwd  # Archivo modificado (ej. usuario añadido)
A /tmp/malware.sh  # Archivo añadido
D /var/log/auth.log  # Archivo eliminado
```  
**Justificación:**  
Si un contenedor fue comprometido, `docker diff` revelaría alteraciones en archivos críticos (ej. claves SSH, cron jobs, o scripts maliciosos).

#### **2. `docker save`**  
**¿Qué hace?**  
Exporta una **imagen** Docker a un archivo `.tar` (incluye todas sus capas y metadatos).  
**Utilidad forense:**  
- Preservar una imagen sospechosa para análisis fuera de producción.  
- Garantizar la integridad de la evidencia (evitar modificaciones durante la investigación).  

**Ejemplo:**  
```bash
docker save -o imagen_sospechosa.tar <nombre_imagen>
```  
**Justificación:**  
Almacenar una imagen comprometida permite analizarla en un entorno controlado (ej. con herramientas como `volatility` o ` autopsy`) sin alterar el estado original.


#### **3. `docker export`**  
**¿Qué hace?**  
Exporta el sistema de archivos de un **contenedor** a un archivo `.tar` (no incluye metadatos ni capas).  
**Utilidad forense:**  
- Capturar el estado exacto de un contenedor en ejecución o detenido.  
- Analizar archivos temporales, procesos o configuraciones volátiles.  

**Ejemplo:**  
```bash
docker export <ID_contenedor> -o contenedor_sospechoso.tar
```  
**Justificación:**  
Si un contenedor ejecutó malware, `docker export` permite extraer su filesystem para buscar artefactos como shells inversos, claves de acceso, o logs modificados.


#### **4. `docker load`**  
**¿Qué hace?**  
Carga una imagen desde un archivo `.tar` generado con `docker save`.  
**Utilidad forense:**  
- Restaurar imágenes sospechosas en un entorno aislado para su análisis.  
- Revisar configuraciones o vulnerabilidades sin exponer sistemas activos.  

**Ejemplo:**  
```bash
docker load -i imagen_sospechosa.tar
```  
**Justificación:**  
Permite recrear un entorno idéntico al comprometido para estudiar el comportamiento del ataque (ej. técnicas de persistencia o exfiltración de datos).


#### **5. `docker import`**  
**¿Qué hace?**  
Crea una nueva imagen a partir de un archivo `.tar` generado con `docker export` (no incluye historial de capas).  
**Utilidad forense:**  
- Analizar filesystems de contenedores en un entorno controlado.  
- Investigar malware que dependa de configuraciones específicas del contenedor.  

**Ejemplo:**  
```bash
docker import contenedor_sospechoso.tar nueva_imagen:forense
```  
**Justificación:**  
Si el malware solo se ejecuta bajo ciertas condiciones del contenedor, `docker import` permite recrear el contexto exacto para observar su comportamiento.


### **Diferencias clave entre `save`/`load` y `export`/`import`**  
| Comando          | Objetivo       | Incluye metadatos/capas | Forense ideal para:                  |
|------------------|----------------|-------------------------|--------------------------------------|
| `docker save`    | Imagen         | Sí                      | Preservar imágenes sospechosas       |
| `docker export`  | Contenedor     | No                      | Capturar filesystems volátiles       |
| `docker load`    | Imagen         | Sí                      | Restaurar imágenes en entornos seguros |
| `docker import`  | Contenedor     | No                      | Analizar filesystems en aislamiento  |

Estos comandos son esenciales para:  
1. **Preservar evidencia:** `save` y `export` garantizan que no se pierdan datos críticos.  
2. **Analizar en entornos controlados:** `load` e `import` permiten estudiar malware sin riesgos.  
3. **Detectar alteraciones:** `diff` identifica cambios sospechosos en tiempo real.  

Ejemplo práctico de flujo forense:  
1. Usar `docker diff` para identificar cambios en un contenedor comprometido.  
2. Exportar el contenedor con `docker export` y analizar su filesystem.  
3. Importar el filesystem con `docker import` para ejecutarlo en un laboratorio.  
4. Guardar la imagen original con `docker save` como respaldo legal.  


### Docker-diff

Es una herramienta que permite identificar los cambios realizados en el sistema de archivos de un contenedor comparado con su imagen base alojada en el servidor Docker Hub o imagenes locales.

Para instalar la herramienta podemos visitar su documentación oficial [Docker-diff](https://github.com/GoogleContainerTools/container-diff).

Para el siguiente ejemplo vamos a comparar dos imagenes debian en local.

```bash
container-diff diff daemon://debian:latest daemon://debian-test:latest
```

![alt text](/assets/img/posts/docker-forense/image-22.png)

![alt text](/assets/img/posts/docker-forense/image-23.png)

Para comprobar los cambios con una imagen oficial en remoto primero debemos iniciar sesión en Docker Hub.

```bash
docker login
```

Y luego podemos ejecutar el siguiente comando:

```bash
container-diff analyze <img> 
# o 
container-diff diff daemon://debian-test:latest remote://debian:latest
```

### Ejemplo práctico

Para realizar la siguiente sección vamos a utilizar una imagen docker con el siguiente contexto.

Se ha obtenido una imagen lógica correspondiente a una instalación de Docker en un sistema informático bajo sospecha. Se sospecha que dicha instalación podría haber sido utilizada para ocultar actividades.

[Imagen docker utilizada](https://drive.google.com/file/d/1bFlnUBg1GH17h8pIQRywhDkHbNeTjvNZ/view?usp=share_link)

Este proceso vamos a realizarlo en un Kali Linux.

```bash
python3 -m venv venv
source venv/bin/activate
pip install wheel docker-explorer
```

```bash
mkdir /tmp/evidence
tar -xzf imagen_docker.tgz -C /tmp/evidence
```

```bash
sudo /home/kali/Desktop/docker/venv/bin/de.py -r /tmp/evidence/var/lib/docker list all_containers
```

![alt text](/assets/img/posts/docker-forense/image-24.png)

![alt text](/assets/img/posts/docker-forense/image-25.png)

Existen tres contenedores que podemos analizar.

En este caso son pocos contenedores, pero si hubieran más podríamos analizar todos de ellos de forma más eficiente.

```bash
sudo /home/kali/Desktop/docker/venv/bin/de.py -r /tmp/evidence/var/lib/docker list all_containers |jq '.[].image_name'
```

![alt text](/assets/img/posts/docker-forense/image-26.png)

Si por ejemplo tenemos como objetivo el contenedor homeassistant podemos analizar sus logs.

```bash
/var/lib/docker/containers/4ea041fd90ad823353e5a62f395f5ddab3c8096a4cbf1816eb5c4f88169d0818/4ea041fd90ad823353e5a62f395f5ddab3c8096a4cbf1816eb5c4f88169d0818-json.log
```

![alt text](/assets/img/posts/docker-forense/image-27.png)

El análisis del log proporcionado revela varios puntos interesantes que pueden ser relevantes desde un punto de vista forense. A continuación, desgloso los hallazgos clave y su posible significado:

**Hallazgos clave**
1. **Posible actividad maliciosa:**  
   - La solicitud mal formada desde la IP `86.127.227.242` es sospechosa y merece más investigación. Podría tratarse de un intento de explotación o prueba de vulnerabilidades en la API de Home Assistant.  
   - Verifica si esta IP tiene acceso legítimo al sistema o si aparece en listas de IPs conocidas por actividades maliciosas.

2. **Configuración reinicializada:**  
   - La creación de una configuración predeterminada en `/config` podría indicar un reinicio forzado o manipulación del entorno. Investiga si esta acción fue intencionada o accidental.

3. **Errores en la API:**  
   - Los errores relacionados con campos vacíos (`country` y `language`) sugieren que alguien intentó enviar datos no válidos a la API. Esto podría ser parte de un ataque de fuzzing o una prueba de inyección de datos.

4. **Dirección IP sospechosa:**  
   - La IP `86.127.227.242` debe ser analizada en profundidad. Puedes usar herramientas como `whois` o servicios de reputación de IPs para determinar su origen y propósito.

Podemos revisar los logs del contenedor nextcloud para identificar posibles actividades maliciosas.

![alt text](/assets/img/posts/docker-forense/image-28.png)

### **1. Actividad principal**
- **Dirección IP recurrente:**  
  La mayoría de las solicitudes provienen de la dirección IP `86.127.227.242`. Esta IP parece ser el usuario principal interactuando con la instancia de Nextcloud.

- **Agente de usuario:**  
  Todas las solicitudes incluyen el siguiente agente de usuario:
  ```
  Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36
  ```
  Esto indica que el usuario está utilizando **Google Chrome versión 112** en un sistema operativo **Windows 10/11 (64 bits)**.

### **2. Solicitudes HTTP**
Las solicitudes HTTP registradas muestran una interacción típica con Nextcloud. Sin embargo, hay algunos puntos destacados:

#### a) **Acceso al dashboard y recursos principales**
- El usuario accede al **dashboard** (`/apps/dashboard/`) y carga varios recursos como:
  - Archivos CSS y JavaScript (`/dist/core-main.js`, `/apps/dashboard/css/dashboard.css`).
  - Imágenes de aplicaciones (`/apps/photos/img/app.svg`, `/apps/dashboard/img/dashboard.svg`).

#### b) **Solicitudes relacionadas con configuraciones y traducciones**
- Se observan múltiples solicitudes para cargar archivos de localización (`l10n/es.js`) y configuraciones específicas del idioma español (`es.js`). Esto sugiere que el usuario tiene configurado el idioma en español.

#### c) **Interacción con aplicaciones instaladas**
- El usuario interactúa con varias aplicaciones de Nextcloud, como:
  - **Activity**: Carga archivos relacionados con la actividad del usuario (`/apps/activity/js/activity-dashboard.js`).
  - **Notifications**: Accede a notificaciones (`/ocs/v2.php/apps/notifications/api/v2/notifications`).
  - **User Status**: Consulta el estado del usuario (`/apps/user_status/img/user-status-online.svg`).
  - **Weather Status**: Accede a favoritos meteorológicos (`/ocs/v2.php/apps/weather_status/api/v1/favorites`).

#### d) **Carga de recursos multimedia**
- Se cargan imágenes de fondo y otros recursos visuales, como:
  ```
  /apps/theming/img/background/kamil-porembinski-clouds.jpg
  ```
  Esto es típico en Nextcloud cuando se utiliza un tema personalizado.

#### e) **Errores y respuestas inusuales**
- Algunas solicitudes devuelven códigos HTTP inusuales:
  - **Error 404 (Not Found):**  
    Ejemplo:
    ```
    216.218.206.74 - - [20/Apr/2023:07:55:02 +0000] "GET /favicon.ico HTTP/1.1" 404 636
    ```
    Esto indica que el recurso solicitado no existe. Podría ser un intento de acceso a un archivo no disponible.

  - **Error 400 (Bad Request):**  
    Ejemplo:
    ```
    216.218.206.126 - - [20/Apr/2023:07:55:53 +0000] "CONNECT www.shadowserver.org:443 HTTP/1.1" 400 14989
    ```
    Este error podría indicar un intento de conexión no válida o mal formada. La URL `www.shadowserver.org` está asociada con un servicio de seguridad que rastrea bots y malware. Esto podría ser relevante si el contenedor fue comprometido.

### **3. Posibles hallazgos forenses**
#### a) **IP sospechosa (`216.218.206.126`)**
- Una solicitud proveniente de la IP `216.218.206.126` intenta realizar una conexión a `www.shadowserver.org:443`. Esto podría ser:
  - Un intento de exfiltración de datos.
  - Un comportamiento malicioso (ej. malware intentando comunicarse con un servidor externo).

#### b) **Acceso repetitivo a recursos**
- La IP `86.127.227.242` realiza múltiples solicitudes en un corto período de tiempo. Esto podría ser normal si el usuario está navegando activamente, pero también podría indicar un script automatizado o un escaneo.

#### c) **Falta de autenticación explícita**
- No se observan solicitudes relacionadas con el inicio de sesión (ej. `/login` o `/index.php/login`). Esto podría significar que el usuario ya estaba autenticado o que las credenciales fueron almacenadas previamente.

#### d) **Uso de APIs internas**
- Se observan varias solicitudes a endpoints de API, como:
  ```
  /ocs/v2.php/apps/notifications/api/v2/notifications
  /apps/recommendations/api/recommendations/always
  ```
  Estas solicitudes son normales en Nextcloud, pero podrían ser abusadas si un atacante intenta explotar vulnerabilidades en estas APIs.

Teniendo entonces en cuenta que esta ha sido posiblemente el contenedor vulnerado podemos montarlo para analizar su contenido.

```bash
mkdir /tmp/evidence-docker
sudo /home/kali/Desktop/docker/venv/bin/de.py -r /tmp/evidence/var/lib/docker mount <id del contenedor> /tmp/evidence-docker
```

![alt text](/assets/img/posts/docker-forense/image-29.png)

Y ya aquí podríamos buscar archivos interesantes.

![alt text](/assets/img/posts/docker-forense/image-30.png)

En este caso es algo de ejemplo y no tenemos mucho más que analizar.

### Docker-scout

Docker Scout es una herramienta poderosa para identificar vulnerabilidades en imágenes de contenedores y mejorar su seguridad. Con los pasos anteriores, puedes instalarlo, analizar imágenes populares o personalizadas, y tomar medidas para mitigar problemas detectados.

Para instalarlo en nuestro sistema docker vamos a utilizar el siguiente comando:

```bash
curl -sSfL https://raw.githubusercontent.com/docker/scout-cli/main/install.sh | sh
```

![alt text](/assets/img/posts/docker-forense/image-31.png)

> Nota: Para poder utilizar este comando debemos tener instalado Docker e iniciar sesión en Docker Hub.
{: prompt-info}

![alt text](/assets/img/posts/docker-forense/image-32.png)

#### Análisis de CVE en imágenes Docker

```bash
docker scout cves debian:latest
```

**cves** : Este subcomando busca vulnerabilidades conocidas (Common Vulnerabilities and Exposures) en la imagen especificada.


```bash
root@localhost:~# docker scout cves debian:latest
    ...Storing image for indexing
    ✓ Image stored for indexing
    ...Indexing
    ✓ Indexed 125 packages
    ✗ Detected 12 vulnerable packages with a total of 23 vulnerabilities


## Overview

                    │       Analyzed Image         
────────────────────┼──────────────────────────────
  Target            │  debian:latest               
    digest          │  d4ccddb816ba                
    platform        │ linux/amd64                  
    vulnerabilities │    0C     0H     0M    23L   
    size            │ 55 MB                        
    packages        │ 125                          


## Packages and Vulnerabilities

   0C     0H     0M     7L  glibc 2.36-9+deb12u9
pkg:deb/debian/glibc@2.36-9%2Bdeb12u9?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2019-9192
      https://scout.docker.com/v/CVE-2019-9192?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2019-1010025
      https://scout.docker.com/v/CVE-2019-1010025?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2019-1010024
      https://scout.docker.com/v/CVE-2019-1010024?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2019-1010023
      https://scout.docker.com/v/CVE-2019-1010023?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2019-1010022
      https://scout.docker.com/v/CVE-2019-1010022?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2018-20796
      https://scout.docker.com/v/CVE-2018-20796?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    
    ✗ LOW CVE-2010-4756
      https://scout.docker.com/v/CVE-2010-4756?s=debian&n=glibc&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.36-9%2Bdeb12u9
      Affected range : >=2.36-9+deb12u9  
      Fixed version  : not fixed         
    

   0C     0H     0M     4L  systemd 252.33-1~deb12u1
pkg:deb/debian/systemd@252.33-1~deb12u1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2023-31439
      https://scout.docker.com/v/CVE-2023-31439?s=debian&n=systemd&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D252.33-1%7Edeb12u1
      Affected range : >=252.33-1~deb12u1  
      Fixed version  : not fixed           
    
    ✗ LOW CVE-2023-31438
      https://scout.docker.com/v/CVE-2023-31438?s=debian&n=systemd&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D252.33-1%7Edeb12u1
      Affected range : >=252.33-1~deb12u1  
      Fixed version  : not fixed           
    
    ✗ LOW CVE-2023-31437
      https://scout.docker.com/v/CVE-2023-31437?s=debian&n=systemd&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D252.33-1%7Edeb12u1
      Affected range : >=252.33-1~deb12u1  
      Fixed version  : not fixed           
    
    ✗ LOW CVE-2013-4392
      https://scout.docker.com/v/CVE-2013-4392?s=debian&n=systemd&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D252.33-1%7Edeb12u1
      Affected range : >=252.33-1~deb12u1  
      Fixed version  : not fixed           
    

   0C     0H     0M     2L  perl 5.36.0-7+deb12u1
pkg:deb/debian/perl@5.36.0-7%2Bdeb12u1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2023-31486
      https://scout.docker.com/v/CVE-2023-31486?s=debian&n=perl&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D5.36.0-7%2Bdeb12u1
      Affected range : >=5.36.0-7+deb12u1  
      Fixed version  : not fixed           
    
    ✗ LOW CVE-2011-4116
      https://scout.docker.com/v/CVE-2011-4116?s=debian&n=perl&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D5.36.0-7%2Bdeb12u1
      Affected range : >=5.36.0-7+deb12u1  
      Fixed version  : not fixed           
    

   0C     0H     0M     2L  gcc-12 12.2.0-14
pkg:deb/debian/gcc-12@12.2.0-14?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2023-4039
      https://scout.docker.com/v/CVE-2023-4039?s=debian&n=gcc-12&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D12.2.0-14
      Affected range : >=12.2.0-14  
      Fixed version  : not fixed    
    
    ✗ LOW CVE-2022-27943
      https://scout.docker.com/v/CVE-2022-27943?s=debian&n=gcc-12&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D12.2.0-14
      Affected range : >=12.2.0-14  
      Fixed version  : not fixed    
    

   0C     0H     0M     1L  libgcrypt20 1.10.1-3
pkg:deb/debian/libgcrypt20@1.10.1-3?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2018-6829
      https://scout.docker.com/v/CVE-2018-6829?s=debian&n=libgcrypt20&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D1.10.1-3
      Affected range : >=1.10.1-3  
      Fixed version  : not fixed   
    

   0C     0H     0M     1L  coreutils 9.1-1
pkg:deb/debian/coreutils@9.1-1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2017-18018
      https://scout.docker.com/v/CVE-2017-18018?s=debian&n=coreutils&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D9.1-1
      Affected range : >=9.1-1    
      Fixed version  : not fixed  
    

   0C     0H     0M     1L  gnupg2 2.2.40-1.1
pkg:deb/debian/gnupg2@2.2.40-1.1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2022-3219
      https://scout.docker.com/v/CVE-2022-3219?s=debian&n=gnupg2&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.2.40-1.1
      Affected range : >=2.2.40-1.1  
      Fixed version  : not fixed     
    

   0C     0H     0M     1L  apt 2.6.1
pkg:deb/debian/apt@2.6.1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2011-3374
      https://scout.docker.com/v/CVE-2011-3374?s=debian&n=apt&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.6.1
      Affected range : >=2.6.1    
      Fixed version  : not fixed  
    

   0C     0H     0M     1L  util-linux 2.38.1-5+deb12u3
pkg:deb/debian/util-linux@2.38.1-5%2Bdeb12u3?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2022-0563
      https://scout.docker.com/v/CVE-2022-0563?s=debian&n=util-linux&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D2.38.1-5%2Bdeb12u3
      Affected range : >=2.38.1-5+deb12u3  
      Fixed version  : not fixed           
    

   0C     0H     0M     1L  tar 1.34+dfsg-1.2+deb12u1
pkg:deb/debian/tar@1.34%2Bdfsg-1.2%2Bdeb12u1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2005-2541
      https://scout.docker.com/v/CVE-2005-2541?s=debian&n=tar&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D1.34%2Bdfsg-1.2%2Bdeb12u1
      Affected range : >=1.34+dfsg-1.2+deb12u1  
      Fixed version  : not fixed                
    

   0C     0H     0M     1L  gnutls28 3.7.9-2+deb12u4
pkg:deb/debian/gnutls28@3.7.9-2%2Bdeb12u4?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2011-3389
      https://scout.docker.com/v/CVE-2011-3389?s=debian&n=gnutls28&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D3.7.9-2%2Bdeb12u3
      Affected range : >=3.7.9-2+deb12u3  
      Fixed version  : not fixed          
    

   0C     0H     0M     1L  shadow 1:4.13+dfsg1-1
pkg:deb/debian/shadow@1:4.13%2Bdfsg1-1?os_distro=bookworm&os_name=debian&os_version=12

    ✗ LOW CVE-2007-5686
      https://scout.docker.com/v/CVE-2007-5686?s=debian&n=shadow&ns=debian&t=deb&osn=debian&osv=12&vr=%3E%3D1%3A4.13%2Bdfsg1-1
      Affected range : >=1:4.13+dfsg1-1  
      Fixed version  : not fixed         
    


23 vulnerabilities found in 12 packages
  CRITICAL  0   
  HIGH      0   
  MEDIUM    0   
  LOW       23  


What's next:
    View base image update recommendations → docker scout recommendations debian:latest
```

El comando genera un informe detallado que incluye:

- Una lista de paquetes instalados en la imagen.
- Vulnerabilidades detectadas (por ejemplo, CVEs).
- Gravedad de las vulnerabilidades (baja, media, alta, crítica).
- Sugerencias para mitigar los problemas.

También se puede en imágenes locales.

```bash
docker scout cves my-local-image:tag
```

### Informe detallado de imágenes Docker

```bash
docker scout quickview nginx:latest
```

```bash
    ✓ SBOM obtained from attestation, 231 packages found
    ✓ Provenance obtained from attestation

  Target     │  nginx:latest                                                                              │    0C     3H     1M    54L     2?   
    digest   │  28edb1806e63                                                                              │                                     
  Base image │  oisupport/staging-amd64:66dc4faa3fc0a9843aed29e2c3af6f3b0a9106624590fe6ad0856c2f8b152749  │                                     

What's next:
    View vulnerabilities → docker scout cves nginx:latest
    Include policy results in your quickview by supplying an organization → docker scout quickview nginx:latest --org <organization>
```

Este comando proporciona una visión general de la imagen, incluyendo:

- El número total de paquetes.
- El número de vulnerabilidades por gravedad.
- Recomendaciones para mejorar la seguridad.

### Checkpoints en Docker

Desde un punto de vista forense, los **checkpoints de Docker** pueden ser extremadamente útiles debido a su capacidad para capturar y restaurar el estado completo de un contenedor en un momento específico.

**1. Captura del estado completo del contenedor**
- **¿Qué hace el checkpoint?**
  Los checkpoints de Docker guardan no solo el sistema de archivos del contenedor, sino también el estado de la memoria (RAM) y los procesos en ejecución en ese momento.
  
**2. Recuperación de credenciales y datos sensibles**
- **Escenario descrito:**
  En el [caso](https://tbhaxor.com/analyzing-docker-image-for-hunting-secrets/) del proceso `authenticator` que maneja credenciales de usuario, estas credenciales fueron proporcionadas previamente a través de la entrada estándar. Sin embargo, al detener el contenedor, el estado de este proceso desaparece porque Docker no conserva la memoria ni los procesos en ejecución.

- **Uso forense del checkpoint:**
  - Si se crea un checkpoint antes de detener el contenedor, se puede restaurar el estado exacto del proceso `authenticator`, incluyendo cualquier dato sensible que estuviera presente en la memoria.
  - Esto permite realizar un volcado de memoria (`memory dump`) del proceso restaurado para extraer las credenciales u otros datos relevantes.


**3. Persistencia temporal de estados volátiles**
- **Problema sin checkpoints:**
  Cuando un contenedor se detiene, todos los estados volátiles (como variables en memoria, procesos en ejecución, etc.) se pierden. Esto dificulta el análisis forense si no se capturó previamente el estado del contenedor.

- **Ventaja de los checkpoints:**
  - Los checkpoints actúan como una "instantánea" temporal que preserva tanto el sistema de archivos como la memoria del contenedor.
  - Esto permite analizar el estado del contenedor en un momento específico, incluso si el contenedor ya no está en ejecución.


**4. Análisis de malware o actividades maliciosas**
- **Uso forense:**
  - Si un contenedor ha sido comprometido o utilizado para actividades maliciosas, los checkpoints permiten restaurar el contenedor a un estado anterior para analizar cómo se comportaba el malware o qué procesos estaban en ejecución.
  - Esto es especialmente útil para identificar patrones de ataque, persistencia de amenazas o exfiltración de datos.

**5. Volcado de memoria para análisis**
- **Proceso descrito:**
  - Una vez restaurado el checkpoint, se puede identificar el PID del proceso `authenticator` en la máquina host.
  - Usando herramientas como `gdb`, se realiza un volcado de memoria del proceso para extraer datos relevantes.

- **Relevancia forense:**
  - El volcado de memoria permite recuperar información que podría estar oculta o cifrada en el sistema de archivos.
  - Herramientas como `strings` facilitan la extracción de datos legibles por humanos, como contraseñas o tokens.


**6. Limitaciones y consideraciones**
- **Limitaciones técnicas:**
  - La funcionalidad de checkpoints aún está en fase experimental y solo está disponible en Linux.
  - Los checkpoints deben crearse explícitamente; no se generan automáticamente cuando un contenedor se detiene.

- **Consideraciones forenses:**
  - Es importante asegurarse de que los checkpoints no modifiquen el estado original del contenedor durante su creación o restauración.
  - Los permisos del sistema pueden afectar la capacidad de realizar volcados de memoria o acceder a ciertos archivos.


