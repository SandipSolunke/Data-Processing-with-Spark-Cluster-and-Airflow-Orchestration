from datetime import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator


# from airflow.providers.docker.operators.docker_compose import DockerComposeOperator
from airflow.utils.dates import days_ago

# Define the DAG
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

dag = DAG(
    "read_csv_data_using_spark",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)


def run_pyspark_on_spark_cluster():
    import logging
    from pyspark.sql import SparkSession
    from pyspark.sql.functions import col, expr

    logging.basicConfig(level=logging.INFO)
    # Create a SparkSession
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
    csv_file_path = "/csv_data/data.csv" 
    df = spark.read.csv(csv_file_path, header=True, inferSchema=True)

    # Show the initial DataFrame
    print("Initial DataFrame:")
    df.show()

    # Apply transformations
    filtered_df = df.filter(col("Age") > 18)

    # Show the transformed DataFrame
    print("Transformed DataFrame:")
    filtered_df.show()

    # Stop the SparkSession
    spark.stop()


start = DummyOperator(
    task_id="start",
    dag=dag,
)

#run spark job using python operator
# run_pyspark_task = PythonOperator(
#     task_id="run_pyspark_job",
#     python_callable=run_pyspark_on_spark_cluster,
#     dag=dag,
# )

#run spark job using bash operator
script_path = "/opt/airflow/dags/pyspark_jobs/job_2.py"
run_pyspark_task = BashOperator(
    task_id="run_pyspark_job",
    bash_command=f'python {script_path}',
    dag=dag,
)

end = DummyOperator(
    task_id="end",
    dag=dag,
)

start >> run_pyspark_task >> end
