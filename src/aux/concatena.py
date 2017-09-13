#-*- coding: utf-8 -*-
import numpy as n, pylab as p

c=2

# dois períodos de uma dente de serra:
d=n.linspace(-1,1,50)
d=n.hstack((d,d))
d=n.hstack((d,d))
d=d[:len(d)/c]

# quatro periodos de uma onda quadrada
q=n.hstack((  n.ones(13)*-1,n.ones(12)  ))
q=n.hstack((q,q))
q=n.hstack((q,q))
q=n.hstack((q,q))
q=q[:len(q)/c]

# senoide ou ruido
s=n.linspace(0,10*2*n.pi,200,endpoint=False)
s=n.sin(s)[:len(s)/c]
e=5.0
ee=4
#p.plot(n.hstack((d,q,s)),'o')
p.figure(figsize=(10.,5.))
p.xticks((),())
p.yticks((),())
p.subplots_adjust(left=0.05,bottom=0.08,right=0.97,top=0.97)
p.plot(d,'o',ms=3)
p.plot(range(len(d),len(d)+len(q)),q,'o', ms=3)
p.plot(range(len(d)+len(q),len(d)+len(q)+len(s)),s,'o', ms=3)
p.plot(n.hstack((d,q,s)))
p.xlabel(r"time $\rightarrow$",fontsize=22)
p.ylabel(r"amplitude $\rightarrow$",fontsize=22)
p.ylim(-1.1,1.1)
p.xlim(-5,305)
p.savefig("../figures/concatenacao__.png")
p.show()
