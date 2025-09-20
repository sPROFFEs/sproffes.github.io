---
categories:
- Anerkennung
- Sniffs
date: 2024-01-19
lang: de
original_lang: es
tags:
- sniffers
- wireshark
- tcpdump
- network-analysis
title: Sniffs
---

## Concepto

Innerhalb einer Computerverbindung, die als Netzwerk bezeichnet wird, sind die Geräte Hosts oder Knoten.

Wenn wir in diesem Netzwerk sind, können wir Daten per Kabel oder WLAN austauschen.

Diese Daten sind Bytes und müssen interpretiert werden, für welche Netzwerkprotokolle verwendet werden, was eine Reihe von Regeln ist, die für Netzwerkinformationen gelten, um sie zu interpretieren.

Ein Sniffer überwacht den gesamten Netzwerkverkehr sowohl in als auch außerhalb des Netzwerks.

Alle diese Daten, die mit den verschiedenen Knoten oder Internet-Netzwerken ausgetauscht werden, werden Netzwerkpakete genannt.

Es gibt Zeiten, in denen wir keine aktiven Erkennungstechniken oder z.B. Verwundbarkeitserkennungs- oder Verwundbarkeitsanalysen verwenden können, weil die Systeme, die mit dem Netzwerk verbunden sind, so alt und so empfindlich sind, dass dieser zusätzliche Verkehr, der anomale Verkehr, der diese aktiven Erkennungstools erzeugt, zum Teil die Unverfügbarkeit eines der Systeme hervorrufen kann und dies die Netzinfrastruktur oder die technologische Infrastruktur im Allgemeinen beeinträchtigt.

In diesen Fällen kann eine der Möglichkeiten sein, unsere Angriffe ein wenig mehr zu lenken, wenn es darum geht, eine gewisse Verwundbarkeit auszunutzen, einen Schnüffler zu nehmen, ihn in diese Infrastruktur zu setzen, einfach zu kopieren, dass der Netzverkehr, d.h. die Überwachung der gesamten Netzwerkaktivität und abhängig von den Protokollen, die es zu abfangen beginnt.

Je nach beispielsweise einigen Werten, die bestimmte Felder der Schichten der Netzwerkpakete haben, können wir erkennen, welche Anwendungen in den verschiedenen Knoten dieses Netzwerks installiert sind und welche Programme sie verwenden und welche Versionen dieser Programme.

## Wireshark

Es ist ein Werkzeug der bekanntesten und mächtigsten, dass standardmäßig in Kali bereits installiert ist.

! [https: / / www.wireshark.org / download] (/ assets / img / beiträge / anerkennung / 20241126 _ 000918 _ 89-1.png)

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 000924 _ 89-2.png)

Die Packungen sind in Schichten unterteilt

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 000935 _ 89-3.png)

Um die Pakete anzuzeigen, in denen die DNS-Namen konsultiert wurden, klicken wir auf die Lupe

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 000953 _ 89-4.png)

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 001008 _ 89-5.png)

Hier wird die Anforderung gestellt, diesen Domainnamen zu beheben

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 001103 _ 89-6.png)

Hier sehen wir die Antworten mit den Hosts und deren IPV4 und IPV6 im folgenden Paket

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 001128 _ 89-7.png)

Nun, Sie wissen, dass HTTP über der TCP-Schicht geht und viele Male, wenn wir Informationen austauschen, die sehr groß sind, wie zum Beispiel eine Website, am Ende stellen wir eine Anfrage an den Webserver, sagen wir ihm.

Schick mir die Website.

Der Webserver sendet Sie an die Webseite.

Aber natürlich ist eine Website eine Menge Informationen.

Okay, also die Netzwerkpakete oder die Menge an Informationen, die in ein bisschen ristra gehen, die ausgetauscht wird, ist in der Größe begrenzt. Es ist keine unendliche Größe. Und wenn die Website oder Informationen, die wir austauschen, zu groß ist, können wir sie nicht alle im selben Segment, im gleichen Bit ristra oder im gleichen Netzwerkpaket senden.

So müssen wir diese Informationen irgendwie fragmentieren und in verschiedenen Segmenten oder in verschiedenen Netzwerkpaketen senden.

## TCPDump

Es unterscheidet sich von wireshark, indem es eine Befehlskonsole-Schnittstelle verwendet.

! [] (/ vermögenswerte / img / beiträge / anerkennung / 20241126 _ 001708 _ 90-1.png)

Dies sind nur einige der angebotenen Optionen, in Ihrer Dokumentation finden Sie viele mehr.

```bash
sudo tcpdump -D
```

! [Netzwerkschnittstellen anzeigen] (/ Assets / img / Beiträge / Erkennung / 20241126 _ 001734 _ 90-2.png)

```bash
sudo tcpdump -i eth0
```

! [Erfassen in Netzwerkschnittstelle] (/ Vermögenswerte / img / Beiträge / Erkennung / 20241126 _ 001804 _ 90-3.png)

Mehr Informationen:

```bash
sudo tcpdump -v -i eth0
sudo tcpdump icmp -i eth0
```

! [Filterprotokolle] (/ Vermögenswerte / img / Beiträge / Erkennung / 20241126 _ 001924 _ 90-4.png)

```bash
sudo tcpdump host 185.230.63.107 -i eth0
```

! [Filter per Host-Adresse] (/ Vermögenswerte / img / Beiträge / Anerkennung / 20241126 _ 001952 _ 90-5.png)

Speichern Sie die Aufnahme, die später mit Wireshark analysiert werden soll

```bash
sudo tcpdump -i eth0 -w Desktop/capture.pcap
```

Öffnen Sie die Erfassung, aber mit TCPDump und Filterprotokollen

```bash
sudo nmap -n port 53 -v -r capture.pcap
sudo nmap -n port 80 -v -r capture.pcap | grep gamivo.com
```