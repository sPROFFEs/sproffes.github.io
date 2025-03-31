---
title: Bypass de Firewall con NMAP
date: 2025-03-27 11:00:00 +0000
categories: [Laboratorios, Redes]
tags: [labs, red, hacking, bypass, firewall, nmap]
image:
  path: /assets/img/cabeceras_genericas/Firewall.jpg
  alt:  Firewall
description: >
  Guía para bypassear un firewall con NMAP
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Objetivo del Lab

Simular una red interna protegida por un firewall/router, desde la cual:

    Sólo el puerto web público (80) es accesible desde fuera.

    Los servicios internos (8080 y 22) están filtrados.

    La máquina atacante (Kali) actúa como un administrador remoto o atacante externo.

```plaintext
┌────────────┐        ┌────────────┐        ┌────────────┐
│   Kali     │ <----->│   Router   │ <----->│  Servidor  │
│10.0.1.10   │        │10.0.1.1/   │        │10.0.2.10   │
│(externa)   │        │10.0.2.1    │        │(interna)   │
└────────────┘        └────────────┘        └────────────┘
```

- Kali y el router están en la red 10.0.1.0/24

- El router y el servidor están en la red 10.0.2.0/24

## Configuración de red (IPs fijas)

Kali

    eth1: 10.0.1.10

    Gateway: 10.0.1.1

Router (Ubuntu Server)

    ens18: 10.0.1.1 (externa)

    ens19: 10.0.2.1 (interna)

Servidor interno (Ubuntu Server)

    ens18: 10.0.2.10

## Servicios internos simulados

En el servidor (10.0.2.10):

    Instalamos Apache con 2 sitios:

        Sitio público en puerto 80 → /var/www/public

        Panel privado en puerto 8080 → /var/www/panel

### Crear los servicios simulados

Instalar Apache

```bash
sudo apt update
sudo apt install apache2
```

Crear las carpetas para cada sitio

```bash
sudo mkdir /var/www/public
sudo mkdir /var/www/panel
```

Crear una página simple para cada sitio

```bash
echo "<h1>Sitio Público</h1>" | sudo tee /var/www/public/index.html
echo "<h1>Panel de Administración Interno</h1>" | sudo tee /var/www/panel/index.html
```

Crear archivos de configuración de Apache para los dos sitios

```bash
sudo tee /etc/apache2/sites-available/public.conf > /dev/null <<EOF
<VirtualHost *:80>
    ServerAdmin webmaster@localhost
    DocumentRoot /var/www/publico
    ErrorLog /var/log/public_error.log
    CustomLog /var/log/public_access.log combined
</VirtualHost>
EOF
```

```bash
sudo tee /etc/apache2/sites-available/panel.conf > /dev/null <<EOF
<VirtualHost *:8080>
    ServerAdmin admin@localhost
    DocumentRoot /var/www/panel
    ErrorLog /var/log/panel_error.log
    CustomLog /var/log/panel_access.log combined
</VirtualHost>
EOF
```
![alt text](/assets/img/posts/nmap_firewall_bypass/image.png)

Habilitar los sitios y puerto 8080

```bash
sudo a2ensite public.conf
sudo a2ensite panel.conf
sudo sed -i 's/^#\?Listen 80/Listen 80\nListen 8080/' /etc/apache2/ports.conf
```

Deshabilitar el sitio por defecto

```bash
sudo a2dissite 000-default.conf
```

Reiniciar Apache

```bash
sudo systemctl restart apache2
```
## Asignando IPs a las interfaces

- Router

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-2.png)

- Servidor interno

```bash
sudo nano /etc/netplan/50-cloud-init.yaml
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-3.png)


- Kali

En este caso lo haremos mediante GUI y suponiendo que tenemos dos interfaces.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-4.png)

Seleccionamos la interfaz que se enuentre en la misma red que el router y la asignamos a la IP 10.0.1.10.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-5.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-6.png)

- Aplicar los cambios en todas las máquinas.

```bash
sudo netplan apply
```

## Reglas de Firewall con iptables

Nombre de las interfaces en el router

![alt text](/assets/img/posts/nmap_firewall_bypass/image-1.png)

Habilitar IP forwarding

```bash
echo "1" > /proc/sys/net/ipv4/ip_forward
# o
sysctl net.ipv4.ip_forward=1
```

Redirección de puertos (NAT)

```bash
iptables -t nat -A PREROUTING -i ens19 -p tcp --dport 80 -j DNAT --to-destination 10.0.2.10:80
iptables -t nat -A PREROUTING -i ens19 -p tcp --dport 8080 -j DNAT --to-destination 10.0.2.10:8080
iptables -t nat -A PREROUTING -i ens19 -p tcp --dport 2022 -j DNAT --to-destination 10.0.2.10:22
```

Permitir/filtrar tráfico

```bash
iptables -A FORWARD -p tcp -d 10.0.2.10 --dport 80 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -p tcp -d 10.0.2.10 --dport 8080 -j DROP
iptables -A FORWARD -p tcp -d 10.0.2.10 --dport 22 -j DROP
```

Masquerade para respuestas NAT

```bash
iptables -t nat -A POSTROUTING -j MASQUERADE
```

Persistencia de las reglas

```bash
sudo apt install iptables-persistent
sudo netfilter-persistent save
```

Comprobación

```bash
sudo iptables -t nat -L -n -v
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-7.png)

## Comprobación de funcionamiento

- En kali

![alt text](/assets/img/posts/nmap_firewall_bypass/image-8.png)

Podemos acceder sin problema a los servicios públicos simulados en el servidor interno a través de la IP externa del router.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-9.png)

No accesibles desde la red externa del router (desde kali).

Escaneo sencillo del router

![alt text](/assets/img/posts/nmap_firewall_bypass/image-10.png)

## (Opcional) Acceso de administrador como bastion host

Simulando de forma más realista (y por curiosidad) podríamos permitir a un administrador de sistemas acceder al panel interno del servidor a través del router.

SSH desde Kali al router (10.0.1.1), y desde ahí al servidor (10.0.2.10).

```bash
ssh usuario@10.0.1.1
```

Y dentro del router

```bash
ssh usuario@10.0.2.10
```

O creamos un túnel SSH

```bash
ssh -L 8080:10.0.2.10:8080 suri@10.0.1.1
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-11.png)

## Evasión de firewalls con nmap

### TCP Scan (-sT) y bloqueo

Un escaneo TCP scan (-sT) para comprobar los puertos abiertos de la máquina.

    Usa una conexión TCP completa (3-way handshake).

    Fácil de detectar y bloquear, especialmente en firewalls con reglas sobre paquetes SYN.

- Escaneo desde Kali

```bash
nmap -sT 10.0.1.1
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-12.png)

Deberías ver el puerto 80 como abierto (redirigido al servidor), y los otros filtrados o cerrados.

- Bloqueo en el router

Añadiremos la regla iptables necesaria para bloquear este escaneo.

```bash
iptables -I FORWARD -p tcp -d 10.0.2.10 --tcp-flags ALL SYN -j REJECT --reject-with tcp-reset
```

Esto bloquea cualquier intento de iniciar una conexión TCP al servidor a los puertos que se encuentren reenviando al servidor interno.

- Comprobación

```bash
nmap -sT -p 80,8080,2022 10.0.1.1
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-14.png)

 El bloqueo solo se aplica si:

    El tráfico pasa realmente por FORWARD, es decir, desde fuera hacia otra máquina.

    En este caso, nmap ve puertos abiertos del router mismo (10.0.1.1), no del servidor (10.0.2.10).

> Motivo: Estos escaneos usan data lengths de 40 bytes y no envían SYN, por lo que pueden pasar por alto una regla que solo bloquea SYN. Con Wireshark puedes confirmar los flags y el tamaño de cada paquete.
{: prompt-info}

### Bypass con escaneos FIN, NULL y XMAS

Saltar el filtrado de paquetes SYN usando escaneos alternativos más “sigilosos”.

Los firewalls que filtran solo SYN no los bloquean, por eso se usan para evasión.

- sF: FIN scan – solo envía paquetes con el flag FIN.

```bash
nmap -sF -p 22,80,8080,2022 10.0.1.1
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-13.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-15.png)

- sN: NULL scan – no establece ningún flag.

```bash
nmap -sN -p 22,80,8080,2022 10.0.1.1
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-16.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-18.png)

- sX: XMAS scan – envía FIN + PSH + URG.

```bash
nmap -sX -p 22,80,8080,2022 10.0.1.1
```
![alt text](/assets/img/posts/nmap_firewall_bypass/image-19.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-17.png)

### Bloqueo de FIN, NULL y XMAS

Configurar el firewall para bloquear estos escaneos alternativos.

- En el router

```bash
# Bloquear FIN scan
iptables -I FORWARD -p tcp -d 10.0.2.10 --tcp-flags ALL FIN -j REJECT --reject-with tcp-reset

# Bloquear NULL scan
iptables -I FORWARD -p tcp -d 10.0.2.10 --tcp-flags ALL NONE -j REJECT --reject-with tcp-reset

# Bloquear XMAS scan
iptables -I FORWARD -p tcp -d 10.0.2.10 --tcp-flags ALL FIN,PSH,URG -j REJECT --reject-with tcp-reset
```

- Desde Kali

![alt text](/assets/img/posts/nmap_firewall_bypass/image-20.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-21.png)

Ahora los escaneos no deberían retornar información útil (todo filtered).

### Filtrado por tamaño de paquetes (ej: 60 bytes)

Utilizar el tamaño de los paquetes para bloquear ciertos escaneos y luego intentar un bypass mediante un escaneo Stealth.

    Un TCP scan (-sT) tiene una data length de 60 bytes.

    Un Stealth scan (-sS) suele enviar SYN con data length ≈ 44 bytes.

Limpiamos las reglas anteriores.

```bash
sudo iptables -F
```

Filtrar paquetes por su tamaño, no por flags.

- En el router

```bash
iptables -I FORWARD -p tcp -d 10.0.2.10 -m length --length 60 -j REJECT --reject-with tcp-reset
```

Paquetes de 60 bytes (típico de -sT) serán bloqueados.

- Desde Kali

![alt text](/assets/img/posts/nmap_firewall_bypass/image-22.png)

    -sT será bloqueado.

    -sS (Stealth scan) podría funcionar, ya que suele usar menos bytes.

Dado que los paquetes en un stealth scan tienen data length de ~44, podrían evadir la regla de 60 bytes.

### Escaneo Fragmentado y tamaño personalizado

Usar fragmentación de paquetes y la opción --data-length de nmap para evadir bloqueos basados en el tamaño.

- En el router

```bash
sudo iptables -I INPUT -p tcp -m length --length 60 -j REJECT --reject-with tcp-reset
sudo iptables -I INPUT -p tcp -m length --length 44 -j REJECT --reject-with tcp-reset
sudo iptables -I INPUT -p tcp -m length --length 40 -j REJECT --reject-with tcp-reset

```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-23.png)

    Fragmented scan puede evitar las reglas.

    --data-length también si el tamaño no coincide con los bloqueados.

> Motivo: La fragmentación divide el TCP header en partes pequeñas, lo que puede hacer que el filtro basado en longitud no se aplique correctamente
{: prompt-info}

- Bloqueo por rango de longitud

 Para bloquear cualquier paquete cuyo tamaño esté entre 1 y 100

 ```bash
sudo iptables -I INPUT -p tcp -m length --length 1:100 -j REJECT --reject-with tcp-reset
```

> Efecto: Esto bloquea la mayoría de los tamaños pequeños, obligando al atacante a enviar paquetes de tamaño mayor (por ejemplo, --data-length 113), lo que puede ser detectado
{: prompt-info}



### Filtrado y Bypass basado en TTL

Utilizar el campo Time-To-Live (TTL) para filtrar paquetes y luego intentar un bypass ajustando este valor.

- En el router

Bloquear paquetes con TTL específico, por ejemplo, para bloquear paquetes con TTL igual a 64:

```bash
iptables -I FORWARD -p tcp --ttl-eq 64 -j REJECT --reject-with tcp-reset
```

> Motivo: Muchos escaneos envían paquetes con TTL de 64 por defecto
{. prompt-info}

Bloquear paquetes con TTL menor o igual a 64

```bash
iptables -I FORWARD -p tcp -m ttl --ttl-lt 65 -j REJECT --reject-with tcp-reset
```

- Desde Kali

Bypass modificando el TTL

![alt text](/assets/img/posts/nmap_firewall_bypass/image-24.png)

Con un TTL mayor, el paquete podría evadir el filtro basado en TTL.

### Filtrado por Puerto Origen y Bypass

Permitir solo conexiones que utilicen un puerto de origen específico y ver si se puede evitar esa restricción.

- En el router

Bloquear todo el tráfico que no tenga un puerto origen específico; por ejemplo, para permitir solo el puerto de origen 443.

```bash
iptables -I FORWARD -p tcp ! --sport 443 -j REJECT --reject-with tcp-reset
```

- En Kali

```bash
nmap -g 443 -p 80 192.168.0.19
```

![alt text](/assets/img/posts/nmap_firewall_bypass/image-25.png)

### Filtrado por Dirección MAC y Técnicas de MAC Spoofing

Permitir solo conexiones de una dirección MAC específica y luego falsificar la MAC para evadir el filtro.

- En el router

Bloquear todas las conexiones que no tengan la MAC permitida

```bash
iptables -A INPUT -p tcp -m mac ! --mac-source 00:11:22:33:44:55 -j DROP
```
Hay que tener en cuenta:

 - Direcciones MAC son de capa 2:
   Las direcciones MAC se utilizan a nivel de enlace (capa 2 del modelo OSI) y sólo son visibles dentro del mismo dominio de difusión (broadcast domain).

 - Ruteo y reescritura de MAC:
   Cuando un paquete atraviesa un router, la dirección MAC de origen se reemplaza por la dirección MAC de la interfaz de salida del router. Por eso, los filtros basados en MAC en una regla INPUT o FORWARD solo se aplican a tráfico que se origina o se encuentra en la misma red local.

Esto significa que en este laboratorio creado en Proxmox no podremos spoofear la MAC ya que tu router recibe como dirección MAC de origen la del bridge o interfaz virtual de Proxmox, no la de tu Kali (ni la que spoofeás con nmap).

Cuando hay un router o un bridge intermedio, se “reescribe” la MAC de origen al pasar paquetes.
Si Kali y el router están en redes distintas (o aunque sea la misma red IP, pero con un bridge virtual que reescribe MAC), el router no ve la MAC “real” de Kali, sino la del interfaz del Proxmox.

Podemos observar como aun indicando el spoofing la MAC.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-26.png)

No coinciden.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-27.png)

### Filtrado por Dirección IP y Técnicas de IP Spoofing

Aplicar reglas para filtrar por la IP de origen y luego intentar falsificar la IP con nmap.

- En el router

Bloquear conexiones de IPs que no sean la permitida; por ejemplo, permitir solo conexiones desde 10.0.1.20

```bash
sudo iptables -I FORWARD -p tcp -s 10.0.1.20 -j ACCEPT
sudo iptables -I FORWARD -p tcp ! -s 10.0.1.20 -j REJECT --reject-with tcp-reset
```

- En kali

Para “spoofear” solo en el envío sin que el sistema deje de recibir las respuestas, la técnica común es hacer que el sistema reconozca la IP que vas a usar como fuente, es decir, asignarla como un alias en tu interfaz. Esto permite que los paquetes salientes tengan la dirección IP falsificada (por ejemplo, 10.0.1.20) mientras que las respuestas, al llegar a esa IP, son aceptadas porque el sistema la reconoce como local.

```bash
sudo ip addr add 10.0.1.20/32 dev eth1
```

Esto le indica al kernel que 10.0.1.20 es una IP local, lo que permite enviar paquetes con esa dirección y recibir las respuestas.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-28.png)

![alt text](/assets/img/posts/nmap_firewall_bypass/image-30.png)

### Programación de Scripts NSE

Desarrollar y probar un script básico NSE para ampliar las capacidades de nmap.

Creamos un script de ejemplo sencillo para escanear un host y verificar si existen y son accesibles los archivos `robots.txt` y `sitemap.xml`.

```lua
---
-- robots-sitemap-check.nse
--
-- Descripción:
--   Script NSE para verificar si existen y son accesibles 'robots.txt' y 'sitemap.xml'
--   en un servicio web.
--
-- Uso de ejemplo:
--   nmap -p80,443 --script robots-sitemap-check <objetivo>
--
-- Autor: (sdksdk)
-- Licencia: Igual que la de Nmap (https://nmap.org/book/man-legal.html)
--

local http = require "http"
local shortport = require "shortport"
local stdnse = require "stdnse"

description = [[
Comprueba si un servidor web responde con éxito (HTTP 2xx/3xx) al solicitar
/robots.txt y /sitemap.xml, reportando si se detectan dichos archivos.
]]

categories = {"discovery"}

-- Regla de puerto: ejecuta el script en servicios que Nmap identifique como HTTP
portrule = shortport.http

-- Función auxiliar para comprobar un recurso
local function check_resource(host, port, path)
  local resp = http.get(host, port, path)
  if resp and resp.status and resp.status < 400 then
    -- Se considera "encontrado" si HTTP status es < 400
    -- (p.e. 200 OK, 301 Moved, etc.)
    return true, resp.status
  else
    return false, resp and resp.status or nil
  end
end

action = function(host, port)
  local results = {}

  -- 1) Comprobar /robots.txt
  local found_robots, status_robots = check_resource(host, port, "/robots.txt")
  if found_robots then
    table.insert(results, string.format("Encontrado /robots.txt (HTTP %d)", status_robots))
  else
    table.insert(results, "/robots.txt no accesible (404/403/...)")
  end

  -- 2) Comprobar /sitemap.xml
  local found_sitemap, status_sitemap = check_resource(host, port, "/sitemap.xml")
  if found_sitemap then
    table.insert(results, string.format("Encontrado /sitemap.xml (HTTP %d)", status_sitemap))
  else
    table.insert(results, "/sitemap.xml no accesible (404/403/...)")
  end

  return table.concat(results, "\n")
end

```

Copiar, actualizar y ejecutar el script:

  - Copia el archivo en el directorio de scripts de Nmap.

    `sudo cp robomap.nse /usr/share/nmap/scripts/`

  - Actualiza el índice de scripts:

    `sudo nmap --script-updatedb`

  - Para escanear host(s) en puertos 80 y 443:

    `nmap -p80,443 --script robots-sitemap-check <objetivo>`

Si un servidor responde en otro puerto (por ejemplo, 8080) y Nmap lo detecta como HTTP, también ejecutará el script en ese puerto.

![alt text](/assets/img/posts/nmap_firewall_bypass/image-29.png)

Para más referencias sobre como se manejan los scripts en NMAP o como crear uno, puedes consultar la documentación de [NMAP](https://nmap.org/book/man-nse.html) y su [tutorial](https://nmap.org/book/nse-tutorial.html).

