from gurobipy import Model, GRB
from conjuntos.py import * # Todos los conjuntos de la modelacio
from parametros.py import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")