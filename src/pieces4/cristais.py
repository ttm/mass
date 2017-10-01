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

### 2..7.5. Simetric scales
Ec_i=[0.,1.,2.,3.,4.,5.,6.,7.,8.,9.,10.,11.]
Et_i=[0.,2.,4.,6.,8.,10.]
Etm_i=[0.,3.,6.,9.]
EtM_i=[0.,4.,8.]
Ett_i=[0.,6.]

notast_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in Et_i]

notast_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Et_i]
s=H( notast_D +notast_A+notast_D)
s1=n.copy(s)

notastm_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in Etm_i]

notastm_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Etm_i]
s=H(( notastm_D +notastm_A+notastm_D))

notastM_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in  EtM_i]

notastM_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in EtM_i]
s=H(( [list(s)]+ notastM_D +notastM_A+notastM_D))

notastt_A=[adsr( v(200*2**(i/12.),d=.2 ) ) for i in  Ett_i]

notastt_D=[adsr( v(400*2**(-i/12.),d=.2 ) ) for i in Ett_i]
s=H(( [list(s)]+ notastt_D +notastt_A+notastt_D))

s=H((s,s[::-1]))
s=H((s,s[::2],s[::-2]))
s=H((  s,s+H((s[::2],s[::-2])),
       s+H((s[::4],s[::-4],s[::4],s[::-8],s[::-8])) ))

W(s, "cristais.wav")
