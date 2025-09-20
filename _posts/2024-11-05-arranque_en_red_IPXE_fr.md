---
categories:
- Légal
- Grille
date: 2024-11-05 11:58:38 +0000
lang: fr
original_lang: es
tags:
- pxe
- kali
- forensics
- ipxe
title: Les outils médico-légaux commencent à partir du réseau (PXE)
---

## Configuration manuelle IPXE

### Installation des exigences

```bash
sudo su
apt update && apt upgrade && apt install dnsmasq ipxe
```

### Configuración de DNSMASQ

```bash
sudo nano /etc/dnsmasq.conf
```

! [Dncsmasq.conf] (/assets/img/posts/start_en_ipxe/1.png)
_Dnsmasq.conf_

Où l'interface et l'IP dépendent de la machine.

### Création de répertoires

```bash
sudo mkdir -p /tftpboot/kali
sudo cp /usr/lib/ipxe/undionly.kpxe /tftpboot/
```

### Descarga y Configuración de la ISO

```bash
sudo mkdir -p /mnt/iso
wget https://cdimage.kali.org/kali-2024.3/kali-linux-2024.3-live-amd64.iso
sudo mount -o loop kali-linux-2024.3-live-amd64.iso /mnt/iso
sudo cp /mnt/iso/live/vmlinuz /tftpboot/kali/
sudo cp /mnt/iso/live/initrd.img /tftpboot/kali/
sudo cp /mnt/iso/live/filesystem.squashfs /tftpboot/kali/
```

### Configuration boot.ipxe

```bash
sudo nano /tftpboot/boot.ipxe
```

Contenido del archivo:

```bash
#!ipxe
:retry_boot
echo Iniciando Kali Linux...
# Configuración de red explícita
set net0/ip 192.168.244.109
set net0/netmask 255.255.255.0
set net0/gateway 192.168.244.128
# Intenta cargar kernel
kernel tftp://${next-server}/kali/vmlinuz || goto retry_boot
initrd tftp://${next-server}/kali/initrd.img || goto retry_boot
imgargs vmlinuz initrd=initrd.img boot=live components fetch=tftp://${next-server}/kali/filesystem.squashfs
boot || goto retry_boot
```

### Configuration du permain

```bash
sudo chmod -R 755 /tftpboot
sudo chown -R nobody:nogroup /tftpboot
```

### Solución de Error de Timeout

```bash
sudo nano /etc/default/dnsmasq
```

Ajouter la ligne suivante:

```bash
DNSMASQ_OPTS= "--log-facility=/var/log/dnsmasq.log --tftp-max-connections=100 --tftp-timeout=600"
```

### Reinicio del Servicio

```bash
sudo systemctl restart dnsmasq
```

> ** IMPORTANT **
>
> - Le problème de ce processus est que l'utilisation de la transmission TFTP est très lente et que celle ajoutée au fait que la taille ISO en direct de Kali est d'environ 4,5 Go n'est pas la plus optimale.
>
> - Une autre chose à garder à l'esprit est qu'il est très facile qu'un paramètre soit bien ajusté dans le processus et que la connexion est en continu ou n'est pas établie.
>
> - Dans ce processus, l'ISO du système doit être chargé en mémoire, donc la machine doit avoir suffisamment d'espace dans RAM.