import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
W = fun.W
Tr_i = fun.Tr
Q_i = fun.Q
D_i = fun.Sa
S_i = fun.S
H = n.hstack
V = n.vstack
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
def T(f1, f2, dur, ttype="exp", tab=S_i, alpha=1.):
    return adsr(fun.P(f1, f2, dur, alpha, tab, ttype))
f_a = 44100 # Hz, sample rate

BPM=60.
DELTA=BPM/60. # duration of the beat in seconds
LAMBDA=DELTA*f_a # number of samples at each beat
LAMBDA_=int(LAMBDA)

tempo=n.zeros(LAMBDA)
cabeca=n.copy(tempo); cabeca[0]=1.
contra=n.copy(tempo); contra[LAMBDA_/2]=1.

# tempo
Delta=4*DELTA # seconds
Lambda=Delta*f_a
Lambda_=int(Lambda)
ii=n.arange(Lambda_)
linha_cabeca=cabeca[ii%LAMBDA_]
linha_contra=contra[ii%LAMBDA_]

som=n.array([-5,6])

som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
print("AA")
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')
print("BB")
T_i=som

W(T_i,"TrenzinhoImpulsivo.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)

contracontra=n.copy(tempo);contracontra[-LAMBDA_/4]=-1.

linha_contracontra=contracontra[ii%LAMBDA_]

print("AA")
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')+\
    n.convolve(som3,linha_contracontra,'same')
print("BB")
T_i=som

W(T_i,"TrenzinhoImpulsivo2.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print("AA")
som=n.convolve(som1,linha_cabeca,'same')+\
    n.convolve(som2,linha_contra,'same')+\
    n.convolve(som3,linha_contracontra,'same')+\
    n.convolve(som4,linha_em3,'same')
print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo3.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print("AA")
som=n.convolve(som2,linha_cabeca+linha_contra,'same')+\
    n.convolve(som4,linha_em3,'same')
print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo4.wav")

##################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca,'same')
linha2=n.convolve(som4,linha_em3,'same')
linha3=n.convolve(som2,linha_contra,'same')
som=n.hstack((linha1+linha2,linha1+linha3,linha2+linha3,\
                                    linha1+linha2+linha3))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo5.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo6.wav")

##################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),10.,10.,-10.)

em3=n.copy(tempo);contracontra[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=contracontra[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,\
                             linha1+linha2+linha3,linha1))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo7.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr( v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),
                                        10.,10.,-20.,180. )

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo8.wav")

#################
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr( v(tabv=Tr_i ,d=.2,fv=10.,nu=7.,f=800.)*A(d=.2),
                                        10.,10.,-20.,180. )

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=6.*n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo9.wav")

###############
som1=adsr(v(tabv=Tr_i ,d=.3,fv=3.,nu=7.0,f=300.),10,10,-10.)
som2=adsr(v(tabv=Tr_i ,d=.2,fv=2.,nu=1.),10,10,-10.)
som3=adsr(v(tabv=Tr_i ,d=.2,fv=10.,nu=7.),10,10,-10.)
som4=adsr(v(tabv=Tr_i ,d=.2,fv=3.,nu=7.,f=1800.),1.,100.,-60.,80.)

em3=n.copy(tempo);em3[[0,LAMBDA_/3,2*LAMBDA_/3]]=1.

linha_em3=em3[ii%LAMBDA_]

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=6.*n.convolve(som4,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo10.wav")

################
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

print("AA")
linha1=n.convolve(som2,linha_cabeca)[:len(linha_cabeca)]
linha2=n.convolve(som4,linha_em3)[:len(linha_em3)]
linha4=n.convolve(som5,linha_em3)[:len(linha_em3)]
linha6=n.convolve(som6,linha_em3)[:len(linha_em3)]
linha3=n.convolve(som2,linha_contra)[:len(linha_contra)]
som=n.hstack((linha1+linha2,linha2+linha3,linha3+linha1,
                             linha1+linha2+linha3,linha2))
som=n.hstack((som,linha4+linha2,linha6+linha3,linha4+linha3+linha1,
                                 linha1+linha2+linha3,linha6+linha2))

print("BB")

T_i=som
aa = n.hstack((T_i,T_i,T_i,T_i,T_i,T_i))
W(aa, "TrenzinhoImpulsivo11.wav")
