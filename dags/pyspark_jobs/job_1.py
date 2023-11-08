import logging

from pyspark.sql import SparkSession

logging.info("INside pyspark Job")
logging.basicConfig(level=logging.INFO)
# Create a SparkSession
spark = (
    SparkSession.builder.appName("SparkClusterTest")
    .master("spark://spark-master:7077")
    .config("spark.executorEnv.PYSPARK_PYTHON", "/opt/bitnami/python/bin/python")
    .getOrCreate()
)

data = [(1, 2), (3, 4), (5, 6)]
df = spark.createDataFrame(data, ["col1", "col2"])
result_df = df.withColumn("sum", df["col1"] + df["col2"])
result_df.show()

spark.stop()
