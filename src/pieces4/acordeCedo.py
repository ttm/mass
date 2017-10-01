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

triadeM=[0.,4.,7.]
def ac(f=200.,notas=[0.,4.,7.,12.],tab=S_i):
    acorde=adsr(v(tab=tab,f=f*2.**(notas[-1]/12.),nu=0))
    for na in notas[:-1]:
        acorde+=adsr(v(tab=tab,f=f*2**(na/12.),nu=0))
    
    return acorde

s=ac(200.,triadeM)
s2=ac(200.,triadeM,Tr_i)
s=H((s,s2,s,s2))


s1=ac(200.,triadeM)
s2=ac(200.,[0,5,9]) # subdominante
s3=ac(200.,[2,7,11]) # dominante
s4=ac(200.,[2,5,9]) # sub relativa
s5=ac(200.,[0,4,9]) # ton relat / sub anti


s=H((s,s1,s2,s3,s1,  s1,s4,s3,s1,  s1,s4,s3,s5, s5,s2,s3,s1  ))

W(s, "acordeCedo.wav")
