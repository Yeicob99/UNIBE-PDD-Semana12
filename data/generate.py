import json, random
N = 1_000_00  # 100 mil por defecto; cambia a 1_000_000 si quieres
vals = [random.random() for _ in range(N)]
with open("data/preprocessed_big.json","w") as f:
    f.write(json.dumps({"id":"big","values":vals}))
print("OK: data/preprocessed_big.json")
