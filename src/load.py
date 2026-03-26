# src/load.py
import os

def load_data(df, export_format="CSV"):
    """
    Load/export data using PySpark
    """
    base_path = os.getcwd()   # project directory
    output_path = os.path.join(base_path, "data", "processed")

    if export_format == "CSV":
        df.write.mode("overwrite").csv(output_path, header=True)

    elif export_format == "JSON":
        df.write.mode("overwrite").json(output_path)

    elif export_format == "Parquet":
        df.write.mode("overwrite").parquet(output_path)

    return output_path