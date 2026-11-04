# Ensayo 2027 - tramo de 0% a $15,000, tasa del 7% al 5%, Crédito por Trabajo +15%

*Estimación de policyengine-pr · Espacios Abiertos · 04/11/2026 · año contributivo 2025*

## En una línea

La reforma cuesta a Hacienda **$588 M al año** (contribución sobre ingresos $-371 M, Crédito por Trabajo $217 M); **54%** de los hogares salen ganando y **2%** perdiendo; el cambio medio es de **$467** por hogar al año.

## Qué cambia

| Parámetro | Valor |
|---|---|
| Inicio del tramo 2 (7%) | 1.5e+04 |
| Tasa del tramo 2 | 0.05 |
| Exención por dependiente | 3,000 |
| Crédito por Trabajo máximo, sin dependientes | 2,063 |
| Crédito por Trabajo máximo, 1 dependiente | 4,814 |
| Crédito por Trabajo máximo, 2 dependientes | 7,562 |
| Crédito por Trabajo máximo, 3+ dependientes | 8,940 |

## Totales (millones de dólares al año)

| Partida | Ley vigente | Reforma | Cambio |
|---|---|---|---|
| Contribución sobre ingresos de PR | 3,918 | 3,547 | -371 |
| Crédito por Trabajo | 1,303 | 1,520 | +217 |
| Crédito federal por hijos | 308 | 310 | +2 |
| PAN | 2,929 | 2,933 | +4 |
| TANF | 176 | 176 | +0 |
| Sección 8 | 139 | 138 | -1 |
| Ingreso neto de los hogares | 50,775 | 51,371 | +596 |

## Por decil de ingreso neto del hogar

| Decil | Ingreso neto medio | Cambio medio | Ganan | Pierden |
|---|---|---|---|---|
| 1 | $5,770 | $+0 | 0% | 0% |
| 2 | $13,315 | $+11 | 3% | 0% |
| 3 | $19,096 | $+252 | 34% | 0% |
| 4 | $24,171 | $+473 | 59% | 0% |
| 5 | $29,223 | $+400 | 51% | 4% |
| 6 | $35,366 | $+558 | 67% | 3% |
| 7 | $42,387 | $+658 | 70% | 3% |
| 8 | $50,659 | $+718 | 79% | 2% |
| 9 | $63,944 | $+706 | 85% | 3% |
| 10 | $113,388 | $+893 | 95% | 2% |

## Hogares de ejemplo

| Hogar | Contribución (vigente → reforma) | Créditos y beneficios | Ingreso neto (cambio) |
|---|---|---|---|
| Trabajador soltero, salario mínimo ($21,840) | $601 → $154 | $3,584 → $3,853 | $23,868 (+717) |
| Madre con dos hijos, $30,000 | $805 → $253 | $11,606 → $12,592 | $40,044 (+1,538) |
| Pareja con dos hijos, $45,000 + $25,000 | $6,951 → $6,150 | $3,400 → $3,400 | $61,895 (+800) |
| Soltero, $95,000 | $16,864 → $16,293 | $0 → $0 | $71,439 (+570) |

## Supuestos y fuentes

- Reglas del año contributivo 2025 codificadas desde los formularios e instrucciones de Hacienda, el IRS, ADSEF y CMS; cada parámetro cita su fuente (repositorio policyengine-pr).
- Microdatos: Encuesta sobre la Comunidad de Puerto Rico 2023 (PUMS), 1.28 millones de hogares ponderados, con pesos calibrados a los totales oficiales de recaudo (Hacienda, AF2023-24), Crédito por Trabajo (año contributivo 2023) y PAN (USDA FNS, AF2024).
- Unidades contributivas construidas desde la composición del hogar; ingresos de 2023 ajustados a 2025 por el salario medio anual de Puerto Rico (BLS QCEW, ×1.0815). La contribución sobre ingresos se muestra antes del Crédito por Trabajo; el recaudo neto calibrado es la diferencia entre ambas filas.
- Respuesta de comportamiento: elasticidad del ingreso tributable de 0.25 aplicada al cambio en la tasa marginal neta de los salarios.
- PAN con el beneficio máximo para todo hogar elegible (ADSEF no publica la tabla de reducción); TANF con el máximo de una familia de tres para todo tamaño.
- Los niveles están calibrados a totales agregados; los cambios son la cifra principal. Estimaciones, no asesoría profesional.
