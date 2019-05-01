# Productos
I = ["skin", "blister", "electronico", "regulador"]

# Recursos
J = ["rigido 200", "rigido 150", "flexible 150"]

# Trabajadores
K = ["chery", "fontus", "marcelin", "miranda", "pierre", "philomene",
     "patricia", "bernarda", "joselin"]

# Proveedores
P = ["pv1", "pv2"]

# Maquinas
M = ["skin", "troqueladora", "selladora"]

# Dias
D = [i for i in range(1, 21)]

# Clientes
C = ["imp", "sfr", "viso", "ball"]

# Etapas de produccion
L = {"blister": ("skin", "troqueladora", "selladora",
                 "relleno", "etiquetado", "envasado"),
     "skin": ("skin", "toqueladora", "etiquetado", "envasado"),
     "electronico": ("skin", "selladora", "desgajado", "etiquetado",
                     "envasado"),
     "regulador": ("skin", "selladora", "envasado")}

Hs = [i for i in range(1, 9)]

# Conjunto de pedidos
#E = [str(e) for e in range(0, 31)]

E = ["skin", "troqueladora", "selladora", "relleno", "etiquetado", "envasado",
     "desgajado"]
