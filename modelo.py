from gurobipy import Model, GRB, quicksum
from conjuntos import *  # Todos los conjuntos de la modelacio
from parametros import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")
print("hola")

X = model.addVars(I, D, vtype=GRB.INTEGER, name="X")
print("1")
Y = model.addVars(M, Hs, D, vtype=GRB.BINARY, name="Y")
print("2")
Z = model.addVars(D, vtype=GRB.BINARY, name="D")
print("3")
F = model.addVars(J, P, D, vtype=GRB.INTEGER, name="F")
print("4")
H = model.addVars(I, D, vtype=GRB.INTEGER, name="H")
print("5")
Q = model.addVars(J, D, vtype=GRB.INTEGER, name="Q")
print("6")
S = model.addVars(K, D, vtype=GRB.BINARY, name="S")  # W_k_d en el modelo
print("7")
O = model.addVars(I, E, D, Hs, vtype=GRB.BINARY, name="O")
print("8")

# Llama a update para agregar las variables al modelo
model.update()


# Restricciones

# 1. No superar presupuesto
# model.addConstrs(quicksum(quicksum(quicksum(Y[m, h, d] * theta[m]for m in M)
#                                   + (quicksum(S[k, d] * t[k]["sueldo"]
#                                      for k in K))+(Z[d] * xi) + gamma
#                                   + (quicksum(quicksum(mu[p] * F[p, j, d] for p in P)for j in J))for h in H)for d in D)) <= PR, "presupuesto")

# model.addConstrs((quicksum(X[i, d] for i in I) + quicksum(quicksum(mu[p][j] * F[j, p, d] for p in P) for j in J) <= PR
#                  for d in D), name="presupuesto")

# 2. Satisfaccion demanda y conservacion de flujo
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

# 3. Se prende la maquina solo si se utiliza en el dia
# M = quicksum(quicksum(delta[i, d] for i in I) for d in D)
#
# model.addConstrs(quicksum(X[i, d] for i in I) <= M * Y[m, d]
#                  for d in D
#                  for m in M)

# 4. La cantidad de materia prima j a comprar en período d debe ser igual o
# mayor a lo que se requiere

# Primer dia
# model.addConstrs(quicksum(MP[i, j] * X[i, 1] for i in I) <=
#                  quicksum(F[j, p, 1] for p in P) + Q[j, 1]
#                  for j in J
#                  if (i, j) in MP)  # Revisar si no genera error por no definir i
# # Otros dias
# model.addConstrs(quicksum(MP[i, j] * X[i, d] for i in I) <= quicksum(F[j, p, d] for p in P) + Q[j, d - 1] - Q[j, d]
#                  for j in J
#                  for d in D[1:]
# if (i, j) in MP)  # Revisar si no genera error por no definir i

# 5. No se puede superar la capacidad de la bodega
model.addConstrs((quicksum(H[i, d] * V[i] for i in I) + quicksum(v[j] * Q[j, d] for j in J) <= CB
                  for d in D), name="bodega")

# 6. Si el contenedor de basura está lleno se debe llamar a camión recolector
# de basura para que retire el material
# M = quicksum(quicksum(delta[i, d] for i in I) for d in D)
# model.addConstr(
#    CBA - quicksum(X[i, d] + X[i, d-1] for i in I) * beta <= M * (i - Z[d]) for d in D)

# 7. Minimo trabajadores nacionales
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[:6]) >= 2)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[6:11]) >= 2)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[11:16]) >= 2)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[16:]) >= 2)

# 8. Minimo trabajadoras mujeres
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[:6]) >= 3)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[6:11]) >= 3)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[11:16]) >= 3)
model.addConstr(
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[16:]) >= 3)

# 9. Cantidad de trabajadores minima por máquina
# model.addConstr(quicksum(Y[m, d] for m in M) * W <= quicksum(S[k, d] for k in K) for d in D)

# 10. Ciclo de trabajo

obj = quicksum(quicksum(quicksum(Y[m, h, d]*theta[m]
                                 for m in M) for h in Hs)for d in D) + quicksum(quicksum(S[k, d] for k in K)for d in D) +\
    quicksum(Z[d]*xi for d in D) + gamma


obj2 = quicksum(quicksum(mu[p, j] for p in P)for j in J)
# model.setObjective(obj, GRB.MINIMIZE)

model.optimize()
# model.printAttr("X")
