#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

# Peça musical baseada em sons estáticos
# são mixagens de sons básicos apresentados na seção 2.1

f_a = 44100  # 44.1kHz, frequência de amostragem de CDs
Delta = 180.  # cada quadro terá Delta segundos
Lambda = int(Delta*f_a)  # número de amostras

ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)

# frequências que dividem f_a
fs = []
for i in xrange(1, f_a/2+1):
    if f_a/float(i) == int(f_a/i):
        fs.append(i)

### Quadro 1: senoides no grave em batimento e
### no agudo uma dente de serra bem suave
f1 = 100
f2 = 100.5

som = n.sin(ii*f1)+n.sin(ii*f2)
dente_aguda = (n.arange(Lambda) % 4-2)
som += dente_aguda/80

# normalição no intervalo [-1,1]
som = ((som - som.min())/(som.max()-som.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * float(2**15))

w.write("quadro1.wav",f_a,som)

print(u"quadro 1 feito em quadro1.wav (mono), são %i amostras \
em uma frequência de amostragem de %iHz" % (len(som), f_a))


### Quadro 2: 3 conjuntos separados de triangulares
fs2 = fs[20:21]+fs[65:70]+fs[77:]
som = n.zeros(Lambda)
ii = n.arange(Lambda)
for f in fs2:
    lambda_f = f_a/f
    som += (1-n.abs(2-(4./lambda_f)*(ii % lambda_f)))*(1./f**1.2)

# normalizando no intervalo [-1,1]
som = ((som - som.min())/(som.max()-som.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * float(2**15))

w.write("quadro2.wav", f_a, som)
print("quadro 2 feito em quadro2.wav (mono), são %i amostras \
em uma frequência de amostragem de %iHz" % (len(som), f_a))


### Quadro 3: estereofonia alternada no espectro harmônico
f = 50.
fs3 = [f*i for i in xrange(1, 7)]  # 6 harmônicos
som_d = n.zeros(Lambda)
som_e = n.zeros(Lambda)
ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)
i = 0
for f in fs3:
    if i % 2 == 0:
        som_d += n.sin(f*ii)*(1./f)
    else:
        som_e += n.sin(f*ii)*(1./f)
    i += 1
som = n.vstack((som_d, som_e)).T
som = ((som - som.min())/(som.max()-som.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * float(2**15))

w.write("quadro3.wav", f_a, som)
print("quadro 3 feito em quadro3.wav (estéreo), são %i amostras \
em uma frequência de amostragem de %iHz" % (len(som), f_a))


### Quadro 4: batimentos intercalados por ouvido e com defasagens
fs4 = n.array([50, 51.01, 52.01, 53])
som_d = n.zeros(Lambda)
som_e = n.zeros(Lambda)
ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)
i = 0
for f in fs4:
    if i % 2 == 0:
        som_d += n.sin(f*ii)*(1./f)
    else:
        som_e += n.sin(f*ii)*(1./f)
    i += 1
som = n.vstack((som_d, som_e)).T

fs4 = n.array([500, 501.01, 502.01, 503])
som_d = n.zeros(Lambda)
som_e = n.zeros(Lambda)
ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)
i = 0
for f in fs4:
    if i % 2 == 0:
        som_d += n.sin(f*ii)*(1./f)
    else:
        som_e += n.sin(f*ii)*(1./f)
    i += 1
som += n.vstack((som_d, som_e)).T/60
som = ((som - som.min())/(som.max()-som.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * float(2**15))

w.write("quadro4.wav", f_a, som)
print("quadro 4 feito em quadro4.wav (estéreo), são %i amostras \
em uma frequência de amostragem de %iHz" % (len(som), f_a))


### Quadro 5: Dente de serra grave bate com harmônico em cada lado
f = 42.  # Hz, freq da dente
lambda_f = 44100/f
dente = ((n.arange(float(Lambda)) % lambda_f)/lambda_f)*2-1

ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)
som_d = dente+n.sin(ii*43)+n.sin(ii*84)
som_e = dente+n.sin(ii*43) + n.sin(ii*126.3)

som = n.vstack((som_d, som_e)).T
som = ((som - som.min())/(som.max()-som.min()))*2-1

# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * float(2**15))

w.write("quadro5.wav", f_a, som)
print("quadro 5 feito em quadro5.wav (estéreo), são %i amostras \
em uma frequência de amostragem de %iHz" % (len(som), f_a))
