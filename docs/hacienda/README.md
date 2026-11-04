# Petición de datos a Hacienda

Material que acompaña a `docs/solicitud_datos_hacienda.docx`, con la misma estructura que los paquetes que Espacios Abiertos entregó a Hacienda en los proyectos William T. Grant y Arnold Ventures.

| Carpeta | Qué es |
|---|---|
| `paquete/` | **`PE_Hacienda_Python`**: lo que se envía a Hacienda. `00_LEEME_primero.md`, `01_documentos/` (cuatro documentos en .docx y .pdf), `02_contrato_y_parametros/` (esquemas, plantilla SQL, ficha), `03_datos_de_prueba/`, `04_programas/`, `05_salidas_de_referencia/`, `06_salidas/`, `MANIFIESTO_md5.txt`. |
| `peticion/` | `Peticion_datos_Hacienda_policyengine-pr.xlsx` (libro de petición: peticiones, columnas, reglas, una hoja por tabla con la plantilla vacía) y el script que lo construye. |
| `fuentes_documentos/` | Los cuatro documentos en Markdown y `md2docx.js`, que los convierte a Word (`npm install docx` en esta carpeta; el PDF se exporta desde Word). |

## Qué enviar a Hacienda

El `.docx` de la carta, el zip de `paquete/` (renombrado `PE_Hacienda_Python_<fecha>.zip`) y el `.xlsx` de `peticion/`.

## Probar localmente

```bash
cd docs/hacienda/paquete
../../../.venv/bin/python 04_programas/pe_tabulaciones.py --anio 2023 --entrada 03_datos_de_prueba/planillas_dummy.csv --w2pr 03_datos_de_prueba/w2pr_dummy.csv --salida 06_salidas/prueba --etiqueta PRUEBA
../../../.venv/bin/python 04_programas/comparar_salidas.py 05_salidas_de_referencia 06_salidas/prueba
```

Requiere `pandas`, `numpy` y `openpyxl` (`uv pip install openpyxl` en el `.venv` del repo). El paquete está excluido de `ruff` (`pyproject.toml`) porque sigue el estilo de 120 columnas de los paquetes anteriores.

## Regenerar

- Datos de prueba: `python 03_datos_de_prueba/gen_dummy.py` (desde `paquete/`).
- Salidas de referencia: ejecutar `pe_tabulaciones.py` con `--salida 05_salidas_de_referencia` (y `--supresion vaciar --salida 05_salidas_de_referencia/modalidad_vaciar`), más `validar_entrada.py --informe` y `verificar_salidas.py --informe` en esa carpeta.
- Documentos: `node fuentes_documentos/md2docx.js fuentes_documentos/<doc>.md paquete/01_documentos/<doc>.docx`; PDF desde Word.
- Libro de petición: `python peticion/construir_peticion_excel.py` (lee los esquemas y las salidas de referencia en modalidad vaciar).
- Manifiesto: desde `paquete/`, `find . -type f ! -name MANIFIESTO_md5.txt ! -path './06_salidas/prueba*' | sort | xargs md5 -r | sed 's#  \./#  #' > MANIFIESTO_md5.txt` (en Mac).

## Supresión

El programa aplica la regla de Hacienda (N < 10) en dos modalidades: `colapsar` (la que pide la carta: la fila pequeña se une a la contigua y los totales se conservan) y `vaciar` (la de los paquetes WTG y AV). En ambas se vacían los conteos parciales entre 1 y 9 y sus sumas, y se protegen los totales. Detalle en `fuentes_documentos/Especificacion_salidas_PE.md`, sección 3.
