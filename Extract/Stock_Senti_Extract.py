import pandas as pd


class StockSentiExtractor:
    """
    Extrae el CSV de `stock_senti_analysis.csv` y devuelve un DataFrame.
    """
    def __init__(self, csv_path: str):
        self.csv = csv_path
        self.data = None

    def queries(self):
        """Lee el CSV (ISO-8859-1 por compatibilidad con el original).
        Devuelve un pandas.DataFrame sin modificar.
        """
        self.data = pd.read_csv(self.csv, encoding='ISO-8859-1')
        return self.data

    def response(self):
        if self.data is None:
            raise ValueError("Los datos no han sido cargados. Llama a queries() primero.")
        return self.data.head()
