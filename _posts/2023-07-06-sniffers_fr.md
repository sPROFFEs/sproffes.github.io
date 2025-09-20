---
categories:
- Reconnaissance
- Sniffers
date: 2024-01-19
lang: fr
original_lang: es
tags:
- sniffers
- wireshark
- tcpdump
- network-analysis
title: Sniffers
---

## Concepto

Dans une interconnexion informatique appelée réseau, l'équipement est un hôte ou un nœud.

Lorsque nous sommes dans ce réseau, nous pouvons échanger des données par câble ou WiFi.

Ces données sont des octets et doivent être interprétées pour les protocoles de réseau utilisés, qui sont un ensemble de règles qui s'appliquent à l'information de réseau pour l'interpréter.

Un sniffer surveille tout le trafic réseau à l'intérieur et à l'extérieur du réseau.

Toutes ces données qui sont échangées avec les différents nœuds ou réseaux Internet sont appelées paquets réseau.

Il y a des moments où nous ne pouvons pas utiliser les techniques de reconnaissance active ou, par exemple, la détection de vulnérabilité ou l'analyse de vulnérabilité, parce que les systèmes connectés au réseau sont si anciens et si sensibles que ce trafic supplémentaire, que le trafic anormal qui génère ces outils de détection active, peut dans certains cas causer l'indisponibilité de l'un quelconque des systèmes et que cela affecte l'infrastructure du réseau ou l'infrastructure technologique en général.

Ainsi, dans ces cas, l'une des options pour essayer de diriger nos attaques un peu plus quand il s'agit d'exploiter une certaine vulnérabilité peut être de prendre un sniffer, de le mettre dans cette infrastructure, simplement copier ce trafic réseau, c'est-à-dire, de surveiller toute l'activité du réseau et selon les protocoles qu'il commence à intercepter.

Selon, par exemple, certaines valeurs qui ont certains champs des couches des paquets réseau, nous pouvons identifier quelles applications sont installées dans les différents nœuds de ce réseau ainsi que quels programmes ils utilisent et quelles versions de ces programmes.

## Wireshark

C'est un outil du plus connu et puissant qui par défaut dans Kali est déjà installé.

- oui. [https: / / www.wireshark.org / télécharger] (/ actifs / img / messages / reconnaissance / 20241126 _ 000918 _ 89-1.png)

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 000924 _ 89-2.png)

Les paquets sont divisés en couches

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 000935 _ 89-3.png)

Pour voir les paquets dans lesquels les noms DNS ont été consultés, cliquez sur la loupe

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 000953 _ 89-4.png)

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 001008 _ 89-5.png)

C'est là que la requête est faite pour résoudre ce nom de domaine

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 001103 _ 89-6.png)

Ici nous voyons les réponses avec les hôtes et leur IP à la fois IPV4 et IPV6 comme vu dans le paquet suivant

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 001128 _ 89-7.png)

Eh bien, vous savez que HTTP va au-dessus de la couche TCP et plusieurs fois lorsque nous échangeons des informations qui sont très grandes, comme peut être par exemple un site Web, à la fin nous faisons une demande au serveur web, nous lui disons.

Envoie-moi ce site.

Le serveur Web vous envoie sur la page Web.

Mais bien sûr, un site Web est beaucoup d'informations.

Ok, donc les paquets réseau ou la quantité d'information qui va dans un peu de ristra qui est échangé, est limitée dans la taille. Ce n'est pas une taille infinie. Et donc, si le site ou l'information que nous échangeons est trop grand, nous ne pouvons pas tout envoyer dans le même segment, dans le même ristra bit ou dans le même paquet réseau.

Donc, nous devons fragmenter ces informations d'une manière ou d'une autre et les envoyer dans différents segments ou dans différents paquets réseau.

## TCPDump

Il diffère de wireshark en ce qu'il utilise une interface de console de commande.

[] (/ actifs / img / postes / reconnaissance / 20241126 _ 001708 _ 90-1.png)

Ce ne sont que quelques-unes des options que vous offrez, dans votre documentation vous pouvez trouver beaucoup plus.

```bash
sudo tcpdump -D
```

- Oui. [Afficher les interfaces réseau] (/ actifs / img / messages / reconnaissance / 20241126 _ 001734 _ 90-2.png)

```bash
sudo tcpdump -i eth0
```

- Oui. [Capture dans l'interface réseau] (/ actifs / img / messages / reconnaissance / 20241126 _ 001804 _ 90-3.png)

Afficher plus d'informations:

```bash
sudo tcpdump -v -i eth0
sudo tcpdump icmp -i eth0
```

- Oui. [Protocoles d'exploitation] (/ actifs / img / messages / reconnaissance / 20241126 _ 001924 _ 90-4.png)

```bash
sudo tcpdump host 185.230.63.107 -i eth0
```

- Oui. [Filtre par adresse d'accueil] (/ actifs / img / messages / reconnaissance / 20241126 _ 001952 _ 90-5.png)

Enregistrer la capture à analyser ultérieurement avec Wireshark

```bash
sudo tcpdump -i eth0 -w Desktop/capture.pcap
```

Ouvrez la capture mais avec les protocoles TCPDump et filter

```bash
sudo nmap -n port 53 -v -r capture.pcap
sudo nmap -n port 80 -v -r capture.pcap | grep gamivo.com
```