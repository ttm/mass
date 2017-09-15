import numpy as n
from scipy.io import wavfile as w

def __n(sonic_array):
    """Normalize sonic_array to have values only between -1 and 1"""

    t = sonic_array
    if n.all(sonic_array==0):
        return sonic_array
    else:
        return ( (t-t.min()) / (t.max() -t.min()) )*2.-1.

def __s(sonic_array=n.random.uniform(size=100000), filename="asound.wav", f_a=44100):
    """A minimal approach to writing 16 bit WAVE files.
    
    One can also use, for example:
        import sounddevice as S
        S.play(array) # the array must have values between -1 and 1"""

    # to write the file using XX bits per sample
    # simply use s = n.intXX(__n(sonic_array)*(2**(XX-1)-1))
    s = n.int16(__n(sonic_array)*32767)
    w.write(filename, f_a, s)


############## Sec. 2.1 Duration
# relation between the number of samples and the sound duration
f_a = 44100  # sample rate
Delta = 3.7   # duration of Delta in seconds

Lambda = int(f_a*Delta)  # number of samples
### Eq. 1
T = n.zeros(Lambda)  # silence with ~Delta, in seconds

# write as a PCM file (WAV)
__s(T, 'silence.wav')

############## Sec. 2.2 Loudness
Lambda = 100  # 100 samples
T = n.random.random(Lambda)  # 100 random samples

### Eq. 2 Power of wave
pow1 = (T**2.).sum()/Lambda

T2 = n.random.normal(size=Lambda)
pow2 = (T2**2.).sum()/Lambda  # power of another wave

### Eq. 3 Volume difference, in decibels, given the powers
V_dB = 10.*n.log10(pow2/pow1)

### Eq. 4 double the amplitude => gains 6 dB
T2 = 2.*T
pow2 = (T2**2.).sum()/Lambda
V_dB = 10.*n.log10(pow2/pow1)
is_6db = abs(V_dB - 6) < .05  # is_6db is True

### Eq. 5 double the power => gains 3 dB
pow2 = 2.*pow1
V_dB = 10.*n.log10(pow2/pow1)
is_3dB = abs(V_dB - 3) < .05  # is_3dB is True

### Eq. 6 double the volume => gains 10 dB => amplitude * 3.16
V_dB = 10.
A = 10.**(V_dB/20.)
T2 = A*T  # A ~ 3.1622776601

### Eq. 7 Decibels to amplification conversion
A = 10.**(V_dB/20.)


############## Sec. 2.3 Pitch
f_0 = 441
lambda_0 = f_a//f_0
cycle = n.arcsin(n.random.random(lambda_0))  # random samples
### Eq. 8 Sound with fundamental frequency f_0
Tf = n.array(list(cycle)*1000)  # 1000 cycles

# normalizing to interval [-1, 1]
__s(Tf,'f_0.wav')


############## Sec. 2.4 Timbre
L = 100000.  # sample number of sequences (Lambda)
ii = n.arange(L)
f = 220.5
lambda_f = f_a/f
### Eq. 9 Sinusoid
Sf = n.sin(2.*n.pi*f*ii/f_a)
### Eq. 10 Sawtooth
Df = (2./lambda_f)*(ii % lambda_f)-1
### Eq. 11 Triangular
Tf = 1.-n.abs(2.-(4./lambda_f)*(ii % lambda_f))
### Eq. 12 Square
Qf = ((ii % lambda_f) < (lambda_f/2))*2-1

Rf = w.read("22686__acclivity__oboe-a-440_periodo.wav")[1]
### Eq. 13 Sampled period
Tf = Rf[n.int64(ii) % len(Rf)]


############## Sec. 2.5 The spectrum of sampled sound
Lambda = 50
T = n.random.random(Lambda)*2.-1.
C_k = n.fft.fft(T)
A_k = n.real(C_k)
B_K = n.imag(C_k)
w_k = 2.*n.pi*n.arange(Lambda)/Lambda

### Eq .14 Spectrum recomposition in time
def t(i):
    return (1./Lambda)*n.sum(C_k*n.e**(1j*w_k*i))

### Eq. 15 Real recomposition
def tR(i):
    return (1./Lambda)*n.sum(n.abs(C_k)*n.cos(w_k*i-n.angle(C_k)))

### Eq. 16 Number of paired spectrum coefficients
tau = int( (Lambda - Lambda % 2)/2 + Lambda % 2-1 )

### Eq. 17 Equivalent coefficients
F_k = C_k[1:tau+1]
F2_k = C_k[Lambda-tau:Lambda][::-1]

### Eq. 18 Equivalent modules of coefficients
ab = n.abs(F_k)
ab2 = n.abs(F2_k)
MIN = n.abs(ab-ab2).sum()  # MIN ~ 0.0

### Eq, 19 Equivalent phases of coefficients
an = n.angle(F_k)
an2 = n.angle(F2_k)
MIN = n.abs(an+an2).sum()  # MIN ~ 0.0

### Eq. 20 Components combination in each sample
w_k = 2*n.pi*n.arange(Lambda)/Lambda

def t_(i):
    return (1./Lambda)*(A_k[0]+2.*n.sum(n.abs(C_k[1:tau+1]) *
                        n.cos(w_k*i-n.angle(C_k)) + A_k[Lambda/2] *
                        (1-Lambda % 2)))


############## Sec. 2.6 The basic note
f = 220.5  # Herz
Delta = 2.5  # seconds
Lambda = int(2.5*f_a)
ii = n.arange(Lambda)

### Eq. 21 Basic note (preliminary)
ti_ = n.random.random(int(f_a/f))  # arbitrary sequence of samples
TfD = ti_[ii % len(ti_)]

### Eq. 22 Choose any waveform
Lf = [Sf, Qf, Tf, Df, Rf][1]  # We already calculated these sequences

### Eq. 23 Basic note
TfD = Lf[ii % len(Lf)]


############## Sec. 2.7 Spatialization: localization and reverberation
zeta = 0.215  # meters
# considering any (x,y) localization
x = 1.5  # meters
y = 1.  # meters
### Eq. 24 Distances from each ear
d = n.sqrt((x-zeta/2)**2+y**2)
d2 = n.sqrt((x+zeta/2)**2+y**2)
### Eq. 25 Interaural Time Difference
ITD = (d2-d)/343.2  # segundos
### Eq. 26 Interaural Intensity Difference
IID = 20*n.log10(d/d2)  # dBs

### Eq. 27 DTI and DII application in a sample sequence (T)
Lambda_ITD = int(ITD*f_a)
IID_a = d/d2
T = 1-n.abs(2-(4./lambda_f)*(ii % lambda_f))  # triangular
T2 = n.hstack((n.zeros(Lambda_ITD), IID_a*T))
T = n.hstack((T, n.zeros(Lambda_ITD)))

som = n.vstack((T2, T)).T
w.write('stereo.wav', f_a, som)
# mirrored
som = n.vstack((T, T2)).T
w.write('stereo2.wav', f_a, som)

### Eq. 28 Object angle
theta = n.arctan(y/x)

### Reverberation is implemented in 3.py
# because it makes use of knowledge of the next section


############## Sec. 2.8 Musical uses
Delta = 3.  # 3 seconds
Lambda = int(Delta*f_a)
f1 = 200.  # Hz
foo = n.linspace(0., Delta*f1*2.*n.pi, Lambda, endpoint=False)
T1 = n.sin(foo)  # sinusoid of Delta seconds and freq  =  f1

f2 = 245.  # Hz
lambda_f2 = int(f_a/f2)
T2 = (n.arange(Lambda) % lambda_f < (lambda_f2/2))*2-1  # square

f3 = 252.  # Hz
lambda_f3 = f_a/f3
T3 = n.arange(Lambda) % lambda_f3  # sawtooth
T3 = (T3/T3.max())*2-1

### Eq. 29 mixing
T = T1+T2+T3
# writing file
__s(T, 'mixed.wav')

### Eq. 30 concatenation
T = n.hstack((T1, T2, T3))
# writing file
__s(T, 'concatenated.wav')
