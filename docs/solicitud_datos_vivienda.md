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

Hemos codificado la fórmula federal de 24 CFR Partes 5 y 982 (ingreso anual y ajustado con las deducciones de HOTMA de $480 por dependiente y $525 por familia de edad avanzada o con incapacidad; pago total del inquilino igual al mayor entre el 30% del ingreso ajustado y el 10% del ingreso bruto; subsidio igual al menor entre el estándar de pago y la renta bruta, menos el pago del inquilino) y las tablas de HUD para el año fiscal 2025: los límites de ingreso y las rentas justas de mercado (FMR) del área San Juan-Guaynabo (eficiencia $552, 1 dormitorio $569, 2 dormitorios $656, 3 dormitorios $861, 4 dormitorios $1,033). Hemos incorporado también el Plan Administrativo del Programa de Vales de Elección de Vivienda (enmienda del 20 de junio de 2025, publicado en avp.pr.gov): el estándar de ocupación (dos personas por dormitorio, dormitorio aparte para el jefe de familia o cónyuge, vale de un dormitorio para una persona sola) y la renta mínima de $0. Lo que no está publicado es el esquema en dólares que la agencia fija cada año dentro de la banda del 90% al 110% de la FMR, y por ello acudimos a ustedes. No solicitamos datos de participantes ni información que permita identificar a persona alguna; solo documentos normativos y estadísticas agregadas.

## 2. Documentos solicitados

1. **El esquema de estándares de pago vigente** (24 CFR 982.503; Plan Administrativo, Sección VI.A) por número de dormitorios y por área de FMR u oficina regional, con su fecha de efectividad y el por ciento de la FMR que representa, y los esquemas de los dos años anteriores.
2. **El esquema de asignaciones por utilidades** (utility allowance schedule) vigente, por tipo de unidad y número de dormitorios.
3. **La fecha de implantación de las deducciones de HOTMA** ($525 por familia de edad avanzada o con incapacidad, en lugar de los $400 que aún figuran en el Plan Administrativo de junio de 2025) y los umbrales vigentes de las deducciones por gastos médicos, de incapacidad y de cuido de niños.
4. **Estadísticas agregadas más recientes** del programa, por oficina regional o área de FMR y por tamaño del hogar: vales autorizados y en uso (12,896 según el Plan Anual 2026), pago de asistencia de vivienda (HAP) promedio, ingreso anual promedio de las familias participantes y distribución por fuente principal de ingreso (salarios, Seguro Social, pensiones, TANF). Estas cifras nos permitirán estimar qué proporción de los hogares de la Encuesta sobre la Comunidad de Puerto Rico recibe el subsidio en cada área y calibrar el modelo.
5. **Los límites de ingreso para admisión** que aplica la agencia a cada área de FMR (ingreso muy bajo y extremadamente bajo), si difieren de las tablas publicadas por HUD.

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
