# ETL: stock_senti_analysis (DJIA Sentiment)

Proyecto: pipeline ETL en Python para el dataset "stock_senti_analysis.csv" (sentiment analysis for Dow Jones DJIA stock).

Este repositorio contiene un pipeline modular (Extract / Transform / Load / Visualization) que lee un CSV con titulares (Top1..Top25) y una etiqueta binaria (`Label`) que indica si el DJIA subió o bajó en el cierre diario. El pipeline limpia y transforma los datos, guarda un CSV limpio y una base de datos SQLite y genera varias visualizaciones EDA.

---

Tabla de contenidos

- Estructura del proyecto
- Requisitos e instalación
- Ejecución
- Variables de entorno / Config
- Artefactos generados
- Notas sobre el dataset
- Buenas prácticas y pruebas mínimas
- Autor

---

## Estructura del proyecto

```
BIgData_DJIA/
├── Config/
│   └── config.py                # Rutas de entrada/salida
├── Extract/
│   ├── Stock_Senti_Extract.py   # Lector CSV
│   └── files/
│       ├── stock_senti_analysis.csv
│       ├── stock_senti_analysis_cleaned.csv (generado)
│       └── stock_senti_analysis.db (generado)
├── Transform/
│   └── Stock_Senti_Transform.py  # Limpieza y transformaciones
├── Load/
│   └── Stock_Senti_Load.py       # Guardado CSV y SQLite
├── Visualization/
│   └── stock_visualization.py    # Genera gráficas y las guarda en Visualization/images/
├── main_stock.py                 # Orquestador ETL para stock_senti_analysis
├── requirements.txt
└── README.md
```

---

## Requisitos e instalación

Requiere Python 3.8+ (se recomienda 3.10+). Instala dependencias desde `requirements.txt`.

```bash
# Crear y activar un entorno virtual (opcional pero recomendado)
python3 -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

---

## Ejecución

Ejecuta el pipeline ETL para `stock_senti_analysis`:

```bash
python main_stock.py
```

Salida esperada (artefactos generados):
- `Extract/files/stock_senti_analysis_cleaned.csv` (CSV limpio)
- `Extract/files/stock_senti_analysis.db` (SQLite, tabla `stock_senti`)
- Imágenes en `Visualization/images/`:
	- `count_label.png`
	- `yearly_freq.png`
	- `heatmap_year_month.png`
	- `month_bar_plot.png`
	- `weekday_bar_plot.png`

---

## Variables de configuración

Rutas de entrada/salida están en `Config/config.py`:

```python
input_file = "Extract/files/stock_senti_analysis.csv"
output_file = "Extract/files/stock_senti_analysis_cleaned.csv"
```

Modifica esas rutas si mueves archivos o quieres cambiar el nombre de salida.

---

## Notas sobre el dataset

- Columnas principales:
	- `Date` (fecha)
	- `Label` (0/1) — 1 indica que el DJIA subió respecto al cierre del día anterior; 0 indica que bajó.
	- `Top1`..`Top25` — titulares o fragments de noticias (texto) por fila.
- Rango temporal: el CSV contiene registros históricos (la muestra empieza en 2000 en el archivo incluido).
- Tamaño: alrededor de 6000+ filas (ver `wc -l Extract/files/stock_senti_analysis.csv`).

---

## Qué hace cada módulo

- `Extract/Stock_Senti_Extract.py`:
	- Lee el CSV con `pd.read_csv(..., encoding='ISO-8859-1')` y devuelve DataFrame.

- `Transform/Stock_Senti_Transform.py`:
	- Convierte `Date` a datetime.
	- Normaliza `Label` a int y lo valida (drop de nulos en `Label`).
	- Crea `Label_text` ("DJIA subió" / "DJIA bajó").
	- Extrae `year`, `month`, `weekday`.
	- Elimina filas con `Date` nulo.

- `Load/Stock_Senti_Load.py`:
	- Guarda CSV limpio y exporta a SQLite (`Extract/files/stock_senti_analysis.db`) con tabla `stock_senti`.

- `Visualization/stock_visualization.py`:
	- Genera y guarda las 5 gráficas EDA en `Visualization/images/`.

- `main_stock.py`:
	- Orquesta extract -> transform -> load -> visualize.

---


## Interpretación rápida de las gráficas

A continuación se ofrecen breves captions para cada una de las imágenes generadas en `Visualization/images/`. Puedes copiarlas directamente en informes o presentaciones.

1) `count_label.png` — Distribución de la etiqueta (Label)
- Qué muestra: barras con el conteo de días etiquetados como 0 (DJIA bajó) y 1 (DJIA subió).
- Cómo interpretarlo: permite ver si la clase 0/1 está balanceada o existe sesgo. Si una clase domina, los modelos deberán manejar desbalance (re-muestreo, pesos, métricas robustas).
- Utilidad práctica: guía la elección de métricas (por ejemplo, F1 en lugar de accuracy) y decisiones de muestreo o regularización.

2) `yearly_freq.png` — Frecuencia anual de días con Label=1 (porcentaje)
- Qué muestra: evolución año a año del porcentaje de días en los que el DJIA subió.
- Cómo interpretarlo: identifica periodos con mayor o menor probabilidad de subidas (picos y valles) y posibles cambios de régimen económico. Útil para analizar drift temporal.
- Utilidad práctica: si la distribución cambia con el tiempo, los modelos deberían validar por año (time-based split) y considerar features temporales o reentrenamiento frecuente.

3) `heatmap_year_month.png` — Heatmap año vs mes (porcentaje de Label=1)
- Qué muestra: mapa de calor que combina año (eje y) y mes (eje x), con el color representando el porcentaje de días con Label=1.
- Cómo interpretarlo: revela patrones estacionales dentro de cada año y años atípicos (por ejemplo, meses consistentemente alcistas o bajistas). Identifica estacionalidad y excepciones puntuales.
- Utilidad práctica: sugiere incluir variables estacionales (mes, trimestre) en el modelo y evaluar si ciertos meses tienen mayor predictive power.

4) `month_bar_plot.png` — Porcentaje promedio por mes (agregado sobre todos los años)
- Qué muestra: barras ordenadas con el promedio del porcentaje de días alcistas por mes (enero a diciembre).
- Cómo interpretarlo: facilita ver la estacionalidad promedio (meses con mayor propensión a subidas). Comparar con el heatmap ayuda a distinguir patrones consistentes de outliers.
- Utilidad práctica: si hay meses con comportamiento marcado, crear features categóricas/encodings para mes puede mejorar rendimiento.

5) `weekday_bar_plot.png` — Porcentaje promedio por día de la semana
- Qué muestra: barras con el porcentaje promedio de días alcistas por día de la semana (lunes–viernes).
- Cómo interpretarlo: detecta efectos de día de la semana (por ejemplo, los lunes pueden ser más volátiles). Útil para detectar sesgos operativos o ventanas de negociación.
- Utilidad práctica: incluir día de la semana en el modelo o diseñar reglas de negocio (backtesting por día) puede mejorar interpretabilidad.



## Autor
AlanHerr

---