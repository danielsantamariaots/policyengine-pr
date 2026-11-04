# Especificación de salidas — proyecto policyengine-pr

Versión 2026-11-04 (rev. 1 del paquete PE). Espacios Abiertos. Definición formal del contrato de datos, de las reglas de confidencialidad que aplica el programa `pe_tabulaciones.py` y de cada una de las tablas de salida. Es el documento de referencia para el personal de estadísticas y de confidencialidad de Hacienda; la Guía de ejecución explica cómo se usa el paquete.

## 1. Objeto

Tabulaciones agregadas de la Planilla de Contribución sobre Ingresos de Individuos (Formulario 482) y, si es posible, de los comprobantes de retención W-2PR, por año contributivo (2021 a 2024), con las que Espacios Abiertos calibrará y validará el modelo público de microsimulación contributiva policyengine-pr. No se solicita ningún dato individual.

## 2. Archivos de entrada

**Planillas** (`planillas_<anio>.csv`): una fila por planilla vigente del año contributivo; 51 columnas definidas en `02_contrato_y_parametros/esquema_planillas.csv`, con nombre fijo, tipo, rango válido, descripción, línea del Formulario 482 de 2025 y consecuencia si falta. Son necesarias 14: `estado_personal` (1 individual; 2 casado que rinde planilla conjunta; 3 casado que rinde planilla separada; 4 cómputo opcional), `edad` (al cierre del año), `salarios` (1A–1C), `iba` (5), `deducciones` (6), `exencion_personal` (7), `exencion_dependientes` y `num_dependientes` (8), `ingreso_neto` (13), `contribucion_tabla` (14), `contribucion_regular` (17), `responsabilidad` (26), `credito_trabajo` (27C) y `creditos_federales` (27D). Las 37 restantes amplían las salidas: ingresos por concepto (líneas 1–4), `ajuste_gradual` (15), `factor` e `ingreso_bruto_factor` (Sección 1021.01(c)), créditos (18, 21, 25), `exceso_cba` (20), `retenida_salarios` (27A), `sobrepago` (29), `balance_pendiente` (31), las deducciones del Anejo A, los ingresos exentos del Anejo IE, el Anejo CT (`ct_dependientes`, `ct_ingreso_ganado`, `ct_reclamado`, `ct_ajustado`), el Anejo O (`cba_ingreso_neto`, `cba_contribucion`), `municipio` y `anio`.

**Comprobantes W-2PR** (`w2pr_<anio>.csv`, opcional): una fila por comprobante, de todas las personas; 6 columnas (`esquema_w2pr.csv`): `id_persona` (clave seudónima generada por Hacienda, que no aparece en las salidas), `salarios`, `retenida`, `exento_135` (encasillado 16, código E), `edad` y `anio`.

Reglas: nombres en minúsculas sin ñ ni acentos; 0 cuando el concepto no aplica; celda vacía solo cuando el dato no consta; ningún identificador. `validar_entrada.py` comprueba el contrato antes de la ejecución.

## 3. Reglas de confidencialidad que aplica el programa

1. **Umbral.** `MIN_N` = 10 planillas (o comprobantes en las Tablas I), conforme a la regla de supresión de Hacienda. Ninguna fila publicada tiene un conteo entre 1 y 9.
2. **Filas, modalidad `colapsar` (por defecto).** Una fila con menos de 10 planillas se une a la fila contigua: el tramo inmediatamente inferior o, si es la primera, el superior; en las tablas sin tramos (estado personal, dependientes, municipio), la fila anterior en el orden de la tabla. Se repite hasta que ninguna fila quede por debajo de 10. La etiqueta pasa a ser el tramo combinado (por ejemplo, «$10,001 – $20,000» o «$150,001 o más»), `nota` lleva «c» y `supr` vale 1. Los totales se conservan exactos. Dentro de las tablas con grupos (estado personal × tramo), el colapso ocurre dentro de cada grupo.
3. **Filas, modalidad `vaciar`.** La fila conserva su etiqueta y todos sus valores quedan vacíos (`nota` «s», `supr` 1). Si en un grupo las filas vacías fueran una sola, o sumaran menos de 10 planillas, se vacían además las filas publicadas más pequeñas hasta que sean dos o más y sumen 10 o más (`supr` 2), de modo que la fila de totales no permita deducirlas.
4. **Celdas.** En toda fila publicada, un conteo parcial (`planillas_*`, `personas_distintas`) entre 1 y 9, o cuyo complemento respecto del conteo de la fila (`planillas` menos el parcial) esté entre 1 y 9, se deja vacío, y con él las sumas que dependen de ese conteo: por regla general `planillas_X` protege la columna `X`; `planillas_num_dependientes` protege `num_dependientes` y `exencion_dependientes`; `planillas_92` y `planillas_95` protegen `contribucion_regular_92` y `contribucion_regular_95`.
5. **Complementaria de celdas.** Por columna y grupo, las celdas vacías de las filas publicadas deben ser dos o más y sumar 0 o al menos 10; si no, se vacían las celdas positivas más pequeñas que hagan falta y, si no queda ninguna, la celda del total.
6. **Totales.** Las filas «Total» (por grupo) y «Total general» se calculan sobre todas las planillas antes de la protección; sus valores son exactos salvo cuando la regla 5 los vacía.
7. **Código `supr`.** 0 = fila publicada; 1 = colapsada o vaciada por tener menos de 10 planillas; 2 = vaciada para proteger otras.
8. No se redondea ningún valor. Ninguna salida contiene identificadores ni valores de una sola planilla.
9. El registro `log_ejecucion_pe.txt` indica, por tabla, las filas colapsadas o vaciadas y las celdas vaciadas por cada regla; no contiene conteos que no estén en las tablas.

## 4. Columnas comunes a todas las tablas

| Columna | Contenido |
|---|---|
| `planillas` (o `planillas_ajustadas`, `comprobantes`) | Conteo de la fila |
| `planillas_X` | Planillas de la fila con la columna X mayor que cero (conteo parcial) |
| `X` (nombre de línea) | Suma en dólares de la línea X en las planillas de la fila |
| `nota` | «c» fila colapsada; «s» fila vaciada; vacío en las demás |
| `supr` | 0, 1 o 2 según la sección 3 |

Los nombres de las columnas de suma son los del esquema de entrada; la hoja «Diccionario» del libro Excel da la descripción y la línea del Formulario 482 de cada una.

## 5. Las tablas de salida

Tramos de IBA (línea 5), usados en A, B y C: $0 o menos; $1–10,000; 10,001–15,000; 15,001–20,000; 20,001–25,000; 25,001–30,000; 30,001–40,000; 40,001–50,000; 50,001–60,000; 60,001–75,000; 75,001–100,000; 100,001–150,000; 150,001–250,000; 250,001–500,000; 500,001 o más. Los límites superiores están incluidos.

| Tabla | Filas | Columnas | Selección y columnas necesarias |
|---|---|---|---|
| 0 Control | Una fila por año | `planillas`; para salarios, IBA, ingreso neto, contribución regular, responsabilidad, Crédito por Trabajo, créditos federales, exención de jóvenes, Anejo A, Anejo IE, ajuste gradual y CBA: planillas con valor y suma; planillas por estado personal (1–4) y por factor (92/95); comprobantes W-2PR, personas distintas y salarios W-2PR | Todas las planillas del archivo; sirve para cuadrar con los totales de Hacienda |
| A Resumen | Estado personal × 15 tramos de IBA, con Total por estado y Total general | `planillas`, `planillas_num_dependientes`, `planillas_credito_trabajo`, las sumas de las líneas 1A–31 (salarios, intereses y dividendos, pensiones, distribuciones de retiro, ganancia de capital, entidades conducto, industria o negocio, pensión por divorcio, IBA, deducciones, exenciones, ingreso neto, contribución según tabla, ajuste gradual, contribución regular, créditos, exceso de CBA, responsabilidad, retención, Crédito por Trabajo, créditos federales, sobrepago, balance), y `planillas_92`, `contribucion_regular_92`, `planillas_95`, `contribucion_regular_95` | Todas las planillas; las columnas de líneas no disponibles se omiten |
| B Anejo A | 15 tramos de IBA + Total | Para intereses hipotecarios (1i), gastos médicos (3), donativos (4), IRA (7b), cuentas educativas (8b), préstamos estudiantiles (9b) y total (11): `planillas_ded_*` y suma | Requiere `ded_total` |
| C Anejo IE | 15 tramos de IBA, calculado sobre IBA + ingresos exentos (para que la exención no mueva de tramo) + Total | Para exención de pensiones, exención de jóvenes (31), profesionales de difícil reclutamiento (32) y total (45): `planillas_exento_*` y suma | Requiere `exento_total` |
| D1 Crédito por Trabajo | Estado personal × dependientes cualificados (0, 1, 2, 3 o más) + totales | `planillas`, `credito_trabajo`, `ct_ingreso_ganado` | Planillas con crédito concedido > 0; requiere `ct_dependientes` |
| D2 Crédito por Trabajo por ingreso ganado | Dependientes (0, 1, 2, 3 o más) × tramos de ingreso bruto ganado de $2,500 desde $0 hasta $55,000 y «$55,001 o más» + totales | `planillas`, `credito_trabajo` | Planillas con crédito > 0; requiere `ct_dependientes`, `ct_ingreso_ganado` |
| D3 Crédito denegado o ajustado | Dependientes (0, 1, 2, 3 o más) + Total | `planillas_ajustadas`, `ct_reclamado`, `credito_concedido`, `ajuste` (reclamado − concedido) | Planillas con `ct_ajustado` = 1; requiere `ct_reclamado`, `ct_ajustado` |
| E Exención para jóvenes | Edad simple 16 a 26 + Total | `planillas`, `exento_jovenes`, `salarios`, `industria_negocio`, `contribucion_determinada` (línea 26) | Planillas con `exento_jovenes` > 0 y edad 16–26 |
| F Umbral de $100,000 | Ingreso bruto (según la Sección 1021.01(c)) en tramos de $2,000 entre $90,000 y $110,000 + Total | `planillas`, `planillas_92`, `contribucion_regular_92`, `planillas_95`, `contribucion_regular_95` | Planillas con ingreso bruto entre $90,000 y $110,000; requiere `factor`, `ingreso_bruto_factor` |
| G1 Ajuste gradual | Estado personal + Total | `planillas`, `ingreso_neto`, `ajuste_gradual` | Planillas con ingreso neto > $500,000; requiere `ajuste_gradual` |
| G2 Contribución básica alterna | Ingreso neto sujeto a CBA: hasta $50,000; 50,001–75,000; 75,001–150,000; 150,001–250,000; 250,001 o más + Total | `planillas`, `cba_ingreso_neto`, `cba_contribucion`, `exceso_cba` | Planillas con CBA > 0; requiere `cba_ingreso_neto`, `cba_contribucion` |
| H Dependientes | Estado personal × dependientes reclamados (0, 1, 2, 3, 4 o más) + totales | `planillas`, `exencion_dependientes`, `credito_trabajo`, `creditos_federales` | Todas las planillas |
| I Comprobantes W-2PR | Tramos de salarios de $2,500 hasta $50,000 y después los tramos 9 a 15 de IBA + Total | `comprobantes`, `personas_distintas`, `salarios`, `retenida`, `exento_135` | Archivo W-2PR |
| I_edad | Grupo de edad (16–25, 26–35, 36–50, 51–64, 65 o más) × los mismos tramos + totales | Las mismas | Archivo W-2PR con `edad` |
| J Municipio | Municipio de residencia (78), ordenados por número de planillas, + Total | `planillas`, `iba`, `contribucion_determinada`, `planillas_credito_trabajo`, `credito_trabajo` | Requiere `municipio`; el colapso une cada municipio pequeño con el siguiente de menor población |

## 6. Formato de salida

Un archivo CSV por tabla (`tabla_0_control.csv`, `tabla_A.csv` … `tabla_J.csv`): UTF-8, separador coma, una fila de encabezado, sin celdas combinadas, cantidades en dólares sin decimales ni separadores de miles, celda vacía donde hay supresión. El libro `tabulaciones_482_<anio>.xlsx` repite las mismas tablas (una hoja por tabla, título en la fila 1, encabezado en la fila 3, filas colapsadas en amarillo y vaciadas en gris) y añade las hojas «Léame» (fuente, fecha de corte, versión, modalidad de supresión, columnas no disponibles) y «Diccionario».

## 7. El registro de ejecución

`log_ejecucion_pe.txt`: versión del programa y de Python, pandas, numpy y openpyxl; sistema operativo; fecha y hora de inicio y fin; parámetros; filas leídas y columnas presentes; avisos de columnas ausentes; por tabla, filas producidas, filas colapsadas, filas vaciadas, filas vaciadas para proteger otras, conteos parciales vaciados y celdas vaciadas para proteger otras; tiempo por tabla.

## 8. Ejecución y prueba

Los pasos, comandos y archivos están en la Guía de ejecución y en la Hoja de ruta. Las salidas de referencia de `05_salidas_de_referencia` (modalidad colapsar; `modalidad_vaciar` para la otra) se obtuvieron con los datos ficticios de `03_datos_de_prueba` y permiten comprobar que el programa se ejecuta igual en los sistemas de Hacienda (`comparar_salidas.py`).

## 9. Contacto

Daniel Santamaría Ots — Espacios Abiertos — daniel@espaciosabiertos.org
