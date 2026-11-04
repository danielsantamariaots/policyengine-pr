# -*- coding: utf-8 -*-
"""
Construye el libro de petición de datos a Hacienda (Peticion_datos_Hacienda_policyengine-pr.xlsx) con la misma
estructura que el libro de la petición de Arnold Ventures: una hoja «Léame», una hoja con las peticiones (R1–R6), las
columnas de los archivos de entrada (leídas de los esquemas del paquete), las reglas del archivo, el índice de tablas, una
hoja por tabla con la plantilla vacía (encabezados y etiquetas de fila, tomadas de las salidas de referencia en modalidad
«vaciar», que conservan todas las filas) y la hoja de confidencialidad y entrega.

Uso: python construir_peticion_excel.py  (desde cualquier carpeta; escribe el .xlsx junto a este archivo)
"""

from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

AQUI = Path(__file__).resolve().parent
PAQ = AQUI.parent / "paquete"
REF = PAQ / "05_salidas_de_referencia" / "modalidad_vaciar"
SALIDA = AQUI / "Peticion_datos_Hacienda_policyengine-pr.xlsx"

NEGRITA = Font(bold=True)
TITULO = Font(bold=True, size=13)
CAB = PatternFill("solid", fgColor="DDEBF7")
GRIS = PatternFill("solid", fgColor="F2F2F2")
AJUSTE = Alignment(wrap_text=True, vertical="top")

TABLAS = [
    ("0", "Tabla de control", "Una fila por año", "Totales del archivo de entrada: planillas, sumas y conteos de las variables principales, planillas por estado personal y por factor, comprobantes W-2PR", "—", "Cuadrar el archivo con los totales de Hacienda"),
    ("A", "Resumen por tramo de IBA y estado personal", "Estado personal × 15 tramos de IBA + totales", "Planillas, planillas con dependientes y con Crédito por Trabajo, suma de cada línea del Formulario 482 (1A–31), planillas y contribución al 92 % y al 95 %", "Líneas 1A–31", "Tabla principal de calibración"),
    ("B", "Deducciones del Anejo A por tramo de IBA", "15 tramos de IBA + total", "Planillas y cantidad de cada deducción (1i, 3, 4, 7b, 8b, 9b) y total (11)", "Anejo A", "Imputar deducciones"),
    ("C", "Ingresos exentos del Anejo IE por tramo de IBA", "15 tramos de IBA (IBA + exentos) + total", "Planillas y cantidad: exención de pensiones, exención de jóvenes (31), difícil reclutamiento (32), total (45)", "Anejo IE", "Reproducir el ingreso exento"),
    ("D1", "Crédito por Trabajo por dependientes y estado personal", "Estado personal × dependientes cualificados (0–3+) + totales", "Planillas, crédito, ingreso bruto ganado", "Anejo CT; línea 27C", "Nivel del crédito"),
    ("D2", "Crédito por Trabajo por tramo de ingreso ganado", "Dependientes (0–3+) × tramos de $2,500 de ingreso ganado hasta $55,000 + totales", "Planillas, crédito", "Anejo CT Parte II línea 3", "Forma de las fases del crédito"),
    ("D3", "Crédito por Trabajo denegado o ajustado", "Dependientes (0–3+) + total", "Planillas ajustadas, crédito reclamado, concedido, ajuste", "Anejo CT", "Tasa de ajuste"),
    ("E", "Exención para jóvenes (Ley 135-2014) por edad", "Edad simple 16–26 + total", "Planillas, cantidad exenta, salarios, ingreso de negocio, contribución determinada", "Anejo IE línea 31", "Calibrar la exención"),
    ("F", "Umbral de $100,000 del factor 92 %/95 %", "Ingreso bruto en tramos de $2,000 entre $90,000 y $110,000 + total", "Planillas al 92 % y al 95 % y su contribución regular", "Sección 1021.01(c); línea 17", "Respuesta al escalón"),
    ("G1", "Ajuste gradual", "Estado personal + total", "Planillas con ingreso neto > $500,000, ingreso neto, ajuste gradual", "Línea 15", "Parte alta de la distribución"),
    ("G2", "Contribución básica alterna", "5 tramos de ingreso neto sujeto a CBA + total", "Planillas, ingreso neto CBA, contribución básica alterna, exceso", "Anejo O; línea 20", "Parte alta de la distribución"),
    ("H", "Dependientes reclamados", "Estado personal × dependientes (0–4+) + totales", "Planillas, exención por dependientes, Crédito por Trabajo, créditos federales", "Líneas 8, 27C, 27D", "Estructura de los hogares"),
    ("I", "Comprobantes W-2PR por tramo de salarios", "Tramos de $2,500 hasta $50,000 y tramos 9–15 de IBA + total", "Comprobantes, personas distintas, salarios, retenida, exentos Ley 135", "Formulario 499R-2/W-2PR", "Personas que no rinden planilla"),
    ("I_edad", "Comprobantes W-2PR por tramo de salarios y edad", "Grupo de edad × los mismos tramos + totales", "Las mismas", "W-2PR", "Idem, por edad"),
    ("J", "Distribución por municipio", "78 municipios + total", "Planillas, IBA, contribución determinada, planillas y cantidad del Crédito por Trabajo", "Pág. 1 (dirección)", "Validación geográfica"),
]

PETICIONES = [
    ("R1", "Construir el archivo de planillas", "Una fila por planilla vigente del Formulario 482 y año contributivo (2021–2024), con las 51 columnas de la hoja «Archivo de planillas» (14 necesarias; las demás, si se pueden extraer).", "planillas_<anio>.csv (se queda en Hacienda); disponibilidad de cada columna anotada en la ficha de extracción.", "La plantilla de la consulta está en 02_contrato_y_parametros/extraccion_SURI_plantilla.sql."),
    ("R2", "Construir el archivo de comprobantes W-2PR (si es posible)", "Una fila por comprobante 499R-2/W-2PR, de todas las personas, con las 6 columnas de la hoja «Archivo W-2PR»; la clave id_persona es un hash con clave secreta de Hacienda.", "w2pr_<anio>.csv (se queda en Hacienda).", "Única fuente sobre quienes devengan salarios y no rinden planilla. Produce las Tablas I e I_edad."),
    ("R3", "Ejecutar el programa tras la prueba con datos ficticios", "Paso 0 con el paquete PE_Hacienda_Python (datos ficticios), después los pasos 2 a 4 sobre los archivos reales, un año cada vez.", "Tablas 0 y A–J, libro Excel, registro, informes de validación y verificación.", "Python 3.9 o posterior con pandas, numpy y openpyxl; sin internet. Menos de un minuto por año."),
    ("R4", "Entregar las salidas, el registro, los informes y la ficha", "Las tablas CSV y el .xlsx de cada año, log_ejecucion_pe.txt, validacion_entrada_<anio>.txt, verificacion_salidas_<anio>.txt y ficha_extraccion_plantilla.csv rellenada.", "Archivos de la hoja «Confidencialidad y entrega».", "La ficha es el libro de códigos de las tablas: qué línea del Formulario 482 se usó en cada año y qué columnas no estaban."),
    ("R5", "Elegir la modalidad de supresión", "Por defecto, colapsar las filas con menos de 10 planillas en la contigua (conserva los totales). Alternativa: vaciar las filas (modalidad de los paquetes WTG y AV).", "Indicación en la ficha (o simplemente la opción --supresion usada).", "Ambas modalidades vacían además los conteos parciales entre 1 y 9 y protegen los totales."),
    ("R6", "Documentación complementaria", "Fecha de corte de cada año y tratamiento de las enmiendas; cualquier tabulación publicada previamente con estas variables (informes al Legislativo, nota de ajuste por inflación del Crédito por Trabajo).", "PDF o XLSX.", "Para asegurar la consistencia con las cifras oficiales."),
]

REGLAS = [
    ("Unidad", "Una fila por planilla vigente del Formulario 482 y año contributivo; si hay enmiendas, una sola fila (la última válida)."),
    ("Años", "2021, 2022, 2023 y 2024 (2025 cuando cierre el ciclo de radicación). Un archivo por año o uno solo con la columna anio."),
    ("Nombres", "Los de la hoja «Archivo de planillas», en minúsculas, sin ñ ni acentos. El orden de las columnas no importa; los nombres sí."),
    ("Valores", "0 cuando el concepto no aplica; celda vacía solo cuando el dato no consta. Punto decimal, sin separadores de miles, sin símbolo de moneda."),
    ("Formato", "CSV en UTF-8, separador coma, una fila de encabezado. Celda vacía para los nulos (no NULL, NA ni punto)."),
    ("Identificadores", "Ninguno: ni número de seguro social, ni nombre, ni número de planilla. En el archivo W-2PR, solo id_persona (hash con clave secreta de Hacienda), que no aparece en ninguna salida."),
    ("Columnas no disponibles", "Se quitan de la consulta y se anotan en la ficha; el programa omite solo lo que depende de ellas (columna «si falta»)."),
    ("Validación", "validar_entrada.py comprueba todo lo anterior y debe terminar con 0 error(es) antes de ejecutar."),
]

ENTREGA = [
    ("Lo que sale de Hacienda", "Solo tablas agregadas ya protegidas: tabla_0_control.csv, tabla_A.csv … tabla_J.csv y tabulaciones_482_<anio>.xlsx de cada año; log_ejecucion_pe.txt; validacion_entrada_<anio>.txt; verificacion_salidas_<anio>.txt; ficha_extraccion_plantilla.csv rellenada."),
    ("Lo que nunca sale", "planillas_<anio>.csv, w2pr_<anio>.csv, la consulta final de SURI, la clave secreta del hash."),
    ("Regla de supresión", "Ninguna fila con menos de 10 planillas (colapsada en la contigua o vaciada, según la modalidad); ningún conteo parcial ni complemento entre 1 y 9; las celdas vacías de una columna son dos o más y suman 0 o al menos 10; no se redondea."),
    ("Revisión", "verificar_salidas.py comprueba las reglas sobre los archivos de salida y debe terminar con «sin incidencias»; después, la revisión propia de Hacienda."),
    ("Uso por Espacios Abiertos", "Calibrar y validar el modelo policyengine-pr y análisis de política pública; resultados publicados solo agregados, citando «Departamento de Hacienda, tabulaciones especiales, [año]»."),
    ("Contrapartida", "Espacios Abiertos entrega a Hacienda sin costo el modelo completo, su documentación y acceso a la herramienta de cálculo, y comparte con antelación cualquier informe que use estos datos. Puede formalizarse en un memorando de entendimiento o acuerdo de uso de datos."),
    ("Contacto", "Daniel Santamaría Ots — Espacios Abiertos — daniel@espaciosabiertos.org"),
]


def hoja_tabla(wb, ws, titulo, filas, anchos=None):
    ws["A1"] = titulo
    ws["A1"].font = TITULO
    for j, c in enumerate(filas[0], 1):
        cell = ws.cell(row=3, column=j, value=c)
        cell.font, cell.fill, cell.alignment = NEGRITA, CAB, AJUSTE
    for i, fila in enumerate(filas[1:], 4):
        for j, v in enumerate(fila, 1):
            ws.cell(row=i, column=j, value=v).alignment = AJUSTE
    for j, w in enumerate(anchos or [22] * len(filas[0]), 1):
        ws.column_dimensions[get_column_letter(j)].width = w
    ws.freeze_panes = "A4"


def main():
    wb = Workbook()
    ws = wb.active
    ws.title = "Léame"
    lineas = [
        ("Petición de datos al Departamento de Hacienda de Puerto Rico", TITULO),
        ("Proyecto policyengine-pr — modelo público de microsimulación contributiva de Puerto Rico — Espacios Abiertos", None),
        ("Borrador 2026-11-04 · Acompaña a la carta de solicitud y al paquete PE_Hacienda_Python", None),
        ("", None),
        ("La petición en un párrafo", NEGRITA),
        ("Hacienda construye, dentro del Departamento, un archivo con una fila por planilla del Formulario 482 y año contributivo (2021–2024) "
         "y, si es posible, otro con una fila por comprobante W-2PR; los valida y ejecuta el programa del paquete, que produce quince tablas "
         "agregadas ya protegidas con la regla de supresión (ninguna celda con menos de 10 planillas); las revisa y envía solo esas tablas. "
         "Los archivos de planillas nunca salen de Hacienda.", None),
        ("", None),
        ("Cómo se ejecuta el procedimiento (los pasos del paquete)", NEGRITA),
        ("Paso 0 · Prueba: Hacienda ejecuta el programa sobre los datos ficticios del paquete y comprueba que reproduce las salidas de referencia.", None),
        ("Paso 1 · Extracción: Hacienda escribe planillas_<anio>.csv (y w2pr_<anio>.csv) con la consulta de la plantilla SQL y documenta la extracción en la ficha.", None),
        ("Paso 2 · Validación: validar_entrada.py comprueba columnas, tipos, rangos y coherencia; debe dar 0 errores.", None),
        ("Paso 3 · Ejecución: pe_tabulaciones.py produce las tablas, el libro Excel y el registro, un año cada vez.", None),
        ("Paso 4 · Revisión: verificar_salidas.py comprueba la supresión; después la revisión propia de Hacienda.", None),
        ("Paso 5 · Entrega: las tablas, el registro, los informes y la ficha, por correo seguro.", None),
        ("", None),
        ("Hojas de este libro", NEGRITA),
        ("Solicitud: las seis peticiones (R1–R6).", None),
        ("Archivo de planillas / Archivo W-2PR: cada columna de los archivos de entrada, con tipo, definición, línea del Formulario 482 y si es necesaria.", None),
        ("Reglas del archivo: unidad, años, nombres, valores, formato, identificadores.", None),
        ("Tablas de salida: índice de las quince tablas; después, una hoja por tabla con la plantilla vacía (encabezados y etiquetas de fila).", None),
        ("Confidencialidad y entrega: qué sale, qué no, la regla de supresión y los compromisos de Espacios Abiertos.", None),
    ]
    for i, (t, f) in enumerate(lineas, 1):
        c = ws.cell(row=i, column=1, value=t)
        c.alignment = Alignment(wrap_text=True, vertical="top")
        if f:
            c.font = f
    ws.column_dimensions["A"].width = 130

    hoja_tabla(wb, wb.create_sheet("Solicitud"), "Lo que Espacios Abiertos pide a Hacienda",
               [("#", "Petición", "Qué exactamente", "Qué entrega Hacienda", "Notas")] + PETICIONES, [6, 34, 70, 45, 55])

    esq = pd.read_csv(PAQ / "02_contrato_y_parametros" / "esquema_planillas.csv", dtype=str).fillna("")
    filas = [("Columna (nombre en el CSV)", "Necesaria", "Tipo", "Rango", "Definición", "Fuente (Formulario 482 de 2025)", "Si falta")]
    filas += [(r.variable, r.obligatoria, r.tipo, f"{r.minimo}–{r.maximo}".strip("–"), r.descripcion, r.fuente_formulario_482_2025, r.si_falta)
              for r in esq.itertuples()]
    hoja_tabla(wb, wb.create_sheet("Archivo de planillas"), "El archivo de una fila por planilla: las 51 columnas", filas, [30, 10, 10, 12, 70, 32, 36])

    esq = pd.read_csv(PAQ / "02_contrato_y_parametros" / "esquema_w2pr.csv", dtype=str).fillna("")
    filas = [("Columna (nombre en el CSV)", "Necesaria", "Tipo", "Rango", "Definición", "Fuente", "Si falta")]
    filas += [(r.variable, r.obligatoria, r.tipo, f"{r.minimo}–{r.maximo}".strip("–"), r.descripcion, r.fuente, r.si_falta) for r in esq.itertuples()]
    hoja_tabla(wb, wb.create_sheet("Archivo W-2PR"), "El archivo de una fila por comprobante W-2PR (opcional): las 6 columnas", filas, [30, 10, 10, 12, 70, 32, 36])

    hoja_tabla(wb, wb.create_sheet("Reglas del archivo"), "Reglas de los archivos de entrada", [("Regla", "Detalle")] + REGLAS, [24, 120])
    hoja_tabla(wb, wb.create_sheet("Tablas de salida"), "Las quince tablas que produce el programa (una hoja por tabla a continuación)",
               [("Tabla", "Título", "Filas", "Columnas", "Línea del Formulario 482", "Para qué sirve")] + TABLAS, [8, 40, 45, 70, 26, 32])

    # Una hoja por tabla: plantilla vacía a partir de las salidas de referencia (modalidad vaciar, que conserva todas las filas)
    for clave, titulo, *_ in TABLAS:
        ruta = REF / ("tabla_0_control.csv" if clave == "0" else f"tabla_{clave}.csv")
        t = pd.read_csv(ruta, dtype={"nota": str})
        ws = wb.create_sheet(f"T_{clave}")
        ws["A1"] = f"Tabla {clave} — {titulo} — plantilla vacía (año contributivo ____)"
        ws["A1"].font = TITULO
        for j, c in enumerate(t.columns, 1):
            cell = ws.cell(row=3, column=j, value=c)
            cell.font, cell.fill, cell.alignment = NEGRITA, CAB, AJUSTE
            ws.column_dimensions[get_column_letter(j)].width = max(12, min(26, len(str(c)) + 2))
        texto = [c for c in t.columns if not pd.api.types.is_numeric_dtype(t[c]) and c not in ("nota", "supr")]
        for i, fila in enumerate(t.itertuples(index=False), 4):
            d = dict(zip(t.columns, fila))
            for j, c in enumerate(t.columns, 1):
                v = d[c] if c in texto and not (isinstance(d[c], float) and pd.isna(d[c])) else None
                cell = ws.cell(row=i, column=j, value=v)
                if c not in texto:
                    cell.fill = GRIS
                if isinstance(v, str) and v.startswith("Total"):
                    cell.font = NEGRITA
        ws.freeze_panes = "A4"

    hoja_tabla(wb, wb.create_sheet("Confidencialidad y entrega"), "Confidencialidad y entrega", [("Asunto", "Detalle")] + ENTREGA, [26, 130])
    wb.save(SALIDA)
    print("Escrito", SALIDA)


if __name__ == "__main__":
    main()
