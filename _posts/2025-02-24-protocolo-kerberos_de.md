---
categories:
- Theorie
- Active Directory
- Kerberos
date: 2025-02-23 11:00:00 +0000
description: 'Funcionamiento de Kerberos en Active Directory

  '
image:
  alt: Microsoft Active Directory
  path: /assets/img/cabeceras_genericas/microsoft-active-directory.jpg
lang: de
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
title: Kerberos Protokoll in Active Directory
toc: true
---

## ¿QUÉ ES KERBEROS?

Dies ist ein Authentifizierungsprotokoll, das 1983 am MIT für das ATHENA-Projekt entwickelt wurde, dessen Ziele die Integration von:

- SSO (Einzelzeichen)
- Unterstützung von Netzwerkdateisystemen
- Unified grafische Umgebung (X Windows)
- Convention Name Service (wie DNS)

## KERBEROS Y MICROSOFT WINDOWS

In diesem System erfolgt die Domain-basierte Authentifizierung von Nutzern und Hosts durch Kerberos.

Kerberos v5 (RFC1510) wurde in Windows Server 2000 implementiert und NTLM (Windows NT LAN Manager) als Standard-Authentifizierungsoption ersetzt.

NTLM wird derzeit noch als lokaler Authentifizierungsmechanismus (nicht an einem Domino befestigt) verwendet.

Dieses Kerberos Protokoll ist heute das älteste und am häufigsten verwendete Protokoll.

Auf der MIT-Website finden wir einen Dialog zwischen zwei Personen Athena und Euripides geschrieben von den Leuten, die dieses Protokoll entworfen haben, in dem sie diskutieren, wie ein Problem zu lösen ist die endgültige Lösung des Kerberos Protokolls.

[Dialogue] (http: / / web.mit.edu / kerberos / www / dialog.html)

## ¿CÓMO FUNCIONA KERBEROS?

Der Benutzer sendet ein flaches Paket mit seinem * * USER * * * an den Authentifizierungsservice, der normalerweise von einem anderen Paket mit einem * Timestap * * mit dem Benutzerschlüssel verschlüsselt wird,

Der Authentisierungsservice prüft, ob der Benutzer existiert, wenn dies sein * * Passwort * * aus der Datenbank nimmt, einen neuen Sitzungsschlüssel generiert und auch den * * Zuteilung Ticketservice * * Schlüssel übernimmt.

`TICKET GRANTING TIKET -  {sessionkey:username:address:servicename:lifespan:timestamp}`

Es zeigt diese Textkette mit dem * Zuteilung Ticketservice * Schlüssel, ein privater Schlüssel des Dienstes selbst, dass der Benutzer nicht weiß. Darüber hinaus erstellen Sie gleichzeitig ein weiteres zusätzliches Paket mit * SessionKey1 * *, nummeriert es mit dem privaten Schlüssel des Benutzers und all das sendet es an * * Benutzer * * *.

Der Benutzer erhält die Informationen, entschlüsselt das Paket mit seinem privaten Schlüssel. Jetzt haben Sie den Session-Schlüssel, die * * Ticketerteilung Ticket * verschlüsselt durch den privaten * * Ticketerteilung Ticket Service * * und Ihren persönlichen privaten Schlüssel.

Der Benutzer nutzt das * * Ticket-Genehmigungsticket * * um mit dem * * Ticket-Genehmigungs-Service * * * zu interagieren, aber so dass es nicht abgefangen werden kann, ohne vorher einen * Authenticator * erstellen

`AUTHENTICATOR - {username:address} encrypted with session key}`

Und diese Zahlen mit dem * * SessionKey1 * * *.

Dies verhindert, dass, wenn jemand das * * Ticket-Genehmigungsticket * * nicht mit dem * * * Ticket-Genehmigungsticket-Service * * interagieren kann, weil sie den * Authenticator * nicht komponieren konnten, da dies die * SessionKey * erfordert, die zuvor in einem verschlüsselten Paket mit dem persönlichen Schlüssel des Benutzers enthalten war.

Jetzt sendet der Benutzer den * * Zuteilung Ticketservice * * den * Authenticator * verschlüsselt und das * Zuteilungsticket *.

Der * * * Zuteilung Ticket-Service * * verwendet seinen * * privaten Service-Schlüssel * * um die * * Zuteilung Ticket * *, erhalten Sie die * SessionKey * und so entschlüsseln Sie den * Authenticator *, überprüfen Sie, dass der Benutzer, der in der * Zuteilung Ticket * * erscheint die gleiche * Authenticator * Spiel und wenn ja, die Validierung.

Jetzt erstellt der * * Zuteilung Ticketservice * * ein * * Service-Ticket für das Dateisystem * * *. Um dies zu tun, erstellen Sie eine neue * SessionKey2 *, die in den * * * Service-Ticket-Dateien * * und diese Figur mit dem * * privaten Schlüssel des Datei-Service. * *.

Diese neue * SessionKey2 * setzt es in ein anderes Paket und nummeriert es mit * SessionKey1 *, dass es aus der Ticketerteilung erhalten und dass der Benutzer bereits hat.

Senden Sie also das * * Service-Ticket für das * * Dateisystem und das * SessionKey2 * Paket verschlüsselt an den Benutzer.

Der Benutzer entkoppelt den * SessionKey2 * mit dem * SessionKey1 *, erstellt einen neuen * Authenticator 2 * und das gleiche wie zuvor mit dem * SessionKey2 * Sie haben gerade.

Senden Sie den * Authenticator 2 * und das * * Service-Ticket für das Dateisystem * * an den * * Datei-Service * * * *.

Der * * * Dateidienst * * defiguriert das * * Service-Ticket für das * * * Dateisystem, in dem die * SessionKey2 * enthalten ist, mit dem wiederum der * Authenticator 2 * offenbart, vergleicht die Informationen des * * Tickets * * mit dem des * Authenticator 2 * und wenn sie einverstanden sind, kann den Benutzer validieren.

Wenn Sie nun die entsprechenden Daten an den Benutzer senden.

All dies wird ein weiterer Schritt in der Kommunikation mit dem Dateisystem hinzugefügt, da der Dienst den Benutzer authentifizieren kann, aber der Benutzer kann den Dienst nicht authentifizieren, so dass er durch einen falschen Service supplantiert werden kann.

In der * * * Authentifizierung * gegenseitig:

- Ja. Der Benutzer, bevor er den Befehl sendet, um die Dienstdatei zu erhalten, sendet nur den * Authenticator 2 * und das * * Dienstticket für das * * Dateisystem.

- Ja. Der Service führt den gesamten vorherigen Prozess durch, authentifiziert den Benutzer und geht fort, sich zu authentifizieren. Erstellen Sie ein Paket mit einem * * Zeitstempel * *, figurieren Sie es mit * SessionKey2 * (als wäre es ein falscher Service, den es nicht erhalten haben konnte), und senden Sie es an den Benutzer.

- Ja. Der Benutzer entkoppelt das Paket mit dem * * Zeitstempel * * * * und wenn es dies richtig tut, bestätigt dies, dass der * * Dienst der authentische * * und nicht ein Suppler ist, jetzt, wenn Sie den Befehl senden, um den Dienst zu nutzen.

- All dies ist notwendig, um zu wissen, warum Sie bestimmte Schritte angreifen können und nutzen, um bestimmte Daten zu erhalten, die Nutzung der Tickets auszunutzen, sie im Auftrag anderer Benutzer usw. zu verwenden.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image.png)

## ¿CÓMO SE IMPLEMENTA ESTE PROTOCOLO EN ACTIVE DIRECTORY?

Bestimmte Namen, die mit AD verbunden sind, werden während des Kerberos-Authentifizierungsprozesses verwendet.

Wenn wir unsere WS01, WS02 starten,... jede innerhalb der Domain, in der ersten Login-Prompt ist, wo dieser ganze Prozess beginnt und wo der Benutzer bekommt seine * * * TicketGrantingTicket (TGT) * * * *.

Wir öffnen Wireshark und setzen ihn in das private Netz des Dominos.

Wir melden uns in der WS01

In wireshark filtern wir durch Kerberos und sehen:

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-1.png)

Dieses erste Paket sendet dem Benutzer die Authentication-Service-Anfrage an.

Wenn wir die Paketdaten bereitstellen, sehen wir, dass sie den Benutzernamen und die von Ihnen angeforderten Dienste sendet

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-2.png)

Alle ActiveDirectory-Dienste werden durch den Service Principal Name (SPN) identifiziert.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-3.png)

Wenn wir das folgende Paket betrachten, ist ein Fehler aus dem Authentifizierungsdienst, der die Notwendigkeit einer Vor-Authentifizierung anzeigt, und dies liegt daran, dass bei der neuen Implementierung von Kerberos v5 die Benutzerüberprüfung durch eine verschlüsselte TimeStamp mit dem Passwort des Benutzers hinzugefügt wurde.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-4.png)

Der Benutzer sendet eine andere Anfrage, aber diesmal mit einem verschlüsselten Zeitstempel.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-5.png)

Der Service reagiert mit einem Authentication Service Replay (AS-REP) Paket

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-6.png)

In seinem Inhalt sehen wir, dass es das zuvor gesehene Ticket und weitere verschlüsselte Daten, die der verschlüsselte Sessionkey mit dem Passwort des Benutzers ist, beigefügt.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-7.png)

Diese Informationen werden auf den Benutzer aufgeschlüsselt und der Benutzer sendet ein TGS-REQ Paket (Ticketerteilung Serviceanfrage)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-8.png)

Wie wir zuvor gesehen haben, enthält dies die TGT, die Sie zuvor erhalten haben, und einen Authentiker

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-9.png)

Aus dem Service erhalten wir ein TGS-REP (Ticket-Zulassung Service-Replay)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-10.png)

Dieses Paket enthält das Service-Ticket mit dem gleichen Namen und die Geräte, von denen Sie die SessionKey anfordern und verschlüsselte Daten, die dann mit dem Host-Service interagieren.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-11.png)

Wenn Sie uns anschauen, stellt der Benutzer eine weitere Anfrage an ein neues Ticket für den LDAP-Service im Domänencontroller-Host.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-12.png)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-13.png)

Der Service reagiert mit dem neuen Ticket

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-14.png)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-15.png)

Von hier aus sehen wir den Verkehr mit den Dienstleistungen, die bereits vom Host angefordert werden

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-16.png)

Im ersten Paket sehen wir

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-17.png)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-18.png)

Er schickt Ihnen die Servicekarte für LDAP und den Authentiker.

Der Dienst sendet ein gegenseitiges Authentifizierungspaket.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-19.png)

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-20.png)

Das, wenn wir uns erinnern, sind Daten wie ein Zeitstempel verschlüsselt mit dem Sessionkey, den der Benutzer bereits besitzt.

## Lo importante a tener en cuenta

All dies geschieht durch einen Benutzer auf dem Domänencontroller. Dies wird standardmäßig erstellt und krbtgt.

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-21.png)

Das KDC oder KeyDistributionCenter umfasst die Dienste der Authentisierung und den Ticket Gratting-Service.

Dieser Benutzer ist für die Verschlüsselung dieser Pakete und Tickets verantwortlich, da der Schlüssel dieses Benutzers der Schlüssel des TGS ist.

Der Standard-Schlüssel dieses Benutzers ist sehr lang und komplex, so dass es offensichtlich nie zu etwas geändert werden sollte, das sehr einfach zu knacken ist.

Wenn wir die ServicePrincipalNames SPN sehen wollen, können Sie sehen, welche Dienste jeder Computer der Infrastruktur bietet und welche SPN Partner hat.

```powershell
Get-NetComputer -Identity WS01
```

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-22.png)

```powershell
Get-NetComputer -Identity DC01
```

! [alt text] (/ vermögenswerte / img / beiträge / theoria-protocolo-kerberos / image-23.png)