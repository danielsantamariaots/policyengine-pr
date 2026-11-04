# Reforma de ejemplo: ampliar el tramo de 0% a $12,000

*Estimación de policyengine-pr · Espacios Abiertos · 04/11/2026 · año contributivo 2025*

## En una línea

La reforma cuesta a Hacienda **$136 M al año** (contribución sobre ingresos $-136 M, Crédito por Trabajo $0 M); **50%** de los hogares salen ganando y **0%** perdiendo; el cambio medio es de **$107** por hogar al año.

## Qué cambia

| Parámetro | Valor |
|---|---|
| Bracket 2 starts (7%) | 1.2e+04 |

## Totales (millones de dólares al año)

| Partida | Ley vigente | Reforma | Cambio |
|---|---|---|---|
| Contribución sobre ingresos de PR | 3,918 | 3,782 | -136 |
| Crédito por Trabajo | 1,303 | 1,303 | +0 |
| Crédito federal por hijos | 305 | 305 | +0 |
| PAN | 2,929 | 2,929 | +0 |
| Ingreso neto de los hogares | 49,784 | 49,921 | +136 |

## Por decil de ingreso neto del hogar

| Decil | Ingreso neto medio | Cambio medio | Ganan | Pierden |
|---|---|---|---|---|
| 1 | $5,395 | $+0 | 0% | 0% |
| 2 | $12,665 | $+0 | 0% | 0% |
| 3 | $18,419 | $+33 | 21% | 0% |
| 4 | $23,630 | $+87 | 48% | 0% |
| 5 | $28,553 | $+81 | 46% | 0% |
| 6 | $34,787 | $+120 | 63% | 0% |
| 7 | $41,692 | $+137 | 68% | 0% |
| 8 | $49,820 | $+165 | 76% | 0% |
| 9 | $62,622 | $+199 | 85% | 0% |
| 10 | $112,088 | $+245 | 96% | 0% |

## Hogares de ejemplo

| Hogar | Contribución (vigente → reforma) | Créditos y beneficios | Ingreso neto (cambio) |
|---|---|---|---|
| Trabajador soltero, salario mínimo ($21,840) | $601 → $408 | $3,584 → $3,584 | $23,344 (+193) |
| Madre con dos hijos, $30,000 | $805 → $612 | $11,606 → $11,606 | $38,699 (+193) |
| Pareja con dos hijos, $45,000 + $25,000 | $6,951 → $6,757 | $3,400 → $3,400 | $61,288 (+193) |
| Soltero, $95,000 | $16,864 → $16,670 | $0 → $0 | $71,062 (+193) |

## Supuestos y fuentes

- Reglas del año contributivo 2025 codificadas desde los formularios e instrucciones de Hacienda, el IRS, ADSEF y CMS; cada parámetro cita su fuente (repositorio policyengine-pr).
- Microdatos: Encuesta sobre la Comunidad de Puerto Rico 2023 (PUMS), 1.28 millones de hogares ponderados, con pesos calibrados a los totales oficiales de recaudo (Hacienda, AF2023-24), Crédito por Trabajo (año contributivo 2023) y PAN (USDA FNS, AF2024).
- Unidades contributivas construidas desde la composición del hogar; ingresos de 2023 sin ajustar a 2025.
- Respuesta de comportamiento: ninguna (modelo estático).
- PAN con el beneficio máximo para todo hogar elegible (ADSEF no publica la tabla de reducción); TANF con el máximo de una familia de tres para todo tamaño.
- Los niveles están calibrados a totales agregados; los cambios son la cifra principal. Estimaciones, no asesoría profesional.
