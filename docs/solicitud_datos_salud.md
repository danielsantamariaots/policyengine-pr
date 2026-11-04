# Solicitud de información sobre los niveles de elegibilidad del Plan Vital

*Borrador para Espacios Abiertos · proyecto policyengine-pr · [fecha]*

---

**A:** Departamento de Salud de Puerto Rico
Programa Medicaid — Oficina del Director Ejecutivo
Con copia a la Administración de Seguros de Salud (ASES)

**De:** [Nombre], [cargo], Espacios Abiertos
[dirección · correo electrónico · teléfono]

**Asunto:** Solicitud de las tablas de elegibilidad por ingresos del Programa Medicaid / Plan Vital, para un modelo público de microsimulación

## 1. Propósito

Espacios Abiertos desarrolla **policyengine-pr**, un modelo de microsimulación de código abierto del sistema de contribuciones y beneficios de Puerto Rico, construido sobre la plataforma PolicyEngine. El modelo estima, para cualquier hogar, la contribución sobre ingresos, los créditos reembolsables y los beneficios (PAN, TANF) y señala los puntos de la escala de ingresos en que un aumento de salario deja al hogar con menos recursos. La elegibilidad al Plan Vital es, junto con el PAN, el umbral que más pesa en esos puntos, y por eso necesitamos reproducirla con exactitud.

Hemos codificado los niveles mensuales de ingreso que publica CMS para Puerto Rico (Medicaid and CHIP Standard Monthly Income Eligibility Levels, vigentes del 1 de abril de 2026 al 2027: $1,835 para una persona y $653 por cada persona adicional en Medicaid; $3,604 y $1,283 en CHIP). No solicitamos datos de beneficiarios ni información que permita identificar a persona alguna; solo los documentos normativos.

## 2. Documentos solicitados

1. **Las tablas de elegibilidad por ingresos vigentes y las de los dos años anteriores** (en particular las del 1 de abril de 2025 al 31 de marzo de 2026), por grupo de elegibilidad (adultos, niños/CHIP, embarazadas, padres y encargados, y los grupos no basados en MAGI: edad avanzada, ceguera e incapacidad) y por tamaño del hogar, con su fecha de efectividad y el por ciento del nivel de pobreza que representan.
2. **El Manual de Elegibilidad del Programa Medicaid** (o la sección del Plan Estatal de Medicaid de Puerto Rico) que define el ingreso contable, las deducciones aplicables y la prueba de recursos, si alguna, para cada grupo.
3. **La definición de la unidad familiar** usada para el tamaño del hogar y la regla para los menores de 19 años cuyo hogar supera el nivel de Medicaid pero no el de CHIP.
4. **Las estadísticas de inscripción más recientes** por grupo de elegibilidad y región (las que alimentan la cifra de 1.3 millones de inscritos que informa CMS), para calibrar el modelo.

Si alguno de estos documentos se publica en medicaid.pr.gov o en el portal de ASES, agradeceríamos el enlace.

## 3. Compromisos de Espacios Abiertos

- Los documentos se utilizarán únicamente para codificar las reglas de elegibilidad en policyengine-pr, cuyo código y fuentes son públicos (github.com/danielsantamariaots/policyengine-pr); cada regla citará el documento del Departamento de Salud del que procede.
- Espacios Abiertos pondrá a disposición del Departamento de Salud y de ASES, sin costo, el modelo, su documentación y la herramienta de cálculo de hogares.
- Compartiremos con antelación cualquier informe que utilice estas reglas.

## 4. Contacto

[Nombre, cargo, correo, teléfono]
Para asuntos técnicos: [nombre del responsable técnico].

Quedamos a su disposición para reunirnos con el personal del Programa Medicaid y aclarar cualquier punto.

Atentamente,

[firma]
