import numpy as np

# Intento de GPU con CuPy (si lo tienes); si no, caemos a NumPy (CPU)
try:
    import cupy as cp
    USE_GPU = True
except Exception:
    cp = None
    USE_GPU = False

def _minmax(arr):
    if USE_GPU:
        g = cp.asarray(arr)
        mn = cp.min(g); mx = cp.max(g)
        return mn, mx, g
    else:
        mn = np.min(arr); mx = np.max(arr)
        return mn, mx, arr

def normalize(arr: np.ndarray):
    mn, mx, X = _minmax(arr)
    rng = (mx - mn) + 1e-12
    if USE_GPU:
        out = (X - mn) / rng
        return cp.asnumpy(out)
    else:
        return (arr - mn) / rng

def standardize(arr: np.ndarray):
    if USE_GPU:
        X = cp.asarray(arr)
        mu = cp.mean(X); sd = cp.std(X) + 1e-12
        out = (X - mu) / sd
        return cp.asnumpy(out)
    else:
        mu = np.mean(arr); sd = np.std(arr) + 1e-12
        return (arr - mu) / sd

def minmax(arr: np.ndarray, a=0.0, b=1.0):
    mn, mx, X = _minmax(arr)
    rng = (mx - mn) + 1e-12
    if USE_GPU:
        out = a + (X - mn) * (b - a) / rng
        return cp.asnumpy(out)
    else:
        return a + (arr - mn) * (b - a) / rng
