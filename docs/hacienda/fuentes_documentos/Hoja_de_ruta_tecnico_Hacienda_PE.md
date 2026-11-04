# Hoja de ruta para el técnico de Hacienda — vía Python, proyecto policyengine-pr

Versión 2026-11-04 (rev. 1 del paquete PE). Tabulaciones agregadas del Formulario 482 para calibrar el modelo público de microsimulación contributiva de Puerto Rico (policyengine-pr) de Espacios Abiertos. El programa `pe_tabulaciones.py` produce hasta quince tablas (0 y A–J) ya protegidas con la regla de supresión de Hacienda (ninguna celda con menos de 10 planillas).

Qué hay que hacer de principio a fin, qué es cada archivo y qué parte escribe Hacienda. Carpeta `PE_Hacienda_Python` — Espacios Abiertos. Es un resumen: el detalle está en `01_documentos/Guia_ejecucion_Python_PE.pdf`.

## 1. En una frase

Hacienda construye, dentro de sus sistemas, un archivo con una fila por planilla de un año contributivo (y, si es posible, otro con una fila por comprobante W-2PR), lo valida, ejecuta un programa que produce tablas agregadas ya protegidas (ninguna celda con menos de 10 planillas, ningún conteo parcial entre 1 y 9 y ningún valor vacío que se pueda obtener restando filas), las revisa y nos envía solo esas tablas. El archivo de planillas nunca sale de Hacienda.

## 2. Los seis pasos

Todos los comandos se escriben desde la carpeta `PE_Hacienda_Python` (Terminal, Símbolo del sistema o la terminal de VS Code; hace falta Python 3.9 o posterior con `pandas`, `numpy` y `openpyxl`).

| Paso | Qué hace el técnico | Qué debe ver | Tiempo |
|---|---|---|---|
| 0 | Probar el programa con los datos ficticios del paquete y comprobar que reproduce nuestras salidas de referencia (dos comandos) | `RESULTADO GLOBAL: IDÉNTICAS dentro de la tolerancia, 15 tablas` | 2 minutos |
| 1 | Construir `planillas_<anio>.csv` con una consulta a SURI: una fila por planilla del año, con las 51 columnas de `esquema_planillas.csv` (14 necesarias y 37 que amplían las salidas; si alguna no se puede extraer, se quita y se anota en la ficha). Opcionalmente, `w2pr_<anio>.csv` con una fila por comprobante W-2PR. Es el único paso que requiere código propio de Hacienda; la plantilla está en `02_contrato_y_parametros/extraccion_SURI_plantilla.sql` | Un CSV por año y archivo | Según su equipo de datos |
| 2 | Validar los archivos: columnas, tipos, códigos, coherencia interna y, en pantalla, un resumen por año para cuadrar con sus propios totales | `0 error(es)`. Los AVISO no impiden seguir y se explican en la ficha de extracción; un ERROR se corrige en la consulta y se repite el paso | 10 minutos |
| 3 | Ejecutar las tabulaciones (un comando por año) | Los archivos `tabla_*.csv`, el libro `tabulaciones_482_<anio>.xlsx` y `log_ejecucion_pe.txt` en `06_salidas/salidas_<anio>` | Menos de 1 minuto por año |
| 4 | Revisar las salidas: comprobación automática y después la revisión propia de Hacienda | `RESULTADO: sin incidencias` (ningún conteo entre 1 y 9, celdas vacías donde corresponde, ninguna columna de identificación, totales que no revelan celdas vacías) | Según protocolo interno |
| 5 | Entregar a Espacios Abiertos por correo seguro | Los `tabla_*.csv` y el `.xlsx` de cada año, `log_ejecucion_pe.txt`, `validacion_entrada.txt`, `verificacion_salidas.txt` y la ficha de extracción rellenada. Nunca `planillas_<anio>.csv` ni `w2pr_<anio>.csv` | — |

Los comandos, en orden (copiar y pegar; en Windows suele ser `python`, en Mac `python3`):

```
# Paso 0 — prueba con datos ficticios
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada 03_datos_de_prueba/planillas_dummy.csv --w2pr 03_datos_de_prueba/w2pr_dummy.csv --salida 06_salidas/prueba --etiqueta PRUEBA
python 04_programas/comparar_salidas.py 05_salidas_de_referencia 06_salidas/prueba

# Paso 1 — construir planillas_2023.csv (y w2pr_2023.csv) con la consulta de Hacienda (sin comando nuestro)

# Paso 2 — validar
python 04_programas/validar_entrada.py --entrada planillas_2023.csv --w2pr w2pr_2023.csv --anio 2023 --informe 06_salidas/validacion_entrada_2023.txt

# Paso 3 — ejecutar (repetir para cada año: 2021, 2022, 2023, 2024)
python 04_programas/pe_tabulaciones.py --anio 2023 --entrada planillas_2023.csv --w2pr w2pr_2023.csv --salida 06_salidas/salidas_2023 --fecha-corte "AAAA-MM-DD"

# Paso 4 — revisar
python 04_programas/verificar_salidas.py --salida 06_salidas/salidas_2023 --informe 06_salidas/verificacion_salidas_2023.txt
```

## 3. Qué es cada archivo

| Archivo | Qué es | Quién lo escribe |
|---|---|---|
| `02_contrato_y_parametros/esquema_planillas.csv` | Las 51 columnas del archivo de planillas: nombre, si es necesaria, tipo, rango, descripción, línea del Formulario 482 y qué se omite si falta | Espacios Abiertos; Hacienda lo lee |
| `02_contrato_y_parametros/esquema_w2pr.csv` | Las 6 columnas del archivo de comprobantes W-2PR (opcional) | Espacios Abiertos; Hacienda lo lee |
| `02_contrato_y_parametros/extraccion_SURI_plantilla.sql` | Plantilla de la consulta, con nombres de tablas y campos inventados entre `< >` | Hacienda la adapta |
| `02_contrato_y_parametros/ficha_extraccion_plantilla.csv` | Ficha que documenta la extracción (fecha, corte, líneas reales usadas por año, columnas no disponibles, filas por año) | Hacienda la rellena y la entrega |
| `03_datos_de_prueba/planillas_dummy.csv`, `w2pr_dummy.csv` | 25,000 planillas y 40,000 comprobantes inventados con la estructura de los archivos de entrada; `gen_dummy.py` los generó | Espacios Abiertos |
| `04_programas/pe_tabulaciones.py` | El programa: lee los archivos, produce las tablas 0 y A–J, aplica la supresión y escribe CSV, Excel y registro | Espacios Abiertos |
| `04_programas/validar_entrada.py` | Comprueba el contrato de datos antes de ejecutar (paso 2) | Espacios Abiertos |
| `04_programas/verificar_salidas.py` | Comprueba las salidas antes de entregarlas (paso 4) | Espacios Abiertos |
| `04_programas/comparar_salidas.py` | Compara dos carpetas de salidas (paso 0) | Espacios Abiertos |
| `05_salidas_de_referencia/` | Las quince tablas, el libro Excel y el registro obtenidos con los datos ficticios, con los informes de validación y verificación; la subcarpeta `modalidad_vaciar` muestra la otra modalidad de supresión | Espacios Abiertos |
| `06_salidas/` | Carpeta de trabajo donde se escriben las salidas | El programa |

## 4. Qué parte escribe Hacienda

Solo la consulta del paso 1 y la ficha de extracción. Ningún programa necesita cambios: los nombres de las columnas son fijos y, si una columna no se puede extraer, basta con no incluirla (el programa omite lo que depende de ella y lo anota en el registro). Si Hacienda prefiere la otra modalidad de supresión (filas vacías en lugar de colapsadas), se añade `--supresion vaciar` al comando del paso 3; ambas modalidades se describen en la Especificación de salidas.

## 5. Contacto

Daniel Santamaría Ots — Espacios Abiertos — daniel@espaciosabiertos.org
