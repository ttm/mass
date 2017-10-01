import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

W = fun.W
Tr_i = fun.Tr
Q_i = fun.Q
D_i = fun.Sa
S_i = fun.S
H = n.hstack
V = n.vstack
def v(f=220, d=2, fv=4, nu=2, tab=Tr_i, tabv=S_i,
        alpha=1, nsamples=0, fs=44100):
    return adsr( fun.V(f, d, fv, nu, tab, tabv,
        alpha, nsamples, fs), A=5, D=4, R=5)
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
def T(f1, f2, dur, ttype="exp", tab=S_i, alpha=1.):
    return adsr(fun.P(f1, f2, dur, alpha, tab, ttype))
f_a = 44100 # Hz, sample rate

############## Poli Hit Mia
# Divisoes do pulso
dd = [1.,2.,3.,4.,5.,6.,7.,8.,9.]

BPM=90. #batidas por minuto
T=(BPM/60.) # duração do tempo
T_=int(T*f_a) # número de amostras

metricas=[]

for d in dd:
    if d in [1,2,4,8]: # compasso metricas
        tempo=n.zeros(T_)
        for ii in range(int(d)):
            if ii%2==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        metricas.append(tempo)
    if d in [3,6,9]: # compassos compostos
        tempo=n.zeros(T_)
        for ii in range(int(d)):
            if ii%3==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        metricas.append(tempo)
    if d in [5,7]: # compassos complexos
        tempo=n.zeros(T_)
        for ii in range(int(d/2)):
            if ii%3==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        for ii in range(int(d/2),int(d)):
            if ii%2==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        metricas.append(tempo)

s1=v(d=.2)
s2=v(f=300.,d=.1)
s7=v(f=800.,d=.05)
s5=v(tab=Tr_i,f=100.,d=.1)

l1=n.convolve(s1,metricas[1])[:T_]
l2=n.convolve(s2,metricas[2])[:T_]
l7=n.convolve(s7,metricas[7])[:T_]
l5=n.convolve(s5,metricas[5])[:T_]

s=H((l1,l1,l2,l2,l1+l2,l1+l2))
s=H((s,l7+l1,l7+l2, l7+l5, l7,   l5+l1, l5+l2, l5+l1,l5+l1+l7   ))

l4=n.zeros(T_)

import random as r
EM_i=[0.,2.,4.,5.,7.,9.,11.]
for i in range(4):
    l4[i*(T_/4):i*(T_/4)+.1*f_a]=\
               v(tab=Tr_i,f=150.*2.**(r.choice(EM_i)/12.),d=.1)

l4b=n.zeros(T_)

import random as r
EM_i=[0.,2.,4.,5.,7.,9.,11.]
for i in range(4):
    l4b[i*(T_/4):i*(T_/4)+.1*f_a]=\
          v(tab=Tr_i,f=150.*2.**(r.choice(EM_i)/12.),d=.1,fv=6.)

s=H((s, l5+l1+l4, l5+l2+l4b, l5+l1+l4,l5+l1+l7+l4 ,
        l5+l1+l4b, l5+l2+l4, l5+l1+l4b,l5+l1+l7+l4))

s=H((s,s[::-2],s[::-4],s[::-4],s))

W(s, "poliHitMia.wav")
