---
categories:
- Forensisch
- Netz
date: 2024-11-05 11:58:38 +0000
lang: de
original_lang: es
tags:
- pxe
- kali
- forensics
- ipxe
title: Forensische Tools beginnen aus dem Netzwerk (PXE)
---

## IPXE -Schaltkonfiguration

### Installation der Anforderungen

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

Wo die Schnittstelle und die IP von der Maschine abhängen.

### Schaffung von Verzeichnissen

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

### Boot.IPXE -Konfiguration

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

### Permain -Konfiguration

```bash
sudo chmod -R 755 /tftpboot
sudo chown -R nobody:nogroup /tftpboot
```

### Solución de Error de Timeout

```bash
sudo nano /etc/default/dnsmasq
```

Fügen Sie die folgende Zeile hinzu:

```bash
DNSMASQ_OPTS= "--log-facility=/var/log/dnsmasq.log --tftp-max-connections=100 --tftp-timeout=600"
```

### Reinicio del Servicio

```bash
sudo systemctl restart dnsmasq
```

> ** Wichtig **
>
> - Das Problem dieses Prozesses ist, dass die Verwendung der TFTP -Übertragung sehr langsam ist und dass die Kali -Live -ISO -Größe bei etwa 4,5 GB nicht die optimalste beträgt.
>
> - Eine andere Sache, die Sie beachten sollten, ist, dass es sehr einfach ist, dass ein Parameter dabei gut angepasst wird und die Verbindung kontinuierlich unterbrochen oder nicht festgelegt ist.
>
> - In diesem Prozess muss die ISO des Systems in den Speicher geladen werden, damit die Maschine über genügend Speicherplatz im RAM verfügt.