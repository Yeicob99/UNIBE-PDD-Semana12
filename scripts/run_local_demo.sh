#!/usr/bin/env bash
set -e
# Activa venv si existe
if [ -f ".venv/bin/activate" ]; then source .venv/bin/activate; fi

echo "== Install deps =="
pip install -r gpu-preprocess/requirements.txt
pip install -r spark/requirements.txt

echo "== Spark DF =="
spark-submit spark/main_df.py file://$(pwd)/data/preprocessed.json file://$(pwd)/out_df
echo "DF listo en out_df/"

echo "== Spark RDD =="
spark-submit spark/main_rdd.py file://$(pwd)/data/preprocessed.json file://$(pwd)/out_rdd
echo "RDD listo en out_rdd/"

echo "Abre los archivos part-*.txt para ver tiempos y métricas."
