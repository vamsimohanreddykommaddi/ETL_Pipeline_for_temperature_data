import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io

# ✅ PySpark ETL modules
from src.extract import extract_data
from src.transform import transform_data
from src.load import load_data

# Page configuration
st.set_page_config(
    page_title="Temperature ETL Pipeline",
    page_icon="🌡️",
    layout="wide"
)

# Custom CSS (UNCHANGED)
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Session state
if 'processed_data' not in st.session_state:
    st.session_state.processed_data = None
if 'pipeline_status' not in st.session_state:
    st.session_state.pipeline_status = "Not Started"
if 'raw_data' not in st.session_state:
    st.session_state.raw_data = None

# Header
st.markdown('<div class="main-header">🌡️ Temperature Data ETL Pipeline</div>', unsafe_allow_html=True)
st.markdown("**Built with PySpark | ETL Pipeline for Global Temperature Analysis**")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Pipeline Controls")
    st.markdown("---")

    uploaded_file = st.file_uploader(
        "Upload Temperature CSV",
        type=['csv'],
        help="Upload temperature dataset (1961-2022)"
    )

    st.markdown("---")
    st.subheader("Pipeline Settings")

    handle_missing = st.checkbox("Handle Missing Values", value=True)
    pivot_data = st.checkbox("Transform to Year-Temperature Format", value=True)
    export_format = st.selectbox(
        "Export Format",
        ["Parquet", "CSV", "JSON"]
    )

    st.markdown("---")
    st.info("💡 **Pipeline Steps:**\n1. Extract\n2. Transform\n3. Load")

# Tabs
tabs = st.tabs(["📊 Dashboard", "🔄 ETL Pipeline", "📈 Analytics", "💾 Export"])

# ---------------- DASHBOARD ----------------
with tabs[0]:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pipeline Status", st.session_state.pipeline_status)

    with col2:
        st.metric(
            "Records Processed",
            "0" if st.session_state.processed_data is None else f"{len(st.session_state.processed_data):,}"
        )

    with col3:
        st.metric(
            "Countries",
            "0" if st.session_state.processed_data is None else
            f"{st.session_state.processed_data['Country'].nunique()}"
        )

    with col4:
        st.metric(
            "Year Range",
            "N/A" if st.session_state.processed_data is None else
            f"{st.session_state.processed_data['Year'].min()}-{st.session_state.processed_data['Year'].max()}"
        )

    st.markdown("---")

    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data

        col1, col2 = st.columns(2)

        with col1:
            yearly_avg = df.groupby('Year')['Temperature'].mean().reset_index()
            fig = px.line(
                yearly_avg,
                x='Year',
                y='Temperature',
                title='Global Average Temperature Trend'
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            top_countries = df.groupby('Country')['Temperature'].mean().nlargest(10).reset_index()
            fig = px.bar(
                top_countries,
                x='Temperature',
                y='Country',
                orientation='h',
                title='Top Countries by Temperature'
            )
            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Upload a dataset to begin")

# ---------------- ETL PIPELINE ----------------
with tabs[1]:
    st.header("🔄 ETL Pipeline Execution")

    if uploaded_file:

        # -------- Extract --------
        with st.expander("Stage 1: Extract", expanded=True):
            if st.button("Run Extract"):

                spark_df = extract_data(uploaded_file)
                st.session_state.raw_data = spark_df
                st.session_state.pipeline_status = "Extracted"

                st.success("Data Loaded using PySpark")

                # Preview (convert to pandas)
                st.dataframe(spark_df.limit(10).toPandas())

        # -------- Transform --------
        with st.expander("Stage 2: Transform"):
            if st.session_state.raw_data is not None:

                if st.button("Run Transform"):

                    spark_df = transform_data(
                        st.session_state.raw_data,
                        handle_missing,
                        pivot_data
                    )

                    # Convert to Pandas for UI
                    pandas_df = spark_df.toPandas()

                    st.session_state.processed_data = pandas_df
                    st.session_state.spark_processed = spark_df
                    st.session_state.pipeline_status = "Transformed"

                    st.success("Transformation Completed using PySpark")
                    st.dataframe(pandas_df.head())

            else:
                st.warning("Run Extract first")

        # -------- Load --------
        with st.expander("Stage 3: Load"):
            if "spark_processed" in st.session_state:

                if st.button("Run Load"):

                    output_path = load_data(
                        st.session_state.spark_processed,
                        export_format
                    )

                    st.session_state.pipeline_status = "Completed"

                    st.success(f"Data saved at {output_path} using PySpark")

            else:
                st.warning("Run Transform first")

    else:
        st.info("Upload a CSV file to start")

# ---------------- ANALYTICS ----------------
with tabs[2]:
    st.header("📈 Analytics")

    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data

        selected_countries = st.multiselect(
            "Countries",
            df['Country'].unique(),
            default=list(df['Country'].unique())[:5]
        )

        filtered_df = df[df['Country'].isin(selected_countries)]

        fig = px.line(
            filtered_df,
            x='Year',
            y='Temperature',
            color='Country',
            title='Temperature Trends'
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Complete pipeline first")

# ---------------- EXPORT ----------------
with tabs[3]:
    st.header("💾 Export Data")

    if st.session_state.processed_data is not None:
        df = st.session_state.processed_data

        csv = df.to_csv(index=False)
        st.download_button("Download CSV", csv, "data.csv")

        json_data = df.to_json(orient='records', indent=2)
        st.download_button("Download JSON", json_data, "data.json")

    else:
        st.info("No data available")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align:center;'>Built with PySpark, Streamlit & Plotly</div>",
    unsafe_allow_html=True
)