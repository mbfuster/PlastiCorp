from gurobipy import Model, GRB
from conjuntos import *  # Todos los conjuntos de la modelacio
from parametros import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")

X = model.addVars(D, I, vtype=GRB.INTEGER, name="X")
Y = model.addVars(M, D, vtype=GRB.BINARY, name="Y")
Z = model.addVars(D, vtype=GRB.BINARY, name="D")
F = model.addVars(J, P, D, vtype=GRB.INTEGER, name="F")
H = model.addVars(I, D, vtype=GRB.INTEGER, name="H")
Q = model.addVars(I, D, vtype=GRB.INTEGER, name="Q")
S = model.addVars(K, D, vtype=GRB.BINARY, name="S")  # W_k_d en el modelo
