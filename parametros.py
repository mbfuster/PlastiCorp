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
delta = {"Imp":{"skin":{1:1412, 2:897, 6:876}},"blister":{10:876}},"regulador":{2:980, 4:945}},"sellado electonico":{}},
"Viso":{"skin":{},"blister":{4:877, 5:915, 15:1877},"regulador":{8:994, 20:864},"sellado electonico":{}},
"Srf":{"skin":{},"blister":{4:875, 9:850},"regulador":{},"sellado electonico":{17:450}},
"ball":{"skin":{},"blister":{},"regulador":{},"sellado electonico":{1:850, 16:637, 18:986}}}  # CAMBIAR!!

# Costo arriendo
gamma = 800000

# Costos proveedores
sigma = {"pv1": {"flexible 150mm":101,"rigido 150mm":205,"rigido 200mm":300},
         "pv2": {"flexible 150mm":105,"rigido 150mm":200,"rigido 200mm":301}
         }

# Volumen desechado
beta = 0.015

# Costo uso maquina
theta = {"skin": 84964, "troqueladora": 60525, "selladora": 70960}

# Precio venta productos
eta = {"skin": 0, "blister": 0, "electronico": 0, "regulador": 0}  # CAMBIAR

# Costo extraccion basura
xi = 60000

# Volumen producto
V = {"skin": 0, "blister": 0, "electronico": 0,
     "regulador": 0}  # CAMBIAR VALORES

# Volumen materia prima
v = {"flexible 150": 0, "rigido 150": 0, "rigido 200": 0}

# Materia prima por producto en unidades de plancha de plastico
MP = {("blister", "rigido 200"): 0, ("skin", "flexible 150"): 0.17,
      ("electonico", "rigido 150"): 0}  # HAY QUE CALCULARLO

# Costo materia prima
mu = {"pv1": {"rigido 200": 0, "rigido 150": 0, "flexible 150": 0},
      "pv2": {"rigido 200": 0, "rigido 150": 0, "flexible 150": 0}}  # CAMBIAR

# Presupuesto inicial
PR = 0
