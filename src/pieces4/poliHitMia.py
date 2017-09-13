#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

f_a = 44100. # Hz, frequência de amostragem

############## 2.2.1 Tabela de busca (LUT)
Lambda_tilde=Lt=1024.*16

# Senoide
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras

# Quadrada:
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )

# Triangular:
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

# Dente de Serra:
D_i=n.linspace(-1,1,Lt)


def v(f=200,d=2.,tab=S_i,fv=2.,nu=2.,tabv=S_i):
    Lambda=n.floor(f_a*d)
    ii=n.arange(Lambda)
    Lv=float(len(tabv))

    Gammav_i=n.floor(ii*fv*Lv/f_a) # índices para a LUT
    Gammav_i=n.array(Gammav_i,n.int)
    # padrão de variação do vibrato para cada amostra
    Tv_i=tabv[Gammav_i%int(Lv)] 

    # frequência em Hz em cada amostra
    F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
    # a movimentação na tabela por amostra
    D_gamma_i=F_i*(Lt/float(f_a))
    Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
    Gamma_i=n.floor( Gamma_i) # já os índices
    Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
    return tab[Gamma_i%int(Lt)] # busca dos índices na tabela

def A(fa=2.,V_dB=10.,d=2.,taba=S_i):
    Lambda=n.floor(f_a*d)
    ii=n.arange(Lambda)
    Lt=float(len(taba))
    Gammaa_i=n.floor(ii*fa*Lt/f_a) # índices para a LUT
    Gammaa_i=n.array(Gammaa_i,n.int)
    # variação da amplitude em cada amostra
    A_i=taba[Gammaa_i%int(Lt)] 
    A_i=A_i*10.**(V_dB/20.)
    return A_i

def adsr(som,A=10.,D=20.,S=-20.,R=100.,xi=1e-2):
    a_S=10**(S/20.)
    Lambda=len(som)
    Lambda_A=int(A*f_a*0.001)
    Lambda_D=int(D*f_a*0.001)
    Lambda_R=int(R*f_a*0.001)

    ii=n.arange(Lambda_A,dtype=n.float)
    A=ii/(Lambda_A-1)
    A_i=A
    ii=n.arange(Lambda_A,Lambda_D+Lambda_A,dtype=n.float)
    D=1-(1-a_S)*(   ( ii-Lambda_A )/( Lambda_D-1) )
    A_i=n.hstack(  (A_i, D  )   )
    S=n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D),dtype=n.float)*a_S
    A_i=n.hstack( ( A_i, S )  )
    ii=n.arange(Lambda-Lambda_R,Lambda,dtype=n.float)
    R=a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
    A_i=n.hstack(  (A_i,R)  )

    return som*A_i

triadeM=[0.,4.,7.]
def ac(f=200.,notas=[0.,4.,7.,12.],tab=S_i):
    acorde=adsr(v(tab=tab,f=f*2.**(notas[-1]/12.),nu=0))
    for na in notas[:-1]:
        acorde+=adsr(v(tab=tab,f=f*2**(na/12.),nu=0))
    
    return acorde


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
        for ii in xrange(int(d)):
            if ii%2==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        metricas.append(tempo)
    if d in [3,6,9]: # compassos compostos
        tempo=n.zeros(T_)
        for ii in xrange(int(d)):
            if ii%3==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        metricas.append(tempo)
    if d in [5,7]: # compassos complexos
        tempo=n.zeros(T_)
        for ii in xrange(int(d/2)):
            if ii%3==0:
                tempo[ii*T_/d]=1
            else:
                tempo[ii*T_/d]=.5
        for ii in xrange(int(d/2),int(d)):
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
for i in xrange(4):
    l4[i*(T_/4):i*(T_/4)+.1*f_a]=\
               v(tab=Tr_i,f=150.*2.**(r.choice(EM_i)/12.),d=.1)

l4b=n.zeros(T_)

import random as r
EM_i=[0.,2.,4.,5.,7.,9.,11.]
for i in xrange(4):
    l4b[i*(T_/4):i*(T_/4)+.1*f_a]=\
          v(tab=Tr_i,f=150.*2.**(r.choice(EM_i)/12.),d=.1,fv=6.)


s=H((s, l5+l1+l4, l5+l2+l4b, l5+l1+l4,l5+l1+l7+l4 ,
        l5+l1+l4b, l5+l2+l4, l5+l1+l4b,l5+l1+l7+l4))

s=H((s,s[::-2],s[::-4],s[::-4],s))

s=((s-s.min())/(s.max()-s.min()))*2.-1.

# most music players read only 16-bit wav files, so let's convert the array
s = n.int16(s * float(2**15))

w.write("poliHitMia.wav",f_a,s)
