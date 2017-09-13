#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

f_a = 44100. # Hz, frequência de amostragem

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


T=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)

T_i=n.hstack((n.zeros(f_a),adsr(v(tabv=Tr_i ,d=2.,fv=10.,nu=7.0),10,10,-5.),T))

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa.wav",f_a,T_i) # escrita do som


############
T=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)
T1=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,10,-10.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,5,-10.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),2,10,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr(v(tabv=Tr_i ,d=2.,fv=3.,  nu=3.),10,10,-10.)
T1=adsr(v(tabv=Tr_i ,d=2.,fv=1., nu=3.),5,10,-10.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=6., nu=3.),5,5,-10.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.),2,10,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa2.wav",f_a,T_i) # escrita do som


############
T= adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,10,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,5,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),2,10,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),10,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.),5,10,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.),5,5,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.),2,10,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa3.wav",f_a,T_i) # escrita do som


############
T= adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),2.,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),1.,10.,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),0.5, 5.,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),0.2,10.,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  5.,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  2,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1.,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,0.5,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa4.wav",f_a,T_i) # escrita do som

##########
T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  5.,-10,1000.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  2,-5,500.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1.,-20,200.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,0.5,-30,1500.)

T_i=n.hstack((T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  50.,-10,1000.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  200,-2,500.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1000.,-15,200.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,300.,-25,1500.)

T_i=n.hstack((T_i,T,T1,T2,T3))

T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa5.wav",f_a,T_i) # escrita do som


###########
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)

T_i=n.hstack((n.zeros(f_a),T1,T2,T3,T4))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa6.wav",f_a,T_i) # escrita do som

##################
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)

T_i=n.hstack((n.zeros(f_a),T1,T2,T3,T4))


T1=adsr(v(tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)


T_i=n.hstack((T_i,T1,T2,T3,T4))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("ADa_e_SaRa7.wav",f_a, T_i) # escrita do som
