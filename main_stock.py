from Config import config
from Extract.Stock_Senti_Extract import StockSentiExtractor
from Transform.Stock_Senti_Transform import StockSentiTransformer
from Load.Stock_Senti_Load import StockSentiLoader
from Visualization.stock_visualization import StockDataVisualizer


def main():
    input_file = config.input_file
    output_file = config.output_file

    # Extract
    extractor = StockSentiExtractor(input_file)
    df = extractor.queries()

    # Transform
    transformer = StockSentiTransformer(df)
    df_clean = transformer.transform_data()

    # Load
    loader = StockSentiLoader(df_clean, output_file)
    loader.to_csv()
    loader.to_sqlite()

    # Visualization
    visualizer = StockDataVisualizer(df_clean)
    visualizer.save_all()

    print("ETL para stock_senti_analysis completado.")


if __name__ == '__main__':
    main()
