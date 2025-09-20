---
categories:
- Forensic
- Grid
date: 2024-11-05 11:58:38 +0000
lang: en
original_lang: es
tags:
- pxe
- kali
- forensics
- ipxe
title: Forensic tools start from the network (PXE)
---

## IPXE manual configuration

### Installation of requirements

```bash
sudo su
apt update && apt upgrade && apt install dnsmasq ipxe
```

### Configuración de DNSMASQ

```bash
sudo nano /etc/dnsmasq.conf
```

! [DNCSMASQ.conf] (/ASSETS/IMG/POSTS/START_EN_IPXE/1.PNG)
_DNSMASQ.conf_

Where the interface and the IP depend on the machine.

### Creation of directories

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

### Boot.ipxe configuration

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

### Permain configuration

```bash
sudo chmod -R 755 /tftpboot
sudo chown -R nobody:nogroup /tftpboot
```

### Solución de Error de Timeout

```bash
sudo nano /etc/default/dnsmasq
```

Add the following line:

```bash
DNSMASQ_OPTS= "--log-facility=/var/log/dnsmasq.log --tftp-max-connections=100 --tftp-timeout=600"
```

### Reinicio del Servicio

```bash
sudo systemctl restart dnsmasq
```

> ** Important **
>
> - The problem of this process is that using TFTP transmission is very slow and that added to the fact that Kali Live iso size is about 4.5GB is not the most optimal.
>
> - Another thing to keep in mind is that it is very easy for a parameter to be well adjusted in the process and the connection is continuously broken or it is not established.
>
> - In this process the ISO of the system must be loaded in memory so the machine should have enough space in RAM.