from gurobipy import Model, GRB, quicksum
from conjuntos import *  # Todos los conjuntos de la modelacio
from parametros import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")

X = model.addVars(I, D, vtype=GRB.INTEGER, name="X")
Y = model.addVars(M, Hs, D, vtype=GRB.BINARY, name="Y")
Z = model.addVars(D, vtype=GRB.BINARY, name="D")
F = model.addVars(J, P, D, vtype=GRB.INTEGER, name="F")
H = model.addVars(I, D, vtype=GRB.INTEGER, name="H")
Q = model.addVars(J, D, vtype=GRB.INTEGER, name="Q")
S = model.addVars(K, D, vtype=GRB.BINARY, name="S")  # W_k_d en el modelo
O = model.addVars(I, E, D, Hs, vtype=GRB.BINARY, name="O")


# Llama a update para agregar las variables al modelo
model.update()


# Restricciones

# 1. No superar presupuesto
model.addConstr(quicksum(quicksum(quicksum(Y[m, h, d]*theta[m]
                                           for m in M) for h in Hs)for d in D) + quicksum(quicksum(S[k, d] for k in K)for d in D) +
                quicksum(Z[d]*xi for d in D) + gamma +
                quicksum(quicksum(quicksum(mu[p][j]*F[j, p, d] for p in P)for j in J)for d in D) <= PR, "presupuesto")

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
model.addConstrs(quicksum(quicksum(O[i, e, d, h] for h in Hs)
                          for i in I) >= quicksum(Y[m, h, d] for h in Hs) for d in D for e in E for m in M if e == m)

model.addConstrs(quicksum(O[i, e, d, h] for i in I) <= Y[m, h, d]
                 for h in Hs for m in M for d in D for e in E if e == m)

# 4. La cantidad de materia prima j a comprar en período d debe ser igual o
# mayor a lo que se requiere

# model.addConstrs(quicksum(MP[i, j]*X[i, d] for i in I) <= quicksum(F[j, p, d]
#                                                                   for p in P)+Q[j, d]-Q[j, d-1] for j in J for d in D if d != 1)

mode.addConstrs(quicksum(MP[i, j] * X[i, j]
                         for i in I) <= quicksum(f[j, p, 1] - q[j, d] for p in P) for j in J)

# Primer dia
# model.addConstrs(quicksum(MP[i, j] * X[i, 1] for i in I) <=
#                quicksum(F[j, p, 1] for p in P) + Q[j, 1]
#                  for j in J
#                  if (i, j) in MP)  # Revisar si no genera error por no definir i
# # Otros dias
# model.addConstrs(quicksum(MP[i, j] * X[i, d] for i in I) <= quicksum(F[j, p, d] for p in P) + Q[j, d - 1] - Q[j, d]
#                  for j in J
#                  for d in D[1:]
# if (i, j) in MP)  # Revisar si no genera error por no definir i
mode.addConstrs(quicksum(MP[i][j] * X[i,j] for i in I) <= quicksum(f[j,p,1] - q[j,d] for p in P) for j in J)

# 5. No se puede superar la capacidad de la bodega
model.addConstrs((quicksum(H[i, d] * V[i] for i in I) + quicksum(v[j] * Q[j, d] for j in J) <= CB
                  for d in D), name="bodega")

# 6. Si el contenedor de basura está lleno se debe llamar a camión recolector
# de basura para que retire el material
model.addConstrs((beta * quicksum(X["electronico", d] for d in range(1, d1 + 1))) / CBA >= Z[d1]
                 for d1 in D)

model.addConstrs(beta * quicksum(X["electronico", d] for d in range(1, d1)) <= CBA * (1 + quicksum(Z[d] for d in range(1, d1)))
                 for d1 in D)
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
model.addConstrs(quicksum(quicksum(Y[m, h, d]for m in M)
                          for h in Hs) <= quicksum(S[k, d] for k in K) for d in D)
# 10. Ciclo de trabajo
model.addConstrs(quicksum(quicksum(O[i, e, d, h] for d in D)
                          for h in Hs) <= O[i, e, d, h]for i in I for e in E for d in D for h in Hs)

obj = quicksum(quicksum(quicksum(Y[m, h, d]*theta[m]
                                 for m in M) for h in Hs)for d in D) + quicksum(quicksum(S[k, d] for k in K)for d in D) +\
    quicksum(Z[d]*xi for d in D) + gamma + \
    quicksum(quicksum(quicksum(mu[p][j]*F[j, p, d] for p in P)for j in J)for d in D)

model.setObjective(obj, GRB.MINIMIZE)
model.optimize()
# model.printAttr("X")
