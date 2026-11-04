# -*- coding: utf-8 -*-
"""
Verificación de las salidas de pe_tabulaciones.py ANTES de entregarlas (apoyo a la revisión de confidencialidad de Hacienda).

Uso:
    python verificar_salidas.py --salida salidas [--informe verificacion_salidas.txt]

Trabaja solo con los archivos de salida (como lo haría quien revisa) y comprueba, tabla por tabla:
  1. columnas: existen «nota» y «supr»; ninguna columna de identificación (ssn, nombre, id_persona, id_planilla);
  2. conteos: todo conteo de planillas o comprobantes (planillas, planillas_*, comprobantes, personas_distintas) es 0, está
     vacío o es >= 10; en cada fila, ningún conteo parcial deja un complemento (n − parcial) entre 1 y 9;
  3. filas: las filas con supr > 0 en modalidad «vaciar» tienen todos sus valores vacíos; en modalidad «colapsar» no hay
     ninguna fila con menos de 10 planillas; las sumas están vacías cuando su conteo parcial lo está;
  4. totales: en cada grupo, la diferencia entre el total publicado y la suma de las filas publicadas es 0 (colapsar) o
     corresponde a dos o más filas vacías y a 10 o más planillas (vaciar); lo mismo, columna por columna, para los
     conteos parciales vacíos de las filas publicadas;
  5. el registro log_ejecucion_pe.txt existe y nombra las mismas tablas.
Imprime un resumen por archivo. Es una segunda comprobación; no sustituye la revisión de Hacienda.
"""

import argparse
import glob
import os
import re
import sys

import numpy as np
import pandas as pd

MIN_N = 10
CONTEOS_FILA = ("planillas", "planillas_ajustadas", "comprobantes")
PROHIBIDAS = re.compile(r"ssn|seguro_social|nombre|id_persona|id_planilla|direccion", re.I)
DEPENDIENTES_EXTRA = {
    "planillas_num_dependientes": ["num_dependientes", "exencion_dependientes"],
    "planillas_92": ["contribucion_regular_92"],
    "planillas_95": ["contribucion_regular_95"],
    "personas_distintas": [],
}


def dependientes(p, cols):
    c = DEPENDIENTES_EXTRA.get(p, [p[len("planillas_"):]] if p.startswith("planillas_") else [])
    return [x for x in c if x in cols]


def entre_1_y_9(v):
    v = pd.to_numeric(v, errors="coerce")
    return (v > 0) & (v < MIN_N)


def verificar_tabla(path, inf):
    nombre = os.path.basename(path).replace(".csv", "")
    t = pd.read_csv(path, dtype={"nota": str})
    incidencias = []
    cols = list(t.columns)
    if "supr" not in cols or "nota" not in cols:
        incidencias.append("faltan las columnas nota/supr")
    malas = [c for c in cols if PROHIBIDAS.search(c)]
    if malas:
        incidencias.append(f"columnas de identificación: {malas}")
    col_n = next((c for c in CONTEOS_FILA if c in cols), None)
    if col_n is None:
        incidencias.append("sin columna de conteo de la fila")
        inf.append(f"  {nombre}: {'; '.join(incidencias)}")
        return len(incidencias) == 0, incidencias
    etiqueta = next((c for c in cols if c not in ("anio",) and not pd.api.types.is_numeric_dtype(t[c]) and c not in ("nota", "supr")), None)
    es_total = t[etiqueta].astype(str).str.startswith("Total") if etiqueta else pd.Series(False, index=t.index)
    grupo = None
    if etiqueta:
        no_num = [c for c in cols if not pd.api.types.is_numeric_dtype(t[c]) and c not in ("nota", "supr")]
        if len(no_num) > 1:
            grupo = no_num[0]
            etiqueta = no_num[1]
    conteos = [c for c in cols if c in CONTEOS_FILA or c.startswith("planillas_") or c == "personas_distintas"]
    numericas = [c for c in cols if pd.api.types.is_numeric_dtype(t[c]) and c not in ("supr", "anio")]

    # 2. conteos entre 1 y 9 y complementos
    for c in conteos:
        m = entre_1_y_9(t[c])
        if m.any():
            incidencias.append(f"{c}: {int(m.sum())} conteo(s) entre 1 y 9")
        if c != col_n and c != "personas_distintas":
            comp = pd.to_numeric(t[col_n], errors="coerce") - pd.to_numeric(t[c], errors="coerce")
            m = (comp > 0) & (comp < MIN_N)
            if m.any():
                incidencias.append(f"{c}: {int(m.sum())} complemento(s) entre 1 y 9")
        for d in dependientes(c, cols):
            m = t[c].isna() & t[d].notna() & ~es_total
            if m.any():
                incidencias.append(f"{d}: {int(m.sum())} suma(s) publicada(s) con su conteo {c} vacío")
    # 3. filas vaciadas
    vac = (t["supr"] > 0) & t[col_n].isna() if "supr" in cols else pd.Series(False, index=t.index)
    if vac.any():
        m = t.loc[vac, numericas].notna().any(axis=1)
        if m.any():
            incidencias.append(f"{int(m.sum())} fila(s) vaciada(s) con algún valor publicado")
    # 4. totales
    claves = t[grupo].astype(str) if grupo else pd.Series("", index=t.index)
    for g, idx in t.groupby(claves, sort=False).groups.items():
        cuerpo = [i for i in idx if not es_total[i]]
        tot = [i for i in idx if es_total[i] and (grupo is None or t.at[i, etiqueta] == "Total")]
        if not tot:
            continue
        for c in [col_n] + [x for x in conteos if x != col_n and x != "personas_distintas"]:
            total = pd.to_numeric(t.loc[tot[0], c], errors="coerce")
            if pd.isna(total):
                continue
            v = pd.to_numeric(t.loc[cuerpo, c], errors="coerce")
            vacios = int(v.isna().sum())
            dif = total - v.sum()
            if vacios == 0 and abs(dif) > 0.5:
                incidencias.append(f"{c} ({g or 'tabla'}): el total no coincide con la suma de las filas (dif. {dif:,.0f})")
            elif vacios == 1:
                incidencias.append(f"{c} ({g or 'tabla'}): una sola celda vacía, deducible del total")
            elif vacios >= 2 and 0 < dif < MIN_N:
                incidencias.append(f"{c} ({g or 'tabla'}): las celdas vacías suman {dif:.0f} (entre 1 y 9)")
    ok = not incidencias
    celdas_vacias = int(t[numericas].isna().sum().sum())
    minimo = pd.to_numeric(t[col_n], errors="coerce")
    minimo = minimo[minimo > 0].min()
    inf.append(f"  {nombre}: {'OK' if ok else 'INCIDENCIAS'}; filas {len(t):,}; columnas {len(cols)}; conteo mínimo distinto de cero "
               f"{minimo:.0f}; celdas vacías {celdas_vacias}" + ("" if ok else "; " + "; ".join(incidencias)))
    return ok, incidencias


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--salida", required=True)
    p.add_argument("--informe")
    a = p.parse_args()
    inf = [f"VERIFICACIÓN DE SALIDAS (policyengine-pr) — carpeta {a.salida}"]
    archivos = sorted(glob.glob(os.path.join(a.salida, "tabla_*.csv")))
    if not archivos:
        print("No hay archivos tabla_*.csv en la carpeta.")
        sys.exit(1)
    total_inc = 0
    for f in archivos:
        ok, inc = verificar_tabla(f, inf)
        total_inc += len(inc)
    log = os.path.join(a.salida, "log_ejecucion_pe.txt")
    if os.path.exists(log):
        with open(log, encoding="utf-8") as fh:
            en_log = set(re.findall(r"Tabla (\S+?):", fh.read()))
        en_carpeta = {os.path.basename(f)[6:-4].replace("0_control", "0_control") for f in archivos}
        faltan = {c for c in en_carpeta if c not in en_log and c != "0_control"}
        inf.append(f"\nREGISTRO: log_ejecucion_pe.txt presente" + (f"; tablas sin mención en el registro: {sorted(faltan)}" if faltan else ""))
        total_inc += len(faltan)
    else:
        inf.append("\nREGISTRO: falta log_ejecucion_pe.txt")
        total_inc += 1
    inf.append(f"\nRESULTADO: {'sin incidencias' if total_inc == 0 else f'{total_inc} incidencia(s): revisar antes de entregar'}")
    texto = "\n".join(inf)
    print(texto)
    if a.informe:
        with open(a.informe, "w", encoding="utf-8") as fh:
            fh.write(texto + "\n")
    sys.exit(1 if total_inc else 0)


if __name__ == "__main__":
    main()
