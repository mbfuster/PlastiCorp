from gurobipy import Model, GRB, quicksum
from conjuntos import *  # Todos los conjuntos de la modelacio
from parametros import *  # Todos los parametros de la modelacio


# Generacion de modelo
model = Model("Factory Planning Plasticorp")

X = model.addVars(I, D, vtype=GRB.CONTINUOUS, name="Cantidad producida ", lb=0)
Y = model.addVars(M, Hs, D, vtype=GRB.BINARY, name="Maquina encendida ")
Z = model.addVars(D, vtype=GRB.BINARY, name="Camion recolector ")
F = model.addVars(J, P, D, vtype=GRB.CONTINUOUS,
                  name="Compra materia prima ", lb=0)
H = model.addVars(I, D, vtype=GRB.CONTINUOUS,
                  name="Cantidad materia producto bodega ", lb=0)
Q = model.addVars(J, D, vtype=GRB.CONTINUOUS,
                  name="Cantidad materia prima bodega ", lb=0)
S = model.addVars(K, D, vtype=GRB.BINARY,
                  name="Empleado trabaja ")  # W_k_d en el modelo
O = model.addVars(I, E, D, Hs, vtype=GRB.BINARY, name="Realiza proceso ")


# Llama a update para agregar las variables al modelo
model.update()


# Restricciones

# 1. No superar presupuesto
model.addConstr(quicksum(quicksum(quicksum(Y[m, h, d] * theta[m]
                                           for m in M) for h in Hs)for d in D)
                + quicksum(quicksum(S[k, d] for k in K)for d in D) +
                quicksum(Z[d] * xi for d in D) + gamma +
                quicksum(quicksum(quicksum(mu[p][j] * F[j, p, d] for p in P)
                                  for j in J)for d in D) <= PR, "presupuesto")

# 2. Satisfaccion demanda y conservacion de flujo
# Primer dia
model.addConstrs((X[i, 1]  >= quicksum(delta[c, 1, i] for c in C) + H[i, 1]
                  for i in I
                  for c in C
                  if (c, 1, i) in delta), name="demanda")
model.addConstrs((X[i, 1]  >= H[i, 1]
                  for i in I
                  for c in C
                  if (c, 1, i) not in delta), name="demanda")
# Otros dias
model.addConstrs((X[i, d] + H[i, d - 1] >= quicksum(delta[c, d, i] for c in C)+ H[i, d]
                  for d in D[1:]
                  for i in I
                  for c in C
                  if (c, d, i) in delta), name="demanda")
model.addConstrs((X[i, d] + H[i, d - 1] >= H[i, d]
                  for d in D[1:]
                  for i in I
                  for c in C
                  if (c, d, i) not in delta), name="demanda")

# 3. Se prende la maquina solo si se utiliza en el dia
model.addConstrs((quicksum(quicksum(O[i, e, d, h] for h in Hs)
                           for i in I) >= quicksum(Y[m, h, d] for h in Hs) for d in D for e in E for m in M if e == m),  name="encender maquina")

model.addConstrs((quicksum(O[i, e, d, h] for i in I) <= Y[m, h, d]
                  for h in Hs for m in M for d in D for e in E if e == m), name="encender maquina")

# 4. La cantidad de materia prima j a comprar en período d debe ser igual o
# mayor a lo que se requiere

# Primer dia
model.addConstrs((quicksum(MP[i, j] * X[i, 1] for i in I) <=
                  quicksum(F[j, p, 1] for p in P) + Q[j, 1]
                  for j in J), name="compra materia prima")
# # Otros dias
model.addConstrs((quicksum(MP[i, j] * X[i, d] for i in I if i in MP) <= quicksum(F[j, p, d] for p in P) + Q[j, d - 1] - Q[j, d]
                  for j in J
                  for d in D[1:]), name="compra materia prima")

# 5. No se puede superar la capacidad de la bodega
model.addConstrs((quicksum(H[i, d] * V[i] for i in I) + quicksum(v[j] * Q[j, d] for j in J) <= CB
                  for d in D), name="bodega")

# 6. Si el contenedor de basura está lleno se debe llamar a camión recolector
# de basura para que retire el material
model.addConstrs(((beta * quicksum(X["electronico", d] for d in range(1, d1 + 1))) / CBA >= Z[d1]
                 for d1 in D), name="basura")

model.addConstrs((beta * quicksum(X["electronico", d] for d in range(1, d1)) <= CBA * (1 + quicksum(Z[d] for d in range(1, d1)))
                 for d1 in D),name="basura")
# 7. Minimo trabajadores nacionales
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[:6]) >= 2), name="tabajadores chilenos")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[6:11]) >= 2),name="tabajadores chilenos")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[11:16]) >= 2),name="tabajadores chilenos")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['chileno'] for k in K) for d in D[16:]) >= 2),name="tabajadores chilenos")

# 8. Minimo trabajadoras mujeres
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[:6]) >= 3), name="tabajadoras mujeres")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[6:11]) >= 3), name="tabajadoras mujeres")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[11:16]) >= 3), name="tabajadoras mujeres")
model.addConstr((
    quicksum(quicksum(S[k, d] * t[k]['mujer'] for k in K) for d in D[16:]) >= 3), name="tabajadoras mujeres")

# 9. Cantidad de trabajadores minima por máquina
model.addConstrs((quicksum(quicksum(Y[m, h, d]for m in M)
                           for h in Hs) <= quicksum(S[k, d] for k in K) for d in D), name="trabajadores por maquina")
# 10. Ciclo de trabajo
model.addConstrs(quicksum(quicksum(O[i, e, d, h] for d in D)
                          for h in Hs) <= O[i, e, d, h]for i in I for e in E for d in D for h in Hs)


# 11. Se produce un tipo de producto por maquina a la vez
model.addConstrs(quicksum(O[i, e, d, h] * U[i, e, m]
                          for i in I) <= 1 for m in M for d in D for h in Hs for e in E)


# Funcion Objetivo
obj = quicksum(quicksum(quicksum(Y[m, h, d] * theta[m]
                                 for m in M) for h in Hs)for d in D) + quicksum(quicksum(S[k, d] for k in K)for d in D) +\
    quicksum(Z[d] * xi for d in D) + gamma + \
    quicksum(quicksum(quicksum(mu[p][j] * F[j, p, d]
                               for p in P)for j in J)for d in D)

model.setObjective(obj, GRB.MINIMIZE)

# Optimizar
model.optimize()

# Imprimir resultado
with open("output.txt", "w") as file:
  for v in model.getVars():
      file.write("%s %g\n" % (v.varName, v.x))

model.printAttr("X")
