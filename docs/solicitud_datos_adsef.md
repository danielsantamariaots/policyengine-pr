# Solicitud de información sobre el Programa de Asistencia Nutricional

*Borrador para Espacios Abiertos · proyecto policyengine-pr · [fecha]*

---

**A:** Administración de Desarrollo Socioeconómico de la Familia (ADSEF)
Departamento de la Familia
Oficina del Administrador / División de Planificación Estratégica

**De:** [Nombre], [cargo], Espacios Abiertos
[dirección · correo electrónico · teléfono]

**Asunto:** Solicitud de la Tabla de Beneficios del PAN, del Plan Estatal de Operaciones del NAP y de la tabla de necesidades básicas del TANF vigentes, para un modelo público de microsimulación

## 1. Propósito

Espacios Abiertos desarrolla **policyengine-pr**, un modelo de microsimulación de código abierto del sistema de contribuciones y beneficios de Puerto Rico, construido sobre la plataforma PolicyEngine. El modelo permite estimar cómo cambian la contribución sobre ingresos, los créditos reembolsables y los beneficios de un hogar a medida que varían sus ingresos, y cómo lo afectaría una reforma. Para que la parte del PAN sea exacta necesitamos reproducir la regla de elegibilidad y la asignación de beneficios tal como la aplica ADSEF.

Hemos codificado las reglas del **Reglamento 8684** (artículos 42, 45 y 51) y las cantidades del **Plan Estatal de Operaciones del NAP para el año fiscal 2022** publicado en el portal de ADSEF (deducciones, límites de ingreso neto y beneficio máximo por tamaño del núcleo, bono de edad avanzada), así como los cambios de agosto de 2024 anunciados por el Departamento (deducción fija de $279, límite de $633 para una persona, deducción máxima por ingreso devengado de $1,400). No solicitamos datos de participantes ni información que permita identificar a persona alguna; solo los documentos normativos.

## 2. Documentos solicitados

1. **La Tabla de Beneficios del PAN vigente** (a la que se refieren el artículo 5, definición 69, y el artículo 51.A del Reglamento 8684): para cada tamaño del núcleo de servicio, el beneficio mensual que corresponde a cada tramo de ingreso neto entre cero y el ingreso neto máximo. Es el único documento que nos falta para reproducir la asignación de beneficios; sin él, el modelo solo puede estimar el beneficio máximo y el punto en que se pierde la elegibilidad.
2. **Los límites de ingreso neto máximo y los beneficios máximos vigentes por tamaño del núcleo** (de 1 a 18 o más personas), con su fecha de efectividad. La versión pública más reciente que conocemos es la de octubre de 2021 (Plan Estatal FY2022, p. 28); el ajuste de agosto de 2024 solo se ha publicado para núcleos de una persona.
3. **El Plan Estatal de Operaciones del NAP para los años fiscales 2025 y 2026** aprobados por el USDA-FNS, o al menos la sección VII (*Criteria for Funds Distribution*) con las deducciones y tablas vigentes.
4. **Las cantidades vigentes de las deducciones** del artículo 45 que no aparecen en los documentos anteriores: deducción por cuido de menores y adultos, por persona incapacitada, por estudiante, por gastos médicos recurrentes y por enfermedad terminal; y la deducción por ingresos de agricultura.
5. **El beneficio máximo para los municipios de Vieques y Culebra** por tamaño del núcleo, y el bono de edad avanzada vigente.
6. Si existe, **la enmienda al Reglamento 8684 de 2024** (número de reglamento y texto) que incorporó los cambios en recursos máximos ($5,000 / $15,000), en el cómputo del 50% de los ingresos de Seguro Social, retiro y desempleo, y en la exención escalonada por nuevo empleo (12 meses al 100%, 6 al 66%, 33% hasta el mes 24).

Sobre el **Programa de Ayuda Temporal para Familias Necesitadas (TANF)**, cuyas reglas hemos codificado a partir del Reglamento 7653 (2008) y de las cifras que el Welfare Rules Database (Urban Institute / ACF) publica para Puerto Rico (beneficio máximo de $584 mensuales y tope de ingresos de $1,620 para una familia de tres personas, 2023):

7. **La tabla de necesidades básicas (estándar de necesidad y de pago) de la categoría C vigente**, por tamaño de la unidad familiar (de 1 a 12 personas), a la que se refieren las secciones 4.16 y 4.22 del Reglamento 7653, con su fecha de efectividad. Solo conocemos el valor para tres personas.
8. **El nuevo reglamento del TANF** que, según la ponencia de ADSEF ante el Comité de Transición (octubre de 2024), sustituiría al Reglamento 7653, si ya fue aprobado; y las cantidades vigentes de las deducciones y exenciones de las secciones 4.18 a 4.20 (gastos de trabajo, cuido de menores, exención por nuevo empleo) y del beneficio regular de las categorías A, B, D, G y T.

Si alguno de estos documentos se publica en el portal de ADSEF o en docs.pr.gov, agradeceríamos el enlace.

## 3. Compromisos de Espacios Abiertos

- Los documentos se utilizarán únicamente para codificar las reglas del PAN y del TANF en policyengine-pr, cuyo código y fuentes son públicos (github.com/danielsantamariaots/policyengine-pr); cada regla citará el documento de ADSEF del que procede.
- Espacios Abiertos pondrá a disposición de ADSEF, sin costo, el modelo, su documentación y la herramienta de cálculo de hogares, que permite ver cómo interactúan el PAN, el Crédito por Trabajo y la contribución sobre ingresos a lo largo de la escala de ingresos.
- Compartiremos con antelación cualquier informe que utilice estas reglas.

## 4. Contacto

[Nombre, cargo, correo, teléfono]
Para asuntos técnicos: [nombre del responsable técnico].

Quedamos a su disposición para reunirnos con el personal de la División de Planificación Estratégica o de la Oficina de Tecnología e Información y aclarar cualquier punto.

Atentamente,

[firma]
