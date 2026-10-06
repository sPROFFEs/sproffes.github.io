---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Playbook: inyecciones del servidor"
toc: true
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Una entrada alcanza SQL, NoSQL, ORM, LDAP, XPath, comandos, plantillas, expresiones, XML, XSLT, serializadores u otro intérprete.

## Método seguro

1. Captura una respuesta base.
2. Introduce un delimitador no destructivo.
3. Busca error, cambio booleano o variación temporal pequeña.
4. Confirma con una condición inversa.
5. Detente antes de extraer datos o ejecutar comandos.

```bash
curl -iskG "$BASE_URL/search" --data-urlencode "q=valor-control'"
curl -iskG "$BASE_URL/search" --data-urlencode 'q=valor-control"'
curl -isk "$BASE_URL/api/filter" -H 'Content-Type: application/json'   --data '{"name":{"unexpectedOperator":"control"}}'
```

Estos valores solo detectan manejo anómalo. Adapta la prueba a la gramática observada sin automatizar extracción.

## Cobertura

Incluye SQL/ORM, NoSQL, LDAP, XPath, command injection, SSTI, expresiones, CRLF, XXE, XSLT, deserialización y fórmulas CSV.

## Decisión

Un error estable, diferencia verdadero/falso, evaluación inocua o interacción con receptor autorizado justifica profundizar. Un bloqueo del WAF no demuestra que la capa de aplicación sea segura.

## Referencias locales

- `hacktricks/src/pentesting-web/command-injection.md`
- `hacktricks/src/pentesting-web/nosql-injection.md`
- `hacktricks/src/pentesting-web/ldap-injection.md`
- `hacktricks/src/pentesting-web/xpath-injection.md`
- `hacktricks/src/pentesting-web/xxe-xee-xml-external-entity.md`
