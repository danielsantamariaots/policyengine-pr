# Cómo funciona este modelo

*policyengine-pr · Espacios Abiertos · versión 2026.11.04*

Esta página explica, sin tecnicismos, qué calcula la herramienta, de dónde
salen sus reglas y sus datos, y qué no debe pedírsele. La versión técnica
está en el repositorio (`ROADMAP.md`, `docs/statutes/`, `CONTRIBUTING.md`).

## 1. Qué calcula para un hogar

Para el hogar que usted describe, el modelo sigue el orden de la planilla
de 2025 (Formulario 482): suma los ingresos, resta deducciones y
exenciones, aplica la tabla de tasas, rebaja el resultado al 92% o 95% como
manda la ley, compara con la contribución básica alterna y resta los
créditos. A eso añade lo que la planilla no incluye pero el hogar sí
recibe o paga: el Seguro Social y Medicare retenidos, el Crédito por
Trabajo, el crédito federal por hijos (ACTC), el PAN, el TANF y la Sección
8, y comprueba la elegibilidad al Plan Vital. El resultado es el ingreso
neto: lo que queda después de contribuciones y ayudas.

Cada regla está escrita a partir de un documento oficial (las instrucciones
de la planilla, el Código de Rentas Internas, los reglamentos de ADSEF, los
boletines de Hacienda, las guías del IRS, las tablas de HUD y el plan
administrativo de Vivienda). El archivo de cada parámetro cita el documento
y la página; las fuentes están en `docs/statutes/`.

## 2. Qué calcula para una reforma contributiva

Una reforma es un conjunto de cambios en parámetros (un tramo, una tasa,
una exención, un máximo del Crédito por Trabajo). El modelo recalcula a
cada hogar de una muestra representativa de Puerto Rico con la ley vigente
y con la reforma, y suma: cuánto recauda Hacienda de más o de menos,
cuántos hogares ganan y pierden, y cuánto cambia el ingreso neto por decil
de ingreso.

La muestra es la Encuesta sobre la Comunidad de Puerto Rico de 2023 (los
microdatos públicos del Censo, unos 12,000 hogares que representan 1.28
millones). Los ingresos de 2023 se llevan a 2025 con el crecimiento del
salario medio (BLS). Como la encuesta no pregunta quién rinde planilla ni
quién recibe cada ayuda, el modelo lo construye: las planillas a partir de
quién vive con quién; los núcleos del PAN según las reglas de ADSEF; los
vales de Sección 8 se asignan al azar entre los hogares arrendatarios de
ingreso muy bajo hasta igualar las cifras de HUD.

Después, los pesos de la encuesta se ajustan para que la muestra reproduzca
trece totales oficiales: hogares y personas, recaudo neto de la contribución
de individuos (Hacienda, año fiscal 2024), total y número de familias con
Crédito por Trabajo (Hacienda, año contributivo 2023), núcleos y dólares
del PAN y su composición (participantes de 60+, con salarios, con Seguro
Social y núcleos sin ingreso, de los listados mensuales de ADSEF hasta
agosto de 2025) y vales de Sección 8 en uso (HUD, 2025).
La tabla *Calibración a totales oficiales* de la página Reforma
contributiva muestra cada uno, antes y después del ajuste.

## 3. Qué fiabilidad tiene

- **Para un hogar concreto**, las reglas de la contribución y de los
  créditos son las de los formularios oficiales, y se comprueban con casos
  calculados a mano (más de cien pruebas automáticas). Está en marcha una
  comprobación con planillas reales de 2025 revisadas por un CPA.
- **Para las ayudas**, hay tres lagunas que la propia herramienta declara:
  ADSEF no publica la tabla que reduce el PAN con el ingreso, de modo que
  el modelo paga el máximo a todo núcleo elegible; el TANF usa el máximo de
  una familia de tres para todo tamaño; la Sección 8 usa las rentas justas
  de mercado de HUD del municipio, no el esquema en dólares de Vivienda.
- **Para una reforma**, los totales están calibrados a las cifras
  oficiales; los *cambios* son la cifra fiable, los niveles menos. El
  modelo es estático salvo que se active la respuesta de comportamiento
  (elasticidad del ingreso tributable), y no proyecta años futuros.
- **Lo que no modela**: las columnas de 4% y 20% del Anejo A2, el arrastre
  de pérdidas de capital, los créditos por inversión del Anejo B, las
  categorías del TANF distintas de la C, y cualquier regla que no sea un
  parámetro (un crédito nuevo exige programarlo).

## 4. Qué datos usa de usted

Ninguno. Lo que escribe en el formulario se usa para el cálculo y no se
guarda; el enlace *Compartir* lleva los datos del hogar en la propia
dirección, que solo ve quien la recibe.

## 5. Quién lo hace y cómo corregirlo

Lo desarrolla Espacios Abiertos sobre la plataforma PolicyEngine, con
código y fuentes abiertos (licencia AGPL-3.0). Cada cambio queda registrado
con su fecha; la versión del modelo aparece al pie de cada página. Un error
o una duda se reporta en
https://github.com/danielsantamariaots/policyengine-pr/issues/new.
