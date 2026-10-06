---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
title: "Fase 4. Identidad, registro y recuperación"
permalink: /guia/02-nucleo-web/04-identidad-registro-y-recuperacion/
order: 204
toc: true
comments: false
math: false
mermaid: true
---

# Fase 4. Identidad, registro y recuperación

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

## 4.1 Registro y enumeración

- [ ] Enumeración por respuesta, tiempo, código, captcha o recuperación.
- [ ] Verificación de correo/teléfono y posibilidad de cambiar el destino durante el flujo.
- [ ] Duplicados, normalización Unicode, mayúsculas, espacios y alias de correo.
- [ ] Asignación de rol, tenant, plan, saldo o atributos manipulables.
- [ ] Invitaciones: caducidad, destinatario, un solo uso, tenant y privilegio.
- [ ] Prevención de registro con dominios o identidades reservadas.

## 4.2 Contraseñas y autenticación

- [ ] Política razonable de longitud y comprobación frente a contraseñas comprometidas.
- [ ] Sin truncado silencioso ni normalización inconsistente.
- [ ] Rate limiting por cuenta, IP, dispositivo y riesgo, evitando bloqueo abusivo.
- [ ] MFA: inscripción, reto, recuperación, cambio y desactivación.
- [ ] Códigos OTP impredecibles, caducidad, un solo uso y límites de intento.
- [ ] “Recordar dispositivo” vinculado y revocable.
- [ ] Reautenticación para acciones sensibles.
- [ ] Resistencia a credential stuffing sin crear DoS de bloqueo.

## 4.3 Recuperación de cuenta

- [ ] Token aleatorio, de alta entropía, corto, de un solo uso y ligado a usuario/propósito.
- [ ] No filtrado en URL, Referer, logs, analytics o terceros.
- [ ] Host header no controla el enlace de recuperación.
- [ ] Cambiar contraseña invalida sesiones y tokens según política.
- [ ] Cambio de email/teléfono exige autenticación fuerte y notifica al canal anterior.
- [ ] Flujos de soporte no permiten saltar controles.

---
date: 2026-10-06 10:35:00 +0200
categories: [Metodología, Análisis de vulnerabilidades]
tags: [pentesting, appsec, seguridad, owasp, metodologia]
pin: false
