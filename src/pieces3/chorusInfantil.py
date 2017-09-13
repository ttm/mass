#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

f_a = 44100. # Hz, frequência de amostragem

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

s=v()
s1=v(fv=0.)
s2=v(nu=0.)
s3=v(fv=0.,nu=0.)
s4=v(tabv=D_i)

T_i=n.hstack((s, s1,s2,s3,s4))

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("chorusInfantil.wav",f_a,T_i) # escrita do som

# soh nos vibratos
s= v(d=8,)
s1=v(d=8,fv=4.)
s2=v(d=8,nu=0.2)
s3=v(d=8,fv=2.,nu=0.7)
s4=v(d=8,fv=3.,nu=.2)

T_i=n.hstack((s+ s1+s2+s3+s4))
T_i=((T_i-T_i.min())/(T_i.max()-T_i.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("chorusInfantil2.wav",f_a,T_i) # escrita do som

# nos vibratos e variacoes de f
amb=.2
s= v(f=200.*2.**((n.random.random()-0.5)*amb),d=8)
s1=v(f=200.*2.**((n.random.random()-0.5)*amb),d=8,fv=4.,nu=2.)
s2=v(f=200.*2.**((n.random.random()-0.5)*amb),d=8,fv=2.,nu=0.2)
s3=v(f=200.*2.**((n.random.random()-0.5)*amb),d=8,fv=2.,nu=0.7)
s4=v(f=200.*2.**((n.random.random()-0.5)*amb),d=8,fv=3.,nu=.2)

T_i=n.hstack((s+ s1+s2+s3+s4))
T_i=((T_i-T_i.min())/(T_i.max()-T_i.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("chorusInfantil3.wav",f_a,T_i) # escrita do som


# nos vibratos e variacoes de f
foobar=v(d=2,nu=0.)
amb=.03
amb_fv=4.
amb_nu=.1
s= v(f=200.*2.**((n.random.random()-0.5)*amb),d=6)
s1=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s2=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s3=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s4=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)

ss=n.hstack((foobar,s+s1+s2+s3+s4))

amb=.03
amb_fv=4.
amb_nu=.1
foobar2=v(tab=Tr_i,d=2,nu=0.)
s= v(tab=Tr_i,f=200.*2.**((n.random.random()-0.5)*amb),d=6)
s1=v(tab=Tr_i,f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s2=v(tab=Tr_i,f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s3=v(tab=Tr_i,f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s4=v(tab=Tr_i,f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)

ss=n.hstack((ss,foobar2,s+s1+s2+s3+s4))


amb=1.5 #AUMENTEI
s= v(f=200.*2.**((n.random.random()-0.5)*amb),d=6)
s1=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s2=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s3=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s4=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
     fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)

ss=n.hstack((ss,foobar,s+ s1+s2+s3+s4))


### agora o dobro dos caras:
amb=.03
s= v(f=200.*2.**((n.random.random()-0.5)*amb),d=6)
s1=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s2=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s3=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s4=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)


foo=s+ s1+s2+s3+s4
s= v(f=200.*2.**((n.random.random()-0.5)*amb),d=6)
s1=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s2=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s3=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)
s4=v(f=200.*2.**((n.random.random()-0.5)*amb),d=6,
    fv=n.random.random()*amb_fv,nu=n.random.random()*amb_nu)

ss=n.hstack((ss,foobar,(foo+s+ s1+s2+s3+s4)*.5))

T_i=ss
T_i=((T_i-T_i.min())/(T_i.max()-T_i.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("chorusInfantil4.wav",f_a,T_i) # escrita do som
