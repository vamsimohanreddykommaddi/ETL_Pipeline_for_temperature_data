from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

def run_pipeline(uploaded_file, handle_missing=True, pivot_data=True, export_format="csv"):
    """
    Complete ETL pipeline
    """

    # Extract
    df = extract_data(uploaded_file)

    # Transform
    processed_df = transform_data(df, handle_missing, pivot_data)

    # Load
    output_data = load_data(processed_df, export_format)

    return processed_df, output_data