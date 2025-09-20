---
categories:
- Laboratoires
date: 2025-01-11 13:01:50 +0100
lang: fr
original_lang: es
tags:
- Linux
- privilege escalation
- vulnerability
- cve-2021-3156
title: Baron Samedit - Privilèges scaling dans Linux
---

En janvier 2021, Qualys a publié un article sur son blog expliquant une nouvelle vulnérabilité critique dans le programme Sudo d'Unix.

Cette vulnérabilité était un débordement de mémoire dans le débord de buffer qui permettait à tout utilisateur d'obtenir des privilèges root, sans que le système ait des paramètres incorrects. La chose inquiétante à propos de cet échec est qu'il fonctionne avec la configuration par défaut et affecte tout utilisateur, indépendamment des permissions que vous avez définies dans sudo. Bien que la vulnérabilité ait déjà été corrigée, elle affecte les versions non mises à jour du programme sudo entre 1.8.2 et 1.8.31p2, et entre 1.9.0 et 1.9.5p1, ce qui signifie que cet échec a été présent pendant une décennie.

Le problème a été rapidement résolu, et les versions découpées ont rapidement été distribuées dans les dépôts officiels, de sorte que les systèmes mis à jour ne sont plus vulnérables. Toutefois, dans les systèmes qui n'ont pas encore été mis à jour, cette vulnérabilité demeure très dangereuse.

Cette vulnérabilité, comme le CVE-2019-18634, est liée à un débordement de mémoire dans le programme sudo. Cependant, dans ce cas, c'est un débordement dans le tas, pas dans la pile, comme dans le cas précédent. La pile est une partie de la mémoire qui organise et gère strictement les données clés du programme, tandis que la pile est un espace mémoire plus flexible, utilisé pour l'affectation dynamique. Bien que nous n'approfondirons pas les détails techniques pour garder le contenu accessible, l'important est de comprendre que cette vulnérabilité est extrêmement puissante et affecte un grand nombre de systèmes.

## Comprobación

Premièrement, nous vérifions si le système est vulnérable:

```bash
sudoedit -s '\' $(python3 -c 'print("A"*1000)')
```

- Oui. [Si le système est vulnéarble, nous obtenons une erreur de corruption de la mémoire] (/ actifs / img / messages / baron _ semedit / 20250111 _ 130150 _ 2025-01-11 _ 14-01.png)
_ Si le système est vulnéarble nous obtenons une erreur de corruption de mémoire _

Ce PoC a été découvert par un octet verrouillé :

[Github] (https: / / github.com / lockedbyte / CVE-Exploits / arbre / maître / CVE-2021-3156)

## Explotación

Quand Qualys a annoncé cette vulnérabilité, il n'a pas fourni le code complet pour l'exploiter. Cependant, d'autres chercheurs ont rapidement réussi à recréer l'échec. La première explosion entièrement fonctionnelle qui a été publiée a été développée par un chercheur nommé bl4sty, et son code est disponible à Github. Dans cette pratique, nous utiliserons cette explosion pour tirer parti de la vulnérabilité.

[Github] (https: / / github.com / blasty / CVE-2021-3156)

Avec le dépôt cloné, nous devons compiler le PoC:

```bash
make
```

- Oui. [Compilation d'explosions] (/ actifs / img / messages / baron _ semedit / 20250111 _ 130714 _ 2025-01-11 _ 14-07.png)

```bash
ls -la
```

- Oui. [Liste de fichiers] (/ actifs / img / messages / baron _ semedit / 20250111 _ 130918 _ 2025-01-11 _ 14-09.png)

```bash
./sudo-hax-me-a-sandwich
```

- Oui. [Exécution d'explosions] (/ actifs / img / messages / baron _ semdit / 20250111 _ 131028 _ 2025-01-11 _ 14-10.png)

Comme nous devons sélectionner la version du système, nous pouvons vérifier ce qui suit:

```bash
cat /etc/issue
```

- Oui. [Vérification de la version] (/ actifs / img / messages / baron _ semedit / 20250111 _ 131601 _ 2025-01-11 _ 14-15.png)

Maintenant que nous connaissons la verion spécifique, nous faisons l'explosion:

```bash
./sudo-hax-me-a-sandwich 0
```

- Oui. [Exécution finale de l'explosion] (/ actifs / img / postes / baron _ semedit / 20250111 _ 131727 _ 2025-01-11 _ 14-17.png)

## Explicación

### Explicación del Heap Buffer Overflow

Un débordement de buffer se produit lorsqu'un programme écrit plus de données sur un buffer (une zone de mémoire) qu'il ne peut gérer. Heap est une région de mémoire utilisée pour l'allocation dynamique de la mémoire, c'est-à-dire lorsque le programme doit réserver la mémoire avec souplesse pendant son exécution.

### El funcionamiento de la vulnerabilidad

L'erreur provient de la façon dont sudo gère certains arguments de la ligne de commande lorsqu'il est utilisé pour exécuter d'autres programmes. sudo a une fonction interne qui traite ces arguments, et c'est là que se produit le débordement.

Normalement, lorsque vous utilisez sudo, il est responsable de vérifier que l'utilisateur a les autorisations nécessaires pour exécuter la commande. Si tout va bien, la commande est exécutée avec des privilèges élevés.

L'échec est lié à la façon dont sudo gère la mémoire pour les arguments d'une commande en cours d'exécution. En raison d'un débordement de tampon dans le tas, une zone de mémoire critique peut être écrasée, permettant à un attaquant de modifier le flux de contrôle du programme. En d'autres termes, l'attaquant peut injecter du code arbitraire dans la mémoire du programme et changer son comportement.

### Cómo se explota

Pour exploiter cette vulnérabilité, un attaquant envoie une entrée malveillante dans le sudo qui provoque le débordement du bufer dans le tas. Ce dépassement pourrait corrompre les données clés dans la mémoire du programme, comme la direction de retour d'une fonction ou des variables de contrôle, permettant à l'attaquant d'exécuter un code arbitraire.

Dans ce cas, l'attaquant n'a pas besoin d'être dans un groupe avec des privilèges de sudo, car l'échec ne dépend pas de la configuration de sudoers (le fichier qui détermine qui peut utiliser sudo), mais d'un défaut dans la gestion de la mémoire de sudo.

### Estructura de control del flujo (return address)

L'un des principaux objectifs d'un dépassement de tampon est d'écraser la direction de retour d'une fonction.

Cette adresse est stockée dans la pile, et quand une fonction est terminée, le programme retourne dans la direction qui se trouve dans la variable de retour pour poursuivre l'exécution.

En écraseant la direction de retour, le programme peut être fait pour sauter dans une direction de mémoire arbitraire, plutôt que retour normal à la fonction qui l'a appelé.

Il permet à l'attaquant de rediriger l'exécution du programme vers un code malveillant.

### Variables de control de seguridad (como los punteros a funciones)

Les fonctions de sudo effectuent plusieurs contrôles de sécurité pour s'assurer que l'utilisateur a les bonnes autorisations. Un attaquant peut tenter d'écraser des variables liées au contrôle d'accès, comme des points aux fonctions que ces vérifications effectuent.

Si ces pointeurs sont écrasés, cela pourrait amener le programme à appeler des fonctions malveillantes plutôt que permettre des fonctions de vérification, permettant l'escalade des privilèges.

Ils permettent à l'attaquant d'éviter les vérifications et d'exécuter des commandes avec des privilèges élevés.

### Memoria relacionada con la configuración de sudoers

Permet éventuellement à l'attaquant de manipuler les paramètres pour exécuter des commandes sans autorisation.

### Buffers de argumentos de comando

Ils permettent l'injection de commandes malveillantes pour fonctionner comme racine.

### Punteros a la memoria en el heap

Ils permettent que l'exécution soit redirigée vers un code contrôlé par l'attaquant.

Il s'agit d'un résumé du concept aussi simple que possible pour comprendre son fonctionnement.