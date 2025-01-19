---
title: Baron Samedit - Escalación de privilegios en Linux
date: 2025-01-11 13:01:50 +0100
categories: [Labs & CTF, Privilege Escalation]
tags: [linux, privilege escalation, sudo, vulnerability, cve-2021-3156]
---

En enero de 2021, Qualys publicó un artículo en su blog explicando una nueva vulnerabilidad crítica en el programa sudo de Unix.

Esta vulnerabilidad era un desbordamiento de memoria en el montón (heap buffer overflow) que permitía a cualquier usuario obtener privilegios de administrador (root), sin que fuera necesario que el sistema tuviera configuraciones incorrectas. Lo preocupante de este fallo es que funciona con la configuración predeterminada y afecta a cualquier usuario, sin importar los permisos que tenga configurados en sudo. Aunque la vulnerabilidad ya fue corregida, afecta a las versiones no actualizadas del programa sudo entre la 1.8.2 y la 1.8.31p2, y entre la 1.9.0 y la 1.9.5p1, lo que significa que este fallo estuvo presente durante una década.

El problema se solucionó rápidamente, y las versiones parcheadas se distribuyeron pronto en los repositorios oficiales, por lo que los sistemas actualizados ya no son vulnerables. Sin embargo, en sistemas que aún no han sido actualizados, esta vulnerabilidad sigue siendo muy peligrosa.

Esta vulnerabilidad, al igual que la CVE-2019-18634, está relacionada con un desbordamiento de memoria en el programa sudo. Sin embargo, en este caso, se trata de un desbordamiento en el montón (heap), no en la pila (stack), como en el caso anterior. La pila es una parte de la memoria que organiza y gestiona datos clave del programa de manera estricta, mientras que el montón es un espacio de memoria más flexible, usado para la asignación dinámica. Aunque no profundizaremos en los detalles técnicos para mantener el contenido accesible, lo importante es entender que esta vulnerabilidad es extremadamente potente y afecta a un gran número de sistemas.

## Comprobación

Primero comprobamos si el sistema es vulnerable:

```bash
sudoedit -s '\' $(python3 -c 'print("A"*1000)')
```

![Si el sistema es vulnearble obtenemos un error por corrupción de memoria](/assets/img/posts/baron_samedit/20250111_130150_2025-01-11_14-01.png)
_Si el sistema es vulnearble obtenemos un error por corrupción de memoria_

Este PoC fue descubierto por lockedbyte:

[Github](https://github.com/lockedbyte/CVE-Exploits/tree/master/CVE-2021-3156)

## Explotación

Cuando Qualys anunció esta vulnerabilidad, no proporcionó el código completo para explotarla. Sin embargo, otros investigadores pronto lograron recrear el fallo. El primer exploit completamente funcional que se publicó fue desarrollado por un investigador apodado bl4sty, y su código está disponible en Github. En esta práctica, utilizaremos ese exploit para aprovechar la vulnerabilidad.

[Github](https://github.com/blasty/CVE-2021-3156)

Con el repositorio clonado debemos compilar el PoC:

```bash
make
```

![Compilación del exploit](/assets/img/posts/baron_samedit/20250111_130714_2025-01-11_14-07.png)

```bash
ls -la
```

![Listado de archivos](/assets/img/posts/baron_samedit/20250111_130918_2025-01-11_14-09.png)

```bash
./sudo-hax-me-a-sandwich
```

![Ejecución del exploit](/assets/img/posts/baron_samedit/20250111_131028_2025-01-11_14-10.png)

Como tenemos que seleccionar la versión del sistema podemos verificar cual es de la siguiente forma:

```bash
cat /etc/issue
```

![Verificación de versión](/assets/img/posts/baron_samedit/20250111_131601_2025-01-11_14-15.png)

Ahora que sabemos la verión concreta ejecutamos el exploit:

```bash
./sudo-hax-me-a-sandwich 0
```

![Ejecución final del exploit](/assets/img/posts/baron_samedit/20250111_131727_2025-01-11_14-17.png)

## Explicación

### Explicación del Heap Buffer Overflow

Un heap buffer overflow ocurre cuando un programa escribe más datos en un búfer (un área de memoria) de lo que este puede manejar. El heap es una región de la memoria utilizada para la asignación dinámica de memoria, es decir, cuando el programa necesita reservar memoria de manera flexible durante su ejecución.

### El funcionamiento de la vulnerabilidad

El error se origina en la forma en que sudo maneja ciertos argumentos de la línea de comandos cuando se utiliza para ejecutar otros programas. sudo tiene una función interna que procesa estos argumentos, y allí es donde ocurre el desbordamiento.

Normalmente, cuando usas sudo, este se encarga de verificar que el usuario tenga los permisos necesarios para ejecutar el comando. Si todo está bien, se ejecuta el comando con privilegios elevados.

El fallo está relacionado con cómo sudo maneja la memoria para los argumentos de un comando en ejecución. Debido a un desbordamiento de búfer en el heap, se puede sobrescribir un área crítica de memoria, lo que permite a un atacante modificar el flujo de control del programa. En otras palabras, el atacante puede inyectar código arbitrario en la memoria del programa y cambiar su comportamiento.

### Cómo se explota

Para explotar esta vulnerabilidad, un atacante envia una entrada maliciosa a sudo que cause el desbordamiento de búfer en el heap. Este desbordamiento podría corromper datos clave en la memoria del programa, como la dirección de retorno de una función o las variables de control, permitiendo al atacante ejecutar código arbitrario.

En este caso, el atacante no necesita estar en un grupo con privilegios de sudo, porque el fallo no depende de la configuración de sudoers (el archivo que determina quién puede usar sudo), sino de un defecto en el manejo de la memoria de sudo.

### Estructura de control del flujo (return address)

Uno de los objetivos principales de un desbordamiento de búfer es sobrescribir la dirección de retorno de una función.

Esta dirección se almacena en la pila, y cuando una función termina de ejecutarse, el programa regresa a la dirección que está en la variable de retorno para continuar la ejecución.

Al sobrescribir la dirección de retorno, se puede hacer que el programa salte a una dirección de memoria arbitraria, en lugar de regresar de manera normal a la función que lo llamó.

Permite que el atacante redirija la ejecución del programa a código malicioso.

### Variables de control de seguridad (como los punteros a funciones)

Las funciones dentro de sudo realizan varias verificaciones de seguridad para asegurarse de que el usuario tiene los permisos adecuados. Un atacante puede intentar sobrescribir variables relacionadas con el control de acceso, como los punteros a las funciones que realizan estas verificaciones.

Si se sobrescriben estos punteros, podría hacer que el programa llame a funciones maliciosas en lugar de las funciones de verificación de permisos, permitiendo la escalada de privilegios.

Permiten al atacante evitar las verificaciones de permisos y ejecutar comandos con privilegios elevados.

### Memoria relacionada con la configuración de sudoers

Potencialmente permite que el atacante manipule configuraciones para ejecutar comandos sin permisos.

### Buffers de argumentos de comando

Permiten la inyección de comandos maliciosos para ejecutar como root.

### Punteros a la memoria en el heap

Permiten redirigir la ejecución hacia código controlado por el atacante.

Esto es un resumen del concepto explicado lo más simple posible para entender el funcionamiento del mismo.