"""
Práctica 2:sistema respiratorio


Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México


Nombre del alumno:Perez Castillo Natalie Jaqueline
Número de control: 22210425
Correo institucional

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""

# Instalar librerias en consola
#!pip install control
#!pip install slycot

# Librerías para cálculo numérico y generación de gráficas
import numpy as np
import math as m
import matplotlib.pyplot as plt
import control as ctrl

# Datos de la simulación
x0,t0,tend,dt,w,h =0,0,30,1E-3,6,3
N = round((tend-t0)/dt)+1
t = np.linspace(t0,tend,N)
u1 = 2.5*np.sin(m.pi/2*t) # Respiración normal
u2 = 1.5*np.sin(m.pi*t) # Respiración anormal [Taquipnea]
u = np.stack((u1, u2), axis = 1)
signal=['Normal','Taquipnea']

def sys_respiratorio(RP,CL):
        RC,LC,CS,CW = 1, 0.01, 0.005, 0.2
        alpha3 = CL*CS*LC*RP*CW
        alpha2 = CL*CS*LC + CL*LC*CW + CS*LC*CW + CL*CS*RC*RP*CW
        alpha1 = CL*CS*RC + CL*RC*CW + CS*RC*CW + CL*RP*CW
        alpha0 = CL + CW
        num = [alpha0]
        den = [alpha3,alpha2,alpha1, alpha0]
        sys = ctrl.tf(num,den)
        return sys

#Funcion de transferencia: Individuo saludable [control]
RP, CL = 0.5, 0.2
sysS = sys_respiratorio(RP, CL)
print('Individuo sano [control]:')
print(sysS)

#Funcion de transferencia: Individuo enfermo [caso]
RP, CL = 7.5, 0.4
sysE = sys_respiratorio(RP, CL)
print('Individuo enfermo [caso]:')
print(sysE)

def plotsignals(u, sysS, sysE, sysPID, signal):
    fig = plt.figure()
    ts,Vs = ctrl.forced_response(sysS,t,u,x0)
    plt.plot(t,Vs, '-', color = [0.1,.5,.7], label = '$P_A(t): Control$')
    ts,Ve = ctrl.forced_response(sysE,t,u,x0)
    plt.plot(t,Ve,'-', color = [1,0,0], label = '$P_A(t): Caso$')
    ts,pid = ctrl.forced_response(sysPID,t,Vs,x0)
    plt.plot(t,pid, ':', linewidth = 3, color = [0.6,.2,.5],
             label = '$PA(t): Tratamiento$')
    plt.grid(False)
    plt.xlim(0, 30)
    plt.ylim(-3, 3)
    plt.xticks(np.arange(0, 31, 2))
    plt.yticks(np.arange(-3, 3.5, 0.5))
    plt.xlabel('$t$ [s]')
    plt.ylabel('$PA(t)$ [V]')
    plt.legend(bbox_to_anchor = (0.5,-0.3), loc = 'center', ncol = 4,
               fontsize = 8, frameon = False)
    plt.show()
    fig.set_size_inches(w,h)
    fig.tight_layout()
    namepng = 'python_' + signal + '.png'
    namepdf = 'python_' + signal + '.pdf'
    fig.savefig(namepng,dpi = 600, bbox_inches = 'tight')
    fig.savefig(namepdf,bbox_inches ='tight')
   
def tratamiento(Cr,Re,Rr,Ce,sysE):
    numPID = [Re*Rr*Ce*Cr,Re*Ce+Rr*Cr,1]
    denPID = [Re*Cr,0]
    PID = ctrl.tf(numPID,denPID)
    X = ctrl.series(PID,sysE)
    sysPID = ctrl.feedback(X, 1, sign = -1)
    return sysPID

# Sistema de control en lazo cerrado
kP, kI, kD, Cr = 16.831946, 330.170634, 0, 1E-6  
Re = 1/(kI*Cr)
Rr = kP*Re
Ce = kD/Rr
sysPID = tratamiento(Cr,Re,Rr,Ce,sysE)
plotsignals(u1, sysS, sysE, sysPID, 'normal')
plotsignals(u2, sysS, sysE, sysPID, 'taquipnea')


