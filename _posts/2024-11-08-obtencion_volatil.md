---
title: Adquisición de Evidencias Volátiles
date: 2024-11-08 11:58:38 +0000
categories: [Forense, Memoria RAM]
tags: [memoria, ram, windows, linux, dumpit, belkasoft, lime, avml]
---


## Introducción

Esta guía presenta diferentes herramientas y métodos para realizar volcados de memoria RAM en caliente en sistemas Windows y Linux. Se analizarán cuatro herramientas principales, sus características y procedimientos de uso.

## Configuración Previa en Windows

> **¡Importante!**
{: .prompt-warning }
> 
> Para realizar volcados de memoria en Windows 10/11 es necesario desactivar la medida de seguridad de aislamiento del núcleo en la configuración de seguridad del dispositivo.

![Configuración de seguridad del dispositivo en Windows](/assets/img/posts/obtencion_volatil/1.png)
_Configuración de seguridad del dispositivo en Windows_

## Herramientas Seleccionadas

### 1. DumpIT (Windows)

Herramienta gratuita para Windows que permite realizar volcados de memoria de forma simple y directa.

[🔗 Descargar DumpIT](https://www.comae.com/){:target="_blank"}

![Interfaz de línea de comandos de DumpIT](/assets/img/posts/obtencion_volatil/2.png)
_Interfaz de línea de comandos de DumpIT_

#### Características principales:

- Ejecución simple con un solo comando
- Debe ejecutarse como administrador
- El volcado se realiza en la misma ubicación del ejecutable

### 2. Belkasoft RAM Capturer (Windows)

Programa gratuito que requiere registro previo para su descarga oficial.

[🔗 Descargar Belkasoft RAM Capturer](https://belkasoft.com/ram-capturer){:target="_blank"}

![Interfaz de Belkasoft RAM Capturer](/assets/img/posts/obtencion_volatil/3.png)
_Interfaz de Belkasoft RAM Capturer mostrando la selección de ruta_

#### Características principales:

- Disponible en versiones de 32 y 64 bits
- Interfaz que permite seleccionar la ruta de destino
- Proceso de volcado simplificado

### 3. LiME (Linux)

Proyecto open source para volcado de RAM en sistemas Linux, incluyendo Android.

[🔗 Repositorio de LiME](https://github.com/504ensicsLabs/LiME){:target="_blank"}

```bash
git clone https://github.com/504ensicsLabs/LiME.git
```

![Compilación de LiME](/assets/img/posts/obtencion_volatil/4.png)
_Proceso de compilación de LiME y archivo resultante_

#### Características principales:

- Compatible con múltiples distribuciones Linux
- Soporta volcado remoto mediante netcat
- Utiliza el kernel de forma directa
- Soporta formatos raw y lime

### 4. Microsoft AVML (Linux)

Herramienta desarrollada por Microsoft para volcado de RAM en sistemas Linux.

[🔗 Repositorio de AVML](https://github.com/microsoft/avml){:target="_blank"}

![Compilación de AVML](/assets/img/posts/obtencion_volatil/5.png)
_Compilación de AVML_

![Comparación de tamaños AVML](/assets/img/posts/obtencion_volatil/6.png)
_Comparación de tamaños de volcado con y sin compresión en AVML_

#### Características principales:

- Distribuida como binario ejecutable
- Incluye opciones de compresión
- No requiere instalación

## Conclusiones y Recomendaciones

### Para Windows:

DumpIT es la opción recomendada por su mínimo impacto en el sistema y facilidad de uso. No requiere instalación y puede ejecutarse directamente desde un dispositivo externo.

### Para Linux:

Aunque LiME es una herramienta muy potente y compatible, AVML puede ser más práctica en muchos casos ya que:

- No requiere instalación de dependencias
- Se ejecuta como binario independiente
- No necesita modificar módulos del kernel