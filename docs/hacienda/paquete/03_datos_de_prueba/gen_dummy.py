# -*- coding: utf-8 -*-
"""
Genera los datos de prueba del paquete PE: planillas_dummy.csv (una fila por planilla, con todas las columnas de
esquema_planillas.csv) y w2pr_dummy.csv (una fila por comprobante W-2PR, esquema_w2pr.csv).

Son planillas INVENTADAS con distribuciones verosímiles y las reglas de 2025 aproximadas (tabla contributiva,
ajuste gradual, factor 92 %/95 %, Crédito por Trabajo de BI RI 26-01, exención de jóvenes). No son datos de Hacienda
y no sirven para ningún análisis: solo para probar el programa y mostrar el formato de las salidas.

Uso (no hace falta ejecutarlo; los CSV ya vienen en la carpeta):
    python gen_dummy.py [--n 25000] [--n-w2 40000] [--semilla 482] [--anio 2023]
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def planillas(n, anio, semilla):
    rng = np.random.default_rng(semilla)
    estado = rng.choice([1, 2, 3, 4], size=n, p=[0.62, 0.30, 0.03, 0.05])
    edad = np.clip(rng.normal(44, 15, n), 16, 95).astype(int)
    salarios = np.where(rng.random(n) < 0.85, np.exp(rng.normal(10.1, 0.85, n)), 0).round()
    negocio = np.where(rng.random(n) < 0.12, np.exp(rng.normal(9.3, 1.1, n)), 0).round()
    pensiones = np.where((edad >= 55) & (rng.random(n) < 0.4), np.exp(rng.normal(9.6, 0.6, n)), 0).round()
    intereses = np.where(rng.random(n) < 0.25, np.exp(rng.normal(5.5, 1.5, n)), 0).round()
    ganancia = np.where(rng.random(n) < 0.04, np.exp(rng.normal(8.5, 1.6, n)), 0).round()
    conducto = np.where(rng.random(n) < 0.03, np.exp(rng.normal(10.5, 1.3, n)), 0).round()
    retiro = np.where(rng.random(n) < 0.06, np.exp(rng.normal(8.8, 1.0, n)), 0).round()
    divorcio = np.where(rng.random(n) < 0.004, 6_000.0, 0)

    exento_jovenes = np.where((edad >= 16) & (edad <= 26), np.minimum(salarios, 40_000), 0)
    exento_pension = np.minimum(pensiones, np.where(edad >= 60, 15_000, 11_000))
    exento_dificil = np.where(rng.random(n) < 0.002, salarios, 0)
    salarios_trib = salarios - exento_jovenes - exento_dificil
    pensiones_trib = pensiones - exento_pension
    exento_total = exento_jovenes + exento_pension + exento_dificil

    iba = (salarios_trib + negocio + pensiones_trib + intereses + ganancia + conducto + retiro - divorcio).round()
    ingreso_bruto_factor = salarios + negocio + pensiones + intereses + ganancia + conducto + retiro

    ded_hip = np.where(rng.random(n) < 0.22, np.minimum(np.exp(rng.normal(8.6, 0.6, n)), 35_000), 0).round()
    ded_med = np.where(rng.random(n) < 0.05, np.exp(rng.normal(7.5, 0.8, n)), 0).round()
    ded_don = np.where(rng.random(n) < 0.15, np.exp(rng.normal(6.0, 1.0, n)), 0).round()
    ded_ira = np.where(rng.random(n) < 0.08, rng.choice([2_000, 5_000, 7_000], n), 0)
    ded_edu = np.where(rng.random(n) < 0.02, 1_000, 0)
    ded_pres = np.where(rng.random(n) < 0.06, np.exp(rng.normal(7.0, 0.7, n)), 0).round()
    ded_total = ded_hip + ded_med + ded_don + ded_ira + ded_edu + ded_pres

    num_dep = np.where(estado == 2, rng.choice([0, 1, 2, 3, 4], n, p=[0.35, 0.3, 0.22, 0.09, 0.04]),
                       rng.choice([0, 1, 2, 3, 4], n, p=[0.7, 0.18, 0.08, 0.03, 0.01]))
    ex_pers = np.where(estado == 2, 7_000, 3_500)
    ex_dep = num_dep * 2_500
    veterano = np.where(rng.random(n) < 0.04, 1_500, 0)
    ingreso_neto = np.maximum(iba - ded_total - ex_pers - ex_dep - veterano, 0)

    def tabla(x):
        return np.select([x <= 9_000, x <= 25_000, x <= 41_500, x <= 61_500],
                         [0, 0.07 * (x - 9_000), 1_120 + 0.14 * (x - 25_000), 3_430 + 0.25 * (x - 41_500)],
                         8_430 + 0.33 * (x - 61_500))

    contrib_tabla = tabla(ingreso_neto).round()
    ajuste = np.where(ingreso_neto > 500_000,
                      np.minimum(0.05 * (ingreso_neto - 500_000), 8_895 + 0.33 * (ex_pers + ex_dep + veterano)), 0).round()
    factor = np.where(ingreso_bruto_factor <= 100_000, 0.92, 0.95)
    contrib_regular = ((contrib_tabla + ajuste) * factor).round()
    cba_base = np.where(ingreso_neto > 25_000, negocio + pensiones_trib + intereses, 0)
    cba_rate = np.select([cba_base <= 25_000, cba_base <= 50_000, cba_base <= 75_000, cba_base <= 150_000, cba_base <= 250_000],
                         [0, 0.01, 0.03, 0.05, 0.10], 0.24)
    cba = (cba_base * cba_rate).round()
    exceso_cba = np.maximum(cba - contrib_regular, 0)
    credito_cba = np.where(rng.random(n) < 0.01, 200.0, 0)
    anejo_b = np.where(rng.random(n) < 0.015, np.exp(rng.normal(7.5, 1.0, n)), 0).round()
    otras_jur = np.where(rng.random(n) < 0.01, np.exp(rng.normal(6.5, 1.0, n)), 0).round()
    responsabilidad = np.maximum(contrib_regular + exceso_cba - otras_jur - credito_cba - anejo_b, 0)
    retenida = np.where(salarios > 0, np.minimum(contrib_regular * rng.uniform(0.7, 1.3, n), salarios * 0.3), 0).round()

    # Crédito por Trabajo (aproximación de las cuatro tablas de BI RI 26-01)
    ct_dep = np.minimum(num_dep, 3)
    ganado = salarios + np.maximum(negocio, 0) + pensiones_trib
    ct_max = np.select([ct_dep == 0, ct_dep == 1, ct_dep == 2], [1_656, 4_600, 6_900], 7_200)
    ct_in = np.select([ct_dep == 0, ct_dep == 1, ct_dep == 2], [0.0828, 0.2, 0.3], 0.3)
    ct_start = np.where(estado == 2, np.select([ct_dep == 0, ct_dep == 1, ct_dep == 2], [26_000, 37_000, 44_000], 44_000),
                        np.select([ct_dep == 0, ct_dep == 1, ct_dep == 2], [20_000, 31_000, 38_000], 38_000))
    ct = np.where(ganado < ct_start, np.minimum(ct_in * ganado, ct_max), np.maximum(ct_max - ct_in * (ganado - ct_start), 0)).round()
    ct = np.where((edad >= 19) & (intereses + ganancia <= 10_000) & (estado != 3), ct, 0)
    ct_ajustado = (ct > 0) & (rng.random(n) < 0.03)
    ct_reclamado = np.where(ct_ajustado, ct * rng.uniform(1.05, 1.6, n), ct).round()
    creditos_fed = np.where((num_dep > 0) & (salarios > 0), np.minimum(1_700 * np.minimum(num_dep, 3), salarios * 0.0765), 0).round()
    pago = retenida + ct + creditos_fed - responsabilidad
    municipios = [f"Municipio {i:02d}" for i in range(1, 79)]
    pesos = rng.pareto(1.2, 78) + 0.3
    municipio = rng.choice(municipios, n, p=pesos / pesos.sum())

    return pd.DataFrame({
        "anio": anio, "estado_personal": estado, "edad": edad, "municipio": municipio,
        "salarios": salarios, "intereses_dividendos": intereses, "pensiones": pensiones, "distribuciones_retiro": retiro,
        "ganancia_capital": ganancia, "entidades_conducto": conducto, "industria_negocio": negocio, "pension_divorcio": divorcio,
        "iba": iba, "deducciones": ded_total, "exencion_personal": ex_pers, "exencion_dependientes": ex_dep,
        "num_dependientes": num_dep, "exencion_veterano": veterano, "ingreso_neto": ingreso_neto,
        "contribucion_tabla": contrib_tabla, "ajuste_gradual": ajuste, "factor": factor, "ingreso_bruto_factor": ingreso_bruto_factor,
        "contribucion_regular": contrib_regular, "credito_otras_jurisdicciones": otras_jur, "exceso_cba": exceso_cba,
        "credito_cba": credito_cba, "creditos_anejo_b": anejo_b, "responsabilidad": responsabilidad, "retenida_salarios": retenida,
        "credito_trabajo": ct, "creditos_federales": creditos_fed, "sobrepago": np.maximum(pago, 0), "balance_pendiente": np.maximum(-pago, 0),
        "ded_hipoteca": ded_hip, "ded_medicos": ded_med, "ded_donativos": ded_don, "ded_ira": ded_ira, "ded_educativa": ded_edu,
        "ded_prestamos": ded_pres, "ded_total": ded_total, "exento_pension": exento_pension, "exento_jovenes": exento_jovenes,
        "exento_dificil_reclutamiento": exento_dificil, "exento_total": exento_total, "ct_dependientes": ct_dep,
        "ct_ingreso_ganado": np.where(ct > 0, ganado, 0), "ct_reclamado": ct_reclamado, "ct_ajustado": ct_ajustado.astype(int),
        "cba_ingreso_neto": cba_base, "cba_contribucion": cba,
    })


def w2pr(n, anio, semilla):
    rng = np.random.default_rng(semilla)
    personas = rng.integers(1, int(n * 0.75), n)
    edad = np.clip(rng.normal(40, 14, n), 16, 80).astype(int)
    salarios = np.exp(rng.normal(9.7, 0.9, n)).round()
    exento = np.where((edad <= 26) & (rng.random(n) < 0.8), np.minimum(salarios, 40_000), 0)
    retenida = np.where(salarios - exento > 15_000, (salarios - exento) * rng.uniform(0.03, 0.12, n), 0).round()
    return pd.DataFrame({"anio": anio, "id_persona": [f"P{p:07d}" for p in personas], "salarios": salarios,
                         "retenida": retenida, "exento_135": exento, "edad": edad})


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--n", type=int, default=25_000)
    p.add_argument("--n-w2", type=int, default=40_000)
    p.add_argument("--semilla", type=int, default=482)
    p.add_argument("--anio", type=int, default=2023)
    p.add_argument("--salida", default=str(Path(__file__).parent))
    a = p.parse_args()
    salida = Path(a.salida)
    planillas(a.n, a.anio, a.semilla).to_csv(salida / "planillas_dummy.csv", index=False, float_format="%.2f")
    w2pr(a.n_w2, a.anio, a.semilla + 17).to_csv(salida / "w2pr_dummy.csv", index=False, float_format="%.2f")
    print(f"Escritos planillas_dummy.csv ({a.n:,} filas) y w2pr_dummy.csv ({a.n_w2:,} filas) en {salida}")


if __name__ == "__main__":
    main()
