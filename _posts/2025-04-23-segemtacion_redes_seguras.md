---
title: Diseño y segmentación de redes seguras
date: 2025-04-23 11:00:00 +0000
categories: [Redes]
tags: [IPV4, IPV6, IP, Segmentación]
image:
  path: /assets/img/posts/segmentacion_redes_seguras/cabecera.png
  alt:  cabecera
description: >
  Ejemplo de diseño y segmentación de redes seguras
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Segmentación de redes

Partimos desde una red o infraestructura corporativa que dividiremos en varias redes más pequeñas denominadas segmentos o subredes. Estas serán más fáciles de manejar y mantener.

Con esto conseguimos:

- Aumento del rendimiento y del número de dispositivos de red
- Mayor velocidad de transmisión al haber menos difusión
- Mejor gestión y control

### Direccionamiento IPV4

Para esto tenemos que tener claro los conceptos sobre las clases de direcciones IPV4.

- **Clase A**: Direcciones privadas de 127.0.0.0 a 127.255.255.255
- **Clase B**: Direcciones privadas de 192.168.0.0 a 192.168.255.255
- **Clase C**: Direcciones privadas de 10.0.0.0 a 10.255.255.255
- **Clase D**: Direcciones públicas de 0.0.0.0 a 255.255.255.255

![alt text](/assets/img/posts/segmentacion_redes_seguras/image.png)

**1. Clases de Direcciones IP:**
- **Clase A:** Rango 1 – 127. El 127 está reservado para pruebas internas (loopback). Su bit inicial es **0**.
- **Clase B:** Rango 128 – 191. Su bit inicial es **10**.
- **Clase C:** Rango 192 – 223. Su bit inicial es **110**.
- **Clase D:** Rango 224 – 239. Reservado para **multicast**.
- **Clase E:** Rango 240 – 255. Reservado para **investigación/experimental**.

**2. Espacio de Direcciones Privadas:**
- **Clase A:** 10.0.0.0 – 10.255.255.255
- **Clase B:** 172.16.0.0 – 172.31.255.255
- **Clase C:** 192.168.0.0 – 192.168.255.255

**3. Máscaras de Subred por Defecto:**
- **Clase A:** 255.0.0.0
- **Clase B:** 255.255.0.0
- **Clase C:** 255.255.255.0

### Subnetting - VLMS

**Subnetting** o **subredes** es una técnica usada para dividir una red grande en varias redes más pequeñas (**subredes**). Esto mejora la **organización**, **seguridad** y **eficiencia** del uso de direcciones IP.

- Una dirección IP tiene dos partes:  
  - **Identificador de red**
  - **Identificador de host (equipo)**
  
Cuando hacemos **subnetting**, **tomamos parte del identificador de host** y lo usamos para crear **subredes**. Entonces, dentro de cada subred, el resto de los bits sigue identificando a cada equipo.

#### **¿Qué es VLSM (Variable Length Subnet Mask)?**

La **VLSM** es una técnica más avanzada de subnetting que permite usar **máscaras de subred de longitud variable**.

🔹 En vez de hacer subredes de tamaño fijo, con VLSM podemos dividir la red en **porciones de distintos tamaños** según las necesidades, como si cortaras un **pastel en trozos desiguales**.

🔹 Esto se hace **"prestando bits"** al identificador del host para crear nuevas subredes con máscaras diferentes.  
Por ejemplo:  
- Una subred puede tener máscara /26 (para 64 direcciones)  
- Otra subred puede tener máscara /30 (para solo 4 direcciones)  

Esto es muy útil cuando algunas partes de la red requieren **más hosts** y otras **menos**.

#### **¿Por qué usar Subnetting y VLSM?**

✅ Uso más eficiente de direcciones IP  
✅ Mejora el rendimiento de la red  
✅ Facilita la seguridad y el control del tráfico  
✅ Permite un diseño de red más flexible

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-1.png)

1. **Número de subredes y hosts:**
   - **Subnets:** Se indican cantidades como 256, 128, 64, 32, etc., que representan el número posible de subredes según los bits prestados.
   - **Hosts:** Se muestran valores como 16, 8, 4, 2, que indican la cantidad de hosts por subred (calculados como \(2^n - 2\), donde \(n\) son los bits restantes).

2. **Dirección base y subredes:**
   - **192.10.10.0**: Es la dirección de red original.
   - **Ejemplos de subredes:**
     - **Subred (1):** 192.10.10.0 (máscara probable /28, rango de hosts: 192.10.10.1 a 192.10.10.15).
     - **Subred (2):** 192.10.10.16 (siguiente bloque, rango: 192.10.10.17 a 192.10.10.31).

3. **Notación binaria y rangos:**
   - Se usan valores binarios (como `0000`, `1110`, `1111`) para representar los bits de host/subred.
   - **Ejemplo:**
     - **Subred (5):** 192.10.10.224 (binario `1110`, rango: 192.10.10.225 a 192.10.10.239).
     - **Subred (16):** 192.10.10.240 (binario `1111`, rango: 192.10.10.241 a 192.10.10.255).

4. **Saltos entre subredes:**
   - El incremento entre subredes es de **16** en la dirección IP (ej: 192.10.10.0, 192.10.10.16, 192.10.10.32, ..., 192.10.10.240), lo que sugiere una máscara de subred **255.255.255.240** (/28).

La imagen muestra cómo una red **Clase C (192.10.10.0)** se divide en subredes más pequeñas usando 4 bits prestados del host (ej: /28).
- Cada subred tiene:
  - **16 direcciones IP** (14 hosts útiles, ya que se restan la dirección de red y broadcast).
  - **Rangos claros** (ej: 192.10.10.0-15, 192.10.10.16-31, etc.).
- Los valores binarios (como `0000`, `1111`) ayudan a visualizar los bits de la subred.

Esta información se puede obtener de dos formas:

**Fórmulas clave:**

1. **Número de subredes:**
   - **\( \text{Number of subnets} = 2^s \)**  
     (Donde \( s \) = bits prestados para subredes).  
     Ejemplo: Si se toman **5 bits**, hay \( 2^5 = 32 \) subredes posibles.  
   - **Alternativa (en entornos classful):**  
     \( 2^s - 2 \) (se excluyen la primera subred -"zero subnet"- y la última -"broadcast subnet"-).

2. **Hosts por subred:**  
   - **\( \text{Number of hosts} = 2^h - 2 \)**  
     (Donde \( h \) = bits restantes para hosts; se restan la dirección de red y broadcast).

**¿Cuándo usar cada fórmula para subredes?**

| **Usar \( 2^s - 2 \) (excluir subredes zero/broadcast)** | **Usar \( 2^s \) (incluir todas las subredes)**      |
|----------------------------------------------------------|------------------------------------------------------|
| Entornos **classful** (ej: RIP v1)                       | Entornos **classless** (ej: RIPv2, EIGRP, OSPF)      |
| Comando `no ip subnet zero` en routers                   | Comando `ip subnet zero` (configuración por defecto) |
| Máscaras fijas por clase (A, B, C)                       | Soporta VLSM (máscaras variables)                    |
|                                                          | Si no hay pistas adicionales, se asume classless.    |

**Diferencias clave entre classful y classless:**

- **Classful routing (ej: RIP v1):**  

  - No envía información de máscara en las actualizaciones de red.  
  - Asume que todas las subredes tienen la misma máscara.  
  - Excluye las subredes "zero" (ej: 192.168.1.0) y "broadcast" (ej: 192.168.1.255).  

- **Classless routing (ej: RIPv2, EIGRP, OSPF):**  

  - Permite máscaras variables (VLSM).  
  - Incluye todas las subredes (zero y broadcast).  
  - Es el estándar moderno.

### Ejemplo práctico subnetting

La fórmula para saber cuántas direcciones tiene una subred es:  
**2^(32 - CIDR)** (donde CIDR es el número después de la barra, por ejemplo `/28`)

De esas direcciones:
- La **primera** es la dirección de **subred**
- La **última** es la dirección de **broadcast**
- Las del medio son direcciones de **host válidas**

#### a) 192.168.100.25/30

- **/30** → Máscara: **255.255.255.252**
- Esto da **2^(32-30) = 4** direcciones por subred
- Los bloques (subredes) en este rango serían:  
  192.168.100.0, 192.168.100.4, 192.168.100.8, 192.168.100.12, ...

**192.168.100.25** cae en la subred **192.168.100.24**

- **Subred**: 192.168.100.24  
- **Broadcast**: 192.168.100.27  
- **Rango de hosts válidos**: 192.168.100.25 – 192.168.100.26

#### b) 192.168.100.37/28

- **/28** → Máscara: **255.255.255.240**
- Esto da **2^(32-28) = 16** direcciones por subred
- Los bloques (subredes) en este rango serían:  
  192.168.100.0, 192.168.100.16, 192.168.100.32, 192.168.100.48, ...

**192.168.100.37** cae en la subred **192.168.100.32**

- **Subred**: 192.168.100.32  
- **Broadcast**: 192.168.100.47 (es la última del bloque de 16)  
- **Rango de hosts válidos**: 192.168.100.33 – 192.168.100.46

#### c) 192.168.100.66/27

- **/27** → Máscara: **255.255.255.224**
- Esto da **2^(32-27) = 32** direcciones por subred
- Los bloques serían:  
  192.168.100.0, 192.168.100.32, 192.168.100.64, 192.168.100.96, ...

**192.168.100.66** cae en la subred **192.168.100.64**

- **Subred**: 192.168.100.64  
- **Broadcast**: 192.168.100.95  
- **Rango de hosts válidos**: 192.168.100.65 – 192.168.100.94

### Ejemplo de cálculo

| Dirección IP           | Clase  | Nº de bits de subred   | Nº de bits de hosts   | Nº de subredes (2^subred)   | Nº de hosts válidos (2^host - 2) |
|------------------------|--------|------------------------|-----------------------|-----------------------------|----------------------------------|
| 10.25.66.154/23        | A      | 15 (23-8)              | 9                     | 32,768                      | 510                              |
| 172.31.254.12/24       | B      | 8 (24-16)              | 8                     | 256                         | 254                              |
| 192.168.20.123/28      | C      | 4 (28-24)              | 4                     | 16                          | 14                               |
| 63.24.89.21/18         | A      | 10 (18-8)              | 14                    | 1024                        | 16,382                           |
| 128.1.1.254/20         | B      | 4 (20-16)              | 12                    | 16                          | 4,094                            |
| 208.100.54.209/30      | C      | 6 (30-24)              | 2                     | 64                          | 2                                |

1. **Clase**: Se basa en el primer octeto:
   - Clase A: 1–126
   - Clase B: 128–191
   - Clase C: 192–223

2. **Bits de subred** = CIDR – bits de red por clase  
   (A: 8 bits, B: 16 bits, C: 24 bits)

3. **Bits de host** = 32 – CIDR

4. **Subredes** = 2^bits de subred  
   **Hosts válidos** = 2^bits de host – 2 (se restan dirección de red y broadcast)

#### Ejercicios de ejemplo: 

##### 1. Usando la siguiente imagen, ¿cuál debería de ser la dirección IP de E0 si quisiéramos usar la octava subred?. El ID de red es 192.168.10.0/28 y necesitamos usar la última dirección ip disponible del rango.

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-2.png)

**Paso 1: Entender la máscara /28**

- Una máscara **/28** significa que los primeros 28 bits son para la red y los últimos 4 bits para hosts.
- **Máscara de subred:** 255.255.255.240.
- **Bloque de direcciones por subred:** \( 2^4 = 16 \) direcciones (14 hosts útiles, ya que se excluyen la dirección de red y broadcast).

**Paso 2: Calcular las subredes**

El incremento entre subredes es de **16** en el último octeto. Las subredes son:
1. 192.168.10.0   (Rango: 192.168.10.1 - 192.168.10.15)
2. 192.168.10.16  (Rango: 192.168.10.17 - 192.168.10.31)
3. 192.168.10.32  (Rango: 192.168.10.33 - 192.168.10.47)
4. 192.168.10.48  (Rango: 192.168.10.49 - 192.168.10.63)
5. 192.168.10.64  (Rango: 192.168.10.65 - 192.168.10.79)
6. 192.168.10.80  (Rango: 192.168.10.81 - 192.168.10.95)
7. 192.168.10.96  (Rango: 192.168.10.97 - 192.168.10.111)
8. **192.168.10.112** (Rango: 192.168.10.113 - 192.168.10.127) ← **Octava subred**

**Paso 3: Identificar la última dirección IP disponible**

En la octava subred (192.168.10.112/28):
- **Dirección de red:** 192.168.10.112 (reservada).
- **Primera dirección usable:** 192.168.10.113.
- **Última dirección usable:** 192.168.10.126 (la dirección 192.168.10.127 es el broadcast).
- **Broadcast:** 192.168.10.127.

**Paso 4: Seleccionar la respuesta correcta**

La última dirección IP disponible en la octava subred es **192.168.10.126**.

**Respuesta correcta:** 192.168.10.126

##### 2. Usando la imagen de la pregunta anterior, ¿cuál debería de ser la dirección IP de S0 si quisiéramos utilizar la segunda subred? El ID de la red es 192.168.10.16/28 y necesitamos utilizar la última dirección disponible en el rango.

Usando la misma lógica que en anterior tenemos que la segunda subred es la 192.168.10.16/28 con rango de direcciones 192.168.10.17 a 192.168.10.31, por lo que la última dirección disponible es **192.168.10.30**.

##### 3. En la red mostrada en el siguiente diagrama, ¿Cuántos hosts pueden haber en la subred B?

![alt text](image-3.png)

Una máscara **/28** significa que los primeros 28 bits son para la red y los últimos 4 bits para hosts.
**Bloque de direcciones por subred:** \( 2^4 = 16 \) direcciones (14 hosts útiles, ya que se excluyen la dirección de red y broadcast).

La subred B puede tener hasta 14 hosts.

##### 4. En el diagrama siguiente, para tener un direccionamiento IP lo más eficiente posible, ¿qué red debería de utilizar una máscara /29?

![alt text](image-4.png)

Para determinar qué red debe usar una máscara **/29** (que permite **6 hosts útiles** por subred), analizaremos los requisitos de hosts de cada red en el diagrama y compararemos con las opciones proporcionadas.

**Datos**

- **Máscara /29:**  
  - **Hosts posibles:** \(2^3 - 2 = 6\) (3 bits para hosts, se restan dirección de red y broadcast). 

- **Redes y sus requisitos de hosts:**  

  - **Network A:** 14 hosts (requiere máscara **/28**, que permite 14 hosts).  
  - **Network B:** 30 hosts (requiere máscara **/27** o mayor, ya que \(2^5 - 2 = 30\)).  
  - **Network C:** 20 hosts (requiere máscara **/27**, que permite 30 hosts).  
  - **Network D:** 6 hosts (coincide exactamente con la capacidad de una máscara **/29**).  
  - **Networks F, G, H:** 2 hosts cada una (requieren máscara **/30**, que permite 2 hosts).  

- **Network D necesita 6 hosts**, y una máscara **/29** proporciona exactamente 6 hosts útiles.  
- Usar una máscara más grande (ej: /28) desperdiciaría direcciones (14 hosts asignados para solo 6 necesarios).  
- Usar una máscara más pequeña (ej: /30) no cumpliría con el requisito (solo 2 hosts).  

##### 5. En el siguiente diagrama, ¿cuál es la razón principal por la que el host no puede hacer un ping hacia el exterior?

![alt text](image-5.png)

**Datos proporcionados:**

- **RouterA:**
  - **Interfaz E0:** 192.168.10.33/27
- **Host:**
  - **Dirección IP:** 192.168.10.28/27
  - **Gateway predeterminado:** 192.168.10.33/27


**Verificar el rango de la subred**

La máscara **/27** divide el espacio de direcciones en subredes de 32 direcciones cada una (30 hosts útiles).  
- **Dirección de red:** 192.168.10.0/27  
- **Rango de hosts:** 192.168.10.1 - 192.168.10.30  
- **Dirección de broadcast:** 192.168.10.31  

**Observación:**  
- La IP del host (192.168.10.28) está dentro del rango válido.  
- La IP del router (192.168.10.33) **no pertenece a esta subred**, ya que está en la siguiente subred (192.168.10.32/27).  


El problema es que el **gateway predeterminado (192.168.10.33)** no está en la misma subred que el host (192.168.10.28/27). El host no puede alcanzar el gateway, lo que impide el ping hacia el exterior.

##### 6. ¿Cuál de las redes del siguiente diagrama puede usar una máscara /29?

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-6.png)

**Máscara /29:**

- **Bits para hosts:** 3 (ya que /29 deja 3 bits para hosts en una IPv4).  
- **Hosts útiles:** \(2^3 - 2 = 6\) (se restan la dirección de red y broadcast).  
- **Rango de direcciones:** 8 direcciones por subred (6 utilizables).  

**Requisitos de cada red:**

1. **Corporate:** 7 usuarios → **Necesita al menos 7 hosts útiles**.  
   - **/29 no es suficiente** (solo permite 6 hosts).  
   - Requiere máscara **/28** (14 hosts).  

2. **L.A.:** 15 usuarios → **Necesita al menos 15 hosts útiles**.  
   - **/29 no es suficiente**.  
   - Requiere máscara **/27** (30 hosts).  

3. **S.F.:** 13 usuarios → **Necesita al menos 13 hosts útiles**.  
   - **/29 no es suficiente**.  
   - Requiere máscara **/28** (14 hosts).  

4. **N.Y.:** 7 usuarios → **Necesita al menos 7 hosts útiles**.  
   - **/29 no es suficiente** (igual que Corporate).  
   - Requiere máscara **/28** (14 hosts).  

5. **Wy.:** 16 usuarios → **Necesita al menos 16 hosts útiles**.  
   - **/29 no es suficiente**.  
   - Requiere máscara **/27** (30 hosts).  

**Conclusión:**
- **Ninguna** de las redes puede usar una máscara **/29**, ya que todas requieren más hosts de los que esta máscara permite (6 hosts útiles).  
- Las redes con 7, 13, 15 o 16 usuarios necesitan máscaras más grandes (/28 o /27).  

##### 7. Diseño de una red corporativa.

La labor que nos han encomendado es optimizar lo máximo posible y securizar la red informática de toda la empresa, pero manteniendo en la medida de lo posible el direccionamiento usado.
Nuestro punto de partida es una red de clase C con direccionamiento 192.168.3.0/24 en la que todos los departamentos tienen direcciones ips de esa red sin ningún tipo de agrupación y los dispositivos de red como switches tienen una configuración plana sin vlans aunque soportan dicha funcionalidad.
La conexión de internet está suministrada mediante un router configurado en modo bridge y un firewall pfsense que se encarga de proporcionar todos los servicios de red necesarios (dns,dhcp, …)

La empresa realizó una clasificación de departamentos y obtuvo el siguiente listado que debemos de usar a la hora de crear nuestras agrupaciones mediante VLANs.

| Departamento   | Nº hosts |
|----------------|----------|
| Comercial      | 5        |
| Administrativo | 6        |
| I+D            | 12       |
| Desarrollo     | 28       |
| Wifi_Corp      | 60       |
| Wifi_Inv       | 25       |
| DMZ            | 28       |
| Red Gestión    | 18       |
| Voz IP         | 30       |

La empresa ha hecho especial hincapié en que en la red I+D no se debe de permitir conectar ningún dispositivo aparte de los ordenadores que ya están conectados, para ello, se ha elaborado un listado con las direcciones mac de los dispositivos.

| Listado de direcciones MAC |
|----------------------------|
|     2A:1D:DC:70:EE:01      |
|     2A:1D:DC:70:EE:02      |
|     2A:1D:DC:70:EE:03      |
|     2A:1D:DC:70:EE:04      |
|     2A:1D:DC:70:EE:05      |
|     2A:1D:DC:70:EE:06      |
|     2A:1D:DC:70:EE:07      |
|     2A:1D:DC:70:EE:08      |
|     2A:1D:DC:70:EE:09      |
|     2A:1D:DC:70:EE:10      |
|     2A:1D:DC:70:EE:11      |
|     2A:1D:DC:70:EE:12      |

Además, tenemos el siguiente listado de los servidores de la empresa con los servicios asociados.

| Nombre de servidor    | IP            | Tipo de servicio      | Puerto     |
|-----------------------|---------------|-----------------------|------------|
| Servidor web          | 192.168.3.98  | http, https y ssh     | 80, 443    |
| Servidor Correo       | 192.168.3.99  | pop, imap, smtp y ssh | 110,143,25 |
| Servidor Contabilidad | 192.168.3.100   | https y RDP           |            |
| Servidor FTP          | 192.168.3.101   | ftp y ssh             | 20, 21     |
| Servidor NAS          | 192.168.3.102   | samba, nfs y ssh      |            |

Para finalizar, se nos ha proporcionado un plano con la ubicación de los switches y departamentos de la empresa, de esta forma podremos sacar un mapa lógico de red.

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-7.png)

a) Cuál es la la IP del PC2 de la red Comercial con su máscara de red.
b) Cuál es la dirección de broadcast de la red Comercial con su máscara de red.
c) Cuál es la la IP del PC28 de la red Desarrollo con su máscara de red.
d) Cuál es la la IP del PC16 de la red Gestión con su máscara de red.

Primero debemos diseñar un esquema de subredes (VLANs) basado en los requisitos de la empresa. Utilizaremos la red **192.168.3.0/24** y asignaremos rangos de direcciones IP a cada departamento según el número de hosts requeridos.

**Diseño de VLANs y Subredes**

| **Departamento**   | **Nº Hosts** | **Máscara** | **Subred**          | **Rango de IPs**               | **Broadcast**       |
|--------------------|--------------|-------------|---------------------|--------------------------------|---------------------|
| Comercial          | 5            | /28         | 192.168.3.0/28      | 192.168.3.1 - 192.168.3.14     | 192.168.3.15        |
| Administrativo     | 6            | /28         | 192.168.3.16/28     | 192.168.3.17 - 192.168.3.30    | 192.168.3.31        |
| I+D                | 12           | /27         | 192.168.3.32/27     | 192.168.3.33 - 192.168.3.62    | 192.168.3.63        |
| Desarrollo         | 28           | /26         | 192.168.3.64/26     | 192.168.3.65 - 192.168.3.126   | 192.168.3.127       |
| Wifi_Corp          | 60           | /25         | 192.168.3.128/25    | 192.168.3.129 - 192.168.3.254  | 192.168.3.255       |
| Wifi_Inv           | 25           | /26         | 192.168.3.192/26    | 192.168.3.193 - 192.168.3.254  | 192.168.3.255       |
| DMZ                | 28           | /26         | 192.168.3.0/26      | 192.168.3.1 - 192.168.3.62     | 192.168.3.63        |
| Red Gestión        | 18           | /27         | 192.168.3.224/27    | 192.168.3.225 - 192.168.3.254  | 192.168.3.255       |
| Voz IP             | 30           | /26         | 192.168.3.64/26     | 192.168.3.65 - 192.168.3.126   | 192.168.3.127       |

**a) IP del PC2 de la red Comercial con su máscara de red**

- **Subred Comercial:** 192.168.3.0/28  
- **Rango de IPs:** 192.168.3.1 - 192.168.3.14  
- **PC2:** 192.168.3.2  
- **Máscara:** 255.255.255.240 (/28)  

**IP del PC2:** `192.168.3.2/28`  

**b) Dirección de broadcast de la red Comercial con su máscara de red**

- **Subred Comercial:** 192.168.3.0/28  
- **Broadcast:** 192.168.3.15  

**Broadcast:** `192.168.3.15/28`  

**c) IP del PC28 de la red Desarrollo con su máscara de red**

- **Subred Desarrollo:** 192.168.3.64/26  
- **Rango de IPs:** 192.168.3.65 - 192.168.3.126  
- **PC28:** 192.168.3.92 (65 + 27 = 92)  
- **Máscara:** 255.255.255.192 (/26)  

**IP del PC28:** `192.168.3.92/26`  

**d) IP del PC16 de la red Gestión con su máscara de red**

- **Subred Gestión:** 192.168.3.224/27  
- **Rango de IPs:** 192.168.3.225 - 192.168.3.254  
- **PC16:** 192.168.3.240 (225 + 15 = 240)  
- **Máscara:** 255.255.255.224 (/27)  

**IP del PC16:** `192.168.3.240/27`  


## Redes virtuales VLAN

VLAN = Virtual Local Area Network
Es una red lógica que agrupa dispositivos, aunque no estén conectados al mismo switch físico.

Nos permite:

- Separar el tráfico de red sin necesidad de hardware adicional

- Aumentar la seguridad (cada VLAN es como una red independiente)

- Mejorar el rendimiento (menos colisiones de datos)

- Facilitar la gestión de red (por ejemplo, agrupar por departamentos)

Gracias a las VLANs podemos mitigar problemas de seguridad como:

- Reducción de packet-sniffing, capturan tráfico a nivel de trama Ethernet para captar información de personal autorizado.

- Acceso a servidores y servicios único y exclusivamente a personal autorizado.

### Cómo se implementan las VLANs

En los switches la segmentación se realiza a través de los puertos, asignándolos a VLANs. Estos puertos no tienen una funcionalidad alguna hasta que un dispositivo cuente con los permisos para acceder a él.

- Para usar VLANs en nuestra red, usaremos switches que soporten el protocolo **IEEE802.1Q** o también llamados **Q-Switches**. Si usamos switches básicos basados en el protocolo **IEEE802.1D** todos los dispositivos conectados se verán entre ellos **D-Switches**.
- Cuando un dispositivo quiere comunicarse con otro necesitara conocer la dirección MAC del destino, para ello usara el protocolo ARP.
- Cuando un **D-Switch** recibe una petición ARP, enviará el paquete a todos los puertos del switch excepto por el que lo ha recibido.
- Un **Q-Switch** determinará primero la VLAN a la que pertenece el paquete y luego lo enviará por los puertos de esa VLAN.

#### Enlace de acceso (Access ports)

- Permite el tráfico a una sola VLAN, el tráfico es recibido y enviado en un formato nativo sin información de VLAN (tagging). Sin etiquetar porque sólo circula una VLAN (PC1, PC2, PC3).
- Cualquier cosa que llegue a un puerto se considera que pertenece a esa VLAN.
- Conexión con dispositivos finales.

#### Enlace troncal (Trunk ports)

- Es un link punto a punto entre dos switches, entre un switch y un router o incluso entre un switch y otro dispositivo que se comunican entre ellos pasándose el tráfico de múltiples VLANs al mismo tiempo.
- Tráfico de múltiples VLAN
- Conexión entre switches o de un switch con la capa superior

#### Voice Access ports

- Tipo especial de puerto en modo Access, en este caso le decimos al switch que puede pasar
tráfico de una segunda vlan que será la vlan asignada para telefonía

### Rango de VLANs en switches

- Rango normal VLAN

  - Redes pequeñas y medianas
  - VLAN ID:1-1005
  - 1002-1005 reservadas
  - Se guardan en vlan.dat (memoria flash)

- Rango extendido VLAN

  - Proveedores de servicio y empresas globales
  - VLAN ID:1006-4094
  - Se guardan el archivo de configuración

### Clasificación de VLANs

#### VLAN de nivel 1 (por puertos)

Se especifica qué puertos del switch pertenecen a la VLAN. Los miembros de dicha VLAN son los que se conectan a esos puertos.

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-8.png)

#### VLAN de nivel 2 (por direcciones MAC)

Se asignan hosts a una VLAN en función de su dirección MAC.

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-9.png)

#### VLAN de nivel 3 (por tipo de protocolo)

La VLAN queda predeterminada por el contenido del campo "tipo de protocolo" detectado en el paquete (IPV4, AppleTalk, IPX, etc.).

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-10.png)

#### VLAN de nivel 4 (por direcciones de subred)

La cabecera de nivel 3 en el modelo OSI se utiliza para mapear la VLAN a la que pertenece.

![alt text](/assets/img/posts/segmentacion_redes_seguras/image-11.png)

### Routing entre VLANs

Las VLANs no se comunican entre sí por sí solas, porque están en redes lógicas separadas.
Si un dispositivo en la VLAN 10 quiere hablar con uno en la VLAN 20, necesitamos un enrutador o un switch de Capa 3.

Esto se llama "routing entre VLANs".

Se necesita:

- Un router tradicional
    (en un escenario antiguo o simple)

- Un switch de Capa 3
    (más moderno y eficiente; puede hacer routing interno)

- Subinterfaces o SVI (Switch Virtual Interfaces)

        Si usas un router → se crean subinterfaces en el puerto troncal

        Si usas switch Capa 3 → se crean SVI, una por cada VLAN

