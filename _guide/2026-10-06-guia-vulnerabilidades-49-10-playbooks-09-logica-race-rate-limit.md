---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: lógica de negocio, race conditions y rate limiting"
toc: true
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Hay pagos, reservas, cupones, saldos, cuotas, invitaciones, aprobaciones, estados o claves de idempotencia.

## Método

Dibuja la máquina de estados indicando actor, transición, precondición, control, efecto y reversibilidad. Prueba omisión, repetición, reordenación y concurrencia.

## Pruebas

- Cero, negativos, máximos y precisión decimal.
- Precio, cantidad, moneda, propietario o estado enviados por cliente.
- Reutilización de cupones, enlaces, invitaciones e idempotencia.
- Saltos de pasos y llamadas directas.
- Dos solicitudes simultáneas sobre un recurso reversible.
- Límites en todas las rutas, identidades y nodos.

```bash
curl -isk -X POST "$BASE_URL/api/action"   -H "Authorization: Bearer $TOKEN_A"   -H 'Idempotency-Key: control-7f3a'   -H 'Content-Type: application/json'   --data '{"resource":"test-only"}'
```

Comienza con dos solicitudes, no con carga sostenida.

## Señales

Doble consumo o abono, transición inválida, precio confiado desde cliente, límite inconsistente o idempotencia no vinculada a actor, operación y cuerpo.

## Referencias locales

- `hacktricks/src/pentesting-web/race-condition.md`
- `hacktricks/src/pentesting-web/rate-limit-bypass.md`
- `hacktricks/src/pentesting-web/bypass-payment-process.md`
