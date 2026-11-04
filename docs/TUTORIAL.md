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

- **Inicio**: dos tarjetas (*¿Cuánto paga mi hogar?* → Calculadora;
  *¿Dónde pierde mi hogar al ganar más?* → CliffWatch), la guía y la lista
  de lo que el modelo no incluye.
- **Calculadora** y **CliffWatch** comparten la barra lateral: el mismo
  hogar y la misma reforma se ven en las dos.

Las dos páginas empiezan con una línea que describe el hogar activo
("Contribuyente de 35 años; planilla individual; 2 dependientes…"), las
mismas cuatro cifras (contribución, créditos, ingreso neto y lo que se va
de cada $100) y una frase en lenguaje llano. Al pie de ambas: *Qué no
incluye*, *Ver supuestos* (los valores de ley vigente usados, con el
archivo de parámetros de cada uno) y *Cómo usar estas páginas*.

## 1. Describir el hogar

En la barra lateral, primero **Hogar tipo**: seis hogares de ejemplo
(trabajador con salario mínimo, madre o padre con dos hijos, pareja con dos
salarios, pensionado de 65, joven de 22, cuenta propia) que rellenan los
campos; después ajuste lo que quiera. *Hogar personalizado* deja los campos
como están.

| Campo | Qué poner |
|---|---|
| Casados que rinden planilla conjunta | Active para una pareja; aparecen los campos del cónyuge |
| Edad y salarios | Por persona. Las edades importan: exención para jóvenes (16–26), exención de pensión (60+), edad de los dependientes para los créditos |
| Es veterano | Añade la exención adicional de $1,500 |
| Otros ingresos | Ganancia neta por cuenta propia (Anejo M), pensión de plan cualificado (Anejo H), Seguro Social (no tributa), intereses bancarios (10%, primeros $100 exentos), dividendos y ganancias de capital (15%, o las tasas ordinarias si resultan menores: Anejo A2) |
| Dependientes (hijos) | Número y edades. Cuentan para la exención por dependiente ($2,500), el Crédito por Trabajo (hasta 18 años, o 25 si estudian) y el crédito federal por hijos (menores de 17) |
| Deducciones (Anejo A) | Cantidades pagadas; la calculadora aplica los límites de ley |
| Avanzado | Partidas sujetas a contribución básica alterna que el modelo aún no calcula |

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

Arriba de la barra lateral, cambie *Calculadora* por *CliffWatch*. Con el
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

- Tasas preferenciales distintas del 10% (intereses bancarios), 15%
  (dividendos y ganancias de capital): columnas de 4% y 20% del Anejo A2.
- Créditos no reembolsables por inversión (Anejo B).
- Beneficios: PAN, Medicaid/Vital, TANF, Sección 8.
- Efectos de comportamiento: el modelo es estático.

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

**4. CliffWatch.** Switch *Calculator* to *CliffWatch* at the top of the
sidebar: net income vs market income in $500 steps to $150,000, taxes and
credits by wage level, the effective marginal rate, and tables of cliffs
(where $500 more in wages lowers net income) and high-rate zones (≥ 50%).
With a reform active, both curves are compared.

**Examples:** age 22 and $30,000 wages (zero tax, EITC kept); two children
at $44,000 vs $45,000 (the EITC cliff); *Bracket 2 starts* at $12,000 (tax
falls $193 for a $30,000 household).

**Not yet included:** preferential rates other than 10%/15% (Anejo A2
columns at 4%/20%), Anejo B investment credits,
benefits (PAN, Medicaid), behavioural responses. Results are estimates, not
professional advice.
