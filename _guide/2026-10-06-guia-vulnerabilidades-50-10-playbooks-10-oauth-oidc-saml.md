---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: OAuth, OIDC, SAML y SSO"
toc: true
permalink: /guia/10-playbooks/10-oauth-oidc-saml/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

El producto delega autenticación, enlaza identidades o actúa como cliente, IdP, SP, authorization server o resource server.

## Pruebas

- `redirect_uri` exacta y previamente registrada.
- `state` y `nonce` únicos, ligados a sesión y de un solo uso.
- PKCE con `S256` en clientes públicos.
- Código ligado a cliente, redirect URI y usuario.
- Firma, emisor, audiencia, tiempo y tipo de token.
- Account linking con prueba de ambas identidades.
- SAML: firma del elemento consumido, destino, audiencia, tiempo, `InResponseTo` y replay.
- Logout y revocación entre participantes.

```bash
curl -isk "$BASE_URL/.well-known/openid-configuration"
```

Captura un flujo propio y modifica un parámetro cada vez. No reutilices tokens reales fuera de cuentas de prueba.

## Señales

Login CSRF, código o assertion reutilizable, token de otro cliente aceptado, enlace inseguro de cuentas o diferencia entre elemento firmado y procesado.

## Referencias locales

- `hacktricks/src/pentesting-web/oauth-to-account-takeover.md`
- `hacktricks/src/pentesting-web/hacking-jwt-json-web-tokens.md`
