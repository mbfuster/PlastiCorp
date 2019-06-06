#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import defaultdict
from conjuntos import *

# Capacidad de la bodega
CB = 475

# Trabajadores por maquina
W = {"skin": 1, "troqueladora": 2, "selladora": 2}

# Trabajadores :
#   g_k = t[k]['mujer'] ; rho_k = t[k]['chileno'] ; alpha_k = t[k]['sueldo']

t = {"chery": {"sueldo": 11784, "mujer": 1, "chileno": 0},
     "fontus": {"sueldo": 11673, "mujer": 0, "chileno": 0},
     "marcelin": {"sueldo": 11674, "mujer": 0, "chileno": 1},
     "miranda": {"sueldo": 15000, "mujer": 1, "chileno": 1},
     "pierre": {"sueldo": 11822, "mujer": 0, "chileno": 0},
     "philomene": {"sueldo": 11595, "mujer": 1, "chileno": 0},
     "patricia": {"sueldo": 9600, "mujer": 1, "chileno": 1},
     "bernarda": {"sueldo": 15000, "mujer": 1, "chileno": 1},
     "joselin": {"sueldo": 11152, "mujer": 1, "chileno": 1}}

# Capacidad del basurero
CBA = 3.3

# Capacidad camión recolector
# CC = None  # REVISAR!!
BIGM = pow(10, 6)

# Pedidos
delta = {("imp", "skin", 1): 1412, ("Imp", "skin", 2): 897,
         ("imp", "skin", 6): 876, ("Imp", "blister", 10): 876,
         ("imp", "regulador", 2): 980, ("imp", "regulador", 4): 945,
         ("viso", "blister", 4): 877, ("viso", "blister", 5): 915,
         ("viso", "blister", 15): 1877, ("viso", "regulador", 8): 944,
         ("viso", "regulador", 20): 867, ("sfr", "blister", 4): 875,
         ("sfr", "blister", 9): 850, ("sfr", "electronico", 17): 450,
         ("ball", "electronico", 1): 850, ("ball", "electronico", 16): 637,
         ("ball", "electronico", 18): 986}

# Costo arriendo
gamma = 800000

# Costos proveedores
sigma = {"pv1": {"flexible 150mm": 101, "rigido 150mm": 205, "rigido 200mm": 300},
         "pv2": {"flexible 150mm": 105, "rigido 150mm": 200, "rigido 200mm": 301}
         }

# Volumen desechado
beta = 0.015

# Costo uso maquina
theta = {"skin": 84964, "troqueladora": 60525, "selladora": 70960}

# Precio venta productos
eta = {"skin": 178, "blister": 306, "electronico": 450, "regulador": 200}
# Costo extraccion basura
xi = 60000

# Volumen producto
V = {"skin": 0.000045, "blister": 0.0001, "electronico": 0.0052,
     "regulador": 0.0047625}

# Volumen materia prima
v = {"flexible 150": 0.00014364, "rigido 150": 0.000216, "rigido 200": 0.0004}

# Materia prima por producto en unidades de plancha de plastico
MP = {("blister", "rigido 200"): 0.066667,
      ("skin", "flexible 150"): 0.0833,
      ("electonico", "rigido 150"): 1.66667}

for i in I:
    for j in J:
        if (i, j) not in MP:
            MP[i, j] = 0

# Costo materia prima
mu = {"pv1": {"rigido 200": 300, "rigido 150": 205, "flexible 150": 101},
      "pv2": {"rigido 200": 301, "rigido 150": 200, "flexible 150": 105}}

# Presupuesto inicial
PR = 300000000

A = {("blister", "skin"): (),
     ("blister", "troqueladora"): ("skin"),
     ("blister", "selladora"): ("skin", "toqueladora"),
     ("blister", "relleno"): ("skin", "troqueladora", "selladora"),
     ("blister", "etiquetado"): ("skin", "troqueladora", "selladora", "relleno"),
     ("blister", "envasado"): ("skin", "troqueladora", "selladora", "relleno",
                               "etiquetado"),
     ("skin", "skin"): (),
     ("skin", "toqueladora"): ("skin"),
     ("skin", "etiquetado"): ("skin", "troqueladora"),
     ("skin", "envasado"): ("skin", "troqueladora", "etiquetado"),
     ("electronico", "skin"): (),
     ("electronico", "selladora"): ("skin"),
     ("electronico", "desgajado"): ("skin", "selladora"),
     ("electronico", "etiquetado"): ("skin", "selladora", "desgajado"),
     ("electronico", "envasado"): ("skin", "selladora", "desgajado"),
     ("regulador", "skin"): (),
     ("regulador", "selladora"): ("skin"),
     ("regulador", "envasado"): ("skin", "selladora")}

# Uso de maquina en proceso
U = {("blister", "skin", "skin"): 1,
     ("blister", "troqueladora", "troqueladora"): 1,
     ("blister", "selladora", "selladora"): 1,
     ("skin", "skin", "skin"): 1,
     ("skin", "troqueladora", "troqueladora"): 1,
     ("electronico", "skin", "skin"): 1,
     ("electronico", "selladora", "selladora"): 1,
     ("regulador", "skin", "skin"): 1,
     ("regulador", "selladora", "selladora"): 1}

for i in I:
    for e in E:
        for m in M:
            if not (i, e, m) in U:
                U[i, e, m] = 0
