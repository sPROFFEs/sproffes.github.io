---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: archivos, rutas y subidas"
toc: true
permalink: /guia/10-playbooks/07-archivos-rutas/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

El producto sube, descarga, previsualiza, transforma, importa, exporta, comprime o descomprime archivos.

## Pruebas

- Nombre, extensión, MIME declarado y contenido real.
- Almacenamiento fuera de raíz pública y nombre generado por servidor.
- Autorización en descarga, miniatura, conversión y URL firmada.
- Traversal y normalización de rutas.
- Rutas internas, enlaces y expansión de comprimidos.
- Procesadores de imagen, PDF, Office, vídeo, antivirus y OCR.

```bash
printf 'contenido-control
' > /tmp/control.txt
curl -isk -X POST "$BASE_URL/upload" -H "Authorization: Bearer $TOKEN_A"   -F 'file=@/tmp/control.txt;type=text/plain'
curl -iskG "$BASE_URL/download" --data-urlencode 'name=control.txt'   -H "Authorization: Bearer $TOKEN_A"
```

No subas ejecutables ni archivos grandes. Usa canarios de texto y ficheros mínimos.

## Señales

Contenido servido como activo, acceso cruzado, ruta fuera del directorio esperado, validación basada solo en extensión o procesador con privilegios innecesarios.

## Referencias locales

- `hacktricks/src/generic-hacking/archive-extraction-path-traversal.md`
- `hacktricks/src/pentesting-web/formula-csv-doc-latex-ghostscript-injection.md`
