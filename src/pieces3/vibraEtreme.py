#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

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
# PARTE 1)

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
    Lv=float(len(S_i))

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

aa=v()
bb=v(nu=4.)
cc=v(f=300)
dd=v()

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr.wav",f_a,AA)

aa=v(f=800)
bb=v(nu=7.)
cc=v(f=300,fv=3)
dd=v()

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr2.wav",f_a,AA)

aa=v(f=600,fv=6)
bb=v(nu=7.,fv=12)
cc=v(f=300,fv=3,nu=24)
dd=v()

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr3.wav",f_a,AA)

aa=v(f=1600,fv=36)
bb=v(nu=36.,fv=12)
cc=v(f=300,fv=3,nu=24,tabv=D_i)
dd=v(tabv=D_i)

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr4.wav",f_a,AA)

aa=v(f=1600,fv=36,tabv=D_i)
bb=v(nu=2*36.,fv=12)
cc=v(f=300,fv=3,nu=24,tabv=Q_i)
dd=v(tabv=Q_i)

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr5.wav",f_a,AA)

aa=v(f=1600,fv=36,tabv=D_i)
aa2=v(f=1600,fv=36,tabv=Q_i)
aa3=v(f=1600,fv=36,tabv=Tr_i)
aa4=v(f=1600,fv=36,tabv=S_i)
bb=v(nu=2*36.,fv=12,tabv=Tr_i)
cc=v(f=300,fv=3,nu=24,tabv=Tr_i)
dd=v(tabv=Tr_i)

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,aa2,aa3,aa4,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr6.wav",f_a,AA)

aa=v(f=1600, fv=3,nu=5,tabv=D_i)
aa2=v(f=1600,fv=3,nu=5,tabv=Q_i)
aa3=v(f=1600,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=1600,fv=3,nu=5,tabv=S_i)
bb=v(f=1600,fv=3,nu=5.5,tabv=S_i)
cc=(v(d=7,f=300,fv=3,nu=4)+v(d=7,f=300,fv=3,nu=4,tabv=Tr_i))*.5
dd=(v(tabv=Tr_i,d=7)+v(d=7))*.5

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack((aa,aa2,aa3,aa4,bb,cc,dd))
AA = n.int16(AA * float(2**15))

w.write("vbr7.wav",f_a,AA)

aa=v(f=1600, fv=3,nu=5,tabv=D_i)
aa2=v(f=1600,fv=3,nu=5,tabv=Q_i)
aa3=v(f=1600,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=1600,fv=3,nu=5,tabv=S_i)
bb=v(f=1600,fv=3,nu=5.5,tabv=S_i)
cc=v(d=7,f=300,fv=3,nu=4)
cc2=v(d=7,f=300,fv=3,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7)
dd2=v(d=7)

# most music players read only 16-bit wav files, so let's convert the array
AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T
AA = n.int16(AA * float(2**15))

w.write("vbr8.wav",f_a,AA)

aa=v(f=100, fv=3,nu=5,tabv=D_i)
aa2=v(f=100,fv=3,nu=5,tabv=Q_i)
aa3=v(f=100,fv=3,nu=5,tabv=Tr_i)
aa4=v(f=100,fv=3,nu=5,tabv=S_i)
bb=v(f=100,fv=3,nu=5.5,tabv=S_i)
cc=v(d=7,f=300,fv=3,nu=14)
cc2=v(d=7,f=300,fv=3,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7)
dd2=v(tabv=D_i,d=7)

# most music players read only 16-bit wav files, so let's convert the array
AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T
AA = n.int16(AA * float(2**15))

w.write("vbr9.wav",f_a,AA)

aa=v(f=100, fv=20,nu=5,tabv=D_i)
aa2=v(f=100,fv=20,nu=5,tabv=Q_i)
aa3=v(f=100,fv=20,nu=5,tabv=Tr_i)
aa4=v(f=100,fv=20,nu=5,tabv=S_i)
bb=v(f=100,fv=20,nu=5.5,tabv=S_i)
cc=v(d=7,f=300, fv=20,nu=14)
cc2=v(d=7,f=300,fv=20,nu=4,tabv=Tr_i)
dd=v(tabv=Tr_i,d=7,fv=20.)
dd2=v(tabv=D_i,d=7,fv=20.)

# most music players read only 16-bit wav files, so let's convert the array
AA = V((H((aa2,aa4,bb,cc2,dd2)), H((aa,aa3,bb,cc,dd)))).T
AA = n.int16(AA * float(2**15))

w.write("vbr10.wav",f_a,AA)

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

# most music players read only 16-bit wav files, so let's convert the array
AA = V((H((dd,dd3,dd5,dd7,dd9)),H((dd2,dd4,dd6,dd8,dd10)))).T
AA = n.int16(AA * float(2**15))

w.write("vbr11.wav",f_a,AA)

zz=V((H((dd,dd3,dd5,dd7,dd9)), H((dd2,dd4,dd6,dd8,dd10))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=7))*5)

# most music players read only 16-bit wav files, so let's convert the array
AA = n.hstack(( (zz+aa1).T*.5, (zz+aa1).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr12.wav",f_a,AA)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=7))* 4)
aa2=n.array(list(v(tabv=D_i,fv=.5,f=200,nu=7))* 4)
aa3=n.array(list(v(tabv=Tr_i,fv=.5,f=200,nu=7))*4)

# most music players read only 16-bit wav files, so let's convert the array
AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr13.wav",f_a,AA)

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

# most music players read only 16-bit wav files, so let's convert the array
AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr14.wav",f_a,AA)

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

# most music players read only 16-bit wav files, so let's convert the array
AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr15.wav",f_a,AA)

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

# most music players read only 16-bit wav files, so let's convert the array
AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr16.wav",f_a,AA)


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

# most music players read only 16-bit wav files, so let's convert the array
AA = n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))
AA = n.int16(AA * float(2**15))

w.write("vbr17.wav",f_a,AA)

