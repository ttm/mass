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

# montagem dedicada a explorar tremolos e vibratos
# independentemente e combinados

# partes:

# 1) som senoidal, vibrato senoidal com
# varreduras de frequência e de profundidade
# com a portadora em ao menos 3 frequencias diferentes

# 2) variacoes de vibrato em escala log e lin

# 3) vibratos com padrões diferentes do senoidal, sons diferentes
# do senoidal

# 4), 5) e 6) análogos para tremolos

# 7) usos combinados de ambos.

# * Todas as etapas se estendem para AM e FM

###################################################
# PART 1)
aa=v()
bb=v(nu=4.)
cc=v(f=300)
dd=v()

AA = n.hstack((aa,bb,cc,dd))
W(AA, "vbr.wav")

aa=v(f=800)
bb=v(nu=7.)
cc=v(f=300,fv=3)
dd=v()

AA = n.hstack((aa,bb,cc,dd))

W(AA, "vbr2.wav")

aa=v(f=600,fv=6)
bb=v(nu=7.,fv=12)
cc=v(f=300,fv=3,nu=24)
dd=v()

AA = n.hstack((aa,bb,cc,dd))

W(AA, "vbr3.wav")

aa=v(f=1600,fv=36)
bb=v(nu=36.,fv=12)
cc=v(f=300,fv=3,nu=24,tabv=D_i)
dd=v(tabv=D_i)

AA = n.hstack((aa,bb,cc,dd))

W(AA, "vbr4.wav")

aa=v(f=1600,fv=36,tabv=D_i)
bb=v(nu=2*36.,fv=12)
cc=v(f=300,fv=3,nu=24,tabv=Q_i)
dd=v(tabv=Q_i)

AA = n.hstack((aa,bb,cc,dd))

W(AA, "vbr5.wav")

aa=v(f=1600,fv=36,tabv=D_i)
aa2=v(f=1600,fv=36,tabv=Q_i)
aa3=v(f=1600,fv=36,tabv=Tr_i)
aa4=v(f=1600,fv=36,tabv=S_i)
bb=v(nu=2*36.,fv=12,tabv=Tr_i)
cc=v(f=300,fv=3,nu=24,tabv=Tr_i)
dd=v(tabv=Tr_i)

AA = n.hstack((aa,aa2,aa3,aa4,bb,cc,dd))

W(AA, "vbr6.wav")

aa=v(f=1600, fv=3,nu=5,tabv=D_i)
aa2=v(f=1600,fv=3,nu=5,tabv=Q_i)
aa3=v(f=1600,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=1600,fv=3,nu=5,tabv=S_i)
bb=v(f=1600,fv=3,nu=5.5,tabv=S_i)
cc=(v(d=7,f=300,fv=3,nu=4)+v(d=7,f=300,fv=3,nu=4,tabv=Tr_i))*.5
dd=(v(tabv=Tr_i,d=7)+v(d=7))*.5

AA = n.hstack((aa,aa2,aa3,aa4,bb,cc,dd))

W(AA, "vbr7.wav")

aa=v(f=1600, fv=3,nu=5,tabv=D_i)
aa2=v(f=1600,fv=3,nu=5,tabv=Q_i)
aa3=v(f=1600,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=1600,fv=3,nu=5,tabv=S_i)
bb=v(f=1600,fv=3,nu=5.5,tabv=S_i)
cc=v(d=7,f=300,fv=3,nu=4)
cc2=v(d=7,f=300,fv=3,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7)
dd2=v(d=7)

AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T

W(AA, "vbr8.wav")

aa=v(f=100, fv=3,nu=5,tabv=D_i)
aa2=v(f=100,fv=3,nu=5,tabv=Q_i)
aa3=v(f=100,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=100,fv=3,nu=5,tabv=S_i)
bb=v(f=100,fv=3,nu=5.5,tabv=S_i)
cc=v(d=7,f=300,fv=3,nu=14)
cc2=v(d=7,f=300,fv=3,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7)
dd2=v(tabv=D_i,d=7)

AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T

W(AA, "vbr9.wav")

aa=v(f=100, fv=20,nu=5,tabv=D_i)
aa2=v(f=100,fv=20,nu=5,tabv=Q_i)
aa3=v(f=100,fv=20,nu=5,tabv=Tr_i)
aa4=v(f=100,fv=20,nu=5,tabv=S_i)
bb=v(f=100,fv=20,nu=5.5,tabv=S_i)
cc=v(d=7,f=300, fv=20,nu=14)
cc2=v(d=7,f=300,fv=20,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7,fv=20.)
dd2=v(tabv=D_i,d=7,fv=20.)

AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T

W(AA, "vbr10.wav")

dd=v(tabv=Tr_i ,d=2,fv=20.)
dd2=v(tabv=D_i ,d=2,fv=20.)

dd3=v(tabv=Tr_i,d=2,fv=20.)
dd4=v(tabv=S_i ,d=2,fv=20.)

dd5=v(tabv=Q_i ,d=2,fv=20.)
dd6=v(tabv=S_i ,d=2,fv=20.)

dd7=v(tabv=Q_i ,d=2,fv=20.)
dd8=v(tabv=D_i ,d=2,fv=20.)

dd9=v(tabv=Tr_i,d=2,fv=20.)
dd10=v(tabv=D_i,d=2,fv=20.)

AA = V((H((dd,dd3,dd5,dd7,dd9)),H((dd2,dd4,dd6,dd8,dd10)))).T

W(AA, "vbr11.wav")

zz=V((H((dd,dd3,dd5,dd7,dd9)), H((dd2,dd4,dd6,dd8,dd10))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=7))*5)

AA = n.hstack(( (zz+aa1).T*.5, (zz+aa1).T*.5))

W(AA, "vbr12.wav")

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=7))* 4)
aa2=n.array(list(v(tabv=D_i,fv=.5,f=200,nu=7))* 4)
aa3=n.array(list(v(tabv=Tr_i,fv=.5,f=200,nu=7))*4)

AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

W(AA, "vbr13.wav")

dd=v(tabv=Tr_i ,d=2,fv=20.,nu=4)
dd2=v(tabv=D_i ,d=2,fv=20.,nu=4)

dd3=v(tabv=Tr_i,d=2,fv=20.,nu=4)
dd4=v(tabv=S_i ,d=2,fv=20.,nu=4)

dd5=v(tabv=Q_i ,d=2,fv=20.,nu=4)
dd6=v(tabv=S_i ,d=2,fv=20.,nu=4)

dd7=v(tabv=Q_i ,d=2,fv=20.,nu=4)
dd8=v(tabv=D_i ,d=2,fv=20.,nu=4)

dd9=v(tabv=Tr_i,d=2,fv=20.,nu=4)
dd10=v(tabv=D_i,d=2,fv=20.,nu=4)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=7))  *4)
aa2=n.array(list(v(tabv=D_i,fv=2,f=200,nu=7))   *4)
aa3=n.array(list(v(tabv=Tr_i,fv=.5,f=200,nu=19))*4)

AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

W(AA, "vbr14.wav")

dd=v(tabv=Tr_i ,d=2,fv=15.,nu=7)
dd2=v(tabv=D_i ,d=2,fv=15.,nu=7)

dd3=v(tabv=Tr_i,d=2,fv=15.,nu=7)
dd4=v(tabv=S_i ,d=2,fv=15.,nu=7)

dd5=v(tabv=Q_i ,d=2,fv=15.,nu=7)
dd6=v(tabv=S_i ,d=2,fv=15.,nu=7)

dd7=v(tabv=Q_i ,d=2,fv=15.,nu=7)
dd8=v(tabv=D_i ,d=2,fv=15.,nu=7)

dd9=v(tabv=Tr_i,d=2,fv=15.,nu=7)
dd10=v(tabv=D_i,d=2,fv=15.,nu=7)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=19))*4)
aa2=n.array(list(v(tabv=D_i,fv=2,f=800,nu=7))  *4)
aa3=n.array(v(tabv=Tr_i,fv=.25,f=200,nu=9.,d=8.))

AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

W(AA, "vbr15.wav")

dd=v(tabv=Tr_i ,d=2,fv=15.,nu=.7)
dd2=v(tabv=D_i ,d=2,fv=15.,nu=.7)

dd3=v(tabv=Tr_i,d=2,fv=15.,nu=.7)
dd4=v(tabv=S_i ,d=2,fv=15.,nu=.7)

dd5=v(tabv=Q_i ,d=2,fv=15.,nu=.7)
dd6=v(tabv=S_i ,d=2,fv=15.,nu=.7)

dd7=v(tabv=Q_i ,d=2,fv=15.,nu=.7)
dd8=v(tabv=D_i ,d=2,fv=15.,nu=.7)

dd9=v(tabv=Tr_i,d=2,fv=15.,nu=.7)
dd10=v(tabv=D_i,d=2,fv=15.,nu=.7)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=29))*4)
aa2=n.array(list(v(tabv=D_i,fv=2,f=800,nu=17))* 4)
aa3=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))

AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

W(AA, "vbr16.wav")


dd=v(tabv=Tr_i ,d=2,fv=35.,nu=.7)
dd2=v(tabv=D_i ,d=2,fv=35.,nu=.7)

dd3=v(tabv=Tr_i,d=2,fv=35.,nu=.7)
dd4=v(tabv=S_i ,d=2,fv=35.,nu=.7)

dd5=v(tabv=Q_i ,d=2,fv=35.,nu=.7)
dd6=v(tabv=S_i ,d=2,fv=35.,nu=.7)

dd7=v(tabv=Q_i ,d=2,fv=35.,nu=.7)
dd8=v(tabv=D_i ,d=2,fv=35.,nu=.7)

dd9=v(tabv=Tr_i,d=2,fv=35.,nu=.7)
dd10=v(tabv=D_i,d=2,fv=35.,nu=.7)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=9))*4)
aa2=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))
aa3=n.array(v(fv=.25/2.,f=200,nu=9,d=8.))

AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

W(AA, "vbr17.wav")

