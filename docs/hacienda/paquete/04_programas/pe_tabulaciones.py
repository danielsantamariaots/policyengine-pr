# -*- coding: utf-8 -*-
"""
Proyecto policyengine-pr (modelo público de microsimulación contributiva de Puerto Rico) — Espacios Abiertos.
Programa para ejecutarse DENTRO del Departamento de Hacienda sobre los microdatos del Formulario 482.

Versión Python (solo pandas, numpy y openpyxl). Produce las tablas 0 y A–J descritas en
Especificacion_salidas_PE, aplicando la regla de supresión de Hacienda (N < 10).

Uso:
    python pe_tabulaciones.py --anio 2023 --entrada planillas.csv [--w2pr w2pr.csv] --salida salidas/
        [--supresion colapsar|vaciar] [--fecha-corte "2025-10-15"] [--etiqueta PRUEBA]

Entrada: un archivo CSV (o Parquet / Excel) con una fila por planilla del año contributivo --anio y las
columnas de 02_contrato_y_parametros/esquema_planillas.csv (14 necesarias; las demás amplían las salidas:
si falta alguna, el programa omite solo lo que depende de ella y lo anota en el registro). Opcionalmente, un
archivo de comprobantes W-2PR (una fila por comprobante; esquema_w2pr.csv), con el que produce la Tabla I.

Salida: en la carpeta --salida, un archivo CSV por tabla (tabla_0_control.csv, tabla_A.csv … tabla_J.csv),
el libro Excel tabulaciones_482_<anio>.xlsx (una hoja por tabla, más «Léame» y «Diccionario») y el registro
log_ejecucion_pe.txt. Ninguna salida contiene datos de planillas individuales.

Regla de supresión (MIN_N = 10), en dos modalidades (--supresion):
  colapsar (la que pide la carta de solicitud; por defecto): toda fila con menos de 10 planillas se une a la
      fila contigua (el tramo inmediatamente inferior; si es la primera, al superior) hasta que ninguna quede
      por debajo de 10; la etiqueta pasa a ser el tramo combinado, la columna «nota» lleva «c» y «supr» vale 1.
      Los totales se conservan exactos.
  vaciar (la de los paquetes WTG y AV): la fila se publica con su etiqueta, pero todos sus valores se dejan
      vacíos (supr = 1); si las filas vacías de un grupo fueran una sola o sumaran menos de 10 planillas,
      se vacían además las filas más pequeñas necesarias (supr = 2, «para proteger otras»).
En las dos modalidades, dentro de cada fila publicada: todo conteo parcial (planillas_*, personas_distintas)
entre 1 y 9, o cuyo complemento respecto del conteo de la fila esté entre 1 y 9, se deja vacío, junto con las
sumas que dependen de él; y, por columna y grupo, los vacíos deben ser dos o más y sumar 0 o al menos 10,
vaciando otras celdas si hace falta. No se redondea ningún valor: la protección es la supresión.
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import platform
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

VERSION = "2026-11-04 (rev. 1 del paquete PE)"

# ============================================================================================== parámetros
MIN_N = 10  # regla de supresión de Hacienda: celdas con menos de 10 planillas
MODOS = ("colapsar", "vaciar")

# Columnas del archivo de planillas (nombres fijos; los define esquema_planillas.csv). Entre paréntesis, la
# línea del Formulario 482 de 2025.
COLS_OBLIG = [
    "estado_personal",  # 1 individual, 2 conjunta, 3 separada, 4 cómputo opcional
    "edad",  # del contribuyente principal al cierre del año
    "salarios",  # 1A–1C
    "iba",  # 5
    "deducciones",  # 6
    "exencion_personal",  # 7
    "exencion_dependientes",  # 8
    "num_dependientes",  # 8 (número)
    "ingreso_neto",  # 13
    "contribucion_tabla",  # 14
    "contribucion_regular",  # 17
    "responsabilidad",  # 26
    "credito_trabajo",  # 27C
    "creditos_federales",  # 27D
]
# Columnas que amplían las salidas: qué se omite si falta cada una.
SI_FALTA = {
    "anio": "se supone que todas las filas son del año --anio",
    "municipio": "no se produce la Tabla J",
    "intereses_dividendos": "sin esa columna en A",
    "pensiones": "sin esa columna en A",
    "distribuciones_retiro": "sin esa columna en A",
    "ganancia_capital": "sin esa columna en A",
    "entidades_conducto": "sin esa columna en A",
    "industria_negocio": "sin esa columna en A y en E",
    "pension_divorcio": "sin esa columna en A",
    "exencion_veterano": "sin esa columna en A",
    "ajuste_gradual": "sin esa columna en A; no se produce G1",
    "factor": "sin las columnas 92 %/95 % en A; no se produce F",
    "ingreso_bruto_factor": "no se produce F",
    "credito_otras_jurisdicciones": "sin esa columna en A",
    "exceso_cba": "sin esa columna en A y en G2",
    "credito_cba": "sin esa columna en A",
    "creditos_anejo_b": "sin esa columna en A",
    "retenida_salarios": "sin esa columna en A",
    "sobrepago": "sin esa columna en A",
    "balance_pendiente": "sin esa columna en A",
    "ded_hipoteca": "sin esa columna en B",
    "ded_medicos": "sin esa columna en B",
    "ded_donativos": "sin esa columna en B",
    "ded_ira": "sin esa columna en B",
    "ded_educativa": "sin esa columna en B",
    "ded_prestamos": "sin esa columna en B",
    "ded_total": "no se produce B",
    "exento_pension": "sin esa columna en C",
    "exento_jovenes": "sin esa columna en C; no se produce E",
    "exento_dificil_reclutamiento": "sin esa columna en C",
    "exento_total": "no se produce C",
    "ct_dependientes": "no se producen D1, D2 ni D3",
    "ct_ingreso_ganado": "no se produce D2; sin esa columna en D1",
    "ct_reclamado": "no se produce D3",
    "ct_ajustado": "no se produce D3",
    "cba_ingreso_neto": "no se produce G2",
    "cba_contribucion": "no se produce G2",
}
COLS_OPC = list(SI_FALTA)
COLS_W2PR_OBLIG = ["id_persona", "salarios"]
COLS_W2PR_OPC = {"retenida": "sin esa columna en I", "exento_135": "sin esa columna en I", "edad": "no se produce I_edad"}
TEXTO = {"municipio", "id_persona"}

ETIQUETA_ESTADO = {1: "Individual", 2: "Casado, planilla conjunta", 3: "Casado, planilla separada", 4: "Cómputo opcional de casados"}

# Tramos de ingreso bruto ajustado (límite superior incluido).
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

# Conteos parciales y las sumas que dependen de cada uno (se vacían juntos). Regla general: planillas_X
# depende de la columna X; aquí solo las excepciones.
DEPENDIENTES_EXTRA = {
    "planillas_num_dependientes": ["num_dependientes", "exencion_dependientes"],
    "planillas_92": ["contribucion_regular_92"],
    "planillas_95": ["contribucion_regular_95"],
    "personas_distintas": [],
}
CONTEOS_FILA = ("planillas", "planillas_ajustadas", "comprobantes")  # el conteo propio de cada tabla

# ============================================================================================== registro
class Registro:
    def __init__(self, ruta):
        self.ruta = ruta
        self.lineas = []
        self.t0 = time.time()

    def __call__(self, texto):
        print(texto)
        self.lineas.append(texto)

    def guardar(self):
        with open(self.ruta, "w", encoding="utf-8") as f:
            f.write("\n".join(self.lineas) + "\n")


# ============================================================================================== utilidades
def tramos_regulares(inicio, fin, paso, etiqueta_final=None):
    tramos, lo = [], inicio
    while lo < fin:
        hi = min(lo + paso, fin)
        tramos.append((lo, hi, f"${lo:,.0f} – ${hi:,.0f}"))
        lo = hi
    if etiqueta_final:
        tramos.append((fin, np.inf, etiqueta_final))
    return tramos


def asignar_tramo(valores, tramos):
    etiquetas = [t[2] for t in tramos]
    bordes = [tramos[0][0]] + [t[1] for t in tramos]
    return pd.cut(pd.to_numeric(valores, errors="coerce"), bins=bordes, labels=etiquetas, right=True, include_lowest=True)


def etiqueta_estado(serie):
    valores = serie.map(ETIQUETA_ESTADO).fillna("Otro")
    categorias = list(ETIQUETA_ESTADO.values()) + (["Otro"] if (valores == "Otro").any() else [])
    return pd.Categorical(valores, categorias, ordered=True)


def agregar(df, filas, columnas_suma, columnas_conteo=None, col_n="planillas"):
    """Suma y cuenta por `filas`. `columnas_conteo`: {nombre_salida: columna} cuenta registros con columna > 0.
    Solo entran las columnas presentes en df."""
    columnas_suma = [c for c in columnas_suma if c in df.columns]
    columnas_conteo = {k: v for k, v in (columnas_conteo or {}).items() if v in df.columns}
    g = df.groupby(filas, observed=False, dropna=False)
    out = g.size().rename(col_n).to_frame()
    for salida, col in columnas_conteo.items():
        out[salida] = g[col].apply(lambda s: int((s > 0).sum()))
    for col in columnas_suma:
        out[col] = g[col].sum()
    return out.reset_index()


def _unir_etiquetas(a, b):
    a, b = str(a), str(b)
    if "–" in a and "–" in b:
        return f"{a.split('–')[0].strip()} – {b.split('–')[-1].strip()}"
    if "–" in a and "o más" in b:
        return f"{a.split('–')[0].strip()} o más"
    if "o menos" in a and "–" in b:
        return f"{b.split('–')[-1].strip()} o menos"
    return f"{a} + {b}"


def columnas_numericas(tabla, excluir):
    return [c for c in tabla.columns if c not in excluir and pd.api.types.is_numeric_dtype(tabla[c])]


# ============================================================================================== protección
class Protector:
    """Aplica la regla de supresión a una tabla y lleva la cuenta de lo que vació."""

    def __init__(self, modo):
        self.modo = modo
        self.filas_colapsadas = 0
        self.filas_vaciadas = 0
        self.filas_proteger = 0
        self.celdas_parciales = 0
        self.celdas_proteger = 0

    # ---- filas -------------------------------------------------------------------------------------
    def filas(self, tabla, col_n, etiqueta, grupo=None):
        tabla = tabla.copy()
        tabla["nota"] = ""
        tabla["supr"] = 0
        fn = self._colapsar if self.modo == "colapsar" else self._vaciar
        if grupo is None:
            return fn(tabla, col_n, etiqueta)
        partes = [fn(b, col_n, etiqueta) for _, b in tabla.groupby(grupo, observed=False, sort=False)]
        return pd.concat(partes, ignore_index=True)

    def _colapsar(self, bloque, col_n, etiqueta):
        numericas = columnas_numericas(bloque, {etiqueta, "nota", "supr"})
        filas = bloque.to_dict("records")
        cambiado = True
        while cambiado and len(filas) > 1:
            cambiado = False
            for i, f in enumerate(filas):
                if f[col_n] < MIN_N:
                    j = i - 1 if i > 0 else i + 1
                    destino = filas[j]
                    for c in numericas:
                        destino[c] = destino[c] + f[c]
                    lo, hi = (destino, f) if j < i else (f, destino)
                    destino[etiqueta] = _unir_etiquetas(lo[etiqueta], hi[etiqueta])
                    destino["nota"], destino["supr"] = "c", 1
                    del filas[i]
                    self.filas_colapsadas += 1
                    cambiado = True
                    break
        return pd.DataFrame(filas)

    def _vaciar(self, bloque, col_n, etiqueta):
        bloque = bloque.reset_index(drop=True)
        numericas = columnas_numericas(bloque, {etiqueta, "nota", "supr"})
        n = bloque[col_n].astype(float)
        supr = (n < MIN_N) & (n > 0)
        # complementaria: las filas vacías deben ser dos o más y sumar al menos 10, salvo que no haya ninguna
        while supr.any() and (supr.sum() < 2 or n[supr].sum() < MIN_N):
            candidatos = n[~supr & (n > 0)]
            if candidatos.empty:
                break
            k = candidatos.idxmin()
            supr[k] = True
            bloque.loc[k, "supr"] = 2
            self.filas_proteger += 1
        bloque.loc[supr & (bloque["supr"] == 0), "supr"] = 1
        self.filas_vaciadas += int((bloque["supr"] == 1).sum())
        bloque.loc[supr, numericas] = np.nan
        bloque.loc[supr, "nota"] = "s"
        return bloque

    # ---- celdas (conteos parciales y sus sumas) ----------------------------------------------------
    def celdas(self, tabla, col_n, etiqueta, grupo=None):
        parciales = [c for c in tabla.columns if (c.startswith("planillas_") and c != col_n) or c == "personas_distintas"]
        if not parciales:
            return tabla
        tabla = tabla.copy()
        n = tabla[col_n].astype(float)
        for p in parciales:
            v = tabla[p].astype(float)
            vaciar = ((v > 0) & (v < MIN_N)) | ((n - v > 0) & (n - v < MIN_N) & (p != "personas_distintas"))
            vaciar &= v.notna()
            self.celdas_parciales += int(vaciar.sum())
            tabla.loc[vaciar, [p] + self._dependientes(p, tabla)] = np.nan
        # por columna y grupo: los vacíos de las filas publicadas deben ser dos o más y sumar 0 o al menos 10
        es_total = tabla[etiqueta].astype(str).str.startswith("Total")
        claves = tabla[grupo].astype(str) if grupo is not None else pd.Series("", index=tabla.index)
        for p in parciales:
            for _, idx in tabla.groupby(claves, sort=False).groups.items():
                cuerpo = [i for i in idx if not es_total[i] and tabla.at[i, "supr"] == 0]
                self._complementaria(tabla, p, cuerpo, [i for i in idx if es_total[i]])
        return tabla

    def _complementaria(self, tabla, p, cuerpo, totales):
        vac = [i for i in cuerpo if pd.isna(tabla.at[i, p])]
        if not vac:
            return
        orig = tabla[p].astype(float)
        while True:
            # valores originales de las celdas vacías los conoce solo este programa: se deducen de los totales
            publicados = [i for i in cuerpo if not pd.isna(tabla.at[i, p])]
            suma_vac = sum(float(tabla.at[t, p]) for t in totales if not pd.isna(tabla.at[t, p])) - sum(
                orig[i] for i in publicados
            ) if totales else np.nan
            ok = len(vac) >= 2 and (np.isnan(suma_vac) or suma_vac == 0 or suma_vac >= MIN_N)
            if ok or not publicados:
                break
            k = min(publicados, key=lambda i: (orig[i] if orig[i] > 0 else np.inf))
            if not np.isfinite(orig[k]) or orig[k] <= 0:
                # no queda ninguna celda positiva que vaciar: se vacía el total
                for t in totales:
                    tabla.loc[t, [p] + self._dependientes(p, tabla)] = np.nan
                    self.celdas_proteger += 1
                break
            tabla.loc[k, [p] + self._dependientes(p, tabla)] = np.nan
            vac.append(k)
            self.celdas_proteger += 1

    @staticmethod
    def _dependientes(p, tabla):
        if p in DEPENDIENTES_EXTRA:
            cols = DEPENDIENTES_EXTRA[p]
        else:
            cols = [p[len("planillas_"):]]
        return [c for c in cols if c in tabla.columns]


def con_totales(tabla, etiqueta, grupo=None, texto="Total"):
    """Fila de totales por grupo y total general, calculados ANTES de la protección (son exactos)."""
    numericas = columnas_numericas(tabla, {"supr"})
    partes = []
    if grupo is not None:
        for g, b in tabla.groupby(grupo, observed=False, sort=False):
            t = b[numericas].sum().to_frame().T
            t[grupo], t[etiqueta] = g, texto
            partes += [b, t]
        tabla = pd.concat(partes, ignore_index=True)
    total = tabla[tabla[etiqueta] != texto][numericas].sum().to_frame().T
    total[etiqueta] = "Total general" if grupo is not None else texto
    if grupo is not None:
        total[grupo] = ""
    return pd.concat([tabla, total], ignore_index=True)


def proteger(prot, tabla, col_n, etiqueta, grupo=None, primeras=None):
    """Totales exactos + protección de filas + protección de celdas + orden de columnas."""
    totales = con_totales(tabla, etiqueta, grupo)
    es_total = totales[etiqueta].astype(str).str.startswith("Total")
    cuerpo = prot.filas(totales[~es_total], col_n, etiqueta, grupo)
    filas_total = totales[es_total].copy()
    filas_total["nota"], filas_total["supr"] = "", 0
    # reordenar: cada grupo seguido de su total
    if grupo is not None:
        partes = []
        for g in list(dict.fromkeys(cuerpo[grupo].astype(str))):
            partes.append(cuerpo[cuerpo[grupo].astype(str) == g])
            partes.append(filas_total[filas_total[grupo].astype(str) == g])
        partes.append(filas_total[filas_total[etiqueta] == "Total general"])
        out = pd.concat(partes, ignore_index=True)
    else:
        out = pd.concat([cuerpo, filas_total], ignore_index=True)
    out = prot.celdas(out, col_n, etiqueta, grupo)
    primeras = primeras or ([grupo] if grupo else []) + [etiqueta, col_n]
    resto = [c for c in out.columns if c not in primeras and c not in ("nota", "supr")]
    return out[[c for c in primeras if c in out.columns] + resto + ["nota", "supr"]]


# ============================================================================================== carga
def leer(path):
    path = Path(path)
    if path.suffix.lower() == ".parquet":
        return pd.read_parquet(path)
    if path.suffix.lower() in (".xlsx", ".xls"):
        return pd.read_excel(path)
    return pd.read_csv(path, low_memory=False, encoding="utf-8")


def preparar(df, oblig, opc, log, nombre):
    faltan = [c for c in oblig if c not in df.columns]
    if faltan:
        log(f"ERROR: faltan columnas necesarias en {nombre}: {', '.join(faltan)}. Se detiene.")
        sys.exit(1)
    ausentes = [c for c in opc if c not in df.columns]
    for c in ausentes:
        log(f"  AVISO: falta {c} en {nombre}: {opc[c] if isinstance(opc, dict) else SI_FALTA[c]}")
    for c in df.columns:
        if c not in TEXTO:
            df[c] = pd.to_numeric(df[c], errors="coerce").fillna(0)
    return df, ausentes


# ============================================================================================== tablas
CAMPOS_A = [
    "salarios", "intereses_dividendos", "pensiones", "distribuciones_retiro", "ganancia_capital", "entidades_conducto",
    "industria_negocio", "pension_divorcio", "iba", "deducciones", "exencion_personal", "exencion_dependientes",
    "num_dependientes", "exencion_veterano", "ingreso_neto", "contribucion_tabla", "ajuste_gradual", "contribucion_regular",
    "credito_otras_jurisdicciones", "exceso_cba", "credito_cba", "creditos_anejo_b", "responsabilidad", "retenida_salarios",
    "credito_trabajo", "creditos_federales", "sobrepago", "balance_pendiente",
]


def con_factor(d):
    if "factor" not in d.columns:
        return d, []
    d = d.assign(
        planillas_92=(d["factor"] < 0.935).astype(int),
        planillas_95=(d["factor"] >= 0.935).astype(int),
        contribucion_regular_92=np.where(d["factor"] < 0.935, d["contribucion_regular"], 0),
        contribucion_regular_95=np.where(d["factor"] >= 0.935, d["contribucion_regular"], 0),
    )
    return d, ["planillas_92", "contribucion_regular_92", "planillas_95", "contribucion_regular_95"]


def tabla_0(df, w2, anio):
    """Tabla de control: totales del archivo de entrada (una fila), para cuadrar con Hacienda."""
    fila = {"anio": anio, "planillas": len(df)}
    for c in ["salarios", "iba", "ingreso_neto", "contribucion_regular", "responsabilidad", "credito_trabajo",
              "creditos_federales", "exento_jovenes", "ded_total", "exento_total", "ajuste_gradual", "cba_contribucion"]:
        if c in df.columns:
            fila[f"planillas_{c}"] = int((df[c] > 0).sum())
            fila[c] = float(df[c].sum())
    for k, v in ETIQUETA_ESTADO.items():
        fila[f"planillas_estado_{k}"] = int((df["estado_personal"] == k).sum())
    if "factor" in df.columns:
        fila["planillas_92"] = int((df["factor"] < 0.935).sum())
        fila["planillas_95"] = int((df["factor"] >= 0.935).sum())
    if w2 is not None:
        fila["comprobantes"] = len(w2)
        fila["personas_distintas"] = int(w2["id_persona"].nunique())
        fila["salarios_w2pr"] = float(w2["salarios"].sum())
    return pd.DataFrame([fila])


def tabla_a(df, prot):
    d, extra = con_factor(df)
    d = d.assign(tramo_iba=asignar_tramo(d["iba"], TRAMOS_IBA), estado=etiqueta_estado(d["estado_personal"]))
    t = agregar(d, ["estado", "tramo_iba"], CAMPOS_A + extra,
                {"planillas_num_dependientes": "num_dependientes", "planillas_credito_trabajo": "credito_trabajo"})
    return proteger(prot, t, "planillas", "tramo_iba", "estado")


def tabla_b(df, prot):
    campos = ["ded_hipoteca", "ded_medicos", "ded_donativos", "ded_ira", "ded_educativa", "ded_prestamos", "ded_total"]
    d = df.assign(tramo_iba=asignar_tramo(df["iba"], TRAMOS_IBA))
    t = agregar(d, ["tramo_iba"], campos, {f"planillas_{c}": c for c in campos})
    return proteger(prot, t, "planillas", "tramo_iba")


def tabla_c(df, prot):
    campos = ["exento_pension", "exento_jovenes", "exento_dificil_reclutamiento", "exento_total"]
    d = df.assign(tramo_iba=asignar_tramo(df["iba"] + df["exento_total"], TRAMOS_IBA))
    t = agregar(d, ["tramo_iba"], campos, {f"planillas_{c}": c for c in campos})
    return proteger(prot, t, "planillas", "tramo_iba")


def _dependientes_ct(df):
    return pd.Categorical(np.minimum(df["ct_dependientes"], 3).map({0: "0", 1: "1", 2: "2", 3: "3 o más"}),
                          ["0", "1", "2", "3 o más"], ordered=True)


def tabla_d1(df, prot):
    d = df[df["credito_trabajo"] > 0]
    d = d.assign(dependientes=_dependientes_ct(d), estado=etiqueta_estado(d["estado_personal"]))
    t = agregar(d, ["estado", "dependientes"], ["credito_trabajo", "ct_ingreso_ganado"])
    return proteger(prot, t, "planillas", "dependientes", "estado")


def tabla_d2(df, prot):
    d = df[df["credito_trabajo"] > 0]
    tramos = tramos_regulares(0, 55_000, 2_500, "$55,001 o más")
    d = d.assign(dependientes=_dependientes_ct(d), tramo_ingreso_ganado=asignar_tramo(d["ct_ingreso_ganado"], tramos))
    t = agregar(d, ["dependientes", "tramo_ingreso_ganado"], ["credito_trabajo"])
    return proteger(prot, t, "planillas", "tramo_ingreso_ganado", "dependientes")


def tabla_d3(df, prot):
    d = df[df["ct_ajustado"] > 0]
    d = d.assign(dependientes=_dependientes_ct(d), ajuste=d["ct_reclamado"] - d["credito_trabajo"])
    t = agregar(d, ["dependientes"], ["ct_reclamado", "credito_trabajo", "ajuste"], col_n="planillas_ajustadas")
    t = t.rename(columns={"credito_trabajo": "credito_concedido"})
    return proteger(prot, t, "planillas_ajustadas", "dependientes")


def tabla_e(df, prot):
    d = df[(df["exento_jovenes"] > 0) & df["edad"].between(16, 26)]
    d = d.assign(edad=d["edad"].astype(int).astype(str), contribucion_determinada=d["responsabilidad"])
    t = agregar(d, ["edad"], ["exento_jovenes", "salarios", "industria_negocio", "contribucion_determinada"])
    t = t.sort_values("edad", key=lambda s: s.astype(int)).reset_index(drop=True)
    return proteger(prot, t, "planillas", "edad")


def tabla_f(df, prot):
    d = df[df["ingreso_bruto_factor"].between(90_000, 110_000)]
    d, extra = con_factor(d)
    d = d.assign(tramo_ingreso_bruto=asignar_tramo(d["ingreso_bruto_factor"], tramos_regulares(90_000, 110_000, 2_000)))
    t = agregar(d, ["tramo_ingreso_bruto"], extra)
    return proteger(prot, t, "planillas", "tramo_ingreso_bruto")


def tabla_g1(df, prot):
    d = df[df["ingreso_neto"] > 500_000]
    d = d.assign(estado=etiqueta_estado(d["estado_personal"]))
    t = agregar(d, ["estado"], ["ingreso_neto", "ajuste_gradual"])
    return proteger(prot, t, "planillas", "estado")


def tabla_g2(df, prot):
    d = df[df["cba_contribucion"] > 0]
    tramos = [(-np.inf, 50_000, "Hasta $50,000"), (50_000, 75_000, "$50,001 – $75,000"), (75_000, 150_000, "$75,001 – $150,000"),
              (150_000, 250_000, "$150,001 – $250,000"), (250_000, np.inf, "$250,001 o más")]
    d = d.assign(tramo_cba=asignar_tramo(d["cba_ingreso_neto"], tramos))
    t = agregar(d, ["tramo_cba"], ["cba_ingreso_neto", "cba_contribucion", "exceso_cba"])
    return proteger(prot, t, "planillas", "tramo_cba")


def tabla_h(df, prot):
    d = df.assign(
        dependientes=pd.Categorical(np.minimum(df["num_dependientes"], 4).map({0: "0", 1: "1", 2: "2", 3: "3", 4: "4 o más"}),
                                    ["0", "1", "2", "3", "4 o más"], ordered=True),
        estado=etiqueta_estado(df["estado_personal"]),
    )
    t = agregar(d, ["estado", "dependientes"], ["exencion_dependientes", "credito_trabajo", "creditos_federales"])
    return proteger(prot, t, "planillas", "dependientes", "estado")


def tabla_i(w2, prot, por_edad=False):
    tramos = tramos_regulares(0, 50_000, 2_500) + TRAMOS_IBA[8:]
    d = w2.assign(tramo_salarios=asignar_tramo(w2["salarios"], tramos))
    filas, grupo = ["tramo_salarios"], None
    if por_edad:
        edades = [(15, 25, "16 – 25"), (25, 35, "26 – 35"), (35, 50, "36 – 50"), (50, 64, "51 – 64"), (64, np.inf, "65 o más")]
        d = d.assign(grupo_edad=asignar_tramo(d["edad"], edades))
        filas, grupo = ["grupo_edad", "tramo_salarios"], "grupo_edad"
    g = d.groupby(filas, observed=False)
    t = g.size().rename("comprobantes").to_frame()
    t["personas_distintas"] = g["id_persona"].nunique()
    for c in ["salarios", "retenida", "exento_135"]:
        if c in d.columns:
            t[c] = g[c].sum()
    return proteger(prot, t.reset_index(), "comprobantes", "tramo_salarios", grupo)


def tabla_j(df, prot):
    t = agregar(df, ["municipio"], ["iba", "responsabilidad", "credito_trabajo"], {"planillas_credito_trabajo": "credito_trabajo"})
    t = t.rename(columns={"responsabilidad": "contribucion_determinada"})
    t = t.sort_values("planillas", ascending=False).reset_index(drop=True)
    # el colapso une cada municipio pequeño con el siguiente de menor población (el anterior en la lista ordenada)
    return proteger(prot, t, "planillas", "municipio")


# (clave, título, función, fuente, columnas necesarias)
TABLAS = [
    ("A", "Resumen por tramo de IBA y estado personal", tabla_a, "planillas", []),
    ("B", "Deducciones del Anejo A por tramo de IBA", tabla_b, "planillas", ["ded_total"]),
    ("C", "Ingresos exentos del Anejo IE por tramo de IBA", tabla_c, "planillas", ["exento_total"]),
    ("D1", "Crédito por Trabajo por dependientes y estado personal", tabla_d1, "planillas", ["ct_dependientes"]),
    ("D2", "Crédito por Trabajo por tramo de ingreso ganado", tabla_d2, "planillas", ["ct_dependientes", "ct_ingreso_ganado"]),
    ("D3", "Crédito por Trabajo denegado o ajustado", tabla_d3, "planillas", ["ct_dependientes", "ct_reclamado", "ct_ajustado"]),
    ("E", "Exención para jóvenes (Ley 135-2014) por edad", tabla_e, "planillas", ["exento_jovenes"]),
    ("F", "Umbral de $100,000 del factor 92 %/95 %", tabla_f, "planillas", ["factor", "ingreso_bruto_factor"]),
    ("G1", "Ajuste gradual (ingreso neto > $500,000)", tabla_g1, "planillas", ["ajuste_gradual"]),
    ("G2", "Contribución básica alterna (Anejo O)", tabla_g2, "planillas", ["cba_ingreso_neto", "cba_contribucion"]),
    ("H", "Dependientes reclamados", tabla_h, "planillas", []),
    ("I", "Comprobantes W-2PR por tramo de salarios", tabla_i, "w2pr", []),
    ("I_edad", "Comprobantes W-2PR por tramo de salarios y edad", lambda w, p: tabla_i(w, p, True), "w2pr", ["edad"]),
    ("J", "Distribución por municipio", tabla_j, "planillas", ["municipio"]),
]

DICCIONARIO = [
    ("planillas", "Número de planillas en la fila (en D3: planillas ajustadas)", "—"),
    ("comprobantes / personas_distintas", "Comprobantes W-2PR y personas distintas en la fila", "Formulario 499R-2/W-2PR"),
    ("planillas_X", "Planillas de la fila con la columna X mayor que cero (conteo parcial)", "—"),
    ("nota", "'c' = fila colapsada con la contigua; 's' = fila vaciada (modalidad vaciar)", "—"),
    ("supr", "0 publicada; 1 colapsada o vaciada por tener menos de 10 planillas; 2 vaciada para proteger otras", "—"),
    ("tramo_iba", "Tramo de ingreso bruto ajustado", "Formulario 482, línea 5"),
    ("estado", "Estado personal", "Formulario 482, encasillado de estado personal"),
    ("salarios", "Salarios, comisiones y propinas", "1A–1C"),
    ("intereses_dividendos", "Intereses y dividendos", "2C, 2D"),
    ("pensiones", "Pensiones y anualidades", "2H"),
    ("distribuciones_retiro", "Distribuciones de planes de retiro e IRA", "2E, 2F, 2L"),
    ("ganancia_capital", "Ganancia neta de capital", "2B"),
    ("entidades_conducto", "Participación distribuible en entidades conducto", "2K"),
    ("industria_negocio", "Ingreso de industria o negocio, profesión, agricultura, alquiler", "2P–2T"),
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
    ("planillas_92 / contribucion_regular_92", "Planillas con factor 92 % y su contribución regular", "17; Sección 1021.01(c)"),
    ("planillas_95 / contribucion_regular_95", "Planillas con factor 95 % y su contribución regular", "17; Sección 1021.01(c)"),
    ("contribucion_regular", "Contribución regular antes del crédito", "17"),
    ("credito_otras_jurisdicciones", "Crédito por contribuciones pagadas a otras jurisdicciones", "18"),
    ("exceso_cba", "Exceso de contribución básica alterna", "20"),
    ("credito_cba", "Crédito por contribución básica alterna", "21"),
    ("creditos_anejo_b", "Créditos contributivos del Anejo B", "25"),
    ("responsabilidad / contribucion_determinada", "Responsabilidad contributiva", "26"),
    ("retenida_salarios", "Contribución retenida sobre salarios", "27A"),
    ("credito_trabajo", "Crédito por Trabajo", "27C; Anejo CT"),
    ("creditos_federales", "Créditos reembolsables del Gobierno Federal", "27D"),
    ("sobrepago", "Sobrepago", "29"),
    ("balance_pendiente", "Balance pendiente de pago", "31"),
    ("ded_hipoteca … ded_total", "Deducciones del Anejo A", "Anejo A, líneas 1i, 3, 4, 7b, 8b, 9b, 11"),
    ("exento_pension", "Exención de pensiones", "Sección 1031.02(a)(13); Anejo IE"),
    ("exento_jovenes", "Exención para jóvenes, Ley 135-2014", "Anejo IE, línea 31"),
    ("exento_dificil_reclutamiento", "Salarios exentos de profesionales de difícil reclutamiento", "Anejo IE, línea 32"),
    ("exento_total", "Total de ingresos exentos", "Anejo IE, línea 45"),
    ("dependientes", "Dependientes cualificados para el Crédito por Trabajo (D) o reclamados (H)", "Anejo CT / línea 8"),
    ("ct_ingreso_ganado", "Ingreso bruto ganado", "Anejo CT, Parte II, línea 3"),
    ("ct_reclamado / credito_concedido / ajuste", "Crédito reclamado, concedido y diferencia (planillas ajustadas)", "Anejo CT"),
    ("edad", "Edad del contribuyente al cierre del año", "—"),
    ("tramo_ingreso_bruto", "Ingreso bruto según se define para el factor 92 %/95 %", "Sección 1021.01(c)"),
    ("cba_ingreso_neto / cba_contribucion", "Ingreso neto sujeto a CBA y contribución básica alterna", "Anejo O"),
    ("retenida", "Contribución retenida (W-2PR)", "W-2PR"),
    ("exento_135", "Salarios exentos bajo la Ley 135-2014", "W-2PR, encasillado 16, código E"),
    ("municipio", "Municipio de residencia del contribuyente", "—"),
]

# ============================================================================================== salida


def escribir(anio, resultados, salida, ausentes, modo, fecha_corte, etiqueta):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.utils import get_column_letter

    salida = Path(salida)
    wb = Workbook()
    ws = wb.active
    ws.title = "Léame"
    lineas = [
        f"Tabulaciones del Formulario 482, año contributivo {anio}" + (f" — {etiqueta}" if etiqueta else ""),
        "Preparadas para Espacios Abiertos (proyecto policyengine-pr)",
        "",
        ("ADVERTENCIA: DATOS DE PRUEBA generados por gen_dummy.py para ilustrar el formato. NO son datos de Hacienda."
         if etiqueta else f"Fuente: Departamento de Hacienda, tabulaciones especiales, {anio}."),
        f"Fecha de corte de las planillas: {fecha_corte or '[indicar]'}",
        f"Generado por pe_tabulaciones.py versión {VERSION}; modalidad de supresión: {modo}",
        "",
        f"Regla de supresión: ninguna celda con menos de {MIN_N} planillas.",
        ("Modalidad colapsar: las filas con menos de 10 planillas se unen a la contigua (tramo inferior); nota = 'c', supr = 1."
         if modo == "colapsar" else
         "Modalidad vaciar: las filas con menos de 10 planillas se publican vacías (supr = 1); otras se vacían para protegerlas (supr = 2)."),
        "En toda fila, los conteos parciales entre 1 y 9 (o con complemento entre 1 y 9) y sus sumas quedan vacíos.",
        "Las filas de totales se calculan sobre todas las planillas. Cantidades en dólares, sin decimales.",
        "",
        "Hojas:",
        "  0: Tabla de control (totales del archivo de entrada)",
    ] + [f"  {clave}: {titulo}" for clave, titulo, _, _, _ in TABLAS if clave in resultados]
    if ausentes:
        lineas += ["", "Columnas no disponibles en los microdatos:", "  " + ", ".join(ausentes)]
    for i, l in enumerate(lineas, 1):
        ws.cell(row=i, column=1, value=l)
    ws["A1"].font = Font(bold=True, size=13)
    if etiqueta:
        ws["A4"].font = Font(bold=True, color="C00000")
    ws.column_dimensions["A"].width = 120

    cabecera = Font(bold=True)
    relleno = PatternFill("solid", fgColor="DDEBF7")
    colapsada = PatternFill("solid", fgColor="FFF2CC")
    vaciada = PatternFill("solid", fgColor="F2F2F2")
    for clave, titulo in [("0", "Tabla de control")] + [(k, t) for k, t, _, _, _ in TABLAS]:
        if clave not in resultados:
            continue
        t = resultados[clave]
        hoja = wb.create_sheet(clave)
        hoja["A1"] = f"Tabla {clave} — {titulo} — año contributivo {anio}" + (f" — {etiqueta}" if etiqueta else "")
        hoja["A1"].font = Font(bold=True, size=12)
        for j, c in enumerate(t.columns, 1):
            cell = hoja.cell(row=3, column=j, value=c)
            cell.font, cell.fill = cabecera, relleno
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        cols = list(t.columns)
        for i, fila in enumerate(t.itertuples(index=False), 4):
            d = dict(zip(cols, fila))
            es_total = any(isinstance(v, str) and v.startswith("Total") for v in fila)
            for j, (c, v) in enumerate(d.items(), 1):
                if isinstance(v, float) and np.isnan(v):
                    v = None
                elif isinstance(v, (np.floating, float)):
                    v = round(float(v))
                elif isinstance(v, np.integer):
                    v = int(v)
                cell = hoja.cell(row=i, column=j, value=v)
                if isinstance(v, int):
                    cell.number_format = "#,##0"
                if es_total:
                    cell.font = cabecera
                if d.get("nota") == "c":
                    cell.fill = colapsada
                elif d.get("supr", 0) > 0:
                    cell.fill = vaciada
        for j, c in enumerate(t.columns, 1):
            hoja.column_dimensions[get_column_letter(j)].width = max(12, min(28, len(str(c)) + 2))
        hoja.freeze_panes = "A4"
        nombre = "tabla_0_control" if clave == "0" else f"tabla_{clave}"
        t.to_csv(salida / f"{nombre}.csv", index=False, float_format="%.0f", encoding="utf-8")

    dic = wb.create_sheet("Diccionario")
    for j, c in enumerate(["columna", "descripción", "línea del Formulario 482 / anejo (formulario 2025)"], 1):
        cell = dic.cell(row=1, column=j, value=c)
        cell.font, cell.fill = cabecera, relleno
    for i, fila in enumerate(DICCIONARIO, 2):
        for j, v in enumerate(fila, 1):
            dic.cell(row=i, column=j, value=v)
    for col, w in zip("ABC", (40, 80, 45)):
        dic.column_dimensions[col].width = w

    ruta = salida / f"tabulaciones_482_{anio}.xlsx"
    wb.save(ruta)
    return ruta


# ============================================================================================== principal


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--anio", type=int, required=True, help="año contributivo")
    p.add_argument("--entrada", required=True, help="archivo de planillas (CSV, Parquet o Excel)")
    p.add_argument("--w2pr", help="archivo de comprobantes W-2PR (opcional; produce la Tabla I)")
    p.add_argument("--salida", default="06_salidas/salidas", help="carpeta de salida")
    p.add_argument("--supresion", choices=MODOS, default="colapsar", help="modalidad de supresión (por defecto: colapsar)")
    p.add_argument("--fecha-corte", default=None, help="fecha de corte de las planillas (texto, para el Léame)")
    p.add_argument("--etiqueta", default=None, help='marca para las salidas de prueba (p. ej. "PRUEBA")')
    args = p.parse_args(argv)

    salida = Path(args.salida)
    salida.mkdir(parents=True, exist_ok=True)
    log = Registro(salida / "log_ejecucion_pe.txt")
    import openpyxl

    log(f"PE tabulaciones (policyengine-pr) — versión {VERSION} — Python {platform.python_version()}, "
        f"pandas {pd.__version__}, numpy {np.__version__}, openpyxl {openpyxl.__version__} — {platform.system()} {platform.release()}")
    log(f"Inicio: {dt.datetime.now():%Y-%m-%d %H:%M:%S}  anio={args.anio}  entrada={args.entrada}  w2pr={args.w2pr or '—'}  "
        f"salida={args.salida}  supresion={args.supresion}" + (f"  etiqueta={args.etiqueta}" if args.etiqueta else ""))
    log(f"Parámetros: MIN_N={MIN_N}; tramos de IBA: {len(TRAMOS_IBA)}; tramos de ingreso ganado (D2): $2,500 hasta $55,000")

    df = leer(args.entrada)
    df, ausentes = preparar(df, COLS_OBLIG, SI_FALTA, log, "planillas")
    if "anio" in df.columns:
        antes = len(df)
        df = df[df["anio"] == args.anio]
        log(f"Filas leídas: {antes:,}; del año {args.anio}: {len(df):,}; columnas: {len([c for c in COLS_OBLIG + COLS_OPC if c in df.columns])} de {len(COLS_OBLIG) + len(COLS_OPC)}")
    else:
        log(f"Filas leídas: {len(df):,}; columnas: {len([c for c in COLS_OBLIG + COLS_OPC if c in df.columns])} de {len(COLS_OBLIG) + len(COLS_OPC)}")
    if df.empty:
        log("ERROR: ninguna planilla del año indicado. Se detiene.")
        sys.exit(1)

    w2 = None
    if args.w2pr:
        w2 = leer(args.w2pr)
        w2, aus_w2 = preparar(w2, COLS_W2PR_OBLIG, COLS_W2PR_OPC, log, "w2pr")
        if "anio" in w2.columns:
            w2 = w2[w2["anio"] == args.anio]
        ausentes += [f"w2pr.{c}" for c in aus_w2]
        log(f"Comprobantes W-2PR leídos: {len(w2):,}; personas distintas: {w2['id_persona'].nunique():,}")
    else:
        log("  AVISO: sin archivo W-2PR: no se producen las Tablas I ni I_edad")

    resultados = {"0": tabla_0(df, w2, args.anio)}
    resultados["0"]["nota"], resultados["0"]["supr"] = "", 0
    log(f"  Tabla 0_control: 1 fila; totales del archivo de entrada (sin supresión: todas las celdas tienen al menos "
        f"{MIN_N} planillas o se vacían)")
    prot0 = Protector(args.supresion)
    resultados["0"] = prot0.celdas(resultados["0"], "planillas", "anio")
    for clave, titulo, fn, fuente, necesarias in TABLAS:
        datos = df if fuente == "planillas" else w2
        if datos is None:
            log(f"  Tabla {clave}: omitida (sin archivo W-2PR)")
            continue
        faltan = [c for c in necesarias if c not in datos.columns]
        if faltan:
            log(f"  Tabla {clave}: omitida (faltan {', '.join(faltan)})")
            continue
        prot = Protector(args.supresion)
        t0 = time.time()
        try:
            t = fn(datos, prot)
        except Exception as e:  # noqa: BLE001 - una tabla fallida no impide las demás
            log(f"  Tabla {clave}: ERROR {e!r}")
            continue
        resultados[clave] = t
        log(f"  Tabla {clave}: {len(t):,} filas; filas colapsadas: {prot.filas_colapsadas}; filas vaciadas (<10): "
            f"{prot.filas_vaciadas}; vaciadas para proteger otras: {prot.filas_proteger}; conteos parciales vaciados: "
            f"{prot.celdas_parciales}; celdas vaciadas para proteger otras: {prot.celdas_proteger}; {time.time() - t0:.1f} s")

    ruta = escribir(args.anio, resultados, salida, ausentes, args.supresion, args.fecha_corte, args.etiqueta)
    log(f"Libro Excel: {ruta}")
    log(f"Fin: {dt.datetime.now():%Y-%m-%d %H:%M:%S}; duración {time.time() - log.t0:.1f} s")
    log.guardar()


if __name__ == "__main__":
    main()
