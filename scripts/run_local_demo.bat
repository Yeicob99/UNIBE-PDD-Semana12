@echo off
REM Activa venv si existe
IF EXIST .venv\Scripts\activate.bat (
    CALL .venv\Scripts\activate.bat
)

echo == Install deps ==
pip install -r gpu-preprocess\requirements.txt
pip install -r spark\requirements.txt

echo == Spark DF ==
spark-submit spark\main_df.py file://%cd%/data/preprocessed.json file://%cd%/out_df
echo DF listo en out_df\

echo == Spark RDD ==
spark-submit spark\main_rdd.py file://%cd%/data/preprocessed.json file://%cd%/out_rdd
echo RDD listo en out_rdd\

echo Abre los archivos part-*.txt para ver tiempos y métricas.
