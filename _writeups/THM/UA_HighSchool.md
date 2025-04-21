---
title: U.A High School - TryHackMe
layout: post
permalink: /writeups/THM/UA_HighSchool
date: 2025-04-21 11:00:00 -0000
description: >
  Write up en español para U.A High School - TryHackMe
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sV -Pn -T4 -O 10.10.221.160
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-21 20:34 CAT
Nmap scan report for 10.10.221.160
Host is up (0.053s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 8.2p1 Ubuntu 4ubuntu0.7 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.41 ((Ubuntu))
Device type: general purpose
Running: Linux 4.X
OS CPE: cpe:/o:linux:linux_kernel:4.15
OS details: Linux 4.15
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

