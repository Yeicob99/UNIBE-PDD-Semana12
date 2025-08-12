import sys, json, time
from pyspark import SparkConf, SparkContext

# Uso: spark-submit main_rdd.py file:///ruta/preprocessed.json file:///ruta/out_rdd

inp = sys.argv[1]
outp = sys.argv[2]

conf = SparkConf().setAppName("RDDPipelineMIN")
sc = SparkContext(conf=conf)

start = time.time()

rdd = sc.textFile(inp).map(lambda s: json.loads(s))
vals = rdd.flatMap(lambda row: row["values"]).map(float).cache()
count = vals.count()
mu = vals.mean()
var = vals.map(lambda x: (x - mu) ** 2).mean()
sd = var ** 0.5

elapsed = time.time() - start

metrics = {"pipeline":"RDD","count":count,"mean":mu,"stdev":sd,"duration_sec":elapsed}
sc.parallelize([json.dumps(metrics)]).coalesce(1).saveAsTextFile(outp)
sc.stop()
