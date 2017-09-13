#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

f_a = 44100. # Hz, frequência de amostragem

############## 2.2.1 Tabela de busca (LUT)
Lambda_tilde=Lt=1024.

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
    Lv=float(len(S_i))

    Gammav_i=n.floor(ii*fv*Lv/f_a) # índices para a LUT
    Gammav_i=n.array(Gammav_i,n.int)
    Tv_i=tabv[Gammav_i%int(Lv)] # padrão de variação do vibrato para cada amostra

    F_i=f*(   2.**(  Tv_i*nu/12.  )   ) # frequência em Hz em cada amostra

    D_gamma_i=F_i*(Lt/float(f_a)) # a movimentação na tabela por amostra
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
### 2.55 padrão de oscilação do vibrato
    A_i=taba[Gammaa_i%int(Lt)] # padrão de variação da amplitude do tremolo para cada amostra
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

        
        

BPM=60. #80 batidas por minuto
DELTA=BPM/60 # duração da batida
LAMBDA=DELTA*f_a # número de samples da batida
LAMBDA_=int(LAMBDA) # inteiro para operação com índices

#cabeca=[1]+[0]*(LAMBDA-1)
#contra=[0]*Lambda/2+[1]+[0]*(Lambda/2-1)
tempo=n.zeros(LAMBDA)
cabeca=n.copy(tempo); cabeca[0]=1.
contra=n.copy(tempo); contra[LAMBDA_/2]=1.


# tempo de musica
Delta=4*DELTA # segundos
Lambda=Delta*f_a
Lambda_=int(Lambda)
ii=n.arange(Lambda_)
linha_cabeca=cabeca[ii%LAMBDA_]
linha_contra=contra[ii%LAMBDA_]

som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.),1.,100.,-60.,80.)
som5=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.)*A(d=.2,fa=100.),1.,100.,-60.,80.)
som6=adsr(v(tabv=Tr_i ,d=.2,fv=30.,nu=7.,f=1800.)*A(d=.2),1.,100.,-60.,80.)

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]

##############
#RUIDOS

Lambda = 100000 # Lambda sempre par
# diferença das frequências entre coeficiêntes vizinhos:
df=f_a/float(Lambda)

# e fase aleatoria
coefs=n.exp(1j*n.random.uniform(0, 2*n.pi, Lambda))
# real par, imaginaria impar
coefs[Lambda/2+1:]=n.real(coefs[1:Lambda/2])[::-1] - 1j*n.imag(coefs[1:Lambda/2])[::-1]
coefs[0]=0. # sem bias
coefs[Lambda/2]=1. # freq max eh real simplesmente

# as frequências relativas a cada coeficiente
# acima de Lambda/2 nao vale
fi=n.arange(coefs.shape[0])*df 
f0=15. # iniciamos o ruido em 15 Hz
i0=n.floor(f0/df) # primeiro coeff a valer
coefs[:i0]=n.zeros(i0)
f0=fi[i0]

# realizando o ruído em suas amostras temporais
ruido=n.fft.ifft(coefs)
r=n.real(ruido)
rb=((r-r.min())/(r.max()-r.min()))*2-1 # ruido branco


# fazendo ruido preto
fator=10.**(-7/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
rp=((r-r.min())/(r.max()-r.min()))*2-1



obj1=rb[:int(.4*f_a)]*A(d=.4,fa=15.)
obj2=rp[:int(.4*f_a)]*A(d=.4,fa=10.)

obj3=adsr(rb[:int(.4*f_a)]*A(d=.4,fa=15.))
obj4=adsr(rp[:int(.4*f_a)]*A(d=.4,fa=10.),S=-5)

obj5=adsr(rp[:int(1.4*f_a)]*A(d=1.4,fa=10.),5.,500.,-20,200)

############

l1=n.convolve(obj1,linha_em3)[:len(linha_em3)]
l2=n.convolve(obj2,linha_em3)[:len(linha_em3)]
l3=n.convolve(obj3,linha_em3)[:len(linha_em3)]
l4=n.convolve(obj4,linha_em3)[:len(linha_em3)]
l6=n.convolve(obj5,linha_em3)[:len(linha_em3)]

l1_=n.convolve(obj1,linha_cabeca)[:len(linha_em3)]
l2_=n.convolve(obj2,linha_contra)[:len(linha_em3)]
l3_=n.convolve(obj3,linha_cabeca)[:len(linha_em3)]
l4_=n.convolve(obj4,linha_contra)[:len(linha_em3)]
l6_=n.convolve(obj5,linha_cabeca)[:len(linha_em3)]



print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha4=n.convolve(som5,linha_em3)[:len(linha_em3)]
linha6=n.convolve(som6,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2+l1,linha2+linha3+l2,linha3+linha1+l3,linha1+linha2+linha3+l4,linha2+l6))
som=n.hstack((som,linha4+linha2+l1_,l2_+linha6+linha3,l3_+linha4+linha3+linha1,l4_+linha1+linha2+linha3,l6_+linha6+linha2))





print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("ruidosaFaixa.wav",f_a, aa) # escrita do som
