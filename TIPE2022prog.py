import numpy as np
import scipy as sp
import sympy as sp
import matplotlib.pyplot as plt
from sympy.physics.mechanics import dynamicsymbols, Point, ReferenceFrame
from IPython.display import display
from matplotlib import animation
from matplotlib import rcParams
rcParams['font.family'] = 'serif'
rcParams['font.size'] = 14


## Déclaration des varibales (repères, longueurs, points...) ##
# définition des variables
l1, l3, l2 = sp.symbols('l1 l3 l2')
theta1, theta2, theta3 = dynamicsymbols('theta1 theta2 theta3')

# définition des repères
R0 = ReferenceFrame('R_0')
R3 = ReferenceFrame('R_3')
R2 = ReferenceFrame('R_2')
R1 = ReferenceFrame('R_1')

# définition de l’orientation des repères (rotation/Cz perpendiculaire au plan)
R3.orient(R0, 'Axis', [theta3, R0.z])
R2.orient(R3, 'Axis', [theta2, R0.z])
R1.orient(R2, 'Axis', [theta1, R0.z])

# définition des points
C = Point('C')
B = Point('B')
A = Point('A')
K = Point('K')

# position relative de ceux-ci
B.set_pos(C, l3 * R3.x)
A.set_pos(B, l2 * R2.x)
K.set_pos(A, l1 * R1.x)

# positionnement des point A et B dans le repère de base (composante selon x et y de R0)
axy = (A.pos_from(C).express(R0)).simplify()
ax = axy.dot(R0.x)
ay = axy.dot(R0.y)
bxy = (B.pos_from(C).express(R0)).simplify()
bx = bxy.dot(R0.x)
by = bxy.dot(R0.y)
Kxy = (K.pos_from(C).express(R0)).simplify()
kx = Kxy.dot(R0.x)
ky = Kxy.dot(R0.y)
print('\nComposatante de A selon x:', ax, '\nComposatante de A selon y:', ay)
print('\nComposatante de B selon x:', bx, '\nComposatante de B selon y:', by)
print('\nComposatante de K selon x:', kx, '\nComposatante de K selon y:', ky)

# simulation géométrique (conversion des formules analytiques en fonction python (numérique) avec lambdify)
Bx = sp.lambdify((l3, theta3), bx, 'numpy')
By = sp.lambdify((l3, theta3), by, 'numpy')
Ax = sp.lambdify((l3, l2, theta3, theta2), ax, 'numpy')
Ay = sp.lambdify((l3, l2, theta3, theta2), ay, 'numpy')
Kx = sp.lambdify((l3, l2, l1, theta3, theta2, theta1), kx, 'numpy')
Ky = sp.lambdify((l3, l2, l1, theta3, theta2, theta1), ky, 'numpy')


## Application numérique (calcul de la position pour différentes valeurs de theta2 et theta3) ##
# nombre de valeurs de théta calculé
Np = 100

# longueur de la jambe en m
L1 = 0.5
L3 = 0.415
L2 = 0.415

# variation des angles
theta3s = np.linspace(np.deg2rad(70), np.deg2rad(90), Np)
theta2s = np.linspace(np.deg2rad(108.5), 0, Np)
theta1s = np.linspace(np.deg2rad(-106.5), 0, Np)

# calcul de la positions des points en fonction des angles
AX = np.array(Ax(L3, L2, theta3s, theta2s))
AY = np.array(Ay(L3, L2, theta3s, theta2s))
BX = np.array(Bx(L3, theta3s))
BY = np.array(By(L3, theta3s))
KX = np.array(Kx(L3, L2, L1, theta3s, theta2s, theta1s))
KY = np.array(Ky(L3, L2, L1, theta3s, theta2s, theta1s))


## Affichage des résultats (trajectoires et mouvements) ##
# tracé des composantes des points et de leurs trajectoires
fig, (fig1, fig2) = plt.subplots(1, 2, figsize=(12, 6))
fig1.plot(np.rad2deg(theta3s), AX, label=r'$A_x$', color='royalblue')
fig1.plot(np.rad2deg(theta3s), AY, label=r'$A_y$', color='navy')
fig1.plot(np.rad2deg(theta2s), BX, label=r'$B_x$', color='orange')
fig1.plot(np.rad2deg(theta2s), BY, label=r'$B_y$', color='orangered')
fig1.set_xlabel(r"Valeurs de $\theta_2$ et $\theta_3$ donnée (en degré)")
fig1.set_ylabel('Position (en metre)')
fig1.set_title(r'Composantes des points A et B dans le repère $R_0$')
fig1.grid()
fig1.legend()
fig2.plot(AX, AY, label='A')
fig2.plot(BX, BY, label='B')
fig2.plot(-0.273, 0.4, marker='o', label='Point A', color='darkgreen')
fig2.plot(0.141, 0.39, marker='o', label='Point B', color='limegreen')
fig2.plot(0, 0, marker='o', label='Point C', color='yellowgreen')
fig2.plot(0.3, 0)
fig2.set_xlabel('Position (en metre)')
fig2.set_title(r'Trajectoire des points A et B dans le repère $R_0$')
fig2.legend()
plt.show()

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
# enregistrement de la vidéo en format .gif
writergif = animation.PillowWriter(fps=20) 
anim.save("animation.gif", writer=writergif)
"""


## Calcul cinématique ##
# définition de la vitesse de C dans son repère
C.set_vel(R0, 0.)

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


## Etude statique de la jambe ##
# définition des paramètres
C3, C2, m, m3, m2, g = sp.symbols('C3 C2 m m_3 m_2 g')
G3 = Point('G3')
G2 = Point('G2')
G3.set_pos(C, l3/2 * R3.x)
G2.set_pos(B, l2/2 * R2.x)
yg3 = G3.pos_from(C).express(R0).dot(R0.y)
yg2 = G2.pos_from(C).express(R0).dot(R0.y)
display('\nYG3:',yg3,'\nYG2:',yg2)

# formulation des travaux
d3, d2 = sp.symbols('delta_theta_3 delta_theta_2')
dy2 = sp.diff(ay, theta3)*d3 + sp.diff(ay, theta2)*d2
dyg3 = sp.diff(yg3, theta3)*d3 + sp.diff(yg3, theta2)*d2
dyg2 = sp.diff(yg2, theta3)*d3 + sp.diff(yg2, theta2)*d2
display('\nDYG3:',dyg3,'\nDYG2:',dyg2)

# calcul de l'équilibre statique
dW = C3*d3 + C2*d2 - m*g*dy2 - m3*g*dyg3 - m2*g*dyg2
dW = sp.expand(dW)
print('\nEquilibre statique:',dW)

# calcul lagrangien (potentiel de gravité)
L = -m*g*ay - m3*g*yg3 - m2*g*yg2
print('\nPotentiel de gravité:',L)
print('\nForce C3:',sp.Eq(-sp.diff(L,theta3).simplify(),C3))
print('\nForce C2:',sp.Eq(-sp.diff(L,theta2).simplify(),C2))

# entree des paramètres (pour une personne de 70kg)
params = [(g, 9.81), (m, 57), (m3, 9), (m2, 14), (l3, L3), (l2, L2)]

# calcul des couples à appliquer pour arriver à une position fixée (Mouvement quasi-statique)
funC3 = sp.lambdify([theta3, theta2], sp.diff(L, theta3).subs(params))
funC2 = sp.lambdify([theta3, theta2], sp.diff(L, theta2).subs(params))
THETA3 = np.linspace(np.deg2rad(70), np.deg2rad(90), Np)
THETA2 = np.linspace(np.deg2rad(108.5), 0, Np)
FC3 = funC3(THETA3, THETA2)
FC2 = funC2(THETA3, THETA2)
X3 = Bx(L3, THETA3)
Y3 = By(L3, THETA3)
X2 = Ax(L3, L2, THETA3, THETA2)
Y2 = Ay(L3, L2, THETA3, THETA2)

# affichage des résultats
fig, (fig3, fig4) = plt.subplots(1, 2, figsize=(12, 6))
fig3.plot(FC2, label="C2")
fig3.plot(FC3, label="C3")
fig3.legend()
fig3.grid()
fig3.set_title('Couples des points A et B')
fig3.set_xlabel(r"Nombres d'itération du calcul des $\theta$")
fig3.set_ylabel('Couple (en N.m)')
fig4.plot(X2, Y2, label='A')
fig4.plot(X3, Y3, label='B')
fig4.plot(0.3, 0)
fig4.set_title(r'Trajectoire des points A et B dans le repère $R_0$')
fig4.set_xlabel('Position (en metre)')
fig4.plot([0, X3[-1], X2[-1]], [0., Y3[-1], Y2[-1]],'-ok', lw=2, markersize=5)
fig4.legend()
plt.show()


## Calcul de la puissance des moteurs lors du mouvement ##
# définition des variables
c2, c3 = dynamicsymbols('couple2 couple3')

# conversion des formules analytiques en fonction python (numérique) avec lambdify)
FP2 = sp.lambdify([c2], sp.Mul(c2*derivtheta2).subs(params))
FP3 = sp.lambdify([c3], sp.Mul(c3*derivtheta3).subs(params))

# calcul des puissances nécessaires
P2 = FP2(FC2)
P3 = FP3(FC3)

# affichage des résultats
fig, (fig5, fig6) = plt.subplots(1, 2, figsize=(12, 6))
fig5.plot(FC2, label="C2")
fig5.plot(FC3, label="C3")
fig5.legend()
fig5.grid()
fig5.set_title('Couples des points A et B')
fig5.set_xlabel(r"Nombres d'itération du calcul des $\theta$")
fig5.set_ylabel('Couple (en N.m)')
fig6.plot(P2, label="P2")
fig6.plot(P3, label="P3")
fig6.legend()
fig6.grid()
fig6.set_title('Puissance nécessaire en A et en B')
fig6.set_xlabel(r"Nombres d'itération du calcul des $\theta$")
fig6.set_ylabel('Puissance (en W)')
plt.show()
