import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ['JOB_NAME'])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

# Load data from S3
datasource = glueContext.create_dynamic_frame.from_options(
    "s3",
    {"paths": ["s3://your-bucket/raw/customer_churn.csv"]},
    format="csv",
    format_options={"withHeader": True}
)

# Transform data
applymapping = ApplyMapping.apply(frame=datasource, mappings=[
    ("customerID", "string", "customerID", "string"),
    ("gender", "string", "gender", "string"),
    ("SeniorCitizen", "long", "SeniorCitizen", "int"),
    ("tenure", "long", "tenure", "int"),
    ("Churn", "string", "Churn", "string")
])

# Write to Redshift
glueContext.write_dynamic_frame.from_jdbc_conf(
    frame=applymapping,
    catalog_connection="redshift-connection",
    connection_options={"dbtable": "public.customer_churn", "database": "dev"},
    redshift_tmp_dir="s3://your-bucket/temp/"
)

job.commit()
