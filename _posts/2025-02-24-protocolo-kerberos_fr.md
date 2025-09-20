---
categories:
- Théorie
- Répertoire actif
- Kerberos
date: 2025-02-23 11:00:00 +0000
description: 'Funcionamiento de Kerberos en Active Directory

  '
image:
  alt: Microsoft Active Directory
  path: /assets/img/cabeceras_genericas/microsoft-active-directory.jpg
lang: fr
math: false
mermaid: false
original_lang: es
pin: false
tags:
- Guía
- Auditoria
- Active Directory
- Windows
- Kerberos
- NTLM
- Hash
- Pass-the-Hash
- Pass-the-Ticket
- AS-REP Roasting
- Golden Ticket
- Silver Ticket
- Silver Ticket
title: Protocole Kerberos dans le répertoire actif
toc: true
---

## ¿QUÉ ES KERBEROS?

Il s'agit d'un protocole d'authentification initialement développé au MIT en 1983 pour le projet ATHENA dont les objectifs comprenaient l'intégration de:

- SSO (Signe unique)
- Prise en charge des systèmes de fichiers réseau
- Environnement graphique unifié (X Windows)
- Service des noms de convention (comme le DNS)

## KERBEROS Y MICROSOFT WINDOWS

Dans ce système, l'authentification par domaine des utilisateurs et des hôtes se fait par Kerberos.

Kerberos v5 (RFC1510) a été implémenté dans le serveur Windows 2000 et remplacé par NTLM (Windows NT LAN Manager) comme option d'authentification par défaut.

NTLM est encore utilisé comme mécanisme d'authentification de machine local (non attaché à un domino).

Ce protocole Kerberos est le protocole le plus ancien et le plus utilisé aujourd'hui.

Sur le site du MIT, nous pouvons trouver un dialogue entre deux personnes Athena et Euripides écrit par les personnes qui ont conçu ce protocole dans lequel ils discutent comment résoudre un problème étant la solution finale du protocole Kerberos.

[Dialogue] (http: / / web.mit.edu / kerberos / www / dialogue.html)

## ¿CÓMO FUNCIONA KERBEROS?

L'utilisateur envoie un paquet plat avec son * * USER * * au service d'authentification normalement accompagné d'un autre paquet avec un * timestap * * chiffré avec la clé utilisateur,

Le service d'authentification vérifie si l'utilisateur existe, si c'est le cas prend son * * mot de passe * * de la base de données, génère une nouvelle clé de session et prend également la * * service de délivrance de ticket * * clé.

`TICKET GRANTING TIKET -  {sessionkey:username:address:servicename:lifespan:timestamp}`

Il figure cette chaîne de texte avec la touche * * accordant le service de billet * *, une clé privée du service lui-même que l'utilisateur ne sait pas. En outre, créer simultanément un autre paquet supplémentaire avec * * SessionKey1 * *, le numéroter avec la clé privée de l'utilisateur et tout cela l'envoie à * * utilisateur * *.

L'utilisateur reçoit les informations, décrypte le paquet avec sa clé privée. Maintenant, vous avez la clé de session, le billet * * accordant * * crypté par le billet privé * * accordant * * et votre clé privée personnelle.

L'utilisateur utilise le ticket d'octroi * * * pour interagir avec le service * * d'octroi de ticket * * mais pour qu'il ne puisse pas être intercepté sans créer d'abord un * Authentificateur *

`AUTHENTICATOR - {username:address} encrypted with session key}`

Et ces chiffres avec la * * SessionKey1 * *.

Cela empêche que, si quelqu'un intercepte le ticket * * n'interagisse pas avec le service * * d'octroi de ticket * * parce qu'il ne pouvait pas composer le * Authentificateur *, car cela nécessite le * SessionKey * précédemment inclus dans un paquet chiffré avec la clé personnelle de l'utilisateur.

Maintenant l'utilisateur envoie le * * service de délivrance de billets * * l'Authentificateur * crypté et le * billet de délivrance *.

Le * * service de billetterie * * utilise sa * * clé de service privé * * pour déchiffrer le * * billetterie * *, obtenir la * SessionKey * et ainsi déchiffrer le * Authentificateur *, vérifier que l'utilisateur qui apparaît dans le * billetterie * * * est le même que le * Authentificateur * correspondant et si oui, la validation.

Maintenant, le service * * d'octroi de billets * * crée un billet * * pour le système de fichiers * *. Pour ce faire, créez une nouvelle * SessionKey2 * qui inclut dans les fichiers de ticket de service * * et cette figure avec la * * clé privée du service de fichiers. * *.

Ce nouveau * SessionKey2 * le met dans un autre paquet et le numéro avec le * SessionKey1 * qu'il a obtenu à partir du ticket d'octroi et que l'utilisateur a déjà.

Envoyez donc le billet de service * * pour le système de fichiers * et le paquet * SessionKey2 * crypté à l'utilisateur.

L'utilisateur découple le * SessionKey2 * avec le * SessionKey1 *, crée un nouveau * Authentificateur 2 * et la même chose qu'avant avec le * SessionKey2 * que vous venez d'obtenir.

Envoyez le * Authentificateur 2 * et le * * ticket de service pour le système de fichiers * * au * * service de fichiers * *.

Le service de fichiers * * * défigure le ticket de service * * pour le système de fichiers * * dans lequel le * SessionKey2 * est contenu avec lequel le * Authentificateur 2 * révèle, compare les informations du * * ticket * * avec celles du * Authentificateur 2 * et si elles sont d'accord peuvent valider l'utilisateur.

Maintenant, si vous envoyez les données correspondantes à l'utilisateur.

À tout cela est ajouté une étape supplémentaire dans la communication avec le système de fichiers que le service peut authentifier l'utilisateur mais l'utilisateur ne peut pas authentifier le service de sorte qu'il peut être supplanté par un faux service.

Dans l'authentification * * * * mutuelle:

- Oui. L'utilisateur avant d'envoyer la commande pour obtenir le fichier de service, envoie seulement le * Authentificateur 2 * et le * * ticket de service pour le système de fichier * *.

- Oui. Le service effectue tout le processus précédent, authentifie l'utilisateur et procède à l'authentification elle-même. Créez un paquet avec un * * horodatage * *, calculez-le avec le * SessionKey2 * (comme s'il s'agissait d'un faux service qu'il n'aurait pas pu obtenir) et envoyez-le à l'utilisateur.

- Oui. L'utilisateur découple le paquet avec le * * timestamp * * et, s'il le fait correctement, il vérifie que le service * * est l'authentique * * et non un suppler, maintenant si vous envoyez la commande pour faire usage du service.

- Tout cela est nécessaire pour savoir pourquoi vous pouvez attaquer certaines étapes et en profiter pour obtenir certaines données, exploiter l'utilisation des tickets, les utiliser pour le compte d'autres utilisateurs, etc.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image.png)

## ¿CÓMO SE IMPLEMENTA ESTE PROTOCOLO EN ACTIVE DIRECTORY?

Certains noms associés à AD sont utilisés pendant le processus d'authentification Kerberos.

Lorsque nous commençons notre WS01, WS02,... tout à l'intérieur du domaine, dans l'invite de connexion initiale est où tout ce processus commence et où l'utilisateur obtient son * * TicketGrantingTicket (TGT) * *.

Nous ouvrons Wireshark et le mettons au réseau privé du domino.

On se connecte au WS01

En fer à repasser, nous filons à travers Kerberos et voyons:

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-1.png)

Ce premier paquet envoie l'utilisateur pour demander le service d'authentification.

Si nous déployons les données du paquet, nous voyons qu'il envoie le nom d'utilisateur et les services que vous demandez

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-2.png)

Tous les services ActiveDirectory sont identifiés par le nom principal du service (SPN).

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-3.png)

Si nous examinons le paquet suivant est une erreur du service d'authentification qui indique la nécessité d'une pré-authentification et c'est parce que dans la nouvelle implémentation de Kerberos v5 l'utilisateur a été vérifié en exigeant un TimeStamp chiffré avec le mot de passe de l'utilisateur.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-4.png)

L'utilisateur envoie une autre demande mais cette fois avec un horodatage chiffré.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-5.png)

Le service répond avec un package de replay de service d'authentification (AS-REP)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-6.png)

Dans son contenu, nous voyons qu'il a joint le ticket que nous avons précédemment vu et une autre donnée chiffrée qui est la clé de session chiffrée avec le mot de passe de l'utilisateur.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-7.png)

Ces informations sont ventilées sur l'utilisateur et l'utilisateur envoie un paquet TGS-REQ (demande de service d'octroi de billets)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-8.png)

Comme nous l'avons vu précédemment, il contient le TGT que vous avez reçu avant et un authentificateur

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-9.png)

Du service nous recevons un TGS-REP (rejouage du service d'octroi de billets)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-10.png)

Ce paquet contient le ticket de service avec le même nom et l'équipement à partir duquel vous demandez et les données chiffrées qui sont la SessionKey puis interagissent avec le service hôte.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-11.png)

Si vous nous regardez, l'utilisateur fait une autre demande pour un nouveau ticket pour le service LDAP dans l'hôte du contrôleur de domaine.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-12.png)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-13.png)

Le service répond avec le nouveau ticket

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-14.png)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-15.png)

De là nous voyons le trafic avec les services qui sont déjà demandés à l'hôte

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-16.png)

Dans le premier paquet, nous voyons

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-17.png)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-18.png)

Il vous envoie le ticket de service pour LDAP et l'authentificateur.

Le service envoie un paquet d'authentification mutuelle.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-19.png)

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-20.png)

Que si nous nous souvenons sont des données comme un horodatage chiffré avec la clé de session que l'utilisateur possède déjà.

## Lo importante a tener en cuenta

Tout cela est fait par un utilisateur sur le contrôleur de domaine. Ceci est créé par défaut et s'appelle krbtgt.

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-21.png)

Le KDC ou KeyDistributionCenter comprend les services d'authentification et le service de grattage des tickets.

Cet utilisateur est responsable du chiffrement de ces paquets et tickets car la clé de cet utilisateur est la clé de la TGS.

La clé par défaut de cet utilisateur est très longue et complexe donc il ne devrait évidemment jamais être changé à quelque chose de très simple à cracker.

Si nous voulons voir le ServicePrincipalNames SPN, vous pouvez voir quels services chaque ordinateur de l'infrastructure offre et quel SPN a des partenaires.

```powershell
Get-NetComputer -Identity WS01
```

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-22.png)

```powershell
Get-NetComputer -Identity DC01
```

- oui. [texte alternatif] (/ actifs / img / messages / théoria-protocolo-kerberos / image-23.png)