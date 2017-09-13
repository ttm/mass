#-*- coding: utf8 -*-
import numpy as n, pylab as p


# variaveis de parametrizacao
fa=44100.
f=200

# tipos: LPF, HPF, BPF, BPF2, notch
# APF, peakingEQ, lowShelf, highShelf
tipo='LPF' 

dBgain=20. # para frequência central

Q=0
BW=100.
S=1.



# variaveis intermediarias
A = 10**(dBgain/40.)
w0=2*n.pi*f/fa
cw0=n.cos(w0)
sw0=n.sin(w0)
if Q:
    alpha = sw0/(2*Q)
elif BW:
    alpha = sw0*n.sinh((n.log(2)/2)*BW*w0/sw0)
elif S:
    alpha = (sw0/2) * n.sqrt( (A+1/A)*(1/S - 1) + 2  )
else:
    print("no quality, bandwidth or slope specified.")

if tipo=='LPF':
    b=[(1-cw0)/2, 1-cw0, (1-cw0)/2]
    a=[1+alpha, -2*cw0, 1-alpha]
elif tipo=='HPF':
    b=[(1+cw0)/2,-(1+cw0),(1+cw0)/2]
    a=[1+alpha,-2*cw0,1-alpha]
elif tipo=='BPF':
    b=[alpha,0,-alpha]
    a=[1+alpha,-2*cw0,1-alpha]
elif tipo=='BPF2':
    b=[alpha,0,-alpha]
    a=[1+alpha,-2*cw0, 1-alpha]
elif tipo=='notch':
    b=[1,-2*cw0,1]
    a=[1+alpha, -2*cw0, 1-alpha]
elif tipo=='APF':
    b=[1-alpha,-2*cw0,1+alpha]
    a=[1+alpha, -2*cw0, 1-alpha]
elif tipo=='peakingEQ':
    b=[1+alpha*A, -2*cw0, 1-alpha*A]
    a=[1+alpha/A, -2*cw0, 1-alpha/A]
elif tipo=='lowShelf':
    b=[A*(  A+1 - (A-1)*cw0+2*n.sqrt(A)*alpha  ),
       2*A*(  A-1 - (A+1)*cw0  ),
       A*(  A+1 - (A-1)*cw0 - 2*n.sqrt(A)*alpha)]
    a=[A+1+(A-1)*cw0+2*n.sqrt(A)*alpha,
       -2*(  A-1 + (A+1)*cw0  ),
       A+1 + (A-1)*cw0 - 2*n.sqrt(A)*alpha]
elif tipo=='highShelf':
    b=[A*(  A+1 + (A-1)*cw0+2*n.sqrt(A)*alpha  ),
       -2*A*(  A-1 + (A+1)*cw0  ),
       A*(  A+1 + (A-1)*cw0 - 2*n.sqrt(A)*alpha)]
    a=[A+1-(A-1)*cw0+2*n.sqrt(A)*alpha,
       2*(  A-1 - (A+1)*cw0  ),
       A+1 - (A-1)*cw0 - 2*n.sqrt(A)*alpha]
   

# Impulse response by hand
# :::
sinal=[b[0]]
sinal+=[b[1]-sinal[-1]*a[1]]
sinal+=[b[2]-sinal[-1]*a[1]-sinal[-2]*a[2]]
for i in xrange(44100): # for 1 second
    sinal.append(-sinal[-1]*a[1]-sinal[-2]*a[2])
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m)
p.show()
