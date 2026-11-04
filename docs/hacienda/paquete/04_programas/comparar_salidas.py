# -*- coding: utf-8 -*-
"""
Compara dos carpetas de salidas de pe_tabulaciones.py (p. ej., las salidas de referencia y las de una nueva ejecución)
archivo por archivo.
Uso: python comparar_salidas.py carpeta_A carpeta_B [tolerancia_absoluta=0.5]
Une cada tabla por sus columnas de texto (grupo y etiqueta) y reporta: columnas, filas, celdas vacías y la diferencia
numérica máxima. Termina con "RESULTADO GLOBAL: IDÉNTICAS dentro de la tolerancia" cuando todo coincide.
"""

import glob
import os
import sys

import numpy as np
import pandas as pd


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    a, b = sys.argv[1], sys.argv[2]
    tol = float(sys.argv[3]) if len(sys.argv) > 3 else 0.5
    archivos = sorted({os.path.basename(f) for f in glob.glob(os.path.join(a, "tabla_*.csv"))}
                      | {os.path.basename(f) for f in glob.glob(os.path.join(b, "tabla_*.csv"))})
    todo_ok, n = True, 0
    for f in archivos:
        pa, pb = os.path.join(a, f), os.path.join(b, f)
        if not (os.path.exists(pa) and os.path.exists(pb)):
            print(f"  {f}: solo en {'A' if os.path.exists(pa) else 'B'}")
            todo_ok = False
            continue
        ta, tb = pd.read_csv(pa, dtype={"nota": str}), pd.read_csv(pb, dtype={"nota": str})
        if list(ta.columns) != list(tb.columns):
            print(f"  {f}: columnas distintas: {sorted(set(ta.columns) ^ set(tb.columns))}")
            todo_ok = False
            continue
        if len(ta) != len(tb):
            print(f"  {f}: filas {len(ta)} frente a {len(tb)}")
            todo_ok = False
            continue
        claves = [c for c in ta.columns if not pd.api.types.is_numeric_dtype(ta[c]) and c != "nota"]
        if not claves:  # tablas sin columnas de texto (la de control): se comparan fila a fila
            ta, tb = ta.assign(_fila=range(len(ta))), tb.assign(_fila=range(len(tb)))
            claves = ["_fila"]
        m = ta.merge(tb, on=claves, how="outer", suffixes=("_a", "_b"), indicator=True)
        if (m["_merge"] != "both").any():
            print(f"  {f}: {int((m['_merge'] != 'both').sum())} fila(s) sin pareja")
            todo_ok = False
            continue
        num = [c for c in ta.columns if pd.api.types.is_numeric_dtype(ta[c]) and c not in ("nota", "_fila")]
        dif_max, vac = 0.0, 0
        for c in num:
            va, vb = m[f"{c}_a"], m[f"{c}_b"]
            vac += int((va.isna() != vb.isna()).sum())
            d = (va - vb).abs().max()
            if pd.notna(d):
                dif_max = max(dif_max, float(d))
        nota = (m["nota_a"].fillna("") != m["nota_b"].fillna("")).sum() if "nota" in ta.columns else 0
        ok = dif_max <= tol and vac == 0 and nota == 0
        todo_ok &= ok
        n += 1
        print(f"  {f}: {'OK' if ok else 'DIFIERE'}; filas {len(ta)}; dif. máx. {dif_max:,.4g}; vacíos distintos {vac}; notas distintas {nota}")
    print(f"\nRESULTADO GLOBAL: {'IDÉNTICAS dentro de la tolerancia' if todo_ok else 'HAY DIFERENCIAS'}, {n} tablas")
    sys.exit(0 if todo_ok else 1)


if __name__ == "__main__":
    main()
