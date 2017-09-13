#-*- coding: utf8 -*-
import numpy as n, pylab as p

# tres metodos de obter a resposta ao impulso
# dos filtros:
# 1) fazendo varios ruidos brancos
# filtrando, fazendo a transformada e somando
# os modulos
# 2) observando a resposta ao impulso
# e o modulo do sinal resultante
# 3) fazer senoides passarem pelo filtro
# e medir a diferenca de intensidade entre as que entraram e saíram

## Passa baixas simples
fc= .1 # frequencia de corte do filtro

x=n.e**(2*n.pi*fc)


#ruido=n.random.random(44100*1000)*2-1
#ruido=n.random.uniform(-1,1,44100*100)


#ruido=n.random.normal(0,1,44100*100)
ruido=n.random.uniform(-1,1,441)
F=n.abs(n.fft.fft(ruido,110+1))
for i in xrange(1000000+1):
    #ruido=n.random.normal(0,1,44100*100)
    ruido=n.random.uniform(-1,1,441)
    F+=n.abs(n.fft.fft(ruido,110+1))/2.
    print i 

p.plot(F/F.max())
p.show()

delta=n.array((1))

a0=0.15
b1=0.85

s=[1]
for i in xrange(1,1000):
   s.append(s[-1]*a0) 




#p.specgram(ruido)
#p.show()
