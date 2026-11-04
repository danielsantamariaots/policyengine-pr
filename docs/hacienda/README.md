# Paquete para Hacienda

Material que acompaña a `docs/solicitud_datos_hacienda.docx`.

| Archivo | Qué es |
|---|---|
| `tabulaciones_hacienda.py` | Guion que Hacienda ejecuta sobre sus propios microdatos. Produce las Tablas A–J de la carta, aplica la regla de supresión (filas con menos de 10 planillas colapsadas en el tramo contiguo, totales conservados, marca "c") y escribe un libro Excel más un CSV por tabla. |
| `ejemplo/tabulaciones_482_2023_SINTETICO.xlsx` | Libro Excel producido por el guion sobre datos **sintéticos** (`--sintetico`). Muestra el formato exacto de cada tabla. **No son datos de Hacienda.** |
| `ejemplo/tabla_*_2023_SINTETICO.csv` | Las mismas tablas en CSV. |

## Qué enviar a Hacienda

El `.docx` de la carta, `tabulaciones_hacienda.py` y el `.xlsx` sintético.

## Probar localmente

```bash
python docs/hacienda/tabulaciones_hacienda.py --anio 2023 --sintetico --salida docs/hacienda/ejemplo
```

Requiere `pandas` y `openpyxl` (`uv pip install openpyxl` en el `.venv` del repo).

## Lo que Hacienda tiene que cambiar

Solo la sección **CONFIGURACIÓN** al inicio del guion: el nombre de cada
columna en sus archivos (`COLUMNAS_PLANILLAS`, `COLUMNAS_W2PR`) y, si lo
desean, `MIN_PLANILLAS`. Una columna que no exista se pone en `None`; el
guion la trata como cero y lo anota en la hoja "Léame" del libro.

## Verificación incluida

Sobre los datos sintéticos, ninguna fila de ninguna tabla queda con menos
de 10 planillas y los totales de cada columna coinciden con la suma de las
filas (comprobado al generar el ejemplo).
