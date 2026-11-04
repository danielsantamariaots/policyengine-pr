# Cómo está construido policyengine-pr

*Nota técnica para científicos de datos y economistas · Espacios Abiertos · versión 2026.11.04*

Repositorio: https://github.com/danielsantamariaots/policyengine-pr (AGPL-3.0). Aplicación: https://policyengine-pr.streamlit.app.

## 1. En una página

policyengine-pr es un modelo de microsimulación de contribuciones y beneficios de Puerto Rico construido sobre **policyengine-core**, el motor de código abierto de PolicyEngine (el mismo que usan sus modelos de Estados Unidos, Reino Unido y Canadá). El modelo separa tres cosas: las **reglas** (variables y parámetros, una por archivo, con su fuente), los **datos** (una base de hogares representativa construida desde los microdatos públicos del Censo y recalibrada a totales administrativos) y las **aplicaciones** (una app web, un generador de informes y una API de puntuación de reformas). Cualquier cantidad que una reforma pudiera cambiar es un parámetro con fecha, no un número dentro de una fórmula; por eso una reforma se escribe como un archivo YAML de pocas líneas y se puntúa en décimas de segundo.

| Componente | Dónde | Tamaño (nov. 2026) |
|---|---|---|
| Variables (fórmulas) | `policyengine_pr/variables/` | 142 archivos Python |
| Parámetros (cantidades de la ley) | `policyengine_pr/parameters/` | 94 archivos YAML |
| Pruebas | `policyengine_pr/tests/` | 109 pruebas (YAML calculadas a mano + Python) |
| Datos | `policyengine_pr/data/` + `data/` | PRCS 2023 → 12,264 hogares, 1.28 M ponderados |
| App | `app/` | Streamlit, 5 páginas, ES/EN |
| Fuentes oficiales | `docs/statutes/` | un `SOURCES.md` por programa |

## 2. El motor: entidades, variables, parámetros

**Entidades.** Persona, hogar (`household`), unidad contributiva (`tax_unit`, la planilla) y núcleo de servicio del PAN (`pan_unit`). Una persona pertenece a una de cada; las variables se definen en la entidad a la que la ley se refiere (la contribución en la planilla, el PAN en el núcleo, la Sección 8 en el hogar) y se agregan o proyectan entre entidades con las primitivas de policyengine-core (`add`, `members`, `map_to`).

**Variables.** Un archivo por variable, con `entity`, `definition_period` (año), `unit`, `documentation` (la línea del formulario o el artículo) y una `formula` vectorizada con NumPy, o `adds`/`subtracts` cuando es una suma. Ejemplo: `pr_income_tax` encadena ingreso bruto ajustado → deducciones y exenciones → ingreso neto sujeto → tabla de tasas → factor 92%/95% → contribución básica alterna → créditos. El árbol de variables sigue la estructura del Código de Rentas Internas de 2011 (`gov/hacienda/...`) y de cada programa (`gov/irs`, `gov/adsef/pan`, `gov/adsef/tanf`, `gov/salud/vital`, `gov/hud/section8`).

**Parámetros.** Un YAML por cantidad, con valores fechados (`2025-01-01: 9000`), `metadata.reference` con título y URL del documento oficial (y página cuando aplica) y un campo `gap` cuando el valor es un supuesto o una laguna. Los tramos de la tabla de tasas son un `brackets`; las tablas por tamaño de hogar o por área son nodos anidados indexables con vectores (`p.income_limit.very_low[area][size]`). Nada se escribe de memoria: si el texto oficial no está en `docs/statutes/`, la regla no entra.

**Reformas.** `policyengine_pr/reforms/parametric.py` define palancas (rutas de parámetros con etiqueta y tipo) y construye una `Reform` que fija nuevos valores desde una fecha. `reforms/*.yaml` son reformas completas (nombre, descripción, fuente, palancas con valores absolutos o relativos como `+20%`); `reforms/files.py` las carga y resuelve. La app, el informe y la API leen el mismo archivo.

## 3. Lo que está modelado y con qué fuente

| Programa | Fuente principal | Lo que cubre | Lagunas declaradas |
|---|---|---|---|
| Contribución sobre ingresos 2025 | Instrucciones y formularios de la planilla 2025 (Formulario 482 y anejos), Código de Rentas Internas (Ley 1-2011) | Ingreso bruto, deducciones del Anejo A, exenciones, tabla de tasas, ajuste gradual, factor 92/95%, contribución básica alterna, tasas preferenciales del Anejo A2 (10% intereses, 15% dividendos y ganancias de capital con la prorrata de la Sec. 1033.20), exención para jóvenes (Ley 135-2014), regla de quién rinde | Columnas de 4% y 20% del Anejo A2, arrastre de pérdidas, créditos del Anejo B |
| Crédito por Trabajo | Sección 1052.01; Boletín Informativo RI 24-04 y 26-01 (ajuste por inflación) | Máximos, fases de aumento y reducción por número de dependientes y estado civil | — |
| Crédito federal adicional por hijos | Formulario 1040-SS 2025, Parte II, e instrucciones | $1,700 por hijo, eliminación gradual, tope por Seguro Social y Medicare pagados | MAGI solo con salarios |
| Seguro Social y Medicare | IRS Tema 751; Schedule SE | Retenciones del empleado y contribución por cuenta propia | — |
| PAN | Reglamento 8684 (2015); Plan Estatal NAP FY2022; ponencia ADSEF 2024 | Núcleos de servicio, ingreso contable (50% de pensiones y Seguro Social), deducciones (ingreso ganado, estándar, edad avanzada, estudiante, cuido, médica), límites por tamaño, beneficio máximo, bono por edad, prueba de recursos | Tabla de reducción del beneficio con el ingreso (no publicada: se paga el máximo); límites de 2021 para núcleos de 2+ |
| TANF | Reglamento 7653; Welfare Rules Database 2023 | Categoría C, deducción de $90, mínimo de $10 | Máximo de familia de tres para todo tamaño |
| Plan Vital | Tabla CMS abril 2026 | Elegibilidad Medicaid/CHIP por MAGI | Sin valor en dólares |
| Sección 8 | 24 CFR partes 5 y 982; tablas HUD FY2025 por área; Plan Administrativo PRPHA 2025 | Ingreso anual y ajustado (HOTMA), pago del inquilino, estándar de ocupación, subsidio por área de HUD (15 áreas) | Esquema de estándares de pago en dólares; asignaciones por utilidades |

Cada tabla de `SOURCES.md` enlaza el PDF guardado y la página leída.

## 4. Los datos

**Fuente.** Microdatos públicos (PUMS) de la Encuesta sobre la Comunidad de Puerto Rico 2023, archivos de personas y viviendas (`data/raw/pums_2023/`, no versionados). `policyengine_pr/data/prcs.py` construye `data/prcs_2023.h5`:

1. Viviendas ocupadas con al menos una persona; se descartan las viviendas colectivas.
2. **Unidades contributivas** desde la relación con el jefe (RELSHIPP): jefe y cónyuge rinden conjunta; sus hijos menores de 21 (o de 26 si estudian) y cualquier menor de 18 son dependientes; cada otro adulto rinde planilla individual; las parejas no casadas rinden por separado.
3. **Núcleos del PAN**: todo el hogar, salvo que cada persona de 60+ que no sea jefe ni cónyuge forma su propio núcleo (Reglamento 8684).
4. **Ingresos** (salarios, cuenta propia, pensiones, Seguro Social, intereses) multiplicados por ADJINC y **llevados de 2023 a 2025** con el crecimiento del salario medio anual de Puerto Rico (BLS QCEW, ×1.0815).
5. **Área de HUD** de cada hogar desde su PUMA (mayoría de municipios); **vale de Sección 8** imputado al azar entre hogares arrendatarios dentro del límite de ingreso muy bajo, por estratos (60+, ingreso extremadamente bajo) hasta igualar las cifras de HUD.
6. Los identificadores y pesos de cada entidad se guardan en el formato de arrays de policyengine-core.

**Calibración.** `policyengine_pr/data/calibration.py` reponderá los hogares por **mínima entropía relativa** (ajuste iterativo tipo raking sobre pesos continuos) para reproducir exactamente doce totales administrativos definidos en `calibration_targets.yaml`: hogares y personas (PRCS), recaudo neto de la contribución de individuos AF2023-24 (Hacienda, $2,615.5 M), total y familias del Crédito por Trabajo AC2023 (Hacienda, $1,303 M y 700 mil), núcleos y beneficios del PAN y su composición (participantes de 60+, con salarios, con Seguro Social, núcleos sin ingreso) de los listados mensuales de ADSEF hasta agosto de 2025 (730,133 casos, $2,933 M), y vales de Sección 8 en uso (HUD 2025, 27,948). Tres cifras se guardan solo como comprobación: participantes del PAN (1.25 M; el modelo da 1.78 M), planillas rendidas (1.2 M proyectadas) y pagos de Sección 8 ($213 M; el modelo da el 73%, diagnosticado en `docs/statutes/hud/SOURCES.md`). El informe `data/calibration_report.csv` muestra antes y después; el 90% de los cocientes de pesos queda entre 0.44 y 2.4. El resultado es `data/prcs_2023_calibrated.h5`, versionado en el repositorio para que la app no tenga que reconstruirlo.

**Lo que los datos no permiten todavía.** La PRCS no pregunta quién rinde planilla, quién recibe cada ayuda ni cuánto; todo eso se construye o imputa. La comparación con cifras publicadas (`docs/validacion/comparacion_participantes.md`) muestra dónde se nota: personas en núcleos PAN (1.72 M en el modelo frente a 1.27 M de FNS) y planillas con Crédito por Trabajo (816 mil frente a las 700 mil «familias» de Hacienda). Las tablas distributivas de Hacienda (solicitadas) sustituirán los totales agregados por objetivos por tramo de ingreso.

## 5. Puntuación de reformas

`policyengine_pr/analysis/scoring.py`: `score(reform, dataset, eti)` corre la base con y sin la reforma y devuelve totales (contribución, Crédito por Trabajo, crédito federal, PAN, TANF, Sección 8, ingreso neto), un resumen (costo para Hacienda, hogares que ganan y pierden, cambio medio) y una tabla por decil de ingreso neto del hogar. Con `eti > 0` aplica una respuesta de comportamiento: cada contribuyente ajusta sus salarios según el cambio en su tasa marginal neta, con la elasticidad del ingreso tributable dada (0.25 como valor central de Saez, Slemrod y Giertz, 2012). Una puntuación tarda 0.2–0.3 s. `benefits_by_decile` produce la foto de partida de créditos y ayudas por decil.

`policyengine_pr/analysis/report.py` genera el informe de dos páginas en Markdown (una línea, qué cambia, totales, deciles, hogares de ejemplo, supuestos); `docs/hacienda/fuentes_documentos/md2docx.js` lo convierte a Word. Un ensayo completo con una reforma de siete palancas tardó menos de 15 minutos desde el texto hasta el Word (`docs/informes/ensayo_2027_notas.md`).

## 6. La aplicación

`app/calculator.py` (Streamlit) con módulos `ui.py` (textos ES/EN, hogares tipo, estado compartido), `cliffwatch.py` (la página ¿Y si gano más?: una sola simulación con `axes` de policyengine-core sobre 301 niveles de salario), `reforms_page.py`, `charts.py` (plantilla Plotly y paleta validada para daltonismo) y `card.py` (tarjetas PNG con Pillow). El estado del hogar viaja en la URL, de modo que un enlace reproduce exactamente lo que se ve; `?reform=<archivo>` carga una reforma del repositorio. Los cálculos de hogar son simulaciones de policyengine-core en memoria; la base calibrada se carga una vez por proceso con `st.cache_resource`.

Alojamiento: Streamlit Community Cloud desde el repositorio público; `requirements.txt` fija versiones; una acción de GitHub visita la app cada cuatro horas para que no se duerma. CI (`.github/workflows/test.yml`) corre ruff y las 109 pruebas en cada push.

## 7. Cómo verificarlo o extenderlo

```bash
git clone https://github.com/danielsantamariaots/policyengine-pr
cd policyengine-pr
uv venv --python 3.12 .venv && source .venv/bin/activate
uv pip install -e ".[dev,app]"
make test                       # 109 pruebas
streamlit run app/calculator.py
```

Para puntuar una reforma propia: copie `reforms/ensayo_2027.yaml`, cambie las palancas y ejecute
`python -m policyengine_pr.analysis.report reforms/mi_reforma.yaml salida.md 0.25`.
Para reconstruir los datos: descargue los PUMS 2023 de Puerto Rico en `data/raw/pums_2023/` y ejecute `python -c "from policyengine_pr.data import build_prcs, build_calibrated; build_prcs(); build_calibrated()"`.

Para añadir una provisión, `CONTRIBUTING.md` describe el único flujo admitido: documento oficial en `docs/statutes/`, parámetros con fuente, variable, prueba calculada a mano, fila en la app, nota en la hoja de ruta. Para preguntas técnicas: [correo del responsable técnico].
