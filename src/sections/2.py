# coding: utf-8
import numpy as n
from scipy.io import wavfile as w

############## 2.1.1 Duration
# the equation relates the number of samples to sound duration
f_a = 44100.  # sample rate
Delta = 3.7   # duration of Delta in seconds

Lambda = int(f_a*Delta)  # number of samples
### 2.1
T_i = n.zeros(Lambda)  # silence with ~Delta, in seconds

# write as a PCM file (WAV)
w.write('silence.wav', f_a, T_i)

############## 2.1.2 Volume
Lambda = 100.  # 100 samples
T_i = n.random.random(Lambda)  # 100 random samples

### 2.2  Potency
pot = (T_i**2.).sum()/Lambda

T2_i = n.random.normal(size=Lambda)
pot2 = (T2_i**2.).sum()/Lambda  # 2 potency
### 2.3 Volume difference, in decibels, given the potencies
V_dB = 10.*n.log10(pot2/pot)

### 2.4 double the amplitude = > gains 6 dB
T2_i = 2.*T_i
pot = (T_i**2.).sum()/Lambda  # potency
pot2 = (T2_i**2.).sum()/Lambda  # 2 potency
V_dB = 10.*n.log10(pot2/pot)
Mm6 = abs(V_dB - 6) < .5  # Mm6 is equal to True

### 2.5 double the potency  = > gains 3 dB
pot2 = 2.*pot
V_dB = 10.*n.log10(pot2/pot)
Mm3 = abs(V_dB - 3) < .5  # Mm3 is equal to True

### 2.7 double the volume  = > gains 10 dB  = > amplitude * 3.16
V_dB = 10.
A = 10.**(V_dB/20.)
T2_i = A*T_i  # A ~ 3.1622776601

### 2.8 Decibels to amplification conversion
A = 10.**(V_dB/20.)


############## 2.1.3 Pitch
f_0 = 441.
lambda_0 = f_a/f_0
cycle = n.arcsin(n.random.random(lambda_0))  # random samples
### 2.9 Sound with fundamental frequency f_0
Tf_i = n.array(list(cycle)*1000)  # 1000 cycles

# normalizing to interval [-1, 1]
Tf_i = ((Tf_i-Tf_i.min())/(Tf_i.max()-Tf_i.min()))*2.-1.
w.write('f_0.wav', f_a, T_i)

############## 2.1.4 Timbre
T = 100000.  # sample number of sequences
ii = n.arange(T)
f = 220.5
lambda_f = f_a/f
### 2.10 Sinusoid
Sf_i = n.sin(2.*n.pi*f*ii/f_a)
### 2.11 Sawtooth
Df_i = (2./lambda_f)*(ii % lambda_f)-1
### 2.12 Triangular
Tf_i = 1.-n.abs(2.-(4./lambda_f)*(ii % lambda_f))
### 2.13 Square
Qf_i = ((ii % lambda_f) < (lambda_f/2))*2-1

Rf_i = w.read("22686__acclivity__oboe-a-440_periodo.wav")[1]
### 2.14 Sampled period
Tf_i = Rf_i[n.int64(ii) % len(Rf_i)]


############## 2.1.5 The spectrum in sampled sound
Lambda = 50.
T_i = n.random.random(Lambda)*2.-1.
C_k = n.fft.fft(T_i)
A_k = n.real(C_k)
B_K = n.imag(C_k)
w_k = 2.*n.pi*n.arange(Lambda)/Lambda


### 2.15 Spectrum recomposition in time
def t(i):
    return (1./Lambda)*n.sum(C_k*n.e**(1j*w_k*i))


### 2.16 Real recomposition
def tR(i):
    return (1./Lambda)*n.sum(n.abs(C_k)*n.cos(w_k*i-n.angle(C_k)))

### 2.17 Number of paired spectrum coefficients
tau = (Lambda - Lambda % 2)/2 + Lambda % 2-1
### 2.18 Equivalent coefficients
kk = n.arange(tau)
F_k = C_k[1:tau+1]
F2_k = C_k[Lambda-tau:Lambda][::-1]

### 2.19 Equivalent coefficients: modules
ab = n.abs(F_k)
ab2 = n.abs(F2_k)
MIN = n.abs(ab-ab2).sum()  # MIN ~ 0.0
### 2.20 Equivalent coefficients: phases
an = n.angle(F_k)
an2 = n.angle(F2_k)
MIN = n.abs(an+an2).sum()  # MIN ~ 0.0

### 2.21 Components combination in each sample
w_k = 2*n.pi*n.arange(Lambda)/Lambda


def t_(i):
    return (1./Lambda)*(A_k[0]+2.*n.sum(n.abs(C_k[1:tau+1]) *
                        n.cos(w_k*i-n.angle(C_k)) + A_k[Lambda/2] *
                        (1-Lambda % 2)))


############## 2.1.6 The basic note
f = 220.5  # Herz
Delta = 2.5  # seconds
Lambda = int(2.5*f_a)
ii = n.arange(Lambda)
Lf_i = Df_i  # We already calculaated Df_i
### 2.24 Basic note
TfD_i = Lf_i[ii % len(Lf_i)]


############## 2.1.7 Spatial localization
zeta = 0.215  # meters
# considering any (x,y) localization
x = 1.5  # meters
y = 1.  # meters
### 2.25 Distances of each ear
d = n.sqrt((x-zeta/2)**2+y**2)
d2 = n.sqrt((x+zeta/2)**2+y**2)
### 2.26 Distances of Interaural Time
DTI = (d2-d)/343.2  # segundos
### 2.27 Distances of Interaural Intensity
DII = 20*n.log10(d/d2)  # dBs

### 2.28 DTI and DII application in T_i
Lambda_DTI = int(DTI*f_a)
DII_a = d/d2
T_i = 1-n.abs(2-(4./lambda_f)*(ii % lambda_f))  # triangular
T2_i = n.hstack((n.zeros(Lambda_DTI), DII_a*T_i))
T_i = n.hstack((T_i, n.zeros(Lambda_DTI)))

som = n.vstack((T2_i, T_i)).T
w.write('estereo.wav', f_a, som)
# mirrored
som = n.vstack((T_i, T2_i)).T
w.write('estereo2.wav', f_a, som)

### 2.29 Object angle
theta = n.arctan(y/x)


############## 2.1.8 Musical uses
Delta = 3.  # 3 seconds
Lambda = int(Delta*f_a)
f1 = 200.  # Hz
foo = n.linspace(0., Delta*f1*2.*n.pi, Lambda, endpoint=False)
T1_i = n.sin(foo)  # sinusoid of Delta seconds and freq  =  f1

f2 = 245.  # Hz
lambda_f2 = int(f_a/f2)
T2_i = (n.arange(Lambda) % lambda_f < (lambda_f2/2))*2-1  # quadrada

f3 = 252.  # Hz
lambda_f3 = f_a/f3
T3_i = n.arange(Lambda) % lambda_f3  # Dente de serra
T3_i = (T3_i/T3_i.max())*2-1

### 2.30 mixing
T_i = T1_i+T2_i+T3_i
# normalization
T_i = ((T_i-T_i.min())/(T_i.max()-T_i.min()))*2-1
# writing file
w.write('mixados.wav', f_a, T_i)

### 2.31 concatenation
T_i = n.hstack((T1_i, T2_i, T3_i))
# writing file
w.write('concatenados.wav', f_a, T_i)
