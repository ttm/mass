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
p.figure(figsize=(10.,5.))
p.xticks((),())
p.yticks((),())
p.subplots_adjust(left=0.05,bottom=0.08,right=0.97,top=0.97)
p.plot(s+ee+3*e,'o')
p.plot(q+ee+1.93*e,'o')
p.plot(d+ee+e*.8,'o')
p.plot(s+q+d,'o')

p.ylim(-3.5,21)
p.xlim(-5,105)

p.text(47,11.4+e-.75,"+",fontsize=48)
p.text(47,11.4-1.65,"+",fontsize=48)
p.text(45.5,11.4-e-3,"=",fontsize=68)

p.xlabel(r"time $\rightarrow$",fontsize=22)
p.ylabel(r"amplitude $\rightarrow$",fontsize=22)

p.savefig("../figures/mixagem__.png")
p.show()
