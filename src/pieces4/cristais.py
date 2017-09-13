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


### 2..7.5. Escalas simétricas
Ec_i=[0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.]
Et_i=[0.,2.,4.,6.,8.,10.]
Etm_i=[0.,3.,6.,9.]
EtM_i=[0.,4.,8.]
Ett_i=[0.,6.]

notast_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in Et_i]

notast_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Et_i]
s=H( notast_D +notast_A+notast_D)
s1=n.copy(s)

notastm_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in Etm_i]

notastm_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Etm_i]
s=H(( notastm_D +notastm_A+notastm_D))

notastM_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in  EtM_i]

notastM_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in EtM_i]
s=H(( [list(s)]+ notastM_D +notastM_A+notastM_D))

notastt_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in  Ett_i]

notastt_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Ett_i]
s=H(( [list(s)]+ notastt_D +notastt_A+notastt_D))

s=H((s,s[::-1]))
s=H((s,s[::2],s[::-2]))
s=H((  s,s+H((s[::2],s[::-2])),
       s+H((s[::4],s[::-4],s[::4],s[::-8],s[::-8])) ))

s=((s-s.min())/(s.max()-s.min()))*2.-1.

# most music players read only 16-bit wav files, so let's convert the array
s = n.int16(s * float(2**15))

w.write("cristais.wav",f_a,s) # escrita do som
