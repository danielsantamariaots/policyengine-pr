# Ensayo de respuesta rápida, 4 de noviembre de 2026

Propuesta ficticia de siete palancas (`reforms/ensayo_2027.yaml`): tramo de
0% hasta $15,000, tasa del segundo tramo al 5%, exención por dependiente a
$3,000, Crédito por Trabajo máximo +15%. Cadena completa medida en un
portátil, base PRCS 2023 calibrada:

| Paso | Tiempo | Resultado |
|---|---|---|
| Escribir el archivo de reforma | 5 min | 7 palancas, valores relativos ("+15%") resueltos por `load_reform` |
| Puntuación estática (`score`) | 0.2 s (1.4 s de carga) | costo $554 M; 55% de hogares ganan, 0% pierden |
| Puntuación con ETI 0.25 | 0.3 s | $588 M |
| Informe Markdown (`analysis.report`) | 3.0 s | `docs/informes/ensayo_2027.md` |
| Word (`md2docx.js`) | 1.0 s | `docs/informes/ensayo_2027.docx` |
| App: reforma de ejemplo, Calculadora, CliffWatch, Reformas | 7.5 s (AppTest) | sin errores; enlace compartible con las 7 palancas en la URL |

Total, desde el texto de la propuesta hasta el Word y el enlace: bajo 15
minutos, casi todo en escribir el archivo.

## Lo que el ensayo encontró y se corrigió

- Las etiquetas de la tabla "Qué cambia" del informe salían en inglés
  (`EITC maximum, no children`); ahora usan las etiquetas en español
  compartidas con la app (`LEVER_LABELS_ES` en `reforms/parametric.py`).

## Lo que sigue manual o débil

1. Un proyecto de ley real cambia cosas que no son palancas (por ejemplo,
   un crédito nuevo o una regla de elegibilidad). Eso exige código, no un
   archivo YAML; el día de la reforma hay que presupuestar horas, no
   minutos, para esa parte.
2. El nombre de la reforma viaja en la URL compartida; con nombres largos
   el enlace es incómodo. Un alias corto (`?reform=ensayo_2027`) que cargue
   el archivo del repositorio evitaría llevar las 7 palancas en la URL.
3. El informe no incluye las gráficas; el Word es solo tablas. Añadir la
   gráfica de deciles como imagen exige exportar Plotly (kaleido).
4. No hay revisión: el informe sale sin que nadie coteje los hogares de
   ejemplo con una planilla a mano. Conviene tener preparados dos casos con
   su cálculo manual y rehacerlos con la reforma antes de publicar.
