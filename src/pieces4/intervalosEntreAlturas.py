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

def v(f=200.,d=2.,tab=S_i,fv=2.,nu=2.,tabv=S_i):
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

### 2.74
I1j=0.
I2m=1.
I2M=2.
I3m=3.
I3M=4.
I4J=5.
ITR=6.
I5J=7.
I6m=8.
I6M=9.
I7m=10.
I7M=11.
I8J=12.
I_i=n.arange(13.)

# o intervalo soma nove nomenclatuda da iversão 
# mas soma sempre 12 na inversão de semitons
def inv(I):
    """retorna intervalo inverso de I: 0<= I <=12"""
    return 12-I

# intervalo harmônico
def intervaloHarmonico(f,I,d=.3):
    return (  v(f,d=d)+v(f*2.**(I/12.),d=d)  )*0.5
# intervalo melódico
def intervaloMelodico(f,I,d=.5):
    return n.hstack((  v(f,d=d),v(f*2.**(I/12.),d=d)  ))

s=n.array([])
for i in I_i:
    s=n.hstack(( s,n.zeros(f_a/10),intervaloMelodico(200.,i,d=0.1) ))

for i in I_i:
    s=n.hstack(( s,n.zeros(f_a/10),intervaloHarmonico(200,i,d=.2) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,i,d=0.01) +v(400,d=0.02)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,-i  ,d=0.05)  ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.05)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,6-i,d= 0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,5-i, d=0.1)))



for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,6-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,5-i ,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,5-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))



for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(300,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(600,7-i ,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,11-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(300,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(600,11-i,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloHarmonico(200,i) ))

s=((s-s.min())/(s.max()-s.min()))*2.-1.

# most music players read only 16-bit wav files, so let's convert the array
s = n.int16(s * float(2**15))

w.write("intervalosEntreAlturas.wav",f_a,s) # escrita do som
