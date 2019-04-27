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
CC = None  # REVISAR!!

# Pedidos
delta = {}

# Costo arriendo
gamma = 800000

# Costos proveedores
sigma = {"pv1": {}, "pv2": {}}

# Volumen desechado
beta = 0.015

# Costo de produccion
# ES NECESARIO???

# Costo uso maquina
theta = {"skin": 84964, "troqueladora": 60525, "selladora": 70960}

# Materia prima por producto en unidades de plancha de plastico
MP = {"blister": {"rigido 200": 0}, "skin": {
    "flexible 150": 0.17}, "electonico": {"rigido 150": 0}}  # HAY QUE CALCULARLO

# Costo extraccion basura
xi = 60000

# Volumen producto
V = {}

# Volumen materia prima
v = {"flexible 150": 0, "rigido 150": 0, "rigido 200": 0}
