---
title: Atenea - DFIR - Reto Linux
date: 2025-02-10 11:00:00 +0000
categories: [Laboratorios, DFIR]
tags: [Linux, Challenges, Write Up, DFIR, Atenea]
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Parte 1

## Banners del dump de memoria

```bash
❯ python3 vol.py -f /home/kali/Downloads/dump-practica5 banners.Banners
Volatility 3 Framework 2.20.0
Progress:  100.00		PDB scanning finished                  
Offset	Banner

0x18000c0	Linux version 4.2.0-16-generic (buildd@lcy01-07) (gcc version 5.2.1 20151003 (Ubuntu 5.2.1-21ubuntu2) ) #19-Ubuntu SMP Thu Oct 8 15:35:06 UTC 2015 (Ubuntu 4.2.0-16.19-generic 4.2.3)
0x1ef5464	Linux version 4.2.0-16-generic (buildd@lcy01-07) (gcc version 5.2.1 20151003 (Ubuntu 5.2.1-21ubuntu2) ) #19-Ubuntu SMP Thu Oct 8 15:35:06 UTC 2015 (Ubuntu 4.2.0-16.19-generic 4.2.3)
0x60cc0fe	Linux version 4.2.0-16-generic (buildd@lcy01-07) (gcc version 5.2.1 20151003 (Ubuntu 5.2.1-21ubuntu2) ) #19-Ubuntu SMP Thu Oct 8 15:35:06 UTC 2015 (Ubuntu 4.2.0-16.19-generic 4.2.3)
0x34a5d5a0	Linux version 4.2.0-16-generic (buildd@lcy01-07) (gcc version 5.2.1 20151003 (Ubuntu 5.2.1-21ubuntu2) ) #19-Ubuntu SMP Thu Oct 8 15:35:06 UTC 2015 (Ubuntu 4.2.0-16.19-generic 4.2.3)
```

Ahora que sabemos la versión del kernel y que es ubuntu vamos a buscar el mapeo de memoria necesario. Lamentablemente no encontramos nada en internet sobre esta versión de ubuntu por lo que nos tocará realizar un mapeo de memoria manual.

## Creando el mapeo de memoria

Primero vamos a descargar la versión correspondiente a este kernel de ubuntu.

[Versiones de ubuntu según Kernel](https://askubuntu.com/questions/517136/list-of-ubuntu-versions-with-corresponding-linux-kernel-version)

En esta lista encontramos que la versión de ubuntu es 15.10 y el kernel es 4.2.0-16-generic.

[Ubuntu old releases](https://old-releases.ubuntu.com/releases/)

Aquí vamos a encontrar la versión 15.10 necesaria. La descargamos y creamos la máquina virtual.

### Añadir los repositorios para versiones antiguas de ubuntu

Como la versión 15.10 ya no está soportada, en los repositorios principales de ubuntu ya no se ofrecen paquetes para esta versión.

Para solucionar esto, vamos a añadir los repositorios de ubuntu antiguos.

```bash
echo "## EOL upgrade sources.list
# Required
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-updates main restricted universe multiverse
deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-security main restricted universe multiverse

# Optional
#deb http://old-releases.ubuntu.com/ubuntu/ CODENAME-backports main restricted universe multiverse" | sudo tee /etc/apt/sources.list
```

Lo mejor es eliminar todos los repositorios dentro del archivo y añadir solo los que necesitemos, entonces quedaría así:

![alt text](/assets/img/posts/reto-atenea-linux/image.png)

### Crear el mapeo de memoria 

Para llevar a cabo el mapeo vamos a utilizar la herramienta que creé para extraer mapas de memoria para debian y ubuntu.

[Enlace en github](https://github.com/sPROFFEs/LinuxMemMapper)

```bash
sudo apt install git
git clone https://github.com/sPROFFEs/LinuxMemMapper.git
cd LinuxMemMapper
chmod +x LMM.sh
sudo ./LMM.sh
```

#### Volatility 2

![alt text](/assets/img/posts/reto-atenea-linux/image-1.png)

![alt text](/assets/img/posts/reto-atenea-linux/image-2.png)

Como vemos lo ha hecho correctamente.

#### Volatility 3

Lamentamente no he conseguido añadir los repositorios antiguos para debug por lo que la imagen para vol3 no la he conseguido. 

![alt text](/assets/img/posts/reto-atenea-linux/image-3.png)

![alt text](/assets/img/posts/reto-atenea-linux/image-4.png)

Por lo que en este caso vamos a prescindir de volatility 3.

### Importación del mapa a volatility 2

Para que volatility 2 pueda leer el mapa de memoria creado debemos añadirlo a la ruta de overlays de nuestro volatility 2, en mi caso:

```bash
/home/kali/Desktop/volatility/volatility/plugins/overlays/linux/
```

Una vez añadido podemos verificar que es correcto con:

```bash
vol2.py --info | grep linux
```
![alt text](/assets/img/posts/reto-atenea-linux/image-5.png)

## Análisis de procesos

Para esta parte del reto se nos pide identificar el PID de un proceso que se sospecha ha estado presuntamente realizando muchas peticiones a una IP externa.

Vamos a utilizar volatility 2 para realizar el análisis.

```bash
❯ python2 vol.py -f /home/kali/Downloads/dump-practica5 --profile=Linuxubuntu-kernel-4_2_0-16-generic-vol2x64 linux_pslist
Volatility Foundation Volatility Framework 2.6.1
Offset             Name                 Pid             PPid            Uid             Gid    DTB                Start Time
------------------ -------------------- --------------- --------------- --------------- ------ ------------------ ----------
0xffff88007c880000 systemd              1               0               0               0      0x000000007cb14000 2017-12-19 10:53:35 UTC+0000
0xffff88007c880dc0 kthreadd             2               0               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c881b80 ksoftirqd/0          3               2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c883700 kworker/0:0H         5               2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c885280 rcu_sched            7               2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c886040 rcu_bh               8               2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c886e00 rcuos/0              9               2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c0000 rcuob/0              10              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c0dc0 migration/0          11              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c1b80 watchdog/0           12              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c2940 khelper              13              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c3700 kdevtmpfs            14              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c44c0 netns                15              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c5280 perf                 16              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c6040 khungtaskd           17              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c8c6e00 writeback            18              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c960000 ksmd                 19              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c960dc0 khugepaged           20              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c961b80 crypto               21              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c962940 kintegrityd          22              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c963700 bioset               23              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c9644c0 kblockd              24              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c965280 ata_sff              25              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c966040 md                   26              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007c966e00 devfreq_wq           27              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007ca98000 kworker/u2:1         28              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007ca9a940 kswapd0              31              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007ca9b700 fsnotify_mark        32              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88007ca9c4c0 ecryptfs-kthrea      33              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88003581e040 kthrotld             44              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88003581ee00 acpi_thermal_pm      45              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff8800359a0000 scsi_eh_0            46              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff8800359a0dc0 scsi_tmf_0           47              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff8800359a1b80 scsi_eh_1            48              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff8800359a2940 scsi_tmf_1           49              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88003581d280 ipv6_addrconf        55              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff880035a76e00 deferwq              74              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff880035aa0000 charger_manager      75              2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88003581c4c0 kpsmoused            117             2               0               0      ------------------ 2017-12-19 10:53:35 UTC+0000
0xffff88003581a940 kworker/0:1H         120             2               0               0      ------------------ 2017-12-19 10:53:36 UTC+0000
0xffff88007ca99b80 scsi_eh_2            121             2               0               0      ------------------ 2017-12-19 10:53:36 UTC+0000
0xffff88007ca9e040 scsi_tmf_2           122             2               0               0      ------------------ 2017-12-19 10:53:36 UTC+0000
0xffff880035405280 jbd2/sda1-8          148             2               0               0      ------------------ 2017-12-19 10:53:39 UTC+0000
0xffff880035406040 ext4-rsv-conver      149             2               0               0      ------------------ 2017-12-19 10:53:39 UTC+0000
0xffff880035aa0dc0 kauditd              191             2               0               0      ------------------ 2017-12-19 10:53:39 UTC+0000
0xffff880035a73700 systemd-journal      209             1               0               0      0x0000000035ade000 2017-12-19 10:53:39 UTC+0000
0xffff880035a72940 systemd-udevd        214             1               0               0      0x0000000035ac6000 2017-12-19 10:53:39 UTC+0000
0xffff880035b58dc0 kworker/0:4          308             2               0               0      ------------------ 2017-12-19 10:53:39 UTC+0000
0xffff880035b5a940 iprt-VBoxWQueue      432             2               0               0      ------------------ 2017-12-19 10:53:39 UTC+0000
0xffff880078edc4c0 rsyslogd             503             1               104             109    0x0000000078fc0000 2017-12-19 10:53:39 UTC+0000
0xffff880078ede040 dbus-daemon          504             1               105             110    0x000000003523b000 2017-12-19 10:53:39 UTC+0000
0xffff880035400dc0 whoopsie             512             1               108             115    0x00000000789ab000 2017-12-19 10:53:40 UTC+0000
0xffff880035400000 cron                 515             1               0               0      0x0000000035627000 2017-12-19 10:53:40 UTC+0000
0xffff880035401b80 systemd-logind       523             1               0               0      0x0000000078ff7000 2017-12-19 10:53:40 UTC+0000
0xffff880035a744c0 cgmanager            526             1               0               0      0x0000000035254000 2017-12-19 10:53:40 UTC+0000
0xffff880035aa6040 cupsd                531             1               0               0      0x0000000035269000 2017-12-19 10:53:40 UTC+0000
0xffff8800359a5280 avahi-daemon         537             1               107             114    0x0000000078634000 2017-12-19 10:53:40 UTC+0000
0xffff880035b5c4c0 accounts-daemon      538             1               0               0      0x0000000078836000 2017-12-19 10:53:40 UTC+0000
0xffff880078561b80 avahi-daemon         546             537             107             114    0x0000000078810000 2017-12-19 10:53:40 UTC+0000
0xffff880078560000 ModemManager         571             1               0               0      0x000000007856f000 2017-12-19 10:53:40 UTC+0000
0xffff88007cbbe040 NetworkManager       575             1               0               0      0x0000000078e4c000 2017-12-19 10:53:40 UTC+0000
0xffff88007cbb8000 dbus                 579             531             7               7      0x0000000078831000 2017-12-19 10:53:40 UTC+0000
0xffff8800785644c0 dbus                 580             531             7               7      0x000000007a71c000 2017-12-19 10:53:40 UTC+0000
0xffff880078566040 dbus                 581             531             7               7      0x000000003524c000 2017-12-19 10:53:40 UTC+0000
0xffff880035b5d280 dbus                 582             531             7               7      0x000000007aaa8000 2017-12-19 10:53:40 UTC+0000
0xffff88007aaf8000 dbus                 583             531             7               7      0x000000007aaa5000 2017-12-19 10:53:40 UTC+0000
0xffff88007aaf8dc0 dbus                 584             531             7               7      0x000000007a732000 2017-12-19 10:53:40 UTC+0000
0xffff88007aaf9b80 dbus                 585             531             7               7      0x0000000078fef000 2017-12-19 10:53:40 UTC+0000
0xffff88007aafa940 dbus                 587             531             7               7      0x0000000078e38000 2017-12-19 10:53:40 UTC+0000
0xffff88007aafc4c0 dbus                 588             531             7               7      0x00000000788b1000 2017-12-19 10:53:40 UTC+0000
0xffff88007aafd280 dbus                 589             531             7               7      0x0000000078e79000 2017-12-19 10:53:40 UTC+0000
0xffff880078ed8dc0 sshd                 605             1               0               0      0x0000000035358000 2017-12-19 10:53:40 UTC+0000
0xffff880035402940 polkitd              627             1               0               0      0x000000007cbc8000 2017-12-19 10:53:40 UTC+0000
0xffff88007cbbb700 cups-browsed         629             1               0               0      0x000000007aab3000 2017-12-19 10:53:40 UTC+0000
0xffff8800786a8000 kerneloops           638             1               114             4      0x000000007aaca000 2017-12-19 10:53:40 UTC+0000
0xffff8800786ae040 vsftpd               641             1               0               0      0x0000000078757000 2017-12-19 10:53:40 UTC+0000
0xffff880035b5e040 ntpd                 646             1               121             129    0x00000000786dc000 2017-12-19 10:53:40 UTC+0000
0xffff8800786ab700 wpa_supplicant       650             1               0               0      0x0000000078734000 2017-12-19 10:53:40 UTC+0000
0xffff8800786a8dc0 dhclient             653             575             0               0      0x0000000076e13000 2017-12-19 10:53:41 UTC+0000
0xffff88007cbbc4c0 apache2              668             1               0               0      0x0000000076e7a000 2017-12-19 10:53:41 UTC+0000
0xffff880077266040 lightdm              737             1               0               0      0x0000000078c5c000 2017-12-19 10:53:41 UTC+0000
0xffff880077261b80 Xorg                 746             737             0               0      0x000000007a28d000 2017-12-19 10:53:41 UTC+0000
0xffff880034cd9b80 agetty               755             1               0               0      0x00000000772c6000 2017-12-19 10:53:42 UTC+0000
0xffff88007aba0dc0 lightdm              821             737             0               0      0x000000007abc6000 2017-12-19 10:53:42 UTC+0000
0xffff8800773644c0 rtkit-daemon         887             1               116             124    0x00000000773ab000 2017-12-19 10:53:43 UTC+0000
0xffff880035729b80 dnsmasq              899             575             -               30     0x000000003577b000 2017-12-19 10:53:43 UTC+0000
0xffff8800357d1b80 upowerd              1118            1               0               0      0x00000000357c1000 2017-12-19 10:53:43 UTC+0000
0xffff880077c06e00 colord               1173            1               111             121    0x000000003532b000 2017-12-19 10:53:44 UTC+0000
0xffff880078563700 systemd              1193            1               1000            1000   0x000000007a6f7000 2017-12-19 10:53:47 UTC+0000
0xffff88003572e040 (sd-pam)             1194            1193            1000            1000   0x0000000078d10000 2017-12-19 10:53:47 UTC+0000
0xffff8800784eee00 gnome-keyring-d      1208            1               1000            1000   0x0000000035737000 2017-12-19 10:53:47 UTC+0000
0xffff8800784ed280 upstart              1210            821             1000            1000   0x0000000077cf0000 2017-12-19 10:53:47 UTC+0000
0xffff880035728dc0 upstart-udev-br      1302            1210            1000            1000   0x0000000078d2e000 2017-12-19 10:53:47 UTC+0000
0xffff880035b58000 dbus-daemon          1308            1210            1000            1000   0x0000000035634000 2017-12-19 10:53:47 UTC+0000
0xffff880035a75280 window-stack-br      1320            1210            1000            1000   0x0000000078d0d000 2017-12-19 10:53:47 UTC+0000
0xffff88007bfdee00 bamfdaemon           1339            1210            1000            1000   0x000000007a3a3000 2017-12-19 10:53:47 UTC+0000
0xffff88007bfdb700 gvfsd                1349            1210            1000            1000   0x000000007a358000 2017-12-19 10:53:47 UTC+0000
0xffff8800784e9b80 gvfsd-fuse           1362            1210            1000            1000   0x000000007a3b7000 2017-12-19 10:53:47 UTC+0000
0xffff8800357d0000 upstart-dbus-br      1372            1210            1000            1000   0x000000007c2bf000 2017-12-19 10:53:47 UTC+0000
0xffff8800357d6e00 at-spi-bus-laun      1375            1210            1000            1000   0x00000000352d8000 2017-12-19 10:53:47 UTC+0000
0xffff880077c00dc0 upstart-dbus-br      1382            1210            1000            1000   0x000000007a617000 2017-12-19 10:53:47 UTC+0000
0xffff8800359a6040 upstart-file-br      1385            1210            1000            1000   0x00000000787cf000 2017-12-19 10:53:47 UTC+0000
0xffff88007bfd8000 dbus-daemon          1395            1375            1000            1000   0x0000000078c86000 2017-12-19 10:53:47 UTC+0000
0xffff880077362940 at-spi2-registr      1399            1210            1000            1000   0x000000003544f000 2017-12-19 10:53:47 UTC+0000
0xffff88007aba6040 ibus-daemon          1407            1210            1000            1000   0x000000003522e000 2017-12-19 10:53:47 UTC+0000
0xffff880078de0000 ibus-dconf           1416            1407            1000            1000   0x00000000784f4000 2017-12-19 10:53:47 UTC+0000
0xffff88007aba6e00 ibus-ui-gtk3         1419            1407            1000            1000   0x0000000079ce5000 2017-12-19 10:53:47 UTC+0000
0xffff880035818000 hud-service          1423            1210            1000            1000   0x000000007c25e000 2017-12-19 10:53:47 UTC+0000
0xffff88007aba5280 unity-settings-      1425            1210            1000            1000   0x000000007c2d2000 2017-12-19 10:53:47 UTC+0000
0xffff88007bfd9b80 ibus-x11             1428            1210            1000            1000   0x0000000000116000 2017-12-19 10:53:47 UTC+0000
0xffff880035aa6e00 compiz               1433            1210            1000            1000   0x0000000035440000 2017-12-19 10:53:47 UTC+0000
0xffff880035aa3700 gnome-session        1439            1210            1000            1000   0x000000007ab42000 2017-12-19 10:53:47 UTC+0000
0xffff8800357d44c0 unity-panel-ser      1446            1210            1000            1000   0x000000007c256000 2017-12-19 10:53:47 UTC+0000
0xffff880078402940 dconf-service        1462            1210            1000            1000   0x00000000353eb000 2017-12-19 10:53:47 UTC+0000
0xffff880034db6e00 ibus-engine-sim      1477            1407            1000            1000   0x0000000079d18000 2017-12-19 10:53:48 UTC+0000
0xffff880034de6e00 indicator-messa      1489            1210            1000            1000   0x000000007bf6c000 2017-12-19 10:53:48 UTC+0000
0xffff88003572b700 indicator-bluet      1490            1210            1000            1000   0x0000000079d9d000 2017-12-19 10:53:48 UTC+0000
0xffff880077c02940 indicator-power      1491            1210            1000            1000   0x0000000079de2000 2017-12-19 10:53:48 UTC+0000
0xffff880078de6040 indicator-datet      1492            1210            1000            1000   0x0000000077cc1000 2017-12-19 10:53:48 UTC+0000
0xffff880078400000 indicator-keybo      1496            1210            1000            1000   0x000000007a82d000 2017-12-19 10:53:48 UTC+0000
0xffff880034db44c0 indicator-sound      1500            1210            1000            1000   0x000000007a905000 2017-12-19 10:53:48 UTC+0000
0xffff88007a8d0000 indicator-print      1502            1210            1000            1000   0x000000007a924000 2017-12-19 10:53:48 UTC+0000
0xffff88007a8d0dc0 indicator-sessi      1505            1210            1000            1000   0x000000007a99f000 2017-12-19 10:53:48 UTC+0000
0xffff88007a9da940 indicator-appli      1514            1210            1000            1000   0x000000007c025000 2017-12-19 10:53:48 UTC+0000
0xffff88007c043700 evolution-sourc      1525            1210            1000            1000   0x000000007c1fb000 2017-12-19 10:53:48 UTC+0000
0xffff88007bc744c0 pulseaudio           1549            1210            1000            1000   0x000000007bd44000 2017-12-19 10:53:48 UTC+0000
0xffff88007bc1c4c0 nautilus             1585            1439            1000            1000   0x000000007bc5c000 2017-12-19 10:53:49 UTC+0000
0xffff88007bc18000 unity-fallback-      1587            1439            1000            1000   0x000000007bc7f000 2017-12-19 10:53:49 UTC+0000
0xffff88007bc1b700 polkit-gnome-au      1588            1439            1000            1000   0x000000003516a000 2017-12-19 10:53:49 UTC+0000
0xffff88007a8d5280 nm-applet            1590            1439            1000            1000   0x00000000351ad000 2017-12-19 10:53:49 UTC+0000
0xffff88007c041b80 evolution-calen      1593            1210            1000            1000   0x000000007a4c9000 2017-12-19 10:53:49 UTC+0000
0xffff88007a511b80 gvfs-udisks2-vo      1610            1210            1000            1000   0x000000007a538000 2017-12-19 10:53:49 UTC+0000
0xffff88007a5144c0 udisksd              1613            1               0               0      0x000000007a579000 2017-12-19 10:53:49 UTC+0000
0xffff88007a5e3700 gvfs-afc-volume      1623            1210            1000            1000   0x000000007a02e000 2017-12-19 10:53:49 UTC+0000
0xffff88007a5e2940 gvfs-mtp-volume      1629            1210            1000            1000   0x000000007a0a2000 2017-12-19 10:53:49 UTC+0000
0xffff88007a0d44c0 gvfs-gphoto2-vo      1637            1210            1000            1000   0x000000007a16d000 2017-12-19 10:53:49 UTC+0000
0xffff88007a1d8000 gconfd-2             1642            1210            1000            1000   0x000000007a000000 2017-12-19 10:53:49 UTC+0000
0xffff88007a5e0000 evolution-calen      1651            1593            1000            1000   0x0000000079f7f000 2017-12-19 10:53:50 UTC+0000
0xffff880079eb8dc0 evolution-calen      1661            1593            1000            1000   0x0000000079ed7000 2017-12-19 10:53:50 UTC+0000
0xffff880079eb9b80 gvfsd-trash          1662            1210            1000            1000   0x0000000079fb0000 2017-12-19 10:53:50 UTC+0000
0xffff880079ebd280 evolution-addre      1667            1210            1000            1000   0x0000000079ffa000 2017-12-19 10:53:50 UTC+0000
0xffff880078b16e00 evolution-addre      1692            1667            1000            1000   0x0000000078ba8000 2017-12-19 10:53:50 UTC+0000
0xffff880078bb5280 gvfsd-burn           1705            1210            1000            1000   0x0000000078bfb000 2017-12-19 10:53:51 UTC+0000
0xffff880077e0d280 unity-scope-loa      1733            1210            1000            1000   0x0000000079dc2000 2017-12-19 10:53:52 UTC+0000
0xffff880077e0ee00 zeitgeist-daemo      1740            1210            1000            1000   0x0000000078ae9000 2017-12-19 10:53:53 UTC+0000
0xffff88007bc19b80 zeitgeist-datah      1748            1210            1000            1000   0x0000000077ef2000 2017-12-19 10:53:53 UTC+0000
0xffff88007bc18dc0 zeitgeist-fts        1749            1210            1000            1000   0x0000000077ef5000 2017-12-19 10:53:53 UTC+0000
0xffff880077f8c4c0 gnome-terminal-      1776            1210            1000            1000   0x0000000077067000 2017-12-19 10:53:55 UTC+0000
0xffff880077c05280 gnome-pty-helpe      1782            1776            1000            1000   0x000000007715f000 2017-12-19 10:53:55 UTC+0000
0xffff880034de5280 bash                 1783            1776            1000            1000   0x0000000077184000 2017-12-19 10:53:55 UTC+0000
0xffff88007bc1d280 telepathy-indic      1795            1439            1000            1000   0x0000000077139000 2017-12-19 10:54:05 UTC+0000
0xffff880077f88000 mission-control      1804            1210            1000            1000   0x00000000770fc000 2017-12-19 10:54:05 UTC+0000
0xffff880077c044c0 bash                 1826            1776            1000            1000   0x0000000078a81000 2017-12-19 10:54:19 UTC+0000
0xffff880035b59b80 irssi                1849            1826            1000            1000   0x0000000079d30000 2017-12-19 10:54:29 UTC+0000
0xffff880078bb6040 bash                 1852            1776            1000            1000   0x0000000077f99000 2017-12-19 10:54:39 UTC+0000
0xffff880035b5ee00 update-notifier      1885            1439            1000            1000   0x0000000077d12000 2017-12-19 10:54:50 UTC+0000
0xffff880034de6040 gvfsd-metadata       1987            1210            1000            1000   0x00000000771c2000 2017-12-19 10:55:17 UTC+0000
0xffff88007a0d2940 htop                 2032            1783            1000            1000   0x000000007a313000 2017-12-19 10:55:41 UTC+0000
0xffff880035011b80 deja-dup-monito      2040            1439            1000            1000   0x00000000352ab000 2017-12-19 10:55:50 UTC+0000
0xffff880077266e00 apache2              2729            668             33              33     0x0000000035691000 2017-12-19 10:56:09 UTC+0000
0xffff880077361b80 apache2              2730            668             33              33     0x0000000076e40000 2017-12-19 10:56:09 UTC+0000
0xffff88007720d280 sudo                 2834            1852            0               1000   0x00000000352a3000 2017-12-19 10:57:42 UTC+0000
0xffff880077208000 tshark               2835            2834            0               0      0x0000000076d03000 2017-12-19 10:57:42 UTC+0000
0xffff88007720b700 dumpcap              2851            2835            0               0      0x0000000076d09000 2017-12-19 10:57:42 UTC+0000
0xffff880077208dc0 bash                 2880            1776            1000            1000   0x0000000034ccc000 2017-12-19 10:58:02 UTC+0000
0xffff880077c01b80 bash                 5411            1776            1000            1000   0x0000000035688000 2017-12-19 11:01:20 UTC+0000
0xffff88007c882940 kworker/u2:2         5423            2               0               0      ------------------ 2017-12-19 11:01:53 UTC+0000
0xffff8800356e6e00 kworker/0:0          5444            2               0               0      ------------------ 2017-12-19 11:03:23 UTC+0000
0xffff880077360dc0 sshd                 5491            605             0               0      0x00000000785c4000 2017-12-19 11:04:48 UTC+0000
0xffff880078b11b80 systemd              5493            1               0               0      0x0000000076dca000 2017-12-19 11:04:50 UTC+0000
0xffff880078b10000 (sd-pam)             5494            5493            0               0      0x00000000785ae000 2017-12-19 11:04:50 UTC+0000
0xffff880077236040 bash                 5554            5491            0               0      0x0000000077248000 2017-12-19 11:04:50 UTC+0000
0xffff880077230dc0 bash                 5580            1776            1000            1000   0x000000007794a000 2017-12-19 11:07:15 UTC+0000
0xffff8800772344c0 sudo                 5594            5580            0               1000   0x0000000077bb9000 2017-12-19 11:07:37 UTC+0000
0xffff880077230000 bash                 5595            5594            0               0      0x0000000076dde000 2017-12-19 11:07:39 UTC+0000
0xffff880077235280 system               5611            5554            0               0      0x0000000077392000 2017-12-19 11:08:19 UTC+0000
0xffff88007a5e1b80 kworker/0:1          5617            2               0               0      ------------------ 2017-12-19 11:08:43 UTC+0000
0xffff88007a5e6040 insmod               5618            5595            0               0      0x0000000027865000 2017-12-19 11:09:06 UTC+0000
0xffff88003581b700 kworker/u2:0         5620            2               0               0      ------------------ 2017-12-19 11:09:17 UTC+0000
```

Como podemos ver por alguno de los procesos, confirmamos que se trata de un sistema ubuntu que parece estar ejecutando algun servicio web con apache además de tener algun tipo de comunicación MQTT o Pub/Sub.

## Análisis de red

```bash
Volatility Foundation Volatility Framework 2.6.1
UNIX 8856               systemd/1     /run/systemd/private
UNIX 23837              systemd/1     
UNIX 8855               systemd/1     /run/systemd/notify
UNIX 11002              systemd/1     /run/acpid.socket
UNIX 11062              systemd/1     
UNIX 14799              systemd/1     
UNIX 14800              systemd/1     
UNIX 8865               systemd/1     /run/systemd/fsck.progress
UNIX 9330               systemd/1     /run/systemd/journal/syslog
UNIX 9063               systemd/1     /run/udev/control
UNIX 8873               systemd/1     /run/systemd/journal/stdout
UNIX 8874               systemd/1     /run/systemd/journal/socket
UNIX 11055              systemd/1     /var/run/avahi-daemon/socket
UNIX 9068               systemd/1     /run/systemd/journal/dev-log
UNIX 11056              systemd/1     /var/run/dbus/system_bus_socket
UNIX 11057              systemd/1     /run/uuidd/request
UNIX 11054              systemd/1     /var/run/cups/cups.sock
UNIX 8873       systemd-journal/209   /run/systemd/journal/stdout
UNIX 8874       systemd-journal/209   /run/systemd/journal/socket
UNIX 9068       systemd-journal/209   /run/systemd/journal/dev-log
UNIX 9616       systemd-journal/209   /run/systemd/journal/stdout
UNIX 11246      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11109      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11614      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11411      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11481      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11530      systemd-journal/209   /run/systemd/journal/stdout
UNIX 13852      systemd-journal/209   /run/systemd/journal/stdout
UNIX 12551      systemd-journal/209   /run/systemd/journal/stdout
UNIX 12553      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11879      systemd-journal/209   /run/systemd/journal/stdout
UNIX 11978      systemd-journal/209   /run/systemd/journal/stdout
UNIX 12647      systemd-journal/209   /run/systemd/journal/stdout
UNIX 13518      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16163      systemd-journal/209   /run/systemd/journal/stdout
UNIX 13051      systemd-journal/209   /run/systemd/journal/stdout
UNIX 13330      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16484      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16487      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16506      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16509      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16594      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16597      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16680      systemd-journal/209   /run/systemd/journal/stdout
UNIX 14868      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18286      systemd-journal/209   /run/systemd/journal/stdout
UNIX 15579      systemd-journal/209   /run/systemd/journal/stdout
UNIX 15889      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16683      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16866      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16878      systemd-journal/209   /run/systemd/journal/stdout
UNIX 16881      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18169      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18172      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17163      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17166      systemd-journal/209   /run/systemd/journal/stdout
UNIX 20653      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17684      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17687      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17774      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17777      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17876      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17879      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17895      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17898      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17915      systemd-journal/209   /run/systemd/journal/stdout
UNIX 17918      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18056      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18059      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18183      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18186      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18197      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18200      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18289      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18418      systemd-journal/209   /run/systemd/journal/stdout
UNIX 18421      systemd-journal/209   /run/systemd/journal/stdout
UNIX 20656      systemd-journal/209   /run/systemd/journal/stdout
UNIX 29471      systemd-journal/209   /run/systemd/journal/stdout
UNIX 9574         systemd-udevd/214   
UNIX 9574         systemd-udevd/214   
UNIX 9063         systemd-udevd/214   /run/udev/control
UNIX 9578         systemd-udevd/214   
UNIX 9618         systemd-udevd/214   
UNIX 9619         systemd-udevd/214   
UNIX 9330              rsyslogd/503   /run/systemd/journal/syslog
UNIX 11107          dbus-daemon/504   
UNIX 11107          dbus-daemon/504   
UNIX 11056          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 11182          dbus-daemon/504   
UNIX 11185          dbus-daemon/504   
UNIX 11186          dbus-daemon/504   
UNIX 11187          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 11558          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 11998          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12226          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12380          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12567          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12524          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12545          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 12581          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13004          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13078          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13345          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13349          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13529          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13599          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13650          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13652          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13653          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13656          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13677          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13679          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13681          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13686          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13690          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 13868          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 16293          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 16427          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 16796          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 16896          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17019          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17088          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17090          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17132          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 22410          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 14872          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 14907          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17148          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 14985          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18433          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17150          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17229          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 15617          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 15621          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17269          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17323          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18205          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 15893          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 16059          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17450          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17781          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17841          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17854          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17888          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17972          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17970          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 17984          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18016          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18078          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18109          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 18435          dbus-daemon/504   /var/run/dbus/system_bus_socket
UNIX 11245             whoopsie/512   
UNIX 11245             whoopsie/512   
UNIX 14906             whoopsie/512   
UNIX 12544             whoopsie/512   
UNIX 11410                 cron/515   
UNIX 11410                 cron/515   
UNIX 11480       systemd-logind/523   
UNIX 11480       systemd-logind/523   
UNIX 11545       systemd-logind/523   
UNIX 11557       systemd-logind/523   
UNIX 11529            cgmanager/526   
UNIX 11529            cgmanager/526   
UNIX 11538            cgmanager/526   /sys/fs/cgroup/cgmanager/sock
UNIX 11613                cupsd/531   
UNIX 11613                cupsd/531   
UNIX 11054                cupsd/531   /var/run/cups/cups.sock
UNIX 12379                cupsd/531   
TCP      ::1             :  631 ::              :    0 LISTEN                      cupsd/531  
TCP      127.0.0.1       :  631 0.0.0.0         :    0 LISTEN                      cupsd/531  
UNIX 11878         avahi-daemon/537   
UNIX 11878         avahi-daemon/537   
UNIX 11055         avahi-daemon/537   /var/run/avahi-daemon/socket
UNIX 11984         avahi-daemon/537   
UNIX 11985         avahi-daemon/537   
UNIX 11997         avahi-daemon/537   
UDP      0.0.0.0         : 5353 0.0.0.0         :    0                      avahi-daemon/537  
UDP      ::              : 5353 ::              :    0                      avahi-daemon/537  
UDP      0.0.0.0         :39389 0.0.0.0         :    0                      avahi-daemon/537  
UDP      ::              :37548 ::              :    0                      avahi-daemon/537  
UNIX 11977      accounts-daemon/538   
UNIX 11977      accounts-daemon/538   
UNIX 12225      accounts-daemon/538   
UNIX 11878         avahi-daemon/546   
UNIX 11878         avahi-daemon/546   
UNIX 11055         avahi-daemon/546   /var/run/avahi-daemon/socket
UNIX 11984         avahi-daemon/546   
UNIX 11986         avahi-daemon/546   
UNIX 12487         ModemManager/571   
UNIX 12522         ModemManager/571   
UNIX 12523         ModemManager/571   
UNIX 12441       NetworkManager/575   
UNIX 12441       NetworkManager/575   
UNIX 12557       NetworkManager/575   
UNIX 12565       NetworkManager/575   /var/run/NetworkManager/private
UNIX 12566       NetworkManager/575   
UNIX 12579       NetworkManager/575   
UNIX 13607       NetworkManager/575   /var/run/NetworkManager/private-dhcp
UNIX 13676                 dbus/579   
UNIX 13678                 dbus/580   
UNIX 13680                 dbus/581   
UNIX 13685                 dbus/582   
UNIX 13649                 dbus/583   
UNIX 13655                 dbus/584   
UNIX 13598                 dbus/585   
UNIX 13651                 dbus/587   
UNIX 13648                 dbus/588   
UNIX 13689                 dbus/589   
UNIX 12646                 sshd/605   
UNIX 12646                 sshd/605   
TCP      0.0.0.0         :   22 0.0.0.0         :    0 LISTEN                       sshd/605  
TCP      ::              :   22 ::              :    0 LISTEN                       sshd/605  
UNIX 13003              polkitd/627   
UNIX 17864              polkitd/627   
UNIX 13050         cups-browsed/629   
UNIX 13050         cups-browsed/629   
TCP      ::1             :33680 ::1             :  631 CLOSE_WAIT           cups-browsed/629  
TCP      ::1             :33682 ::1             :  631 CLOSE_WAIT           cups-browsed/629  
UNIX 13344         cups-browsed/629   
UDP      0.0.0.0         :  631 0.0.0.0         :    0                      cups-browsed/629  
UNIX 13348         cups-browsed/629   
UNIX 13077           kerneloops/638   
UNIX 13329               vsftpd/641   
UNIX 13329               vsftpd/641   
TCP      ::              :   21 ::              :    0 LISTEN                     vsftpd/641  
UNIX 13352                 ntpd/646   
UDP      0.0.0.0         :  123 0.0.0.0         :    0                              ntpd/646  
UDP      ::              :  123 ::              :    0                              ntpd/646  
UDP      127.0.0.1       :  123 0.0.0.0         :    0                              ntpd/646  
UDP      ::1             :  123 ::              :    0                              ntpd/646  
UDP      192.168.1.132   :  123 0.0.0.0         :    0                              ntpd/646  
UDP      fe80::a00:27ff:fe2e:90c7:  123 ::              :    0                              ntpd/646  
UNIX 13517       wpa_supplicant/650   
UNIX 13517       wpa_supplicant/650   
UNIX 13527       wpa_supplicant/650   
UNIX 13528       wpa_supplicant/650   
UNIX 13654             dhclient/653   
UDP      0.0.0.0         :   68 0.0.0.0         :    0                          dhclient/653  
UDP      0.0.0.0         :51344 0.0.0.0         :    0                          dhclient/653  
UDP      ::              :32527 ::              :    0                          dhclient/653  
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/668  
UNIX 13851              lightdm/737   
UNIX 13851              lightdm/737   
UNIX 13976              lightdm/737   
UNIX 13867              lightdm/737   
UNIX 13951                 Xorg/746   
UNIX 13952                 Xorg/746   /tmp/.X11-unix/X0
UNIX 13977                 Xorg/746   
UNIX 16669                 Xorg/746   
UNIX 16702                 Xorg/746   
UNIX 16809                 Xorg/746   
UNIX 16803                 Xorg/746   
UNIX 16815                 Xorg/746   
UNIX 16827                 Xorg/746   
UNIX 16871                 Xorg/746   
UNIX 16838                 Xorg/746   
UNIX 18654                 Xorg/746   
UNIX 17209                 Xorg/746   
UNIX 17247                 Xorg/746   
UNIX 17566                 Xorg/746   
UNIX 17735                 Xorg/746   
UNIX 17743                 Xorg/746   
UNIX 17962                 Xorg/746   
UNIX 17763                 Xorg/746   
UNIX 17975                 Xorg/746   
UNIX 18063                 Xorg/746   
UNIX 18065                 Xorg/746   
UNIX 18300                 Xorg/746   
UNIX 18405                 Xorg/746   
UNIX 13851              lightdm/821   
UNIX 14521              lightdm/821   
UNIX 16058              lightdm/821   
UNIX 14849         rtkit-daemon/887   
UNIX 14849         rtkit-daemon/887   
UNIX 14870         rtkit-daemon/887   
UNIX 14871         rtkit-daemon/887   
UDP      127.0.1.1       :   53 0.0.0.0         :    0                           dnsmasq/899  
TCP      127.0.1.1       :   53 0.0.0.0         :    0 LISTEN                    dnsmasq/899  
UNIX 14984              dnsmasq/899   
UNIX 14992              dnsmasq/899   
UNIX 15578              upowerd/1118  
UNIX 15578              upowerd/1118  
UNIX 15616              upowerd/1118  
UNIX 15620              upowerd/1118  
UNIX 15885               colord/1173  
UNIX 15885               colord/1173  
UNIX 15892               colord/1173  
UNIX 16160              systemd/1193  
UNIX 16160              systemd/1193  
UNIX 16176              systemd/1193  
UNIX 16194              systemd/1193  /run/user/1000/systemd/notify
UNIX 16195              systemd/1193  /run/user/1000/systemd/private
UNIX 16160             (sd-pam)/1194  
UNIX 16160             (sd-pam)/1194  
UNIX 16167             (sd-pam)/1194  
UNIX 16206      gnome-keyring-d/1208  /run/user/1000/keyring/control
UNIX 16561      gnome-keyring-d/1208  /run/user/1000/keyring/ssh
UNIX 16490      gnome-keyring-d/1208  
UNIX 16557      gnome-keyring-d/1208  
UNIX 16559      gnome-keyring-d/1208  /run/user/1000/keyring/pkcs11
UNIX 17548      gnome-keyring-d/1208  
UNIX 16291              upstart/1210  
UNIX 16292              upstart/1210  
UNIX 16331              upstart/1210  
UNIX 16436              upstart/1210  
UNIX 16385              upstart/1210  
UNIX 16439              upstart/1210  
UNIX 16440              upstart/1210  
UNIX 16330      upstart-udev-br/1302  
UNIX 16369          dbus-daemon/1308  
UNIX 16376          dbus-daemon/1308  
UNIX 16377          dbus-daemon/1308  
UNIX 16386          dbus-daemon/1308  
UNIX 16421          dbus-daemon/1308  
UNIX 16463          dbus-daemon/1308  
UNIX 16522          dbus-daemon/1308  
UNIX 16491          dbus-daemon/1308  
UNIX 16715          dbus-daemon/1308  
UNIX 16558          dbus-daemon/1308  
UNIX 16589          dbus-daemon/1308  
UNIX 16620          dbus-daemon/1308  
UNIX 16600          dbus-daemon/1308  
UNIX 16692          dbus-daemon/1308  
UNIX 16704          dbus-daemon/1308  
UNIX 16744          dbus-daemon/1308  
UNIX 16844          dbus-daemon/1308  
UNIX 16851          dbus-daemon/1308  
UNIX 16852          dbus-daemon/1308  
UNIX 16857          dbus-daemon/1308  
UNIX 16860          dbus-daemon/1308  
UNIX 16894          dbus-daemon/1308  
UNIX 16905          dbus-daemon/1308  
UNIX 17035          dbus-daemon/1308  
UNIX 16945          dbus-daemon/1308  
UNIX 16997          dbus-daemon/1308  
UNIX 17114          dbus-daemon/1308  
UNIX 17125          dbus-daemon/1308  
UNIX 17758          dbus-daemon/1308  
UNIX 17127          dbus-daemon/1308  
UNIX 17134          dbus-daemon/1308  
UNIX 17158          dbus-daemon/1308  
UNIX 18176          dbus-daemon/1308  
UNIX 17249          dbus-daemon/1308  
UNIX 17760          dbus-daemon/1308  
UNIX 17252          dbus-daemon/1308  
UNIX 17254          dbus-daemon/1308  
UNIX 17259          dbus-daemon/1308  
UNIX 17263          dbus-daemon/1308  
UNIX 17301          dbus-daemon/1308  
UNIX 18190          dbus-daemon/1308  
UNIX 18012          dbus-daemon/1308  
UNIX 17767          dbus-daemon/1308  
UNIX 17769          dbus-daemon/1308  
UNIX 17861          dbus-daemon/1308  
UNIX 17884          dbus-daemon/1308  
UNIX 17905          dbus-daemon/1308  
UNIX 17908          dbus-daemon/1308  
UNIX 17944          dbus-daemon/1308  
UNIX 17989          dbus-daemon/1308  
UNIX 17966          dbus-daemon/1308  
UNIX 18050          dbus-daemon/1308  
UNIX 18070          dbus-daemon/1308  
UNIX 18080          dbus-daemon/1308  
UNIX 18111          dbus-daemon/1308  
UNIX 18150          dbus-daemon/1308  
UNIX 18222          dbus-daemon/1308  
UNIX 18226          dbus-daemon/1308  
UNIX 18413          dbus-daemon/1308  
UNIX 18302          dbus-daemon/1308  
UNIX 18409          dbus-daemon/1308  
UNIX 18425          dbus-daemon/1308  
UNIX 18430          dbus-daemon/1308  
UNIX 18656          dbus-daemon/1308  
UNIX 20660          dbus-daemon/1308  
UNIX 18474          dbus-daemon/1308  
UNIX 22406          dbus-daemon/1308  
UNIX 16462      window-stack-br/1320  
UNIX 16483           bamfdaemon/1339  
UNIX 16486           bamfdaemon/1339  
UNIX 16588           bamfdaemon/1339  
UNIX 16660           bamfdaemon/1339  
UNIX 16668           bamfdaemon/1339  
UNIX 16691           bamfdaemon/1339  
UNIX 16505                gvfsd/1349  
UNIX 16508                gvfsd/1349  
UNIX 16521                gvfsd/1349  
UNIX 16599           gvfsd-fuse/1362  
UNIX 16420      upstart-dbus-br/1372  
UNIX 16425      upstart-dbus-br/1372  
UNIX 16593      at-spi-bus-laun/1375  
UNIX 16596      at-spi-bus-laun/1375  
UNIX 16619      at-spi-bus-laun/1375  
UNIX 16426      upstart-dbus-br/1382  
UNIX 16431      upstart-dbus-br/1382  
UNIX 16434      upstart-file-br/1385  
UNIX 16593          dbus-daemon/1395  
UNIX 16596          dbus-daemon/1395  
UNIX 16653          dbus-daemon/1395  
UNIX 16664          dbus-daemon/1395  
UNIX 16665          dbus-daemon/1395  
UNIX 16666          dbus-daemon/1395  
UNIX 16694          dbus-daemon/1395  
UNIX 16806          dbus-daemon/1395  
UNIX 16824          dbus-daemon/1395  
UNIX 17039          dbus-daemon/1395  
UNIX 18651          dbus-daemon/1395  
UNIX 17206          dbus-daemon/1395  
UNIX 17244          dbus-daemon/1395  
UNIX 17732          dbus-daemon/1395  
UNIX 17740          dbus-daemon/1395  
UNIX 17756          dbus-daemon/1395  
UNIX 17765          dbus-daemon/1395  
UNIX 18090          dbus-daemon/1395  
UNIX 18297          dbus-daemon/1395  
UNIX 18402          dbus-daemon/1395  
UNIX 16679      at-spi2-registr/1399  
UNIX 16682      at-spi2-registr/1399  
UNIX 16693      at-spi2-registr/1399  
UNIX 16701      at-spi2-registr/1399  
UNIX 16703      at-spi2-registr/1399  
UNIX 16714          ibus-daemon/1407  
UNIX 16720          ibus-daemon/1407  
UNIX 16793          ibus-daemon/1407  
UNIX 16854          ibus-daemon/1407  
UNIX 16859          ibus-daemon/1407  
UNIX 16924          ibus-daemon/1407  
UNIX 17023          ibus-daemon/1407  
UNIX 17452          ibus-daemon/1407  
UNIX 17993          ibus-daemon/1407  
UNIX 18133          ibus-daemon/1407  
UNIX 18309          ibus-daemon/1407  
UNIX 20599          ibus-daemon/1407  
UNIX 16743           ibus-dconf/1416  
UNIX 16775           ibus-dconf/1416  
UNIX 16795           ibus-dconf/1416  
UNIX 16805         ibus-ui-gtk3/1419  
UNIX 16808         ibus-ui-gtk3/1419  
UNIX 16839         ibus-ui-gtk3/1419  
UNIX 16858         ibus-ui-gtk3/1419  
UNIX 16837          hud-service/1423  
UNIX 16850          hud-service/1423  
UNIX 16944          hud-service/1423  
UNIX 16923          hud-service/1423  
UNIX 16950          hud-service/1423  
UNIX 16951          hud-service/1423  
UNIX 16952          hud-service/1423  
UNIX 16953          hud-service/1423  
UNIX 16823      unity-settings-/1425  
UNIX 16826      unity-settings-/1425  
UNIX 16855      unity-settings-/1425  
UNIX 16895      unity-settings-/1425  
UNIX 17326      unity-settings-/1425  
UNIX 17451      unity-settings-/1425  
UNIX 16802             ibus-x11/1428  
UNIX 16843             ibus-x11/1428  
UNIX 16853             ibus-x11/1428  
UNIX 16814               compiz/1433  
UNIX 16856               compiz/1433  
UNIX 17974               compiz/1433  
UNIX 17983               compiz/1433  
UNIX 18062               compiz/1433  
UNIX 18064               compiz/1433  
UNIX 18089               compiz/1433  
UNIX 18124               compiz/1433  
UNIX 18132               compiz/1433  
UNIX 18162               compiz/1433  
UNIX 16865        gnome-session/1439  
UNIX 16865        gnome-session/1439  
UNIX 16865        gnome-session/1439  
UNIX 17034        gnome-session/1439  
UNIX 17018        gnome-session/1439  
UNIX 17359        gnome-session/1439  
UNIX 17360        gnome-session/1439  /tmp/.ICE-unix/1439
UNIX 17730        gnome-session/1439  
UNIX 17600        gnome-session/1439  
UNIX 16870      unity-panel-ser/1446  
UNIX 16904      unity-panel-ser/1446  
UNIX 17038      unity-panel-ser/1446  
UNIX 16877        dconf-service/1462  
UNIX 16880        dconf-service/1462  
UNIX 16893        dconf-service/1462  
UNIX 16996      ibus-engine-sim/1477  
UNIX 17022      ibus-engine-sim/1477  
UNIX 17087      indicator-messa/1489  
UNIX 17113      indicator-messa/1489  
UNIX 17089      indicator-bluet/1490  
UNIX 18473      indicator-bluet/1490  
UNIX 17124      indicator-power/1491  
UNIX 17131      indicator-power/1491  
UNIX 17126      indicator-datet/1492  
UNIX 17149      indicator-datet/1492  
UNIX 17205      indicator-keybo/1496  
UNIX 17208      indicator-keybo/1496  
UNIX 17248      indicator-keybo/1496  
UNIX 17133      indicator-sound/1500  
UNIX 17147      indicator-sound/1500  
UNIX 17346      indicator-sound/1500  
UNIX 17243      indicator-print/1502  
UNIX 17246      indicator-print/1502  
UNIX 17262      indicator-print/1502  
UNIX 17454      indicator-print/1502  
UNIX 17449      indicator-print/1502  
UNIX 17157      indicator-sessi/1505  
UNIX 17228      indicator-sessi/1505  
UNIX 17251      indicator-appli/1514  
UNIX 17258      indicator-appli/1514  
UNIX 17162      evolution-sourc/1525  
UNIX 17165      evolution-sourc/1525  
UNIX 17253      evolution-sourc/1525  
UNIX 17268           pulseaudio/1549  
UNIX 17328           pulseaudio/1549  /run/user/1000/pulse/native
UNIX 17347           pulseaudio/1549  /run/user/1000/pulse/native
UNIX 17300           pulseaudio/1549  
UNIX 17305           pulseaudio/1549  
UNIX 17322           pulseaudio/1549  
UNIX 17325           pulseaudio/1549  /run/user/1000/pulse/native
UNIX 17565           pulseaudio/1549  
UNIX 17599           pulseaudio/1549  
UNIX 16865             nautilus/1585  
UNIX 16865             nautilus/1585  
UNIX 17764             nautilus/1585  
UNIX 17766             nautilus/1585  
UNIX 17961             nautilus/1585  
UNIX 17992             nautilus/1585  
UNIX 18157             nautilus/1585  
UNIX 18118             nautilus/1585  
UNIX 18072             nautilus/1585  
UNIX 16865      unity-fallback-/1587  
UNIX 16865      unity-fallback-/1587  
UNIX 17731      unity-fallback-/1587  
UNIX 17734      unity-fallback-/1587  
UNIX 17757      unity-fallback-/1587  
UNIX 16865      polkit-gnome-au/1588  
UNIX 16865      polkit-gnome-au/1588  
UNIX 17739      polkit-gnome-au/1588  
UNIX 17742      polkit-gnome-au/1588  
UNIX 17759      polkit-gnome-au/1588  
UNIX 17853      polkit-gnome-au/1588  
UNIX 20598      polkit-gnome-au/1588  
UNIX 16865            nm-applet/1590  
UNIX 16865            nm-applet/1590  
UNIX 17755            nm-applet/1590  
UNIX 17762            nm-applet/1590  
UNIX 17768            nm-applet/1590  
UNIX 17887            nm-applet/1590  
UNIX 17907            nm-applet/1590  
UNIX 17971            nm-applet/1590  
UNIX 17683      evolution-calen/1593  
UNIX 17686      evolution-calen/1593  
UNIX 17988      evolution-calen/1593  
UNIX 17773      gvfs-udisks2-vo/1610  
UNIX 17776      gvfs-udisks2-vo/1610  
UNIX 17780      gvfs-udisks2-vo/1610  
UNIX 17860      gvfs-udisks2-vo/1610  
UNIX 17839              udisksd/1613  
UNIX 17840              udisksd/1613  
UNIX 17875      gvfs-afc-volume/1623  
UNIX 17878      gvfs-afc-volume/1623  
UNIX 17883      gvfs-afc-volume/1623  
UNIX 17894      gvfs-mtp-volume/1629  
UNIX 17897      gvfs-mtp-volume/1629  
UNIX 17904      gvfs-mtp-volume/1629  
UNIX 17914      gvfs-gphoto2-vo/1637  
UNIX 17917      gvfs-gphoto2-vo/1637  
UNIX 17943      gvfs-gphoto2-vo/1637  
UNIX 17965             gconfd-2/1642  
UNIX 17969             gconfd-2/1642  
UNIX 17683      evolution-calen/1651  
UNIX 17686      evolution-calen/1651  
UNIX 18011      evolution-calen/1651  
UNIX 18015      evolution-calen/1651  
UNIX 17683      evolution-calen/1661  
UNIX 17686      evolution-calen/1661  
UNIX 18069      evolution-calen/1661  
UNIX 18077      evolution-calen/1661  
UNIX 16505          gvfsd-trash/1662  
UNIX 16508          gvfsd-trash/1662  
UNIX 18049          gvfsd-trash/1662  
UNIX 18073          gvfsd-trash/1662  
UNIX 18119          gvfsd-trash/1662  
UNIX 18125          gvfsd-trash/1662  
UNIX 18163          gvfsd-trash/1662  
UNIX 18055      evolution-addre/1667  
UNIX 18058      evolution-addre/1667  
UNIX 18079      evolution-addre/1667  
UNIX 18055      evolution-addre/1692  
UNIX 18058      evolution-addre/1692  
UNIX 18110      evolution-addre/1692  
UNIX 18108      evolution-addre/1692  
UNIX 16505           gvfsd-burn/1705  
UNIX 16508           gvfsd-burn/1705  
UNIX 18149           gvfsd-burn/1705  
UNIX 18158           gvfsd-burn/1705  
UNIX 18168      unity-scope-loa/1733  
UNIX 18171      unity-scope-loa/1733  
UNIX 18175      unity-scope-loa/1733  
UNIX 18182      zeitgeist-daemo/1740  
UNIX 18185      zeitgeist-daemo/1740  
UNIX 18189      zeitgeist-daemo/1740  
UNIX 18204      zeitgeist-daemo/1740  
UNIX 18182      zeitgeist-datah/1748  
UNIX 18185      zeitgeist-datah/1748  
UNIX 18225      zeitgeist-datah/1748  
UNIX 18196        zeitgeist-fts/1749  
UNIX 18199        zeitgeist-fts/1749  
UNIX 18221        zeitgeist-fts/1749  
UNIX 18284      gnome-terminal-/1776  
UNIX 18288      gnome-terminal-/1776  
UNIX 18296      gnome-terminal-/1776  
UNIX 18299      gnome-terminal-/1776  
UNIX 18301      gnome-terminal-/1776  
UNIX 18308      gnome-terminal-/1776  
UNIX 18306      gnome-terminal-/1776  
UNIX 18307      gnome-pty-helpe/1782  
UNIX 18307      gnome-pty-helpe/1782  
UNIX 16865      telepathy-indic/1795  
UNIX 16865      telepathy-indic/1795  
UNIX 18401      telepathy-indic/1795  
UNIX 18404      telepathy-indic/1795  
UNIX 18408      telepathy-indic/1795  
UNIX 18412      telepathy-indic/1795  
UNIX 18417      mission-control/1804  
UNIX 18420      mission-control/1804  
UNIX 18424      mission-control/1804  
UNIX 18429      mission-control/1804  
UNIX 18432      mission-control/1804  
UNIX 18434      mission-control/1804  
TCP      192.168.1.132   :37816 185.30.166.38   : 6697 ESTABLISHED                 irssi/1849 
UNIX 16865      update-notifier/1885  
UNIX 16865      update-notifier/1885  
UNIX 18650      update-notifier/1885  
UNIX 18653      update-notifier/1885  
UNIX 18655      update-notifier/1885  
UNIX 20652       gvfsd-metadata/1987  
UNIX 20655       gvfsd-metadata/1987  
UNIX 20659       gvfsd-metadata/1987  
UNIX 16865      deja-dup-monito/2040  
UNIX 16865      deja-dup-monito/2040  
UNIX 22405      deja-dup-monito/2040  
UNIX 22409      deja-dup-monito/2040  
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/2729 
TCP      ::              :   80 ::              :    0 LISTEN                    apache2/2730 
UNIX 24652                 sudo/2834  
UNIX 24655                 sudo/2834  
TCP      192.168.1.132   :   22 192.168.1.133   :58690 ESTABLISHED                  sshd/5491 
UNIX 29398                 sshd/5491  
UNIX 29454              systemd/5493  
UNIX 29454              systemd/5493  
UNIX 29462              systemd/5493  
UNIX 29477              systemd/5493  /run/user/0/systemd/notify
UNIX 29478              systemd/5493  /run/user/0/systemd/private
UNIX 29454             (sd-pam)/5494  
UNIX 29454             (sd-pam)/5494  
UNIX 29459             (sd-pam)/5494  
UNIX 29780                 sudo/5594  
UNIX 29783                 sudo/5594  
TCP      0.0.0.0         :    6 0.0.0.0         :    0 CLOSE                      system/5611 
TCP      0.0.0.0         :    6 0.0.0.0         :    0 CLOSE                      system/5611 
TCP      0.0.0.0         :    6 0.0.0.0         :    0 CLOSE                      system/5611 
```

Aquí ya podemos notar algo más raro y es uno de las últimas conexiones activas por TCP.

El proceso irssi PID 1849 parece tener una conexión TCP por el puerto 6697 a una ip externa 185.30.166.38

Esta conexión es una de las pocas que está relacionada con una IP externa y además el puerto 6697 suele estar relacionado con comunicaciones por IRC/TLS, lo que es normal teniendo en cuenta que el proceso irssi es un cliente para comunicaciones por IRC CLI. 

## Detalles sobre el proceso IRSSI

Para poder ver más detalladamente el uso de este proceso en memoria podemos mapearlo.

```bash
❯ python2 vol.py -f /home/kali/Downloads/dump-practica5 --profile=Linuxubuntu-kernel-4_2_0-16-generic-vol2x64 linux_proc_maps -p 1849
Volatility Foundation Volatility Framework 2.6.1
Offset             Pid      Name                 Start              End                Flags               Pgoff Major  Minor  Inode      File Path
------------------ -------- -------------------- ------------------ ------------------ ------ ------------------ ------ ------ ---------- ---------
0xffff880035b59b80     1849 irssi                0x0000000000400000 0x00000000004d9000 r-x                   0x0      8      1     923339 /usr/bin/irssi
0xffff880035b59b80     1849 irssi                0x00000000006d9000 0x00000000006da000 r--               0xd9000      8      1     923339 /usr/bin/irssi
0xffff880035b59b80     1849 irssi                0x00000000006da000 0x00000000006e7000 rw-               0xda000      8      1     923339 /usr/bin/irssi
0xffff880035b59b80     1849 irssi                0x00000000006e7000 0x00000000006e8000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00000000026b7000 0x0000000002864000 rw-                   0x0      0      0          0 [heap]
0xffff880035b59b80     1849 irssi                0x00007f6614000000 0x00007f6614021000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f6614021000 0x00007f6618000000 ---                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661a04b000 0x00007f661a04c000 ---                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661a04c000 0x00007f661a84c000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661a84c000 0x00007f661a84e000 r-x                   0x0      8      1     263068 /usr/lib/x86_64-linux-gnu/gconv/CP1252.so
0xffff880035b59b80     1849 irssi                0x00007f661a84e000 0x00007f661aa4d000 ---                0x2000      8      1     263068 /usr/lib/x86_64-linux-gnu/gconv/CP1252.so
0xffff880035b59b80     1849 irssi                0x00007f661aa4d000 0x00007f661aa4e000 r--                0x1000      8      1     263068 /usr/lib/x86_64-linux-gnu/gconv/CP1252.so
0xffff880035b59b80     1849 irssi                0x00007f661aa4e000 0x00007f661aa4f000 rw-                0x2000      8      1     263068 /usr/lib/x86_64-linux-gnu/gconv/CP1252.so
0xffff880035b59b80     1849 irssi                0x00007f661aa4f000 0x00007f661b131000 r--                   0x0      8      1       7694 /usr/lib/locale/locale-archive
0xffff880035b59b80     1849 irssi                0x00007f661b131000 0x00007f661b19d000 r-x                   0x0      8      1     923111 /lib/x86_64-linux-gnu/libpcre.so.3.13.1
0xffff880035b59b80     1849 irssi                0x00007f661b19d000 0x00007f661b39c000 ---               0x6c000      8      1     923111 /lib/x86_64-linux-gnu/libpcre.so.3.13.1
0xffff880035b59b80     1849 irssi                0x00007f661b39c000 0x00007f661b39d000 r--               0x6b000      8      1     923111 /lib/x86_64-linux-gnu/libpcre.so.3.13.1
0xffff880035b59b80     1849 irssi                0x00007f661b39d000 0x00007f661b39e000 rw-               0x6c000      8      1     923111 /lib/x86_64-linux-gnu/libpcre.so.3.13.1
0xffff880035b59b80     1849 irssi                0x00007f661b39e000 0x00007f661b3a7000 r-x                   0x0      8      1     923002 /lib/x86_64-linux-gnu/libcrypt-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b3a7000 0x00007f661b5a6000 ---                0x9000      8      1     923002 /lib/x86_64-linux-gnu/libcrypt-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b5a6000 0x00007f661b5a7000 r--                0x8000      8      1     923002 /lib/x86_64-linux-gnu/libcrypt-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b5a7000 0x00007f661b5a8000 rw-                0x9000      8      1     923002 /lib/x86_64-linux-gnu/libcrypt-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b5a8000 0x00007f661b5d6000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661b5d6000 0x00007f661b6dd000 r-x                   0x0      8      1     923054 /lib/x86_64-linux-gnu/libm-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b6dd000 0x00007f661b8dc000 ---              0x107000      8      1     923054 /lib/x86_64-linux-gnu/libm-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b8dc000 0x00007f661b8dd000 r--              0x106000      8      1     923054 /lib/x86_64-linux-gnu/libm-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b8dd000 0x00007f661b8de000 rw-              0x107000      8      1     923054 /lib/x86_64-linux-gnu/libm-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b8de000 0x00007f661b8e1000 r-x                   0x0      8      1     923011 /lib/x86_64-linux-gnu/libdl-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661b8e1000 0x00007f661bae0000 ---                0x3000      8      1     923011 /lib/x86_64-linux-gnu/libdl-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bae0000 0x00007f661bae1000 r--                0x2000      8      1     923011 /lib/x86_64-linux-gnu/libdl-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bae1000 0x00007f661bae2000 rw-                0x3000      8      1     923011 /lib/x86_64-linux-gnu/libdl-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bae2000 0x00007f661bca2000 r-x                   0x0      8      1     922992 /lib/x86_64-linux-gnu/libc-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bca2000 0x00007f661bea2000 ---              0x1c0000      8      1     922992 /lib/x86_64-linux-gnu/libc-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bea2000 0x00007f661bea6000 r--              0x1c0000      8      1     922992 /lib/x86_64-linux-gnu/libc-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bea6000 0x00007f661bea8000 rw-              0x1c4000      8      1     922992 /lib/x86_64-linux-gnu/libc-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661bea8000 0x00007f661beac000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661beac000 0x00007f661bed1000 r-x                   0x0      8      1     923154 /lib/x86_64-linux-gnu/libtinfo.so.5.9
0xffff880035b59b80     1849 irssi                0x00007f661bed1000 0x00007f661c0d0000 ---               0x25000      8      1     923154 /lib/x86_64-linux-gnu/libtinfo.so.5.9
0xffff880035b59b80     1849 irssi                0x00007f661c0d0000 0x00007f661c0d4000 r--               0x24000      8      1     923154 /lib/x86_64-linux-gnu/libtinfo.so.5.9
0xffff880035b59b80     1849 irssi                0x00007f661c0d4000 0x00007f661c0d5000 rw-               0x28000      8      1     923154 /lib/x86_64-linux-gnu/libtinfo.so.5.9
0xffff880035b59b80     1849 irssi                0x00007f661c0d5000 0x00007f661c2f1000 r-x                   0x0      8      1     923004 /lib/x86_64-linux-gnu/libcrypto.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c2f1000 0x00007f661c4f0000 ---              0x21c000      8      1     923004 /lib/x86_64-linux-gnu/libcrypto.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c4f0000 0x00007f661c50e000 r--              0x21b000      8      1     923004 /lib/x86_64-linux-gnu/libcrypto.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c50e000 0x00007f661c51a000 rw-              0x239000      8      1     923004 /lib/x86_64-linux-gnu/libcrypto.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c51a000 0x00007f661c51e000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661c51e000 0x00007f661c57c000 r-x                   0x0      8      1     923148 /lib/x86_64-linux-gnu/libssl.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c57c000 0x00007f661c77c000 ---               0x5e000      8      1     923148 /lib/x86_64-linux-gnu/libssl.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c77c000 0x00007f661c780000 r--               0x5e000      8      1     923148 /lib/x86_64-linux-gnu/libssl.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c780000 0x00007f661c787000 rw-               0x62000      8      1     923148 /lib/x86_64-linux-gnu/libssl.so.1.0.0
0xffff880035b59b80     1849 irssi                0x00007f661c787000 0x00007f661c894000 r-x                   0x0      8      1     923029 /lib/x86_64-linux-gnu/libglib-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661c894000 0x00007f661ca93000 ---              0x10d000      8      1     923029 /lib/x86_64-linux-gnu/libglib-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661ca93000 0x00007f661ca94000 r--              0x10c000      8      1     923029 /lib/x86_64-linux-gnu/libglib-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661ca94000 0x00007f661ca95000 rw-              0x10d000      8      1     923029 /lib/x86_64-linux-gnu/libglib-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661ca95000 0x00007f661ca96000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661ca96000 0x00007f661ca99000 r-x                   0x0      8      1      10472 /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661ca99000 0x00007f661cc98000 ---                0x3000      8      1      10472 /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661cc98000 0x00007f661cc99000 r--                0x2000      8      1      10472 /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661cc99000 0x00007f661cc9a000 rw-                0x3000      8      1      10472 /usr/lib/x86_64-linux-gnu/libgmodule-2.0.so.0.4600.1
0xffff880035b59b80     1849 irssi                0x00007f661cc9a000 0x00007f661ccb2000 r-x                   0x0      8      1     923128 /lib/x86_64-linux-gnu/libpthread-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661ccb2000 0x00007f661ceb2000 ---               0x18000      8      1     923128 /lib/x86_64-linux-gnu/libpthread-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661ceb2000 0x00007f661ceb3000 r--               0x18000      8      1     923128 /lib/x86_64-linux-gnu/libpthread-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661ceb3000 0x00007f661ceb4000 rw-               0x19000      8      1     923128 /lib/x86_64-linux-gnu/libpthread-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661ceb4000 0x00007f661ceb8000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661ceb8000 0x00007f661d065000 r-x                   0x0      8      1      10830 /usr/lib/x86_64-linux-gnu/libperl.so.5.20.2
0xffff880035b59b80     1849 irssi                0x00007f661d065000 0x00007f661d264000 ---              0x1ad000      8      1      10830 /usr/lib/x86_64-linux-gnu/libperl.so.5.20.2
0xffff880035b59b80     1849 irssi                0x00007f661d264000 0x00007f661d269000 r--              0x1ac000      8      1      10830 /usr/lib/x86_64-linux-gnu/libperl.so.5.20.2
0xffff880035b59b80     1849 irssi                0x00007f661d269000 0x00007f661d26d000 rw-              0x1b1000      8      1      10830 /usr/lib/x86_64-linux-gnu/libperl.so.5.20.2
0xffff880035b59b80     1849 irssi                0x00007f661d26d000 0x00007f661d291000 r-x                   0x0      8      1     922964 /lib/x86_64-linux-gnu/ld-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661d44c000 0x00007f661d472000 r--                   0x0      8      1     276310 /usr/share/locale-langpack/es/LC_MESSAGES/libc.mo
0xffff880035b59b80     1849 irssi                0x00007f661d472000 0x00007f661d479000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661d486000 0x00007f661d487000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661d487000 0x00007f661d48e000 r--                   0x0      8      1     263305 /usr/lib/x86_64-linux-gnu/gconv/gconv-modules.cache
0xffff880035b59b80     1849 irssi                0x00007f661d48e000 0x00007f661d490000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007f661d490000 0x00007f661d491000 r--               0x23000      8      1     922964 /lib/x86_64-linux-gnu/ld-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661d491000 0x00007f661d492000 rw-               0x24000      8      1     922964 /lib/x86_64-linux-gnu/ld-2.21.so
0xffff880035b59b80     1849 irssi                0x00007f661d492000 0x00007f661d493000 rw-                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007ffed4615000 0x00007ffed4637000 rw-                   0x0      0      0          0 [stack]
0xffff880035b59b80     1849 irssi                0x00007ffed47b4000 0x00007ffed47b6000 r--                   0x0      0      0          0 
0xffff880035b59b80     1849 irssi                0x00007ffed47b6000 0x00007ffed47b8000 r-x                   0x0      0      0          0 [vdso]
```

Aquí encontramos varios elementos clave para determinar que se trata de este proceso.

1. El proceso está usando librerías de criptografía y ssl, confirmando que se realizan comunicaciones cifradas.

```bash
/lib/x86_64-linux-gnu/libcrypto.so.1.0.0
/lib/x86_64-linux-gnu/libssl.so.1.0.0
```

2. Tiene cargadas librerías para manejo de sockets y red.

```bash
/lib/x86_64-linux-gnu/libpthread-2.21.so
/lib/x86_64-linux-gnu/libc-2.21.so
```

3. Tiene cargada una librería para soporte de Perl.

```bash
/usr/lib/x86_64-linux-gnu/libperl.so.5.20.2
```

Esto es particularmente sospechoso porque significa que el proceso puede ejecutar scripts Perl, que es una capacidad comúnmente usada en malware basado en IRC para ejecutar comandos o payloads adicionales.

## Conclusión

Si combinamos esto con la conexión establecida que encontramos antes:

- Conexión cifrada al puerto 6697 (IRC sobre SSL)
- Capacidad de ejecución de scripts Perl
- Conexión persistente a una IP externa

Todo apunta a que este proceso podría estar siendo usado como un bot IRC o un canal de comando y control (C2). Los atacantes frecuentemente usan clientes IRC legítimos como IRSSI modificados para mantener persistencia y control remoto en sistemas comprometidos.

# Parte 2

Para esta sección vamos a analizar una imagen post-mortem de un disco.

Se nos pide analizar el contenido de la imagen y determinar las posibles acciones llevadas a cabo por un atacante. 

Según el administrador de sistemas solo los puertos 21, 22, 23, 3306, 123 estaban abiertos en la máquina, algunos de los cuales son utilizados por él para realizar el mantenimiento del sistema.

Antes de comenzar, aclarar que para esta parte del análisis vamos a utilizar un sistema windows 11 con las herrameintas correspondientes, se puede realizar igual en linux pero para cambiar un poco el sistema operativo y mostrar otras herrameintas y opciones.

## Key analisis 

- Sistema operativo: Linux
- Fecha del incidente: 5 de abril de 2022
- Puertos legítimos abiertos: 21 (FTP), 22 (SSH), 23 (Telnet), 3306 (MySQL), 123 (NTP)

    - Objetivos de investigación:

    - Identificar usuarios no autorizados
    - Detectar malware
    - Encontrar archivos comprometidos
    - Identificar puertos no autorizados
    - Detectar tareas programadas maliciosas

## FTK Imager 

Para empezar abrimos la imagen de disco mediante FTK imager y, aunque no es necesario para su análisis desde FTK, vamos a montar la imagen en una unidad de virtual de solo lectura para que, aprovechando las
últimas mejoras de compatibilidad en powershell con w11 podamos navegar por el disco con comandos similares o nativos de Linux y así poder realizar un análisis más CLI.

![alt text](/assets/img/posts/reto-atenea-linux/image-6.png)

## Análisis de usuarios

Comenzamos listando los archivos passwd y shadow para visualizar posibles usuarios no legítimos.

![alt text](/assets/img/posts/reto-atenea-linux/image-7.png)

Como vemos el intruso no ha sido muy creativo o no ha puesto demasiado empeño en camuflarse, tenemos un usuario que parece que, además de ser el último agregado tiene un nombre potencialmente sospechoso.

Si volcamos el contenido de shadow podemos ver que únicamente tenemos el hash del usuario centosforensics y root.

![alt text](/assets/img/posts/reto-atenea-linux/image-8.png)

Además observamos también el último cambio de contraseña fue posterior a los "legítimos" usuarios del sistema mientras que ellos tienen 19444 el usuario sospechoso es posterior 19470.

## Auth & Secure logs 

Buscando en estos ficheros /var/log observamos que se ha realizado un ataque de fuerza bruta por SSH desde la misma ip, sin conocimiento de los usuarios.

Observando el fichero secure.log

![alt text](/assets/img/posts/reto-atenea-linux/image-9.png)

El actor parece haber utilizado algún diccionario de usuarios para verificar que usuarios existen en el sistema.

Ahora desde FTK vamos a visualizar más facilmente el registro de estos archivos secure.

![alt text](/assets/img/posts/reto-atenea-linux/image-10.png)

Observamos que tienen fechas de registro y además uno parece estar eliminado. Comprobando de forma cronológica los archivos parece indicar que el proceso de intrusión fue realizado entre los meses de marzo, abril y mayo.

El 19 de Marzo se crearon usuarios de servicios, lo que indica que parecen ser legítimos siempre y cuando tengamos en cuenta que es un laboratorio por lo que tiene sentido que el sistema fuese configurado poco antes de ser vulnerado.

![alt text](/assets/img/posts/reto-atenea-linux/image-11.png)

Toda la configuración del sistema parece continuar hasta el 28 de Marzo.

![alt text](/assets/img/posts/reto-atenea-linux/image-12.png)

Desde esta fecha hasta el 7 de Abril se registran lo que parecen logs de administración legítimos por parte del administrador de sistemas. 

No es hasta el 23 de Abril que encontramos el primer rastro inusual, empezando este mismo día sobre las 10:33 AM el ataque de fuerza bruta sobre el protocolo SSH.

![alt text](/assets/img/posts/reto-atenea-linux/image-13.png)

El atacante comienza el ataque con lo que parece un diccionario de usuarios para poder encontrar los posibles usuarios registrados en el sistema.

Como veremos desde el inicio hasta el fin la IP registrada para el ataque de fuerza bruta parece ser la misma 192.168.56.1 lo que indica que el ataque tuvo que ser realizado desde un máquina en la misma red local del objetivo.

Esto podría indicar que el atacante consiguió acceso a un equipo dentro de la red local de la infraestructura desde el que realizó estos ataques.

Cabe destacar que el fichero donde se encuentra el principio de este ataque es el que fue "eliminado" y es el de mayor tamaño. Contiene todo el registro de fallos de autenticación desde las 10:33 hasta las 11:23 AM

![alt text](/assets/img/posts/reto-atenea-linux/image-14.png)

En el siguiente fichero observamos la continuación del proceso. Misma fecha y hora cercana a la del anterior registro vemos como el atacante parece haber encontrado los potenciales usuarios registrados en el sistema.

Podemos verificar que estos usuarios estaban registrados antes del ataque y además que se tratan de los que el atacante ahora intenta conectarse al sistema mediante un diccionario de contraseñas.

Parece que el atacante únicamente intenta con los usuarios richard, john y root.

![alt text](/assets/img/posts/reto-atenea-linux/image-15.png)

Poco más adelante añade al ataque el usuario admin.

![alt text](/assets/img/posts/reto-atenea-linux/image-16.png)

No es hasta las 11:50 AM que el atacante consigue entrar al sistema como el usuario root y rápidamente crea un usuario nuevo llamado ghostHacker en el sistema y sale del usuario root.

![alt text](/assets/img/posts/reto-atenea-linux/image-17.png)

Al día siguiente 24 de Abril sobre las 10:30 el atacante se intenta conectar de nuevo desde una nueva IP con un nombre de usuario erroneo.

![alt text](/assets/img/posts/reto-atenea-linux/image-18.png)

Durante los siguientes 30 minutos realiza varias conexiones como root en el sistema.

A partir de este punto durante los proximos días de Abril y Mayo solo parecen iniciarse varias sesiónes como root desde diferentes IPs.

El último registro de estos logs es el 17 de Mayo.

## Analizando el usuario root

Como vimos que el metodo de entrada al sistema fue un ataque de fuerza bruta por SSH y el usuario que sirvió como punto de entrada fue root vamos a comprobar que podemos averiguar sobre él.

![alt text](/assets/img/posts/reto-atenea-linux/image-19.png)

Como vemos el historial de comandos para root ha sido vaciado y el último comando registrado es exit.

En la carpeta del usuario root parece que hay un keylogger escrito en python. 

![alt text](/assets/img/posts/reto-atenea-linux/image-20.png)

En efecto podemos ver como en los archivos cron se ha añadido una entrada que inicia el keylogger con el sistema en segundo plano. 

![alt text](/assets/img/posts/reto-atenea-linux/image-21.png)

## Servicios

Para comprobar si el atacante abrió algún puerto en el sistema primero debemos tener en cuenta los que ya se encontraban abiertos según el administrador.

Estos eran 21, 22, 23, 3306, 123.

Primero vamos a comprobar los archivos de configuración del firewall en la ruta /etc/firewalld/zones

En este podemos ver dos archivos en los que efectivamente podemos observar un cambio en los puertos abiertos.

![alt text](/assets/img/posts/reto-atenea-linux/image-22.png)

![alt text](/assets/img/posts/reto-atenea-linux/image-23.png)

Sabiendo esto podemos dirigirnos a /etc/services y comprobarlo.

El puerto parece que pertenece al protocolo Kerberos.

![alt text](/assets/img/posts/reto-atenea-linux/image-24.png)

## Posible acceso a archivos confidenciales

En la imagen de disco vemos que existe una carpeta comprimida y un directorio en /mnt con archivos de la empresa.

Entre ellos se encuentran proyectos y contratos a los que ha podido tener acceso el atacante. 

Para obtener una posible linea temporal de estos ficheros hemos analizado el directorio con un software llamado "mac-robber".

Necesitamos montar la imagen de la evidencia en linux y realizar lo siguiente:

![alt text](/assets/img/posts/reto-atenea-linux/image-25.png)

![alt text](/assets/img/posts/reto-atenea-linux/image-26.png)

![alt text](/assets/img/posts/reto-atenea-linux/image-27.png)

Esas últimas fechas de acceso son posteriores a la intrusión lo que pueden indicar que han sido consultados por el atacante.
