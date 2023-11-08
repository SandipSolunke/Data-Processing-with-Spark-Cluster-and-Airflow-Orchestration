
# Airflow-Spark Setup Using Docker
This setup allows you to run Apache Airflow and Apache Spark together using Docker Compose. You can quickly get an Airflow instance with Spark integration up and running.

## Prerequisites
Make sure you have Docker and Docker Compose installed on your system.

## Getting Started
1. Clone this repository.
2. Navigate to the repository's root directory.
3. Run the following command to start the services:

```bash
docker-compose up
```
This command will initialize Airflow, Spark Master, and Spark Workers.

## Accessing the Services
1. Airflow UI: http://localhost:8080
* Username: admin
* Password: admin

2. Spark Master UI: http://localhost:9090