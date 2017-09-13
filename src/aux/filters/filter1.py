#-*- coding: utf8 -*-
# fazendo umi
# perfil quadrado do espectro
# e retornando o as amostras

import numpy as n, pylab as p, scikits.audiolab as a

duracao=2. # segundo
N=int(duracao*44100) #numero de amostras
# sequência de 2205 amostras (50 milisegundos em 44100 kHz)
# coeficientes espectrais de fourier em mesmo numero
# som é real, espectro par:
#perfil_espectral=[0.]*(N/4)+[0.]*(N/8)+[1.]*(N/4)+[0.]*(N/8)+[0.]*(N/4)# eh par



#perfil_espectral=[0.]*(N/4)*3  +[1.]*(N/4)*2   +[0.]*(N/4)*3# eh par

#fase_impar=n.zeros((N*8)/4)

#espectro=perfil_espectral+fase_impar*

perfil_espectral=([0]+[0]*30+[1]*30+[0]*30)


#perfil_espectral=[0.]*(N/4)+[0.]*(N/4)+[1.]*(N/4)+[0.]*(N/4)+[0.]*(N/4)# eh par
#perfil_espectral=[0.]*(N/3)+[1.]*(N/3)+[0.]*(N/3)# eh par
#perfil_espectral=[0.]*(N/5)+[0.]*(N/5)+[1.]*(N/5)+[0.]*(N/5)+[0.]*(N/5)# eh par
#perfil_espectral=[1.]*1000+[0.]*1000+[0.]*1000 # nao eh par

som=n.fft.ifft(perfil_espectral)

p.subplot(411)
p.plot(som.real)
p.plot(som.real,"ro")

p.subplot(412)
p.plot(som.imag)
p.plot(som.imag,"ro")

p.subplot(413)
p.plot(n.abs(som))
p.plot(n.abs(som),"ro")

p.subplot(414)
p.plot(perfil_espectral)


p.show()
