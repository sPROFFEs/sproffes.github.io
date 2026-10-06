---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: sesiones, cookies, JWT y CSRF"
toc: true
permalink: /guia/10-playbooks/02-sesiones-cookies-jwt-csrf/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Se utilizan cookies, sesiones, bearer tokens, JWT, refresh tokens o almacenamiento del navegador.

## Pruebas

- Flags `Secure`, `HttpOnly`, `SameSite`, dominio y ruta.
- Rotación al iniciar sesión y elevar privilegios.
- Revocación al cerrar sesión, suspender usuario o cambiar credenciales.
- Caducidad absoluta, inactividad y sesiones concurrentes.
- JWT: firma, algoritmo fijado, `exp`, `nbf`, `iss`, `aud` y tipo.
- CSRF en toda operación con efecto, incluidas API JSON y GraphQL.

```bash
curl -isk "$BASE_URL/" -D /tmp/headers-control.txt -o /dev/null
grep -i '^set-cookie:' /tmp/headers-control.txt
curl -isk "$BASE_URL/api/me" -H "Authorization: Bearer $TOKEN_A"
```

Para CSRF elimina el token antifalsificación de una petición propia y cambia `Origin` a un origen controlado. No publiques una PoC si una comparación manual es suficiente.

## Evidencia

Conserva petición previa y posterior a la revocación, claims decodificados sin guardar secretos y efecto persistente. Una cookie amplia o una sesión aceptada después de revocarla requieren revisión.

## Referencias locales

- `hacktricks/src/pentesting-web/hacking-jwt-json-web-tokens.md`
- `hacktricks/src/pentesting-web/csrf-cross-site-request-forgery.md`
