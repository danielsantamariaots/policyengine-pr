# PE_Hacienda_Python — versión del 4 de noviembre de 2026 (rev. 1 del paquete PE)

Proyecto policyengine-pr — modelo público de microsimulación contributiva de Puerto Rico — Espacios Abiertos. Acompaña a la carta «Solicitud de tabulaciones estadísticas agregadas de la Planilla de Contribución sobre Ingresos de Individuos (Formulario 482), años contributivos 2021 a 2024».

Esta carpeta contiene **todo lo necesario** para que el Departamento de Hacienda construya los archivos de entrada y produzca las tabulaciones dentro de sus sistemas: cuatro documentos, el contrato de datos con sus plantillas, los datos de prueba, los cuatro programas y las salidas de referencia. Es autosuficiente: con Python 3.9 o posterior y los paquetes `pandas`, `numpy` y `openpyxl`, los seis pasos se ejecutan desde aquí sin ningún otro archivo.

El archivo de entrada tiene una fila por planilla y año contributivo (2021–2024) y **51 columnas**, de las que **14 son necesarias para ejecutar**; las otras 37 amplían las salidas: si alguna no se puede extraer, el programa omite solo lo que depende de ella y lo anota en el registro. Un segundo archivo opcional, con una fila por comprobante W-2PR (6 columnas), produce la Tabla I. El programa `pe_tabulaciones.py` produce hasta **quince tablas** (`tabla_0_control` … `tabla_J`) ya protegidas: ninguna fila con menos de 10 planillas (colapsada en la contigua, conservando los totales), ningún conteo parcial ni complemento entre 1 y 9, y ningún valor vacío que se pueda obtener restando filas. La clave seudónima `id_persona` del archivo W-2PR, generada por Hacienda, se usa solo para contar personas distintas y no aparece en ninguna salida.

| Carpeta | Contenido | Cuándo se usa |
|---|---|---|
| `01_documentos/` | `Hoja_de_ruta_tecnico_Hacienda_PE.pdf` (los seis pasos, los archivos y los programas en pocas páginas); `Guia_ejecucion_Python_PE.pdf` (la guía operativa completa); `Especificacion_salidas_PE.pdf` (la definición formal del contrato, las reglas y las tablas); `Descripcion_conceptual_PE_Hacienda.pdf` (qué es el modelo, qué mide cada tabla y por qué, para el equipo de análisis económico). Cada uno también en `.docx` | Para leer |
| `02_contrato_y_parametros/` | `esquema_planillas.csv` (las 51 columnas, con si es necesaria, tipo, rango, línea del Formulario 482 y qué se omite si falta); `esquema_w2pr.csv` (las 6 columnas del archivo de comprobantes); `extraccion_SURI_plantilla.sql` (plantilla de la consulta, con nombres de tablas y campos inventados entre `< >`); `ficha_extraccion_plantilla.csv` (ficha que documenta la extracción) | Pasos 1, 2 y 5 |
| `03_datos_de_prueba/` | `planillas_dummy.csv` (25,000 planillas inventadas) y `w2pr_dummy.csv` (40,000 comprobantes inventados) con la estructura de los archivos de entrada, y `gen_dummy.py` (su generador; no hace falta ejecutarlo) | Paso 0 |
| `04_programas/` | `validar_entrada.py` (paso 2) · `pe_tabulaciones.py` (pasos 0 y 3, tablas 0 y A–J) · `verificar_salidas.py` (paso 4) · `comparar_salidas.py` (paso 0) | Pasos 0 a 4 |
| `05_salidas_de_referencia/` | Las quince tablas, el libro Excel y el registro obtenidos con los datos ficticios, los informes de validación y verificación de esa prueba, y la subcarpeta `modalidad_vaciar` con la otra modalidad de supresión | Paso 0 |
| `06_salidas/` | Carpeta de trabajo donde se escriben las salidas de cada ejecución (`prueba`, `salidas_<anio>`) | Pasos 0, 3 y 4 |
| `MANIFIESTO_md5.txt` | Suma de comprobación de cada archivo de esta carpeta, para verificar que llegó íntegra | Al recibirla |

## Los seis pasos (comandos desde esta carpeta; en Windows suele ser `python`, en Mac `python3`)

```
# Paso 0 — prueba con datos ficticios (esperado al final: RESULTADO GLOBAL: IDÉNTICAS dentro de la tolerancia, 15 tablas)
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada 03_datos_de_prueba/planillas_dummy.csv --w2pr 03_datos_de_prueba/w2pr_dummy.csv --salida 06_salidas/prueba --etiqueta PRUEBA
python 04_programas/comparar_salidas.py 05_salidas_de_referencia 06_salidas/prueba

# Paso 1 — construir planillas_<anio>.csv (y, si es posible, w2pr_<anio>.csv) con la consulta de Hacienda, según
#          02_contrato_y_parametros/esquema_planillas.csv, a partir de extraccion_SURI_plantilla.sql;
#          documentar la extracción en ficha_extraccion_plantilla.csv

# Paso 2 — validar (esperado: 0 error(es); los avisos se explican en la ficha)
python 04_programas/validar_entrada.py --entrada planillas_2023.csv --w2pr w2pr_2023.csv --anio 2023 --informe 06_salidas/validacion_entrada_2023.txt

# Paso 3 — ejecutar (una vez por año)
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada planillas_2023.csv --w2pr w2pr_2023.csv --salida 06_salidas/salidas_2023 --fecha-corte "AAAA-MM-DD"

# Paso 4 — revisar (esperado: RESULTADO: sin incidencias) y después la revisión propia de Hacienda
python 04_programas/verificar_salidas.py --salida 06_salidas/salidas_2023 --informe 06_salidas/verificacion_salidas_2023.txt

# Paso 5 — entregar a Espacios Abiertos: 06_salidas/salidas_<anio>/tabla_*.csv y tabulaciones_482_<anio>.xlsx,
#          log_ejecucion_pe.txt, validacion_entrada_<anio>.txt, verificacion_salidas_<anio>.txt y la ficha de
#          extracción rellenada. Nunca planillas_<anio>.csv ni w2pr_<anio>.csv.
```

Si Hacienda prefiere la modalidad de supresión de los paquetes anteriores de Espacios Abiertos (filas vacías en lugar de colapsadas), se añade `--supresion vaciar` al comando del paso 3; las dos modalidades están descritas en la Especificación de salidas.

## Para verificar la integridad de la carpeta

En Mac o Linux: `md5sum -c MANIFIESTO_md5.txt` desde esta carpeta (en Mac, si no está `md5sum`: `md5 -r <archivo>`). En Windows (PowerShell): `Get-FileHash -Algorithm MD5 <archivo>` y comparar con el manifiesto.

Requisitos: Python 3.9 o posterior con `pandas` (1.5 o posterior), `numpy` y `openpyxl`; sin internet durante la ejecución; unos 2 GB de memoria por millón de planillas (se ejecuta año por año). Agradecemos al Departamento su colaboración. Contacto: Daniel Santamaría Ots — daniel@espaciosabiertos.org
