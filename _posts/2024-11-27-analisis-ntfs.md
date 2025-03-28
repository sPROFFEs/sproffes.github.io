---
title: Análisis de NTFS
date: 2024-11-27 11:58:38 +0000
categories: [Forense, Discos]
tags: [forense, ntfs, windows, file-system]
pin: false
math: true
mermaid: true
---

## Tabla de Contenidos
1. [Active Disk Editor](#1-active-disk-editor)
2. [Identificación a bajo nivel](#2-identificación-a-bajo-nivel)
3. [MFT2CSV](#3-mft2csv)
4. [NTFSLogFile](#4-ntfslogfile)
5. [UsnJrnl2Csv](#5-usnjrnl2csv)
6. [ANJP](#6-anjp)
7. [Análisis del origen de archivos](#7-análisis-del-origen-de-archivos)
8. [Indx2Csv](#8-indx2csv)
9. [Recuva VS FTK Imager](#9-recuva-vs-ftk-imager)

## 1. Active Disk Editor

Vamos a identificar con la herramienta ADE, mediante la inspección de los registros MFT (1KB), cuales de ellos han sido borrados en base a la propiedad FLAGS (campo "in use" = '0')

![Partición NTFS con tablas MBR](/assets/img/posts/analisis_ntfs/20241127_002906_20241126_183041_Screenshot_From_2024-11-26_18-30-33.png)
_Vemos que se trata de una partición NTFS con tablas de particiones MBR._

### Identificar inicio del boot record NTFS

La ubicación de la Master File Table (MFT) en un sistema NTFS se encuentra en el Boot Sector de la partición NTFS. Este es el primer sector de la partición (sector 0 del volumen NTFS).

![Editar partición NTFS](/assets/img/posts/analisis_ntfs/20241127_002929_20241126_184100_Screenshot_From_2024-11-26_18-40-48.png)
_Hacemos click derecho para editar la partición NTFS_

En el sector de arranque, la información relevante está estructurada como sigue:
- Byte 48 a 55 (0x30 a 0x37): Cluster de inicio de la MFT
- Byte 56 a 63 (0x38 a 0x3F): Cluster de inicio de la MFT espejo (MFTMirr)

![Boot sector structure](/assets/img/posts/analisis_ntfs/20241127_003012_20241126_184141_Screenshot_From_2024-11-26_18-41-36.png)

### Leer el valor del clúster inicial de la MFT

En el Boot Sector (primer sector de la partición NTFS), ubica los siguientes bytes:

![MFT inicio cluster](/assets/img/posts/analisis_ntfs/20241127_003033_20241126_185550_Screenshot_From_2024-11-26_18-55-44.png)
_Byte offset 48 a 55 (0x30 a 0x37): Clúster de inicio de la MFT_

Hacemos CTRL + click para ir al cluster de inicio del archivo. Otro método es hacer clic en navigate MFT

![Registro MFT](/assets/img/posts/analisis_ntfs/20241127_003116_20241126_192810_Screenshot_From_2024-11-26_19-27-56.png)
_Esto mostrará el registro MFT_

![MFT en uso](/assets/img/posts/analisis_ntfs/20241127_003143_20241126_192958_Screenshot_From_2024-11-26_19-29-51.png)
_En este archivo MFT vemos que está en uso_

### Busqueda de archivos eliminados

Teniendo en cuenta que los archivos que hayan sido eliminados del registro cuentan con esa flag a 0 podemos intentar buscar manualmente cuales han sido eliminados.

![Browse file records](/assets/img/posts/analisis_ntfs/20241127_003214_20241126_193205_Screenshot_From_2024-11-26_19-32-00.png)
_Hacemos click en browse file records para una visualización mas clara e investigamos por la carpeta de recycle bin_

Observamos que existe una carpeta con documentos en su interior que existen dentro de la carpeta de reciclaje pero que existen aun en el registro.

![Recycle bin contents](/assets/img/posts/analisis_ntfs/20241127_003239_20241126_193344_Screenshot_From_2024-11-26_19-33-37.png)

Lo interesante es cerca de esta dirección buscar de forma manual ficheros en los que las flags de uso queden a 0. Tras un rato de investigación encontramos un par de archivos.

![Archivo texto-copia.txt](/assets/img/posts/analisis_ntfs/20241127_003255_20241126_193819_Screenshot_From_2024-11-26_19-38-15.png)
_Si nos fijamos bien a la derecha en el bloque verde observamos el nombre del fichero -> "texto -copia.txt"_

Poco más abajo de los datos correspondientes a la carpeta encontramos el primer fichero que aun está en el disco pero que ha sido borrado del registro MFT como vemos en las flags de uso

![Archivo calendarioSept2018.pdf](/assets/img/posts/analisis_ntfs/20241127_003306_20241126_194333_Screenshot_From_2024-11-26_19-43-27.png)
_Si nos fijamos bien a la derecha en el bloque verde observamos el nombre del fichero -> "clendarioSept2018.pdf"_

### Recuperar el archivo mediante FTK

Ahora que tenemos una idea a nivel más bajo de como están elimnados los ficheros del MFT vamos a utilizar el programa FTK Imager para recuperarlo. Montada la imagen de disco en el programa podremos ver más claramente que archivos no están listados en el registro y por lo tanto han sido "eliminados" del sistema.

![Documento desligado](/assets/img/posts/analisis_ntfs/20241127_003337_20241126_194857_Screenshot_From_2024-11-26_19-48-54.png)
_Observamos como el documento anteriormente mencionado se encuentra deligado del registro_

El otro documento txt lo encontramos en "carpeta" con una cruz indicando que fue eliminado

![Documento txt](/assets/img/posts/analisis_ntfs/20241127_003403_20241126_195114_Screenshot_From_2024-11-26_19-51-08.png)   

Para poder recuperar el documento podemos hacer click derecho y exportar

![Exportar documento](/assets/img/posts/analisis_ntfs/20241127_003412_20241126_195227_Screenshot_From_2024-11-26_19-51-52.png)
_Esto crea una copia exacta de los datos que aun queden intactos en el disco_

## 2. Identificación a bajo nivel

### Atributos $10, $30 y $80

En NTFS, los registros de la MFT contienen diferentes atributos, cada uno con información específica sobre los archivos o directorios. Los atributos que te interesan son:

```
$10: Atributo de nombre de archivo ($FILE_NAME)
$30: Atributo de contenido del archivo ($DATA)
$80: Atributo de información de seguridad ($SECURITY_DESCRIPTOR)
```

### Fecha de creación, modificación y acceso

Para esto buscamos el atributo $FILE-NAME correspondiente a $30

![Fechas y nombre](/assets/img/posts/analisis_ntfs/20241127_003500_20241126_200425_Screenshot_From_2024-11-26_20-04-11.png)
_Observamos como salen todas las fechas correspondientes así como el nombre del archivo_

### Propiedad "non-resident" y sus valores asociados (0/1)

Atributo residente:
- La información del atributo está contenida directamente dentro del registro MFT.
- Por ejemplo, el nombre de un archivo pequeño puede estar almacenado directamente en el registro, sin necesidad de buscar bloques de datos adicionales.

Atributo no-residente:
- La información del atributo no está contenida directamente en el registro MFT. En cambio, los datos del atributo están almacenados en otros bloques de disco (fuera de la MFT).
- Esto es común cuando el tamaño del archivo es grande o cuando el atributo tiene mucha información, como el contenido de archivos grandes.

![Atributo DATA residente](/assets/img/posts/analisis_ntfs/20241127_003544_20241126_200725_Screenshot_From_2024-11-26_20-07-18.png)
_En un archivo TXT vemos como el atributo $DATA($30) si es residente_

![Atributo SECURITY_DESCRIPTOR no residente](/assets/img/posts/analisis_ntfs/20241127_003557_20241126_201100_Screenshot_From_2024-11-26_20-10-52.png)
_Sin embargo el atributo $SECURITY_DESCRIPTOR($80) se encuentra fuera del bloque_

## 3. MFT2CSV

### Exportar el fichero de metadatos $MFT usando FTK

Al montar la imagen de nuevo en FTK podemos navegar a root para poder exportar el fichero de registros $MFT

![Exportar MFT](/assets/img/posts/analisis_ntfs/20241127_003629_20241126_201720_Screenshot_From_2024-11-26_20-17-15.png)

Para poder visualizar el archivo debemos indicar al explorador que muestre ficheros ocultos y archivos del sistema. En windows 11, los tres puntos y vamos a configuración

![Configuración Indx2Csv](/assets/img/posts/analisis_ntfs/20241127_003642_20241126_202359_Screenshot_From_2024-11-26_20-23-17.png)
_Recordar la opción dump everything y el separador_

Para determinar qué archivos están presentes y cuáles han sido eliminados o sobrescritos en base a los datos hay que fijarse en ciertas columnas que indican la validez y estado de los registros en la estructura del sistema NTFS.

![Registros NTFS](/assets/img/posts/analisis_ntfs/20241127_003708_20241126_202440_Screenshot_From_2024-11-26_20-24-35.png)

MFTReference y MFTReferenceSeqNo:

- Estos campos indican el número de referencia del archivo en la MFT (Master File Table) y el número de secuencia asociado. Un valor válido será generalmente positivo y consistente.

IndexFlags:
- Los índices indican propiedades del archivo en relación con el directorio y la MFT. Por ejemplo:
  - 0: Archivo regular
  - 1: Archivo eliminado o sobrescrito

IsNotLeaf y LastLsn:
- LastLsn puede usarse para correlacionar operaciones recientes con archivos
- IsNotLeaf indica si es un nodo hoja o tiene referencias a otros índices

Fechas (CTime, ATime, MTime, RTime):
- Si las fechas de modificación o creación parecen inconsistentes o fuera de rango, esto puede ser indicativo de eliminación o corrupción

![Registros eliminados](/assets/img/posts/analisis_ntfs/20241127_003739_20241126_202921_Screenshot_From_2024-11-26_20-28-53.png)
_Tenemos dos registros eliminados y uno posiblemente corrupto o completamente eliminado debido al numero inusualmente elevado del MFTReference_

### Directorio en root

Procesamos el archivo igual que antes y vemos como los documentos de texto antes se encontraban en el directorio raíz

![Documentos en root](/assets/img/posts/analisis_ntfs/20241127_003800_20241126_203037_Screenshot_From_2024-11-26_20-30-07.png)
_Observamos datos similares a los anteriores_

### Directorio de recycle bin

Mediante el mismo proceso analizamos el documento y observamos que no se ha eliminado por completo nada y que todos los archivos que hay fueron movidos al mismo tiempo a la papelera

![Archivos en papelera](/assets/img/posts/analisis_ntfs/20241127_004906_Screenshot_From_2024-11-27_00-48-47.png)

## 9. Recuva VS FTK Imager

Vamos a realizar una comparación entre un software que es utilizado para recuperar archivos eliminados del disco y FTK imager. Esto nos permitirá ver como realmente las herramientas forenses son mucho más potentes que las que comercialmente son vendidas y, además suelen ser más baratas o incluso open source.

Para poder recuperar archivos de la imagen de disco mediante Recuva debemos montarlo como hicimos en el apartado 7 mediante FTK o similares

![Disco en Recuva](/assets/img/posts/analisis_ntfs/20241127_005145_Screenshot_2024-11-27_005036.png)
_Deberíamos ver el disco montado en Recuva_

Damos doble click sobre el disco y nos lo analizará en busca de archivos

![Análisis Recuva](/assets/img/posts/analisis_ntfs/20241127_011105_Screenshot_From_2024-11-27_01-10-47.png)

### Resultados en Recuva

Supuestamente ha encontrado 80 archivos que recuperar. Si observamos bien y comparamos con lo que nos muestra FTK, algunos de esos archivos ni siquiera existen o los está confundiendo con algunos de los rastros que han ido dejando esos movimientos como los que veíamos en el punto anterior donde el fichero "texto.txt" pasó de estar en root a la "carpeta"

![Resultados Recuva](/assets/img/posts/analisis_ntfs/20241127_162721_Screenshot_From_2024-11-27_16-27-03.png)

Por supuesto que si intentamos recuperar cualquiera de estos documentos nos pedirá pagar la licencia.

### Resultados en FTK Imager

Si analizamos manualmente el disco en FTK vemos que en la raíz del disco únicamente encontramos un documento PDF que fue eliminado aquí y no los rastros que dejó el movimiento del texto.txt, por ejemplo

![Análisis FTK](/assets/img/posts/analisis_ntfs/20241127_162721_Screenshot_From_2024-11-27_16-27-03.png)

Sin embargo si nos movemos al directorio carpeta vemos que si nos indica que existe el fichero texto.txt y que se encuentran los datos eliminados de otro llamado texto-copia.txt

![Archivos en carpeta](/assets/img/posts/analisis_ntfs/20241127_163808_Screenshot_From_2024-11-27_16-38-01.png)

El resto de documentos que indicaba Recuva realmente no están eliminados ni se llaman como lo indica. Además si necesitamos recuperar el archivo en FTK simplemente hacemos click derecho y lo exportamos, sin licencias ni nada. Windows](/assets/img/20241126_202359_Screenshot_From_2024-11-26_20-23-17.png)

Aqui habilitamos la opción de mostrar archivos ocultos y desmarcamos la opción de ocultar archivos del sistema

![Opciones archivos ocultos](/assets/img/posts/analisis_ntfs/20241127_163940_Screenshot_From_2024-11-27_16-39-20.png)

Ahora podemos abrir el programa:

```
https://github.com/jschicht/Mft2Csv/releases/download/v2.0.0.51/Mft2Csv_v2.0.0.51.zip
```

Abierto el programa podemos hacer click en elegir MFT e importarlo

![Importar MFT](/assets/img/posts/analisis_ntfs/20241127_164501_Screenshot_From_2024-11-27_16-44-33.png)

Dejando el resto de parámetros por defecto excepto el separador que indicaremos como ";" damos en comenzar

![Configuración MFT2CSV](/assets/img/posts/analisis_ntfs/20241127_165239_Screenshot_From_2024-11-27_16-52-36.png)

### Analizando el CSV

En la carpeta creada contamos con varios CSV, abrimos el primero con algún procesador de hojas de cálculo

![Configuración importación CSV](/assets/img/posts/analisis_ntfs/20241127_004906_Screenshot_From_2024-11-27_00-48-47.png)
_Importante tomar esa configuración para formatear el contenido correctamente_

Nos interesa estudiar qué archivos se han borrado y en qué fecha por lo que vamos a aplicar unos filtros bien sean por "in_use = 0" o "RecordActive" = DELETED/ALLOCATED

![Crear filtros](/assets/img/posts/analisis_ntfs/20241127_005145_Screenshot_2024-11-27_005036.png)
_Creamos filtros_

Encontramos los dos archivos eliminados

![Archivos eliminados](/assets/img/posts/analisis_ntfs/20241127_011105_Screenshot_From_2024-11-27_01-10-47.png)

Si nos movemos un poco más a la derecha podremos observar las fechas y más concretamente la de borrado:

- Creation Time (SI_CTime): Fecha y hora de creación del archivo
- Last Access Time (SI_ATime): Fecha y hora del último acceso al archivo
- Last Modification Time (SI_MTime): Fecha y hora de la última modificación del archivo
- Record Time (SI_RTime): Última vez que el registro fue modificado (utilizado para el propio registro MFT)

Datos importantes:
- Columna clave: "RecordActive" = DELETED
- Fecha de eliminación: 2021-02-09 a las 19:44:23.0319225 (para texto-copia.txt)
- Fecha de eliminación: 2021-02-09 a las 19:44:23.0797836 (para calendarioSept2018.pdf)

![Fechas eliminación](/assets/img/posts/analisis_ntfs/20241127_162721_Screenshot_From_2024-11-27_16-27-03.png)

## 4. NTFSLogFile

Exportar el fichero de metadatos $LogFILE, que junto a la $MFT proporcionará datos sobre las transacciones realizadas en el sistema de archivos.

Software necesario:
```
https://github.com/jschicht/LogFileParser/releases/tag/v2.0.0.51
```

Para extraer el $LogFile realizamos el mismo proceso que con $MFT con FTK imager. Una vez lo tengamos procedemos a extraer los datos usando este software.

![Configuración LogFileParser](/assets/img/posts/analisis_ntfs/20241127_163808_Screenshot_From_2024-11-27_16-38-01.png)
_Importante importar el $MFT ya procesado en formato csv y seleccionar el separador como ";"_

Lo abrimos exactamente igual con un procesador de hojas de cálculo

![Importar LogFile CSV](/assets/img/posts/analisis_ntfs/20241127_163940_Screenshot_From_2024-11-27_16-39-20.png)
_Una vez importado recordad aplicar los filtros automáticos_

### Transacciones

Buscamos las transacciones donde el campo "lf_RedoOperation" valga "DeallocateFileRecordSegment" para localizar ficheros borrados definitivamente puesto que como su nombre indica la operación fue desasignar el segmento del registro del fichero.

Campos clave:

- lf_Offset: Posición del registro en el archivo
- lf_MFTReference: Número de referencia del archivo en Master File Table
- lf_RedoOperation y lf_UndoOperation: Operaciones de registro (ambos son "DeallocateFileRecordSegment" y "InitializeFileRecordSegment")
- lf_FileName: Nombre del archivo

![Campos LogFile](/assets/img/posts/analisis_ntfs/20241127_164501_Screenshot_From_2024-11-27_16-44-33.png)

Estos son registros de log de eliminación de archivos en un sistema de archivos NTFS. Cada línea representa un archivo que fue borrado, con:

- Operación de desasignación de segmento de registro de archivo
- Nombre del archivo eliminado
- Información de seguimiento de cambios en la Master File Table

## 5. UsnJrnl2Csv

```
https://github.com/jschicht/UsnJrnl2Csv
```

Exportar el fichero de metadatos correspondiente al $USNJournal ( $Extend -> $USNjrl -> $J). Para esto igual que antes usamos FTK imager teniendo en cuenta los siguientes pasos:

![Directorio $EXTEND](/assets/img/posts/analisis_ntfs/20241127_165239_Screenshot_From_2024-11-27_16-52-36.png)
_Dentro del directorio $EXTEND buscamos $UsnJrnl y damos doble click en él_

![Exportar $J](/assets/img/posts/analisis_ntfs/20241127_165400_Screenshot_From_2024-11-27_16-53-55.png)
_Exportamos $J_

Ahora si podemos importarlo en la herramienta para poder ser procesado

![Configuración UsnJrnl2Csv](/assets/img/posts/analisis_ntfs/20241127_165644_Screenshot_From_2024-11-27_16-56-39.png)
_Recordad establecer el separador en ";" y dump everything_

Una vez procesado lo encontramos en la misma carpeta del programa. Lo abrimos con un editor al igual que antes

![Abrir USNJrnl CSV](/assets/img/posts/analisis_ntfs/20241127_185831_Screenshot_From_2024-11-27_18-58-09.png)

Filtramos la información resultante por el campo "Reason" = "CLOSE+DELETE" para obtener las fechas de cuando se produjo el borrado definitivo de los ficheros.

![Filtrar por CLOSE+DELETE](/assets/img/posts/analisis_ntfs/20241127_172059_Screenshot_From_2024-11-27_17-20-55.png)

## 6. ANJP

Esta herramienta (descontinuada) permite realizar un procesamiento conjunto de la $MFT, $LogFile y $USNJrnl. Dispone de una pestaña donde decodificar la información (Parse) y otra donde visualizar los resultados (Report).

Añadimos los tres ficheros extraidos anteriormente y los procesamos

![Procesamiento ANJP](/assets/img/posts/analisis_ntfs/20241127_174005_Screenshot_From_2024-11-27_17-39-28.png)

![Conectar base de datos](/assets/img/posts/analisis_ntfs/20241127_174229_Screenshot_From_2024-11-27_17-42-19.png)
_Antes de visualizar los reportes debemos conectar con la base de datos_

![MFT en ANJP](/assets/img/posts/analisis_ntfs/20241127_174446_Screenshot_From_2024-11-27_17-44-00.png)
_$MFT_

![LogFile en ANJP](/assets/img/posts/analisis_ntfs/20241127_174514_Screenshot_From_2024-11-27_17-45-05.png)
_$LogFile_

![USNJrnl en ANJP](/assets/img/posts/analisis_ntfs/20241127_174545_Screenshot_From_2024-11-27_17-45-40.png)
_$USNJrnl_

## 7. Análisis del origen de archivos

### Alternate Stream View

```
https://alternatestreamview.en.lo4d.com/windows
```

Para usar este software primero debemos montar la imagen del disco mediante FTK o similares

![Montar imagen](/assets/img/posts/analisis_ntfs/20241127_175855_Screenshot_From_2024-11-27_17-57-09.png)

![Alternate Stream View scan](/assets/img/posts/analisis_ntfs/20241127_180002_Screenshot_From_2024-11-27_17-59-53.png)
_En Alternate Stream View vamos a escanear la imagen del disco ya montada_

### ¿Qué son los archivos Zone identifier?

Zone.Identifier es un atributo de archivo en sistemas de archivos Windows que se utiliza para marcar archivos descargados de Internet u otras ubicaciones externas.

![Zone Identifier](/assets/img/posts/analisis_ntfs/20241127_180236_Screenshot_From_2024-11-27_18-02-09.png)

Cuando se descarga un archivo de Internet, Windows agrega automáticamente el atributo Zone.Identifier para indicar que el archivo proviene de una "zona" menos confiable que los archivos locales. El atributo contiene información sobre la "zona de seguridad" del archivo, como si proviene de Internet, una intranet, etc. Esto ayuda a los programas a aplicar políticas de seguridad apropiadas. Los archivos con este atributo pueden tener restricciones, como la imposibilidad de ejecutarlos directamente por motivos de seguridad.

### Por ejemplo

Nombre de flujo: Zone.Identifier:$DATA
Nombre de archivo: E:26507936.pdf
Nombre de flujo completo: E:26507936.pdf:Zone.Identifier
Tamaño de flujo: 26 bytes
Tamaño de asignación de flujo: 32 bytes
Extensión: pdf
Fecha de modificación: 03/02/2021 20:30:05
Fecha de creación: 09/02/2021 20:31:55
Fecha de modificación de entrada: 03/02/2021 20:30:05
Atributos de archivo: A (Archivo)

Esto indica que el flujo "Zone.Identifier:$DATA" está asociado al archivo "E:26507936.pdf". Proporciona metadatos sobre el archivo, como su tamaño, fechas de creación y modificación, y atributos.

![Ejemplo Zone Identifier](/assets/img/posts/analisis_ntfs/20241127_180505_Screenshot_From_2024-11-27_18-04-39.png)

En los sistemas de archivos de Windows, los archivos con el atributo "Zone.Identifier" se encuentran junto a los archivos originales a los que están asociados. Cuando se descarga un archivo de Internet u otra ubicación externa, Windows agrega automáticamente este atributo al archivo descargado.

Entonces, los archivos "Zone.Identifier" se encuentran en la misma ubicación que los archivos a los que están vinculados, actuando como un indicador de su origen y seguridad pero no son visibles de forma directa.

### FTK Imager

En FTK podremos ver menos información sobre los archivos pero para poder sacarla lo hacemos de esta manera. Una vez abierto el disco de evidencias o imagen buscamos algún archivo de interés y damos click derecho exportar "File Hash List"

![Exportar Hash List](/assets/img/posts/analisis_ntfs/20241127_183950_Screenshot_From_2024-11-27_18-39-47.png)

Aquí observamos los datos correspondientes al documento pdf y a su zone identifier

![Datos PDF y Zone Identifier](/assets/img/posts/analisis_ntfs/20241127_184206_Screenshot_From_2024-11-27_18-41-58.png)

Si hacemos click en el documento a la derecha podremos ver el contenido del zone idenfifier

![Contenido Zone Identifier](/assets/img/posts/analisis_ntfs/20241127_185545_Screenshot_From_2024-11-27_18-54-38.png)

## 8. Indx2Csv

```
https://github.com/jschicht/Indx2Csv
```

Para empezar vamos a exportar los ficheros de metadatos de tipo índice de directorios ($I30) de los tres directorios que aparecen en la imagen de disco.

Para esto, tomando de referencia desde la carpeta ROOT de la imaagen del disco vamos a exportar cada uno de los archivos de metadatos llamdos $I30

![I30 en root](/assets/img/posts/analisis_ntfs/20241127_185608_Screenshot_From_2024-11-27_18-56-05.png)
_El de la raiz en root_

![I30 en papelera](/assets/img/posts/analisis_ntfs/20241127_185608_Screenshot_From_2024-11-27_18-56-05.png)
_El de la carpeta existente en la papelera_

![I30 en carpeta](/assets/img/posts/analisis_ntfs/20241127_185644_Screenshot_From_2024-11-27_18-56-41.png)
_El de la carpeta llamada carpeta_

![Archivos I30](/assets/img/posts/analisis_ntfs/20241127_185831_Screenshot_From_2024-11-27_18-58-09.png)

### Directorio "carpeta"

Con Indx2csv ahora vamos a importar el primero

![Configuración Indx2Csv](/assets/img/posts/analisis_ntfs/20241127_185915_Screenshot_From_2024-11-27_18-59-12.png)
_Recordar la opción dump everything y el separador_

Para determinar qué archivos están presentes y cuáles han sido eliminados o sobrescritos en base a los datos hay que fijarse en ciertas columnas que indican la validez y estado de los registros en la estructura del sistema NTFS

![Registros NTFS](/assets/img/posts/analisis_ntfs/20241127_190248_Screenshot_From_2024-11-27_19-02-25.png)

MFTReference y MFTReferenceSeqNo:
- Estos campos indican el número de referencia del archivo en la MFT (Master File Table) y el número de secuencia asociado. Un valor válido será generalmente positivo y consistente.

IndexFlags:
- Los índices indican propiedades del archivo en relación con el directorio y la MFT. Por ejemplo:
  - 0: Archivo regular
  - 1: Archivo eliminado o sobrescrito

IsNotLeaf y LastLsn:
- LastLsn puede usarse para correlacionar operaciones recientes con archivos
- IsNotLeaf indica si es un nodo hoja o tiene referencias a otros índices

Fechas (CTime, ATime, MTime, RTime):
- Si las fechas de modificación o creación parecen inconsistentes o fuera de rango, esto puede ser indicativo de eliminación o corrupción

![Registros eliminados](/assets/img/posts/analisis_ntfs/20241127_191047_Screenshot_From_2024-11-27_19-10-44.png)
_Tenemos dos registros eliminados y uno posiblemente corrupto o completamente eliminado debido al numero inusualmente elevado del MFTReference_

### Directorio en root

Procesamos el archivo igual que antes y vemos como los documentos de texto antes se encontraban en el directorio raíz

![Documentos en root](/assets/img/posts/analisis_ntfs/20241127_192401_Screenshot_From_2024-11-27_19-23-57.png)
_Observamos datos similares a los anteriores_

### Directorio de recycle bin

Mediante el mismo proceso analizamos el documento y observamos que no se ha eliminado por completo nada y que todos los archivos que hay fueron movidos al mismo tiempo a la papelera

![Archivos en papelera](/assets/img/posts/analisis_ntfs/20241127_192649_Screenshot_From_2024-11-27_19-26-45.png)

## 9. Recuva VS FTK Imager

Vamos a realizar una comparación entre un software que es utilizado para recuperar archivos eliminados del disco y FTK imager. Esto nos permitirá ver como realmente las herramientas forenses son mucho más potentes que las que comercialmente son vendidas y, además suelen ser más baratas o incluso open source.

Para usar este software primero debemos montar la imagen del disco mediante FTK o similares

![Montar imagen](/assets/img/posts/analisis_ntfs/20241127_193336_Screenshot_From_2024-11-27_19-33-33.png)
_Deberíamos ver el disco montado en Recuva_

Damos doble click sobre el disco y nos lo analizará en busca de archivos

![Análisis Recuva](/assets/img/posts/analisis_ntfs/20241127_193439_Screenshot_From_2024-11-27_19-34-37.png)

### Resultados en Recuva

Supuestamente ha encontrado 80 archivos que recuperar. Si observamos bien y comparamos con lo que nos muestra FTK, algunos de esos archivos ni siquiera existen o los está confundiendo con algunos de los rastros que han ido dejando esos movimientos como los que veíamos en el punto anterior donde el fichero "texto.txt" pasó de estar en root a la "carpeta"

![Resultados Recuva](/assets/img/posts/analisis_ntfs/20241127_193751_Screenshot_From_2024-11-27_19-37-44.png)

Por supuesto que si intentamos recuperar cualquiera de estos documentos nos pedirá pagar la licencia.

### Resultados en FTK Imager

Si analizamos manualmente el disco en FTK vemos que en la raíz del disco únicamente encontramos un documento PDF que fue eliminado aquí y no los rastros que dejó el movimiento del texto.txt, por ejemplo

![Análisis FTK](/assets/img/posts/analisis_ntfs/20241127_194349_Screenshot_From_2024-11-27_19-42-39.png)

Sin embargo si nos movemos al directorio carpeta vemos que si nos indica que existe el fichero texto.txt y que se encuentran los datos eliminados de otro llamado texto-copia.txt

![Archivos en carpeta](/assets/img/posts/analisis_ntfs/20241127_194512_Screenshot_From_2024-11-27_19-45-09.png)

El resto de documentos que indicaba Recuva realmente no están eliminados ni se llaman como lo indica. Además si necesitamos recuperar el archivo en FTK simplemente hacemos click derecho y lo exportamos, sin licencias ni nada.