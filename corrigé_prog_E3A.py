import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 14

# nombre d'itération du calcul
Np = 100

# création des arrays pour le tableau
X = np.linspace(-273, 0, Np)
Y = np.linspace(400, 830, Np)

# définition des variables utilisées
theta3, theta2 = np.linspace(0, 0, Np), np.linspace(0, 0, Np)
sumtheta = theta2+theta3
L3, L2 = 415, 415


# fonction équivalente à F(theta3(t),x(t),y(t))
def equa_inverseF(theta3, x, y):
    global L3, L2
    return (L3*np.cos(theta3)-x)**2+(L3*np.sin(theta3)-y)**2-L2**2

# foncion équivalente à G(theta2(t)+theta3(t),x(t),y(t))
def equa_inverseG(sumtheta, x, y):
    global L3, L2
    return (L2*np.cos(sumtheta)-x)**2+(L2*np.sin(sumtheta)-y)**2-L3**2

# fonction effectuant la dichotomie pour résoudre l'équation f fourni à 10**(-5) près dans un interval [a,b]
def dichoto(f, a, b):
    if (b-a) > (2*10**(-5)):
        m = (a+b)/2
    if f(m) == 0:
        return m
    elif (f(a)*f(m)) < 0:
        b = m
    else:
        a = m
    return (a+b)/2


# innitialisation du calcul
if __name__ == '__main__':
    # début de la boucle pour le calcul des thêtas par dichotomie
    for i in range(Np):
        def equa_inverseF_tet(theta3): return equa_inverseF(theta3, X[i], Y[i])
        def equa_inverseG_tet(sumtheta): return equa_inverseG(sumtheta, X[i], Y[i])
        theta3[i] = dichoto(equa_inverseF_tet, 60*np.pi/180, 100*np.pi/180)
        theta2[i] = dichoto(equa_inverseG_tet, -150*np.pi/180, 50*np.pi/180)
    print("thêta2 final (en rad):", round(theta3[-1], 3), "\nthêta3 final (en rad):", round(theta2[-1], 3))


"""
On observe qu'on trouve au final comme angle pour thêta3 1,5708rad soit 90° et pour thêta2 0rad soit 0°
Ce sont bien les valeurs attendus de thêta (celle que l'on peut retrouver dans le tableau des données géométriques fourni)
Ce sont ces valeurs qui permettent ensuite de calculer les dérivées de thêta 2 et 3 donnant ainsi une vitesse
"""
