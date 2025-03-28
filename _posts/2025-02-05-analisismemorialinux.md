---
title: Análisis básico de memoria RAM en Linux
date: 2025-02-05 14:00:00 -0000
categories: [Forense, Linux]
tags: [Forense, memoria ram, linux, dump, memdump, fmem, LiME, avml]
description: >
  Repaso y guía rapida de algunos comandos para realizar análisis de memoria RAM en Linux.
pin: false  
toc: true   
math: false 
mermaid: false 
---


# Diferencia entre Linux y Windows

Como comentabamos en la [sección anterior ](https://sproffes.github.io/posts/memorydumpslinux/) sobre el análisis de memoria RAM en linux, a diferencia de windows la disposción de los elementos de la memoria RAM es diferente dependiendo del kernel y la versión base de linux que el sistema esté utilizando.


En esta sección vamos a dentrarnos en el análisis "básico" de la memoria RAM en linux pero sin indagar en lso detalles de mapeo según la versión de linux que esté utilizando.

Para ello os recomiendo visitar el post donde explicamos más profundamente el método para crear nuestro propios mapas de memoria RAM en linux.

# Preparación

## Instalación de Volatility 3

```bash
git clone https://github.com/volatilityfoundation/volatility3.git

sudo apt install -y python3-pip

cd volatility3

python3 vol.py -h
```

## Instalción de Volatility 2

```bash
sudo apt update

sudo apt install python2.7 python2.7-dev python3 git -y

git clone https://github.com/volatilityfoundation/volatility.git

wget https://bootstrap.pypa.io/pip/2.7/get-pip.py

sudo python2.7 get-pip.py

pip2 install distorm3 yara-python pycrypto

cd volatility/

python2 vol.py -h OR python2.7 vol.py -h
```

## Dump de memoria RAM

Para esta sección el dump de memoria utilizado es el siguiente:

[Google Drive](https://drive.google.com/file/d/1CyqiIkxw4tHdL6OB38frX6idKMluitct/view?usp=share_link)

[Perfil para Volatility 2](https://drive.google.com/file/d/1bMbvUi50zUsxfeNgt5jT50eduAl7N5es/view?usp=share_link)

[Perfil para Volatility 3](https://drive.google.com/file/d/16BgoOSZ6B717IW4iYJbYa7aAZfudbT-5/view?usp=share_link)

Vamos a comenzar con Volatility 2.

# Volatility 2

Como ya indicamos anteriormente en esta sección vamos a omitir la selección y extracción de mapas de memoria vamos a asumir que ya realizamos ese proceso.

Asumiendo lo anterior y con el mapa de memoria RAM ubicado en /volatility/plugins/overlays/linux/debian-XXXX-memmap.zip, continuamos con la ejecución del vol.py

```bash
python2 vol.py --info

Linuxdebian10-4_19_0-23-686x86
```

Nos indicará qué mapas tenemos cargados.

![alt text](/assets/img/posts/analisismemorialinux/image.png)

## Análisis de procesos

### linux_pslist

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_pslist
```

```bash
Offset     Name                 Pid             PPid            Uid             Gid    DTB        Start Time
---------- -------------------- --------------- --------------- --------------- ------ ---------- ----------
0xf491cb40 systemd              1               0               0               0      0x34a8e000 0
0xf4918ac0 kthreadd             2               0               0               0      ---------- 0
0xf4919580 rcu_gp               3               2               0               0      ---------- 0
0xf491b5c0 rcu_par_gp           4               2               0               0      ---------- 0
0xf4918000 kworker/0:0H         6               2               0               0      ---------- 0
0xf491a040 mm_percpu_wq         8               2               0               0      ---------- 0
0xf491e0c0 ksoftirqd/0          9               2               0               0      ---------- 0
0xf491eb80 rcu_sched            10              2               0               0      ---------- 0
0xf491ab00 rcu_bh               11              2               0               0      ---------- 0
0xf493cb40 migration/0          12              2               0               0      ---------- 0
0xf493b5c0 cpuhp/0              14              2               0               0      ---------- 0
0xf493c080 cpuhp/1              15              2               0               0      ---------- 0
0xf4938000 migration/1          16              2               0               0      ---------- 0
0xf493d600 ksoftirqd/1          17              2               0               0      ---------- 0
0xf493e0c0 kworker/1:0H         19              2               0               0      ---------- 0
0xf493eb80 kdevtmpfs            20              2               0               0      ---------- 0
0xf493ab00 netns                21              2               0               0      ---------- 0
0xf49c8000 kauditd              22              2               0               0      ---------- 0
0xf49cd600 khungtaskd           23              2               0               0      ---------- 0
0xf49ca040 oom_reaper           24              2               0               0      ---------- 0
0xf49ce0c0 writeback            25              2               0               0      ---------- 0
0xf49ceb80 kcompactd0           26              2               0               0      ---------- 0
0xf49cab00 ksmd                 27              2               0               0      ---------- 0
0xf49ccb40 khugepaged           28              2               0               0      ---------- 0
0xf49c8ac0 crypto               29              2               0               0      ---------- 0
0xf49c9580 kintegrityd          30              2               0               0      ---------- 0
0xf49cb5c0 kblockd              31              2               0               0      ---------- 0
0xf49cc080 edac-poller          32              2               0               0      ---------- 0
0xf4a50ac0 devfreq_wq           33              2               0               0      ---------- 0
0xf4a51580 watchdogd            34              2               0               0      ---------- 0
0xf4a54080 kswapd0              36              2               0               0      ---------- 0
0xf4be8ac0 kthrotld             54              2               0               0      ---------- 0
0xf4beab00 ipv6_addrconf        55              2               0               0      ---------- 0
0xf64a2040 kstrp                65              2               0               0      ---------- 0
0xf4beeb80 ata_sff              101             2               0               0      ---------- 0
0xf4a560c0 scsi_eh_0            102             2               0               0      ---------- 0
0xf4be8000 scsi_eh_1            103             2               0               0      ---------- 0
0xf4becb40 scsi_tmf_1           104             2               0               0      ---------- 0
0xf4beb5c0 scsi_eh_2            105             2               0               0      ---------- 0
0xf64b4b40 scsi_tmf_2           106             2               0               0      ---------- 0
0xf4a55600 scsi_tmf_0           108             2               0               0      ---------- 0
0xf6664080 kworker/1:1H         113             2               0               0      ---------- 0
0xf6662b00 kworker/0:2          136             2               0               0      ---------- 0
0xf6666b80 kworker/0:1H         138             2               0               0      ---------- 0
0xf6660ac0 kworker/u5:0         166             2               0               0      ---------- 0
0xf6664b40 jbd2/sda1-8          168             2               0               0      ---------- 0
0xf6660000 ext4-rsv-conver      169             2               0               0      ---------- 0
0xf4a52040 systemd-journal      202             1               0               0      0x35d40000 0
0xf5d0c080 systemd-udevd        219             1               0               0      0x35dc0000 0
0xf5d09580 systemd-timesyn      241             1               101             102    0x35f70000 0
0xf5d08000 ttm_swap             262             2               0               0      ---------- 0
0xf5d0b5c0 irq/18-vmwgfx        263             2               0               0      ---------- 0
0xf64a1580 systemd-logind       330             1               0               0      0x35915000 0
0xf64a6b80 rsyslogd             332             1               0               0      0x35914000 0
0xf64a2b00 dbus-daemon          335             1               104             110    0x35e7a000 0
0xf64a60c0 cron                 339             1               0               0      0x33870000 0
0xf38eab00 dhclient             348             1               0               0      0x35b27000 0
0xf64a0000 sshd                 350             1               0               0      0x34b8f000 0
0xf64a4b40 login                351             1               0               0      0x339ba000 0
0xf5d0ab00 systemd              374             1               0               0      0x33b1a000 0
0xf5d08ac0 (sd-pam)             375             374             0               0      0x33b0e000 0
0xf64a35c0 bash                 385             351             0               0      0x33bf4000 0
0xf5d0d600 sshd                 392             350             0               0      0x3347e000 0
0xf64a5600 systemd              395             1               1000            1000   0x33843000 0
0xf4a52b00 (sd-pam)             396             395             1000            1000   0x3349c000 0
0xf3561580 sshd                 409             392             1000            1000   0x33592000 0
0xf35660c0 bash                 410             409             1000            1000   0x33466000 0
0xf327a040 su                   606             410             1000            1000   0x33753000 0
0xf3560000 bash                 607             606             0               0      0x33727000 0
0xf4a56b80 kworker/u4:0         633             2               0               0      ---------- 0
0xf4938ac0 kworker/0:1          8912            2               0               0      ---------- 0
0xf4a50000 kworker/1:0          10483           2               0               0      ---------- 0
0xf4a535c0 kworker/u4:2         10538           2               0               0      ---------- 0
0xf493a040 kworker/1:1          10585           2               0               0      ---------- 0
0xf6665600 kworker/u4:1         10597           2               0               0      ---------- 0
0xf66635c0 kworker/1:2          10603           2               0               0      ---------- 0
0xf3440000 insmod               11218           607             0               0      0x3633d000 0
```


### linux_psaux

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_pslist
```

```bash
Pid    Uid    Gid    Arguments                                                       
1      0      0      /sbin/init                                                      
2      0      0      [kthreadd]                                                      
3      0      0      [rcu_gp]                                                        
4      0      0      [rcu_par_gp]                                                    
6      0      0      [kworker/0:0H]                                                  
8      0      0      [mm_percpu_wq]                                                  
9      0      0      [ksoftirqd/0]                                                   
10     0      0      [rcu_sched]                                                     
11     0      0      [rcu_bh]                                                        
12     0      0      [migration/0]                                                   
14     0      0      [cpuhp/0]                                                       
15     0      0      [cpuhp/1]                                                       
16     0      0      [migration/1]                                                   
17     0      0      [ksoftirqd/1]                                                   
19     0      0      [kworker/1:0H]                                                  
20     0      0      [kdevtmpfs]                                                     
21     0      0      [netns]                                                         
22     0      0      [kauditd]                                                       
23     0      0      [khungtaskd]                                                    
24     0      0      [oom_reaper]                                                    
25     0      0      [writeback]                                                     
26     0      0      [kcompactd0]                                                    
27     0      0      [ksmd]                                                          
28     0      0      [khugepaged]                                                    
29     0      0      [crypto]                                                        
30     0      0      [kintegrityd]                                                   
31     0      0      [kblockd]                                                       
32     0      0      [edac-poller]                                                   
33     0      0      [devfreq_wq]                                                    
34     0      0      [watchdogd]                                                     
36     0      0      [kswapd0]                                                       
54     0      0      [kthrotld]                                                      
55     0      0      [ipv6_addrconf]                                                 
65     0      0      [kstrp]                                                         
101    0      0      [ata_sff]                                                       
102    0      0      [scsi_eh_0]                                                     
103    0      0      [scsi_eh_1]                                                     
104    0      0      [scsi_tmf_1]                                                    
105    0      0      [scsi_eh_2]                                                     
106    0      0      [scsi_tmf_2]                                                    
108    0      0      [scsi_tmf_0]                                                    
113    0      0      [kworker/1:1H]                                                  
136    0      0      [kworker/0:2]                                                   
138    0      0      [kworker/0:1H]                                                  
166    0      0      [kworker/u5:0]                                                  
168    0      0      [jbd2/sda1-8]                                                   
169    0      0      [ext4-rsv-conver]                                               
202    0      0      /lib/systemd/systemd-journald                                   
219    0      0      /lib/systemd/systemd-udevd                                      
241    101    102    /lib/systemd/systemd-timesyncd                                  
262    0      0      [ttm_swap]                                                      
263    0      0      [irq/18-vmwgfx]                                                 
330    0      0      /lib/systemd/systemd-logind                                     
332    0      0      /usr/sbin/rsyslogd -n -iNONE                                    
335    104    110    /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
339    0      0      /usr/sbin/cron -f                                               
348    0      0      /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3
350    0      0                                                                      
351    0      0                                                                      
374    0      0      /lib/systemd/systemd --user                                     
375    0      0      (sd-pam)                                                        
385    0      0      -bash                                                           
392    0      0      sshd: usuario [priv]                                            
395    1000   1000   /lib/systemd/systemd --user                                     
396    1000   1000   (sd-pam)                                                        
409    1000   1000                                                                   
410    1000   1000                                                                   
606    1000   1000                                                                   
607    0      0      -bash                                                           
633    0      0      [kworker/u4:0]                                                  
8912   0      0      [kworker/0:1]                                                   
10483  0      0      [kworker/1:0]                                                   
10538  0      0      [kworker/u4:2]                                                  
10585  0      0      [kworker/1:1]                                                   
10597  0      0      [kworker/u4:1]                                                  
10603  0      0      [kworker/1:2]                                                   
11218  0      0      insmod lime-4.19.0-23-686.ko path=ram.lime format=lime 
```

### linux_pstree

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_pstree
```
```bash
Name                 Pid             Uid            
systemd              1                              
.systemd-journal     202                            
.systemd-udevd       219                            
.systemd-timesyn     241             101            
.systemd-logind      330                            
.rsyslogd            332                            
.dbus-daemon         335             104            
.cron                339                            
.sshd                350                            
..sshd               392                            
...sshd              409             1000           
....bash             410             1000           
.....su              606             1000           
......bash           607                            
.......insmod        11218                          
.login               351                            
..bash               385                            
.dhclient            348                            
.systemd             374                            
..(sd-pam)           375                            
.systemd             395             1000           
..(sd-pam)           396             1000           
[kthreadd]           2                              
.[rcu_gp]            3                              
.[rcu_par_gp]        4                              
.[kworker/0:0H]      6                              
.[mm_percpu_wq]      8                              
.[ksoftirqd/0]       9                              
.[rcu_sched]         10                             
.[rcu_bh]            11                             
.[migration/0]       12                             
.[cpuhp/0]           14                             
.[cpuhp/1]           15                             
.[migration/1]       16                             
.[ksoftirqd/1]       17                             
.[kworker/1:0H]      19                             
.[kdevtmpfs]         20                             
.[netns]             21                             
.[kauditd]           22                             
.[khungtaskd]        23                             
.[oom_reaper]        24                             
.[writeback]         25                             
.[kcompactd0]        26                             
.[ksmd]              27                             
.[khugepaged]        28                             
.[crypto]            29                             
.[kintegrityd]       30                             
.[kblockd]           31                             
.[edac-poller]       32                             
.[devfreq_wq]        33                             
.[watchdogd]         34                             
.[kswapd0]           36                             
.[kthrotld]          54                             
.[ipv6_addrconf]     55                             
.[kstrp]             65                             
.[ata_sff]           101                            
.[scsi_eh_0]         102                            
.[scsi_eh_1]         103                            
.[scsi_tmf_1]        104                            
.[scsi_eh_2]         105                            
.[scsi_tmf_2]        106                            
.[scsi_tmf_0]        108                            
.[kworker/1:1H]      113                            
.[kworker/0:2]       136                            
.[kworker/0:1H]      138                            
.[kworker/u5:0]      166                            
.[jbd2/sda1-8]       168                            
.[ext4-rsv-conver]   169                            
.[ttm_swap]          262                            
.[irq/18-vmwgfx]     263                            
.[kworker/u4:0]      633                            
.[kworker/0:1]       8912                           
.[kworker/1:0]       10483                          
.[kworker/u4:2]      10538                          
.[kworker/1:1]       10585                          
.[kworker/u4:1]      10597                          
.[kworker/1:2]       10603  
```

### linux_cpuinfo

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_cpuinfo
```
```bash
Processor    Vendor           Model
------------ ---------------- -----
0            GenuineIntel     Intel(R) Core(TM) i3-4130T CPU @ 2.90GHz
1            GenuineIntel     Intel(R) Core(TM) i3-4130T CPU @ 2.90GHz
```


## Análisis de red

### linux_arp

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_arp
```
```bash
[192.168.10.1                              ] at 64:d1:54:ec:e9:9d    on enp0s3
[192.168.10.8                              ] at 08:00:27:3f:5c:82    on enp0s3
[192.168.10.20                             ] at f8:32:e4:72:f8:c6    on enp0s3
[fe80::66d1:54ff:feec:e99d                 ] at 64:d1:54:ec:e9:9d    on enp0s3
[ff02::1:ffba:fc21                         ] at 33:33:ff:ba:fc:21    on enp0s3
[ff02::2                                   ] at 33:33:00:00:00:02    on enp0s3
[ff02::16                                  ] at 33:33:00:00:00:16    on enp0s3
```

### linux_ifconfig

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_ifconfig
```
```bash
Interface        IP Address           MAC Address        Promiscous Mode
---------------- -------------------- ------------------ ---------------
lo               127.0.0.1            00:00:00:00:00:00  False          
enp0s3           192.168.10.226       08:00:27:ba:fc:21  False 
```

### linux_route_cache y linux_netstat

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_route_cache o linux_netstat
```
En este caso los plugins `linux_netstat` y `route_cache` no funcionan, porque no se puede obtener la información de la tabla de enrutamiento.



## Análisis de ficheros y kernel

### linux_enumerate_files

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_enumerate_files
```
```bash
Inode Address Inode Number              Path
------------- ------------------------- ----
   0xf600b840                     10328 /sys/fs/cgroup
   0xf61fd4d0                     10363 /sys/fs/cgroup/rdma
   0xf61fcfa8                     10362 /sys/fs/cgroup/cpuset
   0xf61fc3a0                     10361 /sys/fs/cgroup/pids
   0xf61fd688                     10360 /sys/fs/cgroup/memory
   0xf61fdd68                     10359 /sys/fs/cgroup/freezer
   0xf61fd9f8                     10358 /sys/fs/cgroup/perf_event
   0xf61fcc38                     10357 /sys/fs/cgroup/net_cls
   0xf66cec38                     10356 /sys/fs/cgroup/net_prio
   0xf66ce558                     10355 /sys/fs/cgroup/net_cls,net_prio
   0xf66cea80                     10354 /sys/fs/cgroup/devices
   0xf66cf9f8                     10353 /sys/fs/cgroup/cpuacct
   0xf604fbb0                     10352 /sys/fs/cgroup/cpu
   0xf604e030                     10351 /sys/fs/cgroup/cpu,cpuacct
   0xf65da558                     10350 /sys/fs/cgroup/blkio
   0xf600a8c8                     10330 /sys/fs/cgroup/systemd
   0xf600b318                     10329 /sys/fs/cgroup/unified
   0xf413f3e8                         1 /sys
   0xf41bc620                         5 /sys/dev
   0xf42ebd18                         7 /sys/dev/char
   0xf3d42f50                      7691 /sys/dev/char/4:64
   0xf3d43260                      7789 /sys/dev/char/4:66
   0xf3d43570                      7740 /sys/dev/char/4:65
   0xf3d42620                      7838 /sys/dev/char/4:67
   0xf3c29a08                     13481 /sys/dev/char/13:33
   0xf3c290d8                     14235 /sys/dev/char/13:34
   0xf414e7a8                        10 /sys/class
   0xf3c2adc8                     14362 /sys/class/drm_dp_aux_dev
   0xf43e90d8                     13993 /sys/class/scsi_generic
   0xf43e53e8                     13300 /sys/class/sound
   0xf3d43a08                     15364 /sys/class/sound/card0
   0xf4118000                         4 /sys/devices
   0xf3c1dd18                     14797 /sys/devices/power
   0xf3c1da08                     14798 /sys/devices/power/uevent
   0xf4140dc8                      1388 /sys/devices/LNXSYSTM:00
   0xf4144188                      2519 /sys/devices/LNXSYSTM:00/LNXSLPBN:00
   0xf43da7a8                     13172 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/driver
   0xf43db0d8                     13173 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input
   0xf43da000                     13174 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4
   0xf3c2fa08                     13180 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/phys
   0xf3c2fd18                     13176 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/subsystem
   0xf3c2e000                     14510 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/event3
   0xf3c2ef50                     14511 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/event3/uevent
   0xf43cfd18                     13179 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/name
   0xf43db570                     13184 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/id
   0xf43db880                     13185 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/id/bustype
   0xf43db3e8                     13183 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/properties
   0xf43dbd18                     13189 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/capabilities
   0xf43da620                     13191 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/capabilities/key
   0xf43daab8                     13192 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/capabilities/rel
   0xf43dbb90                     13193 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/capabilities/abs
   0xf43dba08                     13190 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/capabilities/ev
   0xf43daf50                     13175 /sys/devices/LNXSYSTM:00/LNXSLPBN:00/input/input4/uevent
   0xf4144ab8                      2494 /sys/devices/LNXSYSTM:00/LNXPWRBN:00
   <snip>
   ```

### linux_find_file

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_find_file -F "/etc/passwd"
```
```bash
Inode Number          Inode File Path
---------------- ---------- ---------
          262243 0xf4363a30 /etc/passwd
```

### linux_recover_filesystem

```bash
sudo python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_recover_filesystem
```
Aquí la salida es la estructura del sistema que en momento de captura estaba cargada en ram.

![alt text](/assets/img/posts/analisismemorialinux/image-1.png)

### linux_mount

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_mount
```

```bash
tmpfs                     /sys/fs/cgroup                      tmpfs        ro,nosuid,nodev,noexec                                            
sysfs                     /sys                                sysfs        ro,relatime,nosuid,nodev,noexec                                   
tmpfs                     /home                               tmpfs        ro,relatime,nosuid,noexec                                         
debugfs                   /sys/kernel/debug                   debugfs      ro,relatime                                                       
/dev/sda1                 /                                   ext4         ro,relatime                                                       
tmpfs                     /dev                                tmpfs        ro,nosuid,noexec                                                  
udev                      /dev                                devtmpfs     rw,relatime,nosuid                                                
cgroup                    /sys/fs/cgroup/blkio                cgroup       ro,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/pids                 cgroup       rw,relatime,nosuid,nodev,noexec                                   
proc                      /proc                               proc         rw,relatime,nosuid,nodev,noexec                                   
systemd-1                 /proc/sys/fs/binfmt_misc            autofs       rw,relatime                                                       
cgroup                    /sys/fs/cgroup/net_cls,net_prio     cgroup       rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/perf_event           cgroup       rw,relatime,nosuid,nodev,noexec                                   
hugetlbfs                 /dev/hugepages                      hugetlbfs    rw,relatime                                                       
tmpfs                     /dev/shm                            tmpfs        rw,nosuid,nodev                                                   
securityfs                /sys/kernel/security                securityfs   rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/cpuset               cgroup       rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/devices              cgroup       rw,relatime,nosuid,nodev,noexec                                   
tmpfs                     /run/user/0                         tmpfs        rw,relatime,nosuid,nodev                                          
pstore                    /sys/fs/pstore                      pstore       rw,relatime,nosuid,nodev,noexec                                   
mqueue                    /dev/mqueue                         mqueue       rw,relatime                                                       
bpf                       /sys/fs/bpf                         bpf          rw,relatime,nosuid,nodev,noexec                                   
tmpfs                     /run/user/1000                      tmpfs        rw,relatime,nosuid,nodev                                          
cgroup                    /sys/fs/cgroup/rdma                 cgroup       rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/freezer              cgroup       rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/cpu,cpuacct          cgroup       ro,relatime,nosuid,nodev,noexec                                   
cgroup2                   /sys/fs/cgroup/unified              cgroup2      rw,relatime,nosuid,nodev,noexec                                   
devpts                    /dev/pts                            devpts       rw,relatime,nosuid,noexec                                         
cgroup                    /sys/fs/cgroup/systemd              cgroup       rw,relatime,nosuid,nodev,noexec                                   
tmpfs                     /run/lock                           tmpfs        rw,relatime,nosuid,nodev,noexec                                   
cgroup                    /sys/fs/cgroup/memory               cgroup       ro,relatime,nosuid,nodev,noexec
```

### linux_mount_cache

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_mount_cache
```
No está soportado

```bash
INFO    : volatility.debug    : SLUB is currently unsupported.
```

### linux_bash

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_bash
```
```bash
Pid      Name                 Command Time                   Command
-------- -------------------- ------------------------------ -------
     385 bash                 2023-03-15 13:25:03 UTC+0000   find . -name "linux"
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install linux-headers-$(uname -a)
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install linux-headers-$(uname -r)
     385 bash                 2023-03-15 13:25:03 UTC+0000   ip address
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd tools/
     385 bash                 2023-03-15 13:25:03 UTC+0000   make
     385 bash                 2023-03-15 13:25:03 UTC+0000   S??u??????
     385 bash                 2023-03-15 13:25:03 UTC+0000   uname -a
     385 bash                 2023-03-15 13:25:03 UTC+0000   uname -r
     385 bash                 2023-03-15 13:25:03 UTC+0000   uname -a
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd plugins/linux/
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd volatility/
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt search linux-headers | grep headers
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt search linux-headers | grep headers | more
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   make
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt update
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd linux
     385 bash                 2023-03-15 13:25:03 UTC+0000   git clone https://github.com/volatilityfoundation/volatility.git
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install build-essential
     385 bash                 2023-03-15 13:25:03 UTC+0000   make
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd ..
     385 bash                 2023-03-15 13:25:03 UTC+0000   rm -R volatility/
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install linux-headers-$(uname -a)
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install volatility
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd ..
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install build-essential
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd ..
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install linux-headers-$(uname -r)
     385 bash                 2023-03-15 13:25:03 UTC+0000   cd ..
     385 bash                 2023-03-15 13:25:03 UTC+0000   dwarfdump 
     385 bash                 2023-03-15 13:25:03 UTC+0000   git clone https://github.com/volatilityfoundation/volatility.git
     385 bash                 2023-03-15 13:25:03 UTC+0000   shutdown -h 0
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install dwarf
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt search linux-image-4.19.0-16-686
     385 bash                 2023-03-15 13:25:03 UTC+0000   make
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   apt install dwarfdump
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   ls
     385 bash                 2023-03-15 13:25:03 UTC+0000   WVS?f????(?
     <snip>
```

### linux_dmesg

```bash
python2.7 vol.py -f ram.lime --profile=Linuxdebian10-4_19_0-23-686x86 linux_dmesg
```
```bash
Volatility Foundation Volatility Framework 2.6.1
*** Failed to import volatility.plugins.registry.shutdown (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.getservicesids (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.timeliner (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.malware.apihooks (NameError: name 'distorm3' is not defined)
*** Failed to import volatility.plugins.malware.servicediff (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.userassist (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.getsids (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.shellbags (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.evtlogs (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.shimcache (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.tcaudit (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.dumpregistry (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.lsadump (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.malware.threads (NameError: name 'distorm3' is not defined)
*** Failed to import volatility.plugins.mac.apihooks_kernel (ImportError: No module named distorm3)
*** Failed to import volatility.plugins.registry.amcache (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.mac.check_syscall_shadow (ImportError: No module named distorm3)
*** Failed to import volatility.plugins.malware.svcscan (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.registry.auditpol (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.ssdt (NameError: name 'distorm3' is not defined)
*** Failed to import volatility.plugins.registry.registryapi (ImportError: No module named Crypto.Hash)
*** Failed to import volatility.plugins.mac.apihooks (ImportError: No module named distorm3)
*** Failed to import volatility.plugins.envars (ImportError: No module named Crypto.Hash)
[0.0] Linux version 4.19.0-23-686 (debian-kernel@lists.debian.org) (gcc version 8.3.0 (Debian 8.3.0-6)) #1 SMP Debian 4.19.269-1 (2022-12-20)
[0.0] x86/fpu: Supporting XSAVE feature 0x001: 'x87 floating point registers'
[0.0] x86/fpu: Supporting XSAVE feature 0x002: 'SSE registers'
[0.0] x86/fpu: Supporting XSAVE feature 0x004: 'AVX registers'
[0.0] x86/fpu: xstate_offset[2]:  576, xstate_sizes[2]:  256
[0.0] x86/fpu: Enabled xstate features 0x7, context size is 832 bytes, using 'standard' format.
[0.0] BIOS-provided physical RAM map:
[0.0] BIOS-e820: [mem 0x0000000000000000-0x000000000009fbff] usable
[0.0] BIOS-e820: [mem 0x000000000009fc00-0x000000000009ffff] reserved
[0.0] BIOS-e820: [mem 0x00000000000f0000-0x00000000000fffff] reserved
[0.0] BIOS-e820: [mem 0x0000000000100000-0x000000003ffeffff] usable
[0.0] BIOS-e820: [mem 0x000000003fff0000-0x000000003fffffff] ACPI data
[0.0] BIOS-e820: [mem 0x00000000fec00000-0x00000000fec00fff] reserved
[0.0] BIOS-e820: [mem 0x00000000fee00000-0x00000000fee00fff] reserved
[0.0] BIOS-e820: [mem 0x00000000fffc0000-0x00000000ffffffff] reserved
[0.0] Notice: NX (Execute Disable) protection cannot be enabled: non-PAE kernel!
[0.0] SMBIOS 2.5 present.
[0.0] DMI: innotek GmbH VirtualBox/VirtualBox, BIOS VirtualBox 12/01/2006
[0.0] Hypervisor detected: KVM
[0.0] kvm-clock: Using msrs 4b564d01 and 4b564d00
[831.0] kvm-clock: cpu 0, msr 9a30001, primary cpu clock
[904.0] kvm-clock: using sched offset of 7370052075 cycles
[3395.0] clocksource: kvm-clock: mask: 0xffffffffffffffff max_cycles: 0x1cd42e4dffb, max_idle_ns: 881590591483 ns
[5981.0] tsc: Detected 2893.298 MHz processor
[1780280.0] e820: update [mem 0x00000000-0x00000fff] usable ==> reserved
[1782221.0] e820: remove [mem 0x000a0000-0x000fffff] usable
[1786001.0] last_pfn = 0x3fff0 max_arch_pfn = 0x100000
[1797223.0] MTRR default type: uncachable
[1797967.0] MTRR variable ranges disabled:
[1798647.0] Disabled
[1799773.0] x86/PAT: MTRRs disabled, skipping PAT initialization too.
[1802657.0] CPU MTRRs all blank - virtualized system.
[1805082.0] x86/PAT: Configuration [0-7]: WB  WT  UC- UC  WB  WT  UC- UC  
[1835283.0] found SMP MP-table at [mem 0x0009fff0-0x0009ffff]
[68949783.0] initial memory mapped: [mem 0x00000000-0x09ffffff]
[69017833.0] RAMDISK: [mem 0x3568b000-0x36b3cfff]
[69022980.0] ACPI: Early table checksum verification disabled
[69046561.0] ACPI: RSDP 0x00000000000E0000 000024 (v02 VBOX  )
[69050763.0] ACPI: XSDT 0x000000003FFF0030 00003C (v01 VBOX   VBOXXSDT 00000001 ASL  00000061)
[69056309.0] ACPI: FACP 0x000000003FFF00F0 0000F4 (v04 VBOX   VBOXFACP 00000001 ASL  00000061)
[69062049.0] ACPI: DSDT 0x000000003FFF0610 002353 (v02 VBOX   VBOXBIOS 00000002 INTL 20100528)
<snip>
```




# Volatility 3

Como ya indicamos anteriormente en esta sección vamos a omitir la selección y extracción de mapas de memoria vamos a asumir que ya realizamos ese proceso.

Asumiendo lo anterior y con el mapa de memoria RAM ubicado en volatility3/volatility3/symbols/linux/debian-XXX.json.xz, continuamos con la ejecución del vol.py

## Análisis 

### linux.bash.Bash

```bash
❯ python3 vol.py -f ram.lime linux.bash.Bash
Volatility 3 Framework 2.20.0
Progress:  100.00		Stacking attempts finished                 
PID	Process	CommandTime	Command

385	bash	2023-03-15 13:25:03.000000 UTC	apt install linux-headers-$(uname -a)
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	ip address
385	bash	2023-03-15 13:25:03.000000 UTC	cd tools/
385	bash	2023-03-15 13:25:03.000000 UTC	make
385	bash	2023-03-15 13:25:03.000000 UTC	uname -a
385	bash	2023-03-15 13:25:03.000000 UTC	apt install linux-headers-$(uname -r)
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	S�u���ú�
385	bash	2023-03-15 13:25:03.000000 UTC	uname -a
385	bash	2023-03-15 13:25:03.000000 UTC	cd plugins/linux/
385	bash	2023-03-15 13:25:03.000000 UTC	cd volatility/
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-headers | grep headers | more
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-headers | grep headers
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	uname -r
385	bash	2023-03-15 13:25:03.000000 UTC	apt update
385	bash	2023-03-15 13:25:03.000000 UTC	cd linux
385	bash	2023-03-15 13:25:03.000000 UTC	git clone https://github.com/volatilityfoundation/volatility.git
385	bash	2023-03-15 13:25:03.000000 UTC	apt install build-essential
385	bash	2023-03-15 13:25:03.000000 UTC	cd ..
385	bash	2023-03-15 13:25:03.000000 UTC	rm -R volatility/
385	bash	2023-03-15 13:25:03.000000 UTC	make
385	bash	2023-03-15 13:25:03.000000 UTC	apt install volatility
385	bash	2023-03-15 13:25:03.000000 UTC	cd ..
385	bash	2023-03-15 13:25:03.000000 UTC	apt install build-essentials
385	bash	2023-03-15 13:25:03.000000 UTC	cd ..
385	bash	2023-03-15 13:25:03.000000 UTC	apt install linux-headers-$(uname -a)
385	bash	2023-03-15 13:25:03.000000 UTC	apt install linux-headers-$(uname -r)
385	bash	2023-03-15 13:25:03.000000 UTC	dwarfdump 
385	bash	2023-03-15 13:25:03.000000 UTC	shutdown -h 0
385	bash	2023-03-15 13:25:03.000000 UTC	apt install dwarfdump
385	bash	2023-03-15 13:25:03.000000 UTC	ip address
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-image
385	bash	2023-03-15 13:25:03.000000 UTC	apt install dwarf
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-image | grep image
385	bash	2023-03-15 13:25:03.000000 UTC	make
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-image | more
385	bash	2023-03-15 13:25:03.000000 UTC	find . -name "linux"
385	bash	2023-03-15 13:25:03.000000 UTC	ls
385	bash	2023-03-15 13:25:03.000000 UTC	apt search linux-image-4.19.0-16-686
385	bash	2023-03-15 13:25:03.000000 UTC	cd ..
385	bash	2023-03-15 13:25:03.000000 UTC	zip debian10-$(uname -r).zip module.dwarf  /boot/System.map-4.19.0-23-686 
385	bash	2023-03-15 13:25:03.000000 UTC	apt install build-essential
385	bash	2023-03-15 13:25:03.000000 UTC	WVS�f����(�
<snip>
```

### linux.kmsg.Kmsg

```bash
❯ python3 vol.py -f ram.lime linux.kmsg.Kmsg
Volatility 3 Framework 2.20.0
Progress:  100.00		Stacking attempts finished                 
facility	level	timestamp	caller	line

56	info	5833691318.373523	-	ζZ�,oY���פ���\����~�6�I��7�!l�����
56	info	5833691318.373523	-	iC�(�-�U%,�4
56	info	5833691318.373523	-	���\���
56	info	5833691318.373523	-	/u-ϳ����z4]QW�I�"���7�?ȩz}-�9b�Q�uEE�QZ
56	info	5833691318.373523	-	dS��F
56	info	5833691318.373523	-	�Z���]$�VX"+`��W��7�ߍv�k=�+�(c��E�&/�M
56	info	5833691318.373523	-	}H��dz;��6���m�hJH	
56	info	5833691318.373523	-	�����fͱ�v@ԛؿІ
56	info	5833691318.373523	-	�@���6���\s������;� r���S���#�u�eH>���Hm)���K�mo�.��
56	info	5833691318.373523	-	�a)��RC�7>�gI�� �|��;,M�.A��ग़��QN�K�;�jJ[�wD��@v���1.K��lF� l�_���:�f���;�ض
56	info	5833691318.373523	-	����zv�ó�o�O��S��=t�o�O���ӿ���c5�K�G���=t:�Ac~��Ƣ������>@���C�F�Ac��m��;�tG�0U�T�����5�5|:M�ۨ�.3h2&�[
56	info	5833691318.373523	-	?M@ ���k~+!F�m�f����E��|� s4c<Њ���0����@�l�^.I��$�	k���1:���Z��(xO����|��Wl4����V�
56	info	5833691318.373523	-	��g�QŶ�
56	info	5833691318.373523	-	�	�g�t!��L�j�R�n?���j�(5
56	info	5833691318.373523	-	�o�C��P�%�oK���0�uq�6��k=ќ�����o&�U����Ý�gj�3$ ������
56	info	5833691318.373523	-	�̗�,�M!�D�A��ܜ��Q?�m`|�`��}�v^�b+D1׹.p���4����J+��40�]K۫υ���v�3��6��	�7x�!w��ֻ/�w�u��9��>O�FZ�Y�D��hG+�D�6�	-���O�/�"����n�'TV
56	info	5833691318.373523	-	~�W_�*
56	info	5833691318.373523	-	�k8l�O%�~M%�e+`c=�*��؄�e�o������~KxFq�5�"
56	info	5833691318.373523	-	��i��C�Ll/Ԡ"���H{.iUm���َHz�9���zJ��q�u8������mz`�ǎ��j�c�
56	info	5833691318.373523	-	С�Z6�
56	info	5833691318.373523	-	y�co�oۤÛ�uh�j:��:\�K���#��C����#�����;Z�
56	info	5833691318.373523	-	���{vp�&�a��M��/�ql��
56	info	5833691318.373523	-	�A�1�ω
56	info	5833691318.373523	-	�
56	info	5833691318.373523	-	�1�1���M��#?%b6K�S�N�D���ܔ��KvJ�����c���D��D�u����6���{�o���q��D_�fĂ[N� USj�hF�*fWس�x��篍`F��`��E�|�
56	info	5833691318.373523	-	
56	info	5833691318.373523	-	��yG���"�;�2����>(`���s�V��>>6־���J�������N�0���z�O3? �g��<�@Bg�̳����p7s1s�2͂�-�|�؋�WB2��g�������M��g�����$��$ӧ�X�Il%�;�������'PM��r��k3�Q_	������į���4����,]�mx�����Wƕ�؏��"�lÈ�T��t�yܢEO�̩8��o����wn��v���%��\3��h�m��չ�9[o��ܹ��6-R����Zf���6����ǋ���D?���f���83�н�.K��NWO���uOY����k"|�ƫO9�o^O92��,���z
56	info	5833691318.373523	-	t��+�*�M�DkEStE�=�����";i��2��7����
56	info	5833691318.373523	-	����^�|mY�"�Y#�
56	info	5833691318.373523	-	��6GZQ�YT�;Jָ�MU4�!�	�Q/
56	info	5833691318.373523	-	���
56	info	5833691318.373523	-	]�
56	info	5833691318.373523	-	��
56	info	5833691318.373523	-	�0������np�a/��7�� T�0�(w|>��VE�S�R��
56	info	5833691318.373523	-	��7����k��Ή���✉���X�kv ր耾ͧ4��"�5�eEI�:
<snip>
```

### linux.lsmod.Lsmod

```bash
❯ python3 vol.py -f ram.lime linux.lsmod.Lsmod
Volatility 3 Framework 2.20.0
Progress:  100.00		Stacking attempts finished                 
Offset	Name	Size

0xf77f9040	lime	20480
0xf77e80c0	joydev	20480
0xf76e31c0	crc32_pclmul	16384
0xf76d4380	intel_rapl_perf	16384
0xf7cf6a80	vmwgfx	225280
0xf77135c0	ttm	65536
0xf76aa040	evdev	20480
0xf75fe080	pcspkr	16384
0xf77b64c0	drm_kms_helper	135168
0xf76784c0	snd_intel8x0	32768
0xf77e2140	serio_raw	16384
0xf75ef0c0	hid_generic	16384
0xf7704080	sg	28672
0xf7cbb040	drm	323584
0xf77d3400	snd_ac97_codec	98304
0xf7552080	ac97_bus	16384
0xf76fa500	snd_pcm	81920
0xf769d080	snd_timer	28672
0xf74b0000	fb_sys_fops	16384
0xf76c7240	snd	61440
0xf766a140	ac	16384
0xf762e000	syscopyarea	16384
0xf76b91c0	video	45056
0xf7570040	sysfillrect	16384
0xf7639000	sysimgblt	16384
0xf7634000	soundcore	16384
0xf7640180	button	16384
0xf7661200	vboxguest	32768
0xf75bf1c0	ip_tables	20480
0xf756b1c0	x_tables	24576
0xf75b9600	autofs4	36864
0xf754d680	usbhid	45056
0xf7693fc0	hid	102400
0xf778dc00	ext4	532480
0xf74a6000	crc16	16384
0xf7476080	mbcache	16384
0xf7656100	jbd2	86016
0xf746c1c0	crc32c_generic	16384
0xf751e180	fscrypto	24576
0xf74710c0	ecb	16384
0xf74551c0	crc32c_intel	16384
0xf76200c0	sr_mod	24576
0xf7619280	sd_mod	49152
0xf760c380	cdrom	49152
0xf75416c0	aesni_intel	20480
0xf75383c0	ata_generic	16384
0xf74ab2c0	ohci_pci	16384
0xf7467180	aes_i586	20480
0xf7533040	crypto_simd	16384
0xf752a0c0	cryptd	20480
0xf75af840	ohci_hcd	45056
0xf75e2540	psmouse	131072
0xf74f61c0	ehci_pci	16384
0xf7564a80	ehci_hcd	61440
0xf745f900	ata_piix	32768
0xf75f9480	ahci	36864
0xf74f1300	libahci	28672
0xf74e62c0	i2c_piix4	24576
0xf74db680	usbcore	188416
0xf759e340	libata	192512
0xf7524040	usb_common	16384
0xf7515f80	e1000	118784
0xf749ebc0	scsi_mod	172032
```

### linux.lsof.Lsof

```bash
❯ python3 vol.py -f ram.lime linux.lsof.Lsof
Volatility 3 Framework 2.20.0
Progress:  100.00		Stacking attempts finished                 
PID	TID	Process	FD	Path	Device	Inode	Type	Mode	Changed	Modified	Accessed	Size

1	1	systemd	0	/dev/null	0:6	1028	CHR	crw-rw-rw-	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	0
1	1	systemd	1	/dev/null	0:6	1028	CHR	crw-rw-rw-	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	0
1	1	systemd	2	/dev/null	0:6	1028	CHR	crw-rw-rw-	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	2023-03-15 13:25:00.252000 UTC	0
1	1	systemd	3	/dev/kmsg	0:6	1034	CHR	crw-r--r--	2023-03-15 13:25:00.248000 UTC	2023-03-15 13:25:00.248000 UTC	2023-03-15 13:25:00.248000 UTC	0
1	1	systemd	4	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	5	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	6	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	7	/sys/fs/cgroup/unified	0:24	1	DIR	dr-xr-xr-x	2023-03-15 13:24:59.736000 UTC	2023-03-15 13:24:59.736000 UTC	2023-03-15 13:24:59.736000 UTC	0
1	1	systemd	8	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	9	socket:[10496]	0:9	10496	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	10	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	11	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	13	/proc/1/mountinfo	0:4	10497	REG	-r--r--r--	2023-03-15 13:24:59.804000 UTC	2023-03-15 13:24:59.804000 UTC	2023-03-15 13:24:59.804000 UTC	0
1	1	systemd	14	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	15	/proc/swaps	0:4	4026532062	REG	-r--r--r--	2023-03-15 13:24:59.416000 UTC	2023-03-15 13:24:59.416000 UTC	2023-03-15 13:24:59.416000 UTC	0
1	1	systemd	16	socket:[10498]	0:9	10498	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	17	socket:[10500]	0:9	10500	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	18	socket:[10501]	0:9	10501	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	19	socket:[10502]	0:9	10502	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	23	socket:[13866]	0:9	13866	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	24	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	25	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	26	socket:[10509]	0:9	10509	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	27	socket:[10512]	0:9	10512	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	28	socket:[10516]	0:9	10516	SOCK	srwxrwxrwx	-	-	-	0
1	1	systemd	29	anon_inode:[8319]	0:13	8319	-	?rw-------	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	2023-03-15 13:25:04.865525 UTC	0
1	1	systemd	30	/dev/autofs	0:6	10322	CHR	crw-r--r--	2023-03-15 13:25:00.264000 UTC	2023-03-15 13:25:00.264000 UTC	2023-03-15 13:25:00.264000 UTC	0
1	1	systemd	31	pipe:[10534]	0:12	10534	FIFO	prw-------	2023-03-15 13:24:59.868000 UTC	2023-03-15 13:24:59.868000 UTC	2023-03-15 13:24:59.868000 UTC	0
```

### linux.malfind.Malfind

```bash
❯ python3 vol.py -f ram.lime linux.malfind.Malfind
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
PID     Process Start   End     Protection      Hexdump Disasm
```
En este caso no encuentra posibles artefactos malignos en memoria.

### linux.mountinfo.MountInfo

```bash
❯ python3 vol.py -f ram.lime linux.mountinfo.MountInfo
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
MNT_NS_ID       MOUNT ID        PARENT_ID       MAJOR:MINOR     ROOT    MOUNT_POINT     MOUNT_OPTIONS   FIELDS  FSTYPE  MOUNT_SRC       SB_OPTIONS

4026531840      0       0       0:1     /       /       rw              rootfs  rootfs  rw
4026531840      19      24      0:18    /       /sys    rw,nosuid,nodev,noexec,relatime shared:7        sysfs   sysfs   rw
4026531840      20      24      0:4     /       /proc   rw,nosuid,nodev,noexec,relatime shared:14       proc    proc    rw
4026531840      21      24      0:6     /       /dev    rw,nosuid,relatime      shared:2        devtmpfs        udev    rw
4026531840      22      21      0:19    /       /dev/pts        rw,nosuid,noexec,relatime       shared:3        devpts  devpts  rw
4026531840      23      24      0:20    /       /run    rw,nosuid,noexec,relatime       shared:5        tmpfs   tmpfs   rw
4026531840      24      0       8:1     /       /       rw,relatime     shared:1        ext4    /dev/sda1       rw
4026531840      25      19      0:7     /       /sys/kernel/security    rw,nosuid,nodev,noexec,relatime shared:8        securityfs      securityfs      rw
4026531840      26      21      0:21    /       /dev/shm        rw,nosuid,nodev shared:4        tmpfs   tmpfs   rw
4026531840      27      23      0:22    /       /run/lock       rw,nosuid,nodev,noexec,relatime shared:6        tmpfs   tmpfs   rw
4026531840      28      19      0:23    /       /sys/fs/cgroup  ro,nosuid,nodev,noexec  shared:9        tmpfs   tmpfs   ro
4026531840      29      28      0:24    /       /sys/fs/cgroup/unified  rw,nosuid,nodev,noexec,relatime shared:10       cgroup2 cgroup2 rw
4026531840      30      28      0:25    /       /sys/fs/cgroup/systemd  rw,nosuid,nodev,noexec,relatime shared:11       cgroup  cgroup  rw
4026531840      31      19      0:26    /       /sys/fs/pstore  rw,nosuid,nodev,noexec,relatime shared:12       pstore  pstore  rw
4026531840      32      19      0:27    /       /sys/fs/bpf     rw,nosuid,nodev,noexec,relatime shared:13       bpf     bpf     rw
4026531840      33      28      0:28    /       /sys/fs/cgroup/blkio    rw,nosuid,nodev,noexec,relatime shared:15       cgroup  cgroup  rw
4026531840      34      28      0:29    /       /sys/fs/cgroup/cpu,cpuacct      rw,nosuid,nodev,noexec,relatime shared:16       cgroup  cgroup  rw
4026531840      35      28      0:30    /       /sys/fs/cgroup/devices  rw,nosuid,nodev,noexec,relatime shared:17       cgroup  cgroup  rw
4026531840      36      28      0:31    /       /sys/fs/cgroup/net_cls,net_prio rw,nosuid,nodev,noexec,relatime shared:18       cgroup  cgroup  rw
4026531840      37      28      0:32    /       /sys/fs/cgroup/perf_event       rw,nosuid,nodev,noexec,relatime shared:19       cgroup  cgroup  rw
4026531840      38      28      0:33    /       /sys/fs/cgroup/freezer  rw,nosuid,nodev,noexec,relatime shared:20       cgroup  cgroup  rw
4026531840      39      28      0:34    /       /sys/fs/cgroup/memory   rw,nosuid,nodev,noexec,relatime shared:21       cgroup  cgroup  rw
4026531840      40      28      0:35    /       /sys/fs/cgroup/pids     rw,nosuid,nodev,noexec,relatime shared:22       cgroup  cgroup  rw
4026531840      41      28      0:36    /       /sys/fs/cgroup/cpuset   rw,nosuid,nodev,noexec,relatime shared:23       cgroup  cgroup  rw
4026531840      42      28      0:37    /       /sys/fs/cgroup/rdma     rw,nosuid,nodev,noexec,relatime shared:24       cgroup  cgroup  rw
4026531840      43      20      0:38    /       /proc/sys/fs/binfmt_misc        rw,relatime     shared:25       autofs  systemd-1       rw
4026531840      44      21      0:17    /       /dev/mqueue     rw,relatime     shared:26       mqueue  mqueue  rw
4026531840      45      21      0:39    /       /dev/hugepages  rw,relatime     shared:27       hugetlbfs       hugetlbfs       rw
<snip>
```

### linux.proc.Maps

```bash
❯ python3 vol.py -f ram.lime linux.proc.Maps
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
PID     Process Start   End     Flags   PgOff   Major   Minor   Inode   File Path       File output

1       systemd 0x469000        0x47f000        r--     0x0     8       1       787585  /usr/lib/systemd/systemd        Disabled
1       systemd 0x47f000        0x538000        r-x     0x16000 8       1       787585  /usr/lib/systemd/systemd        Disabled
1       systemd 0x538000        0x5aa000        r--     0xcf000 8       1       787585  /usr/lib/systemd/systemd        Disabled
1       systemd 0x5aa000        0x5ca000        r--     0x140000        8       1       787585  /usr/lib/systemd/systemd        Disabled
1       systemd 0x5ca000        0x5cb000        rw-     0x160000        8       1       787585  /usr/lib/systemd/systemd        Disabled
1       systemd 0x1b66000       0x1c0c000       rw-     0x0     0       0       0       [heap]  Disabled
1       systemd 0xb70ec000      0xb70f0000      rw-     0x0     0       0       0       Anonymous Mapping       Disabled
1       systemd 0xb70f0000      0xb70fa000      r--     0x0     8       1       783962  /usr/lib/i386-linux-gnu/libm-2.28.so    Disabled
1       systemd 0xb70fa000      0xb71bc000      r-x     0xa000  8       1       783962  /usr/lib/i386-linux-gnu/libm-2.28.so    Disabled
1       systemd 0xb71bc000      0xb71f4000      r--     0xcc000 8       1       783962  /usr/lib/i386-linux-gnu/libm-2.28.so    Disabled
1       systemd 0xb71f4000      0xb71f5000      r--     0x103000        8       1       783962  /usr/lib/i386-linux-gnu/libm-2.28.so    Disabled
1       systemd 0xb71f5000      0xb71f6000      rw-     0x104000        8       1       783962  /usr/lib/i386-linux-gnu/libm-2.28.so    Disabled
1       systemd 0xb71f6000      0xb71f9000      r--     0x0     8       1       786721  /usr/lib/i386-linux-gnu/libudev.so.1.6.13       Disabled
1       systemd 0xb71f9000      0xb7210000      r-x     0x3000  8       1       786721  /usr/lib/i386-linux-gnu/libudev.so.1.6.13       Disabled
1       systemd 0xb7210000      0xb721b000      r--     0x1a000 8       1       786721  /usr/lib/i386-linux-gnu/libudev.so.1.6.13       Disabled
1       systemd 0xb721b000      0xb721c000      r--     0x24000 8       1       786721  /usr/lib/i386-linux-gnu/libudev.so.1.6.13       Disabled
1       systemd 0xb721c000      0xb721d000      rw-     0x25000 8       1       786721  /usr/lib/i386-linux-gnu/libudev.so.1.6.13       Disabled
1       systemd 0xb721d000      0xb721f000      rw-     0x0     0       0       0       Anonymous Mapping       Disabled
1       systemd 0xb721f000      0xb7222000      r--     0x0     8       1       784311  /usr/lib/i386-linux-gnu/libgpg-error.so.0.26.1  Disabled
1       systemd 0xb7222000      0xb7235000      r-x     0x3000  8       1       784311  /usr/lib/i386-linux-gnu/libgpg-error.so.0.26.1  Disabled
1       systemd 0xb7235000      0xb7242000      r--     0x16000 8       1       784311  /usr/lib/i386-linux-gnu/libgpg-error.so.0.26.1  Disabled
1       systemd 0xb7242000      0xb7243000      r--     0x22000 8       1       784311  /usr/lib/i386-linux-gnu/libgpg-error.so.0.26.1  Disabled
1       systemd 0xb7243000      0xb7244000      rw-     0x23000 8       1       784311  /usr/lib/i386-linux-gnu/libgpg-error.so.0.26.1  Disabled
1       systemd 0xb7244000      0xb7246000      r--     0x0     8       1       787402  /usr/lib/i386-linux-gnu/libjson-c.so.3.0.1      Disabled
1       systemd 0xb7246000      0xb724c000      r-x     0x2000  8       1       787402  /usr/lib/i386-linux-gnu/libjson-c.so.3.0.1      Disabled
1       systemd 0xb724c000      0xb724f000      r--     0x8000  8       1       787402  /usr/lib/i386-linux-gnu/libjson-c.so.3.0.1      Disabled
1       systemd 0xb724f000      0xb7250000      r--     0xa000  8       1       787402  /usr/lib/i386-linux-gnu/libjson-c.so.3.0.1      Disabled
1       systemd 0xb7250000      0xb7251000      rw-     0xb000  8       1       787402  /usr/lib/i386-linux-gnu/libjson-c.so.3.0.1      Disabled

<snip>
```

### linux.psaux.PsAux

```bash
❯ python3 vol.py -f ram.lime linux.psaux.PsAux
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
PID     PPID    COMM    ARGS

1       0       systemd /sbin/init
2       0       kthreadd        [kthreadd]
3       2       rcu_gp  [rcu_gp]
4       2       rcu_par_gp      [rcu_par_gp]
6       2       kworker/0:0H    [kworker/0:0H]
8       2       mm_percpu_wq    [mm_percpu_wq]
9       2       ksoftirqd/0     [ksoftirqd/0]
10      2       rcu_sched       [rcu_sched]
11      2       rcu_bh  [rcu_bh]
12      2       migration/0     [migration/0]
14      2       cpuhp/0 [cpuhp/0]
15      2       cpuhp/1 [cpuhp/1]
16      2       migration/1     [migration/1]
17      2       ksoftirqd/1     [ksoftirqd/1]
19      2       kworker/1:0H    [kworker/1:0H]
20      2       kdevtmpfs       [kdevtmpfs]
21      2       netns   [netns]
22      2       kauditd [kauditd]
23      2       khungtaskd      [khungtaskd]
24      2       oom_reaper      [oom_reaper]
25      2       writeback       [writeback]
26      2       kcompactd0      [kcompactd0]
27      2       ksmd    [ksmd]
28      2       khugepaged      [khugepaged]
29      2       crypto  [crypto]
30      2       kintegrityd     [kintegrityd]
31      2       kblockd [kblockd]
32      2       edac-poller     [edac-poller]
33      2       devfreq_wq      [devfreq_wq]
34      2       watchdogd       [watchdogd]
36      2       kswapd0 [kswapd0]
54      2       kthrotld        [kthrotld]
55      2       ipv6_addrconf   [ipv6_addrconf]
65      2       kstrp   [kstrp]
101     2       ata_sff [ata_sff]
102     2       scsi_eh_0       [scsi_eh_0]
103     2       scsi_eh_1       [scsi_eh_1]
104     2       scsi_tmf_1      [scsi_tmf_1]
105     2       scsi_eh_2       [scsi_eh_2]
106     2       scsi_tmf_2      [scsi_tmf_2]
108     2       scsi_tmf_0      [scsi_tmf_0]
113     2       kworker/1:1H    [kworker/1:1H]
136     2       kworker/0:2     [kworker/0:2]
138     2       kworker/0:1H    [kworker/0:1H]
166     2       kworker/u5:0    [kworker/u5:0]
168     2       jbd2/sda1-8     [jbd2/sda1-8]
169     2       ext4-rsv-conver [ext4-rsv-conver]
202     1       systemd-journal /lib/systemd/systemd-journald
219     1       systemd-udevd   /lib/systemd/systemd-udevd
241     1       systemd-timesyn /lib/systemd/systemd-timesyncd
262     2       ttm_swap        [ttm_swap]
263     2       irq/18-vmwgfx   [irq/18-vmwgfx]
330     1       systemd-logind  /lib/systemd/systemd-logind
332     1       rsyslogd        /usr/sbin/rsyslogd -n -iNONE
335     1       dbus-daemon     /usr/bin/dbus-daemon --system --address=systemd: --nofork --nopidfile --systemd-activation --syslog-only
339     1       cron    /usr/sbin/cron -f
348     1       dhclient        /sbin/dhclient -4 -v -i -pf /run/dhclient.enp0s3.pid -lf /var/lib/dhcp/dhclient.enp0s3.leases -I -df /var/lib/dhcp/dhclient6.enp0s3.leases enp0s3
350     1       sshd    -
351     1       login   -
374     1       systemd /lib/systemd/systemd --user
375     374     (sd-pam)        (sd-pam)
385     351     bash    -bash
392     350     sshd    sshd: usuario [priv]
395     1       systemd /lib/systemd/systemd --user
396     395     (sd-pam)        (sd-pam)
409     392     sshd    -
410     409     bash    -
606     410     su      -
607     606     bash    -bash
633     2       kworker/u4:0    [kworker/u4:0]
8912    2       kworker/0:1     [kworker/0:1]
10483   2       kworker/1:0     [kworker/1:0]
10538   2       kworker/u4:2    [kworker/u4:2]
10585   2       kworker/1:1     [kworker/1:1]
10597   2       kworker/u4:1    [kworker/u4:1]
10603   2       kworker/1:2     [kworker/1:2]
11218   607     insmod  insmod lime-4.19.0-23-686.ko path=ram.lime format=lime
```


### linux.pslist.PsList

```bash
❯ python3 vol.py -f ram.lime linux.pslist.PsList
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
OFFSET (V)      PID     TID     PPID    COMM    UID     GID     EUID    EGID    CREATION TIME   File output

0xf491cb40      1       1       0       systemd 0       0       0       0       2023-03-15 13:25:04.100016 UTC  Disabled
0xf4918ac0      2       2       0       kthreadd        0       0       0       0       2023-03-15 13:25:04.100016 UTC  Disabled
0xf4919580      3       3       2       rcu_gp  0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf491b5c0      4       4       2       rcu_par_gp      0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf4918000      6       6       2       kworker/0:0H    0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf491a040      8       8       2       mm_percpu_wq    0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf491e0c0      9       9       2       ksoftirqd/0     0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf491eb80      10      10      2       rcu_sched       0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf491ab00      11      11      2       rcu_bh  0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493cb40      12      12      2       migration/0     0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493b5c0      14      14      2       cpuhp/0 0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493c080      15      15      2       cpuhp/1 0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf4938000      16      16      2       migration/1     0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493d600      17      17      2       ksoftirqd/1     0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493e0c0      19      19      2       kworker/1:0H    0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493eb80      20      20      2       kdevtmpfs       0       0       0       0       2023-03-15 13:25:04.208016 UTC  Disabled
0xf493ab00      21      21      2       netns   0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49c8000      22      22      2       kauditd 0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49cd600      23      23      2       khungtaskd      0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49ca040      24      24      2       oom_reaper      0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49ce0c0      25      25      2       writeback       0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49ceb80      26      26      2       kcompactd0      0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49cab00      27      27      2       ksmd    0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49ccb40      28      28      2       khugepaged      0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49c8ac0      29      29      2       crypto  0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49c9580      30      30      2       kintegrityd     0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49cb5c0      31      31      2       kblockd 0       0       0       0       2023-03-15 13:25:04.212016 UTC  Disabled
0xf49cc080      32      32      2       edac-poller     0       0       0       0       2023-03-15 13:25:04.264016 UTC  Disabled
0xf4a50ac0      33      33      2       devfreq_wq      0       0       0       0       2023-03-15 13:25:04.264016 UTC  Disabled
0xf4a51580      34      34      2       watchdogd       0       0       0       0       2023-03-15 13:25:04.264016 UTC  Disabled
0xf4a54080      36      36      2       kswapd0 0       0       0       0       2023-03-15 13:25:04.690982 UTC  Disabled
0xf4be8ac0      54      54      2       kthrotld        0       0       0       0       2023-03-15 13:25:05.180348 UTC  Disabled
0xf4beab00      55      55      2       ipv6_addrconf   0       0       0       0       2023-03-15 13:25:05.539074 UTC  Disabled
0xf64a2040      65      65      2       kstrp   0       0       0       0       2023-03-15 13:25:05.546060 UTC  Disabled
0xf4beeb80      101     101     2       ata_sff 0       0       0       0       2023-03-15 13:25:05.742973 UTC  Disabled
0xf4a560c0      102     102     2       scsi_eh_0       0       0       0       0       2023-03-15 13:25:05.748902 UTC  Disabled
0xf4be8000      103     103     2       scsi_eh_1       0       0       0       0       2023-03-15 13:25:05.752885 UTC  Disabled
0xf4becb40      104     104     2       scsi_tmf_1      0       0       0       0       2023-03-15 13:25:05.756135 UTC  Disabled
0xf4beb5c0      105     105     2       scsi_eh_2       0       0       0       0       2023-03-15 13:25:05.756499 UTC  Disabled
0xf64b4b40      106     106     2       scsi_tmf_2      0       0       0       0       2023-03-15 13:25:05.756513 UTC  Disabled
0xf4a55600      108     108     2       scsi_tmf_0      0       0       0       0       2023-03-15 13:25:05.757558 UTC  Disabled
0xf6664080      113     113     2       kworker/1:1H    0       0       0       0       2023-03-15 13:25:06.091620 UTC  Disabled
0xf6662b00      136     136     2       kworker/0:2     0       0       0       0       2023-03-15 13:25:06.142868 UTC  Disabled
0xf6666b80      138     138     2       kworker/0:1H    0       0       0       0       2023-03-15 13:25:06.700590 UTC  Disabled
0xf6660ac0      166     166     2       kworker/u5:0    0       0       0       0       2023-03-15 13:25:07.623253 UTC  Disabled
0xf6664b40      168     168     2       jbd2/sda1-8     0       0       0       0       2023-03-15 13:25:07.675683 UTC  Disabled
0xf6660000      169     169     2       ext4-rsv-conver 0       0       0       0       2023-03-15 13:25:07.675890 UTC  Disabled
0xf4a52040      202     202     1       systemd-journal 0       0       0       0       2023-03-15 13:25:08.048522 UTC  Disabled
0xf5d0c080      219     219     1       systemd-udevd   0       0       0       0       2023-03-15 13:25:08.147251 UTC  Disabled
0xf5d09580      241     241     1       systemd-timesyn 101     102     101     102     2023-03-15 13:25:08.282660 UTC  Disabled
0xf5d08000      262     262     2       ttm_swap        0       0       0       0       2023-03-15 13:25:08.383345 UTC  Disabled
0xf5d0b5c0      263     263     2       irq/18-vmwgfx   0       0       0       0       2023-03-15 13:25:08.387636 UTC  Disabled
0xf64a1580      330     330     1       systemd-logind  0       0       0       0       2023-03-15 13:25:08.581727 UTC  Disabled
0xf64a6b80      332     332     1       rsyslogd        0       0       0       0       2023-03-15 13:25:08.583059 UTC  Disabled
0xf64a2b00      335     335     1       dbus-daemon     104     110     104     110     2023-03-15 13:25:08.585553 UTC  Disabled
0xf64a60c0      339     339     1       cron    0       0       0       0       2023-03-15 13:25:08.597762 UTC  Disabled
0xf38eab00      348     348     1       dhclient        0       0       0       0       2023-03-15 13:25:08.633962 UTC  Disabled
0xf64a0000      350     350     1       sshd    0       0       0       0       2023-03-15 13:25:08.654858 UTC  Disabled
0xf64a4b40      351     351     1       login   0       0       0       0       2023-03-15 13:25:08.656266 UTC  Disabled
0xf5d0ab00      374     374     1       systemd 0       0       0       0       2023-03-15 13:25:11.376197 UTC  Disabled
0xf5d08ac0      375     375     374     (sd-pam)        0       0       0       0       2023-03-15 13:25:11.381435 UTC  Disabled
0xf64a35c0      385     385     351     bash    0       0       0       0       2023-03-15 13:25:11.591839 UTC  Disabled
0xf5d0d600      392     392     350     sshd    0       0       0       0       2023-03-15 13:26:14.141124 UTC  Disabled
0xf64a5600      395     395     1       systemd 1000    1000    1000    1000    2023-03-15 13:26:17.441770 UTC  Disabled
0xf4a52b00      396     396     395     (sd-pam)        1000    1000    1000    1000    2023-03-15 13:26:17.447031 UTC  Disabled
0xf3561580      409     409     392     sshd    1000    1000    1000    1000    2023-03-15 13:26:17.494809 UTC  Disabled
0xf35660c0      410     410     409     bash    1000    1000    1000    1000    2023-03-15 13:26:17.554898 UTC  Disabled
0xf327a040      606     606     410     su      1000    1000    0       1000    2023-03-15 13:29:18.171496 UTC  Disabled
0xf3560000      607     607     606     bash    0       0       0       0       2023-03-15 13:29:24.323004 UTC  Disabled
0xf4a56b80      633     633     2       kworker/u4:0    0       0       0       0       2023-03-15 13:31:16.675558 UTC  Disabled
0xf4938ac0      8912    8912    2       kworker/0:1     0       0       0       0       2023-03-15 13:40:43.748058 UTC  Disabled
0xf4a50000      10483   10483   2       kworker/1:0     0       0       0       0       2023-03-15 18:31:16.768512 UTC  Disabled
0xf4a535c0      10538   10538   2       kworker/u4:2    0       0       0       0       2023-03-15 18:41:38.565089 UTC  Disabled
0xf493a040      10585   10585   2       kworker/1:1     0       0       0       0       2023-03-15 18:52:00.932717 UTC  Disabled
0xf6665600      10597   10597   2       kworker/u4:1    0       0       0       0       2023-03-15 18:55:40.101714 UTC  Disabled
0xf66635c0      10603   10603   2       kworker/1:2     0       0       0       0       2023-03-15 18:57:12.843642 UTC  Disabled
0xf3440000      11218   11218   607     insmod  0       0       0       0       2023-03-15 18:59:29.561172 UTC  Disabled
```

### linux.psscan.PsScan

```bash
❯ python3 vol.py -f ram.lime linux.psscan.PsScan
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
OFFSET (P)      PID     TID     PPID    COMM    EXIT_STATE

0x1cb51bf       9027    9027    10488   rm      EXIT_DEAD
0x1cb5c7f       9025    9025    10488   ip      EXIT_DEAD
0x1cb673f       9028    9028    10488   chown   EXIT_DEAD
0x1ddc1ff       105     105     2       scsi_eh_2       TASK_RUNNING
0x1ddccbf       241     284     1       sd-resolve      TASK_RUNNING
0x1ddd77f       104     104     2       scsi_tmf_1      TASK_RUNNING
0x1dde23f       300     300     1       swapon  EXIT_DEAD
0x1ddecff       56      56      2       kworker/dying   EXIT_DEAD
0x1ddf7bf       101     101     2       ata_sff TASK_RUNNING
0x2063c3f       10488   10488   348     T�F2#   EXIT_DEAD
0x242077f       331     331     286     setfont EXIT_DEAD
0x242123f       341     341     286     setfont EXIT_DEAD
0x2421cff       326     326     323     gzip    EXIT_DEAD
0x24227bf       344     344     286     mkdir   EXIT_DEAD
0x25f7c3f       262     262     2       �lK"|�i�;
�V��=�  TASK_RUNNING
0x26b94bd       393     393     392             EXIT_DEAD
0x2c1083b       9028    9028    10488   v�fȑ�ry!4��
                                                   5    EXIT_DEAD
0x3c9688b       1654384128      100     0               TASK_RUNNING
<snip>
```

### linux.pstree.PsTree

```bash
❯ python3 vol.py -f ram.lime linux.pstree.PsTree
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
OFFSET (V)      PID     TID     PPID    COMM

0xf491cb40      1       1       0       systemd
* 0xf4a52040    202     202     1       systemd-journal
* 0xf5d0c080    219     219     1       systemd-udevd
* 0xf5d09580    241     241     1       systemd-timesyn
* 0xf64a1580    330     330     1       systemd-logind
* 0xf64a6b80    332     332     1       rsyslogd
* 0xf64a2b00    335     335     1       dbus-daemon
* 0xf64a60c0    339     339     1       cron
* 0xf38eab00    348     348     1       dhclient
* 0xf64a0000    350     350     1       sshd
** 0xf5d0d600   392     392     350     sshd
*** 0xf3561580  409     409     392     sshd
**** 0xf35660c0 410     410     409     bash
***** 0xf327a040        606     606     410     su
****** 0xf3560000       607     607     606     bash
******* 0xf3440000      11218   11218   607     insmod
* 0xf64a4b40    351     351     1       login
** 0xf64a35c0   385     385     351     bash
* 0xf5d0ab00    374     374     1       systemd
** 0xf5d08ac0   375     375     374     (sd-pam)
* 0xf64a5600    395     395     1       systemd
** 0xf4a52b00   396     396     395     (sd-pam)
0xf4918ac0      2       2       0       kthreadd
* 0xf4919580    3       3       2       rcu_gp
* 0xf491b5c0    4       4       2       rcu_par_gp
* 0xf4918000    6       6       2       kworker/0:0H
* 0xf491a040    8       8       2       mm_percpu_wq
* 0xf491e0c0    9       9       2       ksoftirqd/0
* 0xf491eb80    10      10      2       rcu_sched
* 0xf491ab00    11      11      2       rcu_bh
* 0xf493cb40    12      12      2       migration/0
* 0xf493b5c0    14      14      2       cpuhp/0
* 0xf493c080    15      15      2       cpuhp/1
* 0xf4938000    16      16      2       migration/1
* 0xf493d600    17      17      2       ksoftirqd/1
* 0xf493e0c0    19      19      2       kworker/1:0H
* 0xf493eb80    20      20      2       kdevtmpfs
* 0xf493ab00    21      21      2       netns
* 0xf49c8000    22      22      2       kauditd
* 0xf49cd600    23      23      2       khungtaskd
* 0xf49ca040    24      24      2       oom_reaper
* 0xf49ce0c0    25      25      2       writeback
* 0xf49ceb80    26      26      2       kcompactd0
* 0xf49cab00    27      27      2       ksmd
* 0xf49ccb40    28      28      2       khugepaged
* 0xf49c8ac0    29      29      2       crypto
* 0xf49c9580    30      30      2       kintegrityd
* 0xf49cb5c0    31      31      2       kblockd
* 0xf49cc080    32      32      2       edac-poller
* 0xf4a50ac0    33      33      2       devfreq_wq
* 0xf4a51580    34      34      2       watchdogd
* 0xf4a54080    36      36      2       kswapd0
* 0xf4be8ac0    54      54      2       kthrotld
* 0xf4beab00    55      55      2       ipv6_addrconf
* 0xf64a2040    65      65      2       kstrp
* 0xf4beeb80    101     101     2       ata_sff
* 0xf4a560c0    102     102     2       scsi_eh_0
* 0xf4be8000    103     103     2       scsi_eh_1
* 0xf4becb40    104     104     2       scsi_tmf_1
* 0xf4beb5c0    105     105     2       scsi_eh_2
* 0xf64b4b40    106     106     2       scsi_tmf_2
* 0xf4a55600    108     108     2       scsi_tmf_0
* 0xf6664080    113     113     2       kworker/1:1H
* 0xf6662b00    136     136     2       kworker/0:2
* 0xf6666b80    138     138     2       kworker/0:1H
* 0xf6660ac0    166     166     2       kworker/u5:0
* 0xf6664b40    168     168     2       jbd2/sda1-8
* 0xf6660000    169     169     2       ext4-rsv-conver
* 0xf5d08000    262     262     2       ttm_swap
* 0xf5d0b5c0    263     263     2       irq/18-vmwgfx
* 0xf4a56b80    633     633     2       kworker/u4:0
* 0xf4938ac0    8912    8912    2       kworker/0:1
* 0xf4a50000    10483   10483   2       kworker/1:0
* 0xf4a535c0    10538   10538   2       kworker/u4:2
* 0xf493a040    10585   10585   2       kworker/1:1
* 0xf6665600    10597   10597   2       kworker/u4:1
* 0xf66635c0    10603   10603   2       kworker/1:2
```

### linux.sockstat.Sockstat

```bash
❯ python3 vol.py -f ram.lime linux.sockstat.Sockstat
Volatility 3 Framework 2.20.0
Progress:  100.00               Stacking attempts finished                 
NetNS   Process Name    PID     TID     FD      Sock Offset     Family  Type    Proto   Source Addr     Source Port     Destination Addr        Destination Port        State   Filter

4026531992      systemd 1       1       9       0xf6211800      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       1       group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd 1       1       16      0xf647d200      AF_UNIX DGRAM   -       /run/systemd/notify     10498   -       -       UNCONNECTED     -
4026531992      systemd 1       1       17      0xf647c900      AF_UNIX DGRAM   -       -       10500   -       10501   UNCONNECTED     -
4026531992      systemd 1       1       18      0xf647cf00      AF_UNIX DGRAM   -       -       10501   -       10500   UNCONNECTED     -
4026531992      systemd 1       1       19      0xf647ea00      AF_UNIX STREAM  -       /run/systemd/private    10502   -       -       LISTEN  -
4026531992      systemd 1       1       23      0xf3b57600      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13866   -       13312   ESTABLISHED     -
4026531992      systemd 1       1       26      0xf647c600      AF_UNIX SEQPACKET       -       /run/udev/control       10509   -       -       UNCONNECTED     -
4026531992      systemd 1       1       27      0xf647e100      AF_UNIX STREAM  -       /run/systemd/journal/stdout     10512   -       -       LISTEN  -
4026531992      systemd 1       1       28      0xf647e400      AF_UNIX DGRAM   -       /run/systemd/journal/socket     10516   -       -       UNCONNECTED     -
4026531992      systemd 1       1       32      0xf647de00      AF_UNIX STREAM  -       /run/systemd/fsck.progress      10536   -       -       LISTEN  -
4026531992      systemd 1       1       33      0xf5cbf800      AF_NETLINK      RAW     NETLINK_AUDIT   groups:0x00000001       1       group:0x00000000        0       UNCONNECTED     -
4026531992      systemd 1       1       34      0xf647c300      AF_UNIX DGRAM   -       /run/systemd/journal/dev-log    10584   -       -       UNCONNECTED     -
4026531992      systemd 1       1       35      0xf5cbc000      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000001       3202108639      group:0x00000000        0       UNCONNECTED     -
4026531992      systemd 1       1       37      0xf647f300      AF_UNIX DGRAM   -       /run/systemd/journal/syslog     10594   -       -       UNCONNECTED     -
4026531992      systemd 1       1       42      0xf5ce1800      AF_NETLINK      RAW     NETLINK_AUDIT   -       4022139371      group:0x00000000        0       UNCONNECTED     -
4026531992      systemd 1       1       47      0xf647f000      AF_UNIX DGRAM   -       -       10884   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd 1       1       48      0xf64d3300      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13414   -       -       LISTEN  -
4026531992      systemd 1       1       49      0xf5eaf600      AF_UNIX STREAM  -       /run/systemd/journal/stdout     11602   -       11508   ESTABLISHED     -
4026531992      systemd 1       1       50      0xf5fdcc00      AF_UNIX STREAM  -       /run/systemd/journal/stdout     11824   -       11161   ESTABLISHED     -
4026531992      systemd 1       1       51      0xf35aa100      AF_UNIX STREAM  -       /run/systemd/journal/stdout     14034   -       14538   ESTABLISHED     -
4026531992      systemd 1       1       57      0xf64d1e00      AF_UNIX STREAM  -       -       13440   /var/run/dbus/system_bus_socket 13704   ESTABLISHED     -
4026531992      systemd 1       1       58      0xf39f1800      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13803   -       13802   ESTABLISHED     -
4026531992      systemd 1       1       60      0xf3902400      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13559   -       13558   ESTABLISHED     -
4026531992      systemd 1       1       61      0xf3907c00      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13561   -       12969   ESTABLISHED     -
4026531992      systemd 1       1       62      0xf390c900      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13629   -       13628   ESTABLISHED     -
4026531992      systemd-journal 202     202     3       0xf647e100      AF_UNIX STREAM  -       /run/systemd/journal/stdout     10512   -       -       LISTEN  -
4026531992      systemd-journal 202     202     4       0xf647e400      AF_UNIX DGRAM   -       /run/systemd/journal/socket     10516   -       -       UNCONNECTED     -
4026531992      systemd-journal 202     202     5       0xf647c300      AF_UNIX DGRAM   -       /run/systemd/journal/dev-log    10584   -       -       UNCONNECTED     -
4026531992      systemd-journal 202     202     6       0xf5cbf800      AF_NETLINK      RAW     NETLINK_AUDIT   groups:0x00000001       1       group:0x00000000        0       UNCONNECTED     -
4026531992      systemd-journal 202     202     14      0xf64d0300      AF_UNIX DGRAM   -       -       11318   /run/systemd/notify     10498   UNCONNECTED     -
4026531992      systemd-journal 202     202     17      0xf39f1800      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13803   -       13802   ESTABLISHED     -
4026531992      systemd-journal 202     202     18      0xf5eaf600      AF_UNIX STREAM  -       /run/systemd/journal/stdout     11602   -       11508   ESTABLISHED     -
4026531992      systemd-journal 202     202     19      0xf5fdcc00      AF_UNIX STREAM  -       /run/systemd/journal/stdout     11824   -       11161   ESTABLISHED     -
4026531992      systemd-journal 202     202     20      0xf3b57600      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13866   -       13312   ESTABLISHED     -
4026531992      systemd-journal 202     202     21      0xf35aa100      AF_UNIX STREAM  -       /run/systemd/journal/stdout     14034   -       14538   ESTABLISHED     -
4026531992      systemd-journal 202     202     22      0xf3902400      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13559   -       13558   ESTABLISHED     -
4026531992      systemd-journal 202     202     23      0xf3907c00      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13561   -       12969   ESTABLISHED     -
4026531992      systemd-journal 202     202     24      0xf390c900      AF_UNIX STREAM  -       /run/systemd/journal/stdout     13629   -       13628   ESTABLISHED     -
4026531992      systemd-udevd   219     219     1       0xf64d1800      AF_UNIX STREAM  -       -       11508   /run/systemd/journal/stdout     11602   ESTABLISHED     -
4026531992      systemd-udevd   219     219     2       0xf64d1800      AF_UNIX STREAM  -       -       11508   /run/systemd/journal/stdout     11602   ESTABLISHED     -
4026531992      systemd-udevd   219     219     3       0xf5cbc000      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000001       3202108639      group:0x00000000        0       UNCONNECTED     -
4026531992      systemd-udevd   219     219     4       0xf647c600      AF_UNIX SEQPACKET       -       /run/udev/control       10509   -       -       UNCONNECTED     -
4026531992      systemd-udevd   219     219     5       0xf5eacc00      AF_UNIX DGRAM   -       -       11582   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd-udevd   219     219     6       0xf5eac300      AF_UNIX DGRAM   -       -       11584   -       11585   UNCONNECTED     -
4026531992      systemd-udevd   219     219     7       0xf5eaea00      AF_UNIX DGRAM   -       -       11585   -       11584   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     1       0xf647c000      AF_UNIX STREAM  -       -       11161   /run/systemd/journal/stdout     11824   ESTABLISHED     -
4026531992      systemd-timesyn 241     241     2       0xf647c000      AF_UNIX STREAM  -       -       11161   /run/systemd/journal/stdout     11824   ESTABLISHED     -
4026531992      systemd-timesyn 241     241     3       0xf3877c00      AF_UNIX DGRAM   -       -       12219   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     7       0xf3874900      AF_UNIX DGRAM   -       -       12221   -       12222   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     8       0xf3874c00      AF_UNIX DGRAM   -       -       12222   -       12221   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     9       0xf3875b00      AF_UNIX DGRAM   -       -       12223   -       12224   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     10      0xf3876100      AF_UNIX DGRAM   -       -       12224   -       12223   UNCONNECTED     -
4026531992      systemd-timesyn 241     241     15      0xf38a4900      AF_UNIX STREAM  -       -       13422   /var/run/dbus/system_bus_socket 13703   ESTABLISHED     -
4026531992      sd-resolve      241     284     1       0xf647c000      AF_UNIX STREAM  -       -       11161   /run/systemd/journal/stdout     11824   ESTABLISHED     -
4026531992      sd-resolve      241     284     2       0xf647c000      AF_UNIX STREAM  -       -       11161   /run/systemd/journal/stdout     11824   ESTABLISHED     -
4026531992      sd-resolve      241     284     3       0xf3877c00      AF_UNIX DGRAM   -       -       12219   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      sd-resolve      241     284     7       0xf3874900      AF_UNIX DGRAM   -       -       12221   -       12222   UNCONNECTED     -
4026531992      sd-resolve      241     284     8       0xf3874c00      AF_UNIX DGRAM   -       -       12222   -       12221   UNCONNECTED     -
4026531992      sd-resolve      241     284     9       0xf3875b00      AF_UNIX DGRAM   -       -       12223   -       12224   UNCONNECTED     -
4026531992      sd-resolve      241     284     10      0xf3876100      AF_UNIX DGRAM   -       -       12224   -       12223   UNCONNECTED     -
4026531992      sd-resolve      241     284     15      0xf38a4900      AF_UNIX STREAM  -       -       13422   /var/run/dbus/system_bus_socket 13703   ESTABLISHED     -
4026531992      systemd-logind  330     330     1       0xf64d1b00      AF_UNIX STREAM  -       -       13558   /run/systemd/journal/stdout     13559   ESTABLISHED     -
4026531992      systemd-logind  330     330     2       0xf64d1b00      AF_UNIX STREAM  -       -       13558   /run/systemd/journal/stdout     13559   ESTABLISHED     -
4026531992      systemd-logind  330     330     3       0xf3901800      AF_UNIX DGRAM   -       -       13648   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd-logind  330     330     8       0xf3970000      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       330     group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd-logind  330     330     11      0xf3971800      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       3103251597      group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd-logind  330     330     12      0xf3970800      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       3022121101      group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd-logind  330     330     13      0xf3973c00      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       2279401286      group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd-logind  330     330     14      0xf3903900      AF_UNIX STREAM  -       -       13681   /var/run/dbus/system_bus_socket 13705   ESTABLISHED     -
4026531992      rsyslogd        332     332     3       0xf647f300      AF_UNIX DGRAM   -       /run/systemd/journal/syslog     10594   -       -       UNCONNECTED     -
4026531992      rsyslogd        332     332     6       0xf3933000      AF_UNIX DGRAM   -       -       12992   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      in:imuxsock     332     345     3       0xf647f300      AF_UNIX DGRAM   -       /run/systemd/journal/syslog     10594   -       -       UNCONNECTED     -
4026531992      in:imuxsock     332     345     6       0xf3933000      AF_UNIX DGRAM   -       -       12992   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      in:imklog       332     346     3       0xf647f300      AF_UNIX DGRAM   -       /run/systemd/journal/syslog     10594   -       -       UNCONNECTED     -
4026531992      in:imklog       332     346     6       0xf3933000      AF_UNIX DGRAM   -       -       12992   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      rs:main Q:Reg   332     347     3       0xf647f300      AF_UNIX DGRAM   -       /run/systemd/journal/syslog     10594   -       -       UNCONNECTED     -
4026531992      rs:main Q:Reg   332     347     6       0xf3933000      AF_UNIX DGRAM   -       -       12992   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      dbus-daemon     335     335     1       0xf647ed00      AF_UNIX STREAM  -       -       12969   /run/systemd/journal/stdout     13561   ESTABLISHED     -
4026531992      dbus-daemon     335     335     2       0xf647ed00      AF_UNIX STREAM  -       -       12969   /run/systemd/journal/stdout     13561   ESTABLISHED     -
4026531992      dbus-daemon     335     335     3       0xf64d3300      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13414   -       -       LISTEN  -
4026531992      dbus-daemon     335     335     5       0xf3971400      AF_NETLINK      RAW     NETLINK_AUDIT   -       0       group:0x00000000        0       UNCONNECTED     -
4026531992      dbus-daemon     335     335     7       0xf399a700      AF_UNIX STREAM  -       -       13701   -       13702   ESTABLISHED     -
4026531992      dbus-daemon     335     335     8       0xf3999200      AF_UNIX STREAM  -       -       13702   -       13701   ESTABLISHED     -
4026531992      dbus-daemon     335     335     9       0xf38a7300      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13703   -       13422   ESTABLISHED     -
4026531992      dbus-daemon     335     335     10      0xf64d3000      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13704   -       13440   ESTABLISHED     -
4026531992      dbus-daemon     335     335     11      0xf3901e00      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13705   -       13681   ESTABLISHED     -
4026531992      dbus-daemon     335     335     13      0xf3b55500      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 13883   -       14374   ESTABLISHED     -
4026531992      dbus-daemon     335     335     14      0xf35a9500      AF_UNIX STREAM  -       /var/run/dbus/system_bus_socket 14569   -       14568   ESTABLISHED     -
4026531992      cron    339     339     1       0xf64d3900      AF_UNIX STREAM  -       -       13628   /run/systemd/journal/stdout     13629   ESTABLISHED     -
4026531992      cron    339     339     2       0xf64d3900      AF_UNIX STREAM  -       -       13628   /run/systemd/journal/stdout     13629   ESTABLISHED     -
4026531992      cron    339     339     4       0xf398a400      AF_UNIX DGRAM   -       -       12994   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      dhclient        348     348     3       0xf588e100      AF_UNIX DGRAM   -       -       13696   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      dhclient        348     348     6       0xf5f0f800      AF_PACKET       RAW     ETH_P_ALL       enp0s3  -       -       -       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      dhclient        348     348     7       0xf5fe1a00      AF_INET DGRAM   UDP     0.0.0.0 68      0.0.0.0 0       UNCONNECTED     -
4026531992      sshd    350     350     1       0xf39f1200      AF_UNIX STREAM  -       -       13802   /run/systemd/journal/stdout     13803   ESTABLISHED     -
4026531992      sshd    350     350     2       0xf39f1200      AF_UNIX STREAM  -       -       13802   /run/systemd/journal/stdout     13803   ESTABLISHED     -
4026531992      sshd    350     350     3       0xf3a886c0      AF_INET STREAM  TCP     0.0.0.0 22      0.0.0.0 0       LISTEN  -
4026531992      sshd    350     350     4       0xf3a95e40      AF_INET6        STREAM  TCP     ::      22      ::      0       LISTEN  -
4026531992      login   351     351     3       0xf3ab7600      AF_UNIX DGRAM   -       -       13164   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      systemd 374     374     1       0xf647e700      AF_UNIX STREAM  -       -       13312   /run/systemd/journal/stdout     13866   ESTABLISHED     -
4026531992      systemd 374     374     2       0xf647e700      AF_UNIX STREAM  -       -       13312   /run/systemd/journal/stdout     13866   ESTABLISHED     -
4026531992      systemd 374     374     3       0xf3b54c00      AF_UNIX DGRAM   -       -       14349   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd 374     374     9       0xf3b50c00      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       374     group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd 374     374     12      0xf3b54f00      AF_UNIX STREAM  -       /run/user/0/gnupg/S.gpg-agent.browser   14378   -       -       LISTEN  -
4026531992      systemd 374     374     16      0xf3b57900      AF_UNIX DGRAM   -       /run/user/0/systemd/notify      14368   -       -       UNCONNECTED     -
4026531992      systemd 374     374     17      0xf3b56400      AF_UNIX DGRAM   -       -       14370   -       14371   UNCONNECTED     -
4026531992      systemd 374     374     18      0xf3b54600      AF_UNIX DGRAM   -       -       14371   -       14370   UNCONNECTED     -
4026531992      systemd 374     374     19      0xf3b57c00      AF_UNIX STREAM  -       /run/user/0/systemd/private     14372   -       -       LISTEN  -
4026531992      systemd 374     374     20      0xf3b56700      AF_UNIX STREAM  -       -       14374   /var/run/dbus/system_bus_socket 13883   ESTABLISHED     -
4026531992      systemd 374     374     26      0xf3b56d00      AF_UNIX STREAM  -       /run/user/0/gnupg/S.gpg-agent.ssh       14381   -       -       LISTEN  -
4026531992      systemd 374     374     27      0xf3b55e00      AF_UNIX STREAM  -       /run/user/0/gnupg/S.gpg-agent.extra     14383   -       -       LISTEN  -
4026531992      systemd 374     374     28      0xf3b57300      AF_UNIX STREAM  -       /run/user/0/gnupg/S.dirmngr     14385   -       -       LISTEN  -
4026531992      systemd 374     374     29      0xf3b56100      AF_UNIX STREAM  -       /run/user/0/gnupg/S.gpg-agent   14387   -       -       LISTEN  -
4026531992      (sd-pam)        375     375     1       0xf647e700      AF_UNIX STREAM  -       -       13312   /run/systemd/journal/stdout     13866   ESTABLISHED     -
4026531992      (sd-pam)        375     375     2       0xf647e700      AF_UNIX STREAM  -       -       13312   /run/systemd/journal/stdout     13866   ESTABLISHED     -
4026531992      (sd-pam)        375     375     7       0xf3b55800      AF_UNIX DGRAM   -       -       14344   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      sshd    392     392     3       0xf3a89440      AF_INET STREAM  TCP     192.168.10.226  22      192.168.10.20   51295   ESTABLISHED     -
4026531992      sshd    392     392     4       0xf39f2400      AF_UNIX DGRAM   -       -       13954   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      sshd    392     392     6       0xf38fbc00      AF_UNIX STREAM  -       -       14445   -       0       ESTABLISHED     -
4026531992      sshd    392     392     7       0xf64d2d00      AF_UNIX STREAM  -       -       14058   -       14057   ESTABLISHED     -
4026531992      systemd 395     395     1       0xf647d500      AF_UNIX STREAM  -       -       14538   /run/systemd/journal/stdout     14034   ESTABLISHED     -
4026531992      systemd 395     395     2       0xf647d500      AF_UNIX STREAM  -       -       14538   /run/systemd/journal/stdout     14034   ESTABLISHED     -
4026531992      systemd 395     395     3       0xf35a9b00      AF_UNIX DGRAM   -       -       14549   /run/systemd/journal/socket     10516   UNCONNECTED     -
4026531992      systemd 395     395     9       0xf3557400      AF_NETLINK      RAW     NETLINK_KOBJECT_UEVENT  groups:0x00000002       395     group:0x00000000        0       UNCONNECTED     filter_type=socket_filter,bpf_filter_type=cBPF
4026531992      systemd 395     395     12      0xf35a8f00      AF_UNIX STREAM  -       /run/user/1000/gnupg/S.gpg-agent.extra  14573   -       -       LISTEN  -
4026531992      systemd 395     395     16      0xf35a8300      AF_UNIX DGRAM   -       /run/user/1000/systemd/notify   14562   -       -       UNCONNECTED     -
4026531992      systemd 395     395     17      0xf35abc00      AF_UNIX DGRAM   -       -       14564   -       14565   UNCONNECTED     -
4026531992      systemd 395     395     18      0xf35ab600      AF_UNIX DGRAM   -       -       14565   -       14564   UNCONNECTED     -
4026531992      systemd 395     395     19      0xf35a9e00      AF_UNIX STREAM  -       /run/user/1000/systemd/private  14566   -       -       LISTEN  -
4026531992      systemd 395     395     20      0xf35aaa00      AF_UNIX STREAM  -       -       14568   /var/run/dbus/system_bus_socket 14569   ESTABLISHED     -
4026531992      systemd 395     395     26      0xf35ab000      AF_UNIX STREAM  -       /run/user/1000/gnupg/S.dirmngr  14576   -       -       LISTEN  -
4026531992      systemd 395     395     27      0xf35ab900      AF_UNIX STREAM  -       /run/user/1000/gnupg/S.gpg-agent.browser        14578   -       -       LISTEN  -
4026531992      systemd 395     395     28      0xf35aa400      AF_UNIX STREAM  -       /run/user/1000/gnupg/S.gpg-agent        14580   -       -       LISTEN  -
4026531992      systemd 395     395     29      0xf35ab300      AF_UNIX STREAM  -       /run/user/1000/gnupg/S.gpg-agent.ssh    14582   -       -       LISTEN  -
4026531992      (sd-pam)        396     396     1       0xf647d500      AF_UNIX STREAM  -       -       14538   /run/systemd/journal/stdout     14034   ESTABLISHED     -
4026531992      (sd-pam)        396     396     2       0xf647d500      AF_UNIX STREAM  -       -       14538   /run/systemd/journal/stdout     14034   ESTABLISHED     -
4026531992      (sd-pam)        396     396     7       0xf35aad00      AF_UNIX DGRAM   -       -       14544   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      sshd    409     409     3       0xf3a89440      AF_INET STREAM  TCP     192.168.10.226  22      192.168.10.20   51295   ESTABLISHED     -
4026531992      sshd    409     409     4       0xf39f2400      AF_UNIX DGRAM   -       -       13954   /run/systemd/journal/dev-log    10584   UNCONNECTED     -
4026531992      sshd    409     409     5       0xf64d0c00      AF_UNIX STREAM  -       -       14057   -       14058   ESTABLISHED     -
4026531992      sshd    409     409     6       0xf38fbc00      AF_UNIX STREAM  -       -       14445   -       0       ESTABLISHED     -
4026531992      su      606     606     3       0xf3606d00      AF_UNIX DGRAM   -       -       14322   /run/systemd/journal/dev-log    10584   UNCONNECTED     -

```



# Conclusiones

Como ya hemos visto el análisis de memoria RAM en linux nos proporciona información sobre el estado de las tareas que se están ejecutando en el sistema.

En este caso se ha hecho un reapaso de los comandos básicos de Volatility 2 y 3 para realizar análisis de memoria RAM.

Para saber como crear mapas de memoria RAM en linux podemos consultar el post de [Creación de mapas de memoria RAM en linux](https://sproffes.github.io/posts/linuxmemorymaps/).