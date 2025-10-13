import pandas as pd
import sqlite3


class StockSentiLoader:
    def __init__(self, df: pd.DataFrame, output_csv: str):
        self.df = df
        self.output_csv = output_csv

    def to_csv(self, output_path: str = None):
        path = output_path or self.output_csv
        try:
            self.df.to_csv(path, index=False)
            print(f"Datos guardados en {path}")
        except Exception as e:
            print(f"Error al guardar CSV: {e}")

    def to_sqlite(self, db_path: str = "Extract/files/stock_senti_analysis.db", table_name: str = "stock_senti"):
        try:
            conn = sqlite3.connect(db_path)
            self.df.to_sql(table_name, conn, if_exists='replace', index=False)
            conn.close()
            print(f"Datos guardados en la base de datos SQLite: {db_path}, tabla: {table_name}")
        except Exception as e:
            print(f"Error al guardar en SQLite: {e}")
