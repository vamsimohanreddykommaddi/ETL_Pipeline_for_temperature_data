import os
import tempfile
from pyspark.sql import SparkSession


def get_spark_session():
    spark = SparkSession.builder \
        .appName("Temperature_ETL_Pipeline") \
        .getOrCreate()
    return spark


def extract_data(uploaded_file):
    spark = get_spark_session()

    # Create temp file safely
    temp_dir = tempfile.gettempdir()
    temp_path = os.path.join(temp_dir, "temperature.csv")

    # Save uploaded file
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Read with Spark
    df = spark.read.csv(temp_path, header=True, inferSchema=True)

    return df