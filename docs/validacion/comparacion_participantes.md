# Participantes de PAN, Crédito por Trabajo y Sección 8: modelo frente a cifras publicadas

*policyengine-pr · base PRCS 2023 calibrada · 4 de noviembre de 2026*

Comprobación de la gráfica *Créditos y beneficios por decil* (página
Reformas) contra las cifras oficiales disponibles. Los totales de hogares y
dólares están calibrados y coinciden por construcción; lo que se comprueba
aquí es la composición.

## PAN

| Medida | Modelo | Publicado | Fuente |
|---|---|---|---|
| Hogares | 738,510 | 738,510 (AF2024, promedio mensual) | USDA FNS Keydata, feb. 2025 (calibrado) |
| Beneficios | $2,929 M | $2,929 M | ídem (calibrado) |
| Personas en hogares PAN | 1,964,707 | 1,274,983 | USDA FNS Keydata, feb. 2025 |
| Tamaño medio del hogar PAN | 2.31 | 1.73 (= personas / hogares) | derivado |
| Hogares PAN con alguna persona de 60+ | 59% | — | — |
| Participantes de 60+ | 34% | 24% (2018) | CBPP, *Characteristics of participants in Puerto Rico's NAP* (resumen de búsqueda; página bloqueada a la descarga) |
| Participantes menores de 18 | 17% | — | — |
| Hogares con PAN, deciles 1–2 de ingreso neto | 100% | — | — |

**Actualización (misma fecha, tras crear la entidad `pan_unit`).** Con las
personas de 60+ que no son jefe ni cónyuge como núcleos aparte, y
calibrando a 738,510 *núcleos* con beneficio (no hogares), las personas en
núcleos PAN bajan de 1.96 a 1.72 millones (FNS: 1.27), el tamaño medio del
núcleo queda en 2.33 (FNS: 1.73; un tercio de los núcleos son de una
persona) y la proporción de participantes de 60+
del 34% al 29% (CBPP 2018: 24%). Lo que queda es la participación
incompleta (no todo núcleo elegible solicita) y el supuesto del beneficio
máximo; ambos se resuelven con la Tabla y las características de ADSEF.

**Lectura original.** El modelo trataba a todo el hogar como un solo núcleo de PAN,
por lo que cuenta 1.96 millones de personas donde ADSEF cuenta 1.27
millones: los núcleos reales son más pequeños (1.7 personas) porque dentro
de un hogar pueden convivir varios núcleos y porque no todos los miembros
participan. El beneficio por hogar es correcto en promedio (calibrado),
pero el beneficio por persona queda un 35% por debajo. La proporción de
personas de 60+ (34%) supera el 24% de 2018 de CBPP; parte es el
envejecimiento desde 2018 y parte el mismo efecto de contar a todo el hogar.
Pendiente: la Tabla de ADSEF por núcleo y las características de
participantes (carta a ADSEF, punto 4).

## PAN: comparación con los listados mensuales de ADSEF (añadido 4 nov. 2026)

ADSEF entregó a Espacios Abiertos sus listados de emisiones de septiembre de
2023 a agosto de 2025 por municipio y oficina
(`docs/statutes/pan/adsef_listados/`). Promedio de los doce meses hasta
agosto de 2025 frente al modelo (base calibrada):

| Medida | Modelo | ADSEF (sep. 2024 – ago. 2025) |
|---|---|---|
| Núcleos (casos) con beneficio | 738,510 (calibrado a FNS AF2024) | 730,133 |
| Participantes | 1,721,325 | 1,247,785 |
| Personas por núcleo | 2.33 | 1.71 |
| Beneficio por núcleo al mes | $331 | $335 |
| Participantes de 60+ | 29.4% | 34.3% |
| Participantes menores de 18 | 19.4% | 21.3% |
| Participantes con salarios | 25.7% | 17.3% |
| Participantes con Seguro Social | 25.8% | 36.0% |
| Núcleos sin ningún ingreso | 11% | 20.1% |

**Tras recalibrar con estas cifras (misma fecha).** Los núcleos, los dólares,
los participantes de 60+, con salarios, con Seguro Social y los núcleos sin
ingreso se reproducen exactamente; los participantes totales quedan en 1.78
millones (objetivo 1.25 M, solo comprobación): el número de personas por
núcleo es una propiedad de la estructura de los hogares de la encuesta y de
la regla de pagar el máximo, y forzarlo con los pesos los vuelve extremos.
El 90% de los cocientes de pesos queda entre 0.19 y 3.0; el 2.6% del peso
queda en hogares escalados más de cinco veces.

**Lectura.** El dinero por núcleo cuadra (es el objetivo de calibración).
Lo que no cuadra es la composición: el modelo mete demasiadas personas por
núcleo y demasiados trabajadores, y pocas personas mayores y núcleos sin
ingreso. Son dos defectos del mismo origen: (1) la elegibilidad del modelo
es más amplia que la participación real (toda unidad bajo el límite recibe
el máximo), y la calibración la recorta reponderando hogares en vez de
quitar a los que no participan; (2) muchos núcleos reales son una persona
mayor sola o una familia sin ingresos declarados, que en la encuesta
aparecen dentro de hogares más grandes con trabajadores. Los listados dan
los objetivos para corregirlo: participantes, 60+, con salarios, con Seguro
Social, sin ingreso, y todo ello por municipio.

## PAN: serie anual 2013–2026 del Observatorio Fiscal (añadido 10 nov. 2026)

El panel *Datos del PAN* del Observatorio Fiscal de Espacios Abiertos
(`docs/statutes/pan/observatorio/`) da la serie anual por año fiscal federal
construida con los datos de ADSEF. Confirma los objetivos de calibración
(AFF2025: 1,246,507 participantes y $2,944 M, frente a 1,247,785 y $2,933 M
de los listados mensuales hasta agosto de 2025) y añade la tendencia: los
participantes de 60 años o más pasan del 19.5% en 2013 al 35.0% en 2026, los
que tienen salarios del 8.3% al 18.2%, los que no tienen ingreso del 29.1% al
15.3%, y los participantes por hogar de 2.12 a 1.79. El AFF2026 (1,222,408
participantes, $2,989 M) es el dato a usar cuando el modelo pase a las reglas
de 2026. También trae participantes, hogares, mayores y menores por municipio
y año, útiles para una calibración regional.

## Crédito por Trabajo

| Medida | Modelo | Publicado | Fuente |
|---|---|---|---|
| Hogares con crédito | 700,000 | «cerca de 700,000 familias» (AC2023) | Hacienda, comunicado 26 dic. 2024 (calibrado) |
| Unidades contributivas con crédito | 816,264 | — | — |
| Total | $1,303 M | $1,303 M | ídem (calibrado) |
| Crédito medio por unidad contributiva | $1,596 | $1,861 por «familia» (= 1,303 M / 700 k) | derivado |
| Reclamantes por ingreso ganado: ≤$10k / $10–20k / $20–30k / $30–40k / >$40k | 30% / 31% / 31% / 7% / 1% | — | — |
| Hogares del decil 10 con algún miembro que reclama | 45% | — | — |

**Lectura.** Hacienda cuenta «familias», que en la práctica son planillas;
el modelo calibra a 700,000 *hogares* y produce 816,000 planillas con
crédito, porque muchos hogares contienen a otro adulto (un hijo adulto con
salario bajo) que rinde planilla propia y reclama el crédito. Eso explica
también que el 45% de los hogares del decil más alto tengan algún
reclamante. Dos cosas por resolver cuando lleguen las tablas de Hacienda:
(1) calibrar a planillas en vez de hogares; (2) comprobar si la
distribución por ingreso ganado (un tercio por debajo de $10,000) coincide
con la de Hacienda; Hacienda no publica esa distribución y la petición del
Senado 2026-0070 la ha solicitado.

## Sección 8

Véase `docs/statutes/hud/SOURCES.md` (diagnóstico): ingreso y pago del
inquilino coinciden con HUD ($7,361 vs $7,634; $174 vs $178); el subsidio
total queda en el 65% por el estándar de pago y el tamaño de las unidades.

## Fuentes

- USDA FNS, Program Information Report (Keydata), febrero de 2025, Tabla 2b (`docs/statutes/calibration/`).
- Hacienda, comunicado de prensa de 26 de diciembre de 2024 (`docs/statutes/calibration/`); comunicado de 25 de marzo de 2025 (ciclo 2024: $1,106.8 M pagados a esa fecha, proyección $1,432 M, créditos de $1,745 a $7,563).
- CBPP, *Characteristics of Participants in Puerto Rico's Nutritional Assistance Program* (cbpp.org; la página rechaza descargas automatizadas; cifra de 60+ tomada del resumen de búsqueda, por verificar).
- HUD, Picture of Subsidized Households 2025 (`docs/statutes/hud/psh_2025_pr_vouchers.csv`).
