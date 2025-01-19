---
title: Anonimato
date: 2023-06-25
categories: [Conceptos básicos, Privacidad]
tags: [anonymity, vpn, proxy, tor, privacy]
---

## Conceptos básicos

### Relativos a redes de ordenadores y riesgos de seguridad a los que estamos expuestos por el simple hecho de estar conectados a Internet

La dirección IP y dirección MAC de los dispositivos que tenemos conectados a nuestra red doméstica/privada (incluidas las máquinas virtuales) no están directamente expuestas a Internet. 

Para conectarnos a Internet necesitamos un dispositivo denominado router, que, de manera genérica, conecta nuestra red doméstica/privada con otras redes de las que se compone Internet. Todos los dispositivos que tenemos conectados a nuestra red doméstica/privada tienen una dirección IP privada que solo es accesible por otros dispositivos conectados a esta misma red.

Por lo tanto, para poder conectarse a internet, tienen que hacerlo a través del router, que tiene una dirección ip pública concreta que utilizarán todos los sistemas informáticos que tengamos conectados a nuestra red privada.

## ¿Dónde entra el concepto de anonimato?

Utilizando algún método para garantizar el anonimato como puede ser una VPN, un proxy, red tor... de manera genérica lo que estamos haciendo es tunelizar nuestro tráfico de red aplicando algún tipo de cifrado desde una máquina en nuestra red doméstica/local hasta un servidor en Internet que se encargará de descifrar el tráfico y realizar la petición a donde nosotros queramos dirigirla.

Es importante entender, que aunque el contenido del tráfico de red vaya cifrado, ese tráfico de red sigue pasando por nuestro router para poder llegar al servidor que lo descifra y, por lo tanto, nuestro router sigue estando expuesto a Internet.

## ¿Qué es lo que tratamos de conseguir con las técnicas que intentar garantizar el anonimato en Internet?

Con este tipo de técnicas y herramientas tratamos de garantizar la privacidad y confidencialidad de nuestras conexiones. De esta manera, cuando nos conectamos a una máquina en Internet, por ejemplo un servidor de aplicación que proporciona una página web, lo hacemos a través de una o varias máquinas intermedias con las que establecemos una comunicación cifrada.

Las máquinas que se utilizan para salir a internet cuando utilizas mecanismos de anonimato como una VPN, tienen que descifrar tu tráfico de red y, por lo tanto, pueden monitorizar y registrarlo. Conocen lo que estás haciendo y también el origen de la conexión. Si utilizas un servicio gratuito de proxy, VPN... que te encuentres por Internet, es posible que incluso te estén monitorizando y puedan llegar a robarte información. 

La opción más sencilla es utilizar un proxy. Si utilizas un proxy gratuito y público ten en cuenta que en esa máquina de destino por la que estas saliendo a Internet pueden estar monitorizando tu navegación.

Otro de los mecanismos más comunes es utilizar una VPN. Existen muchos servicios de VPN gratuitos, por mi experiencia personal, os recomiendo ProtonVPN. Este servicio tiene una versión gratuita que podéis utilizar de manera segura.

Aunque es menos popular, podéis conectaros a Internet a través de la Red Tor, esto garantiza que los nodos de salida a Internet pertenezcan a esta red y, por lo tanto, su dirección ip pública sea diferente a la tuya. En este caso también debes tener en cuenta que mucha gente utiliza este mecanismos y sus direcciones ip públicas están bloqueadas frecuentemente por los buscadores más populares como Google.

Podéis establecer vuestra propia máquina de salto en la nube. Puedes crear una cuenta gratuita de AWS (Amazon Web Services) y crear una máquina (instancia) en la nube que puedes utilizar de máquina de salto para conectarte a Internet y hacer las peticiones a través de ella, sería muy similar a tener tu proxy personal.