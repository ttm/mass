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

        
        

BPM=60. # BPM batidas por minuto
DELTA=BPM/60. # duração da batida em segundos
LAMBDA=DELTA*f_a # número de samples da batida
LAMBDA_=int(LAMBDA) # inteiro para operação com índices

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

som=n.array([-5,6])

som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
print "AA"
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')
print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TrenzinhoImpulsivo.wav",f_a,T_i) # escrita do som


#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)

contracontra=n.copy(tempo);contracontra[-LAMBDA_/4]=-1.

linha_contracontra=contracontra[ii%LAMBDA_]

print "AA"
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')+\
    n.convolve(som3,linha_contracontra,'same')
print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

# escrita do som em disco
w.write("TrenzinhoImpulsivo2.wav",f_a,T_i)


#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]


print "AA"
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')+\
    n.convolve(som3,linha_contracontra,'same')+\
    n.convolve(som4,linha_em3,'same')
print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo3.wav",f_a,aa)

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]


print "AA"
som=n.convolve(som2,linha_cabeca+linha_contra,'same')+\
    n.convolve(som4,linha_em3,'same')
print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo4.wav",f_a,aa)

##################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print "AA"
linha1=n.convolve(som2,linha_cabeca,'same')
linha2=n.convolve(som4,linha_em3,'same')
linha3=n.convolve(som2,linha_contra,'same')
som=n.hstack((linha1+linha2,linha1+linha3,linha2+linha3,\
                                    linha1+linha2+linha3))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo5.wav",f_a,aa)

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo6.wav",f_a,aa)

##################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,\
                             linha1+linha2+linha3,linha1))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo7.wav",f_a,aa)

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr( v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),
                                        10.,10.,-20.,180. )

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo8.wav",f_a,aa)

#
#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr( v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),
                                        10.,10.,-20.,180. )

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=6.*n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo9.wav",f_a,aa)

som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.),1.,100.,-60.,80.)

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=6.*n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo10.wav",f_a,aa)


som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.),1.,100.,-60.,80.)
som5=adsr( v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.)*A(d=.2,fa=100.),
                                                 1.,100.,-60.,80. )
som6=adsr( v(tabv=Tr_i ,d=.2,fv=30.,nu=7.,f=1800.)*A(d=.2),
                                          1.,100.,-60.,80. )

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]


print "AA"
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha4=n.convolve(som5,linha_em3)[:len(linha_em3)]
linha6=n.convolve(som6,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))
som=n.hstack((som,linha4+linha2,linha6+linha3,linha4+linha3+linha1,
                                 linha1+linha2+linha3,linha6+linha2))

print "BB"
T_i=som

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
aa = n.int16(aa * float(2**15))

w.write("TrenzinhoImpulsivo11.wav",f_a,aa)
