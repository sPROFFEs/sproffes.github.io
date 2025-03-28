---
title: Reto DFIR 1 - Atenea CCN
date: 2025-01-15 10:19:16 +0100
categories: [Laboratorios, DFIR]
tags: [dfir, forensics, truecrypt, memory analysis, volatility]
---

## Recursos

[Descarga del dump usado (Google Drive)](https://drive.google.com/file/d/1J_OfVL5IzVE44t5fergJA146wnbDSHA6/view)

## Contexto

La policía ha detenido a un sujeto y tenemos como evidencia el ordenador encendido.
Se le ha realizado una captura de RAM y análisis de la memoria no volátil. En ella se ha
encontrado un extraño fichero que no saben de que puede ser.

Tenemos un fichero llamado magic_file sin extension del cual no sabemos nada, solo que parece encriptado debido a la alta entropia de los datos contenidos.

## Analisis de procesos

Primero vamos a ver que procesos estaban abiertos en el momento

![Listado de procesos en memoria](/assets/img/posts/atenea_dfir_1/20250115_101916_2025-01-15_11-19.png)

De la lista de procesos en la memoria, algunos pueden llamar la atención:

- MagnetRAMCapture.exe (PID 3120): Este es un software legítimo utilizado para capturar RAM, pero su presencia puede indicar que alguien realizó una captura de memoria en este sistema. Evalúa el motivo y quién pudo haberlo usado.

- TrueCrypt.exe (PID 3612): TrueCrypt es una herramienta de cifrado. Su presencia puede sugerir que hay volúmenes cifrados en el sistema, tal vez relacionados con el archivo magic_file.

- sppsvc.exe (PID 3076): Servicio relacionado con la protección de software de Windows. Aunque es legítimo, en ocasiones se aprovecha para esconder malware.

- WmiPrvSE.exe (PIDs 404 y 2948): Normalmente son legítimos, pero múltiples instancias simultáneas pueden ser sospechosas.

## Proceso TrueCrypt

Ya que nuestro fichero parece encriptado es posible pensar que se hizo mediante este software.

TrueCrypt fue un popular software de encriptación descontinuado a partir de 2015 y el proyecto Veracrypt tomó el relevo del mismo.

Por suerte para este tipo de casos ya existe un plugin en volatility que nos puede ser de utilidad con TrueCrypt

![Extracción de contraseña](/assets/img/posts/atenea_dfir_1/20250115_102236_2025-01-15_11-22.png)
_Extrae la contraseña de encriptación cargada en el proceso de TrueCrypt si este se encontraba en ejecución al momento de la captura_

## Identificación del fichero objetivo

Ya que tenemos la posible contraseña para descifrar el contenido del fichero ahora podemos probar a desencriptar los datos haciendo uso de dos variantes:

- Usar veracrypt:

  Es posible que alguna de las primeras versiones de veracrypt contase con un modulo de compatibilidad para TrueCrypt pero en las últimas versiones esto ha sido eliminado

- Usar TrueCrypt:

  Ya que sabemos que el proceso en ejecución se trataba de TrueCrypt podemos utilizar a última versión disponible antes de su descontinuación

### Enlace de TrueCrypt

[Web Oficial](https://www.truecrypt71a.com/downloads/)

Vamos a utilizar la versión Linux x64 cli.

Para instalar damos permisos de ejecución al script de instalación y seleccionamos instalación completa o temporal.

## Desencriptado y acceso a los datos

![Proceso de desencriptado](/assets/img/posts/atenea_dfir_1/20250115_103036_2025-01-15_11-30.png)

Creamos la ruta para montar el volumen y utilizamos la contraseña anteriormente extraida para visualizar el contenido.