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

**Lectura.** El modelo trata a todo el hogar como un solo núcleo de PAN,
por lo que cuenta 1.96 millones de personas donde ADSEF cuenta 1.27
millones: los núcleos reales son más pequeños (1.7 personas) porque dentro
de un hogar pueden convivir varios núcleos y porque no todos los miembros
participan. El beneficio por hogar es correcto en promedio (calibrado),
pero el beneficio por persona queda un 35% por debajo. La proporción de
personas de 60+ (34%) supera el 24% de 2018 de CBPP; parte es el
envejecimiento desde 2018 y parte el mismo efecto de contar a todo el hogar.
Pendiente: la Tabla de ADSEF por núcleo y las características de
participantes (carta a ADSEF, punto 4).

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
