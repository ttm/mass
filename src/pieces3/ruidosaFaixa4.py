#-*- coding: utf-8 -*-
import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
W = fun.W
Tr_i = fun.Tr
Q_i = fun.Q
D_i = fun.Sa
S_i = fun.S
H = n.hstack
V = n.vstack
f_a = 44100 # Hz, sample rate

BPM=60.  # beats per minute
DELTA=BPM/60  # beat duration in seconds
LAMBDA=DELTA*f_a  # samples per beat
LAMBDA_=int(LAMBDA)

tempo=n.zeros(LAMBDA)
cabeca=n.copy(tempo); cabeca[0]=1.
contra=n.copy(tempo); contra[LAMBDA_/2]=1.

# tempo
Delta=4*DELTA
Lambda=Delta*f_a
Lambda_=int(Lambda)
ii=n.arange(Lambda_)
linha_cabeca=cabeca[ii%LAMBDA_]
linha_contra=contra[ii%LAMBDA_]

som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.),1.,100.,-60.,80.)
som5=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.)*A(d=.2,fa=100.),
                                                 1.,100.,-60.,80.)
som6=adsr(v(tabv=Tr_i ,d=.2,fv=30.,nu=7.,f=1800.)*A(d=.2),
                                          1.,100.,-60.,80.)

em3=n.copy(tempo); em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]

##############
# Noises

Lambda = 100000  # Lambda always even
# frequency difference between neighbor coefficients:
df=f_a/float(Lambda)

# as in section 3
coefs=n.exp(1j*n.random.uniform(0, 2*n.pi, Lambda))
coefs[Lambda/2+1:]=n.real(coefs[1:Lambda/2])[::-1] \
                   - 1j*n.imag(coefs[1:Lambda/2])[::-1]
coefs[0]=0.  # no bias
coefs[Lambda/2]=1.  # max freq is only real

fi=n.arange(coefs.shape[0])*df 
f0=15.
i0=n.floor(f0/df)
coefs[:i0]=n.zeros(i0)
f0=fi[i0]

ruido=n.fft.ifft(coefs)
r=n.real(ruido)
rb=((r-r.min())/(r.max()-r.min()))*2-1  # white noise

# black noise
fator=10.**(-7/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] -\
                1j*n.imag(c[1:Lambda/2])[::-1]
ruido=n.fft.ifft(c)
r=n.real(ruido)
rp=((r-r.min())/(r.max()-r.min()))*2-1

LR=rb[n.arange(int(len(linha_em3)*2.5))%len(rb)]*\
   A(d=int(len(linha_em3)*2.5)/f_a,fa=.2,V_dB=50.)*10**(-60/20.)

LR2=rb[n.arange(int(len(linha_em3)*4.5))%len(rb)]*\
    A(d=int(len(linha_em3)*4.5)/f_a)*.05

LR3=6.*rp[n.arange(int(len(linha_em3)*6.5))%len(rp)]*\
    A(d=int(len(linha_em3)*6.5)/f_a)*.05

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

linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha4=n.convolve(som5,linha_em3)[:len(linha_em3)]
linha6=n.convolve(som6,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]

H_i=(n.random.random(int(f_a*1.2))*2-1)*n.e**(-n.arange(int(f_a*1.2)))
def r(l):
    return n.convolve(H_i,l)[:len(linha_em3)]
    
som_e=n.hstack((r(linha2)+l1,linha3+r(l2),linha1+l3,
                       r(linha1)+linha2+linha3,r(l6)))
som_e=n.hstack((som_e, r(linha4)+l1_, r(l2_), l3_+linha3+linha1,
                           r(l4_)+linha1+linha3, r(l6_)+linha2))

som_d=n.hstack((linha1+r(linha2), linha2+linha3, r(linha3)+linha1,
                                         linha2+linha3+l4, linha2))
som_d=n.hstack((som_d, r(linha4)+l1_, r(l2_), l3_+linha4+linha1,
                        r(l4_)+linha2+linha3, r(linha6)+linha2))

som=n.vstack((som_e,som_d))

som[:, :len(LR)] += LR

som[:, len(l1)*3 : len(l1)*3 + len(LR2)] += LR2
som[:, int(len(l1)*3.5) : int(len(l1)*3.5) + len(LR3)] += LR3
som[:, len(l1)*7 : len(l1)*7 + len(LR)] += LR                     

T_i = som

aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i)).T
W(aa, "ruidosaFaixa4.wav")
