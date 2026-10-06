---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Fase 3. Baseline y configuración transversal"
permalink: /guia/01-preparacion/03-baseline-y-configuracion-transversal/
order: 103
toc: true
comments: false
math: false
mermaid: true
---

# Fase 3. Baseline y configuración transversal

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

## 3.1 Transporte y HTTP

- [ ] HTTPS forzado y ausencia de mixed content.
- [ ] Protocolos y cifrados TLS adecuados; certificados, cadena, hostname y renovación.
- [ ] HSTS consistente en dominios aplicables.
- [ ] Headers: CSP, frame-ancestors/X-Frame-Options, nosniff, Referrer-Policy y Permissions-Policy.
- [ ] Política de caché para respuestas sensibles.
- [ ] CORS por endpoint, método, credenciales y origen.
- [ ] Métodos HTTP innecesarios deshabilitados.
- [ ] Host header y URLs absolutas generadas de forma segura.
- [ ] Normalización coherente entre CDN, proxy, WAF, gateway y backend.

## 3.2 Exposición y endurecimiento

- [ ] Sin banners, versiones, stack traces o comentarios sensibles.
- [ ] Sin listados de directorio, backups, `.git`, `.env`, logs o dumps.
- [ ] Debug, profiling, Swagger, Actuator, metrics y consolas protegidos.
- [ ] Cuentas, rutas y credenciales por defecto eliminadas.
- [ ] Separación del plano de administración.
- [ ] Mensajes de error genéricos hacia cliente y detalle solo en logs.
- [ ] Límites de body, headers, archivos, profundidad JSON/XML y tiempo de proceso.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
