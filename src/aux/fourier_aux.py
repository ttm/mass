# coding: utf-8
# abs: 0.889857529063, a1: -0.878235820903, b1: -0.143346659928, fas: 0.163221149167A
import pylab as p, numpy as n
f=n.fft.fft
n3=n.array([-0.66522536,  0.29577169,  0.13024923])

ff=f(n3)

a0=n.real(ff[0])
b0=n.imag(ff[0])

ab1=n.abs(ff[1])
a1=n.real(ff[1])
b1=n.imag(ff[1])
#fas=b1/a1
fas=n.arctan(a1/b1) # fas/2 = 0.70450095568094961
print("abs: %s, a1: %s, b1: %s, fas: %s" % (ab1,a1,b1,fas))

ii=n.linspace(-0.5*n.pi,1.5*n.pi,200)
iii=n.linspace(-0.5,2.5,200)
#s=(2/3.)*-ab1*n.cos(ii-fas+.5+.3+.05)+a0/3; p.plot(iii,s,"m--"); p.plot(n3,"bo");p.show()

s=(2/3.)*-ab1*n.cos(ii+fas/2)+a0/3; p.plot(iii,s,"m--"); p.plot(n3,"bo");
s=(2/3.)*-ab1*n.cos(ii+0.48677885598324417)+a0/3; p.plot(iii,s,"g--"); p.plot(n3,"bo");p.show()

#s=(2/3.)*-ab1*n.cos(ii+0.68677885598324417)+a0/3; p.plot(iii,s,"m--"); p.plot(n3,"bo");p.show()
#s=.67*-ab1*n.cos(ii-fas+.5+.3+.05)-.1+.02; p.plot(iii,s,"m--"); p.plot(n3,"bo");p.show()
#p.plot(iii,s,"m--")
#p.plot(n3,"bo")
