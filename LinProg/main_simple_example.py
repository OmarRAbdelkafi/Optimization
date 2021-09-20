#coding:utf-8

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import linprog

#1. Problem description :
"""
Une aciérie produit des bandes et des rouleaux métalliques. Elle fonctionne 40 heures par
semaine. Les vitesses de production sont de 200 bandes par heure et de 140 rouleaux par heure.
Les bandes sont vendues 25 euros l’unité; les rouleaux 30 euros l’unité. Le marché est limité : il
est impossible de vendre plus de 6000 bandes et 4000 rouleaux par semaine. Comment maximiser
le profit ? Pour modéliser, on dégage
1. les variables (ce qu’on cherche à calculer),
2. les paramètres (les données numériques présentes dans l’énoncé ou qui se calculent facilement à partir de ces dernières),
3. les contraintes,
4. l’objectif (il n’y en a qu’un).
"""

#2. Mathematical model
"""
Objectif : Max(x1,x2) 25*x1 + 30*x2
x1 ≤ 6000 (limitation de marché : bandes)
x2 ≤ 4000 (limitation de marché : rouleaux)
(1/200) x1 + (1/140) x2 ≤ 40 (limitation de la production)
x1, x2 ≥ 0 (bound)
"""

#3. transform to standard minimzation problem
"""
Objectif : Min(x1,x2) -25*x1 - 30*x2
x1 ≤ 6000 (limitation de marché : bandes)
x2 ≤ 4000 (limitation de marché : rouleaux)
(1/200)*x1 + (1/140)*x2 ≤ 40 (limitation de la production)
x1, x2 ≥ 0 (bounds)
"""

"""
Objectif
"""
c = np.array([-25, -30])

"""
Constraintes Inequation
"""
A_ub = np.array([[1, 0],[0, 1],[(1/200), (1/140)]])
b_ub = np.array([6000, 4000, 40])

"""
Constraintes equation
"""

"""
Bounds
"""
x1_bounds = (0, np.inf)
x2_bounds = (0, np.inf)  # +/- np.inf can be used instead of None
bounds = [x1_bounds, x2_bounds]

"""
SOLVE
"""
result = linprog(c, A_ub=A_ub, b_ub=b_ub, bounds=bounds)

"""
Print results
"""
print(result)
