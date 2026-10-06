---
layout: page
date: 2026-10-06 10:35:00 +0200
pin: false
title: "Playbook: red, servicios, cloud y contenedores"
toc: true
permalink: /guia/10-playbooks/12-red-cloud-contenedores/
---

> **Uso autorizado.** Ejecuta estas comprobaciones únicamente sobre activos incluidos expresamente en el alcance. Sustituye las variables por cuentas, objetos y sistemas de prueba. Comienza con una sola solicitud y detente cuando obtengas la evidencia mínima necesaria.

> **Regla de decisión.** El fallo de un payload no permite declarar `NO-APLICA`. Para descartarlo debe demostrarse que no existe la capacidad, el flujo, el componente o el intérprete necesario. Si existe pero no puede probarse, registra `BLOQUEADO` o `APLICA-PENDIENTE`.

## Activar si

El alcance incluye hosts, puertos, servicios, cloud, contenedores, Kubernetes, registries o almacenamiento de objetos.

## Descubrimiento acotado

```bash
nmap -sV -Pn --top-ports 100 --max-rate 50 "$TARGET"
curl -isk "https://$TARGET/"
```

Ajusta puertos y velocidad al mandato. No uses scripts intrusivos por defecto.

## Para cada servicio

1. Confirma protocolo y versión sin confiar solo en el banner.
2. Revisa exposición, TLS, autenticación y autorización.
3. Comprueba acceso anónimo con operaciones de solo lectura.
4. Evalúa segmentación y privilegios de la identidad del servicio.
5. Correlaciona versión y avisos del fabricante sin asumir explotabilidad.

## Cloud y contenedores

- IAM efectivo, roles asumibles y separación entre cuentas.
- Buckets, blobs, snapshots, secretos y URLs firmadas.
- Security groups, endpoints privados y egress.
- Imágenes, tags, firmas, SBOM y procedencia.
- Kubernetes RBAC, service accounts, admission y API.
- Docker socket, registries y contenedores privilegiados.

## Referencias locales

- `hacktricks/src/network-services-pentesting/2375-pentesting-docker.md`
- `hacktricks/src/network-services-pentesting/5000-pentesting-docker-registry.md`
- Directorio `hacktricks/src/network-services-pentesting/` para cada puerto.
