# coding: utf-8
import pylab as p, numpy as n

# plotando polinomios
a=n.linspace(0,1,5000)
p.xlim(-0.1,1.1)
p.ylim(-.1,1.1)
for i in xrange(100):
    b=a**(i/25.)
    p.plot(a,a**i)


p.show()

# diferenca estre termos polinomiais
n=1 # reta
mm=1000 # comparando ateh termos de 100 grau
cruzamentos=[]
for m in xrange(n+1,mm):
    foo=(n/float(n+m))**(1/float(m))
    cruzamentos.append(foo)

# cruzamentos eh estritramente crescente e limitado em 1, converge
