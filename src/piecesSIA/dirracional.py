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

seq=[(i-1.)/i for i in range(60)[1::2]]
# particionamento d oitava em 17 grados, 18 com a oitava
seq=[i for i in n.linspace(0,1,14)] 
s1=seq[::2]+seq[::-2]  # simetrica
s2=seq[::4]+seq[::-2]  # na primeira metade
s3=seq[::2]+seq[::-4]  # na segunda metade
s4=seq  # no comec
s5=seq[::-1]  # no fim
pausa=p=[0.]*8
s_=s1+p+s2+p+s3+p+s4+p+s5+p+p

s=H(([adsr(v(tab=Tr_i,f=800.*2.**(ss),nu=0.5,d=.2,fv=20),
                            70.,100.,R=20.) for ss in s_]))
W(s, "dirracional.wav")
