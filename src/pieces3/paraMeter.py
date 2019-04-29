#-*- coding: utf-8 -*-
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

# peça dedicada e expor as diferentes transições
# de intensidade e altura

# partes
# 1) Transições de altura log e lin e com alpha
# 2) Transições de intensidade log e in e com alpha
# 3) Usos combinados de ambos

############################################
# PARTE 1)

# 1a: comparando variação linear e logarítmica
#class 
"""parametros pré-estabelecidos para maior coerência da exploração"""

f=[50.,100.,150.,200.,250.,300.,350.,400.,450.,500.,550.,  600.]
#  01  11    25  31    43  55    67   71   82   83   94#   105
d=[0.1,0.2,0.3,0.5,1.0,1.5,2.0,3.0,5.0,7.0,10.0]
#  0    1   2   3   4   5   6   7   8  9    10
a=[0.01,0.1,1.0,10.,100.]
#   0    1   2   3    4


#intro (8 segundos)
intr=n.hstack((T(f[9],f[0],d[7]),T(f[0],f[10],d[8],'lin',Tr_i)))

#entrada (8 segundos)
entr=  n.hstack(( T(f[10],f[10],d[8],'lin',Tr_i),n.zeros(f_a*d[7])))+ \
           n.hstack(( T(f[3],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),
     T(f[2],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),
     T(f[3],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),T(f[1],f[0],d[3]),
     T(f[5],f[0],d[3]),
     T(f[3],f[0],d[3]),T(f[2],f[0],d[3]),T(f[1],f[0],d[3],'lin') ))

#desenvolvimento da entrada (8 segundos)
devEntr=n.hstack(( T(f[0],f[0],d[8]),T(f[0],f[0],d[4]),
     T(f[0],f[0],d[3],'lin',Tr_i),
     T(f[0],f[0],d[3],'lin',Tr_i),T(f[0],f[0],d[3],'lin',Q_i),\
     T(f[0],f[0],d[3],'lin',Tr_i) )) + n.hstack(( T(f[5],f[2],d[3]),
     T(f[5],f[8],d[3]),T(f[5],f[2],d[3]),T(f[8],f[5],d[3]),
     T(f[5],f[2],d[3]),
     T(f[5],f[1],d[3]),T(f[5],f[0],d[3]),T(f[1],f[2],d[3]),
     T(f[5],f[2],d[3]),
     T(f[10],f[2],d[3]),T(f[10],f[0],d[3]),T(f[10],f[9],d[3]),
     T(f[5],f[2],d[3]),
     T(f[7],f[5],d[3]),T(f[7],f[2],d[3]),T(f[0],f[2],d[3]) ))

#sublimada 1 / passagem para outros funcionamentos e estereofonia 8s
sub_e=n.hstack(( T(f[1],f[0],d[3],'log',Q_i),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
      T(f[1],f[0],d[3],'log',Q_i),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
      T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]) )) + \
                 n.hstack(( T(f[0],f[10],d[9])+\
                 T(f[0],f[10],d[9],'lin',Tr_i),n.zeros(f_a*d[4]) ))

sub_d=n.hstack(( T(f[1],f[0],d[3],'log',Q_i),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
      T(f[1],f[0],d[3],'log',Q_i),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]),
      T(f[1],f[0],d[3]),
     T(f[1],f[0],d[3]),T(f[1],f[0],d[3],'lin'),T(f[1],f[0],d[3]) )) + \
      n.hstack(( T(f[0],f[10],d[9],'log',Tr_i)+\
      T(f[0],f[10],d[9],'lin'),n.zeros(f_a*d[4]) ))

# dev da sublimada +8s
sub2_e=n.hstack(( T(f[10],f[9],d[3]),
     T(f[10],f[7],d[3]),T(f[10],f[9],d[3]),T(f[10],f[6],d[3]),
     T(f[10],f[9],d[3]),
     T(f[10],f[7],d[3]),T(f[10],f[9],d[3]),T(f[10],f[6],d[3]), )) + \
n.hstack(( T(f[10],f[8],d[3],tab=Tr_i),
     T(f[10],f[5],d[3],tab=Tr_i),T(f[10],f[4],d[3],tab=Tr_i),
         T(f[10],f[6],d[3],tab=Tr_i),
     T(f[10],f[10],d[3],tab=Tr_i),
     T(f[10],f[5],d[3],tab=Tr_i),T(f[10],f[0],d[3],tab=Tr_i),
         T(f[10],f[1],d[3],tab=Tr_i)  ))

sub2_d=n.hstack(( T(f[10],f[9],d[3],tab=Tr_i),
     T(f[10],f[7],d[3],tab=Tr_i),T(f[10],f[9],d[3],tab=Tr_i),
        T(f[10],f[6],d[3],tab=Tr_i),
     T(f[10],f[9],d[3],tab=Tr_i),
     T(f[10],f[7],d[3],tab=Tr_i),T(f[10],f[9],d[3],tab=Tr_i),
     T(f[10],f[6],d[3],tab=Tr_i) )) + n.hstack(( T(f[10],f[8],d[3]),
     T(f[10],f[5],d[3]),T(f[10],f[4],d[3]),T(f[10],f[6],d[3]),
     T(f[10],f[10],d[3]),
     T(f[10],f[5],d[3]),T(f[10],f[0],d[3]),T(f[10],f[1],d[3]) ))

# rarefação e repetições preparando para término
rar_e=n.hstack(( T(f[7],f[9],d[3]),
     n.zeros(d[3]), T(f[10],f[9],d[3]),T(f[0],f[9],d[3]),
     n.zeros(d[3]),T(f[0],f[9],d[5]),
     n.zeros(d[6]),
     T(f[1],f[9],d[6],'lin')    ))

rar_d=n.hstack(( T(f[7],f[9],d[3],'lin'),
     n.zeros(d[3]), n.zeros(d[3]),T(f[1],f[9],d[3]),
     T(f[0],f[10],d[4],'lin',Tr_i),
     T(f[9],f[9],d[4]),
     T(f[1],f[9],d[6],'log')    ))

# finalização com elementos dos outros momentos
intr=n.hstack((T(f[9],f[0],d[7]),T(f[0],f[10],d[8],'lin',Tr_i)))

def Z(sonic_vector):
    s1 = fun.F(d=0.05)
    s2 = fun.F(d=0.05, out=False)
    e = n.hstack(( s1, n.zeros(len(sonic_vector)-len(s1)-len(s2)), s2 ))
    return sonic_vector*e

fin_e=n.copy(intr)
fin_d=n.copy(intr)
fin_e[d[4]*f_a:d[5]*f_a] = Z(fin_e[d[4]*f_a:d[5]*f_a])
fin_d[d[5]*f_a:d[6]*f_a] = Z(fin_d[d[5]*f_a:d[6]*f_a])

fin_e[7*f_a:7.5*f_a]    = Z(fin_e[7*f_a:7.5*f_a]    )
fin_d[7.25*f_a:7.75*f_a]= Z(fin_d[7.25*f_a:7.75*f_a])

_e=n.hstack((   intr,entr,devEntr,sub_e,sub2_e,rar_e,fin_e   ))
_d=n.hstack((   intr,entr,devEntr,sub_d,sub2_d,rar_d,fin_d,n.zeros(2)   ))
s=n.vstack((_e,_d)).T

W(s, 'trans1.wav')


# Exploracao sistemática dos tremolos:
#first=n.array(())
#for d in d[:5]:
#  prinT(d)
#  for f in f:
#    for f2 in f:
#      first=n.hstack((first,
#        trans(f,f2,d),
#        trans(f,f2,d,'lin'),
#        trans(f,f2,d,tab=Tr_i),
#        trans(f,f2,d,'lin',tab=Tr_i),
#        trans(f,f2,d,tab=D_i),
#        trans(f,f2,d,'lin',tab=D_i),
#        (trans(f,f2,d)+trans(f,f2,d,'lin'))*.5,
#        (trans(f,f2,d,tab=Tr_i)+trans(f,f2,d,'lin',tab=Tr_i))*.5,
#        (trans(f,f2,d,tab=Q_i)+trans(f,f2,d,'lin',tab=Q_i))*0.5  ))
