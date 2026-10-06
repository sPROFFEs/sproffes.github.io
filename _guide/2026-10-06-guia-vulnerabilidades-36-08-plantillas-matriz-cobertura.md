---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Matriz de cobertura y aplicabilidad"
permalink: /guia/08-plantillas/matriz-cobertura/
order: 890
toc: true
comments: false
math: false
mermaid: true
---

# Matriz de cobertura y aplicabilidad

> Duplicar esta nota por evaluación. Crear una fila por combinación relevante de superficie, actor y familia.

| ID | Familia | Capacidad/precondición | Superficie | Actor/rol/tenant | Control esperado | Caso positivo/negativo/límite | Estado | Evidencia | Cobertura residual |
|---|---|---|---|---|---|---|---|---|---|
| COV-001 | Autorización de objeto | Objetos con propietario | `GET /api/items/{id}` | usuario A / usuario B | Comprobación de owner en servidor | propio / ajeno / inexistente | Pendiente | | |

## Estados permitidos

- `APLICA-PENDIENTE`
- `HALLAZGO`
- `SIN-HALLAZGO`
- `NO-APLICA`
- `BLOQUEADO`
- `FUERA-DE-ALCANCE`

## Reglas de calidad

- “No aplica” exige evidencia de ausencia de precondición.
- “Sin hallazgo” exige muestra, identidades usadas y limitaciones.
- “Bloqueado” exige acción concreta para resolverlo.
- “Fuera de alcance” no implica que el riesgo no exista.
