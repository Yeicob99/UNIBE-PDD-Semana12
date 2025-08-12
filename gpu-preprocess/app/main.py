from fastapi import FastAPI, HTTPException
from .models import ArrayPayload
from .gpu_ops import normalize, standardize, minmax
import numpy as np, time, os

app = FastAPI(title="GPU Preprocess (MIN)")

@app.get("/")
def root():
    return {"ok": True, "service": "gpu-preprocess-min"}

@app.post("/process")
def process(payload: ArrayPayload):
    start = time.time()
    arr = np.array(payload.data, dtype=float)
    if payload.op == "normalize":
        out = normalize(arr)
    elif payload.op == "standardize":
        out = standardize(arr)
    elif payload.op == "minmax":
        out = minmax(arr)
    else:
        raise HTTPException(400, f"Unknown op {payload.op}")
    dur = time.time() - start
    return {"id": payload.id, "op": payload.op, "duration_sec": dur, "n": len(out), "result": out.tolist()}
