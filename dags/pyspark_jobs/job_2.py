import logging
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, expr

logging.basicConfig(level=logging.INFO)


spark = (
    SparkSession.builder.appName("SparkClusterTest")
    .master("spark://spark-master:7077")
    .config("spark.executor.instances", "1")
    .config("spark.executor.memory", "1g")
    .config("spark.driver.memory", "1g")
    .config("spark.driver.maxResultSize", "1g")
    .config("spark.executor.cores", "1")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/bitnami/python/bin/python")
    .getOrCreate()
)

# Read the CSV file
csv_file_path = "/csv_data/data.csv"  # Replace with the actual file path
df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

# Show the initial DataFrame
print("Initial DataFrame:")
df.show()

# Apply transformations
# 1. Filter employees with a salary greater than 70000
filtered_df = df.filter(col("Age") > 18)

# Show the transformed DataFrame
print("Transformed DataFrame:")
filtered_df.show()

# Stop the SparkSession
spark.stop()
