---
categories:
- Guia
- IDS
date: 2025-01-19 11:58:38 +0000
math: false
mermaid: false
pin: false
render_with_liquid: true
tags:
- ids
- velociraptor
title: 'Guía de Instalación y Configuración de Velociraptor en Ubuntu Server'
---

* Requisitos Previos
  * Un servidor Ubuntu Server (recomendado 20.04 LTS o superior)
  * Acceso de usuario con privilegios sudo
  * Conexión a internet





# Pasos de Instalación

## Actualizar el Sistema

```bash
sudo apt update
sudo apt upgrade -y

```

## Descargar Velociraptor

```bash
# Verificar la última versión en https://github.com/Velocidex/velociraptor/releases
wget https://github.com/Velocidex/velociraptor/releases/download/v0.73/velociraptor-v0.73.1-linux-amd64
chmod +x velociraptor-v0.73.1-linux-amd64
```

## Configuración Inicial

```bash
# Crear directorio de configuración
sudo mkdir /opt/velociraptor

# Generar configuración de servidor
sudo ./velociraptor-v0.73.1-linux-amd64 config generate -i 
```

* Durante la configuración interactiva, te preguntará:
  * Tipo de despliegue (server, client, o standalone)
  * Dirección IP del servidor
  * Puertos a utilizar
  * Configuración de CA y certificados

![Desktop View](/assets/img/posts/velociraptor/Peek 2025-01-19 14-39.gif){: .center }

## Configurar IP de la interfaz

```bash
sudo nano /opt/velociraptor/server.config.yaml
```
![Desktop View](/assets/img/posts/velociraptor/Peek 2025-01-19 14-40.gif){: .center }

## Crear instalador de servicio

```bash
sudo ./velociraptor-v0.73.1-linux-amd64 --config /opt/velociraptor/server.config.yaml debian server --binary velociraptor-v0.73.1-linux-amd64

sudo dpkg -i velociraptor_server_0.73.1_amd64.deb
```

## Iniciar y Habilitar el Servicio

```bash
# Recargar systemd
sudo systemctl daemon-reload

# Iniciar servicio
sudo systemctl start velociraptor

# Habilitar inicio automático
sudo systemctl enable velociraptor

# Verificar estado
sudo systemctl status velociraptor
```

## Acceso Web

![Desktop View](/assets/img/posts/velociraptor/Peek 2025-01-19 15-03.gif){: .center }

# Ejemplo de Prueba: Monitoreo de un Cliente


## En el Servidor: Generar Configuración de Cliente

```bash
wget https://github.com/Velocidex/velociraptor/releases/download/v0.73/velociraptor-v0.73.1-windows-amd64.exe

# Generar paquete de instalación para cliente Linux
sudo ./velociraptor-v0.73.1-linux-amd64 config repack --exe velociraptor-v0.73.1-windows-amd64.exe /opt/velociraptor/client.config.yaml VelociraptorClient.exe
```

## En el Cliente Windows:


```powershell
.\VelociraptorClient.exe service install 
```

## En la interfaz web:

![Desktop View](/assets/img/posts/velociraptor/Peek 2025-01-19 15-20.gif){: .center }
![Desktop View](/assets/img/posts/velociraptor/Peek 2025-01-19 14-50.gif){: .center }
