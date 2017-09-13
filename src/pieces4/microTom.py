#-*- coding: utf-8 -*-
import numpy as n
import random as r
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


def ac(f=200.,notas=[0.,4.,7.,12.],tab=S_i):
    acorde=adsr(v(tab=tab,f=f*2.**(notas[-1]/12.),nu=0))
    for na in notas[:-1]:
        acorde+=adsr(v(tab=tab,f=f*2**(na/12.),nu=0))
    
    return acorde


# Microtonalidade
epslon=2**(1/12.)  # divisão da oitava em 12 semitons
# quartos de tom sao metade do semitom
ff=[0.,0.5,3.5,4.,4.5,5. ,  7.,7.5]
dd=[.5,.25,  .25,.5/2,.25, .25,.5/4,.5/4]
tt=[adsr(v(tab=Tr_i,f=200*2**(f/12),d=d,nu=0),R=30.) for
        f,d in zip(ff,dd)]
s=H((tt+tt[::-1]))

ff=[3.5,4.,4.5,  6.5, 7.,7.5, 7. ,  6.5]
dd=[.5,.25, .25,  .5/2, .25, .25,.5/4,.5/4]
tt=[adsr(v(tab=Tr_i,f=200*2**(f/12),d=d,nu=0),R=30.) for 
        f,d in zip(ff,dd)]
so=H((tt+tt[::-1]))
s=H(([s]+tt+tt[::-1]))

# ou em 7 grados na oitava com um estilo tradicional tailandês
epslon=2**(1/7.)
ff=[0.,1.,2.,3.,4.,5.,6.,7.]
dd=[.8,0.4,0.2,.1,0.4]

ff=[200.*2.**(r.choice(ff)/7.) for i in xrange(15*3)] # 15 notas
dd=[r.choice(dd) for i in               xrange(15*3)] # 15 notas

tt=[adsr(v(tab=Tr_i,f=f,d=d,nu=0),R=50.) for f,d in zip(ff,dd)]
s=H(([s]+tt+tt[::-1]))

sa=H((s[::2],s[::-2],s[::2],s[::-2]))

ff=[0.,1.,2.,3.,4.,5.,6.,7.]
ff=[50.*2.**(r.choice(ff)/7.) for i in xrange(15*3)] # 15 notas
dd=[.8,0.4,0.2,.1,0.4]
dd=[r.choice(dd) for i in               xrange(15*3)] # 15 notas

tt=[adsr(v(tab=Tr_i,f=f,d=d,nu=7.,fv=12),R=50.) for 
        f,d in zip(ff,dd)]
sg=H((tt+tt[::-1]))*2.

m=min(len(so),len(sa),len(sg))
foo=H((so[:m]+sa[:m]+sg[:m]))

s=H((s,foo,foo,foo,foo,foo,foo,foo))

s=((s-s.min())/(s.max()-s.min()))*2.-1.

# most music players read only 16-bit wav files, so let's convert the array
s = n.int16(s * float(2**15))

w.write("microTom.wav",f_a,s)
