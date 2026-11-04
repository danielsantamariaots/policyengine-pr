# Solicitud de datos estadísticos al Departamento de Hacienda

*Borrador para Espacios Abiertos · proyecto policyengine-pr · [fecha]*

---

**A:** Departamento de Hacienda de Puerto Rico
Área de Política Contributiva / Oficina de Asuntos Económicos y Financieros

**De:** [Nombre], [cargo], Espacios Abiertos
[dirección · correo electrónico · teléfono]

**Asunto:** Solicitud de tabulaciones estadísticas agregadas de la Planilla de Contribución sobre Ingresos de Individuos (Formulario 482), años contributivos 2021 a 2024, para un modelo público de microsimulación contributiva

## 1. Propósito

Espacios Abiertos desarrolla **policyengine-pr**, un modelo de microsimulación de código abierto del sistema contributivo de individuos de Puerto Rico, construido sobre la plataforma PolicyEngine (la misma arquitectura que utilizan los modelos de Estados Unidos, el Reino Unido y Canadá). El modelo codifica las reglas del Código de Rentas Internas de 2011, según enmendado, a partir de los formularios e instrucciones oficiales de Hacienda, y permite estimar el efecto de propuestas de reforma sobre el recaudo y sobre los hogares por nivel de ingreso.

Para que las estimaciones de recaudo sean confiables, la base de datos de encuesta que utiliza el modelo (la Encuesta sobre la Comunidad de Puerto Rico del Censo) debe **calibrarse** a los totales administrativos reales de las planillas. Con ese fin solicitamos las tabulaciones que se describen a continuación. No solicitamos datos individuales ni información que permita identificar a contribuyente alguno.

## 2. Diseño de las tabulaciones conforme a la regla de supresión

Entendemos que Hacienda aplica una regla de supresión que elimina toda fila con menos de diez (10) observaciones. Las tabulaciones se han diseñado para minimizar las celdas afectadas, y pedimos que, cuando aplique la supresión, se proceda así:

1. **Colapsar en vez de eliminar.** Que la fila con menos de 10 planillas se agregue a la fila contigua (el tramo de ingreso inmediatamente inferior), identificando la fila resultante con el tramo combinado (por ejemplo, "$500,000 o más") en lugar de omitirla. Así se preserva el total de la columna.
2. **Conservar siempre la fila de totales** de cada tabla, aun cuando se hayan suprimido o colapsado filas intermedias.
3. **Indicar las celdas colapsadas** con una marca (por ejemplo, "c") y, si Hacienda aplica supresión complementaria para evitar la deducción de celdas suprimidas, indicarlo igualmente.
4. **Tramos amplios en la parte alta de la distribución**, donde las planillas son pocas, y más finos donde se concentran los contribuyentes.

Los tramos de ingreso bruto ajustado (IBA, línea 5 del Formulario 482) propuestos son:

| # | Tramo de IBA | # | Tramo de IBA |
|---|---|---|---|
| 1 | $0 o menos (incluye negativos) | 9 | $50,001 – $60,000 |
| 2 | $1 – $10,000 | 10 | $60,001 – $75,000 |
| 3 | $10,001 – $15,000 | 11 | $75,001 – $100,000 |
| 4 | $15,001 – $20,000 | 12 | $100,001 – $150,000 |
| 5 | $20,001 – $25,000 | 13 | $150,001 – $250,000 |
| 6 | $25,001 – $30,000 | 14 | $250,001 – $500,000 |
| 7 | $30,001 – $40,000 | 15 | $500,001 o más |
| 8 | $40,001 – $50,000 | | |

Los tramos 2 a 8 siguen los puntos de quiebre de la tabla contributiva ($9,000, $25,000, $41,500, $61,500 de ingreso neto) y de los límites del Crédito por Trabajo, de modo que las tabulaciones reflejen los cambios de régimen que el modelo debe reproducir.

## 3. Tabulaciones solicitadas

Para cada una de las tablas, **un archivo por año contributivo (2021, 2022, 2023 y 2024)**, en formato CSV o Excel, con planillas radicadas hasta la fecha de corte que Hacienda indique (incluyendo prórrogas). Las columnas de "cantidad" son sumas en dólares; las de "planillas" son conteos.

### Tabla A — Resumen por tramo de IBA y estado personal

Filas: 15 tramos de IBA × estado personal (individual; casado que rinde conjunta; casado que rinde separado; cómputo opcional de casados), más totales.

Columnas (planillas y cantidad, según aplique), por línea del Formulario 482 de 2025 o su equivalente en cada año:

| Columna | Línea |
|---|---|
| Número de planillas | — |
| Salarios (W-2PR y W-2 federal) | 1A–1C |
| Intereses y dividendos | 2C, 2D |
| Pensiones y anualidades | 2H |
| Distribuciones de planes de retiro e IRA | 2E, 2F, 2L |
| Ganancia de capital | 2B |
| Participación en entidades conducto | 2K |
| Ingreso de industria o negocio (todos los anejos) | 2P–2T |
| Pensión pagada por divorcio | 4 |
| Ingreso bruto ajustado | 5 |
| Total de deducciones | 6 |
| Exención personal | 7 |
| Exención por dependientes y número de dependientes | 8A–8C |
| Exención adicional por veterano | 9 |
| Ingreso neto sujeto a contribución | 13 |
| Contribución según tabla | 14 |
| Ajuste gradual | 15 |
| Contribución regular antes del crédito, separando planillas al 92% y al 95% | 17 |
| Crédito por contribuciones pagadas a otras jurisdicciones | 18 |
| Exceso de contribución básica alterna | 20 |
| Crédito por contribución básica alterna | 21 |
| Créditos contributivos (Anejo B) | 25 |
| Responsabilidad contributiva | 26 |
| Contribución retenida sobre salarios | 27A |
| Crédito por Trabajo | 27C |
| Créditos reembolsables del Gobierno Federal | 27D |
| Sobrepago / balance pendiente | 29, 31 |

### Tabla B — Deducciones del Anejo A por tramo de IBA

Filas: 15 tramos de IBA. Columnas: planillas y cantidad para intereses hipotecarios (línea 1i), gastos médicos (3), donativos (4), aportaciones a IRA (7b), cuentas de aportación educativa (8b), préstamos estudiantiles (9b) y total (11).

### Tabla C — Ingresos exentos del Anejo IE por tramo de IBA

Filas: 15 tramos de IBA (donde el IBA se calcula antes de la exención). Columnas: planillas y cantidad para la exención de pensiones (Sección 1031.02(a)(13)), la exención para jóvenes de la Ley 135-2014 (línea 31), los salarios exentos de profesionales de difícil reclutamiento (32), y el total de ingresos exentos (45).

### Tabla D — Crédito por Trabajo (Anejo CT)

D.1. Filas: número de dependientes cualificados (0, 1, 2, 3 o más) × estado personal (individual; conjunta). Columnas: planillas que reclaman el crédito, cantidad total del crédito, ingreso bruto ganado total (Anejo CT, Parte II, línea 3).

D.2. Filas: tramos de ingreso bruto ganado en intervalos de $2,500 desde $0 hasta $55,000, × número de dependientes cualificados (0, 1, 2, 3+). Columnas: planillas y cantidad del crédito. Esta tabla permite verificar la forma de la fase de aumento y de reducción del crédito.

D.3. Planillas con Crédito por Trabajo reclamado y denegado o ajustado, por número de dependientes, con la cantidad ajustada.

### Tabla E — Exención para jóvenes (Ley 135-2014)

Filas: edad del contribuyente al cierre del año (16 a 26, un año por fila; colapsar según la regla de supresión). Columnas: planillas que reclaman la exención, cantidad exenta, salarios totales, ingreso de cuenta propia total, contribución determinada.

### Tabla F — Umbral de $100,000 de la Sección 1021.01(c)

Filas: ingreso bruto (según se define para el factor del 92%/95%) en intervalos de $2,000 entre $90,000 y $110,000. Columnas: planillas al 92%, planillas al 95%, contribución regular antes del crédito en cada grupo. Esta tabla permite medir la respuesta de los contribuyentes al cambio de factor.

### Tabla G — Ajuste gradual y contribución básica alterna

G.1. Planillas con ingreso neto sujeto a contribución superior a $500,000: número, ingreso neto total, ajuste gradual total (línea 15), por estado personal.

G.2. Planillas con contribución básica alterna (Anejo O): número, ingreso neto sujeto a contribución básica alterna, contribución básica alterna y exceso sobre la contribución regular, por tramo de ingreso neto sujeto a CBA (hasta $50,000; $50,001–$75,000; $75,001–$150,000; $150,001–$250,000; más de $250,000).

### Tabla H — Dependientes

Filas: número de dependientes reclamados (0, 1, 2, 3, 4 o más) × estado personal. Columnas: planillas, exención por dependientes total, Crédito por Trabajo total, créditos reembolsables federales (27D) total.

### Tabla I — Comprobantes de retención W-2PR (Formulario 499R-2/W-2PR), independientemente de si se radicó planilla

Filas: tramos de salarios de $2,500 hasta $50,000 y luego los tramos 9 a 15 de la Tabla A. Columnas: número de comprobantes, número de personas distintas, salarios totales, contribución retenida total, salarios exentos bajo la Ley 135 (encasillado 16 con código E). Si es posible, una versión adicional por grupo de edad (16–25, 26–35, 36–50, 51–64, 65 o más).

Esta tabla es la única fuente administrativa sobre personas que devengan salarios pero no rinden planilla, un grupo relevante para cualquier reforma dirigida a ingresos bajos.

### Tabla J — Distribución geográfica

Filas: municipio de residencia del contribuyente (78 municipios). Columnas: planillas, IBA total, contribución determinada total, planillas y cantidad del Crédito por Trabajo. Dado el tamaño de los municipios, no anticipamos celdas con menos de 10 planillas; si las hubiera, colapsar con el municipio contiguo de menor población.

## 4. Documentación que acompañe los datos

- Diccionario de datos con la correspondencia entre cada columna y la línea del Formulario 482 (o del anejo) de cada año, dado que la numeración de líneas cambia entre años.
- Fecha de corte de las planillas incluidas y si se incluyen planillas enmendadas.
- Nota sobre la regla de supresión aplicada y, si hubo supresión complementaria, las celdas afectadas.
- Cualquier tabulación publicada previamente por Hacienda con estas variables (por ejemplo, las utilizadas en informes al Legislativo o en la nota de ajuste por inflación del Crédito por Trabajo), para asegurar consistencia.

## 5. Compromisos de Espacios Abiertos

- Los datos se utilizarán únicamente para calibrar y validar el modelo policyengine-pr y para análisis de política pública; no se intentará identificar a persona alguna, lo que en todo caso sería imposible con datos agregados.
- Los resultados que se publiquen serán agregados; las tabulaciones recibidas se citarán como "Departamento de Hacienda, tabulaciones especiales, [año]".
- Espacios Abiertos entregará a Hacienda, sin costo, el modelo completo, su documentación y acceso a la herramienta de cálculo, y compartirá con antelación cualquier informe que utilice estos datos.
- Si Hacienda prefiere, podemos acordar un memorando de entendimiento o un acuerdo de uso de datos con los términos anteriores.

## 6. Contacto

[Nombre, cargo, correo, teléfono]
Para asuntos técnicos de la especificación de las tablas: [nombre del responsable técnico].

Agradecemos su atención y quedamos a su disposición para reunirnos con el personal técnico de Hacienda y ajustar la especificación a los formatos que les resulten más sencillos de producir.

Atentamente,

[firma]

---

## Anexo técnico (para el personal de estadísticas de Hacienda)

**Prioridad si no es posible producir todas las tablas.** En orden: Tabla A (resumen), Tabla D.1 y D.2 (Crédito por Trabajo), Tabla I (W-2PR), Tabla B (deducciones), Tabla E (jóvenes). Las Tablas C, F, G, H y J pueden entregarse en una segunda fase.

**Años.** Si solo es posible un año, 2023 (planillas radicadas en 2024) es el preferido por ser el más reciente con el ciclo de radicación completo.

**Formato.** Un archivo CSV por tabla y año, con una fila de encabezado, sin celdas combinadas, valores monetarios en dólares sin separadores de miles, y las celdas colapsadas marcadas en una columna adicional ("nota").

**Paquete de programas y libro de petición.** Para reducir el trabajo del personal de Hacienda, acompañamos esta solicitud con la carpeta `PE_Hacienda_Python`, con la misma estructura que los paquetes que Espacios Abiertos ha entregado a Hacienda en los proyectos de la Fundación William T. Grant y de Arnold Ventures:

1. Cuatro documentos (`01_documentos/`): la hoja de ruta para el técnico, la guía de ejecución, la especificación de salidas (contrato de datos, reglas de supresión y definición de cada tabla) y la descripción conceptual del modelo.
2. El contrato de datos (`02_contrato_y_parametros/`): el esquema de las 51 columnas del archivo de planillas (14 necesarias; las demás amplían las salidas y, si no están, el programa omite solo lo que depende de ellas) y de las 6 del archivo de comprobantes W-2PR, con la línea del Formulario 482 de cada una; una plantilla de la consulta de extracción con los nombres de tablas y campos entre `< >` para que Hacienda los sustituya; y la ficha de extracción que documenta la correspondencia real usada en cada año.
3. Datos de prueba inventados (`03_datos_de_prueba/`) y cuatro programas en Python (`04_programas/`, solo pandas, numpy y openpyxl): `validar_entrada.py` comprueba el archivo antes de ejecutar; `pe_tabulaciones.py` produce las tablas de la Sección 3, más una tabla de control, aplica la regla de supresión y escribe un CSV por tabla, un libro Excel (una hoja por tabla, más «Léame» y «Diccionario») y un registro de ejecución; `verificar_salidas.py` comprueba las salidas antes de entregarlas; `comparar_salidas.py` confirma que el programa reproduce en los sistemas de Hacienda las salidas de referencia del paquete (`05_salidas_de_referencia/`, obtenidas con los datos de prueba).
4. El libro `Peticion_datos_Hacienda_policyengine-pr.xlsx`, con las peticiones, las columnas de los archivos de entrada, las reglas y una hoja por tabla con la plantilla vacía.

Ningún microdato sale de los programas: solo se escriben sumas y conteos ya protegidos. El programa aplica la regla de supresión en la modalidad que pide esta carta (colapsar las filas con menos de 10 planillas en la contigua, conservando los totales) y ofrece también la modalidad de los paquetes anteriores (vaciar la fila y, si hace falta, otras para protegerla); en ambas vacía además los conteos parciales entre 1 y 9 y evita que una celda vacía se deduzca de los totales. Hacienda puede revisar el código completo antes de ejecutarlo, modificarlo o sustituirlo por su propio proceso siempre que el resultado tenga la misma estructura.

**Definición de IBA para las filas.** Línea 5 del Formulario 482 del año correspondiente. Para la Tabla C, el IBA más los ingresos exentos del Anejo IE, de modo que la exención no mueva al contribuyente de tramo.

**Alternativa de mayor valor.** Si Hacienda contempla producir un archivo de microdatos anonimizado (muestra estratificada con identificadores eliminados, edades en grupos, municipio sustituido por región, ingresos altos acotados), ese archivo sustituiría a todas las tablas anteriores y permitiría al modelo reproducir la distribución completa sin calibración. Espacios Abiertos está disponible para discutir las salvaguardas que Hacienda considere necesarias.
