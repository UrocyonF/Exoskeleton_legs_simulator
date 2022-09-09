import numpy as np
import scipy as sp
import sympy as sp
import matplotlib.pyplot as plt
from sympy.physics.mechanics import dynamicsymbols, Point, ReferenceFrame
from IPython.display import display
from matplotlib import animation



l = sp.symbols('distance')

theta = dynamicsymbols('theta')

R0 = ReferenceFrame('R_0')
R1 = ReferenceFrame('R_1')
R1.orient(R0, 'Axis', [theta, R0.z])

E = Point('E')
E.set_vel(R0, 0.)

M = Point('M')
M.set_pos(E, l * R1.x)

mxy = (M.pos_from(E).express(R0)).simplify()
mx = mxy.dot(R0.x)
my = mxy.dot(R0.y)
print('\nComposatante de A selon x:', mx, '\nComposatante de A selon y:', my)


Mx = sp.lambdify((l, theta), mx, 'numpy')
My = sp.lambdify((l, theta), my, 'numpy')


Np = 400
dem1 = np.linspace(356000, 406000, int(Np/4))
dem2 = np.linspace(406000, 356000, int(Np/4))
L = np.append(dem1, np.append(dem2, np.append(dem1, dem2)))

thetas = np.linspace(0, 2*np.pi, Np)

MX = np.array(Mx(L, thetas))
MY = np.array(My(L, thetas))


fig, (fig1, fig2) = plt.subplots(1, 2, figsize=(12, 6))
fig1.plot(np.rad2deg(thetas), MX, label=r'$M_x$', color='orange')
fig1.plot(np.rad2deg(thetas), MY, label=r'$M_y$', color='orangered')
fig1.set_xlabel(r"Valeurs de $\theta$ donnée (en degré)")
fig1.set_ylabel('Position (en metre)')
fig1.set_title(r'Composantes du point M dans le repère $R_0$')
fig1.grid()
fig1.legend()
fig2.plot(MX, MY, label='Trajectoire')
fig2.plot(356000, 0, marker='o', label='Lune', color='darkgreen')
fig2.plot(0, 0, marker='o', label='Terre', color='yellowgreen')
fig2.set_xlabel('Position (en metre)')
fig2.set_title(r'Trajectoire du point M dans le repère $R_0$')
fig2.legend()
plt.show()

"""
# fonction d'animation
def animate(i):
    global BX, BY, AX, AY, KX, KY
    line1.set_data([0., BX[i]], [0., BY[i]])
    line2.set_data([BX[i], AX[i]], [BY[i], AY[i]])
    line3.set_data([AX[i], KX[i]], [AY[i], KY[i]])
    return(line1, line2, line3)

# animation du mouvement de la jambe
Fig = plt.figure(figsize=(10, 10))
ax = Fig.add_subplot(111, aspect='equal')
ax.set_axis_off()
ax.set_xlim((-1.2*(L3+L2), 1.2*(L3+L2)))
ax.set_ylim((-0.5, 1.2*(L3+L2+L1)))
ax.set_title("Mouvement de l'utilisateur de la position assise à debout", fontsize=30)
fig.set_facecolor("#ffffff")
line1, = ax.plot([0., L3], [0., 0.], 'o-b', lw=18, markersize=25)
line2, = ax.plot([L3, L3+L2], [0., 0.], 'o-', lw=18, markersize=25)
line3, = ax.plot([L3+L2, L3+L2], [0., L1], 'o-', lw=18, markersize=25)

# affichage de l'animation
anim = animation.FuncAnimation(Fig, animate, np.arange(1, Np), interval=20, blit=True)
plt.show()
"""


"""
# calcul de l'experssion de la vitesse de B dans le repère R0
B.v2pt_theory(C, R0, R3)
vB = B.vel(R0)
#print('\nVitesse de B:', vB.express(R0).simplify())

# calcul de l'experssion de la vitesse de A dans le repère R0
A.v2pt_theory(B, R0, R2)
vA = A.vel(R0)
#print('\nVitesse de A:', vA.express(R0).simplify())

# vérification de la composition des vitesses
omegA = R2.ang_vel_in(R0)
BA = A.pos_from(B)
#print('\nComposition des vitesse de A et B:',(B.vel(R0) + omegA.cross(BA)).express(R0).simplify())

# calcul de l'experssion de l'accélération de B dans le repère R0
B.a2pt_theory(C, R0, R3)
aB = B.acc(R0)
#print('\nAccélération de B:', aB.express(R0).simplify())

# calcul de l'experssion de l'accélération de A dans le repère R0
A.a2pt_theory(B, R0, R2)
aA = A.acc(R0)
#print('\nAccélération de A:', aA.express(R0).simplify())

# vérification de la composition des accélérations
omegA = R2.ang_vel_in(R0)
omegaA = R2.ang_acc_in(R0)
BA = A.pos_from(B)
#print('\nComposition des accélération de A et B:', (B.acc(R0) + omegaA.cross(BA) + omegA.cross(omegA.cross(BA))).simplify())


## Calcul des vitesse des composantes de A dans le repère r0 ##
# définition de la vitesse de thêta2 et thêta3
derivtheta2 = np.deg2rad(108.5)/5
derivtheta3 = np.deg2rad(20)/5

# définition des variables utiles
X, Y = [], []

# fonction permettant le calcul de la vitesse de la composante selon x0 de A
def vitessex(t):
    global theta2s, theta3s, derivtheta2, derivtheta3, L2, L3
    return(L2*(derivtheta2 - derivtheta3)*np.sin(theta2s[t] + theta3s[t]) - L3*np.sin(theta3s[t])*derivtheta3)

# fonction permettant le calcul de la vitesse de la composante selon y0 de A
def vitessey(t):
    global theta2s, theta3s, derivtheta2, derivtheta3, L2, L3
    return(-L2*(derivtheta2 - derivtheta3)*np.cos(theta2s[t] + theta3s[t]) + L3*np.cos(theta3s[t])*derivtheta3)

# boucle pour le calcul des vitesses
for t in range(Np):
    X.append(vitessex(t)*1000)
    Y.append(vitessey(t)*1000)

# affichage des résultats (tracé des vitesse des composante)
plt.plot(range(Np), X, label="ẋ(t)", color='royalblue')
plt.plot(range(Np), Y, label="ẏ(t)", color='navy')
plt.ylabel("Vitesse (en mm/s)")
plt.xlabel("Nombre d'intération de la dichotomie")
plt.title('Evolution de ẋ(t) et de ẏ(t) en fonction du temps')
plt.legend()
plt.grid()
plt.show()
"""