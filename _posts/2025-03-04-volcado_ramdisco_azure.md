---
title: Dump de memoria RAM y disco en entornos IaaS (Azure)
date: 2025-03-03 14:00:00 +0000
categories: [Forense, Azure]
tags: [Forense, Memory Dump, Disk Dump, Azure, Memory Dump, Disk Dump]
image:
  path: /assets/img/cabeceras_genericas/azure.webp
  alt:  Azure
description: >
  Guía para volcado de memoria y disco en Azure
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Introducción 

En esta sección vamos a ver como podemos crear un volcado de memoria RAM y disco duro en Azure.

A diferencia de la sección donde veíamos el proceso en un entorno de virtualización [Proxmox VE](https://sproffes.github.io/posts/proxmox-_volcado_ram_disco/), en azure no tenemos posibilidad de forma centralizada de crear volcados de ram por lo que vamos a necesitar acceso directo a la máquina afectada para poder realizar este tipo de operaciones. Sin embargo si que contamos con capacidad para crear volcados de disco duro.

## Volcado de RAM

Para realizar este tipo de operaciones vamos a necesitar tener acceso a la máquina que queremos volcar. En nuestro caso es una máquina de pruebas con poca memoria RAM y disco duro por lo que los volcados de RAM no serán muy pesados.

Dentro de nuestro panel de administración Azure vamos a iniciar la máquina. Suponiendo que la máquina ya está completamente configurada solo los queda acceder por SSH o el panel de administración CLI de Azure.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image.png)

Aquí tenemos ambas opciones para acceder a la máquina.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-1.png)

Para el volcado de RAM en este caso vamos a utilizar [AVML](https://github.com/microsoft/avml) ya que es sencillo de usar, no requiere compilación ni instalación de ninguna herramienta.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-2.png)

Damos permisos de ejecución al binario y lo ejecutamos como sudo.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-3.png)

Cuando tengamos el archivo podemos copiarlo a nuestra máquina local por SCP.

```bash
scp -C -p user@100.100.100.100:/home/user/memdump ./memdump
```

Adicionalemente podemos descargarlo desde la interfaz CLI de Azure.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-4.png)

## Volcado de disco 

Para crear el volcado de disco podemos hacerlo mediante el uso de la interfaz CLI de Azure o la interfaz web de Azure.

### Interfaz web de Azure

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-5.png)

Al crear esta snapshot nos aseguramos de que es completa y que el tipo de almacenamiento es local.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-6.png)

El resto de opciones podemos dejar como están ya que luego esta snapshot será eliminada.

Ahora que tenemos esta snapshot podemos crear el disco de nuevo para poder exportarlo sin miedo a perdida o corrupción de datos.

Navegamos al recurso y creamos e disco nuevo.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-8.png)

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-7.png)

Ahora nos dirigimos al recurso y en el panel izquierdo buscamos la opción de exportar el disco.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-9.png)

Aquí podremos generar la URL temporal para descargar el archivo y además podemos añadir una autenticación de seguridad que sería lo óptimo para un caso de uso real aunque para este caso no es necesario.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-10.png)

Una vez generados tenemos las url.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-11.png)

### Interfaz CLI de Azure

Para ejecutar este Azure CLI para este caso vamos a utilizar la versión para Windows.

Primero debemos iniciar sesión en la cuenta que tenga acceso a la máquina que queremos volcar.

```powershell
az login
```

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-12.png)

Para crear un snapshot, necesitas saber el ID.

```powershell
az vm show --resource-group <nombre-del-grupo-de-recursos> --name <nombre-de-la-vm> --query "storageProfile.osDisk.managedDisk.id" -o tsv
```

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-13.png)

Creamos el snapshot de la máquina.

```powershell
az snapshot create \
  --resource-group <nombre-del-grupo-de-recursos> \
  --source <disk-id> \
  --name <nombre-del-snapshot> \
  --output json
```

Pasamos la snapshot a disco.

```powershell
az disk create \
  --resource-group <nombre-del-grupo-de-recursos> \
  --name <nombre-del-disco> \
  --source <snapshot-id> \
  --output json
```

En este caso ya hicimos el disco mediante la interfaz web por lo que vamos a reutilizarlo.

Ahora generamos la URL para descargar el archivo.

```powershell
az disk grant-access \
  --resource-group <nombre-del-grupo-de-recursos> \
  --name <nombre-del-disco> \
  --duration-in-seconds 3600 \
  --access-level Read
```

Una vez creado la URL podemos descargar el archivo igua que antes.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-14.png)

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-15.png)

## Uso de libcloudforensics

Existen herramientas que permiten realizar este tipo de operaciones de forma automatizada en diferentes proveedores como AWS, Azure, etc.

[Libcloudforensics](https://github.com/google/cloud-forensics-utils)

En este caso estamos ante un módulo de python.

Para instalar la librería necesitamos ejecutar el siguiente comando:

```bash
pip install libcloudforensics
```

Antes de continuar vamos a necesitar hacer unas configuraciones en nuestro entorno de trabajo de pruebas.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-16.png)

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-17.png)

Una vez creado el registro de la aplicación ahora tenemos los datos necesarios para realizar el volcado de disco.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-18.png)

Añadimos ahora un certificado de acceso.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-19.png)

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-20.png)

Perfecto, ahora vamos a crear un script con el siguiente contenido, que nos permitirá establecer las variables necesarias para ejecutar los comandos de la librería y realizar el volcado de disco.

La idea principal de este modulo es crear una copia del disco de una cuenta de Azure a otra. Esto viene bien ya que podríamos analizar la máquina con diferentes respaldos de forma independiente a la afectada.

Primero necesitamos establecer las variables de entorno si queremos realizar el clonado en la misma cuenta de Azure.

```python
export AZURE_SUBSCRIPTION_ID=xxx
export AZURE_CLIENT_ID=xxx
export AZURE_CLIENT_SECRET=xxx
export AZURE_TENANT_ID=xxx
```

Si queremos copiar el disco a otra cuenta de Azure debemos crear un archivo con las de ambas cuentas en `~/.azure/credentials.jso`

```json
{
  # Access credentials to Account A
  'src_profile': {
      'subscriptionId': xxx,
      'tenantId': xxx,
      'clientId': xxx,
      'clientSecret': xxx
  },
  # Access credentials to Account B
  'dst_profile': {
      'subscriptionId': yyy,
      'tenantId': yyy,
      'clientId': yyy,
      'clientSecret': yyy
  },
  ...
}
```

En este caso dejamos el clonado en la misma cuenta de Azure.

Ahora tenemos que asignar los permisos necesarios al equipo para acceder a los recursos.

```powershell
az role assignment create --assignee <client-id> --role "Contributor" --scope /subscriptions/<subscription-id>
```

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-21.png)

Para comprobar que es correcto.

```powershell
az role assignment list --assignee <client-id> --output table
```

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-22.png)

Con todo listo vamos a utilizar el siguiente script donde establecemos las variables necesarias para la ejecución del script y además podemos seleccionar las diferentes opciones que queramos.

```python
import os
from libcloudforensics.providers.azure import forensics

# Set environment variables
os.environ["AZURE_SUBSCRIPTION_ID"] = "xxx"
os.environ["AZURE_CLIENT_ID"] = "xxx"
os.environ["AZURE_CLIENT_SECRET"] = "xxx"
os.environ["AZURE_TENANT_ID"] = "xxx"


def main():
    print("Environment variables configured.")
    
    # Prompt for user inputs
    resource_group = input("Enter the resource group name: ")
    disk_name = input("Enter the disk name: ")

    print("Choose a scenario to create a disk copy:")
    print("1. Use environment variables for credentials (default region)")
    print("2. Use environment variables for credentials (specific region)")
    print("3. Use profiles from ~/.azure/credentials.json")
    
    choice = input("Enter the number of your choice (1, 2, or 3): ")

    if choice == '1':
        copy = forensics.CreateDiskCopy(resource_group, disk_name=disk_name)
        print("Disk copy created using Scenario 1.")
    elif choice == '2':
        region = input("Enter the region (e.g., 'westus'): ")
        copy = forensics.CreateDiskCopy(resource_group, disk_name=disk_name, region=region)
        print("Disk copy created using Scenario 2.")
    elif choice == '3':
        src_profile = input("Enter the source profile: ")
        dst_profile = input("Enter the destination profile: ")
        copy = forensics.CreateDiskCopy(resource_group, disk_name=disk_name, src_profile=src_profile, dst_profile=dst_profile)
        print("Disk copy created using Scenario 3.")
    else:
        print("Invalid choice. Please run the script again and choose a valid option.")

if __name__ == "__main__":
    main()

```
Cuando ejecutemos seleccionamos la opción que necesitemos y esto realizará el proceso anterior de forma automática.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-23.png)

Vemos que incluso elimina la snapshot de la máquina creada, etc. para únicamente conservar el disco clonado.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-24.png)

Para poder descargar el disco, simplemente realizamos los mismos pasos que se vieron en la interfaz web Azure.

![alt text](/assets/img/posts/cloud-forense-IaaS-azure/image-25.png)