import sys, json, time
from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, col, avg, stddev_pop

# Uso: spark-submit main_df.py file:///ruta/preprocessed.json file:///ruta/out_df

inp = sys.argv[1]
outp = sys.argv[2]

spark = SparkSession.builder.appName("DFPipelineMIN").getOrCreate()
start = time.time()

df = spark.read.json(inp, multiLine=False)
vals = df.select(explode(col("values")).alias("v")).select(col("v").cast("double").alias("v"))
res = vals.agg(avg("v").alias("mean"), stddev_pop("v").alias("stdev"))
row = res.collect()[0]
count = vals.count()

elapsed = time.time() - start

metrics = {"pipeline":"DataFrame","count":count,"mean":row["mean"],"stdev":row["stdev"],"duration_sec":elapsed}
(spark.createDataFrame([(json.dumps(metrics),)], ["json"]).coalesce(1).write.mode("overwrite").text(outp))

spark.stop()
