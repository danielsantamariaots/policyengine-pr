#!/usr/bin/env python3
"""
Tabulaciones estadísticas del Formulario 482 para el proyecto policyengine-pr
(Espacios Abiertos). Guion para ejecutarse DENTRO del Departamento de Hacienda.

Qué hace
--------
1. Lee los microdatos de planillas de un año contributivo (un archivo CSV,
   Parquet o Excel) y, opcionalmente, el archivo de comprobantes W-2PR.
2. Produce las Tablas A a J descritas en la carta de solicitud.
3. Aplica la regla de supresión de Hacienda: toda fila con menos de
   MIN_PLANILLAS (10) planillas se COLAPSA con la fila contigua (el tramo
   inmediatamente inferior) en lugar de eliminarse; la fila resultante se
   identifica con el tramo combinado y se marca con "c" en la columna "nota".
   Las filas de totales se conservan siempre.
4. Escribe un libro Excel por año (una hoja por tabla, más "Léame" y
   "Diccionario") y un CSV por tabla.

Ningún microdato sale del guion: solo se escriben sumas y conteos, ya
suprimidos. Hacienda puede revisar el código completo antes de ejecutarlo.

Cómo usarlo
-----------
    # 1. Ajuste la sección CONFIGURACIÓN (rutas y nombres de columnas).
    # 2. Ejecute, por ejemplo:
    python tabulaciones_hacienda.py --anio 2023 --planillas planillas_2023.csv \
        --w2pr w2pr_2023.csv --salida ./salida

    # Prueba sin datos reales (genera microdatos sintéticos):
    python tabulaciones_hacienda.py --anio 2023 --sintetico --salida ./salida

Requisitos: Python 3.9+, pandas, numpy, openpyxl (pip install pandas openpyxl).
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "1.0 (2026-11-04)"

# =========================================================================
# CONFIGURACIÓN — lo único que Hacienda debería tener que modificar
# =========================================================================

MIN_PLANILLAS = 10  # regla de supresión: filas con menos de esto se colapsan

# Correspondencia entre las columnas del archivo de Hacienda y los nombres
# que usa este guion. Clave: nombre interno; valor: nombre de la columna en el
# archivo de Hacienda. Si una columna no existe, déjela en None y la tabla
# correspondiente se omitirá o se rellenará con ceros (se indica en "Léame").
# Entre paréntesis, la línea del Formulario 482 de 2025.
COLUMNAS_PLANILLAS = {
    # identificación y demografía
    "estado_personal": "estado_personal",  # 1 individual, 2 conjunta, 3 separada, 4 cómputo opcional
    "edad": "edad",  # del contribuyente principal al cierre del año
    "municipio": "municipio",  # nombre o código del municipio de residencia
    # ingresos (Parte 1)
    "salarios": "salarios",  # 1A–1C
    "intereses_dividendos": "intereses_dividendos",  # 2C, 2D
    "pensiones": "pensiones",  # 2H
    "distribuciones_retiro": "distribuciones_retiro",  # 2E, 2F, 2L
    "ganancia_capital": "ganancia_capital",  # 2B
    "entidades_conducto": "entidades_conducto",  # 2K
    "industria_negocio": "industria_negocio",  # 2P–2T
    "pension_divorcio": "pension_divorcio",  # 4
    "iba": "iba",  # 5 ingreso bruto ajustado
    # deducciones y exenciones
    "deducciones": "deducciones",  # 6
    "exencion_personal": "exencion_personal",  # 7
    "exencion_dependientes": "exencion_dependientes",  # 8
    "num_dependientes": "num_dependientes",  # 8 (número)
    "exencion_veterano": "exencion_veterano",  # 9
    "ingreso_neto": "ingreso_neto",  # 13
    # cómputo de la contribución
    "contribucion_tabla": "contribucion_tabla",  # 14
    "ajuste_gradual": "ajuste_gradual",  # 15
    "factor": "factor",  # 0.92 o 0.95 (Sección 1021.01(c))
    "ingreso_bruto_factor": "ingreso_bruto_factor",  # ingreso bruto usado para el umbral de $100,000
    "contribucion_regular": "contribucion_regular",  # 17
    "credito_otras_jurisdicciones": "credito_otras_jurisdicciones",  # 18
    "exceso_cba": "exceso_cba",  # 20
    "credito_cba": "credito_cba",  # 21
    "creditos_anejo_b": "creditos_anejo_b",  # 25
    "responsabilidad": "responsabilidad",  # 26
    "retenida_salarios": "retenida_salarios",  # 27A
    "credito_trabajo": "credito_trabajo",  # 27C
    "creditos_federales": "creditos_federales",  # 27D
    "sobrepago": "sobrepago",  # 29
    "balance_pendiente": "balance_pendiente",  # 31
    # Anejo A
    "ded_hipoteca": "ded_hipoteca",  # A-1i
    "ded_medicos": "ded_medicos",  # A-3
    "ded_donativos": "ded_donativos",  # A-4
    "ded_ira": "ded_ira",  # A-7b
    "ded_educativa": "ded_educativa",  # A-8b
    "ded_prestamos": "ded_prestamos",  # A-9b
    "ded_total": "ded_total",  # A-11
    # Anejo IE
    "exento_pension": "exento_pension",  # 1031.02(a)(13)
    "exento_jovenes": "exento_jovenes",  # IE-31, Ley 135-2014
    "exento_dificil_reclutamiento": "exento_dificil_reclutamiento",  # IE-32
    "exento_total": "exento_total",  # IE-45
    # Anejo CT
    "ct_dependientes": "ct_dependientes",  # número de dependientes cualificados
    "ct_ingreso_ganado": "ct_ingreso_ganado",  # CT Parte II línea 3
    "ct_reclamado": "ct_reclamado",  # cantidad reclamada por el contribuyente
    "ct_ajustado": "ct_ajustado",  # 1 si Hacienda denegó o ajustó el crédito
    # Anejo O
    "cba_ingreso_neto": "cba_ingreso_neto",  # ingreso neto sujeto a CBA
    "cba_contribucion": "cba_contribucion",  # contribución básica alterna
}

# Archivo de comprobantes W-2PR (un registro por comprobante).
COLUMNAS_W2PR = {
    "id_persona": "id_persona",  # cualquier identificador consistente; solo se cuentan distintos
    "salarios": "salarios",
    "retenida": "retenida",
    "exento_135": "exento_135",  # encasillado 16, código E
    "edad": "edad",
}

ETIQUETA_ESTADO = {
    1: "Individual",
    2: "Casado, planilla conjunta",
    3: "Casado, planilla separada",
    4: "Cómputo opcional de casados",
}


def etiqueta_estado(serie):
    """Estado personal como categoría ordenada (1 a 4)."""
    valores = serie.map(ETIQUETA_ESTADO).fillna("Otro")
    categorias = list(ETIQUETA_ESTADO.values()) + (
        ["Otro"] if (valores == "Otro").any() else []
    )
    return pd.Categorical(valores, categorias, ordered=True)


# Tramos de ingreso bruto ajustado (Tabla A y otras). Límite superior incluido.
TRAMOS_IBA = [
    (-np.inf, 0, "$0 o menos"),
    (0, 10_000, "$1 – $10,000"),
    (10_000, 15_000, "$10,001 – $15,000"),
    (15_000, 20_000, "$15,001 – $20,000"),
    (20_000, 25_000, "$20,001 – $25,000"),
    (25_000, 30_000, "$25,001 – $30,000"),
    (30_000, 40_000, "$30,001 – $40,000"),
    (40_000, 50_000, "$40,001 – $50,000"),
    (50_000, 60_000, "$50,001 – $60,000"),
    (60_000, 75_000, "$60,001 – $75,000"),
    (75_000, 100_000, "$75,001 – $100,000"),
    (100_000, 150_000, "$100,001 – $150,000"),
    (150_000, 250_000, "$150,001 – $250,000"),
    (250_000, 500_000, "$250,001 – $500,000"),
    (500_000, np.inf, "$500,001 o más"),
]

# =========================================================================
# Utilidades
# =========================================================================


def tramos_regulares(inicio, fin, paso, etiqueta_final=None):
    """Tramos de ancho fijo (límite superior incluido), p. ej. $0–$2,500."""
    tramos, lo = [], inicio
    while lo < fin:
        hi = min(lo + paso, fin)
        tramos.append((lo, hi, f"${lo:,.0f} – ${hi:,.0f}"))
        lo = hi
    if etiqueta_final:
        tramos.append((fin, np.inf, etiqueta_final))
    return tramos


def asignar_tramo(valores, tramos):
    """Devuelve una Categorical ordenada con la etiqueta del tramo de cada valor."""
    etiquetas = [t[2] for t in tramos]
    bordes = [tramos[0][0]] + [t[1] for t in tramos]
    cat = pd.cut(
        pd.to_numeric(valores, errors="coerce"),
        bins=bordes,
        labels=etiquetas,
        right=True,
        include_lowest=True,
    )
    return cat


def agregar(df, filas, columnas_suma, columnas_conteo=None, col_n="planillas"):
    """Suma y cuenta por `filas` (lista de columnas). Devuelve un DataFrame
    con columna `col_n` (conteo de registros) seguida de las sumas.

    `columnas_conteo`: {nombre_salida: columna} que cuenta registros con la
    columna > 0 (p. ej. "planillas con deducción").
    """
    g = df.groupby(filas, observed=False, dropna=False)
    out = g.size().rename(col_n).to_frame()
    for salida, col in (columnas_conteo or {}).items():
        out[salida] = g[col].apply(lambda s: int((s > 0).sum()))
    for col in columnas_suma:
        out[col] = g[col].sum()
    return out.reset_index()


def suprimir(
    tabla, col_n="planillas", grupo=None, orden=None, minimo=MIN_PLANILLAS
):
    """Aplica la regla de supresión colapsando filas.

    Recorre las filas en el orden dado (dentro de cada `grupo`, si lo hay).
    Toda fila con menos de `minimo` en `col_n` se suma a la fila anterior
    (el tramo inferior); si es la primera fila, a la siguiente. Se repite
    hasta que ninguna fila quede por debajo del mínimo. La etiqueta de la
    fila resultante une la primera y la última etiqueta colapsadas; la
    columna "nota" lleva "c" en las filas colapsadas.
    """
    tabla = tabla.copy()
    tabla["nota"] = ""
    etiqueta = orden
    numericas = [
        c
        for c in tabla.columns
        if c not in (etiqueta, "nota") and (grupo is None or c != grupo)
    ]
    numericas = [
        c for c in numericas if pd.api.types.is_numeric_dtype(tabla[c])
    ]

    def colapsar(bloque):
        filas = bloque.to_dict("records")
        cambiado = True
        while cambiado and len(filas) > 1:
            cambiado = False
            for i, f in enumerate(filas):
                if f[col_n] < minimo:
                    j = i - 1 if i > 0 else i + 1
                    destino = filas[j]
                    for c in numericas:
                        destino[c] = destino[c] + f[c]
                    lo, hi = (destino, f) if j < i else (f, destino)
                    destino[etiqueta] = _unir_etiquetas(
                        lo[etiqueta], hi[etiqueta]
                    )
                    destino["nota"] = "c"
                    del filas[i]
                    cambiado = True
                    break
        return pd.DataFrame(filas)

    if grupo is None:
        return colapsar(tabla)
    partes = [
        colapsar(b)
        for _, b in tabla.groupby(grupo, observed=False, sort=False)
    ]
    return pd.concat(partes, ignore_index=True)


def _unir_etiquetas(a, b):
    """'$10,001 – $15,000' + '$15,001 – $20,000' -> '$10,001 – $20,000'."""
    a, b = str(a), str(b)
    if "–" in a and "–" in b:
        return f"{a.split('–')[0].strip()} – {b.split('–')[-1].strip()}"
    if "–" in a and ("o más" in b):
        return f"{a.split('–')[0].strip()} o más"
    if ("o menos" in a) and "–" in b:
        return f"{b.split('–')[-1].strip()} o menos"
    return f"{a} + {b}"


def con_totales(tabla, etiqueta, grupo=None, texto="Total"):
    """Añade una fila de totales (por grupo si lo hay) y un total general."""
    numericas = [
        c for c in tabla.columns if pd.api.types.is_numeric_dtype(tabla[c])
    ]
    partes = []
    if grupo is not None:
        for g, b in tabla.groupby(grupo, observed=False, sort=False):
            t = b[numericas].sum().to_frame().T
            t[grupo], t[etiqueta], t["nota"] = g, texto, ""
            partes += [b, t]
        tabla = pd.concat(partes, ignore_index=True)
    total = tabla[tabla[etiqueta] != texto][numericas].sum().to_frame().T
    total[etiqueta] = "Total general" if grupo is not None else texto
    total["nota"] = ""
    if grupo is not None:
        total[grupo] = ""
    return pd.concat([tabla, total], ignore_index=True)


def ordenar_columnas(tabla, primeras):
    resto = [c for c in tabla.columns if c not in primeras and c != "nota"]
    return tabla[
        [c for c in primeras if c in tabla.columns] + resto + ["nota"]
    ]


# =========================================================================
# Carga de datos
# =========================================================================


def leer(path):
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path)
    return pd.read_csv(path, low_memory=False)


def normalizar(df, mapa, faltantes):
    """Renombra columnas al nombre interno; las que faltan se crean con 0."""
    out = pd.DataFrame(index=df.index)
    for interno, externo in mapa.items():
        if externo is not None and externo in df.columns:
            out[interno] = df[externo]
        else:
            faltantes.append(interno)
            out[interno] = 0
    for c in out.columns:
        if c not in ("municipio", "id_persona"):
            out[c] = pd.to_numeric(out[c], errors="coerce").fillna(0)
    return out


# =========================================================================
# Datos sintéticos (solo para probar el guion; NO son datos de Hacienda)
# =========================================================================


def datos_sinteticos(n=60_000, semilla=482):
    rng = np.random.default_rng(semilla)
    estado = rng.choice([1, 2, 3, 4], size=n, p=[0.62, 0.30, 0.03, 0.05])
    edad = np.clip(rng.normal(44, 15, n), 16, 95).astype(int)
    salarios = np.where(
        rng.random(n) < 0.85, np.exp(rng.normal(10.1, 0.85, n)), 0
    ).round()
    negocio = np.where(
        rng.random(n) < 0.12, np.exp(rng.normal(9.3, 1.1, n)), 0
    ).round()
    pensiones = np.where(
        (edad >= 55) & (rng.random(n) < 0.4),
        np.exp(rng.normal(9.6, 0.6, n)),
        0,
    ).round()
    intereses = np.where(
        rng.random(n) < 0.25, np.exp(rng.normal(5.5, 1.5, n)), 0
    ).round()
    ganancia = np.where(
        rng.random(n) < 0.04, np.exp(rng.normal(8.5, 1.6, n)), 0
    ).round()
    conducto = np.where(
        rng.random(n) < 0.03, np.exp(rng.normal(10.5, 1.3, n)), 0
    ).round()
    retiro = np.where(
        rng.random(n) < 0.06, np.exp(rng.normal(8.8, 1.0, n)), 0
    ).round()
    divorcio = np.where(rng.random(n) < 0.004, 6_000.0, 0)

    exento_jovenes = np.where(
        (edad >= 16) & (edad <= 26), np.minimum(salarios, 40_000), 0
    )
    exento_pension = np.minimum(
        pensiones, np.where(edad >= 60, 15_000, 11_000)
    )
    exento_dificil = np.where(rng.random(n) < 0.002, salarios, 0)
    salarios_trib = salarios - exento_jovenes - exento_dificil
    pensiones_trib = pensiones - exento_pension
    exento_total = exento_jovenes + exento_pension + exento_dificil

    iba = (
        salarios_trib
        + negocio
        + pensiones_trib
        + intereses
        + ganancia
        + conducto
        + retiro
        - divorcio
    ).round()
    ingreso_bruto_factor = (
        salarios
        + negocio
        + pensiones
        + intereses
        + ganancia
        + conducto
        + retiro
    )

    ded_hip = np.where(
        rng.random(n) < 0.22,
        np.minimum(np.exp(rng.normal(8.6, 0.6, n)), 35_000),
        0,
    ).round()
    ded_med = np.where(
        rng.random(n) < 0.05, np.exp(rng.normal(7.5, 0.8, n)), 0
    ).round()
    ded_don = np.where(
        rng.random(n) < 0.15, np.exp(rng.normal(6.0, 1.0, n)), 0
    ).round()
    ded_ira = np.where(
        rng.random(n) < 0.08, rng.choice([2_000, 5_000, 7_000], n), 0
    )
    ded_edu = np.where(rng.random(n) < 0.02, 1_000, 0)
    ded_pres = np.where(
        rng.random(n) < 0.06, np.exp(rng.normal(7.0, 0.7, n)), 0
    ).round()
    ded_total = ded_hip + ded_med + ded_don + ded_ira + ded_edu + ded_pres

    num_dep = np.where(
        estado == 2,
        rng.choice([0, 1, 2, 3, 4], n, p=[0.35, 0.3, 0.22, 0.09, 0.04]),
        rng.choice([0, 1, 2, 3, 4], n, p=[0.7, 0.18, 0.08, 0.03, 0.01]),
    )
    ex_pers = np.where(estado == 2, 7_000, 3_500)
    ex_dep = num_dep * 2_500
    veterano = np.where(rng.random(n) < 0.04, 1_500, 0)
    ingreso_neto = np.maximum(iba - ded_total - ex_pers - ex_dep - veterano, 0)

    def tabla(x):
        return np.select(
            [x <= 9_000, x <= 25_000, x <= 41_500, x <= 61_500],
            [
                0,
                0.07 * (x - 9_000),
                1_120 + 0.14 * (x - 25_000),
                3_430 + 0.25 * (x - 41_500),
            ],
            8_430 + 0.33 * (x - 61_500),
        )

    contrib_tabla = tabla(ingreso_neto).round()
    ajuste = np.where(
        ingreso_neto > 500_000,
        np.minimum(
            0.05 * (ingreso_neto - 500_000),
            8_895 + 0.33 * (ex_pers + ex_dep + veterano),
        ),
        0,
    ).round()
    factor = np.where(ingreso_bruto_factor <= 100_000, 0.92, 0.95)
    contrib_regular = ((contrib_tabla + ajuste) * factor).round()
    cba_base = np.where(
        ingreso_neto > 25_000, negocio + pensiones_trib + intereses, 0
    )
    cba_rate = np.select(
        [
            cba_base <= 25_000,
            cba_base <= 50_000,
            cba_base <= 75_000,
            cba_base <= 150_000,
            cba_base <= 250_000,
        ],
        [0, 0.01, 0.03, 0.05, 0.10],
        0.24,
    )
    cba = (cba_base * cba_rate).round()
    exceso_cba = np.maximum(cba - contrib_regular, 0)
    credito_cba = np.where(rng.random(n) < 0.01, 200.0, 0)
    anejo_b = np.where(
        rng.random(n) < 0.015, np.exp(rng.normal(7.5, 1.0, n)), 0
    ).round()
    otras_jur = np.where(
        rng.random(n) < 0.01, np.exp(rng.normal(6.5, 1.0, n)), 0
    ).round()
    responsabilidad = np.maximum(
        contrib_regular + exceso_cba - otras_jur - credito_cba - anejo_b, 0
    )
    retenida = np.where(
        salarios > 0,
        np.minimum(contrib_regular * rng.uniform(0.7, 1.3, n), salarios * 0.3),
        0,
    ).round()

    # Crédito por Trabajo (aproximación de las cuatro tablas de BI RI 26-01)
    ct_dep = np.minimum(num_dep, 3)
    ganado = salarios + np.maximum(negocio, 0) + pensiones_trib
    ct_max = np.select(
        [ct_dep == 0, ct_dep == 1, ct_dep == 2], [1_656, 4_600, 6_900], 7_200
    )
    ct_in = np.select(
        [ct_dep == 0, ct_dep == 1, ct_dep == 2], [0.0828, 0.2, 0.3], 0.3
    )
    ct_po = np.select(
        [ct_dep == 0, ct_dep == 1, ct_dep == 2], [0.0828, 0.2, 0.3], 0.3
    )
    ct_start = np.where(
        estado == 2,
        np.select(
            [ct_dep == 0, ct_dep == 1, ct_dep == 2],
            [26_000, 37_000, 44_000],
            44_000,
        ),
        np.select(
            [ct_dep == 0, ct_dep == 1, ct_dep == 2],
            [20_000, 31_000, 38_000],
            38_000,
        ),
    )
    ct = np.where(
        ganado < ct_start,
        np.minimum(ct_in * ganado, ct_max),
        np.maximum(ct_max - ct_po * (ganado - ct_start), 0),
    ).round()
    ct = np.where(
        (edad >= 19) & (intereses + ganancia <= 10_000) & (estado != 3), ct, 0
    )
    ct_ajustado = (ct > 0) & (rng.random(n) < 0.03)
    ct_reclamado = np.where(
        ct_ajustado, ct * rng.uniform(1.05, 1.6, n), ct
    ).round()
    creditos_fed = np.where(
        (num_dep > 0) & (salarios > 0),
        np.minimum(1_700 * np.minimum(num_dep, 3), salarios * 0.0765),
        0,
    ).round()
    pago = retenida + ct + creditos_fed - responsabilidad
    municipios = [f"Municipio {i:02d}" for i in range(1, 79)]
    pesos = rng.pareto(1.2, 78) + 0.3
    municipio = rng.choice(municipios, n, p=pesos / pesos.sum())

    return pd.DataFrame(
        {
            "estado_personal": estado,
            "edad": edad,
            "municipio": municipio,
            "salarios": salarios,
            "intereses_dividendos": intereses,
            "pensiones": pensiones,
            "distribuciones_retiro": retiro,
            "ganancia_capital": ganancia,
            "entidades_conducto": conducto,
            "industria_negocio": negocio,
            "pension_divorcio": divorcio,
            "iba": iba,
            "deducciones": ded_total,
            "exencion_personal": ex_pers,
            "exencion_dependientes": ex_dep,
            "num_dependientes": num_dep,
            "exencion_veterano": veterano,
            "ingreso_neto": ingreso_neto,
            "contribucion_tabla": contrib_tabla,
            "ajuste_gradual": ajuste,
            "factor": factor,
            "ingreso_bruto_factor": ingreso_bruto_factor,
            "contribucion_regular": contrib_regular,
            "credito_otras_jurisdicciones": otras_jur,
            "exceso_cba": exceso_cba,
            "credito_cba": credito_cba,
            "creditos_anejo_b": anejo_b,
            "responsabilidad": responsabilidad,
            "retenida_salarios": retenida,
            "credito_trabajo": ct,
            "creditos_federales": creditos_fed,
            "sobrepago": np.maximum(pago, 0),
            "balance_pendiente": np.maximum(-pago, 0),
            "ded_hipoteca": ded_hip,
            "ded_medicos": ded_med,
            "ded_donativos": ded_don,
            "ded_ira": ded_ira,
            "ded_educativa": ded_edu,
            "ded_prestamos": ded_pres,
            "ded_total": ded_total,
            "exento_pension": exento_pension,
            "exento_jovenes": exento_jovenes,
            "exento_dificil_reclutamiento": exento_dificil,
            "exento_total": exento_total,
            "ct_dependientes": ct_dep,
            "ct_ingreso_ganado": np.where(ct > 0, ganado, 0),
            "ct_reclamado": ct_reclamado,
            "ct_ajustado": ct_ajustado.astype(int),
            "cba_ingreso_neto": cba_base,
            "cba_contribucion": cba,
        }
    )


def w2pr_sintetico(n=90_000, semilla=499):
    rng = np.random.default_rng(semilla)
    personas = rng.integers(1, 70_000, n)
    edad = np.clip(rng.normal(40, 14, n), 16, 80).astype(int)
    salarios = np.exp(rng.normal(9.7, 0.9, n)).round()
    exento = np.where(
        (edad <= 26) & (rng.random(n) < 0.8), np.minimum(salarios, 40_000), 0
    )
    retenida = np.where(
        salarios - exento > 15_000,
        (salarios - exento) * rng.uniform(0.03, 0.12, n),
        0,
    ).round()
    return pd.DataFrame(
        {
            "id_persona": personas,
            "salarios": salarios,
            "retenida": retenida,
            "exento_135": exento,
            "edad": edad,
        }
    )


# =========================================================================
# Tablas
# =========================================================================

CAMPOS_A = [
    "salarios",
    "intereses_dividendos",
    "pensiones",
    "distribuciones_retiro",
    "ganancia_capital",
    "entidades_conducto",
    "industria_negocio",
    "pension_divorcio",
    "iba",
    "deducciones",
    "exencion_personal",
    "exencion_dependientes",
    "num_dependientes",
    "exencion_veterano",
    "ingreso_neto",
    "contribucion_tabla",
    "ajuste_gradual",
    "contribucion_regular",
    "credito_otras_jurisdicciones",
    "exceso_cba",
    "credito_cba",
    "creditos_anejo_b",
    "responsabilidad",
    "retenida_salarios",
    "credito_trabajo",
    "creditos_federales",
    "sobrepago",
    "balance_pendiente",
]


def tabla_a(df):
    d = df.assign(
        tramo_iba=asignar_tramo(df["iba"], TRAMOS_IBA),
        estado=etiqueta_estado(df["estado_personal"]),
        planillas_92=(df["factor"] < 0.935).astype(int),
        planillas_95=(df["factor"] >= 0.935).astype(int),
        contribucion_regular_92=np.where(
            df["factor"] < 0.935, df["contribucion_regular"], 0
        ),
        contribucion_regular_95=np.where(
            df["factor"] >= 0.935, df["contribucion_regular"], 0
        ),
    )
    campos = CAMPOS_A + [
        "planillas_92",
        "contribucion_regular_92",
        "planillas_95",
        "contribucion_regular_95",
    ]
    t = agregar(
        d,
        ["estado", "tramo_iba"],
        campos,
        {
            "planillas_con_dependientes": "num_dependientes",
            "planillas_credito_trabajo": "credito_trabajo",
        },
    )
    t = suprimir(t, grupo="estado", orden="tramo_iba")
    t = con_totales(t, "tramo_iba", grupo="estado")
    return ordenar_columnas(t, ["estado", "tramo_iba", "planillas"])


def tabla_b(df):
    d = df.assign(tramo_iba=asignar_tramo(df["iba"], TRAMOS_IBA))
    campos = [
        "ded_hipoteca",
        "ded_medicos",
        "ded_donativos",
        "ded_ira",
        "ded_educativa",
        "ded_prestamos",
        "ded_total",
    ]
    t = agregar(
        d, ["tramo_iba"], campos, {f"planillas_{c[4:]}": c for c in campos}
    )
    t = suprimir(t, orden="tramo_iba")
    return ordenar_columnas(
        con_totales(t, "tramo_iba"), ["tramo_iba", "planillas"]
    )


def tabla_c(df):
    d = df.assign(
        tramo_iba=asignar_tramo(df["iba"] + df["exento_total"], TRAMOS_IBA)
    )
    campos = [
        "exento_pension",
        "exento_jovenes",
        "exento_dificil_reclutamiento",
        "exento_total",
    ]
    t = agregar(
        d, ["tramo_iba"], campos, {f"planillas_{c[7:]}": c for c in campos}
    )
    t = suprimir(t, orden="tramo_iba")
    return ordenar_columnas(
        con_totales(t, "tramo_iba"), ["tramo_iba", "planillas"]
    )


def _dependientes_ct(df):
    return pd.Categorical(
        np.minimum(df["ct_dependientes"], 3).map(
            {0: "0", 1: "1", 2: "2", 3: "3 o más"}
        ),
        ["0", "1", "2", "3 o más"],
        ordered=True,
    )


def tabla_d1(df):
    d = df[df["credito_trabajo"] > 0]
    d = d.assign(
        dependientes=_dependientes_ct(d),
        estado=etiqueta_estado(d["estado_personal"]),
    )
    t = agregar(
        d, ["estado", "dependientes"], ["credito_trabajo", "ct_ingreso_ganado"]
    )
    t = suprimir(t, grupo="estado", orden="dependientes")
    return ordenar_columnas(
        con_totales(t, "dependientes", grupo="estado"),
        ["estado", "dependientes", "planillas"],
    )


def tabla_d2(df):
    d = df[df["credito_trabajo"] > 0]
    tramos = tramos_regulares(0, 55_000, 2_500, "$55,001 o más")
    d = d.assign(
        dependientes=_dependientes_ct(d),
        tramo_ingreso_ganado=asignar_tramo(d["ct_ingreso_ganado"], tramos),
    )
    t = agregar(
        d, ["dependientes", "tramo_ingreso_ganado"], ["credito_trabajo"]
    )
    t = suprimir(t, grupo="dependientes", orden="tramo_ingreso_ganado")
    return ordenar_columnas(
        con_totales(t, "tramo_ingreso_ganado", grupo="dependientes"),
        ["dependientes", "tramo_ingreso_ganado", "planillas"],
    )


def tabla_d3(df):
    d = df[df["ct_ajustado"] > 0]
    d = d.assign(
        dependientes=_dependientes_ct(d),
        ajuste=d["ct_reclamado"] - d["credito_trabajo"],
    )
    t = agregar(
        d, ["dependientes"], ["ct_reclamado", "credito_trabajo", "ajuste"]
    )
    t = t.rename(
        columns={
            "planillas": "planillas_ajustadas",
            "credito_trabajo": "credito_concedido",
        }
    )
    t = suprimir(t, col_n="planillas_ajustadas", orden="dependientes")
    return ordenar_columnas(
        con_totales(t, "dependientes"), ["dependientes", "planillas_ajustadas"]
    )


def tabla_e(df):
    d = df[(df["exento_jovenes"] > 0) & df["edad"].between(16, 26)]
    d = d.assign(
        edad=d["edad"].astype(int).astype(str),
        contribucion_determinada=d["responsabilidad"],
    )
    t = agregar(
        d,
        ["edad"],
        [
            "exento_jovenes",
            "salarios",
            "industria_negocio",
            "contribucion_determinada",
        ],
    )
    t = t.sort_values("edad", key=lambda s: s.astype(int))
    t = suprimir(t, orden="edad")
    return ordenar_columnas(con_totales(t, "edad"), ["edad", "planillas"])


def tabla_f(df):
    d = df[df["ingreso_bruto_factor"].between(90_000, 110_000)]
    tramos = tramos_regulares(90_000, 110_000, 2_000)
    d = d.assign(
        tramo_ingreso_bruto=asignar_tramo(d["ingreso_bruto_factor"], tramos),
        planillas_92=(d["factor"] < 0.935).astype(int),
        planillas_95=(d["factor"] >= 0.935).astype(int),
        contribucion_regular_92=np.where(
            d["factor"] < 0.935, d["contribucion_regular"], 0
        ),
        contribucion_regular_95=np.where(
            d["factor"] >= 0.935, d["contribucion_regular"], 0
        ),
    )
    t = agregar(
        d,
        ["tramo_ingreso_bruto"],
        [
            "planillas_92",
            "contribucion_regular_92",
            "planillas_95",
            "contribucion_regular_95",
        ],
    )
    t = suprimir(t, orden="tramo_ingreso_bruto")
    return ordenar_columnas(
        con_totales(t, "tramo_ingreso_bruto"),
        ["tramo_ingreso_bruto", "planillas"],
    )


def tabla_g1(df):
    d = df[df["ingreso_neto"] > 500_000]
    d = d.assign(estado=etiqueta_estado(d["estado_personal"]))
    t = agregar(d, ["estado"], ["ingreso_neto", "ajuste_gradual"])
    t = suprimir(t, orden="estado")
    return ordenar_columnas(con_totales(t, "estado"), ["estado", "planillas"])


def tabla_g2(df):
    d = df[df["cba_contribucion"] > 0]
    tramos = [
        (-np.inf, 50_000, "Hasta $50,000"),
        (50_000, 75_000, "$50,001 – $75,000"),
        (75_000, 150_000, "$75,001 – $150,000"),
        (150_000, 250_000, "$150,001 – $250,000"),
        (250_000, np.inf, "$250,001 o más"),
    ]
    d = d.assign(tramo_cba=asignar_tramo(d["cba_ingreso_neto"], tramos))
    t = agregar(
        d,
        ["tramo_cba"],
        ["cba_ingreso_neto", "cba_contribucion", "exceso_cba"],
    )
    t = suprimir(t, orden="tramo_cba")
    return ordenar_columnas(
        con_totales(t, "tramo_cba"), ["tramo_cba", "planillas"]
    )


def tabla_h(df):
    d = df.assign(
        dependientes=pd.Categorical(
            np.minimum(df["num_dependientes"], 4).map(
                {0: "0", 1: "1", 2: "2", 3: "3", 4: "4 o más"}
            ),
            ["0", "1", "2", "3", "4 o más"],
            ordered=True,
        ),
        estado=etiqueta_estado(df["estado_personal"]),
    )
    t = agregar(
        d,
        ["estado", "dependientes"],
        ["exencion_dependientes", "credito_trabajo", "creditos_federales"],
    )
    t = suprimir(t, grupo="estado", orden="dependientes")
    return ordenar_columnas(
        con_totales(t, "dependientes", grupo="estado"),
        ["estado", "dependientes", "planillas"],
    )


def tabla_i(w2, por_edad=False):
    tramos = tramos_regulares(0, 50_000, 2_500) + TRAMOS_IBA[8:]
    d = w2.assign(tramo_salarios=asignar_tramo(w2["salarios"], tramos))
    filas = ["tramo_salarios"]
    if por_edad:
        edades = [
            (15, 25, "16 – 25"),
            (25, 35, "26 – 35"),
            (35, 50, "36 – 50"),
            (50, 64, "51 – 64"),
            (64, np.inf, "65 o más"),
        ]
        d = d.assign(grupo_edad=asignar_tramo(d["edad"], edades))
        filas = ["grupo_edad", "tramo_salarios"]
    g = d.groupby(filas, observed=False)
    t = g.size().rename("comprobantes").to_frame()
    t["personas_distintas"] = g["id_persona"].nunique()
    for c in ["salarios", "retenida", "exento_135"]:
        t[c] = g[c].sum()
    t = t.reset_index()
    t = suprimir(
        t,
        col_n="comprobantes",
        grupo="grupo_edad" if por_edad else None,
        orden="tramo_salarios",
    )
    t = con_totales(
        t, "tramo_salarios", grupo="grupo_edad" if por_edad else None
    )
    return ordenar_columnas(t, filas + ["comprobantes", "personas_distintas"])


def tabla_j(df):
    t = agregar(
        df,
        ["municipio"],
        ["iba", "responsabilidad", "credito_trabajo"],
        {"planillas_credito_trabajo": "credito_trabajo"},
    )
    t = t.rename(columns={"responsabilidad": "contribucion_determinada"})
    t = t.sort_values("planillas", ascending=False).reset_index(drop=True)
    # colapso con el municipio contiguo de menor población = el siguiente en la lista ordenada
    t = suprimir(t, orden="municipio")
    return ordenar_columnas(
        con_totales(t, "municipio"), ["municipio", "planillas"]
    )


TABLAS = [
    ("A", "Resumen por tramo de IBA y estado personal", tabla_a, "planillas"),
    ("B", "Deducciones del Anejo A por tramo de IBA", tabla_b, "planillas"),
    (
        "C",
        "Ingresos exentos del Anejo IE por tramo de IBA",
        tabla_c,
        "planillas",
    ),
    (
        "D1",
        "Crédito por Trabajo por dependientes y estado personal",
        tabla_d1,
        "planillas",
    ),
    (
        "D2",
        "Crédito por Trabajo por tramo de ingreso ganado",
        tabla_d2,
        "planillas",
    ),
    ("D3", "Crédito por Trabajo denegado o ajustado", tabla_d3, "planillas"),
    (
        "E",
        "Exención para jóvenes (Ley 135-2014) por edad",
        tabla_e,
        "planillas",
    ),
    ("F", "Umbral de $100,000 del factor 92%/95%", tabla_f, "planillas"),
    ("G1", "Ajuste gradual (ingreso neto > $500,000)", tabla_g1, "planillas"),
    ("G2", "Contribución básica alterna (Anejo O)", tabla_g2, "planillas"),
    ("H", "Dependientes reclamados", tabla_h, "planillas"),
    ("I", "Comprobantes W-2PR por tramo de salarios", tabla_i, "w2pr"),
    (
        "I_edad",
        "Comprobantes W-2PR por tramo de salarios y edad",
        lambda w: tabla_i(w, True),
        "w2pr",
    ),
    ("J", "Distribución por municipio", tabla_j, "planillas"),
]

DICCIONARIO = [
    ("planillas", "Número de planillas en la fila", "—"),
    (
        "nota",
        "'c' = fila colapsada con la contigua por tener menos de 10 planillas",
        "—",
    ),
    (
        "tramo_iba",
        "Tramo de ingreso bruto ajustado",
        "Formulario 482, línea 5",
    ),
    (
        "estado",
        "Estado personal",
        "Formulario 482, encasillado de estado personal",
    ),
    ("salarios", "Salarios, comisiones y propinas", "1A–1C"),
    ("intereses_dividendos", "Intereses y dividendos", "2C, 2D"),
    ("pensiones", "Pensiones y anualidades", "2H"),
    (
        "distribuciones_retiro",
        "Distribuciones de planes de retiro e IRA",
        "2E, 2F, 2L",
    ),
    ("ganancia_capital", "Ganancia neta de capital", "2B"),
    (
        "entidades_conducto",
        "Participación distribuible en entidades conducto",
        "2K",
    ),
    (
        "industria_negocio",
        "Ingreso de industria o negocio, profesión, agricultura, alquiler",
        "2P–2T",
    ),
    ("pension_divorcio", "Pensión pagada por divorcio o separación", "4"),
    ("iba", "Ingreso bruto ajustado", "5"),
    ("deducciones", "Total de deducciones", "6"),
    ("exencion_personal", "Exención personal", "7"),
    ("exencion_dependientes", "Exención por dependientes", "8"),
    ("num_dependientes", "Número de dependientes reclamados", "8"),
    ("exencion_veterano", "Exención adicional por veterano", "9"),
    ("ingreso_neto", "Ingreso neto sujeto a contribución", "13"),
    ("contribucion_tabla", "Contribución según tabla", "14"),
    ("ajuste_gradual", "Ajuste gradual", "15"),
    (
        "planillas_92 / contribucion_regular_92",
        "Planillas con factor 92% y su contribución regular",
        "17; Sección 1021.01(c)",
    ),
    (
        "planillas_95 / contribucion_regular_95",
        "Planillas con factor 95% y su contribución regular",
        "17; Sección 1021.01(c)",
    ),
    ("contribucion_regular", "Contribución regular antes del crédito", "17"),
    (
        "credito_otras_jurisdicciones",
        "Crédito por contribuciones pagadas a otras jurisdicciones",
        "18",
    ),
    ("exceso_cba", "Exceso de contribución básica alterna", "20"),
    ("credito_cba", "Crédito por contribución básica alterna", "21"),
    ("creditos_anejo_b", "Créditos contributivos del Anejo B", "25"),
    (
        "responsabilidad / contribucion_determinada",
        "Responsabilidad contributiva",
        "26",
    ),
    ("retenida_salarios", "Contribución retenida sobre salarios", "27A"),
    ("credito_trabajo", "Crédito por Trabajo", "27C; Anejo CT"),
    (
        "creditos_federales",
        "Créditos reembolsables del Gobierno Federal",
        "27D",
    ),
    ("sobrepago", "Sobrepago", "29"),
    ("balance_pendiente", "Balance pendiente de pago", "31"),
    (
        "ded_hipoteca … ded_total",
        "Deducciones del Anejo A",
        "Anejo A, líneas 1i, 3, 4, 7b, 8b, 9b, 11",
    ),
    (
        "exento_pension",
        "Exención de pensiones",
        "Sección 1031.02(a)(13); Anejo IE",
    ),
    (
        "exento_jovenes",
        "Exención para jóvenes, Ley 135-2014",
        "Anejo IE, línea 31",
    ),
    (
        "exento_dificil_reclutamiento",
        "Salarios exentos de profesionales de difícil reclutamiento",
        "Anejo IE, línea 32",
    ),
    ("exento_total", "Total de ingresos exentos", "Anejo IE, línea 45"),
    (
        "dependientes",
        "Número de dependientes cualificados para el Crédito por Trabajo",
        "Anejo CT",
    ),
    (
        "ct_ingreso_ganado",
        "Ingreso bruto ganado",
        "Anejo CT, Parte II, línea 3",
    ),
    (
        "ct_reclamado / credito_concedido / ajuste",
        "Crédito reclamado, concedido y diferencia (planillas ajustadas)",
        "Anejo CT",
    ),
    ("edad", "Edad del contribuyente al cierre del año", "—"),
    (
        "tramo_ingreso_bruto",
        "Ingreso bruto según se define para el factor 92%/95%",
        "Sección 1021.01(c)",
    ),
    (
        "cba_ingreso_neto / cba_contribucion",
        "Ingreso neto sujeto a CBA y contribución básica alterna",
        "Anejo O",
    ),
    (
        "comprobantes / personas_distintas",
        "Comprobantes W-2PR y personas distintas",
        "Formulario 499R-2/W-2PR",
    ),
    ("retenida", "Contribución retenida (W-2PR)", "W-2PR"),
    (
        "exento_135",
        "Salarios exentos bajo la Ley 135-2014",
        "W-2PR, encasillado 16, código E",
    ),
    ("municipio", "Municipio de residencia del contribuyente", "—"),
]

# =========================================================================
# Salida
# =========================================================================


def escribir(anio, resultados, salida, faltantes, sintetico, fecha_corte):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    salida = Path(salida)
    salida.mkdir(parents=True, exist_ok=True)
    sufijo = "_SINTETICO" if sintetico else ""
    wb = Workbook()
    ws = wb.active
    ws.title = "Léame"
    lineas = [
        f"Tabulaciones del Formulario 482, año contributivo {anio}",
        "Preparadas para Espacios Abiertos (proyecto policyengine-pr)",
        "",
        "ADVERTENCIA: DATOS SINTÉTICOS generados por el guion para ilustrar el formato. NO son datos de Hacienda."
        if sintetico
        else f"Fuente: Departamento de Hacienda, tabulaciones especiales, {anio}.",
        f"Fecha de corte de las planillas: {fecha_corte or '[indicar]'}",
        f"Generado por tabulaciones_hacienda.py versión {VERSION}",
        "",
        f"Regla de supresión: filas con menos de {MIN_PLANILLAS} planillas colapsadas con la fila contigua",
        "(tramo inferior); marcadas con 'c' en la columna 'nota'. Las filas de totales se conservan.",
        "Cantidades en dólares, sin decimales. Conteos en número de planillas o comprobantes.",
        "",
        "Hojas:",
    ] + [
        f"  {clave}: {titulo}"
        for clave, titulo, _, _ in TABLAS
        if clave in resultados
    ]
    if faltantes:
        lineas += [
            "",
            "Columnas no disponibles en los microdatos (tratadas como 0):",
            "  " + ", ".join(faltantes),
        ]
    for i, l in enumerate(lineas, 1):
        ws.cell(row=i, column=1, value=l)
    ws["A1"].font = Font(bold=True, size=13)
    if sintetico:
        ws["A4"].font = Font(bold=True, color="C00000")
    ws.column_dimensions["A"].width = 110

    cabecera = Font(bold=True)
    relleno = PatternFill("solid", fgColor="DDEBF7")
    colapsada = PatternFill("solid", fgColor="FFF2CC")
    for clave, titulo, _, _ in TABLAS:
        if clave not in resultados:
            continue
        t = resultados[clave]
        hoja = wb.create_sheet(clave)
        hoja["A1"] = f"Tabla {clave} — {titulo} — año contributivo {anio}"
        hoja["A1"].font = Font(bold=True, size=12)
        for j, c in enumerate(t.columns, 1):
            cell = hoja.cell(row=3, column=j, value=c)
            cell.font, cell.fill = cabecera, relleno
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        for i, fila in enumerate(t.itertuples(index=False), 4):
            es_total = any(
                isinstance(v, str) and v.startswith("Total") for v in fila
            )
            for j, v in enumerate(fila, 1):
                if isinstance(v, (np.floating, float)):
                    v = round(float(v))
                elif isinstance(v, np.integer):
                    v = int(v)
                cell = hoja.cell(row=i, column=j, value=v)
                if isinstance(v, int):
                    cell.number_format = "#,##0"
                if es_total:
                    cell.font = cabecera
                if fila[-1] == "c":
                    cell.fill = colapsada
        for j, c in enumerate(t.columns, 1):
            hoja.column_dimensions[get_column_letter(j)].width = max(
                12, min(28, len(str(c)) + 2)
            )
        hoja.freeze_panes = "A4"
        t.to_csv(
            salida / f"tabla_{clave}_{anio}{sufijo}.csv",
            index=False,
            float_format="%.0f",
        )

    dic = wb.create_sheet("Diccionario")
    for j, c in enumerate(
        [
            "columna",
            "descripción",
            "línea del Formulario 482 / anejo (formulario 2025)",
        ],
        1,
    ):
        cell = dic.cell(row=1, column=j, value=c)
        cell.font, cell.fill = cabecera, relleno
    for i, fila in enumerate(DICCIONARIO, 2):
        for j, v in enumerate(fila, 1):
            dic.cell(row=i, column=j, value=v)
    for col, w in zip("ABC", (40, 70, 45)):
        dic.column_dimensions[col].width = w

    ruta = salida / f"tabulaciones_482_{anio}{sufijo}.xlsx"
    wb.save(ruta)
    return ruta


# =========================================================================
# Principal
# =========================================================================


def main(argv=None):
    p = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    p.add_argument("--anio", type=int, required=True, help="año contributivo")
    p.add_argument(
        "--planillas",
        help="archivo de microdatos de planillas (CSV, Parquet o Excel)",
    )
    p.add_argument(
        "--w2pr",
        help="archivo de comprobantes W-2PR (opcional; produce la Tabla I)",
    )
    p.add_argument("--salida", default="salida", help="carpeta de salida")
    p.add_argument(
        "--fecha-corte",
        default=None,
        help="fecha de corte de las planillas (texto)",
    )
    p.add_argument(
        "--sintetico",
        action="store_true",
        help="usar microdatos sintéticos (prueba)",
    )
    args = p.parse_args(argv)

    faltantes = []
    if args.sintetico:
        planillas, w2 = datos_sinteticos(), w2pr_sintetico()
    else:
        if not args.planillas:
            p.error("indique --planillas o use --sintetico")
        planillas = normalizar(
            leer(args.planillas), COLUMNAS_PLANILLAS, faltantes
        )
        w2 = (
            normalizar(leer(args.w2pr), COLUMNAS_W2PR, faltantes)
            if args.w2pr
            else None
        )

    print(
        f"Planillas leídas: {len(planillas):,}"
        + (f"; comprobantes W-2PR: {len(w2):,}" if w2 is not None else "")
    )
    resultados = {}
    for clave, titulo, fn, fuente in TABLAS:
        datos = planillas if fuente == "planillas" else w2
        if datos is None:
            print(f"  Tabla {clave}: omitida (sin archivo W-2PR)")
            continue
        try:
            resultados[clave] = fn(datos)
            print(f"  Tabla {clave}: {len(resultados[clave])} filas")
        except Exception as e:  # noqa: BLE001 - una tabla fallida no impide las demás
            print(f"  Tabla {clave}: ERROR {e!r}", file=sys.stderr)

    ruta = escribir(
        args.anio,
        resultados,
        args.salida,
        faltantes,
        args.sintetico,
        args.fecha_corte,
    )
    print(f"Libro Excel: {ruta}")


if __name__ == "__main__":
    main()
