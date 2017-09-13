#-*- coding: utf8 -*-
import numpy as n, pylab as p

impulso=[1.]

fc=.05
x=n.e**(-2*n.pi*fc) # fc=> freq de corte em 3dB

###### passa baixas
p.subplot(221)
# cálculo dos coefs
a0=1-x
b1=x

# aplicação da equação a diferenças
sinal=[impulso[0]*a0]
for i in xrange(1000):
    sinal.append(sinal[-1]*b1)
# cálculo do espectro
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2])
#p.plot([fc*len(m),fc*len(m)],[-1000,1000])
p.text(100,.9,r"$f_c=0.05$")
p.ylim(0,1)
pb=sinal[:]


##### passa altas
p.subplot(222)
# cálculo dos coefs
a0=(1+x)/2
a1=-(1+x)/2
b1=x
sinal=[impulso[0]*a0]
sinal+=[impulso[0]*a1+sinal[-1]*b1]
# aplicação da equação a diferenças
for i in xrange(1000):
    sinal.append(sinal[-1]*b1)
# cálculo do espectro
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2])
p.plot([fc*len(m),fc*len(m)],[-1000,1000])
p.ylim(0,1)
pa=sinal[:]



###### nó
p.subplot(223)
f=0.2
bw=0.02

r=1-3*bw
k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))

# coefs rejeita banda
a0=k
a1=-2*k*n.cos(2*n.pi*f)
a2=k
b1=2*r*n.cos(2*n.pi*f)
b2=-r**2

sinal=[impulso[0]*a0]
sinal+=[impulso[0]*a1+sinal[-1]*b1]
sinal+=[impulso[0]*a2+sinal[-1]*b1+sinal[-2]*b2]
for i in xrange(1000):
    sinal.append(sinal[-1]*b1+sinal[-2]*b2)
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2], label=r"$f=0.2$ e $bw=0.02$")


# segunda largura de banda
bw=0.002 
r=1-3*bw
k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))

# coefs rejeita banda
a0=k
a1=-2*k*n.cos(2*n.pi*f)
a2=k
b1=2*r*n.cos(2*n.pi*f)
b2=-r**2

sinal=[impulso[0]*a0]
sinal+=[impulso[0]*a1+sinal[-1]*b1]
sinal+=[impulso[0]*a2+sinal[-1]*b1+sinal[-2]*b2]
for i in xrange(1000):
    sinal.append(sinal[-1]*b1+sinal[-2]*b2)
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2], label=r"$f=0.2$ e $bw=0.002$")

# passa banda
f=0.1
bw=0.006

r=1-3*bw
k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))

# coefs rejeita banda
a0=1-k
a1=-2*(k-r)*n.cos(2*n.pi*f)
a2=r**2 -k
b1=2*r*n.cos(2*n.pi*f)
b2=-r**2

sinal=[impulso[0]*a0]
sinal+=[impulso[0]*a1+sinal[-1]*b1]
sinal+=[impulso[0]*a2+sinal[-1]*b1+sinal[-2]*b2]
for i in xrange(1000):
    sinal.append(sinal[-1]*b1+sinal[-2]*b2)
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2],label=r"$f=0.1$ e $br=0.006$")


# segunda largura de banda
bw=0.0009

r=1-3*bw
k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))

# coefs rejeita banda
a0=1-k
a1=-2*(k-r)*n.cos(2*n.pi*f)
a2=r**2 -k
b1=2*r*n.cos(2*n.pi*f)
b2=-r**2

sinal=[impulso[0]*a0]
sinal+=[impulso[0]*a1+sinal[-1]*b1]
sinal+=[impulso[0]*a2+sinal[-1]*b1+sinal[-2]*b2]
for i in xrange(1000):
    sinal.append(sinal[-1]*b1+sinal[-2]*b2)
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m[:len(m)/2], label=r"$f=0.2$ e $bw=0.0009$")


p.legend(loc="upper right")


#p.plot([fc*len(m),fc*len(m)],[-1000,1000])
p.ylim(0,1)
rb=sinal[:]
p.show()
