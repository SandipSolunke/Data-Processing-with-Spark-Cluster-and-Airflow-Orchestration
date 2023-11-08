from datetime import datetime
from airflow import DAG
from airflow.operators.docker_operator import DockerOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago

# Define the DAG
default_args = {
    "owner": "airflow",
    "start_date": days_ago(1),
}

dag = DAG(
    "spark_cluster_dag",
    default_args=default_args,
    schedule_interval=None,
    catchup=False,
)


def run_pyspark_on_spark_cluster():
    import logging
    from pyspark.sql import SparkSession

    logging.basicConfig(level=logging.INFO)

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


script_path = "/opt/airflow/dags/pyspark_jobs/job_1.py"


def run_external_script():
    import subprocess
    import logging

    logging.info("Running Pyspark job %s" % script_path)
    # Run the external script using subprocess
    subprocess.run(["python", script_path])


start = DummyOperator(
    task_id="start",
    dag=dag,
)


##### Diff Ways to run pyspark job

# run_pyspark_task = PythonOperator(
#     task_id="run_pyspark_job",
#     python_callable=run_pyspark_on_spark_cluster,
#     dag=dag,
# )


# #cannot get logs of spark job
# run_pyspark_task = PythonOperator(
#     task_id="run_pyspark_job",
#     python_callable=run_external_script,
#     dag=dag,
# )

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
