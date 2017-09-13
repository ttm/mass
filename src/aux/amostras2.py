#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n
f=n.fft.fft
fi=n.fft.ifft
a=[-1,1]
#-1 * cos(n.pi*l)
p.plot([0,1],a,"bo")
ii=n.linspace(-0.5*n.pi,1.5*n.pi,200)
iii=n.linspace(-0.5,1.5,200)
s=-n.cos(ii)
p.plot(iii,s,"m--")

p.xlim(-1.2,2)
#p.xlim(0,T2*.56)
p.ylim(-1.1,1.1)

p.ylabel(r"amplitude $\rightarrow$")
p.xlabel(r"time $\rightarrow$")
p.show()




d=[-.6,-.2,.2,.6]
t=[-1,0,1,0]
q=[-1,-1,1,1]

da1=n.pi

da2=n.pi/2

das=n.linspace(-n.pi/2,-5*n.pi/2,4,endpoint=False)
s1=n.sin(das)
s2=n.array(a*2)

#p.plot(s1)
#p.plot(s2)
#p.plot(s1+s2)
#p.plot(d)
#p.show()

