# src/transform.py

from pyspark.sql.functions import col, expr


def transform_data(df, handle_missing=True, pivot_data=True):
    """
    Transform data using PySpark
    """

    # Handle missing values
    if handle_missing and "ISO2" in df.columns:
        df = df.fillna({"ISO2": "Unknown"})

    if pivot_data:
        # Identify temperature columns (F1961, F1962...)
        temp_cols = [c for c in df.columns if c.startswith("F")]

        # Create stack expression dynamically
        stack_expr = ", ".join([f"'{c}', {c}" for c in temp_cols])

        df_pivot = df.selectExpr(
            "ObjectId", "Country", "ISO3",
            f"stack({len(temp_cols)}, {stack_expr}) as (Year, Temperature)"
        )

        # Convert Year (F1961 → 1961)
        df_pivot = df_pivot.withColumn(
            "Year",
            expr("int(substring(Year, 2, 4))")
        )

        # Drop null temperature
        df_pivot = df_pivot.filter(col("Temperature").isNotNull())

        return df_pivot

    return df