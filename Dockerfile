FROM apache/airflow:2.8.1
USER root
USER airflow
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt