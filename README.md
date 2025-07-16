
# **Customer Churn Analytics on AWS**

## **Project Overview**

This project implements an end-to-end data engineering pipeline on AWS to analyze Telecom customer churn patterns. It automates data ingestion, ETL, schema management, and orchestration, and visualizes insights using Power BI dashboards for business decision-making.


## **Architecture**

![AWS Architecture](./Customer%20Churn%20Project%20AWS1.drawio.png)

**Tools & Services Used:**

* **AWS S3** – Storage for raw and transformed churn datasets
* **AWS Glue** – ETL transformation and schema management
* **AWS Glue Crawler** – Infers schema and populates Glue Data Catalog
* **Amazon Redshift** – Data warehouse for structured analytics
* **Amazon Athena** – Ad-hoc queries on churn data
* **Apache Airflow** – Orchestration of Glue job execution and monitoring
* **Power BI** – Visualization of churn metrics and KPIs

---

## **Project Structure**

```
customer-churn-analytics-aws/
│
├── airflow_dags/
│   ├── customer_churn_dag.py       # Airflow DAG to automate Glue & Redshift pipeline
│
├── glue_scripts/
│   ├── s3_to_redshift_etl.py       # Glue ETL script (custom transformations)
│
├── data/
│   ├── raw CSV Files/                        # Raw churn dataset (CSV)
│   ├── processed/                  # Cleaned and transformed data
│
├── dashboards/
│   ├── Churn BI dashboard.png         # Dashboard preview image
│
├── sql_queries/
│   ├── churn_redshift_queries.sql  # Redshift queries for churn analytics
│
├── requirements.txt                # Python dependencies for Airflow
└── README.md
```

---

## **Prerequisites**

* **AWS Account** with permissions for S3, Glue, and Redshift
* **Apache Airflow** installed locally or on EC2
* **Python 3.8+**
* Install dependencies:

```bash
pip install -r requirements.txt
```

---

## **Pipeline Workflow**

### **Step 1: Data Ingestion**

* Upload the raw churn dataset into **Amazon S3 (Raw Zone)**.

### **Step 2: Schema Discovery**

* Configure **AWS Glue Crawler** to infer schema and store metadata in **Glue Data Catalog**.

### **Step 3: Data Transformation**

* Create **AWS Glue ETL Job** to clean and transform data.
* Output stored in **Amazon S3 (Processed Zone)** in **Parquet format**.

### **Step 4: Load into Redshift**

* Load the transformed data into **Amazon Redshift** for analytics.

### **Step 5: Orchestration with Airflow**

* Use **customer\_churn\_dag.py** to:

  * Trigger Glue job.
  * Retrieve Job Run ID.
  * Monitor Glue job completion with **GlueJobSensor**.

```python
glue_job_trigger = PythonOperator(
    task_id='tsk_glue_job_trigger',
    python_callable=glue_job_s3_redshift_transfer,
    op_kwargs={'job_name': 's3_upload_to_redshift_gluejob'}
)
```

### **Step 6: Query with Athena**

* Enable **ad-hoc SQL queries** using Athena for quick churn insights.

### **Step 7: Visualization with Power BI**

* Connect Power BI to **Amazon Redshift**.
* Build interactive dashboards for **churn rate, customer demographics, churn reasons, and payment preferences**.

---

## **Dashboard Preview**

![Power BI Dashboard](./Churn%20BI%20dashboard.png)

**Key Insights with Metrics**

| **#** | **Business Question**                 | **Insight (with Numbers)**                                            | **Action**                                     |
| ----- | ------------------------------------- | --------------------------------------------------------------------- | ---------------------------------------------- |
| 1     | Which segment churns most?            | **Fiber Optic users: 43.96%** churn; Singles churn more.              | Offer retention plans & loyalty perks.         |
| 2     | How does payment method affect churn? | **Electronic Check: 33.58%**, highest churn vs. Credit Card (22.89%). | Promote auto-pay & discounts.                  |
| 3     | What are top churn reasons?           | **Attitude of support staff** is top .                                | Improve support & pricing strategy.            |
| 4     | Which internet type churns most?      | **Fiber Optic: 43.96%**, DSL: 34.37%, No Internet: 21.67%.            | Ensure reliability & offer service guarantees. |
| 5     | Does age affect churn?                | Majority churn from **Non-senior citizens (6K+)**.                    | Launch youth-focused loyalty programs.         |

