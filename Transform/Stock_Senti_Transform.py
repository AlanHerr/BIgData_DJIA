import pandas as pd


class StockSentiTransformer:
    """
    Aplica la limpieza y transformaciones especificadas para `stock_senti_analysis.csv`.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def transform_data(self) -> pd.DataFrame:
        df = self.df

        # Convertir Date a datetime
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        # Asegura que Label sea 0/1
        df['Label'] = pd.to_numeric(df['Label'], errors='coerce').astype('Int8')
        df = df.dropna(subset=['Label']).copy()
        df['Label'] = df['Label'].astype('int8').clip(0, 1)

        # Columna textual para Label
        df['Label_text'] = df['Label'].map({1: 'DJIA subió', 0: 'DJIA bajó'}).astype('category')

        # Añadir year, month, weekday
        df['year'] = df['Date'].dt.year
        df['month'] = df['Date'].dt.month
        df['weekday'] = df['Date'].dt.weekday

        # Eliminar filas con Date nula (si existen)
        df = df.dropna(subset=['Date']).copy()

        # Opcional: eliminar columnas con muchos nulos si las hay (no implementado automáticamente)

        self.df = df
        return self.df
