import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class StockDataVisualizer:
    def __init__(self, df: pd.DataFrame, output_dir: str = "Visualization/images"):
        self.df = df
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def count_label_plot(self):
        orden = ["DJIA subió", "DJIA bajó"]
        counts = (self.df["Label_text"].value_counts().reindex(orden, fill_value=0))

        fig, ax = plt.subplots(figsize=(6, 6))
        bars = ax.bar(counts.index, counts.values, color=["blue", "orange"])  # azul y naranja
        ax.set_title("Conteo de días por etiqueta (DJIA subió / DJIA bajó)")
        ax.set_xlabel("Etiqueta")
        ax.set_ylabel("Número de días")

        for bar, val in zip(bars, counts.values):
            ax.annotate(f"{int(val):,}",
                        xy=(bar.get_x() + bar.get_width()/2, bar.get_height()),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha="center", va="bottom", fontsize=10)

        path = os.path.join(self.output_dir, "count_label.png")
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"Guardado: {path}")

    def yearly_freq_plot(self):
        pct_up = self.df.groupby("year")["Label"].mean() * 100.0
        pct_down = 100.0 - pct_up

        plot_df = pd.DataFrame({
            "Cerró ARRIBA del día anterior (Label=1)": pct_up,
            "Cerró IGUAL o ABAJO del día anterior (Label=0)": pct_down
        })

        fig, ax = plt.subplots(figsize=(12, 6))
        plot_df.plot(kind="bar", ax=ax)
        ax.set_title("DJIA por año: frecuencia de la dirección del cierre diario")
        ax.set_xlabel("Año")
        ax.set_ylabel("DJIA por año: % de cierres arriba vs igual/abajo")

        ax.legend(
            title="Dirección del cierre diario",
            loc="upper left",
            bbox_to_anchor=(1.02, 0.5),
            borderaxespad=0.0
        )

        path = os.path.join(self.output_dir, "yearly_freq.png")
        plt.tight_layout(rect=[0, 1.0, 1.0, 0.05])
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"Guardado: {path}")

    def heatmap_year_month(self):
        # Agrupar por año y mes y obtener % de días con Label=1
        table = (self.df.groupby(["year", "month"])["Label"]
                 .mean()
                 .mul(100)
                 .reset_index()
                 .pivot(index="year", columns="month", values="Label")
                 .sort_index())

        # Si la tabla está vacía, lanzar excepción para ser manejada por el caller
        if table.size == 0:
            raise ValueError("No hay datos para generar el heatmap de year/month")

        plt.figure()
        plt.imshow(table.values, aspect="auto", interpolation="nearest")
        plt.title("% de días con subida por año y mes")
        plt.xlabel("Mes")
        plt.ylabel("Año")
        plt.xticks(range(0,12), list(range(1,13)))
        plt.yticks(range(len(table.index)), table.index.tolist())
        cbar = plt.colorbar()
        cbar.set_label("% subidas")
        path = os.path.join(self.output_dir, "heatmap_year_month.png")
        plt.tight_layout()
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"Guardado: {path}")

    def month_bar_plot(self):
        pct_up = (self.df.groupby("month")["Label"].mean() * 100.0).reindex(range(1,13))
        pct_down = 100.0 - pct_up

        meses = np.arange(1, 13)
        width = 0.42

        fig, ax = plt.subplots(figsize=(11, 6))
        bars_up = ax.bar(meses - width/2, pct_up.values, width, label="DJIA subió (Label=1)", color="blue")
        bars_down = ax.bar(meses + width/2, pct_down.values, width, label="DJIA bajó (Label=0)", color="orange")

        ax.set_title("Por mes: % de días que sube vs. baja (agregado 2000–2016)")
        ax.set_xlabel("Mes")
        ax.set_ylabel("Porcentaje de días")
        ax.set_xticks(meses); ax.set_xticklabels(meses)

        for bars in (bars_up, bars_down):
            for b in bars:
                val = b.get_height()
                if not np.isnan(val):
                    ax.annotate(f"{val:.1f}%",
                                (b.get_x() + b.get_width()/2, val),
                                xytext=(0, 3), textcoords="offset points",
                                ha="center", va="bottom", fontsize=9)

        ax.legend(title="Dirección del cierre diario",
                  loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0.0)

        path = os.path.join(self.output_dir, "month_bar_plot.png")
        plt.tight_layout(rect=[0, 1.0, 1.0, 0.05])
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"Guardado: {path}")

    def weekday_bar_plot(self):
        orden = [0,1,2,3,4]
        nombres = {0:"Lun", 1:"Mar", 2:"Mié", 3:"Jue", 4:"Vie"}

        pct_up = (self.df.groupby("weekday")["Label"].mean() * 100.0).reindex(orden)
        pct_down = 100.0 - pct_up

        x = np.arange(len(orden))
        width = 0.42

        fig, ax = plt.subplots(figsize=(10, 6))
        bars_up = ax.bar(x - width/2, pct_up.values, width, label="DJIA subió (Label=1)", color="blue")
        bars_down = ax.bar(x + width/2, pct_down.values, width, label="DJIA bajó (Label=0)", color="orange")

        ax.set_title("Por día de la semana: % de días que sube vs. baja (agregado)")
        ax.set_xlabel("Día de la semana")
        ax.set_ylabel("Porcentaje de días")
        ax.set_xticks(x)
        ax.set_xticklabels([nombres[i] for i in orden])

        for bars in (bars_up, bars_down):
            for b in bars:
                val = b.get_height()
                if not np.isnan(val):
                    ax.annotate(f"{val:.1f}%",
                                (b.get_x() + b.get_width()/2, val),
                                xytext=(0, 3), textcoords="offset points",
                                ha="center", va="bottom", fontsize=9)

        ax.legend(title="Dirección del cierre diario",
                  loc="center left", bbox_to_anchor=(1.02, 0.5), borderaxespad=0.0)

        path = os.path.join(self.output_dir, "weekday_bar_plot.png")
        plt.tight_layout(rect=[0, 1.0, 1.0, 0.05])
        plt.savefig(path, dpi=150)
        plt.close()
        print(f"Guardado: {path}")

    def save_all(self):
        self.count_label_plot()
        self.yearly_freq_plot()
        try:
            self.heatmap_year_month()
        except Exception:
            print("No se pudo generar heatmap (posiblemente valores faltantes en year/month)")
        self.month_bar_plot()
        self.weekday_bar_plot()
