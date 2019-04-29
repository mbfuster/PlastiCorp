from gurobipy import Model, GRB, quicksum
from conjuntos import *  # Todos los conjuntos de la modelacio
from parametros import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")

X = model.addVars(I, D, vtype=GRB.INTEGER, name="X")
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
model.addConstrs((quicksum(X[i, d] for i in I) + quicksum(quicksum(mu[p][j] * F[j, p, d] for p in P) for j in J) <= PR
                  for d in D), name="presupuesto")

# Satisfaccion demanda y conservacion de flujo
# Primer dia
model.addConstrs((X[i, 1] - H[i, 1] >= delta[c, 1, i]
                  for i in I
                  for c in C
                  if (c, 1, i) in delta), name="demanda")
model.addConstrs((X[i, 1] - H[i, 1] >= 0
                  for i in I
                  for c in C
                  if (c, 1, i) not in delta), name="demanda")  # Revisar si es necesaria
# Otros dias
model.addConstrs((X[i, d] + H[i, d - 1] >= delta[c, d, i] + H[i, d]
                  for d in D[1:]
                  for i in I
                  for c in C
                  if (c, d, i) in delta), name="demanda")
model.addConstrs((X[i, d] + H[i, d - 1] >= 0
                  for d in D[1:]
                  for i in I
                  for c in C
                  if (c, d, i) not in delta), name="demanda")  # Revisar si es necesaria

# Se prende la maquina solo si se utiliza en el dia
# M = quicksum(quicksum(X[i, d] for i in I) for d in D).getValue()

# model.addConstrs(quicksum(X[i, d] for i in I) <= M * Y[m, d]
#                  for d in D
#                  for m in M)

# La cantidad de materia prima j a comprar en período d debe ser igual o
# mayor a lo que se requiere

# # Primer dia
# model.addConstrs(quicksum(MP[i, j] * X[i, 1] for i in I) <=
#                  quicksum(F[j, p, 1] for p in P) + Q[j, 1]
#                  for j in J
#                  if (i, j) in MP)  # Revisar si no genera error por no definir i
# # Otros dias
# model.addConstrs(quicksum(MP[i, j] * X[i, d] for i in I) <= quicksum(F[j, p, d] for p in P) + Q[j, d - 1] - Q[j, d]
#                  for j in J
#                  for d in D[1:]
# if (i, j) in MP)  # Revisar si no genera error por no definir i

# No se puede superar la capacidad del camion
