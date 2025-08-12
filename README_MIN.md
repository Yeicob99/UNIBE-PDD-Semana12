# Consenso Distribuido con Raft – Demo en Python

Este proyecto es una simulación sencilla del algoritmo Raft para consenso distribuido, usando 3 nodos simulados en Python.

## Descripción
- Elección automática de líder.
- Replicación del valor `A=1` desde el líder a los followers.
- Simulación de la caída del líder y nueva elección.
- Verificación de que el estado se mantiene en todos los nodos.

## Cómo ejecutar
1. Clonar este repositorio:
   ```bash
   git clone https://github.com/usuario/raft-demo.git
   cd raft-demo
## Pon este comando para ejecutar
python raft_sim.py
