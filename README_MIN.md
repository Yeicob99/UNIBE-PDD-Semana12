
# Proyecto Híbrido (MIN) — Demo Local Paso a Paso

Este es el **mínimo viable** para que corras todo **local** sin nubes ni GPUs reales.
Incluye:
- Microservicio "GPU" (FastAPI) que normaliza datos (con CPU por defecto; usa CuPy si tienes GPU).
- Dos pipelines de Spark: **RDD** y **DataFrame** para comparar rendimiento.
- Datos de ejemplo y scripts para correr todo rápido.

---

## Requisitos (rápido)
- **Python 3.10+** (Windows: te sirve el Python normal).  
- **pip** (viene con Python).  
- **Java 8 o 11** (necesario para PySpark).  
- **pip install pyspark==3.5.1** (lo instalamos abajo).

> Si estás en Windows, te recomiendo **WSL** o Anaconda, pero con Python normal también funciona.

---

## 1) Crear entorno e instalar dependencias

```bash
# ubicáte aquí (carpeta del proyecto)
cd proyecto_hibrido_min

# (Opcional) crea venv
python -m venv .venv
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate

# instala para FastAPI y para Spark
pip install -r gpu-preprocess/requirements.txt
pip install -r spark/requirements.txt
```

---

## 2) Levanta el microservicio "GPU" (FastAPI)

```bash
cd gpu-preprocess
uvicorn app.main:app --reload --port 8080
```
Prueba en otra terminal:
```bash
curl -X POST http://127.0.0.1:8080/process -H "content-type: application/json" -d '{"id":"demo","data":[1,2,3,4,5,100],"op":"normalize"}'
```

Deberías ver un JSON con `result` (valores normalizados) y `duration_sec`.

> Si tienes GPU y CuPy instalado, el servicio la usa automáticamente. Si no, corre en CPU (NumPy).

---

## 3) Prepara un archivo JSON de entrada para Spark
Ya te dejé un ejemplo en `data/preprocessed.json` con una línea JSON tipo:
```json
{"id":"demo","values":[0.0,0.2,0.4,0.6,0.8,1.0]}
```

> Si quieres usar la salida real del microservicio, convierte su `result` a este formato y guárdalo como una **línea** JSON.

---

## 4) Ejecuta Spark — DataFrame vs RDD

**DataFrame:**
```bash
spark-submit spark/main_df.py file://$(pwd)/data/preprocessed.json file://$(pwd)/out_df
```

**RDD:**
```bash
spark-submit spark/main_rdd.py file://$(pwd)/data/preprocessed.json file://$(pwd)/out_rdd
```

> En Windows PowerShell puedes usar `$(Get-Location)` en lugar de `$(pwd)`.

Los resultados quedan en:
- `out_df/` → un archivo `part-*.txt` con una línea JSON: mean, stdev, duration_sec…
- `out_rdd/` → similar, para RDD.

---

## 5) Comparar rendimiento
Abre ambos `part-*.txt` y compara `duration_sec`.  
Calcula **speedup**: `speedup = T_RDD / T_DF` (si DF es más rápido, speedup > 1).

---

## 6) (Opcional) Dataset más grande
Genera un vector grande para ver diferencias:
```python
# data/generate.py
import json, random
N = 1_000_000
vals = [random.random() for _ in range(N)]
with open("data/preprocessed_big.json","w") as f:
    f.write(json.dumps({"id":"big","values":vals}))
```
Luego:
```bash
python data/generate.py
spark-submit spark/main_df.py file://$(pwd)/data/preprocessed_big.json file://$(pwd)/out_df_big
spark-submit spark/main_rdd.py file://$(pwd)/data/preprocessed_big.json file://$(pwd)/out_rdd_big
```

---

## ¿Y el Actor Model y Serverless?
Este MIN te deja lista la **lógica base** (GPU→preproceso, Spark RDD/DF→métricas).  
Cuando lo domines, pasamos a:
- Orquestación (Akka) que hace los POST al microservicio y lanza Spark (en la nube).
- Cloud (GCP o AWS) para correr **serverless**.

Si quieres, en la próxima te monto el **paso 2 (cloud)** con tus cuentas y lo hacemos junto.
```

