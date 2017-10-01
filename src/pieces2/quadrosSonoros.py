import numpy as n
from scipy.io import wavfile as w

f_a = 44100  # 44.1kHz, sample rate
Delta = 180.  # each sonic picture will have Delta seconds
Lambda = int(Delta*f_a)  # number of samples

ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)

# frequencies
fs = []
for i in range(1, f_a/2+1):
    if f_a/i == int(f_a/i):
        fs.append(i)

### Picture 1: sinusoids that make beating in the low frequencies
### and in the high frequencies a sawtooth
f1 = 100
f2 = 100.5

som = n.sin(ii*f1)+n.sin(ii*f2)
dente_aguda = (n.arange(Lambda) % 4-2)
som += dente_aguda/80

# normalization for samples to be within [-1,1]
som = ((som - som.min())/(som.max()-som.min()))*2-1
# most music players read only 16-bit wav files, so let's convert the array
som = n.int16(som * (2**15-1))
w.write("picture1.wav",f_a,som)

print(u"picture 1 written in picture1.wav(mono), %i samples \
in a sample rate of %iHz" % (len(som), f_a))


### Picture 2:: 3 sets of triangular waves
fs2 = fs[20:21]+fs[65:70]+fs[77:]
som = n.zeros(Lambda)
ii = n.arange(Lambda)
for f in fs2:
    lambda_f = f_a/f
    som += (1-n.abs(2-(4./lambda_f)*(ii % lambda_f)))*(1./f**1.2)

som = ((som - som.min())/(som.max()-som.min()))*2-1
som = n.int16(som * (2**15-1))
w.write("picture2.wav", f_a, som)
print("picture 2 written in picture2.wav (mono), %i samples \
in a sample rate of %iHz" % (len(som), f_a))


### Picture 3: alternated stereophony in the harmonic spectrum
f = 50.
fs3 = [f*i for i in xrange(1, 7)]  # 6 harmonics
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
som = n.int16(som * (2**15-1))
w.write("picture3.wav", f_a, som)
print("picture 3 written in picture3.wav (stereo), %i samples \
in a sample rate of %iHz" % (len(som), f_a))


### Picture 4: beatings interspersed by side and with lags
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
som_d = ((som_d - som_d.min())/(som_d.max()-som_d.min()))*2-1
som_e = ((som_e - som_e.min())/(som_e.max()-som_e.min()))*2-1
som += n.vstack((som_d, som_e)).T/60

som = n.int16(som * (2**15-1))
w.write("picture4.wav", f_a, som)
print("picture 4 written in picture4.wav (stereo), %i samples \
in a sample rate of %iHz" % (len(som), f_a))


### Picture 5: Low-frequency sawtooth with beating in each side (L-R)
f = 42.
lambda_f = 44100/f
dente = ((n.arange(float(Lambda)) % lambda_f)/lambda_f)*2-1

ii = n.linspace(0, Delta*2*n.pi, Lambda, endpoint=False)
som_d = dente+n.sin(ii*43)+n.sin(ii*84)
som_e = dente+n.sin(ii*43) + n.sin(ii*126.3)

som = n.vstack((som_d, som_e)).T
som = ((som - som.min())/(som.max()-som.min()))*2-1

som = n.int16(som * (2**15-1))
w.write("picture5.wav", f_a, som)
print("picture 5 written in picture5.wav (stereo), %i samples \
in a sample frequency of %iHz" % (len(som), f_a))
