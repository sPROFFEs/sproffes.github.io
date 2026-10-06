---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: autorización, IDOR y multitenancy"
toc: true
permalink: /guia/10-playbooks/03-autorizacion-idor-multitenancy/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Existen objetos, funciones, roles, organizaciones, tenants o recursos pertenecientes a usuarios.

## Matriz mínima

Cruza `listar`, `leer`, `crear`, `modificar`, `borrar`, `exportar` y `compartir` con propietario, no propietario, otro tenant y rol superior. Incluye objetos activos, archivados, borrados y compartidos.

```bash
curl -isk "$BASE_URL/api/objects/$ID_A" -H "Authorization: Bearer $TOKEN_A"
curl -isk "$BASE_URL/api/objects/$ID_B" -H "Authorization: Bearer $TOKEN_A"
curl -isk -X PATCH "$BASE_URL/api/objects/$ID_A"   -H "Authorization: Bearer $TOKEN_A" -H 'Content-Type: application/json'   --data '{"displayName":"control-autorizado"}'
```

Utiliza exclusivamente objetos de las cuentas de prueba. Sustituye un identificador cada vez en URL, cuerpo, cabecera y estructuras anidadas.

## Ampliación

Comprueba mass assignment, endpoints versionados, miniaturas, exportaciones, búsquedas, WebSockets, trabajos asíncronos, enlaces compartidos y cachés tras cambiar membresías.

## Señales y decisión

Confirma si se devuelve información cruzada, se modifica un objeto ajeno, se accede a una función privilegiada o la separación solo existe en la interfaz. Un `404` no basta para descartar si otras operaciones o identificadores no se probaron.

## Referencias locales

- `hacktricks/src/pentesting-web/idor.md`
- `hacktricks/src/pentesting-web/mass-assignment-cwe-915.md`
