---
title: "Traces - Cyber Apocalypse 2025"
layout: post
permalink: /writeups/cyberapocalypse2025/traces
categories: [HacktheBox, CTF]
tags: [CyberApocalypse, HTB, Crypto]
description: >
  Explotación de vulnerabilidad de reutilización de keystream en AES-CTR en el reto Traces de Cyber Apocalypse 2025.
pin: false
toc: true
math: false
mermaid: false
---

## Introducción

El reto consistía en explotar una vulnerabilidad de **reutilización de clave y nonce en AES-CTR**, combinado con el uso de mensajes con prefijos conocidos (`!nick <nickname>`), lo que nos permitió aplicar la técnica clásica de **crib dragging** para obtener los mensajes originales y la flag.

---

## Análisis del servicio

El servidor simula un pequeño sistema de chat IRC donde:

- Cada usuario envía su primer mensaje de la forma `!nick <nickname>`.
- Las conversaciones se cifran con **AES-256 en modo CTR**.
- El servicio reutiliza el mismo **keystream** para todos los mensajes.

Dado que:

\[\text{C} = \text{P} \oplus K\]

Si obtenemos dos mensajes cifrados \(C_0\) y \(C_1\) de dos mensajes originales \(P_0\) y \(P_1\) cifrados con el mismo keystream \(K\):

\[C_0 \oplus C_1 = P_0 \oplus P_1\]

Esto nos permite obtener la XOR directa entre los textos planos.

---

## Explotación - General Channel

Al conectarnos al canal `#general` observamos múltiples mensajes cifrados.

Sabemos que cada mensaje comienza con `!nick <nickname>`, por tanto, aplicando crib-dragging:

1. Suponemos que el mensaje de `Runeblight` es `!nick Runeblight`.
2. Calculamos el keystream parcial.
3. Recuperamos automáticamente otros mensajes como:

```
!nick Doomfang
!nick Stormbane
... (conversación) ...
Here is the passphrase for our secure channel: %mi2gvHHCV5f_kcb=
```

Obtuvimos la contraseña para el canal secreto: `%mi2gvHHCV5f_kcb=`

---

## Explotación - Secret Channel

Repetimos la misma estrategia dentro del canal `#secret`.

Aplicamos **crib-dragging** de nuevo para ir recuperando los mensajes hasta encontrar en claro la flag:

```
It is labeled as: HTB{Crib_Dragging_Saves_The_Day}
```

---

## Técnica empleada

| Técnica | Descripción |
|---------|-------------|
| Reutilización de keystream | Mismo keystream utilizado para cifrar múltiples mensajes |
| Crib dragging | Aprovechar conocimiento parcial del mensaje para descifrar XORs |
| AES-CTR | Modo de cifrado vulnerable a este ataque si se reutiliza el nonce |

---

## Nota final

El reto es un ejemplo clásico de por qué **no se debe reutilizar nonce y clave** en AES-CTR. Basta una pequeña pista conocida para desmoronar por completo la seguridad del sistema.

El script utilizado permite interactuar de forma dinámica con los ciphertexts aplicando crib-dragging hasta revelar todos los mensajes y obtener la flag.

---

## Script completo

```python
#Genreal Channel
import binascii
from pwn import xor
from collections import defaultdict

# =============================================
# ConfiguraciÃƒÂ³n inicial con los mensajes reales
# =============================================

ciphertexts = [
    "598f7a3368a4c9537fd7a22da9a0",
    "598f7a3368a4de487fc8a92ea6a981",
    "598f7a3368a4df497edfa620aea08ccc",
    "2f84342666a4ea53649aa56ca9a293982220b07aafefd36af60c986090e5a44727e70cb55432baa9328796c82a19cb8a102da1007f384b7002160377320f84c6d790",
    "2d8f773571f7f9537fdeea6c8fa697982221a528abadde7ae742cc699bbcf6512ce50ee61574d6b82ec588c83319c9885f37a41b313c03621f5810607b1690c092d2a354bdfe56f75b2efe",
    "368e67707ae1f91030d8b138e78ec3d5762aa83fade6d571e50c9f6798a0f6572bf713b31b7ed6bf2fc78b892d0f80da7924f406373e5a3105531d763e5990c19e9eb542e9b352ff453fe11d9c26a0d0b25747462e10ab238acfbf4b1ce02ca0e55fe0580d0a",
    "2c897a2323e7e55d7ed4a120e7ae97983826b47abdecda7aa24a837ad5a9b94c22a214a7167985e266ec809c660f8e89472ba011377b577e565906777b0997dbc4dfb642e9ac54f74065",
    "3084613523edfe1c64d2a16cb7a697cb2621b23bbde89c79ed5ecc6780b7f65120e115b41f3295a427ce8b8d2d468edf5d2be61529136b522003155a301a878fe88ab47285af54c1676dae27",
    "3f8e67706af0a31c5fd4a835e7b48cd9242ce033baadcb76f644cc6780b7f64f2af114e60e6083bf32c581c82010c2935531fa",
    "2184607e23cbf84e30d6a53fb3e789d7202ce037aff49c77e35a892899a0b05665f612a7197785e266f780c82c09dd8e1020b152293e5168565512773e1f90de9c",
    "31c67e7060ece85f7bd3aa2be7a891ca7625af3dbdadc870a24e892886b0a44765ec0fe60e6097af23808a8e6113db881023b70636344d62564416683a108bc19c",
    "3384762023e9e81c65caa02db3a280967600a67abae5d966a24f8d7c96adf64d2bae40b11f359aa066c8849e245cda951023b7067f3d42620218",
    "31c67f3c23e7e25160dbb629e7b38cdd7625a12eabfec83fe64d9869d5b2bf562da20fb3083294ad25cb9098610cc29b5e6cf4253a7b4e6405425360291896d792dfac5ee9ad52ff436bb610dd27a082a3180f403414eb",
    "3187333575e1ff4564d2ad22a0e78dcb762aac3fafff903ff549cc659ab3b30231ed40b21277d6a223d891c83208cf9d556cf43d2a29037619571f25320ac5c5dbcaaa4ea7fe49fd4c28a95b",
    "308e7f3423ebe31230f3e321e7b481dd3f27a77abdf9ce7eec4b892886acb14c24ee13e61c6099a166cf909c3215ca9f1e6283177f364a761e4253673e5992d3c6ddaa42adf0",
    "2f84333362eaaa4830cea527a2e785d62f69b233bde6cf31a260897cd2b6f64e20e316a35a669ea5358086802012c09f5c62b6173934517456421b60225991c0d3dda907bcad15",
    "3986613566e0a31c5dd5b229e7a688d4763da136a5fe9c6bed0c986090e5a6502cf401b21f3284a329cdcbc81309c09f522ebd15372f0f31065a1664281cc5d1dedba355e9aa53fd0d27ae128e70ad95b45d49",
    "2d8f773571f7f9537fdeea6c8ee089983220b339a1e3d27ae158856692e5b84d32ac408f1c3282a423d9c580200acbda4327b11c7f2e503d56411625360c96c692daab54a8ae4bfd4c39e11c903da094af5913402a08eb",
    "598d763175e1",
    "598d763175e1",
    "598d763175e1"
]

# Pares conocidos (basados en los ÃƒÂºltimos mensajes idÃƒÂ©nticos)
known_pairs = [
    ("598d763175e1", b"!leave")  # Los 3 ÃƒÂºltimos mensajes son idÃƒÂ©nticos y probablemente son !leave
]

# =============================================
# ReconstrucciÃƒÂ³n inteligente del Keystream
# =============================================

class KeystreamManager:
    def __init__(self):
        self.keystream = bytearray()
        self.known_positions = set()
    
    def add_known_pair(self, ct_hex, plaintext):
        """AÃƒÂ±ade un par conocido (cifrado, texto plano) al keystream"""
        ct = binascii.unhexlify(ct_hex)
        if len(ct) > len(self.keystream):
            # Extender el keystream con bytes nulos si es necesario
            self.keystream.extend(b'\x00' * (len(ct) - len(self.keystream)))
        
        # Calcular la porciÃƒÂ³n del keystream
        new_ks = xor(ct, plaintext)
        
        # Actualizar el keystream y marcar posiciones conocidas
        for i in range(len(new_ks)):
            if i < len(plaintext):  # Solo para las posiciones donde tenemos texto plano
                self.keystream[i] = new_ks[i]
                self.known_positions.add(i)
    
    def add_crib(self, ct_hex, crib, offset):
        """AÃƒÂ±ade un crib (texto supuesto) al keystream"""
        ct = binascii.unhexlify(ct_hex)
        if offset + len(crib) > len(ct):
            print(f"Error: Crib demasiado largo (offset {offset}, len {len(crib)}, ciphertext len {len(ct)})")
            return
        
        # Calcular la porciÃƒÂ³n del keystream
        new_ks = xor(ct[offset:offset+len(crib)], crib)
        
        # Extender el keystream si es necesario
        if len(self.keystream) < offset + len(new_ks):
            self.keystream.extend(b'\x00' * (offset + len(new_ks) - len(self.keystream)))
        
        # Actualizar el keystream
        for i in range(len(new_ks)):
            self.keystream[offset + i] = new_ks[i]
            self.known_positions.add(offset + i)
    
    def decrypt(self, ct_hex):
        """Descifra un mensaje usando el keystream actual"""
        ct = binascii.unhexlify(ct_hex)
        decrypted = bytearray()
        
        for i in range(len(ct)):
            if i < len(self.keystream) and i in self.known_positions:
                decrypted.append(ct[i] ^ self.keystream[i])
            else:
                decrypted.append(0x3F)  # '?' para bytes desconocidos
        
        try:
            return decrypted.decode('utf-8', errors='replace')
        except:
            return str(decrypted)
    
    def find_repetitions(self):
        """Busca repeticiones en el keystream para identificar patrones"""
        repetitions = defaultdict(list)
        for i, byte in enumerate(self.keystream):
            if byte != 0:  # Ignorar bytes no descubiertos
                repetitions[byte].append(i)
        return {k: v for k, v in repetitions.items() if len(v) > 1}

# =============================================
# AnÃƒÂ¡lisis inicial
# =============================================

ks_manager = KeystreamManager()

# 1. AÃƒÂ±adir pares conocidos
for ct, pt in known_pairs:
    ks_manager.add_known_pair(ct, pt)

# 2. Analizar los primeros mensajes (probablemente comandos !nick)
ks_manager.add_crib("598f7a3368a4c9537fd7a22da9a0", b"!nick Doomfang", 0)
ks_manager.add_crib("598f7a3368a4de487fc8a92ea6a981", b"!nick Stormbane", 0)
ks_manager.add_crib("598f7a3368a4df497edfa620aea08ccc", b"!nick Runeblight", 0)
# =============================================
# VisualizaciÃƒÂ³n mejorada de mensajes
# =============================================

def print_full_messages():
    print("\n=== MENSAJES COMPLETOS ===")
    print("(Los caracteres desconocidos se muestran como ?)\n")
    
    for idx, ct_hex in enumerate(ciphertexts):
        decrypted = ks_manager.decrypt(ct_hex)
        ct_length = len(binascii.unhexlify(ct_hex))
        known_bytes = sum(1 for i in range(ct_length) if i in ks_manager.known_positions)
        
        print(f"\n=== Mensaje {idx} ({known_bytes}/{ct_length} bytes conocidos) ===")
        print(f"Hex: {ct_hex[:12]}...{ct_hex[-12:]}")
        print("Texto completo:")
        print(decrypted)
        print("-" * 80)

# =============================================
# Descifrado interactivo mejorado
# =============================================

def interactive_decryption():
    print("\n=== DESCIFRADO INTERACTIVO MEJORADO ===")
    print("Instrucciones:")
    print("1. Revisa los mensajes completos mostrados")
    print("2. Cuando identifiques un fragmento legible, ingresa:")
    print("   - NÃƒÂºmero de mensaje")
    print("   - Offset donde comienza el texto conocido")
    print("   - El texto supuesto (crib)")
    print("3. Escribe 'quit' para salir\n")
    
    while True:
        print_full_messages()
        
        user_input = input("\nIngresa (mensaje offset crib) o 'quit': ").strip()
        if user_input.lower() == 'quit':
            break
        
        try:
            parts = user_input.split()
            msg_idx = int(parts[0])
            offset = int(parts[1])
            crib = ' '.join(parts[2:]).encode()
            
            if msg_idx < 0 or msg_idx >= len(ciphertexts):
                print("Error: ÃƒÂndice de mensaje invÃƒÂ¡lido")
                continue
            
            ks_manager.add_crib(ciphertexts[msg_idx], crib, offset)
            print(f"\nCrib aÃƒÂ±adido: mensaje {msg_idx}, offset {offset}, texto '{crib.decode()}'")
        except Exception as e:
            print(f"\nError: {e}. Formato esperado: 'mensaje offset texto'")

# =============================================
# EjecuciÃƒÂ³n principal
# =============================================

if __name__ == "__main__":
    # Mostrar estado inicial del keystream
    print("\n=== ESTADO INICIAL DEL KEYSTREAM ===")
    print(f"Longitud actual: {len(ks_manager.keystream)} bytes")
    print(f"Bytes conocidos: {len(ks_manager.known_positions)}")
    
    # Iniciar el modo interactivo
    interactive_decryption()
    
    # Mostrar estado final del keystream
    print("\n=== ESTADO FINAL DEL KEYSTREAM ===")
    print(f"Longitud: {len(ks_manager.keystream)} bytes")
    print(f"Bytes conocidos: {len(ks_manager.known_positions)}")
    print(f"Porcentaje conocido: {len(ks_manager.known_positions)/len(ks_manager.keystream)*100:.2f}%")
```

```python
#Secret Channel
import binascii
from pwn import xor
from collections import defaultdict

# =============================================
# ConfiguraciÃƒÂ³n inicial con los mensajes reales
# =============================================

ciphertexts = [
    "598f7a3368a4c9537fd7a22da9a0",
    "598f7a3368a4de487fc8a92ea6a981",
    "598f7a3368a4df497edfa620aea08ccc",
    "2f8433236bebf850749aaf29a2b7c4d7233be02aa2ecd271eb428b289da0a4476ba234ae1f3299b932c597c8291dc2964362b5003a7b4d7e02160060380c97d79e9ea349adfe4ff7426bac149329e595bf5d14053110b12787cfa4560be037b1e345a9581645d777e81667d5",
    "3986613566e0a31c44d2a16ca2a981d52f6eb37abdeed36af65fcc6f87aaa10228ed12a35a6293be35c9969c2412dad4100bb2522b334668565512713811c5d7c4dbac07a8fe4cf04438b1108f70aa96e65712576615a0378688be4d42e02ca9e352a94c1748d539e015629ebe2200036550263abe6bb38a150562ad27d15eb3acd6072373d69a0d713cd6f8fdf66f50023010449e2732cb7debd036ed1843b76b358dbb504cbb0eb94e721aaa279dd18f9fb1",
    "31c6653523e6e8597e9ab738b2a39dd1382ee02ea6e89c6bf04d8f6d86e5ba4723f640a41f7a9fa2228087916113db881032a61729324c6405161a6b38188bc6d3caab48a7ad17b84c25a5558e3fa895b2500e4b2151a3218a83a31e19b237afe105a9740b569977e80e6394ec28470d6a1e263efb72acd7153a66fe6ad748a9f898072227978508792597e0e6b3724d02221b01993a79ca60bccd66e61851f4703480a04c48f811f1407348e43b87d1df83f9e55bdb24227c9f4b21a44370b5b30b8fd30a37e182ac15c8e7633fa4147f812841f40ab0351d938adf0d4317cbc2ec28f348355e80d1221e54a53e731bf7eb88dace14d3e8d2ec4f1c7d4b5786e2dba266ad611ca6da13601da111200f6164ca61581307d62e507f0c8b1ad5e54594ed1894f8918698750c5e7914d8dc699c89f814f0de1b13c5e098bae7e3b86f98e6a98229579e685fb3b0006b920a0e25d2522decd318d7de",
    "31c67e7062e8ff5971debd6ca4b58bcb2564a332abeed776ec4bcc6780b7f65135e70caa0d7d84a766c182892812dd8e1036bc177f3a4d721f531d717b0b80d1ddcca654e7fe72fe0d3fa91c8e70a795a75b084b6606a437cf9fb14c1ae037a7a64ae71b1148dd7cff5a7195fd2b060c78533020ea32e0ed123e6bad2ccd43a3acc81a383cd1d8415c3e82acfcf5264b56631c52cc3571d066bdc666ea1247bb3f2ec5aa4c0daf00b949661eef7488948f9ef0a742cd696d29a2576eb5457fbcb305cde2423fb2c1a014deee6673a3157f832e46e806b03b5fd4c5da4c580709211734f90c6653c9d12c4b4eec2a7b1ff7b8dfd6dd09d3f6d1f90c1b7c4b548ce2c7b277ff6106e3d6092519ea111c0678748d704348",
    "2f84333362eae353649aa52aa1a896dc7621a529a7f9dd6beb438226d58cb00231ea09b55a7b85ec2780879a241dcd921c62a01a3a3503651e53534d321e8d92f1d1b749aab757bf5e6ba71a8f33a083e655065c6610a9368a8eb4474ea23de1e945a9540b56996dff1b7d97b06322146950753af67be0d758336be12fd759e7e1d11b2332dc93417d2483e0f1b3624d4d2e554e992632c161bfca34e15d53f6722acca64543f645ce442705ff279d949c83f1a347da6963689f0321b8496ff0be438fe8172cb2c3bd19dce5623fa214398a2946f910fe3a50c5808d4f4f068581e032f25c67538898305b58e2",
    "3d99723377e8f41230fbaa28e7a292dd3869a93ceefad93ff04981699cabf6572bf105a3143290a334808b8736508e8d5562ba173a3f03721958076c351e80dcd1c7e257a5bf55eb036b8813dd24ad95e67b08502812ac28cf89bf4c1aa93ea8e358a9520a579974ec1d7d98ff2f47006d4c2727fb6cb388152562ad29cb58abe898043820d2d6007d2893ffe6b3724d02371d44852632d77bb9cc28e3155ffb7b2983ef6642f812fc016f09fc31c9d5df9ffaa641c660227b920323b34b64a3f74ac9a70730e6d0b65ad4ed276bae147f9f355cf102ac2b11d484d9480a0a9881f038fe407058da",
    "2184607c23e6f84830cda16caab297cc763db23faff99c76f60c836699bcf64336a201e6167385b866d2809b2e0edad4100bb252283e037015421a733a0d8092dbcae253a6b11beb4224af59dd27a0d0b451144e6603a0328a8ebc5700a778a8f258a9571147d86de4157ad5be0a1342654d7522ff7ca5c8503627ec399e0d8fd8fa131421de943e5a3997ebf2fa68457d060d51803b7bd06ebfca29ea2267fe6b32f2844754872bf64f640dd5068cc18c89beb8",
    "3f8e7c342da4c35330c8a12fa8b58098392fe033baadd16af158cc6d8daca55665eb0ee60e7a93ec31d28c9c3519c0da442db9172c75035856411a69375980dcc1cbb042e9bf57f40d3fb3149e35b6d0a74a02052303a4378a8bfc1e0fae3ce1ef5fa9481645d575ad14718dfb314700691e263ef175a5ca153d61ad25d448a9e0c146771ad1d615762ed6e9fbf66b5b022603449e747ec16eb9cd35a41256b7762e81ef5548f812f04d6b48e2359fd1df82f0e55dcd672c678f032dbe4b64b3b20b",
    "3986613566e0a31c44d2a16caaa896dd763ea57aaae4cf7cf75f9f289cb1fa0231ea05e61d6093ad32c597c83514cbda422ba719717b666713440a25361688d7dccae250acfe5ffd412ab859dd24ad95e67b08502812ac28cf9ca44c0bae3fb5ee4ee7485e4dcd6aad1e719dfb2d14077f107519fb3eadd1462627ec29d00db4e3d7067731d2900e6c2ed6e3e0e126554b2d114e9b747dc22fa4d336eb0f44e27133d9b6024eb40aea447446",
    "31c67f3c23e7e25160dbb629e7b38cdd7625a12eabfec83fe64d9869d5b2bf562da20fb3083294ad25cb9098610cc29b5e6cf4253a7b4e6405425360291896d792dfac5ee9ad52ff436bb610dd27a082a3180f403414eb",
    "2f8433236bebf850749aa122a3e790d03f3ae037abe8c876ec4bcc699ba1f64f2af405e60e7dd6ad66cd8a9a245cdd9f5337a6177f28427f154206687559acd492caaa42a0ac1bf54c2ca406dd3fb7d0b5480e403551a4368acfb35201b331afe10be0555204cd71e8033496ff3a470b624a303cfd7bb0d0153d72ff6ad342b5e8cb467704d2d60c6b3882acfbfc720256221e44cc207ac57bebc02ee51353f2317ae1aa560dac0df052270aef749ddc9accf3a45ddc242e6c98502fb14f2ab9b905dbef0b2db2d2a31bdeee29",
    "308e7f3423ebe31230f3e321e7b481dd3f27a77abdf9ce7eec4b892886acb14c24ee13e61c6099a166cf909c3215ca9f1e6283177f364a761e4253673e5992d3c6ddaa42adf0",
    "598d763175e1",
    "598d763175e1",
    "598d763175e1",
    "368e67707ae1f91030d8b138e78ec3d5762aa83fade6d571e50c9f6798a0f6572bf713b31b7ed6bf2fc78b892d0f80da7924f406373e5a3105531d763e5990c19e9eb542e9b352ff453fe11d9c26a0d0b25747462e10ab238acfbf4b1ce02ca0e55fe0580d0a"
]
# Pares conocidos (basados en los ÃƒÂºltimos mensajes idÃƒÂ©nticos)
known_pairs = [
    ("598d763175e1", b"!leave")  # Los 3 ÃƒÂºltimos mensajes son idÃƒÂ©nticos y probablemente son !leave
]

# =============================================
# ReconstrucciÃƒÂ³n inteligente del Keystream
# =============================================

class KeystreamManager:
    def __init__(self):
        self.keystream = bytearray()
        self.known_positions = set()
    
    def add_known_pair(self, ct_hex, plaintext):
        """AÃƒÂ±ade un par conocido (cifrado, texto plano) al keystream"""
        ct = binascii.unhexlify(ct_hex)
        if len(ct) > len(self.keystream):
            # Extender el keystream con bytes nulos si es necesario
            self.keystream.extend(b'\x00' * (len(ct) - len(self.keystream)))
        
        # Calcular la porciÃƒÂ³n del keystream
        new_ks = xor(ct, plaintext)
        
        # Actualizar el keystream y marcar posiciones conocidas
        for i in range(len(new_ks)):
            if i < len(plaintext):  # Solo para las posiciones donde tenemos texto plano
                self.keystream[i] = new_ks[i]
                self.known_positions.add(i)
    
    def add_crib(self, ct_hex, crib, offset):
        """AÃƒÂ±ade un crib (texto supuesto) al keystream"""
        ct = binascii.unhexlify(ct_hex)
        if offset + len(crib) > len(ct):
            print(f"Error: Crib demasiado largo (offset {offset}, len {len(crib)}, ciphertext len {len(ct)})")
            return
        
        # Calcular la porciÃƒÂ³n del keystream
        new_ks = xor(ct[offset:offset+len(crib)], crib)
        
        # Extender el keystream si es necesario
        if len(self.keystream) < offset + len(new_ks):
            self.keystream.extend(b'\x00' * (offset + len(new_ks) - len(self.keystream)))
        
        # Actualizar el keystream
        for i in range(len(new_ks)):
            self.keystream[offset + i] = new_ks[i]
            self.known_positions.add(offset + i)
    
    def decrypt(self, ct_hex):
        """Descifra un mensaje usando el keystream actual"""
        ct = binascii.unhexlify(ct_hex)
        decrypted = bytearray()
        
        for i in range(len(ct)):
            if i < len(self.keystream) and i in self.known_positions:
                decrypted.append(ct[i] ^ self.keystream[i])
            else:
                decrypted.append(0x3F)  # '?' para bytes desconocidos
        
        try:
            return decrypted.decode('utf-8', errors='replace')
        except:
            return str(decrypted)
    
    def find_repetitions(self):
        """Busca repeticiones en el keystream para identificar patrones"""
        repetitions = defaultdict(list)
        for i, byte in enumerate(self.keystream):
            if byte != 0:  # Ignorar bytes no descubiertos
                repetitions[byte].append(i)
        return {k: v for k, v in repetitions.items() if len(v) > 1}

# =============================================
# AnÃƒÂ¡lisis inicial
# =============================================

ks_manager = KeystreamManager()

# 1. AÃƒÂ±adir pares conocidos
for ct, pt in known_pairs:
    ks_manager.add_known_pair(ct, pt)

# 2. Analizar los primeros mensajes (probablemente comandos !nick)
ks_manager.add_crib("598f7a3368a4c9537fd7a22da9a0", b"!nick Doomfang", 0)
ks_manager.add_crib("598f7a3368a4de487fc8a92ea6a981", b"!nick Stormbane", 0)
ks_manager.add_crib("598f7a3368a4df497edfa620aea08ccc", b"!nick Runeblight", 0)
ks_manager.add_crib("368e67707ae1f91030d8b138e78ec3d5762aa83fade6d571e50c9f6798a0f6572bf713b31b7ed6bf2fc78b892d0f80da7924f406373e5a3105531d763e5990c19e9eb542e9b352ff453fe11d9c26a0d0b25747462e10ab238acfbf4b1ce02ca0e55fe0580d0a", b"Not yet, but I'm checking some unusual signals. If they sense us, we might have to change our tactics.", 0)

# =============================================
# VisualizaciÃƒÂ³n mejorada de mensajes
# =============================================

def print_full_messages():
    print("\n=== MENSAJES COMPLETOS ===")
    print("(Los caracteres desconocidos se muestran como ?)\n")
    
    for idx, ct_hex in enumerate(ciphertexts):
        decrypted = ks_manager.decrypt(ct_hex)
        ct_length = len(binascii.unhexlify(ct_hex))
        known_bytes = sum(1 for i in range(ct_length) if i in ks_manager.known_positions)
        
        print(f"\n=== Mensaje {idx} ({known_bytes}/{ct_length} bytes conocidos) ===")
        print(f"Hex: {ct_hex[:12]}...{ct_hex[-12:]}")
        print("Texto completo:")
        print(decrypted)
        print("-" * 80)

# =============================================
# Descifrado interactivo mejorado
# =============================================

def interactive_decryption():
    print("\n=== DESCIFRADO INTERACTIVO MEJORADO ===")
    print("Instrucciones:")
    print("1. Revisa los mensajes completos mostrados")
    print("2. Cuando identifiques un fragmento legible, ingresa:")
    print("   - NÃƒÂºmero de mensaje")
    print("   - Offset donde comienza el texto conocido")
    print("   - El texto supuesto (crib)")
    print("3. Escribe 'quit' para salir\n")
    
    while True:
        print_full_messages()
        
        user_input = input("\nIngresa (mensaje offset crib) o 'quit': ").strip()
        if user_input.lower() == 'quit':
            break
        
        try:
            parts = user_input.split()
            msg_idx = int(parts[0])
            offset = int(parts[1])
            crib = ' '.join(parts[2:]).encode()
            
            if msg_idx < 0 or msg_idx >= len(ciphertexts):
                print("Error: ÃƒÂndice de mensaje invÃƒÂ¡lido")
                continue
            
            ks_manager.add_crib(ciphertexts[msg_idx], crib, offset)
            print(f"\nCrib aÃƒÂ±adido: mensaje {msg_idx}, offset {offset}, texto '{crib.decode()}'")
        except Exception as e:
            print(f"\nError: {e}. Formato esperado: 'mensaje offset texto'")

# =============================================
# EjecuciÃƒÂ³n principal
# =============================================

if __name__ == "__main__":
    # Mostrar estado inicial del keystream
    print("\n=== ESTADO INICIAL DEL KEYSTREAM ===")
    print(f"Longitud actual: {len(ks_manager.keystream)} bytes")
    print(f"Bytes conocidos: {len(ks_manager.known_positions)}")
    
    # Iniciar el modo interactivo
    interactive_decryption()
    
    # Mostrar estado final del keystream
    print("\n=== ESTADO FINAL DEL KEYSTREAM ===")
    print(f"Longitud: {len(ks_manager.keystream)} bytes")
    print(f"Bytes conocidos: {len(ks_manager.known_positions)}")
    print(f"Porcentaje conocido: {len(ks_manager.known_positions)/len(ks_manager.keystream)*100:.2f}%")
```
