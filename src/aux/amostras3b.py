#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n
f=n.fft.fft

#n3=n.random.rand(3)*2-1
n3=n.array([-0.20356754,  0.91942605,  0.44866268])
#n3=n.array([-0.40+.3,  0.+.3,  0.4+.3])
#n3=n.array([-0.40+.3,  0.4+.3,  0.4+.3])
#n3=n.array([-0.40+.3, - 0.4+.3,  0.4+.3])
#n3=n.array([+0.40+.3, - 0+.3, - 0.4+.3])
#n3=n.array([-0.40+.3, + 0.4+.3, - 0.4+.3])
p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.18,bottom=0.15,right=0.97,top=0.94)
p.plot(n3,"bo")

ff=f(n3)
a0=n.real(ff[0]) 
b0=n.imag(ff[0]) # sempre zero

ab1=n.abs(ff[1])
a1=n.real(ff[1])
b1=n.imag(ff[1])
fas=n.arctan(b1/a1) # fase
if a1<0: fas+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a1: %s, b1: %s, fas: %s" % (ab1,a1,b1,fas))

fr1=(2*n.pi/3)/2 #ciclo em 3 * \delta_a, metade disso
fr2=1/2. # metade de \delta_a
ii=n.linspace(0-fr1,2*n.pi-fr1,200) # [0,2*pi] ciclo completo
iii=n.linspace(0-fr2,3-fr2,200) # [0,3] == 3 \delta_a, período

s=(2/3.)*ab1*n.cos(ii+fas)+a0/3
p.plot(iii,s,"m--")

p.plot((-10,10),(a0/3,)*2,"k--")
p.plot((-10,10),(a0/3-2*ab1/3,)*2,"k--")
p.plot((-10,10),(a0/3+2*ab1/3,)*2,"k--")
p.xticks((-1,0,1,2,3),(r"$-\delta_a$",r"$0$",r"$\delta_a$",r"$2\delta_a$",r"$3\delta_a$"),
        size=20)
p.yticks((a0/3-2*ab1/3,a0/3,a0/3+2*ab1/3),
        (r'$\frac{a_0-2|c_1|}{3}$',r'$\frac{a_0}{3}$',r'$\frac{a_0+2|c_1|}{3}$'),
        color = 'k', size = 33)

p.xlim(-1.2,3.2)
p.ylim(-1.1+.5,1.1)

p.ylabel(r"amplitude $\rightarrow$", fontsize=19)
p.xlabel(r"time $\rightarrow$", fontsize=19)
p.savefig("../figures/amostras3b_.png")
p.show()
