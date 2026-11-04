# -*- coding: utf-8 -*-
"""
Validación de los archivos de entrada (planillas.csv y, si lo hay, w2pr.csv) ANTES de ejecutar pe_tabulaciones.py.

Uso:
    python validar_entrada.py --entrada planillas.csv [--w2pr w2pr.csv] [--anio 2023] [--informe validacion_entrada.txt]

Comprueba el contrato de datos (02_contrato_y_parametros/esquema_planillas.csv y esquema_w2pr.csv) y produce un informe con:
  1. codificación UTF-8 y columnas presentes y faltantes: las necesarias (si falta alguna es un ERROR) y las que amplían
     las salidas (si falta alguna es un AVISO que dice qué tabla o columna se omite); columnas no previstas; tipos;
  2. rangos y códigos válidos (estado_personal 1–4, edad 0–120, factor 0.92/0.95, indicadores 0/1, signos, máximo de la
     exención de jóvenes, etc.);
  3. coherencia interna (ingreso_neto ≤ iba; contribucion_regular ≈ (contribucion_tabla + ajuste_gradual) × factor;
     exención de jóvenes solo entre 16 y 26 años; crédito sin dependientes CT; W-2PR: exento_135 ≤ salarios);
  4. un resumen por año (planillas, sumas de las variables fiscales) para cuadrar con los totales de Hacienda.
Los avisos ("AVISO") no impiden la ejecución; los errores ("ERROR") sí deben corregirse antes.

Pantalla e informe. En pantalla aparece todo, con el número de filas afectadas y el resumen por año, para la revisión
interna de Hacienda. El informe guardado (--informe), que se entrega a Espacios Abiertos, repite las mismas comprobaciones
sin conteos de filas ni sumas (salvo el total de filas de cada archivo) y sin el resumen por año: la Tabla 0 de control
ya da esos totales, protegidos.
"""

import argparse
import datetime as dt
import sys
from pathlib import Path

import numpy as np
import pandas as pd

AQUI = Path(__file__).resolve().parent
ESQUEMAS = AQUI.parent / "02_contrato_y_parametros"
TEXTO = {"municipio", "id_persona"}


class Informe:
    def __init__(self):
        self.pantalla, self.archivo = [], []
        self.errores = self.avisos = 0

    def linea(self, texto, oculto=None):
        """`oculto`: versión sin cifras para el informe guardado (si es None, se guarda igual)."""
        print(texto)
        self.pantalla.append(texto)
        self.archivo.append(texto if oculto is None else oculto)

    def error(self, texto, n=None):
        self.errores += 1
        self.linea(f"ERROR: {texto}" + (f" ({n:,} filas)" if n is not None else ""), f"ERROR: {texto}")

    def aviso(self, texto, n=None):
        self.avisos += 1
        self.linea(f"AVISO: {texto}" + (f" ({n:,} filas)" if n is not None else ""), f"AVISO: {texto}")


def leer_esquema(nombre):
    e = pd.read_csv(ESQUEMAS / nombre, dtype=str).fillna("")
    return e.set_index("variable")


def es_utf8(path):
    try:
        with open(path, "rb") as f:
            while True:
                b = f.read(1 << 20)
                if not b:
                    return True
                b.decode("utf-8")
    except UnicodeDecodeError:
        return False


def validar_archivo(path, esquema, nombre, inf):
    inf.linea(f"\n{nombre}: {path}")
    if str(path).lower().endswith(".csv") and not es_utf8(path):
        inf.error(f"{nombre}: el archivo no está en UTF-8")
        return None
    df = pd.read_csv(path, low_memory=False) if str(path).lower().endswith(".csv") else pd.read_excel(path)
    inf.linea(f"  Filas: {len(df):,}   Columnas: {list(df.columns)}")
    oblig = [v for v, r in esquema.iterrows() if r["obligatoria"] == "si"]
    opc = [v for v, r in esquema.iterrows() if r["obligatoria"] != "si"]
    faltan = [c for c in oblig if c not in df.columns]
    if faltan:
        inf.error(f"{nombre}: faltan columnas necesarias: {', '.join(faltan)}")
    for c in [c for c in opc if c not in df.columns]:
        inf.aviso(f"{nombre}: falta {c}: {esquema.at[c, 'si_falta']}")
    ajenas = [c for c in df.columns if c not in esquema.index]
    if ajenas:
        inf.aviso(f"{nombre}: columnas no previstas (se ignoran): {', '.join(ajenas)}")
    inf.linea(f"  columnas del esquema presentes: {len([c for c in esquema.index if c in df.columns])} de {len(esquema)}")

    # tipos, rangos y signos
    for c in [c for c in esquema.index if c in df.columns and c not in TEXTO]:
        v = pd.to_numeric(df[c], errors="coerce")
        no_num = v.isna() & df[c].notna()
        if no_num.any():
            inf.error(f"{nombre}.{c}: valores no numéricos", int(no_num.sum()))
        r = esquema.loc[c]
        if r["tipo"] == "entero" and ((v.dropna() % 1) != 0).any():
            inf.error(f"{nombre}.{c}: debe ser entero", int(((v % 1) != 0).sum()))
        if r["minimo"] != "":
            m = (v < float(r["minimo"]))
            if m.any():
                inf.error(f"{nombre}.{c}: valores por debajo de {r['minimo']}", int(m.sum()))
        if r["maximo"] != "":
            m = (v > float(r["maximo"]))
            if m.any():
                inf.error(f"{nombre}.{c}: valores por encima de {r['maximo']}", int(m.sum()))
        if c in oblig and v.isna().any():
            inf.aviso(f"{nombre}.{c}: hay vacíos en una columna necesaria (el programa los trata como 0)", int(v.isna().sum()))
        df[c] = v
    if "factor" in df.columns:
        m = ~df["factor"].isin([0.92, 0.95]) & df["factor"].notna()
        if m.any():
            inf.error(f"{nombre}.factor: valores distintos de 0.92 y 0.95", int(m.sum()))
    if "estado_personal" in df.columns:
        m = ~df["estado_personal"].isin([1, 2, 3, 4])
        if m.any():
            inf.error(f"{nombre}.estado_personal: códigos fuera de 1–4", int(m.sum()))
    return df


def coherencia_planillas(df, inf):
    def chk(mask, texto, error=False):
        n = int(mask.fillna(False).sum())
        if n:
            (inf.error if error else inf.aviso)(f"planillas: {texto}", n)

    c = df.columns
    if {"ingreso_neto", "iba"} <= set(c):
        chk(df["ingreso_neto"] > df["iba"].clip(lower=0) + 1, "ingreso_neto mayor que iba")
    if {"contribucion_regular", "contribucion_tabla", "factor"} <= set(c):
        esperado = (df["contribucion_tabla"] + df.get("ajuste_gradual", 0)) * df["factor"]
        chk((df["contribucion_regular"] - esperado).abs() > 2, "contribucion_regular no es (contribucion_tabla + ajuste_gradual) × factor (±$2)")
    if {"exento_jovenes", "edad"} <= set(c):
        chk((df["exento_jovenes"] > 0) & ~df["edad"].between(16, 26), "exención de jóvenes fuera de 16–26 años")
    if {"credito_trabajo", "ct_dependientes", "num_dependientes"} <= set(c):
        chk(df["ct_dependientes"] > df["num_dependientes"], "ct_dependientes mayor que num_dependientes")
    if {"ct_ajustado", "ct_reclamado", "credito_trabajo"} <= set(c):
        chk((df["ct_ajustado"] == 0) & (df["ct_reclamado"] != df["credito_trabajo"]), "ct_reclamado distinto del concedido sin marca ct_ajustado")
    if {"exencion_dependientes", "num_dependientes"} <= set(c):
        chk((df["num_dependientes"] > 0) & (df["exencion_dependientes"] == 0), "dependientes sin exención por dependientes")
    if {"ingreso_bruto_factor", "factor"} <= set(c):
        chk((df["ingreso_bruto_factor"] <= 100_000) & (df["factor"] == 0.95), "factor 0.95 con ingreso bruto ≤ $100,000")
        chk((df["ingreso_bruto_factor"] > 100_000) & (df["factor"] == 0.92), "factor 0.92 con ingreso bruto > $100,000")


def coherencia_w2pr(w2, inf):
    if {"exento_135", "salarios"} <= set(w2.columns):
        m = w2["exento_135"] > w2["salarios"] + 1
        if m.any():
            inf.aviso("w2pr: exento_135 mayor que salarios", int(m.sum()))
    if "id_persona" in w2.columns:
        if w2["id_persona"].astype(str).str.fullmatch(r"\d{9}|\d{3}-\d{2}-\d{4}").any():
            inf.error("w2pr.id_persona: parece un número de seguro social; debe ser una clave seudónima")


def resumen(df, inf, anio):
    """Solo en pantalla (la Tabla 0 de control da estos totales protegidos)."""
    g = df.groupby("anio") if "anio" in df.columns else df.assign(anio=anio or "todas").groupby("anio")
    cols = [c for c in ["salarios", "iba", "ingreso_neto", "contribucion_regular", "responsabilidad", "credito_trabajo",
                        "creditos_federales", "exento_jovenes"] if c in df.columns]
    r = g.size().rename("planillas").to_frame().join(g[cols].sum())
    print("\nResumen por año (solo en pantalla, para la revisión interna de Hacienda):")
    print(r.to_string(float_format=lambda x: f"{x:,.0f}"))
    inf.archivo.append("\nResumen por año: solo en pantalla, para la revisión interna de Hacienda (la Tabla 0 de control da esos totales, protegidos).")


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--entrada", required=True)
    p.add_argument("--w2pr")
    p.add_argument("--anio", type=int)
    p.add_argument("--informe")
    a = p.parse_args()
    inf = Informe()
    inf.linea(f"VALIDACIÓN DE LOS ARCHIVOS DE ENTRADA (policyengine-pr) — {dt.datetime.now():%Y-%m-%d %H:%M}")
    inf.linea("(Informe para entregar a Espacios Abiertos: las comprobaciones sin conteos de filas ni sumas, salvo el total de filas; "
              "las cifras y el resumen por año se muestran solo en pantalla.)")
    df = validar_archivo(a.entrada, leer_esquema("esquema_planillas.csv"), "planillas", inf)
    if df is not None:
        if a.anio and "anio" in df.columns:
            m = df["anio"] != a.anio
            if m.any():
                inf.aviso(f"planillas: filas de otros años distintos de {a.anio} (el programa las descarta)", int(m.sum()))
        coherencia_planillas(df, inf)
        resumen(df, inf, a.anio)
    if a.w2pr:
        w2 = validar_archivo(a.w2pr, leer_esquema("esquema_w2pr.csv"), "w2pr", inf)
        if w2 is not None:
            coherencia_w2pr(w2, inf)
    inf.linea(f"\nRESULTADO: {inf.errores} error(es), {inf.avisos} aviso(s). "
              + ("El archivo cumple el contrato; revisar los avisos." if inf.errores == 0 else "Corregir los errores antes de ejecutar."))
    if a.informe:
        Path(a.informe).parent.mkdir(parents=True, exist_ok=True)
        with open(a.informe, "w", encoding="utf-8") as f:
            f.write("\n".join(inf.archivo) + "\n")
    sys.exit(1 if inf.errores else 0)


if __name__ == "__main__":
    main()
