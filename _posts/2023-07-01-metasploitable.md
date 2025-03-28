---
title: Configuración de Metasploitable 3
date: 2023-07-01
categories: [Guia, Maquinas]
tags: [metasploitable3, vmware, security-lab]
---

En esta guía veremos cómo configurar el entorno vulnerable Metasploitable 3, que consta de dos servidores: un servidor Ubuntu Linux y un Windows Server.

## Preparación Inicial

Este entorno vulnerable va a estar formado por dos servidores, un primer servidor Linux, que se corresponderá con un Ubuntu y un segundo servidor Windows que se corresponderá con un Windows Server.

El repositorio oficial del proyecto se encuentra en:
[https://github.com/rapid7/metasploitable3](https://github.com/rapid7/metasploitable3)

Vamos al siguiente enlace y descargamos las imágenes para nuestra versión de software que en este caso será vmware_desktop:
[https://app.vagrantup.com/rapid7/](https://app.vagrantup.com/rapid7/)

Con ambos archivos descargados les cambiamos la extensión a .zip. Al terminar la descompresión, con los archivos resultantes repetimos el proceso.

![Preparación de archivos](/assets/img/posts/metasploitable3/20241125_210709_93-1.png)
_Cambiamos el nombre a las carpetas y las movemos a nuestro directorio de máquinas virtuales para añadirlas a VMware._

![Configuración VMware](/assets/img/posts/metasploitable3/20241125_210901_93-2.png)

![Configuración VMware](/assets/img/posts/metasploitable3/20241125_210929_93-3.png)

Vamos a configurar la red y algunas configuraciones más.

## Ubuntu

Usuario: vagrant | Password: vagrant

![Configuración de red](/assets/img/posts/metasploitable3/20241125_211114_93-4.png)
_Configuramos una subred que en mi caso asigna a los nodos en 192.168.20.0_

![Configuración adicional](/assets/img/posts/metasploitable3/20241125_211206_93-5.png)

Vamos a eliminar las reglas IPtables de la máquina que se tratan de un "firewall" implementado en máquinas linux para evitar problemas o limitaciones de conexión entre las máquinas.

```bash
iptables -S
```

![IPtables inicial](/assets/img/posts/metasploitable3/20241125_211255_93-6.png)

```bash
sudo iptables -F
```

![IPtables limpio](/assets/img/posts/metasploitable3/20241125_211326_93-7.png)
_Si se reinicia la máquina puede que se vuelvan a añadir así que si existen problemas de conexión es conveniente revisar si existen o no estas reglas._

## Windows

Ambos usuarios tienen la contraseña "vagrant". No está activada pero no importa y además pedirá reiniciar la máquina para instalar vmware tools.

Añadimos la máquina a nuestra subred:

![Configuración de red Windows](/assets/img/posts/metasploitable3/20241125_211417_93-9.png)

![Opciones de red](/assets/img/posts/metasploitable3/20241125_211438_93-10.png)
_vamos a las opciones de red_

![Opciones avanzadas](/assets/img/posts/metasploitable3/20241125_211511_93-11.png)
_Cambiar opciones avanzadas_

![Activar opciones](/assets/img/posts/metasploitable3/20241125_211525_93-12.png)
_Activamos todas las opciones_

Comprobamos conectividad entre las máquinas:

![Prueba de conectividad](/assets/img/posts/metasploitable3/20241125_211550_93-13.png)

![Prueba de conectividad adicional](/assets/img/posts/metasploitable3/20241125_211604_93-14.png)