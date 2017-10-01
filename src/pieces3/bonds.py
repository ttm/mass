#-*- coding: utf-8 -*-
import numpy as n
# from scipy.io import wavfile as w
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
W = fun.W
H = n.hstack
V = n.vstack
Tr_i = fun.Tr
Q_i = fun.Q
D_i = fun.Sa
S_i = fun.S

###############
T=v(tabv=Tr_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Tr_i ,d=2.,fv=0.,nu=7.0)*A()

T_i=n.hstack((T,T2))

W(T_i, "TremolosVibratosEaFrequencia.wav") 

###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0)*A()

T_i=n.hstack((T,T2))

W(T_i, "TremolosVibratosEaFrequencia2.wav") 

###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()

T_i=n.hstack((T,T2))

W(T_i, "TremolosVibratosEaFrequencia3.wav") 

###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()
T3=v(tabv=Q_i ,d=2.,fv=40.,nu=7.0,f=100)*A()
T4=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100)*A()
T5=v(tabv=Q_i ,d=2.,fv=32.,nu=7.0,f=100)*A()

T_i=n.hstack((T,T2,T3,T4,T5))

W(T_i, "TremolosVibratosEaFrequencia4.wav") 

###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()
T3=v(tabv=Q_i ,d=2.,fv=40.,nu=7.0,f=100)*A()
T4=v(tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100)*A()
T5=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100)*A()

T_i=n.hstack((T,T2,T3,T4,T5))

W(T_i, "TremolosVibratosEaFrequencia5.wav") 

#########
T4=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T5=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100)

T_i=n.hstack((T4,T5,T4,T5,T4,T5))

W(T_i, "TremolosVibratosEaFrequencia6.wav") 

##########
T1=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T2=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T3=v(tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T4=v(tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)

T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))

W(T_i, "TremolosVibratosEaFrequencia7.wav") 

##########
T1=v(tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T2=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T3=v(tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T4=v(tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A()

T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))

W(T_i, "TremolosVibratosEaFrequencia8.wav") 

##########
T1=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))

W(T_i, "TremolosVibratosEaFrequencia9.wav") 

#####################################
###
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T1,T2,T3,T4))

##
T1=v(tab=Q_i,tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=Q_i,tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=Q_i,tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=Q_i,tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=D_i,tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=D_i,tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=D_i,tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=D_i,tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=Tr_i,tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=Tr_i,tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=Tr_i,tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia10.wav") 

#####################################
###
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T1,T2,T3,T4))

##
T1=v(tab=Q_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=Q_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=Q_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=Q_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=D_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=D_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=D_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=D_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=Tr_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=Tr_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=Tr_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia11.wav") 

#####################
##
T1=v(tab=Tr_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=Tr_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=Tr_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=9.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=9.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=9.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=9.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 11.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 11.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 11.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=11.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 13.0,f=100 )*A(fa=1.)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 13.0,f=100 )*A(fa=1.)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 13.0,f=100 )*A(fa=1.)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=13.0,f=100)*A(fa=1.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia12.wav") 

#####################
##
T1=v(tab=Tr_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T2=v(tab=Tr_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T3=v(tab=Tr_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T4=v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=7.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu=9.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu=9.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu=9.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=9.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 11.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 11.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 11.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=11.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

##
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=13.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia13.wav") 

#########################
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 13.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=13.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i  ,d=2.,fv=30.,nu= 15.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i  ,d=2.,fv=30.,nu= 15.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i  ,d=2.,fv=30.,nu= 15.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu= 15.0,f=40 )*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 17.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 17.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 17.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=17.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=19.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia14.wav") 

######################
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 19.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=19.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=29.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=39.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5)
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia15.wav") 

##########################

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5) # YEH
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=29.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5) # Massa
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5) # bonito
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.5)
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=39.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3,T4))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5) # forte
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5) # bonito2
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5) # Animal
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5) # mto bom 

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia16.wav") 

##########################
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5) # YEH
#T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
#T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
#T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=29.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=3.) # Massa
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=1.) # bonito
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.05)
#T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=39.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5) # forte
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=.1) # bonito2
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=6.) # Animal
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5) # Fodah

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia17.wav") 

##########################
T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=.1) # YEH
#T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
#T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 29.0,f=40 )*A(fa=0.5)
#T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=29.0,f=40)*A(fa=0.5)

T_i=n.hstack((T1))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=8.) # Massa
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=3.) # bonito
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 39.0,f=40 )*A(fa=0.05)
#T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=39.0,f=40)*A(fa=0.5)

T_i=n.hstack((T_i,T1,T2,T3))

T1=v(tab=S_i,tabv=D_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=0.5) # forte
T2=v(tab=S_i,tabv=Q_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=.01) # bonito2
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=.2) # Animal
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5) # Fodah

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia18.wav") 

##########################
T1=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=6.,taba=D_i) # Animal
T2=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=7.,taba=D_i) # Animal
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=8.,taba=D_i) # Animal
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5) # Fodah

T_i=n.hstack((T1,T2,T3,T4))

W(T_i, "TremolosVibratosEaFrequencia19.wav") 
