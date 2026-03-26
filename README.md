# 🌡️ Temperature Data ETL Pipeline (PySpark + Streamlit)

## 📌 Overview

This project demonstrates a complete **End-to-End ETL (Extract, Transform, Load) pipeline** built using **PySpark** and visualized through an interactive **Streamlit dashboard**.

The pipeline processes global temperature data (1961–2022), performs data cleaning and transformation using distributed computing concepts, and provides real-time analytics and export capabilities.

---

## 🚀 Key Features

### 🔹 ETL Pipeline

* **Extract**: Load raw CSV data using PySpark
* **Transform**:

  * Handle missing values
  * Reshape wide dataset into long format (Year–Temperature)
  * Data cleaning and normalization
* **Load**:

  * Export processed data as CSV, JSON, or Parquet
  * Supports distributed file output (Spark partitions)

---

### 📊 Interactive Dashboard (Streamlit)

* Real-time pipeline execution
* KPI metrics (records, countries, year range)
* Visualizations:

  * Temperature trends over years
  * Country-wise comparisons
  * Statistical summaries
* Filters for country and year range

---

### ⚡ Big Data Processing

* Built using **PySpark DataFrames**
* Uses `stack()` for dynamic column transformation
* Handles large-scale datasets with distributed processing

---

## 🏗️ Project Structure

```
temperature-etl-pipeline/

├── app/
│   └── streamlit_app.py        # Streamlit UI & dashboard

├── src/
│   ├── extract.py              # Data extraction (PySpark)
│   ├── transform.py            # Data transformation (PySpark)
│   ├── load.py                 # Data export (PySpark)

├── data/
│   ├── raw/                    # Input datasets
│   └── processed/              # Output data (Spark partitions)

├── requirements.txt
└── README.md
```

---

## 🛠️ Tech Stack

* **Programming**: Python
* **Big Data**: PySpark
* **Visualization**: Streamlit, Plotly
* **Data Handling**: Pandas (for UI layer)
* **Storage Formats**: CSV, JSON, Parquet

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository

```
git clone https://github.com/your-username/ETL_pipeline_for_temperature_data.git
cd ETL_pipeline_for_temperature_data
```

---

### 2️⃣ Create Virtual Environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3️⃣ Install Dependencies

```
pip install -r requirements.txt
```

---

### 4️⃣ Install Java (Required for PySpark)

* Install Java 8 or 11

Verify:

```
java -version
```

---

### 5️⃣ Setup Hadoop (Windows Only)

PySpark requires Hadoop binaries on Windows.

Steps:

1. Download winutils from:
   https://github.com/steveloughran/winutils

2. Place in:

```
C:\hadoop\bin\winutils.exe
```

3. Set Environment Variables:

```
HADOOP_HOME = C:\hadoop
Add to PATH: C:\hadoop\bin
```

4. Restart system

---

## ▶️ Run the Application

```
streamlit run app/streamlit_app.py
```
<img width="1907" height="858" alt="etl-pipeline-demo" src="https://github.com/user-attachments/assets/31519d71-1040-498f-85e1-ac6793bbd62b" />


---

## 📂 Output Details

PySpark saves output as **partitioned files** (not a single file).

Example:

```
data/processed/
 ├── part-00000-xxxx.csv
 ├── part-00001-xxxx.csv
 └── _SUCCESS
```

👉 This is expected behavior in distributed systems.

---

## 📈 Sample Workflow

1. Upload dataset
2. Run Extract stage
3. Run Transform stage
4. Run Load stage
5. Analyze results in dashboard
6. Export processed data

---

## 🧠 Key Learnings

* Built modular ETL pipeline using PySpark
* Implemented distributed data transformation using `stack()`
* Handled cross-platform file system issues (Windows + Hadoop)
* Integrated backend pipeline with frontend dashboard
* Managed data conversion between Spark and Pandas

---

## 🎯 Future Improvements

* Deploy on **Databricks**
* Add **Airflow scheduling**
* Integrate **real-time data streaming**
* Add **cloud storage (AWS S3 / Azure Blob)**

---

## 👨‍💻 Author

**Vamsi Mohan Reddy Kommaddi**
📧 [vamsimohan2122@gmail.com](mailto:vamsimohan2122@gmail.com)
🔗 LinkedIn | GitHub

---

## ⭐ If you like this project

Give it a ⭐ on GitHub and feel free to fork it!
