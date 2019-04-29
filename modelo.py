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

# Llama a update para agregar las variables al modelo
model.update()

# Restricciones

# No superar presupuesto
model.addVConstrs((quicksum(X[i, d] for i in I) + quicksum(quicksum(mu[j][p] * F[j, p, d] for p in P) for j in J)) <= PR
                  for d in D, name="presupuesto")

# Satisfaccion demanda y conservacion de flujo
# Primer dia
model.addConstrs(X[i, 1] - H[i, 1] >= delta[c, p, d]
                 for i in I
                 for c in C
                 if (c, p, d) in delta, name="demanda")
model.addConstrs(X[i, 1] - H[i, 1] >= 0
                 for i in I
                 for c in C
                 if (c, p, d) not in delta, name="demanda")  # Revisar si es necesaria
# Otros dias
model.addConstrs(X[i, d] + H[i, d - 1] >= delta[c] + H[i, d]
                 for i in I
                 for c in C
                 if (c, p, d) in delta, name="demanda")
model.addConstrs(X[i, d] + H[i, d - 1] >= 0
                 for i in I
                 for c in C
                 if (c, p, d) not in delta, name="demanda")  # Revisar si es necesaria
