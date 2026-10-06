---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: autenticación, recuperación y MFA"
toc: true
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Existe inicio de sesión, registro, invitación, recuperación, cambio de correo o contraseña, MFA, enlace mágico, clave API o autenticación federada.

## Preparación

Crea dos usuarios controlados y, si existe separación de privilegios, una cuenta con rol diferente. Registra mensajes, códigos, tamaños y tiempos para una identidad existente y otra inexistente.

## Pruebas

- Enumeración por mensaje, código HTTP, longitud o tiempo.
- Rate limiting por cuenta, IP, sesión, dispositivo y endpoint equivalente.
- Reutilización, expiración, entropía y propósito de tokens.
- Invalidación de sesiones tras cambiar contraseña, correo o MFA.
- MFA en login, recuperación, desactivación y operaciones sensibles.
- Diferencias entre identidad local, invitada y federada.

```bash
curl -isk "$BASE_URL/login" -H 'Content-Type: application/json'   --data '{"username":"usuario-control","password":"incorrecta-unica"}'

curl -isk "$BASE_URL/password/reset" -H 'Content-Type: application/json'   --data '{"email":"cuenta-control@example.invalid"}'
```

Repite manualmente pocas veces y compara con una identidad inexistente. No realices fuerza bruta.

## Señales y decisión

Es hallazgo una diferencia estable que enumere cuentas, un token reutilizable o válido para otro propósito, ausencia de invalidación, omisión de MFA o límites ineficaces. Declara `NO-APLICA` solo si la capacidad no existe y hay evidencia de arquitectura o configuración.

## Referencias locales

- `hacktricks/src/pentesting-web/account-takeover.md`
- `hacktricks/src/pentesting-web/reset-password.md`
- `hacktricks/src/pentesting-web/2fa-bypass.md`
- `hacktricks/src/pentesting-web/rate-limit-bypass.md`
