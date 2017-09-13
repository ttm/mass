#-*- coding: utf8 -*-

###########################
# Este arquivo procura entender
# a distribuicao de energia
# na reconstrucao de fourier com
# os coeficientes organizados
# 1 1 1 1 1 
# 1 0 1 0 1 0 1 ...
# 1 0 0 1 0 0 1 0 0 1
# 1 0 0 0 1 0 0 0 1 0 0 0 1
# etc...
# rodar normalmente e resulta em figuras e objetos
# para inspecao

import numpy as n, pylab as p
ones=n.ones
ifft=n.fft.ifft

N=100 # numero de amostras
# (N/2)%3 == 2
# (N/2)%2 == 0
# N = 40, 100, etc (faz um for i in xrange e acha os iis)
e=ones(N)
#e[0]=0
s1=ifft(e)

ii=n.arange(0,N/2,2)+1
ee=e[:]
ee[ii]=0
ee[ii+N/2]=0
s2=ifft(ee)

e=ones(N/2+2)
#e[0]=0
ee=e[:]
ii=n.arange(0,N/2,3)
ee[ii+1]=0
ee[ii+2]=0
ee=n.hstack((ee[:-1],ee[1:-2][::-1]))
s3=ifft(ee)

e=ones(N/2+3)
#e[0]=0
ee=e[:]
ii=n.arange(0,N/2,4)
ee[ii+1]=0
ee[ii+2]=0
ee[ii+3]=0
ee=n.hstack((ee[:-2],ee[1:-3][::-1]))
s4=ifft(ee)

e=ones(N/2+4)
#e[0]=0
ee=e[:]
ii=n.arange(0,N/2,5)
ee[ii+1]=0
ee[ii+2]=0
ee[ii+3]=0
ee[ii+4]=0
ee=n.hstack((ee[:-3],ee[1:-4][::-1]))
s5=ifft(ee)


p.subplot(511)
p.plot(s1,"ro")
p.subplot(512)
p.plot(s2,"bo")
p.subplot(513)
p.plot(s3,"go")
p.subplot(514)
p.plot(s4,"yo")
p.subplot(515)
p.plot(s5,"co")
p.show()






