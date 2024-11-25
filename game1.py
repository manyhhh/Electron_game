#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 15:26:27 2022
Modified on Fri Mar 11 15:26:27 2022
@author: ????????????????????????

Description
------------
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

# Create the source charges

qs = [1,-1,1,-1]
qx = [60,-30,-20,40]
qy = [60,80,-150,-50]

# Set the default initial conditions for v0, angle, and y0
v0, angle, y0 = 50.0, 30.0, 30.0    
# Keep x0 fixed at -100
x0 = -100.

# Create the pyplot window
fig = plt.figure('Game Window')
def clear():
    plt.clf()
    plt.axis('square')
    plt.xlim(-200,200)
    plt.ylim(-200,200)
    plt.title('Electrostatic Projectile Game',fontsize=16)
    plt.xlabel('x position (meters)',fontsize=16)
    plt.ylabel('y position (meters)',fontsize=16)
    plt.grid(visible=True)
    plt.tight_layout()    
    plt.show()
    return
clear()

############################################################

def show_potential():
    
    # your code goes here
    #fig1 = plt.figure(1)
    #ax1 = fig1.gca()
    xvals = np.linspace(-200,200,150)
    yvals = np.linspace(-200,200,150)
    X, Y = np.meshgrid(xvals,yvals)
    outpot = np.zeros(150*150).reshape(150,150)
    for row in range(150):
        for col in range(150):
            outpot[row,col] = potential(X[row,col],Y[row,col])
    return plt.contour(X,Y,outpot,levels=np.linspace(-6000,6000,30))

#def wire_pot():
    #xvals = np.linspace(-200,200,500)
    #yvals = np.linspace(-200,200,500)
    #X, Y = np.meshgrid(xvals,yvals)
    #outpot = np.zeros(500*500).reshape(500,500)
    #for row in range(500):
        #for col in range(500):
            #outpot[row,col] = potential(X[row,col],Y[row,col])
    #fig1 = plt.figure(1)
    #ax1 = fig1.add_subplot(projection='3d')
    #return ax1.plot_wireframe(X,Y,outpot)

############################################################

def show_forcefield():
    
    # your code goes here
    #fig2 = plt.figure()
    #ax2 = fig2.gca()
    xvals = np.linspace(-200,200,150)
    yvals = np.linspace(-200,200,150)
    X, Y = np.meshgrid(xvals,yvals)
    FX = np.zeros(150*150).reshape(150,150)
    FY = np.zeros(150*150).reshape(150,150)
    for row in range(150):
        for col in range(150):
            FX[row,col], FY[row,col] = force(X[row,col],Y[row,col])
    return plt.streamplot(X,Y,FX,FY)

############################################################

def play():
    
    global v0, angle, y0
    
    print("Starting x location is -100")
    v0 = float(input("Enter the initial speed between zero and 100.\n"))
    assert(v0 >= 0 and v0 <= 100), "Initial velocity should > 0 and < 100"
    angle = float(input("Enter the initial angle in degrees.\n"))
    assert(angle >= -180.00 and angle <= 180.00), \
        "Angle should be between -180 and +180"
    y0 = float(input("Enter the initial y position.\n"))
    assert(y0 >= -200 and y0 <= 200), "y0 should be between -200 and +200"
    
    plot_trajectory()
    
    return

############################################################

def plot_trajectory():

    # Your code goes here
    def derivatives(t,s):
        # s[0] = xpos
        # s[1] = xvel
        # s[2] = ypos
        # s[3] = yvel
        D = [0,0,0,0]
        D[0] = s[1]
        D[1] = force(s[0],s[2])[0]
        D[2] = s[3]
        D[3] = force(s[0],s[2])[1]
        return D
    vx0 = v0*np.cos(np.pi*angle/180)
    vy0 = v0*np.sin(np.pi*angle/180)
    #x0, y0 previously defined as -100, 30 respectively
    s0 = (x0,vx0,y0,vy0)
    t0, t1 = 0, 10
    solution = solve_ivp(derivatives,(t0,t1),s0,dense_output=True)
    tt=np.linspace(t0,t1,100)
    xpos,xvel,ypos,yvel = solution.sol(tt)
    #fig3 = plt.figure()
    #ax3 = fig2.gca()
    plt.plot(xpos,ypos)
    plt.plot(xpos[::5],ypos[::5],'ok',markersize=4)
    plt.show()
    return 

############################################################

def solve_it():
    print('Does quadrant 1 have:\n(1) a positive charge \n(2) a negative charge \n(3) neither \n(4) both')
    q1a = int(input('Enter an integer in between 1 and 4 to answer.\n'))
    #Q1 has a positive charge
    if q1a == 1:
        print('Correct!')
    else:
        print('Incorrect :(')
    print('Does quadrant 2 have:\n(1) a positive charge \n(2) a negative charge \n(3) neither \n(4) both')
    q2a = int(input('Enter an integer in between 1 and 4 to answer.\n'))
    #Q2 has a negative charge
    if q2a == 2:
        print('Correct!')
    else:
        print('Incorrect :(')
    print('Does quadrant 3 have:\n(1) a positive charge \n(2) a negative charge \n(3) neither \n(4) both')
    q3a = int(input('Enter an integer in between 1 and 4 to answer.\n'))
    #Q3 has a positive charge
    if q3a == 1:
        print('Correct!')
    else:
        print('Incorrect :(')
    print('Does quadrant 4 have:\n(1) a positive charge \n(2) a negative charge \n(3) neither \n(4) both')
    q4a = int(input('Enter an integer in between 1 and 4 to answer.\n'))
    #Q2 has a negative charge
    if q4a == 2:
        print('Correct!')
    else:
        print('Incorrect :(')
    qtot = q1a/7 + q2a/13 + q3a/17 + q4a/23
    ans = 1/7 + 2/13 + 1/17 + 2/23
    if qtot == ans:
        print('Congragulations!')
        show_potential()
    else:
        print('Sorry, try again.')
    return


############################################################

def force(x,y):
    
    k = 1000.0
    Fx = 0.0
    Fy = 0.0
    
    for i in range(len(qs)):
        distance_sqrd = (x-qx[i])**2 + (y-qy[i])**2
        if not np.isclose(distance_sqrd,0.0):
            Fx = Fx + k*qs[i]*(x-qx[i])/distance_sqrd
            Fy = Fy + k*qs[i]*(y-qy[i])/distance_sqrd

    return Fx, Fy


############################################################

def potential(x, y):

    k = 1000.0
    Vee = 0.0
    
    for i in range(len(qs)):
        distance = np.sqrt((x-qx[i])**2 + (y-qy[i])**2)
        if not np.isclose(distance,0.0):
            Vee = Vee + k*qs[i]*np.log(1.0/distance)

    return Vee










