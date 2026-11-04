# Descripción conceptual — proyecto policyengine-pr y las tabulaciones solicitadas a Hacienda

Versión 2026-11-04 (rev. 1 del paquete PE). Espacios Abiertos. Para el equipo de análisis económico y de política contributiva del Departamento de Hacienda: qué es el modelo, qué mide cada tabla que se solicita y por qué, y qué protege la regla de supresión.

## 1. El proyecto en breve

policyengine-pr es un modelo de microsimulación de código abierto del sistema contributivo de individuos de Puerto Rico, construido sobre la plataforma PolicyEngine (la misma arquitectura que usan los modelos públicos de Estados Unidos, el Reino Unido y Canadá). Codifica, regla por regla y con cita al Código de Rentas Internas de 2011 y a los formularios e instrucciones de Hacienda, el cómputo de la contribución sobre ingresos de un hogar: ingreso bruto ajustado, deducciones, exenciones, tabla contributiva, ajuste gradual, factor del 92 %/95 %, contribución básica alterna, Crédito por Trabajo y crédito federal adicional por hijos. Con él, cualquier persona puede calcular la contribución de un hogar y comparar la ley vigente con una propuesta de reforma; y Espacios Abiertos puede estimar, para una reforma, su costo de recaudo y su efecto por nivel de ingreso en pocos días.

Para estimar el recaudo, el modelo aplica esas reglas a una base de datos que representa a todos los hogares de Puerto Rico: la Encuesta sobre la Comunidad de Puerto Rico (PRCS) del Negociado del Censo. La encuesta tiene la estructura de los hogares (edades, relaciones, empleo) pero mide los ingresos con error y no contiene las partidas de la planilla (deducciones, créditos, planillas rendidas). Por eso hay que **calibrarla**: ajustar los pesos y las partidas de la encuesta para que el modelo reproduzca los totales administrativos reales de las planillas, por tramo de ingreso, estado personal y número de dependientes. Las tabulaciones que se solicitan son esos totales.

## 2. Qué es la calibración y qué necesita

La calibración es el procedimiento habitual de los modelos de microsimulación (TAXSIM, el modelo del Joint Committee on Taxation, EUROMOD, PolicyEngine): se parte de una encuesta y se reponderan sus hogares para que las sumas simuladas coincidan con los agregados administrativos conocidos. Cuanto más detallados son esos agregados —por tramo de ingreso, por tipo de planilla, por partida— más fiel es el modelo en la parte de la distribución que importa para cada reforma.

Las reglas del Código producen cambios de régimen en puntos concretos de la distribución, y es ahí donde la calibración necesita detalle: los puntos de quiebre de la tabla contributiva ($9,000, $25,000, $41,500 y $61,500 de ingreso neto), los umbrales de reducción y los límites del Crédito por Trabajo, el umbral de $100,000 de ingreso bruto del factor del 92 %, los $500,000 de ingreso neto del ajuste gradual y los tramos de la contribución básica alterna. Los tramos de ingreso bruto ajustado de las tablas se eligieron para reflejar esos puntos: finos donde se concentran los contribuyentes y amplios en la parte alta, donde las planillas son pocas.

## 3. Qué mide cada tabla y para qué sirve

| Tabla | Qué mide | Para qué la usa el modelo |
|---|---|---|
| 0 Control | Totales del archivo de entrada | Cuadrar el archivo con los totales oficiales y comprobar que ninguna planilla se perdió |
| A Resumen por tramo de IBA y estado personal | Planillas, cada partida de ingreso, deducciones, exenciones, ingreso neto, contribución y créditos, por tramo y estado personal | Es la tabla de calibración principal: fija el número de planillas y los totales de cada línea en cada tramo y estado personal |
| B Deducciones del Anejo A | Planillas que reclaman y cantidad de cada deducción, por tramo | Imputar a la encuesta quién deduce y cuánto; valorar reformas de las deducciones |
| C Ingresos exentos del Anejo IE | Exención de pensiones, exención de jóvenes, salarios de difícil reclutamiento, por tramo | Reproducir el ingreso exento, que la encuesta no distingue del ingreso tributable |
| D Crédito por Trabajo | Planillas y cantidad por dependientes y estado personal (D1); por tramo de ingreso ganado de $2,500 (D2); créditos ajustados (D3) | Verificar que el modelo reproduce la fase de aumento, la meseta y la fase de reducción del crédito, y el nivel de reclamación y de ajuste |
| E Exención para jóvenes | Por edad simple de 16 a 26 años | Calibrar la exención de la Ley 135-2014, que cambia la contribución y el Crédito por Trabajo de los jóvenes |
| F Umbral de $100,000 | Planillas al 92 % y al 95 % en tramos de $2,000 alrededor del umbral | Medir la concentración de planillas justo por debajo del umbral (respuesta al escalón) |
| G Ajuste gradual y CBA | Planillas de más de $500,000 y su ajuste; planillas con contribución básica alterna por tramo | Calibrar la parte alta de la distribución, donde la encuesta es menos fiable y donde se concentra el recaudo de las tasas marginales altas |
| H Dependientes | Planillas, exención, Crédito por Trabajo y créditos federales por número de dependientes | Ajustar la estructura de los hogares de la encuesta a la de las planillas |
| I Comprobantes W-2PR | Comprobantes, personas y salarios por tramo y edad, rindan o no planilla | Dimensionar a quienes devengan salarios y no rinden planilla: el grupo que una reforma del tramo inferior o del Crédito por Trabajo puede incorporar |
| J Municipio | Planillas, IBA, contribución y Crédito por Trabajo por municipio | Validar la distribución geográfica del modelo (la encuesta se publica por áreas de microdatos, no por municipio) |

## 4. Las reglas que el modelo reproduce

El modelo codifica, con el texto oficial como fuente, las reglas del año contributivo 2025 y mantiene las de los años anteriores donde difieren: la tabla contributiva de la Sección 1021.01(a) (0, 7, 14, 25 y 33 %); la exención personal ($3,500 y $7,000) y por dependientes ($2,500) y la adicional por veterano ($1,500); el ajuste gradual del 5 % sobre el ingreso neto en exceso de $500,000; el factor del 92 % cuando el ingreso bruto no excede $100,000 (desde 2020) y del 95 % en los demás casos; la contribución básica alterna del Anejo O; la exención de pensiones ($11,000 y $15,000); la exención para jóvenes de la Ley 135-2014 (primeros $40,000 de 16 a 26 años); las deducciones del Anejo A con sus límites; el Crédito por Trabajo del Boletín Informativo RI 26-01 en sus cuatro tablas; y el crédito federal adicional por hijos de los residentes de Puerto Rico (Formulario 1040-SS), limitado por las contribuciones al Seguro Social y Medicare. Cada parámetro es una cifra con su cita, de modo que una reforma se simula cambiando el parámetro, no el programa.

## 5. La regla de supresión y por qué colapsar

Hacienda suprime toda fila con menos de diez observaciones. Para que esa regla no destruya los totales que la calibración necesita, el programa **colapsa** la fila pequeña en la contigua en lugar de eliminarla: el total de la columna se conserva, y la información que se pierde es solo la división entre dos tramos vecinos. Además, dentro de cada fila publicada, los conteos parciales entre 1 y 9 (y los que dejarían un complemento entre 1 y 9) se vacían junto con sus sumas, y se evita que una celda vacía pueda deducirse de la fila de totales. El programa también ofrece la modalidad de los paquetes anteriores de Espacios Abiertos (William T. Grant, Arnold Ventures), que vacía la fila y, si hace falta, otras para protegerla; Hacienda elige.

## 6. Lo que no sale de las planillas

Solo salen conteos y sumas por celda, ya protegidos. Ningún archivo de entrada, ninguna fila individual, ningún identificador, ninguna clave seudónima. El programa es de código abierto y Hacienda puede leerlo completo antes de ejecutarlo; el registro de ejecución documenta cada celda suprimida.

## 7. Compromisos de Espacios Abiertos

Los datos se usarán únicamente para calibrar y validar el modelo y para análisis de política pública; los resultados publicados serán agregados y citarán «Departamento de Hacienda, tabulaciones especiales, [año]»; Espacios Abiertos entregará a Hacienda sin costo el modelo completo, su documentación y acceso a la herramienta de cálculo, y compartirá con antelación cualquier informe que use estos datos. Si Hacienda lo prefiere, estos términos pueden recogerse en un memorando de entendimiento o un acuerdo de uso de datos.

## 8. Contacto

Daniel Santamaría Ots — Espacios Abiertos — daniel@espaciosabiertos.org
