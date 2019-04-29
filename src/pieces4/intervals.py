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
def adsr(s, A=3, D=2, S=-10, R=2):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
def T(f1, f2, dur, ttype="exp", tab=S_i, alpha=1.):
    return adsr(fun.P(f1, f2, dur, alpha, tab, ttype))
f_a = 44100 # Hz, sample rate

### 2.74
I1j=0.
I2m=1.
I2M=2.
I3m=3.
I3M=4.
I4J=5.
ITR=6.
I5J=7.
I6m=8.
I6M=9.
I7m=10.
I7M=11.
I8J=12.
I_i=n.arange(13.)

# Interval inversion
def inv(I):
    """retorna intervalo inverso de I: 0<= I <=12"""
    return 12-I

# harmonic interval
def intervaloHarmonico(f,I,d=.3):
    return (  adsr(v(f,d=d)+v(f*2.**(I/12.),d=d))  )*0.5
# melodic interval
def intervaloMelodico(f,I,d=.5):
    return n.hstack((  adsr(v(f,d=d)), adsr(v(f*2.**(I/12.),d=d))  ))

s=n.array([])
for i in I_i:
    s=n.hstack(( s,n.zeros(f_a/10),intervaloMelodico(200.,i,d=0.1) ))

for i in I_i:
    s=n.hstack(( s,n.zeros(f_a/10),intervaloHarmonico(200,i,d=.2) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,i,d=0.01) +v(400,d=0.02)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,-i  ,d=0.05)  ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.05)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,6-i,d= 0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,12-i,d=0.1)))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,5-i, d=0.1)))



for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,6-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,5-i ,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,5-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,12-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))



for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(300,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(600,7-i ,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloMelodico(200,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(400,11-i,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(300,7-i ,d=0.05) ))

for i in I_i:
    s=n.hstack(( s,intervaloMelodico(600,11-i,d=0.05) ))


for i in I_i:
    s=n.hstack(( s,intervaloHarmonico(200,i) ))

W(s, "intervalosEntreAlturas.wav")
