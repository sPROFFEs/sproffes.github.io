---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Fase 24. Cobertura, informe, reprueba y cierre"
permalink: /guia/07-cierre/24-cobertura-informe-reprueba-y-cierre/
order: 724
toc: true
comments: false
math: false
mermaid: true
---

# Fase 24. Cobertura, informe, reprueba y cierre

> **RESUMEN: Navegación**
> [Mapa principal]({{ site.baseurl }}/) · [Índice del bloque]({{ site.baseurl }}/guia/)

## Protocolo obligatorio de aplicabilidad

> **IMPORTANTE: No descartar por ausencia de explotación**
> Una prueba fallida no demuestra que la vulnerabilidad no aplique. El evaluador debe demostrar primero si existe la precondición técnica y después verificar el control.

Para cada familia o control de esta sección:

1. **Identificar la capacidad**: comprobar si el producto implementa el componente, flujo, parser, protocolo, intérprete, almacén, frontera de confianza o privilegio relacionado.
2. **Localizar la superficie**: enumerar endpoints, parámetros, mensajes, ficheros, jobs, interfaces, roles, tenants y dependencias que utilizan esa capacidad.
3. **Trazar entrada a destino**: determinar de dónde procede el dato, qué transformaciones recibe, qué componente toma la decisión y dónde termina.
4. **Revisar controles**: verificar validación, autorización, aislamiento, canonicalización, límites, integridad, configuración y logging en la capa que realmente ejecuta la acción.
5. **Diseñar casos**: preparar un caso positivo válido, un caso negativo, un caso de límite y, cuando proceda, comparación entre usuarios, roles o tenants.
6. **Probar de forma segura**: usar marcadores únicos y el mínimo impacto suficiente. Evitar datos reales, persistencia, agotamiento y acciones destructivas.
7. **Confirmar por dos señales**: por ejemplo, respuesta más cambio de estado; petición más log; diferencia de identidad más acceso al objeto.
8. **Clasificar y justificar** mediante uno de estos estados:
   - **Aplica, pendiente de prueba**: existe la precondición o superficie.
   - **Hallazgo**: el control puede eludirse y existe evidencia reproducible.
   - **Probado sin hallazgo**: la superficie existe, se cubrió una muestra definida y el control resistió.
   - **No aplica**: no existe la capacidad o precondición. Debe indicarse cómo se comprobó.
   - **Bloqueado**: no fue posible decidir por falta de acceso, información, entorno o por riesgo operativo.
9. **Registrar cobertura residual**: indicar endpoints no probados, roles ausentes, integraciones inaccesibles y diferencias respecto de producción.

### Evidencia mínima para descartar

Solo puede marcarse **No aplica** si queda registrada al menos una evidencia verificable, como arquitectura confirmada, configuración, inventario, revisión de código, especificación de API o entrevista técnica contrastada. La ausencia de un parámetro visible o el fallo de un payload no es evidencia suficiente.


---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false

## 24.1 Control de cobertura

- [ ] Todos los componentes de la matriz de superficie tienen resultado.
- [ ] Todas las identidades y tenants previstos fueron utilizados.
- [ ] Todos los flujos críticos tienen máquina de estados revisada.
- [ ] Cada “No aplica” contiene justificación verificable.
- [ ] Cada “Sin hallazgo” indica muestra y limitaciones.
- [ ] Cada hallazgo tiene petición/flujo mínimo reproducible.
- [ ] Los scanners fueron validados manualmente.
- [ ] Se revisaron falsos negativos probables por WAF, caché, asincronía o entorno.
- [ ] Se eliminaron datos y cuentas de prueba conforme al acuerdo.

## 24.2 Plantilla de hallazgo

```markdown
# [ID] Título orientado al impacto

## Resumen
Qué control falla, dónde y qué puede conseguir un atacante.

## Activos afectados
- Componente:
- Endpoint/versión:
- Roles/tenants:

## Precondiciones
Acceso, rol, interacción de víctima, red o configuración necesarios.

## Pasos de reproducción
1. Preparación segura.
2. Petición o acción mínima.
3. Resultado verificable.

## Evidencia
Petición/respuesta sanitizada, captura, log y marcas temporales.

## Impacto
Confidencialidad, integridad, disponibilidad y efecto de negocio.

## Probabilidad y severidad
CVSS v4.0, exposición, complejidad y justificación empresarial.

## Causa raíz
Control ausente o aplicado en la capa incorrecta.

## Recomendación
Corrección estructural, defensa adicional y prueba unitaria/integración sugerida.

## Referencias
CWE, OWASP ASVS/WSTG/API Top 10 y documentación específica.

## Reprueba
Versión, fecha, casos positivos/negativos y resultado.
```

## 24.3 Reprueba

- [ ] Reproducir el caso original.
- [ ] Añadir caso negativo y caso límite.
- [ ] Comprobar variantes equivalentes y endpoints hermanos.
- [ ] Validar que la corrección está en servidor.
- [ ] Revisar regresiones funcionales.
- [ ] Actualizar severidad solo con evidencia.
- [ ] Cerrar como corregido, parcialmente corregido, no corregido o riesgo aceptado.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
