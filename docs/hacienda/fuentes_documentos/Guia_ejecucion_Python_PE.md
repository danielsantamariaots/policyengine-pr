# Guía de ejecución — vía Python, proyecto policyengine-pr

Versión 2026-11-04 (rev. 1 del paquete PE). Espacios Abiertos. Guía operativa completa para el equipo técnico del Departamento de Hacienda: cómo construir los archivos de entrada, validarlos, ejecutar el programa, revisar las salidas y entregarlas. La Hoja de ruta resume estos pasos en pocas páginas; la Especificación de salidas define formalmente el contrato de datos, las reglas de confidencialidad y cada tabla.

## 1. Qué produce el programa y por qué

Espacios Abiertos desarrolla policyengine-pr, un modelo de microsimulación de código abierto del sistema contributivo de individuos de Puerto Rico. El modelo codifica las reglas del Código de Rentas Internas de 2011 a partir de los formularios e instrucciones oficiales y usa como base de datos la Encuesta sobre la Comunidad de Puerto Rico. Para que sus estimaciones de recaudo sean confiables, esa base debe calibrarse a los totales administrativos reales de las planillas. Las tablas que produce este paquete son esos totales: sumas y conteos por tramo de ingreso bruto ajustado, estado personal, número de dependientes, edad y municipio, para cada año contributivo de 2021 a 2024.

El programa `pe_tabulaciones.py` lee el archivo de planillas de un año, calcula las tablas 0 y A–J y aplica la regla de supresión de Hacienda antes de escribir nada. Ninguna salida contiene datos individuales.

## 2. Paso 0 — Prueba con datos ficticios (antes de tocar datos reales)

Requisitos: Python 3.9 o posterior con `pandas` (1.5 o posterior), `numpy` y `openpyxl`. Sin internet durante la ejecución. Comprobar con `python --version` y `python -c "import pandas, numpy, openpyxl"`; si falta algo, `pip install pandas numpy openpyxl`.

Desde la carpeta `PE_Hacienda_Python`:

```
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada 03_datos_de_prueba/planillas_dummy.csv --w2pr 03_datos_de_prueba/w2pr_dummy.csv --salida 06_salidas/prueba --etiqueta PRUEBA
python 04_programas/comparar_salidas.py 05_salidas_de_referencia 06_salidas/prueba
```

El primer comando tarda menos de un minuto y escribe quince tablas, un libro Excel y el registro en `06_salidas/prueba`. El segundo compara esas salidas con las de referencia del paquete y debe terminar con `RESULTADO GLOBAL: IDÉNTICAS dentro de la tolerancia, 15 tablas`. Si difiere, la causa habitual es una versión de pandas muy distinta; anótenlo en la ficha y avísennos.

Los datos ficticios son 25,000 planillas y 40,000 comprobantes inventados por `03_datos_de_prueba/gen_dummy.py` con distribuciones verosímiles y las reglas de 2025 aproximadas. No son datos de Hacienda ni sirven para ningún análisis: solo prueban el programa y muestran el formato de las salidas. La marca `--etiqueta PRUEBA` aparece en el Léame y en el título de cada hoja del libro Excel para que nadie confunda estas salidas con las reales.

## 3. Paso 1 — Construir los archivos de entrada

### 3.1 Universo y unidad

Una fila por planilla de individuos (Formulario 482) radicada para el año contributivo, en su versión vigente (si hay enmiendas, una sola fila: la última válida), con las planillas radicadas hasta la fecha de corte que Hacienda indique en la ficha (incluyendo prórrogas). Un archivo por año contributivo (2021, 2022, 2023 y 2024) o un solo archivo con la columna `anio`.

Opcionalmente, un archivo de comprobantes W-2PR (Formulario 499R-2/W-2PR) con una fila por comprobante, de todas las personas, rindan o no planilla. Es la única fuente administrativa sobre quienes devengan salarios y no rinden planilla.

### 3.2 Columnas

Están en `02_contrato_y_parametros/esquema_planillas.csv` (51 columnas) y `esquema_w2pr.csv` (6 columnas). Cada fila del esquema da el nombre fijo de la columna, si es necesaria, el tipo, el rango válido, la descripción, la línea del Formulario 482 de 2025 y qué se omite si falta.

Las 14 columnas necesarias del archivo de planillas: `estado_personal`, `edad`, `salarios`, `iba`, `deducciones`, `exencion_personal`, `exencion_dependientes`, `num_dependientes`, `ingreso_neto`, `contribucion_tabla`, `contribucion_regular`, `responsabilidad`, `credito_trabajo`, `creditos_federales`. Sin alguna de ellas el programa se detiene. Las otras 37 amplían las salidas: si alguna no se puede extraer, se quita de la consulta y el programa omite solo la tabla o la columna que depende de ella (por ejemplo, sin `municipio` no hay Tabla J; sin `factor` no hay Tabla F ni las columnas 92 %/95 % de la Tabla A).

Reglas comunes: nombres en minúsculas, sin ñ ni acentos; 0 cuando el concepto no aplica; celda vacía solo cuando el dato no consta; ningún identificador (ni número de seguro social, ni nombre, ni número de planilla). En el archivo W-2PR, la única clave es `id_persona`, un hash con clave secreta que genera Hacienda y que el programa usa solo para contar personas distintas; nunca aparece en las salidas.

### 3.3 Esquema de la consulta de extracción

`02_contrato_y_parametros/extraccion_SURI_plantilla.sql` es una consulta en SQL genérico con todos los nombres de tablas y campos inventados entre `< >`. El equipo de Hacienda los sustituye por los reales, la ejecuta y exporta el resultado a CSV (UTF-8, separador coma, punto decimal, sin separadores de miles, celda vacía para los nulos). El orden de las columnas no importa; los nombres sí. Las líneas del Formulario 482 que se citan son las de 2025 y cambian entre años: la correspondencia real usada en cada año se anota en la ficha.

### 3.4 La ficha de extracción

`02_contrato_y_parametros/ficha_extraccion_plantilla.csv` documenta la extracción: fecha, años y fecha de corte, tabla de origen, tratamiento de las enmiendas, codificación del estado personal, regla de edad, cómo se obtuvo el factor 92 %/95 %, cómo se identifican los créditos ajustados, códigos de municipio, fuente y clave de los W-2PR, filas por año y columnas no disponibles. Se rellena en el paso 1 y se entrega en el paso 5: es el libro de códigos de las tablas recibidas.

## 4. Paso 2 — Validar los archivos de entrada

```
python 04_programas/validar_entrada.py --entrada planillas_2023.csv --w2pr w2pr_2023.csv --anio 2023 --informe 06_salidas/validacion_entrada_2023.txt
```

Comprueba la codificación UTF-8, las columnas presentes y faltantes (necesarias: ERROR; que amplían: AVISO con lo que se omite), los tipos, los rangos y códigos (estado personal 1–4, edad 0–120, factor 0.92 o 0.95, indicadores 0/1, signos), la coherencia interna (ingreso neto no mayor que el IBA, contribución regular igual a la contribución según tabla más el ajuste gradual por el factor, exención de jóvenes solo entre 16 y 26 años, crédito reclamado distinto del concedido sin marca de ajuste) y, en pantalla, un resumen por año (planillas y sumas de las variables fiscales) para cuadrar con los totales de Hacienda.

Debe terminar con `0 error(es)`. Los avisos no impiden seguir y se explican en la ficha; un error se corrige en la consulta y se repite el paso. El informe guardado repite las comprobaciones sin conteos de filas ni sumas (salvo el total de filas): las cifras del resumen por año se muestran solo en pantalla, porque la Tabla 0 de control ya las entrega protegidas.

## 5. Paso 3 — Ejecutar las tabulaciones

### 5.1 Comando

```
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada planillas_2023.csv --w2pr w2pr_2023.csv --salida 06_salidas/salidas_2023 --fecha-corte "AAAA-MM-DD"
```

Opciones: `--w2pr` (omitir si no hay archivo de comprobantes: no se producen las Tablas I e I_edad); `--supresion colapsar|vaciar` (modalidad de supresión; por defecto `colapsar`, la que pide la carta de solicitud; véase la sección 5.4); `--fecha-corte` (texto que se copia al Léame del libro Excel); `--etiqueta` (solo para pruebas). Se repite el comando para cada año, con una carpeta de salida por año.

### 5.2 Memoria y tiempo

Con un millón de planillas y 51 columnas el archivo ocupa unos 400 MB en CSV y el programa necesita unos 2 GB de memoria; tarda menos de un minuto. Se ejecuta año por año, de modo que nunca hace falta cargar todos los años a la vez.

### 5.3 Qué hace el programa, en orden

1. Lee la cabecera y comprueba que estén las 14 columnas necesarias (si falta alguna, se detiene con un mensaje que las nombra); anota en el registro cada columna que amplía las salidas y no está, con lo que omite.
2. Si existe la columna `anio`, se queda con las filas del año indicado.
3. Calcula la Tabla 0 de control: totales del archivo de entrada (planillas, sumas y conteos de las variables principales, planillas por estado personal y por factor, comprobantes W-2PR y personas distintas).
4. Para cada tabla A–J: asigna a cada planilla su tramo (de IBA, de ingreso ganado, de edad, etc.), agrega sumas y conteos por fila, calcula las filas de totales sobre todas las planillas (son exactas), aplica la protección de filas (colapso o vaciado) y después la protección de celdas (conteos parciales y sus sumas).
5. Escribe un CSV por tabla, el libro Excel (una hoja por tabla, más «Léame» y «Diccionario») y el registro `log_ejecucion_pe.txt`.

### 5.4 Reglas de confidencialidad que aplica el programa

1. Ninguna fila publicada tiene menos de 10 planillas (o comprobantes, en las Tablas I). Modalidad `colapsar`: la fila se une a la contigua (el tramo inmediatamente inferior; si es la primera, al superior) hasta que ninguna quede por debajo de 10; la etiqueta pasa a ser el tramo combinado («$150,001 o más»), la columna `nota` lleva «c» y `supr` vale 1. Los totales se conservan exactos. Modalidad `vaciar`: la fila se publica con su etiqueta y todos sus valores vacíos (`supr` = 1); si las filas vacías de un grupo fueran una sola o sumaran menos de 10 planillas, se vacían además las filas más pequeñas necesarias (`supr` = 2, «para proteger otras»), de modo que el total no permita deducirlas.
2. Dentro de cada fila publicada, todo conteo parcial (`planillas_*`, `personas_distintas`) entre 1 y 9, o cuyo complemento respecto del conteo de la fila esté entre 1 y 9, se deja vacío, junto con las sumas que dependen de él (por ejemplo, `planillas_ded_hipoteca` y `ded_hipoteca`).
3. Por columna y grupo, las celdas vacías de las filas publicadas deben ser dos o más y sumar 0 o al menos 10 (lo que se deduce del total); si no, se vacían otras celdas (las más pequeñas) y, en último término, la del total.
4. No se redondea ningún valor: la protección es la supresión y el colapso.
5. El registro indica, por tabla, cuántas filas se colapsaron o vaciaron y cuántas celdas se vaciaron por cada regla.

## 6. Paso 4 — Revisar las salidas

### 6.1 Los archivos

En `06_salidas/salidas_<anio>`: `tabla_0_control.csv`, `tabla_A.csv` … `tabla_J.csv` (hasta 15 tablas según las columnas disponibles), `tabulaciones_482_<anio>.xlsx` (las mismas tablas, una por hoja, con las filas colapsadas en amarillo y las vaciadas en gris) y `log_ejecucion_pe.txt`.

### 6.2 Comprobación automática

```
python 04_programas/verificar_salidas.py --salida 06_salidas/salidas_2023 --informe 06_salidas/verificacion_salidas_2023.txt
```

Trabaja solo con los archivos de salida y comprueba, tabla por tabla: que existen las columnas `nota` y `supr` y ninguna de identificación; que todo conteo es 0, está vacío o es 10 o más y ningún conteo parcial deja un complemento entre 1 y 9; que las filas vaciadas no tienen ningún valor publicado y las sumas están vacías cuando su conteo lo está; que en cada grupo el total publicado menos las filas publicadas es 0 (colapsar) o corresponde a dos o más filas vacías y 10 o más planillas (vaciar), y lo mismo columna por columna; y que el registro existe. Debe terminar con `RESULTADO: sin incidencias`. Es una segunda comprobación: no sustituye la revisión de Hacienda.

### 6.3 Para la revisión metodológica

La Tabla 0 de control da los totales del archivo de entrada por año; cuadrarlos con los totales propios de Hacienda (los del resumen por año del paso 2 y los de la consulta) confirma que el programa leyó el archivo completo. Las filas de totales de cada tabla A–J suman las mismas planillas que la Tabla 0 (salvo las tablas que seleccionan un subconjunto: D, E, F, G).

## 7. Paso 5 — Entrega a Espacios Abiertos

Por correo seguro o el medio que Hacienda prefiera:

1. Los archivos `tabla_*.csv` y `tabulaciones_482_<anio>.xlsx` de cada año.
2. `log_ejecucion_pe.txt` de cada año.
3. `validacion_entrada_<anio>.txt` y `verificacion_salidas_<anio>.txt`.
4. La ficha de extracción rellenada (`ficha_extraccion_plantilla.csv`).

Nunca `planillas_<anio>.csv` ni `w2pr_<anio>.csv`.

## 8. Preguntas frecuentes

**¿Qué pasa si no tenemos alguna columna?** Se quita de la consulta. El programa omite solo lo que depende de ella (columna `si_falta` del esquema) y lo anota en el registro y en el Léame del libro Excel. Las 14 necesarias no pueden faltar.

**¿Podemos cambiar los tramos o el umbral de supresión?** Sí: están al inicio de `pe_tabulaciones.py` (`TRAMOS_IBA`, `MIN_N`). Si lo hacen, anótenlo en la ficha para que sepamos cómo leer las tablas.

**¿Podemos usar nuestro propio programa?** Sí, siempre que las tablas tengan la misma estructura (mismas filas, columnas y reglas de supresión); `verificar_salidas.py` sirve igual para comprobarlas.

**¿Por qué la modalidad colapsar por defecto?** Porque conserva los totales exactos de cada columna, que es lo que el modelo necesita para calibrarse, y porque es lo que pide la carta de solicitud. La modalidad vaciar es la de los paquetes anteriores de Espacios Abiertos (William T. Grant y Arnold Ventures); el programa la ofrece por si Hacienda prefiere mantener un único criterio.

**¿Las salidas de prueba se parecen a las reales?** Solo en el formato. Las cifras son inventadas.

## 9. Contacto

Daniel Santamaría Ots — Espacios Abiertos — daniel@espaciosabiertos.org
