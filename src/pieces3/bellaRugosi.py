# coding: utf-8 
import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

WS = fun.W
H=n.hstack
V=n.vstack

# Tamanho da LUT > 2**10 para usar também em oscilacoes
# de comprimento de onda grandes (LFO)
Lambda_tilde=Lt=(2**5)*(2**10)
# Senoide
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras

# Quadrada:
Q_i=n.hstack(  ( n.ones(Lt//2)*-1 , n.ones(Lt//2) )  )

# Triangular:
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

def v(fv=2, nu=2, tab=S_i, tabv=S_i, d=2,f=200):
    return fun.V(f=200, tabv=tabv, fv=fv, d=d, nu=nu)

# Dente de Serra:
D_i=n.linspace(-1,1,Lt)

dd=v(tabv=Tr_i ,d=2,fv=35.,nu=7.0)
dd2=v(tabv=D_i ,d=2,fv=35.,nu=7.0)

dd3=v(tabv=Tr_i,d=2,fv=35.,nu=7.0)
dd4=v(tabv=S_i ,d=2,fv=35.,nu=7.0)

dd5=v(tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd6=v(tabv=S_i ,d=2,fv=35.,nu=7.0)

dd7=v(tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd8=v(tabv=D_i ,d=2,fv=35.,nu=7.0)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))

aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=9))*4)
aa2=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))
aa3=n.array(v(fv=.25/2.,f=200,nu=9,d=8.))

aa=n.vstack(( (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

dd= v(tab=Tr_i,tabv=Tr_i ,d=2,fv=35.,nu=7.0)
dd2=v(tab=Tr_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

dd3=v(tab=Tr_i,tabv=Tr_i,d=2,fv=35.,nu=7.0)
dd4=v(tab=Tr_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd5=v(tab=Tr_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd6=v(tab=Tr_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd7=v(tab=Tr_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd8=v(tab=Tr_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=9))*4)
aa2=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))
aa3=n.array(v(fv=.25/2.,f=200,nu=9,d=8.))

aa=n.vstack(( aa, (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

dd= v(tab=Q_i,tabv=Tr_i ,d=2,fv=35.,nu=7.0)
dd2=v(tab=Q_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

dd3=v(tab=Q_i,tabv=Tr_i,d=2,fv=35.,nu=7.0)
dd4=v(tab=Q_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd5=v(tab=Q_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd6=v(tab=Q_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd7=v(tab=Q_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd8=v(tab=Q_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=9))*4)
aa2=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))
aa3=n.array(v(fv=.25/2.,f=200,nu=9,d=8.))

aa=n.vstack(( aa, (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

dd= v(tab=D_i,tabv=Tr_i ,d=2,fv=35.,nu=7.0)
dd2=v(tab=D_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

dd3=v(tab=D_i,tabv=Tr_i,d=2,fv=35.,nu=7.0)
dd4=v(tab=D_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd5=v(tab=D_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd6=v(tab=D_i,tabv=S_i ,d=2,fv=35.,nu=7.0)

dd7=v(tab=D_i,tabv=Q_i ,d=2,fv=35.,nu=7.0)
dd8=v(tab=D_i,tabv=D_i ,d=2,fv=35.,nu=7.0)

zz=V((H((dd,dd3,dd5,dd7)), H((dd2,dd4,dd6,dd8))))
aa1=n.array(list(v(tabv=Q_i,fv=.5,f=200,nu=9))*4)
aa2=n.array(v(tabv=Tr_i,fv=.25/2.,f=200,nu=9,d=8.))
aa3=n.array(v(fv=.25/2.,f=200,nu=9,d=8.))

aa=n.vstack(( aa, (zz+aa1).T*.5, (zz+aa2).T*.5,(zz+aa3).T*.5))

WS(aa, "BellaRugosiSdadE.wav")
print("BellaRugosiSdadE.wav written")
