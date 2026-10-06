---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: móvil, escritorio y extensiones"
toc: true
permalink: /guia/10-playbooks/14-clientes/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

Existe APK, IPA, cliente de escritorio, Electron, extensión, protocolo personalizado o deep link.

## Pruebas

- Permisos, componentes exportados, deep links y esquemas URL.
- Datos en preferencias, bases, logs, caché y copias.
- TLS y almacén de confianza.
- IPC, intents, WebViews y bridges JavaScript.
- Firma, actualización, rollback y plugins.
- Extensiones: permisos, content scripts, mensajes, páginas accesibles y CSP.
- Escritorio: ACL, argumentos, protocol handlers y servicios auxiliares.

```bash
apkanalyzer manifest print app-control.apk 2>/dev/null || true
unzip -l app-control.apk | head -40
```

Ejecuta estos comandos solo sobre binarios incluidos en el alcance. No distribuyas aplicaciones modificadas ni desactives controles de dispositivos ajenos.

## Señales

Componente invocable sin autorización, dato sensible recuperable, bridge privilegiado accesible desde origen no confiable o actualización no autenticada.

## Referencias locales

- `hacktricks/src/mobile-pentesting/android-checklist.md`
- `hacktricks/src/mobile-pentesting/ios-pentesting-checklist.md`
- `hacktricks/src/mobile-pentesting/cordova-apps.md`
