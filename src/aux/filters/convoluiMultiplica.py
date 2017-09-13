#-*- coding: utf8 -*-
import numpy as n, pylab as p
ifft=n.fft.ifft
fft=n.fft.fft
convolve=n.convolve
plot=p.plot
show=p.show

espectro1 = [0]*20+[1]*25+[0]*19
espectro2=[1]*25+[0]*15+[1]*24

som1=ifft(espectro1).real
som2=ifft(espectro2).real

resulta=convolve(som1,som2)

espectro=fft(resulta)

xx=n.linspace(0,len(espectro),len(espectro1))
plot(xx,espectro1)
plot(xx,espectro2)
plot(n.abs(espectro))
show()
