---
title: Clonado de Disco por Red
date: 2024-10-20 11:58:38 +0000
categories: [Forense, Discos]
tags: [forense, clonado, network]
---

## Configuración Inicial

Para comenzar vamos a plantear la máquina de la que debemos obtener las evidencias que en este caso es llamada DC-1.

![Configuración DC-1](/assets/img/posts/clonado_de_disco_red/1.png)
_Máquina DC-1 con 4GB de disco duro en red privada host-only_

Como observamos tenemos una máquina ligera con tan solo 4Gb de disco duro ya que se trata de un "mini" servidor vulnerable pero para el caso nos servirá.

![Configuración Kali](/assets/img/posts/clonado_de_disco_red/2.png)
![Configuración Kali](/assets/img/posts/clonado_de_disco_red/3.png)
_Máquina Kali y Parrot en la misma red local_

> Más adelante se añade una nota al proceso de clonado por netcat porque han surgido complicaciones con el sistema inicial de la estación forense parrot. Así que en esa parte se hace un cambio a esta máquina kali.

## Preparación del Entorno

Para comenzar la máquina forense debe estar ya encendida y antes de abrir la máquina de las evidencias vamos a asignarle el inicio de kali live.

![Inicio Kali Live](/assets/img/posts/clonado_de_disco_red/4.png)
_Inicio de máquina en modo Kali Live_

Recordad iniciar la máquina en modo forense.

![Verificación de conectividad](/assets/img/posts/clonado_de_disco_red/5.png)
_Comprobación de conectividad entre máquinas_

### Verificación de Conectividad

![Verificación de conectividad](/assets/img/posts/clonado_de_disco_red/6.png)
_Comprobación de conectividad entre máquinas_

### Identificación de Discos

![Listado de discos](/assets/img/posts/clonado_de_disco_red/7.png)
_Listado de discos disponibles_

## Clonado por SSH

En este caso haremos uso de una conexión mediante SSH para la transferencia de datos.

### Configuración de SSH en Parrot OS

```bash
# 1. Verificar instalación SSH
sudo apt install openssh-server

# 2. Habilitar e iniciar servicio SSH
sudo systemctl enable ssh
sudo systemctl start ssh

# 3. Verificar estado del servicio
sudo systemctl status ssh

# 4. Configurar firewall
sudo ufw allow 22/tcp
sudo ufw enable

# 5. Verificar puerto
sudo netstat -tulpn | grep 22
```

![Clonado por SSH](/assets/img/posts/clonado_de_disco_red/8.png)
![Clonado por SSH](/assets/img/posts/clonado_de_disco_red/9.png)
![Clonado por SSH](/assets/img/posts/clonado_de_disco_red/10.png)
_Proceso de clonado mediante SSH_

> Este mismo proceso se puede realizar comprimiendo la clonación para que pese menos:
> ```bash
> dd if=/dev/sdaX | gzip -1 - | ssh usuario@estacion_forense "dd of=/ruta/imagen.gz"
> ```

## Clonado por Netcat

En este caso haremos uso de netcat para el envío de los datos por red.

{: .warning }
Se trata de un proceso más rápido debido a que el envío de datos se hace por el protocolo UDP pero es más susceptible a fallos o corrupción de paquetes en tránsito debido a la naturaleza del mismo.

{: .note }
En este proceso he tenido problemas con la máquina original utilizada como estación forense por lo que se ha cambiado rápidamente a un kali linux ya que la original era un Parrot OS. El problema reside en la configuración del firewall en parrot y aun no he dado con la solución.

![Clonado por Netcat](/assets/img/posts/clonado_de_disco_red/11.png)
![Clonado por Netcat](/assets/img/posts/clonado_de_disco_red/12.png)
_Proceso de clonado mediante Netcat_

### Verificación de Hash

![Verificación de hash](/assets/img/posts/clonado_de_disco_red/13.png)
_Comparación de hash entre origen y destino_