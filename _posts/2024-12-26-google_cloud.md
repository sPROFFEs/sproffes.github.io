---
title: Google Cloud Labs - Respuesta a una intrusión
date: 2024-12-26
categories: [Cloud, Google cloud]
tags: [google-cloud, security, incident-response, cloud-security]
---

## Situación

Durante el último año, trabajaste como analista júnior de seguridad en la nube en Cymbal Retail. 

Cymbal Retail es un gigante de venta minorista que en la actualidad opera en 170 tiendas físicas y una plataforma en línea en 28 países. En la empresa, se registraron $15,000 millones en ingresos en 2022. Hoy en día, tienen 80,400 empleados en todo el mundo.

La empresa experimentó una brecha en la seguridad de los datos. Como miembro júnior del equipo de seguridad, ayudarás al equipo a través del ciclo de vida de este incidente de seguridad. Para esto, identicarás las vulnerabilidades relacionadas con la violación, la aislarás y la contendrás con el objetivo de evitar un mayor acceso no autorizado, recuperarás los sistemas comprometidos, vericarás el cumplimiento con frameworks y solucionarás cualquier problema pendiente relacionado con el cumplimiento.

## Analiza la filtración de datos y recopila información

Una mañana, el equipo de seguridad detecta actividad inusual dentro de sus sistemas. Una investigación más detallada de esta actividad revela rápidamente que la empresa ha sufrido una brecha masiva de seguridad en sus aplicaciones, redes, sistemas y repositorios de datos. Los atacantes obtuvieron acceso no autorizado a información sensible de los clientes, incluidos datos de tarjetas de crédito y detalles personales. Este incidente requiere atención inmediata y una investigación exhaustiva. El primer paso para comprender el alcance y el impacto de esta violación es recopilar información y analizar los datos disponibles.

Primero, navegamos al Security Command Center para ver una visión general de las vulnerabilidades activas.

![En la consola de Google Cloud, en el menú de navegación (navigation_menu), haz clic en Seguridad > Visión general. Se abrirá la página de Visión general del Security Command Center.](/assets/img/posts/google_cloud/20241219_120604_2024-12-19_13-05.png)
_En la consola de Google Cloud, en el menú de navegación (navigation_menu), haz clic en Seguridad > Visión general. Se abrirá la página de Visión general del Security Command Center._

Selecciona la pestaña "Hallazgos por tipo de recurso". Los hallazgos de seguridad o vulnerabilidades, organizados según el tipo de recurso en la nube afectado (por ejemplo, instancias, buckets, bases de datos), se muestran aquí. Al revisar las vulnerabilidades y hallazgos activos por tipo de recurso, podrás priorizar y abordar los problemas de seguridad de manera eficaz.

![Notarás que hay hallazgos de alta y media gravedad relacionados con el bucket de Cloud Storage, la máquina virtual de la instancia de Compute y el firewall.](/assets/img/posts/google_cloud/20241219_121014_2024-12-19_13-10.png)
_Notarás que hay hallazgos de alta y media gravedad relacionados con el bucket de Cloud Storage, la máquina virtual de la instancia de Compute y el firewall._

A continuación, navega al informe PCI DSS.

1. En el menú del Security Command Center, haz clic en Cumplimiento. Se abrirá la página de Cumplimiento.
2. En la sección de estándares de cumplimiento de Google Cloud, haz clic en Ver detalles en el cuadro PCI DSS 3.2.1. Se abrirá el informe PCI DSS 3.2.1.
3. Haz clic en la columna de Hallazgos para ordenar los hallazgos y mostrar los hallazgos activos en la parte superior de la lista.

![](/assets/img/posts/google_cloud/20241219_121401_2024-12-19_13-13.png)

![](/assets/img/posts/google_cloud/20241219_121455_2024-12-19_13-14.png)

El Estándar de Seguridad de Datos de la Industria de Tarjetas de Pago (PCI DSS, por sus siglas en inglés) es un conjunto de requisitos de seguridad que las organizaciones deben seguir para proteger los datos sensibles de los titulares de tarjetas. Como una empresa minorista que acepta y procesa pagos con tarjeta de crédito, Cymbal Retail también debe garantizar el cumplimiento de los requisitos de PCI DSS para proteger los datos de los titulares de tarjetas.

Al examinar el informe PCI DSS 3.2.1, observa que enumera las reglas que no cumplen con los requisitos y que están relacionadas con la violación de datos:

1. La grabación de reglas de firewall debe estar habilitada para poder auditar el acceso a la red: Este hallazgo de gravedad media indica que la grabación de reglas de firewall está deshabilitada, lo que significa que no hay registro de qué reglas de firewall se están aplicando ni qué tráfico se está permitiendo o denegando. Esto representa un riesgo de seguridad, ya que dificulta el seguimiento e investigación de actividades sospechosas.

2. Las reglas de firewall no deben permitir conexiones desde todas las direcciones IP en los puertos TCP o UDP 3389: Este hallazgo de gravedad alta indica que el firewall está configurado para permitir el tráfico del Protocolo de Escritorio Remoto (RDP) para todas las instancias de la red desde todo Internet. Esto representa un riesgo de seguridad, ya que permite que cualquier persona en Internet se conecte al puerto RDP en cualquier instancia de la red.

3. Las reglas de firewall no deben permitir conexiones desde todas las direcciones IP en los puertos TCP o SCTP 22: Este hallazgo de gravedad alta indica que el firewall está configurado para permitir el tráfico del Protocolo de Shell Seguro (SSH) hacia todas las instancias de la red desde todo Internet. SSH es un protocolo que permite el acceso remoto seguro a una computadora. Si un atacante logra acceder a una máquina a través de SSH, podría robar datos, instalar malware o interrumpir las operaciones.

4. Las VMs no deben tener direcciones IP públicas asignadas: Este hallazgo de gravedad alta indica que una dirección IP particular está expuesta activamente a Internet y potencialmente accesible para personas no autorizadas. Este hallazgo se considera un riesgo de seguridad potencial, ya que podría permitir que los atacantes escaneen vulnerabilidades o lancen ataques en el recurso asociado.

5. Los buckets de Cloud Storage no deben ser accesibles de forma anónima o pública: Este hallazgo de gravedad alta indica que hay una entrada en la lista de control de acceso (ACL) para el bucket de almacenamiento que es públicamente accesible, lo que significa que cualquier persona en Internet puede leer los archivos almacenados en el bucket. Esta es una vulnerabilidad de seguridad de alto riesgo que debe ser priorizada para su remediación.

6. Las instancias no deben estar configuradas para usar la cuenta de servicio predeterminada con acceso total a todas las API de Cloud: Este hallazgo de gravedad media indica que a una identidad o cuenta de servicio se le ha otorgado acceso total a todas las API de Google Cloud. Este hallazgo se considera un riesgo de seguridad significativo, ya que otorga a la identidad o cuenta de servicio la capacidad de realizar cualquier acción dentro del entorno de Google Cloud, incluidas la accesibilidad a datos sensibles, la modificación de configuraciones y la eliminación de recursos.

![](/assets/img/posts/google_cloud/20241219_121813_2024-12-19_13-17.png)

![](/assets/img/posts/google_cloud/20241219_121818_2024-12-19_13-18.png)

La siguiente tabla empareja las reglas listadas en el informe con su categoría correspondiente de hallazgos.

![](/assets/img/posts/google_cloud/20241219_122124_2024-12-19_13-21.png)

A continuación, navega al Security Command Center y filtra los hallazgos para un examen y análisis más detallado de las vulnerabilidades en el entorno de Google Cloud.

1. En la consola de Google Cloud, en el menú de navegación (navigation_menu), haz clic en Seguridad > Hallazgos. Se abrirá la página de Hallazgos.
2. En el panel de Filtros rápidos, en la sección de Tipo de recurso, selecciona la casilla de verificación para el tipo de recurso **Google Cloud Storage bucket**.

![](/assets/img/posts/google_cloud/20241219_122321_2024-12-19_13-22.png)

Los siguientes hallazgos activos relacionados con el bucket de almacenamiento deben ser listados:

1. ACL pública del bucket: Este hallazgo está listado en el informe PCI DSS e indica que cualquier persona con acceso a Internet puede leer los datos almacenados en el bucket.

2. Política de bucket deshabilitada: Esto indica que no hay una política explícita en el bucket para controlar quién puede acceder a los datos en él.

3. Registro del bucket deshabilitado: Esto indica que no se ha habilitado el registro para el bucket, por lo que será difícil rastrear quién está accediendo a los datos.

Estos hallazgos indican que el bucket está configurado con una combinación de configuraciones de seguridad que podrían exponer los datos a accesos no autorizados. Deberás remediar estos hallazgos eliminando la lista de control de acceso pública, deshabilitando el acceso público al bucket y habilitando la política de acceso uniforme a nivel de bucket.

En el panel de Filtros rápidos, en la sección de Tipo de recurso, desmarca Google Cloud storage bucket y selecciona la casilla de verificación para el tipo de recurso Google Compute Instance.

![](/assets/img/posts/google_cloud/20241219_122629_2024-12-19_13-26.png)

Los siguientes hallazgos activos relacionados con la máquina virtual cc-app-01 deben ser listados:

1. Malware bad domain: Este hallazgo indica que un dominio conocido por estar asociado con malware fue accesado desde la instancia google.compute.instanc* llamada cc-app-01. Aunque este hallazgo se considera de baja gravedad, indica que ha ocurrido una actividad maliciosa en la instancia de la máquina virtual y que ha sido comprometida.

2. Secure boot deshabilitado: Este hallazgo de gravedad media indica que el arranque seguro está deshabilitado para la máquina virtual. Esto representa un riesgo de seguridad, ya que permite que la máquina virtual inicie con código no autorizado, lo que podría ser utilizado para comprometer el sistema.

3. Cuenta de servicio predeterminada usada: Este hallazgo de gravedad media indica que la máquina virtual está utilizando la cuenta de servicio predeterminada. Esto representa un riesgo de seguridad, ya que la cuenta de servicio predeterminada tiene un alto nivel de acceso y podría ser comprometida si un atacante obtiene acceso al proyecto.

4. Dirección IP pública: Este hallazgo de gravedad alta está listado en el informe PCI DSS e indica que la máquina virtual tiene una dirección IP pública. Esto representa un riesgo de seguridad, ya que permite que cualquier persona en Internet se conecte directamente a la máquina virtual.

5. Acceso completo a las API: Este hallazgo de gravedad media está listado en el informe PCI DSS e indica que a la máquina virtual se le ha otorgado acceso completo a todas las API de Google Cloud.

## Arreglar las vulnerabilidades de Compute Engine

Apagarás la máquina virtual vulnerable cc-app-01 y crearás una nueva máquina virtual a partir de una instantánea tomada antes de la infección por malware. Las instantáneas de la máquina virtual son efectivas para restaurar el sistema a un estado limpio y aseguran que la nueva máquina virtual no estará infectada con el mismo malware que comprometió la máquina virtual original.

1. En la consola de Google Cloud, haz clic en el menú de navegación (navigation_menu).

2. Selecciona Compute Engine > VM instances. Se abrirá la página de Instancias de VM.

La máquina virtual cc-app-01 actual debe estar listada bajo Instancias de VM. Esta es la máquina virtual vulnerable que ha sido comprometida y debe apagarse.

3. Marca la casilla para la máquina virtual **cc-app-01**.
4. Haz clic en **Detener**.
5. Aparecerá una ventana emergente pidiéndote confirmar que la máquina virtual debe ser detenida, haz clic en **Detener**.

![](/assets/img/posts/google_cloud/20241219_123658_2024-12-19_13-36.png)

![](/assets/img/posts/google_cloud/20241219_123753_2024-12-19_13-37.png)

A continuación, crea una nueva máquina virtual a partir de una instantánea. Esta instantánea ya ha sido creada como parte del plan de respaldo de datos a largo plazo de Cymbal Retail.

1. En la barra de acciones, haz clic en + Crear instancia.

2. En el campo Nombre, escribe cc-app-02.

3. En la sección Tipo de máquina, expande el menú desplegable, selecciona Shared-core, y luego selecciona e2-medium.

4. En la sección Disco de arranque, haz clic en Cambiar. Se abrirá el cuadro de diálogo del disco de arranque.

5. Selecciona la pestaña Instantáneas.

6. Expande el menú desplegable de Instantánea, y selecciona cc-app01-snapshot.

7. Haz clic en Seleccionar.

8. En la sección Identidad y acceso a la API, expande el menú desplegable de Cuentas de servicio, y selecciona Qwiklabs User Service Account.

9. Expande la sección de Opciones avanzadas.

10. Expande la sección de Redes.

11. En el campo Etiquetas de red, escribe cc. Usarás esta etiqueta para aplicar reglas de firewall a esta máquina virtual específica.

12. En la sección de Interfaces de red, expande la red predeterminada.

13. Expande el menú desplegable de Dirección IPv4 externa, y selecciona Ninguna.

14. Haz clic en Crear.

![](/assets/img/posts/google_cloud/20241219_124829_Peek_2024-12-19_13-48.gif)

La nueva máquina virtual cc-app-02 ahora debería haber sido creada a partir de la instantánea cc-app01-snapshot. (Puede tardar unos minutos en crearse la nueva VM).

Ahora, activa el Arranque Seguro para la nueva máquina virtual cc-app-02 para abordar el hallazgo de Arranque Seguro deshabilitado.

1. Marca la casilla para la máquina virtual cc-app-02.

2. Haz clic en Detener.

3. Aparecerá una ventana emergente pidiéndote confirmar que la máquina virtual debe ser detenida, haz clic en Detener.
Espera a que la máquina virtual cc-app-02 se detenga antes de continuar.

4. En la sección de Instancias de VM, haz clic en el enlace cc-app-02. Se abrirá la página de cc-app-02.

5. En la barra de herramientas de cc-app-02, haz clic en Editar. Se abrirá la página Editar instancia cc-app-02.

6. Desplázate hacia abajo hasta la sección de Seguridad y acceso, y bajo VM blindada, marca la casilla para la opción Activar Arranque Seguro. Esto resolverá el hallazgo de Arranque Seguro deshabilitado.

7. Haz clic en Guardar.

8. En el menú de Compute Engine, selecciona Instancias de VM.

9. Marca la casilla para la máquina virtual cc-app-02.

10. Haz clic en Iniciar/Reanudar.

11. Aparecerá una ventana emergente pidiéndote confirmar que la máquina virtual debe ser iniciada, haz clic en Iniciar.

La instancia de la máquina virtual cc-app-02 se reiniciará y el hallazgo de Arranque Seguro deshabilitado será corregido.

![](/assets/img/posts/google_cloud/20241219_125106_2024-12-19_13-50.png)

![](/assets/img/posts/google_cloud/20241219_125614_Peek_2024-12-19_13-55.gif)

![](/assets/img/posts/google_cloud/20241219_125724_2024-12-19_13-57.png)

## Arreglar los permisos del bucket de Cloud Storage

Revocarás el acceso público al bucket de almacenamiento y cambiarás a control de acceso uniforme a nivel de bucket, lo que reducirá significativamente el riesgo de brechas de datos. Al eliminar todos los permisos de usuario del bucket de almacenamiento, puedes evitar el acceso no autorizado a los datos almacenados.

1. En el menú de navegación, selecciona Cloud Storage > Buckets. Se abrirá la página de Buckets.

2. Haz clic en el enlace del bucket _bucket storage. Se abrirá la página de detalles del bucket.

Notarás que hay un archivo myfile.csv en el bucket accesible públicamente. Este es el archivo que contiene la información sensible que fue volcada por el actor malicioso. Realiza los siguientes pasos para abordar el hallazgo de Public bucket ACL.

1. Haz clic en la pestaña Permissions.

2. En el cuadro de Public access, haz clic en Prevent public access.

3. Haz clic en Confirm.

![](/assets/img/posts/google_cloud/20241219_132659_2024-12-19_13-59.png)

![](/assets/img/posts/google_cloud/20241219_132723_Peek_2024-12-19_13-56.gif)

![](/assets/img/posts/google_cloud/20241219_132751_Peek_2024-12-19_14-02.gif)

![](/assets/img/posts/google_cloud/20241219_132813_Peek_2024-12-19_14-04.gif)

## Limitar el acceso a los puertos del firewall

Restringirás el acceso a los puertos RDP y SSH solo a redes de origen autorizadas para minimizar la superficie de ataque y reducir el riesgo de acceso remoto no autorizado.

Ejercita una extrema precaución antes de modificar reglas de firewall demasiado permisivas. Las reglas pueden estar permitiendo tráfico legítimo, y restringirlo incorrectamente podría interrumpir operaciones críticas. En este laboratorio, asegúrate de que las instancias de máquina virtual de Compute Engine etiquetadas con la etiqueta de destino "cc" sigan siendo accesibles a través de conexiones SSH desde el rango de direcciones de Google Cloud Identity-Aware Proxy (35.235.240.0/20). Para mantener el acceso continuo de administración, crea una nueva regla de firewall de acceso limitado para el tráfico SSH antes de eliminar la regla existente que permite conexiones SSH desde cualquier dirección.

![](/assets/img/posts/google_cloud/20241219_132952_Peek_2024-12-19_14-06.gif)

![](/assets/img/posts/google_cloud/20241219_133055_Peek_2024-12-19_14-10.gif)

## Arreglar la configuración del firewall

Eliminarás tres reglas específicas de firewall de VPC que son responsables de permitir el acceso sin restricciones a ciertos protocolos de red, como ICMP, RDP y SSH, desde cualquier fuente dentro de la red VPC. Luego, habilitarás el registro en las reglas de firewall restantes.

Eliminarás las reglas de firewall default-allow-icmp, default-allow-rdp y default-allow-ssh. Estas reglas son demasiado amplias y, al eliminarlas, permitirás un entorno de red más seguro y controlado.

Al eliminar estas reglas, habrás restringido el acceso a estos protocolos, limitando el potencial de intentos de acceso no autorizado y reduciendo la superficie de ataque de tu red.

![](/assets/img/posts/google_cloud/20241219_133307_Peek_2024-12-19_14-11.gif)

### Enable logging

Habilita el registro para las reglas de firewall limit-ports (la regla que creaste en una tarea anterior) y default-allow-internal.

Habilitar el registro te permite rastrear y analizar el tráfico que es permitido por esta regla, lo cual probablemente sea tráfico interno entre instancias dentro de tu VPC.

![](/assets/img/posts/google_cloud/20241219_133349_Peek_2024-12-19_14-12.gif)

## Verificar cumplimiento

Después de abordar diligentemente las vulnerabilidades identificadas en el informe PCI DSS 3.2.1, es crucial verificar la efectividad de tus esfuerzos de remediación. En esta tarea, volverás a ejecutar el informe para asegurarte de que las vulnerabilidades previamente identificadas hayan sido mitigadas con éxito y ya no representen un riesgo de seguridad para el entorno.

1. En el menú de Security Command Center, haz clic en Compliance. Se abrirá la página de cumplimiento.

2. En la sección de Google Cloud compliance standards, haz clic en View details en el recuadro de PCI DSS 3.2.1. Se abrirá el informe PCI DSS 3.2.1.

3. Haz clic en la columna de Findings para ordenar los hallazgos y mostrar los hallazgos activos en la parte superior de la lista.

Todas las vulnerabilidades principales ahora están resueltas.

![Aunque abordaste las vulnerabilidades de alta y media severidad, los registros de flujo siguen deshabilitados para varias subredes. Este hallazgo seguirá visible en el informe después de que hayas completado las tareas de remediación, ya que está relacionado con este entorno de laboratorio.](/assets/img/posts/google_cloud/20241219_133930_Screenshot_2024-12-19_at_14-35-52_Solution_guide_Respond_and_recover_from_a_data_breach_Google_Cloud_Skills_Boost.png)
_Aunque abordaste las vulnerabilidades de alta y media severidad, los registros de flujo siguen deshabilitados para varias subredes. Este hallazgo seguirá visible en el informe después de que hayas completado las tareas de remediación, ya que está relacionado con este entorno de laboratorio._