import numpy as n
import random as r
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

# Microtonality
epslon=2**(1/12.)
# quarter tones
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

# octave in 7 steps as one genre of Tai music
epslon=2**(1/7.)
ff=[0.,1.,2.,3.,4.,5.,6.,7.]
dd=[.8,0.4,0.2,.1,0.4]

ff=[200.*2.**(r.choice(ff)/7.) for i in range(15*3)] # 15 notas
dd=[r.choice(dd) for i in               range(15*3)] # 15 notas

tt=[adsr(v(tab=Tr_i,f=2*f,d=d,nu=0),R=50.) for f,d in zip(ff,dd)]
s_=H(([s]+tt+tt[::-1]))
sb=adsr(H((s_[::2],s_[::-2],s_[::2],s_[::-2])))

tt=[adsr(v(tab=Tr_i,f=f,d=d,nu=0),R=50.) for f,d in zip(ff,dd)]
s=H(([s]+tt+tt[::-1]))
sa=adsr(H((s[::2],s[::-2],s[::2],s[::-2])))

ff=[0.,1.,2.,3.,4.,5.,6.,7.]
ff=[100.*2.**(r.choice(ff)/7.) for i in range(15*3)] # 15 notas
dd=[.8,0.4,0.2,.1,0.4]
dd=[r.choice(dd) for i in               range(15*3)] # 15 notas

tt=[adsr(v(tab=Tr_i,f=f,d=d,nu=7.,fv=12),R=50.) for 
        f,d in zip(ff,dd)]
sg=H((tt+tt[::-1]))*2.

m=min(len(so),len(sa),len(sg))
foo=H((so[:m]+sa[:m]+sg[:m]))
foo2=H((so[:m]+sb[:m]+sg[:m]))

s=H((s,foo,foo,foo2,foo2,foo,foo,foo))

W(s, "microTom.wav")
