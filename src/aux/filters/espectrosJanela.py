#-*- coding: utf8 -*-
import numpy as n, pylab as p

N=60000 # N par

coeffs=n.random.random((N,2))-1

# Fazer complexos com os primeiros N elementos
# depois normalizar para norma ==1

j=n.complex(0,1)

coeffs=coeffs[:,0]+coeffs[:,1]*j
coeffs=coeffs/n.abs(coeffs)

# real par, imaginaria impar
coeffs[N/2+1:]=n.real(coeffs[1:N/2])[::-1] - j*n.imag(coeffs[1:N/2])[::-1]

coeffs[0]=0.
coeffs[N/2]=0.9

noise=n.fft.ifft(coeffs)

p.plot(n.real(noise))
p.show()

