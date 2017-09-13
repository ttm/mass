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





T=v(tabv=Tr_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Tr_i ,d=2.,fv=0.,nu=7.0)*A()


T_i=n.hstack((T,T2))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia.wav",f_a,T_i) 


###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0)*A()


T_i=n.hstack((T,T2))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia2.wav",f_a,T_i) 


###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()


T_i=n.hstack((T,T2))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia3.wav",f_a,T_i) 



###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()
T3=v(tabv=Q_i ,d=2.,fv=40.,nu=7.0,f=100)*A()
T4=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100)*A()
T5=v(tabv=Q_i ,d=2.,fv=32.,nu=7.0,f=100)*A()


T_i=n.hstack((T,T2,T3,T4,T5))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia4.wav",f_a,T_i) 

###############
T=v(tabv=Q_i ,d=2.,fv=35.,nu=7.0)*A()
T2=v(tabv=Q_i ,d=2.,fv=20.,nu=12.0,f=100)*A()
T3=v(tabv=Q_i ,d=2.,fv=40.,nu=7.0,f=100)*A()
T4=v(tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100)*A()
T5=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100)*A()


T_i=n.hstack((T,T2,T3,T4,T5))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia5.wav",f_a,T_i) 



#########
T4=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T5=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100)


T_i=n.hstack((T4,T5,T4,T5,T4,T5))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia6.wav",f_a,T_i) 

##########
T1=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T2=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T3=v(tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100)
T4=v(tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)


T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia7.wav",f_a,T_i) 



##########
T1=v(tabv=D_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T2=v(tabv=Q_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T3=v(tabv=S_i ,d=2.,fv=30.,nu=7.0,f=100 )*A()
T4=v(tabv=Tr_i ,d=2.,fv=30.,nu=7.0,f=100)*A()


T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia8.wav",f_a,T_i) 


##########
T1=v(tabv=D_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T2=v(tabv=Q_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T3=v(tabv=S_i ,d=2.,fv=5*30.,nu=7.0,f=100 )*A(fa=1.)
T4=v(tabv=Tr_i ,d=2.,fv=5*30.,nu=7.0,f=100)*A(fa=1.)


T_i=n.hstack((T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T2,T3,T4,T1,T1,T1))
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia9.wav",f_a,T_i) 


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


T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia10.wav",f_a,T_i) 




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


T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia11.wav",f_a,T_i) 



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





T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia12.wav",f_a,T_i) 


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





T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia13.wav",f_a,T_i) 




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



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia14.wav",f_a,T_i) 


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







T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia15.wav",f_a,T_i) 

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



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia16.wav",f_a,T_i) 

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



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia17.wav",f_a,T_i) 

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



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia18.wav",f_a,T_i) 


T1=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=6.,taba=D_i) # Animal
T2=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=7.,taba=D_i) # Animal
T3=v(tab=S_i,tabv=S_i ,d=2.,fv=30.,nu= 49.0,f=40 )*A(fa=8.,taba=D_i) # Animal
T4=v(tab=S_i,tabv=Tr_i ,d=2.,fv=30.,nu=49.0,f=40)*A(fa=0.5) # Fodah

T_i=n.hstack((T1,T2,T3,T4))



T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())

# most music players read only 16-bit wav files, so let's convert the array
T_i = n.int16(T_i * float(2**15))

w.write("TremolosVibratosEaFrequencia19.wav",f_a,T_i) 

