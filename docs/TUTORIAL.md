# Guía de uso · Calculadora contributiva de hogares de Puerto Rico

*English version below.*

La calculadora estima, para un hogar, la contribución sobre ingresos de
Puerto Rico del año 2025, los créditos reembolsables y el ingreso neto, y
permite comparar la ley vigente con una reforma. Cada regla está citada a un
documento oficial de Hacienda o del IRS (véase `docs/statutes/`).

## Cómo abrirla

```bash
cd policyengine-pr
source .venv/bin/activate
streamlit run app/calculator.py
```

Se abre en el navegador en `http://localhost:8501`. El idioma se elige
arriba de la barra lateral (Español por defecto). Debajo, tres páginas:

- **Inicio**: el botón *Empezar con un ejemplo* abre *Mi hogar* con una madre de 32 años y dos hijos; debajo, tres tarjetas (*¿Cuánto paga mi hogar?* → Mi hogar;
  *¿Dónde pierde mi hogar al ganar más?* → CliffWatch), la guía y la lista
  de lo que el modelo no incluye.
- **Mi hogar** (la calculadora) y **¿Y si gano más?** (CliffWatch) comparten la barra lateral: el mismo
  hogar y la misma reforma se ven en las dos.

Las dos páginas empiezan con una línea que describe el hogar activo
("Contribuyente de 35 años; planilla individual; 2 dependientes…"), las
mismas cuatro cifras (contribución, créditos, ingreso neto y lo que se va
de cada $100) y una frase en lenguaje llano. Al pie de ambas: *Qué no
incluye*, *Ver supuestos* (los valores de ley vigente usados, con el
archivo de parámetros de cada uno) y *Cómo usar estas páginas*.

## 1. Describir el hogar

En *Mi hogar* el formulario está en el panel principal, en tres pasos:
**1 · ¿Quién vive en el hogar?** (planilla conjunta o no, edades, hijos),
**2 · ¿Qué ingresos tienen?** (salarios; pensión, Seguro Social y cuenta
propia bajo *otros ingresos*; deducciones del Anejo A si las tiene) y
**3 · Vivienda y ayudas** (municipio, vale de Sección 8, recursos y gastos
que afectan al PAN). Puede empezar con un *hogar tipo* y cambiar lo que
quiera. En las demás páginas el mismo formulario, en versión compacta,
está en la barra lateral; lo que escriba en un sitio se conserva en el
otro.

## 2. Leer los resultados

- **Arriba:** contribución sobre ingresos de PR, créditos reembolsables
  (Crédito por Trabajo + crédito federal por hijos), ingreso neto y la tasa
  contributiva neta. Una tasa negativa significa que el hogar recibe más en
  créditos de lo que paga en contribuciones.
- **Línea por línea (derecha):** sigue el orden del Formulario 482, de
  ingreso bruto ajustado a ingreso neto, con el número de línea de la
  planilla y una columna *Qué es* que explica cada partida en una frase.
- **A lo largo de la escala de ingresos (izquierda):** el mismo hogar con
  los salarios del contribuyente de $0 a $150,000. La línea punteada marca
  el hogar actual. *Ver tabla* muestra las cifras y la tasa marginal
  efectiva: cuánto de cada $100 adicionales se va en contribuciones y
  créditos perdidos.

## 3. Probar una reforma

Al final de la barra lateral, **Reforma** empieza con *Reformas de
ejemplo* (ampliar el tramo de 0% a $12,000; subir 20% el Crédito por
Trabajo máximo; eliminar el salto del 92% al 95%; exención personal a
$5,000 / $10,000), que rellenan los parámetros, y un *Nombre de la reforma*
que aparece en las gráficas. Debajo, los parámetros que una propuesta suele
tocar: tramos y tasas, exenciones, el factor 92%/95% y su umbral, los
máximos y límites del Crédito por Trabajo, y la exención para jóvenes.
Cambie uno o varios; los demás mantienen la ley vigente.

La página pasa a modo de comparación:

- cada cifra muestra su diferencia frente a la ley vigente (verde = mejora
  para el hogar);
- aparece la gráfica **Cambio en ingreso neto**, que muestra quién gana y
  quién pierde a lo largo de la escala de ingresos;
- la tabla Línea por línea añade las columnas Ley vigente / Reforma / Cambio.

Para volver a la ley vigente, restaure el valor original del parámetro.

## 4. CliffWatch

Arriba de la barra lateral, cambie *Mi hogar* por *¿Y si gano más?* (CliffWatch). Con el
mismo hogar, la página muestra:

- **Ingreso neto frente a ingreso de mercado**, con los salarios del
  contribuyente de $0 a $150,000 en pasos de $500; los precipicios se marcan
  con una X roja.
- **Contribuciones y créditos por nivel de salarios**: Crédito por Trabajo y
  crédito federal por hijos arriba del cero; contribución de PR y Seguro
  Social/Medicare debajo.
- **Tasa marginal efectiva**: de cada $100 adicionales, cuánto se va en
  contribuciones y créditos perdidos. Las zonas al 50% o más se sombrean.
- **Precipicios detectados** (salarios, pérdida de ingreso neto y causa
  principal) y **zonas de tasa marginal alta** (desde, hasta, tasa media).

Con una reforma activa se comparan las curvas de la ley vigente y de la
reforma, y los precipicios se calculan sobre la reforma.

**Comparar con otro hogar.** Al final de la página, *Comparar con* dibuja
el ingreso neto y la tasa marginal de otro hogar tipo sobre el mismo eje de
salarios. Si el hogar presenta planilla conjunta, la opción *Los mismos
adultos sin casarse* calcula la penalidad (o bono) por matrimonio: el
ingreso neto de la pareja menos la suma de los dos hogares por separado,
con el contribuyente a cargo de los hijos y el cónyuge solo con sus
propios ingresos.

**Vivienda (Sección 8).** En la barra lateral, marque *El hogar tiene un
vale de Sección 8* para añadir el subsidio de vivienda: la renta justa de
mercado de San Juan-Guaynabo (FY2025) para el tamaño del hogar menos el
30% del ingreso ajustado ($480 por cada menor de 18, $525 si hay una
persona de 62 años o más), según 24 CFR 5.611, 5.628 y 982.505. Si indica
la renta mensual, el subsidio no supera la renta.

**Compartir.** La dirección de la página incluye el hogar, la reforma y la
página abierta; el desplegable *Compartir* de la barra lateral muestra el
enlace. Quien lo abra verá exactamente lo mismo.

## 5. Reforma contributiva

La tercera página simula cada reforma sobre los microdatos de la Encuesta
sobre la Comunidad de Puerto Rico 2023 (PUMS, unos 1.28 millones de
hogares ponderados) con las reglas de 2025. La tabla muestra, para cada
reforma de ejemplo y para la reforma activa en la barra lateral: el costo
para Hacienda (contribución perdida más Crédito por Trabajo adicional), el
cambio en PAN, el porcentaje de hogares que ganan y pierden, y el cambio
medio por hogar. Debajo, para la reforma elegida: el cambio medio por decil
de ingreso neto, los hogares que ganan y pierden por decil, y los totales.

Los niveles (recaudo total, gasto en PAN) no están calibrados a las
planillas de Hacienda ni a los participantes de ADSEF; los cambios son la
cifra útil. Requiere `data/prcs_2023.h5` (véase `policyengine_pr/data/`).

## Ejemplos

1. **Exención para jóvenes.** Edad 22, salarios $30,000: contribución cero,
   y el Crédito por Trabajo se mantiene (los salarios exentos siguen
   contando como ingreso ganado).
2. **El precipicio del Crédito por Trabajo.** Dos dependientes, salarios
   $44,000 y luego $45,000: con $1,000 más de salario se pierde todo el
   crédito restante.
3. **Ampliar el tramo de 0%.** *Inicio del tramo 2* en $12,000: para un
   hogar con $30,000 la contribución baja $193 (7% × $3,000 × 0.92).
4. **Familia de un solo ingreso.** Planilla conjunta, cónyuge sin salarios,
   dos hijos: compare los umbrales conjuntos del Crédito por Trabajo con
   los individuales.

## Qué no incluye todavía

**No incluido:** tasas preferenciales distintas del 10% (intereses
bancarios) y 15% (dividendos y ganancias de capital), es decir, las
columnas de 4% y 20% del Anejo A2, y el arrastre de pérdidas de capital;
créditos no reembolsables por inversión (Anejo B); las categorías A, B,
D, G y T del TANF; efectos de comportamiento (el modelo
es estático).

**Incluido con salvedades:**

- **PAN** (Reglamento 8684 y Plan Estatal NAP): elegibilidad por ingreso
  neto mensual y beneficio máximo según el tamaño del hogar, con el bono
  por edad avanzada. ADSEF no publica la tabla que reduce el beneficio a
  medida que sube el ingreso neto, así que el modelo paga el máximo a todo
  hogar elegible (el precipicio al superar el límite es en parte un
  artefacto); los límites para hogares de 2 o más personas son los de
  octubre de 2021. La prueba de recursos ($5,000; $15,000 con una persona
  de 60+) y las deducciones por cuido, estudio y gastos médicos se aplican
  si usted las indica en *PAN: recursos y gastos*; no se modelan la
  deducción por incapacidad ni el suplemento de Vieques y Culebra.
- **TANF** (categoría C: madre o padre solo con hijos menores): máximo de
  una familia de tres ($584 al mes, Welfare Rules Database 2023) aplicado
  a todo tamaño, porque ADSEF no publica la tabla de necesidades; el
  ingreso contable se descuenta dólar por dólar tras $90 de gastos de
  trabajo.
- **Plan Vital**: miembros elegibles según los niveles de ingreso de CMS
  (tabla de abril de 2026), sin asignarle valor en dólares.
- **Sección 8**: solo si usted indica que el hogar tiene vale; usa las
  rentas justas de mercado y los límites de ingreso de HUD del municipio
  elegido (15 áreas) y el estándar de ocupación de Vivienda, pero no el
  esquema de estándares de pago en dólares, que Vivienda no publica
  (`docs/statutes/hud/SOURCES.md`). En los microdatos el vale se imputa y
  se calibra a 27,948 hogares (HUD, 2025).

Los resultados son estimaciones y no sustituyen asesoría profesional.

---

# User guide · Puerto Rico household tax calculator

The calculator estimates a household's 2025 Puerto Rico income tax,
refundable credits and net income, and compares current law with a reform.
Every rule is cited to an official Hacienda or IRS document (see
`docs/statutes/`).

**Open it:** `streamlit run app/calculator.py` from the repo with the venv
active; it opens at `http://localhost:8501`. Choose the language at the top
of the sidebar.

**1. Describe the household** in the sidebar: filing status, ages (they
drive the youth exemption at 16–26, the pension exemption at 60+, and the
children's eligibility for credits), wages, veteran status, other income
(self-employment, pensions, Social Security), dependents, Anejo A
deductions.

**2. Read the results.** Headline metrics at the top; *Line by line* on the
right follows Formulario 482; the chart on the left varies the filer's wages
from $0 to $150,000, with *Table view* adding the effective marginal rate.

**3. Try a reform.** *Reform* at the bottom of the sidebar lists the
levers a proposal is likely to move. Change any of them and the page shows
deltas against current law plus a *Change in net income* chart.

**4. CliffWatch.** Switch *My household* to *What if I earn more?* at the top of the
sidebar: net income vs market income in $500 steps to $150,000, taxes and
credits by wage level, the effective marginal rate, and tables of cliffs
(where $500 more in wages lowers net income) and high-rate zones (≥ 50%).
With a reform active, both curves are compared. *Compare with*, at the
bottom, overlays another preset household on the same wage axis; for a
joint return, *The same adults unmarried* gives the marriage penalty or
bonus (the couple's net income minus the two separate households, filer
with the children, spouse alone).

**Housing (Section 8).** Tick *Household holds a Section 8 voucher* in the
sidebar to add the housing subsidy: the FY2025 San Juan-Guaynabo fair
market rent for the household's size less 30% of adjusted income ($480 per
member under 18, $525 for a member aged 62+), per 24 CFR 5.611, 5.628 and
982.505; a monthly rent, if given, caps the subsidy.

**Share.** The page address carries the household, the reform and the open
page; the *Share* expander in the sidebar shows the link.

**Examples:** age 22 and $30,000 wages (zero tax, EITC kept); two children
at $44,000 vs $45,000 (the EITC cliff); *Bracket 2 starts* at $12,000 (tax
falls $193 for a $30,000 household).

**Not yet included:** preferential rates other than 10%/15% (Anejo A2
columns at 4%/20%), Anejo B investment credits, TANF categories other than
C, behavioural responses. **With caveats:** PAN pays the maximum to every
eligible household (ADSEF's benefit schedule is unpublished); TANF uses the
three-person maximum for every size; Plan Vital is eligibility only;
Section 8 only when the household says it holds a voucher, with HUD's
limits and fair market rents for the chosen municipio rather than
Vivienda's unpublished payment-standard schedule. Results are estimates,
not professional advice.


> Desde el 4 de noviembre de 2026 los parámetros uno a uno (tramos, tasas, exenciones, Crédito por Trabajo) están ocultos tras el interruptor *Ajustar los parámetros uno a uno* en la sección *Reforma contributiva* de la barra lateral; las *Propuestas de ejemplo* los fijan sin abrirlo.
