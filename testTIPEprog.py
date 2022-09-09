import matplotlib.pyplot as plt
import numpy as np


"""
nptheta2,nptheta3=np.linspace(np.deg2rad(70),np.deg2rad(90),1000),np.linspace(np.deg2rad(108.5),0,1000)
L3,L2=415,415


def equa_inverseF(theta3,x,y):
    global L3,L2
    return (L3*np.cos(theta3)-x)**2+(L3*np.sin(theta3)-y)**2-L2**2

def equa_inverseG(sumtheta,x,y):
    global L3,L2
    return (L2*np.cos(sumtheta)-x)**2+(L2*np.sin(sumtheta)-y)**2-L3**2


def x(theta2,theta3):
    global L3,L2
    return(L3*np.cos(theta3)+L2*np.cos(theta2+theta3))

def y(theta2,theta3):
    global L3,L2
    return(L3*np.sin(theta3)+L2*np.sin(theta2+theta3))


def derivx(theta2,theta3):
    global L3,L2
    return(-(L2*L3)/2*(theta3*(np.sin(theta2+2*theta3)+np.sin(-theta2))))


if __name__ == '__main__':
    X,Y=[],[]
    #equF,equG=[],[]
    for i in range(1000):
        X.append(x(nptheta2[i],nptheta3[i]))
        Y.append(y(nptheta2[i],nptheta3[i]))
        #equF.append(equa_inverseF(nptheta3[i],X[i],Y[i]))
        #equG.append(equa_inverseG(nptheta3[i]+nptheta2[i],X[i],Y[i]))

    plt.plot(range(len(X)),X)
    plt.plot(range(len(Y)),Y)
    plt.plot(X,Y)
    plt.ylabel("Position (en mm)")
    plt.xlabel("Temps")
    plt.show()

    #plt.plot(range(len(equF)),equF)
    #plt.plot(range(len(equG)),equG)
    #plt.show()

    #plt.plot(equF,equG)
    #plt.show()
"""