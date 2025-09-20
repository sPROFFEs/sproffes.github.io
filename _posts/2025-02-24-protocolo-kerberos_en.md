---
categories:
- Theory
- Active Directory
- Kerberos
date: 2025-02-23 11:00:00 +0000
description: 'Funcionamiento de Kerberos en Active Directory

  '
image:
  alt: Microsoft Active Directory
  path: /assets/img/cabeceras_genericas/microsoft-active-directory.jpg
lang: en
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
title: Kerberos Protocol in Active Directory
toc: true
---

## ¿QUÉ ES KERBEROS?

This is an authentication protocol originally developed at the MIT in 1983 for the ATHENA project whose objectives included the integration of:

- SSO (Single sign-on)
- Support for network file systems
- Unified graphic environment (X Windows)
- Convention Name Service (such as DNS)

## KERBEROS Y MICROSOFT WINDOWS

In this system, domain-based authentication of users and hosts is done through Kerberos.

Kerberos v5 (RFC1510) was implemented in windows server 2000 and replaced NTLM (Windows NT LAN Manager) as a default authentication option.

NTLM is currently still used as a local machine authentication mechanism (not attached to a domino).

This Kerberos protocol is the oldest and most commonly used protocol today.

On the MIT website we can find a dialogue between two people Athena and Euripides written by the people who designed this protocol in which they discuss how to solve a problem being the final solution the Kerberos protocol.

[Dialogue] (http: / / web.mit.edu / kerberos / www / dialogue.html)

## ¿CÓMO FUNCIONA KERBEROS?

The user sends a flat package with his * * USER * * to the authentication service normally accompanied by another package with a * timestap * * encrypted with the user key,

The authentication service checks if the user exists, if so takes his * * password * * from the database, generates a new session key and also takes the * * granting ticket service * * key.

`TICKET GRANTING TIKET -  {sessionkey:username:address:servicename:lifespan:timestamp}`

It figures this text chain with the * * granting ticket service * * key, a private key of the service itself that the user does not know. In addition, simultaneously create another additional package with * * SessionKey1 * *, numbers it with the user's private key and all this sends it to * * user * *.

The user receives the information, decrypt the package with his private key. Now you have the session key, the * * ticket granting ticket * * encrypted by the private * * ticket granting ticket service * * and your personal private key.

The user uses the * * ticket granting ticket * * to interact with the * * ticket granting ticket service * * but so that it cannot be intercepted without more first creating an * Authenticator *

`AUTHENTICATOR - {username:address} encrypted with session key}`

And this figures with the * * SessionKey1 * *.

This prevents that, if someone intercepts the * * ticket granting ticket * * cannot interact with the * * ticket granting ticket service * * because they could not compose the * Authenticator *, as this requires the * SessionKey * that was previously included in an encrypted package with the user's personal key.

Now the user sends the * * granting ticket service * * the * Authenticator * encrypted and the * granting ticket *.

The * * granting ticket service * * uses its * * private service key * * to decipher the * * granting ticket * *, get the * SessionKey * and so decipher the * Authenticator *, check that the user that appears in the * * granting ticket * * is the same as the * Authenticator * match and if so, the validation.

Now the * * granting ticket service * * creates a * * service ticket for the file system * *. To do this create a new * SessionKey2 * that includes in the * * service ticket files * * and this figure with the * * private key of the file service. * *.

This new * SessionKey2 * puts it in another package and numbers it with the * SessionKey1 * that it obtained from the ticket granting ticket and that the user already has.

So send the * * service ticket for the * * file system and the * SessionKey2 * package encrypted to the user.

The user decouples the * SessionKey2 * with the * SessionKey1 *, creates a new * Authenticator 2 * and the same as before with the * SessionKey2 * you just got.

Send the * Authenticator 2 * and the * * service ticket for the file system * * to the * * file service * *.

The * * file service * * disfigures the * * service ticket for the * * file system in which the * SessionKey2 * is contained with which in turn the * Authenticator 2 * discloses, compares the information of the * * ticket * * with that of the * Authenticator 2 * and if they agree can validate the user.

Now if you send the corresponding data to the user.

To all this is added an additional step in communication with the file system as the service can authenticate the user but the user cannot authenticate the service so it can be supplanted by a false service.

In the * * authentication * * mutual:

- The user before sending the command to get the service file, only sends the * Authenticator 2 * and the * * service ticket for the * * file system.

- The service performs the entire previous process, authenticates the user and proceeds to authenticate itself. Create a package with a * * timestamp * *, figure it with the * SessionKey2 * (as if it were a false service it could not have obtained that key) and send it to the user.

- The user decouples the package with the * * timestamp * * and if it does so correctly this verifies that the * * service is the authentic * * and not a suppler, now if you send the command to make use of the service.

- All this is necessary to know why you can attack certain steps and take advantage to get certain data, exploit the use of tickets, use them on behalf of other users, etc.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image.png)

## ¿CÓMO SE IMPLEMENTA ESTE PROTOCOLO EN ACTIVE DIRECTORY?

Certain names that are associated with AD are used during the Kerberos authentication process.

When we start our WS01, WS02,... any inside the domain, in the initial login prompt is where this whole process begins and where the user gets his * * TicketGrantingTicket (TGT) * *.

We open Wireshark and put him to the private network of the domino.

We log into the WS01

In wireshark we filter through Kerberos and see:

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-1.png)

This first package sends the user to request the Authentication service request.

If we deploy the package data we see that it sends the user name and the services you are requesting

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-2.png)

All ActiveDirectory services are identified by the Service Principal Name (SPN).

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-3.png)

If we look at the following package is an error from the authentication service that indicates the need for a pre- authentication and this is because in the new implementation of Kerberos v5 the user check was added by requiring an encrypted TimeStamp with the user's password.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-4.png)

The user sends another request but this time with an encrypted timestamp.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-5.png)

The service responds with an Authentication service replay (AS-REP) package

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-6.png)

In its content we see that it attached the ticket we previously saw and another encrypted data that is the encrypted sessionkey with the user's password.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-7.png)

This information is broken down on the user and the user sends a TGS-REQ package (ticket granting service request)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-8.png)

As we saw before, this contains the TGT you received before and an authenticator

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-9.png)

From the service we receive a TGS-REP (ticket granting service replay)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-10.png)

This package contains the service ticket with the same name and the equipment from which you request and encrypted data that are the SessionKey and then interact with the host service.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-11.png)

If you look at us the user makes another request for a new ticket for the LDAP service in the domain controller host.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-12.png)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-13.png)

The service responds with the new ticket

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-14.png)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-15.png)

From here we see the traffic with the services that are already being requested from the host

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-16.png)

In the first package we see

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-17.png)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-18.png)

He sends you the service ticket for LDAP and the authenticator.

The service sends a mutual authentication package.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-19.png)

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-20.png)

That if we remember are data like a timestamp encrypted with the sessionkey that the user already possesses.

## Lo importante a tener en cuenta

All this is done by a user on the domain controller. This is created by default and is called krbtgt.

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-21.png)

The KDC or KeyDistributionCenter includes the services of authentication and the ticket gratnting service.

This user is responsible for encryption these packages and tickets because the key of this user is the key of the TGS.

This user's default key is very long and complex so it should obviously never be changed to something very simple to crack.

If we want to see the ServicePrincipalNames SPN, you can see what services each computer of the infrastructure offers and which SPN has partners.

```powershell
Get-NetComputer -Identity WS01
```

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-22.png)

```powershell
Get-NetComputer -Identity DC01
```

! [alt text] (/ assets / img / posts / theoria-protocolo-kerberos / image-23.png)