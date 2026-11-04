# Peticiones de información pendientes para completar la plataforma

*policyengine-pr · Espacios Abiertos · 4 de noviembre de 2026*

Lo que la plataforma ya hace no depende de nadie: las reglas salen de documentos públicos y las pruebas se calculan a mano. Lo que falta para pasar de prototipo a herramienta que podamos defender en público depende de datos que solo tienen cuatro agencias, de una comprobación profesional y de dos decisiones nuestras. Este documento reúne todo en una lista, en el orden en que conviene pedirlo. Las cuatro cartas ya están redactadas (`docs/solicitud_datos_*.docx`); aquí se resume qué se pide, para qué sirve y qué cambia en la plataforma cuando llegue.

## Resumen

| A quién | Qué | Para qué | Urgencia |
|---|---|---|---|
| Hacienda | Tabulaciones de las planillas 2023 y 2024 por tramo de ingreso (diez tablas) | Calibrar el modelo por tramo, no solo a totales; validar la contribución y el Crédito por Trabajo | **Máxima**: es el plazo más largo y condiciona la calibración final |
| ADSEF | Tabla de Beneficios del PAN, límites vigentes, deducciones, estándar de necesidad del TANF | Cerrar la laguna más grande del modelo (el PAN paga el máximo a todos) | Alta |
| Departamento de Salud / ASES | Tablas de elegibilidad del Plan Vital 2025 y manual | Elegibilidad exacta de 2025 (hoy se usa la tabla de 2026) | Media |
| Vivienda / AVP | Estándares de pago, utilidades, estadísticas por región | Subsidio de Sección 8 real (hoy el modelo da el 65% del total de HUD) | Media |
| IRS (público) | Totales del crédito adicional por hijos pagados a Puerto Rico | Calibrar el crédito federal por hijos y medir el *take-up* | Media (se puede buscar sin carta) |
| CPA | 10–15 planillas reales anonimizadas de 2025 | Poder decir «comprobado con planillas reales» | Alta: necesita semanas de aviso |
| Espacios Abiertos | Nombre del producto y dominio; cinco sesiones de prueba con usuarios | Lanzar con marca propia y con los problemas de uso corregidos | Alta: antes de compartir en público |

## 1. Hacienda (Departamento de Hacienda, Área de Planificación / Estadísticas)

**Qué se pide.** Tabulaciones agregadas de las planillas de individuos de los años contributivos 2023 y 2024, por tramo de ingreso bruto ajustado y estado personal, con la regla de supresión de Hacienda (colapsar filas con menos de 10 planillas, conservar totales). Diez tablas:

- A. Resumen por tramo de IBA y estado personal: planillas, ingreso bruto, deducciones, exenciones, ingreso neto sujeto, contribución determinada, créditos, contribución neta.
- B. Deducciones del Anejo A por tramo (hipoteca, médicos, donativos, IRA, educación, préstamos).
- C. Ingresos exentos del Anejo IE por tramo (pensiones, Seguro Social, intereses).
- D. Crédito por Trabajo (Anejo CT): planillas y monto por número de dependientes, estado personal y tramo de ingreso ganado.
- E. Exención para jóvenes (Ley 135-2014): planillas y monto por tramo.
- F. Planillas a uno y otro lado del umbral de $100,000 de la Sección 1021.01(c).
- G. Ajuste gradual y contribución básica alterna: planillas y montos.
- H. Dependientes: distribución de planillas por número de dependientes y tramo.
- I. Comprobantes W-2PR por tramo de salario, rindan o no planilla (para medir quién no rinde).
- J. Distribución por municipio.

Además: diccionario de datos, fecha de corte, nota de supresión, y las tabulaciones ya publicadas en informes al Legislativo. Las cifras de la **línea 27D** (crédito federal por hijos reclamado a través de la planilla) salen de la Tabla A.

**Qué cambia cuando llegue.** La calibración pasa de siete totales a objetivos por tramo de ingreso; el Crédito por Trabajo se calibra a planillas y no a hogares; la distribución por decil de la página *Reforma contributiva* deja de depender de la construcción de unidades contributivas desde la encuesta; y cada estimación de reforma puede acompañarse de «coincide con Hacienda en X».

## 2. ADSEF (Administración de Desarrollo Socioeconómico de la Familia)

**PAN.**
1. La **Tabla de Beneficios** vigente (artículo 5, def. 69, y artículo 51.A del Reglamento 8684): beneficio mensual por tamaño del núcleo y tramo de ingreso neto. Es la laguna más importante del modelo: sin ella, todo núcleo elegible recibe el máximo y el precipicio al superar el límite es en parte un artefacto.
2. Límites de ingreso neto máximo y beneficios máximos por tamaño del núcleo (1 a 18+), con fecha; solo conocemos los de octubre de 2021 y el ajuste de 2024 para una persona.
3. Plan Estatal de Operaciones del NAP de los años fiscales 2025 y 2026 (o su sección VII).
4. Cantidades vigentes de las deducciones del artículo 45 (cuido, incapacidad, estudiante, gastos médicos, enfermedad terminal, agricultura).
5. Beneficio máximo de Vieques y Culebra y bono de edad avanzada vigentes.
6. La enmienda de 2024 al Reglamento 8684 (recursos, 50% de pensiones y Seguro Social, exención por nuevo empleo).
7. ~~Características de los participantes~~ **Ya recibido**: los listados mensuales de ADSEF (sep. 2023 – ago. 2025, por municipio) dan núcleos, participantes, edades, fuente de ingreso y beneficio emitido. Sirven para calibrar y validar; no sustituyen la Tabla de Beneficios ni los límites (puntos 1 a 6).

**TANF.**
8. La tabla de necesidades básicas (estándar de necesidad y de pago) de la categoría C por tamaño de la unidad (secciones 4.16 y 4.22 del Reglamento 7653); solo conocemos el valor para tres personas.
9. El nuevo reglamento del TANF, si ya fue aprobado, y las deducciones y beneficios vigentes de todas las categorías.

**Qué cambia cuando llegue.** El PAN se reduce con el ingreso como en la realidad, el precipicio del PAN se dibuja donde está de verdad, el TANF usa el tamaño de familia correcto, y los totales de personas y beneficios cuadran con FNS.

## 3. Departamento de Salud / ASES (Plan Vital)

1. Tablas de elegibilidad por ingresos vigentes y de los dos años anteriores (en particular del 1 de abril de 2025 al 31 de marzo de 2026), por grupo y tamaño del hogar.
2. Manual de Elegibilidad del Programa Medicaid (ingreso contable, deducciones, recursos).
3. Definición de la unidad familiar y regla de los menores de 19 entre Medicaid y CHIP.
4. Estadísticas de inscripción por grupo y región.

**Qué cambia cuando llegue.** La elegibilidad de 2025 deja de apoyarse en la tabla de 2026, y se puede dar un valor en dólares al Plan Vital (el costo per cápita por grupo) en lugar de solo «elegible o no».

## 4. Departamento de la Vivienda / Administración de Vivienda Pública (Sección 8)

1. Esquema de estándares de pago vigente por dormitorios y área (el Plan Administrativo solo da la banda del 90% al 110% de la renta justa de mercado).
2. Esquema de asignaciones por utilidades.
3. Fecha de implantación de las deducciones de HOTMA ($525 por familia de edad avanzada; el plan de junio de 2025 aún dice $400) y umbrales de las deducciones médicas, de incapacidad y de cuido.
4. Estadísticas por oficina regional o área: vales en uso, pago promedio, ingreso promedio, fuente principal de ingreso.
5. Límites de ingreso para admisión por área, si difieren de HUD.
6. Práctica de asignación de dormitorios: el modelo asigna 9% de vales de 3 o más dormitorios; HUD informa 47%.

**Qué cambia cuando llegue.** El subsidio modelado (hoy el 65% del total de HUD) pasa a cuadrar, y la Sección 8 puede entrar con peso propio en las estimaciones de reforma.

## 5. IRS y Tesoro federal (sin carta: información pública por localizar)

1. Totales del **crédito adicional por hijos** pagados a residentes de Puerto Rico (Formulario 1040-SS) por año contributivo, en las tablas de *Statistics of Income* o en el *IRS Data Book* (fila de Puerto Rico), para calibrar el crédito y medir el *take-up*. El modelo estima $307 millones de derecho; sin el total pagado no sabemos cuánto se reclama.
2. Confirmación de las cantidades de 2025 del crédito tras la ley federal de 2025 ($2,200 por hijo, $1,700 reembolsable), ya reflejadas en el Formulario 1040-SS que usamos.

## 6. Comprobación profesional (CPA)

- Entre 10 y 15 planillas reales de 2025, anonimizadas, con sus anejos, de hogares variados (asalariado soltero, pareja con hijos, cuenta propia, pensionado, con Crédito por Trabajo, con ingresos a tasas preferenciales).
- Un CPA que las recalcule con la plataforma y documente las diferencias en el cuaderno ya preparado (`docs/validacion/casos_validacion_2025.xlsx`).
- Con el resultado, el pie de cada página dirá «Comprobado contra N planillas reales de 2025 revisadas por un CPA».

## 7. Decisiones y trabajo nuestro

- **Nombre del producto y dominio**: antes de que se comparta en público; hoy es «policyengine-pr» y una dirección de streamlit.app.
- **Cinco sesiones de prueba con usuarios** (trabajador social, periodista, asesor legislativo, madre o padre con salario bajo, persona pensionada), con el guion ya preparado (`docs/pruebas_usuarios/guion.md`); las tres confusiones más frecuentes marcan el trabajo de la semana siguiente.
- **Revisión de copia** por una persona de Puerto Rico de todos los textos de la plataforma.
- **Reseñadores** para la beta privada de marzo de 2027: un contador, alguien del personal legislativo y un periodista que cubra Hacienda.

## Orden recomendado

1. Enviar la carta a Hacienda esta semana (plazo más largo).
2. Enviar ADSEF, Salud y Vivienda la misma semana; pedir reunión con ADSEF y con la oficina de Sección 8.
3. Contratar al CPA y reunir las planillas (noviembre–diciembre).
4. Decidir nombre y dominio; hacer las cinco sesiones de prueba (noviembre).
5. Localizar los totales del IRS (lo hace el equipo técnico, sin carta).
