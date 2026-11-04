-- ============================================================================================
--  PLANTILLA de la consulta de extracción de SURI  ->  planillas.csv  y  w2pr.csv        (PASO 1)
--  Proyecto policyengine-pr (modelo público de microsimulación contributiva) — Espacios Abiertos
--  planillas.csv: una fila por planilla y año contributivo (2021–2024; 2025 cuando cierre), 51 columnas:
--    · 14 necesarias para ejecutar el programa (obligatoria = si en esquema_planillas.csv);
--    · 37 que amplían las salidas: si alguna no se puede extraer, se quita de la consulta y se anota en
--      la ficha; el programa omite solo la tabla o la columna que depende de ella (columna si_falta).
--  w2pr.csv (opcional): una fila por comprobante W-2PR, 6 columnas (esquema_w2pr.csv); produce la Tabla I.
--  Versión 2026-11-04 (rev. 1 del paquete PE).
-- ============================================================================================
--
--  ESTA CONSULTA NO FUNCIONA TAL CUAL. Espacios Abiertos no conoce las tablas de SURI:
--  todos los nombres de tablas y de campos son INVENTADOS y van marcados entre < >.
--  El equipo de Hacienda los sustituye por los reales, ejecuta la consulta dentro de sus
--  sistemas y exporta el resultado a un CSV. Ni la consulta final ni el CSV salen del
--  Departamento: Espacios Abiertos recibe solo las tablas agregadas de los pasos 3 y 4.
--
--  Lo que SÍ es fijo (lo comprueba 04_programas/validar_entrada.py en el paso 2):
--    1. los NOMBRES de las columnas de salida (los alias que siguen a "AS"), en minúsculas, sin ñ ni acentos;
--    2. una fila por planilla y año contributivo, solo la versión vigente de cada planilla;
--    3. las reglas de cada columna (esquema_planillas.csv): 0 cuando el concepto no aplica; celda vacía
--       solo cuando el dato no consta;
--    4. ningún identificador: ni número de seguro social, ni nombre, ni número de planilla. En w2pr.csv,
--       la única clave es id_persona, un hash con clave secreta que genera Hacienda y que el programa usa
--       solo para contar personas distintas (nunca aparece en las salidas).
--
--  Las líneas del Formulario 482 cambian entre años: las que se citan son las del formulario de 2025 y
--  Hacienda confirma la línea real de cada año en ficha_extraccion_plantilla.csv (se entrega en el paso 5).
--
--  Sintaxis: SQL genérico. Ajustar al motor de SURI, por ejemplo
--    año de una fecha:   YEAR(f) (SQL Server / MySQL)  |  EXTRACT(YEAR FROM f) (Oracle / PostgreSQL)
--    valor si nulo:      COALESCE(x, 0) (todos)  |  ISNULL(x, 0) (SQL Server)  |  NVL(x, 0) (Oracle)
--    hash con clave:     HASHBYTES('SHA2_256', <clave_secreta> + ssn) (SQL Server)
--                        encode(digest(<clave_secreta> || ssn, 'sha256'), 'hex') (PostgreSQL, pgcrypto)
-- ============================================================================================

-- ------------------------------------------------------------------------------------------ planillas.csv
SELECT
    p.<periodo_contributivo>                                    AS anio,                  -- año contributivo
    CASE p.<estado_personal>
         WHEN <codigo_individual>        THEN 1
         WHEN <codigo_casado_conjunta>   THEN 2
         WHEN <codigo_casado_separada>   THEN 3
         WHEN <codigo_computo_opcional>  THEN 4 END             AS estado_personal,       -- pág. 1
    p.<periodo_contributivo> - <YEAR>(p.<fecha_nacimiento_contribuyente_principal>)
                                                                AS edad,                  -- edad al cierre del año
    p.<municipio_direccion_residencial>                         AS municipio,             -- nombre o código; vacío si fuera de PR

    -- Ingresos (Encasillado 1)
    COALESCE(p.<salarios_1A>, 0) + COALESCE(p.<salarios_1B>, 0) + COALESCE(p.<salarios_federales_1C>, 0)
                                                                AS salarios,              -- 1A–1C, incluida la parte exenta
    COALESCE(p.<intereses_2C>, 0) + COALESCE(p.<dividendos_2D>, 0) AS intereses_dividendos, -- 2C, 2D
    COALESCE(p.<pensiones_2H>, 0)                               AS pensiones,             -- 2H (total, antes de la exención)
    COALESCE(p.<distribuciones_2E>, 0) + COALESCE(p.<distribuciones_2F>, 0) + COALESCE(p.<distribuciones_2L>, 0)
                                                                AS distribuciones_retiro, -- 2E, 2F, 2L
    COALESCE(p.<ganancia_capital_2B>, 0)                        AS ganancia_capital,      -- 2B
    COALESCE(p.<entidades_conducto_2K>, 0)                      AS entidades_conducto,    -- 2K
    COALESCE(p.<linea_2P>, 0) + COALESCE(p.<linea_2Q>, 0) + COALESCE(p.<linea_2R>, 0)
      + COALESCE(p.<linea_2S>, 0) + COALESCE(p.<linea_2T>, 0)   AS industria_negocio,     -- 2P–2T
    COALESCE(p.<pension_divorcio_4>, 0)                         AS pension_divorcio,      -- 4
    p.<ingreso_bruto_ajustado_5>                                AS iba,                   -- 5

    -- Deducciones, exenciones e ingreso neto
    COALESCE(p.<total_deducciones_6>, 0)                        AS deducciones,           -- 6
    COALESCE(p.<exencion_personal_7>, 0)                        AS exencion_personal,     -- 7
    COALESCE(p.<exencion_dependientes_8>, 0)                    AS exencion_dependientes, -- 8 (cantidad)
    COALESCE(p.<numero_dependientes_8>, 0)                      AS num_dependientes,      -- 8 (número)
    COALESCE(p.<exencion_veterano_9>, 0)                        AS exencion_veterano,     -- 9
    COALESCE(p.<ingreso_neto_13>, 0)                            AS ingreso_neto,          -- 13

    -- Cómputo de la contribución (Encasillado 3)
    COALESCE(p.<contribucion_tabla_14>, 0)                      AS contribucion_tabla,    -- 14
    COALESCE(p.<ajuste_gradual_15>, 0)                          AS ajuste_gradual,        -- 15
    CASE WHEN <ingreso_bruto_para_umbral> <= 100000 THEN 0.92 ELSE 0.95 END
                                                                AS factor,                -- Sección 1021.01(c)
    <ingreso_bruto_para_umbral>                                 AS ingreso_bruto_factor,  -- ingreso bruto usado para el umbral
    COALESCE(p.<contribucion_regular_17>, 0)                    AS contribucion_regular,  -- 17
    COALESCE(p.<credito_otras_jurisdicciones_18>, 0)            AS credito_otras_jurisdicciones, -- 18
    COALESCE(p.<exceso_cba_20>, 0)                              AS exceso_cba,            -- 20
    COALESCE(p.<credito_cba_21>, 0)                             AS credito_cba,           -- 21
    COALESCE(p.<creditos_anejo_b_25>, 0)                        AS creditos_anejo_b,      -- 25
    COALESCE(p.<responsabilidad_contributiva_26>, 0)            AS responsabilidad,       -- 26
    COALESCE(p.<retenida_salarios_27A>, 0)                      AS retenida_salarios,     -- 27A
    COALESCE(ct.<credito_concedido>, 0)                         AS credito_trabajo,       -- 27C (concedido)
    COALESCE(p.<creditos_federales_27D>, 0)                     AS creditos_federales,    -- 27D
    COALESCE(p.<sobrepago_29>, 0)                               AS sobrepago,             -- 29
    COALESCE(p.<balance_pendiente_31>, 0)                       AS balance_pendiente,     -- 31

    -- Anejo A
    COALESCE(a.<intereses_hipotecarios_1i>, 0)                  AS ded_hipoteca,
    COALESCE(a.<gastos_medicos_3>, 0)                           AS ded_medicos,
    COALESCE(a.<donativos_4>, 0)                                AS ded_donativos,
    COALESCE(a.<aportaciones_ira_7b>, 0)                        AS ded_ira,
    COALESCE(a.<cuentas_educativas_8b>, 0)                      AS ded_educativa,
    COALESCE(a.<prestamos_estudiantiles_9b>, 0)                 AS ded_prestamos,
    COALESCE(a.<total_11>, 0)                                   AS ded_total,

    -- Anejo IE
    COALESCE(ie.<exencion_pensiones>, 0)                        AS exento_pension,        -- Sección 1031.02(a)(13)
    COALESCE(ie.<linea_31>, 0)                                  AS exento_jovenes,        -- Ley 135-2014
    COALESCE(ie.<linea_32>, 0)                                  AS exento_dificil_reclutamiento,
    COALESCE(ie.<linea_45>, 0)                                  AS exento_total,

    -- Anejo CT
    COALESCE(ct.<numero_dependientes_cualificados>, 0)          AS ct_dependientes,
    COALESCE(ct.<ingreso_bruto_ganado_parte_II_3>, 0)           AS ct_ingreso_ganado,
    COALESCE(p.<credito_trabajo_reclamado_27C>, 0)              AS ct_reclamado,          -- tal como se radicó
    CASE WHEN COALESCE(p.<credito_trabajo_reclamado_27C>, 0) <> COALESCE(ct.<credito_concedido>, 0) THEN 1 ELSE 0 END
                                                                AS ct_ajustado,

    -- Anejo O
    COALESCE(o.<ingreso_neto_sujeto_cba>, 0)                    AS cba_ingreso_neto,
    COALESCE(o.<contribucion_basica_alterna>, 0)                AS cba_contribucion

FROM <tabla_planillas_482> p                                                   -- una fila por planilla y año (versión vigente)
LEFT JOIN <tabla_anejo_a>  a  ON a.<id_planilla>  = p.<id_planilla>
LEFT JOIN <tabla_anejo_ie> ie ON ie.<id_planilla> = p.<id_planilla>
LEFT JOIN <tabla_anejo_ct> ct ON ct.<id_planilla> = p.<id_planilla>
LEFT JOIN <tabla_anejo_o>  o  ON o.<id_planilla>  = p.<id_planilla>
WHERE p.<periodo_contributivo> BETWEEN 2021 AND 2024
  AND p.<version_de_la_planilla> = <codigo_version_vigente>;                   -- una sola versión por planilla

-- ------------------------------------------------------------------------------------------ w2pr.csv (opcional)
SELECT
    w.<periodo_contributivo>                                    AS anio,
    <HASH_SHA256>(<clave_secreta_de_hacienda> || w.<ssn_empleado>) AS id_persona,       -- clave seudónima; la clave secreta no sale de Hacienda
    COALESCE(w.<salarios_comisiones_propinas>, 0)               AS salarios,
    COALESCE(w.<contribucion_retenida>, 0)                      AS retenida,
    CASE WHEN w.<codigo_encasillado_16> = 'E' THEN COALESCE(w.<cantidad_encasillado_16>, 0) ELSE 0 END
                                                                AS exento_135,            -- encasillado 16, código E
    w.<periodo_contributivo> - <YEAR>(w.<fecha_nacimiento_empleado>) AS edad
FROM <tabla_comprobantes_w2pr> w
WHERE w.<periodo_contributivo> BETWEEN 2021 AND 2024;
-- Se incluyen los comprobantes de todas las personas, rindan o no planilla.

-- ============================================================================================
--  COMPROBACIONES RÁPIDAS antes de exportar (agregados; sirven para cuadrar con validar_entrada.py y la Tabla 0)
-- ============================================================================================
--  SELECT anio, COUNT(*), SUM(salarios), SUM(iba), SUM(ingreso_neto), SUM(contribucion_regular), SUM(responsabilidad),
--         SUM(credito_trabajo), SUM(creditos_federales), SUM(exento_jovenes)
--  FROM ( ...la consulta de arriba... ) t GROUP BY anio ORDER BY anio;
--    * un recuento por año que Hacienda reconozca como el número de planillas vigentes de ese año;
--    * estado_personal solo 1–4; factor solo 0.92 o 0.95; ct_ajustado solo 0/1;
--    * ingreso_neto <= iba; contribucion_regular ≈ (contribucion_tabla + ajuste_gradual) × factor;
--    * en w2pr.csv: SELECT anio, COUNT(*), COUNT(DISTINCT id_persona) ...
--  Estos totales por año se anotan en la ficha de extracción.

-- ============================================================================================
--  EXPORTACIÓN A CSV (formato que lee el programa)
-- ============================================================================================
--  * Codificación UTF-8, separador coma, una fila de encabezado con los nombres de arriba.
--  * Punto decimal; sin separadores de miles, sin símbolo de moneda, sin comillas.
--  * Celda vacía para los NULL (no escribir NULL, NA ni un punto).
--  * Un archivo por año (planillas_2023.csv, w2pr_2023.csv) o uno solo con la columna anio.
--  * El orden de las columnas no importa; los nombres sí.
--  Siguiente paso:  python 04_programas/validar_entrada.py --entrada planillas_2023.csv --w2pr w2pr_2023.csv --informe 06_salidas/validacion_entrada.txt
