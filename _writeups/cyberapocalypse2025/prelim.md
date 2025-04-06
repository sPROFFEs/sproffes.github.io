---
title: "Prelim - Cyber Apocalypse 2025"
layout: post
permalink: /writeups/cyberapocalypse2025/prelim
categories: [HacktheBox, CTF]
tags: [CyberApocalypse, HTB, Crypto]
description: >
  Resolución del reto Prelim de la categoría Crypto durante el CTF HackTheBox Cyber Apocalypse 2025.
pin: false
toc: true
math: false
mermaid: false
---

## 1. La permutación y su potencia

En el código original, se genera una lista `message` de tamaño `n = 0x1337 = 4919` que contiene los números del 0 al 4918 y se le aplica `shuffle`, produciendo una **permutación** \(p\).

Posteriormente, se toma esa permutación y se **eleva** a la potencia \(e = 65537\):
\[
p^e = \underbrace{p \circ p \circ \cdots \circ p}_{e\text{ veces}}
\]

Esta operación es simplemente la composición repetida de la permutación consigo misma.  
En el fichero `tales.txt` nos proporcionan directamente esta permutación elevada:

```
scrambled_message = [...]
```

---

## 2. Generación de la clave y cifrado de la flag

La clave de cifrado es:

```
key = sha256(str(p).encode())
```

Esta clave se usa para cifrar la flag mediante **AES en modo ECB**.  
Nos dan también:

- `scrambled_message` = \(p^e\)
- `enc_flag` = AES-ECB( key, flag_padded )

Pero no conocemos directamente la permutación \(p\), solo \(p^e\). El reto consiste en obtener \(p\) a partir de \(p^e\) para poder calcular la clave.

---

## 3. ¿Por qué se puede invertir \(p^e\)?

Gracias a propiedades de las permutaciones:

- Toda permutación puede descomponerse en **ciclos disjuntos**.
- Cada ciclo de \(p\) y su correspondiente ciclo en \(p^e\) tienen la misma longitud, ya que \(e = 65537\) es un primo mayor que cualquier ciclo \(c \leq n\).

Esto nos permite calcular para cada ciclo:

\[
d \equiv e^{-1} \pmod{c}
\]

Aplicando \(p^e\) exactamente \(d\) veces a cada elemento de su ciclo recuperamos el paso original de \(p\):

\[
p(x) = (p^e)^d (x)
\]

De esta manera podemos reconstruir la permutación completa \(p\).

---

## 4. Proceso del exploit

1. Leemos `tales.txt` y extraemos `scrambled_message` y `enc_flag`.
2. Descomponemos `scrambled_message` en ciclos disjuntos.
3. Calculamos el inverso modular \(d\) para cada ciclo.
4. Reconstruimos la permutación original \(p\).
5. Calculamos la clave: `sha256(str(p).encode())`.
6. Desencriptamos la flag con **AES-ECB**.
7. Quitamos el padding y obtenemos la flag.

---

## 5. Script completo

```python
#!/usr/bin/env python3

import re
from hashlib import sha256
from Crypto.Util.number import inverse
from Crypto.Cipher import AES

# Ajusta si es necesario
n = 0x1337  # = 4919
e = 0x10001 # = 65537

def main():
    # 1) Leemos el archivo tales.txt
    with open("tales.txt", "r") as f:
        data = f.read()

    # 2) Extraemos scrambled_message y enc_flag con expresiones regulares
    #    tales.txt viene con lines como:
    #       scrambled_message = [57,  ... , 45]
    #       enc_flag = 'abcdef0123...'
    #
    #    Con la siguiente regex aislamos el contenido de la lista y la cadena:
    sm_re = re.search(r"scrambled_message\s*=\s*(\[.*?\])", data)
    ef_re = re.search(r"enc_flag\s*=\s*'([^']+)'", data)

    if not sm_re or not ef_re:
        print("No se pudo extraer scrambled_message o enc_flag de tales.txt")
        return

    sm_str = sm_re.group(1)  # La parte que contiene [57, 123, ...]
    enc_flag_hex = ef_re.group(1)

    # 3) Parseamos la lista scrambled_message con eval (rápido, aunque algo inseguro si no controlas la fuente).
    scrambled_message = eval(sm_str)

    # 4) Reconstruimos la permutación original p a partir de scrambled_message = p^e
    s = scrambled_message
    visited = [False] * n
    p = [None] * n

    for start in range(n):
        if not visited[start]:
            cycle = []
            current = start

            # Recorremos el ciclo
            while not visited[current]:
                visited[current] = True
                cycle.append(current)
                current = s[current]

            c = len(cycle)  # longitud de este ciclo

            # Calculamos d tal que (e * d) % c == 1
            d = inverse(e, c)

            # Para cada x en este ciclo, p(x) = s^d(x)
            for x in cycle:
                tmp = x
                for _ in range(d):
                    tmp = s[tmp]
                p[x] = tmp

    # 5) Calculamos la key
    key = sha256(str(p).encode()).digest()

    # 6) Desencriptamos enc_flag con AES-ECB
    cipher = AES.new(key, AES.MODE_ECB)
    enc_flag = bytes.fromhex(enc_flag_hex)
    flag_padded = cipher.decrypt(enc_flag)

    # 7) Quitamos el relleno PKCS#7
    pad_len = flag_padded[-1]
    flag = flag_padded[:-pad_len]

    print("Flag:", flag.decode(errors="replace"))

if __name__ == "__main__":
    main()
```

---
