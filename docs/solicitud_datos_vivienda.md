# Solicitud de información sobre el Programa de Vales de Elección de Vivienda (Sección 8)

*Borrador para Espacios Abiertos · proyecto policyengine-pr · [fecha]*

---

**A:** Departamento de la Vivienda de Puerto Rico
Administración de Vivienda Pública — Oficina del Administrador
Programa de Vales de Elección de Vivienda (Housing Choice Voucher, Sección 8)
Con copia a la Oficina de Campo de HUD en San Juan

**De:** [Nombre], [cargo], Espacios Abiertos
[dirección · correo electrónico · teléfono]

**Asunto:** Solicitud de los estándares de pago, estándares de subsidio y estadísticas del Programa de Vales de Elección de Vivienda, para un modelo público de microsimulación

## 1. Propósito

Espacios Abiertos desarrolla **policyengine-pr**, un modelo de microsimulación de código abierto del sistema de contribuciones y beneficios de Puerto Rico, construido sobre la plataforma PolicyEngine. El modelo estima, para cualquier hogar, la contribución sobre ingresos, los créditos reembolsables y los beneficios (PAN, TANF, Plan Vital) y señala los puntos de la escala de ingresos en que un aumento de salario deja al hogar con menos recursos. El subsidio de vivienda se reduce en 30 centavos por cada dólar adicional de ingreso ajustado, de modo que, sumado al PAN y a las contribuciones, determina cuánto conserva una familia que trabaja más. Por eso necesitamos reproducirlo con exactitud.

Hemos codificado la fórmula federal de 24 CFR Partes 5 y 982 (ingreso anual y ajustado con las deducciones de HOTMA de $480 por dependiente y $525 por familia de edad avanzada o con incapacidad; pago total del inquilino igual al mayor entre el 30% del ingreso ajustado y el 10% del ingreso bruto; subsidio igual al menor entre el estándar de pago y la renta bruta, menos el pago del inquilino) y las tablas de HUD para el año fiscal 2025: los límites de ingreso y las rentas justas de mercado (FMR) del área San Juan-Guaynabo (eficiencia $552, 1 dormitorio $569, 2 dormitorios $656, 3 dormitorios $861, 4 dormitorios $1,033). Lo que HUD no publica es lo que fija cada agencia de vivienda pública (PHA), y por ello acudimos a ustedes. No solicitamos datos de participantes ni información que permita identificar a persona alguna; solo documentos normativos y estadísticas agregadas.

## 2. Documentos solicitados

1. **Los estándares de pago vigentes** (24 CFR 982.503) por número de dormitorios y por municipio o área de FMR, con su fecha de efectividad y el por ciento de la FMR que representan, para el programa que administra la Administración de Vivienda Pública y, de ser posible, para las agencias municipales (San Juan, Carolina, Bayamón, Ponce, Mayagüez y las demás que administran vales).
2. **El estándar de subsidio** (24 CFR 982.402): la regla que asigna el tamaño del vale (número de dormitorios) según la composición de la familia, tal como figura en el Plan Administrativo del programa.
3. **La renta mínima** (24 CFR 5.630) adoptada por la agencia y las exenciones por dificultad económica.
4. **El Plan Administrativo del Programa de Vales de Elección de Vivienda** completo, o las secciones sobre elegibilidad, cálculo del ingreso y del subsidio, preferencias de admisión y terminación por subsidio cero (24 CFR 982.455).
5. **Las deducciones y exclusiones de ingreso** que aplica la agencia además de las federales (gastos médicos, de incapacidad y de cuido de niños), con los umbrales vigentes tras la implantación de HOTMA.
6. **Estadísticas agregadas más recientes** del programa, por municipio o área de FMR y por tamaño del hogar: número de vales autorizados y en uso, pago de asistencia de vivienda (HAP) promedio, ingreso anual promedio de las familias participantes y distribución por fuente principal de ingreso (salarios, Seguro Social, pensiones, TANF). Estas cifras nos permitirán estimar qué proporción de los hogares de la Encuesta sobre la Comunidad de Puerto Rico recibe el subsidio y calibrar el modelo.
7. **Los límites de ingreso para admisión** que aplica la agencia a cada área de FMR (ingreso muy bajo y extremadamente bajo), si difieren de las tablas publicadas por HUD.

Si alguno de estos documentos se publica en vivienda.pr.gov o en el portal de la Administración de Vivienda Pública, agradeceríamos el enlace.

## 3. Compromisos de Espacios Abiertos

- Los documentos se utilizarán únicamente para codificar las reglas del programa en policyengine-pr, cuyo código y fuentes son públicos (github.com/danielsantamariaots/policyengine-pr); cada regla citará el documento del Departamento de la Vivienda del que procede.
- Espacios Abiertos pondrá a disposición del Departamento de la Vivienda y de la Administración de Vivienda Pública, sin costo, el modelo, su documentación y la herramienta de cálculo de hogares, incluida la página CliffWatch que muestra cómo cambia el subsidio con los salarios.
- Compartiremos con antelación cualquier informe que utilice estas reglas.

## 4. Contacto

[Nombre, cargo, correo, teléfono]
Para asuntos técnicos: [nombre del responsable técnico].

Quedamos a su disposición para reunirnos con el personal del programa y aclarar cualquier punto.

Atentamente,

[firma]
