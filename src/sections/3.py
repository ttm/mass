import numpy as n
from scipy.io import wavfile as w

def __n(sonic_array):
    """Normalize sonic_array to have values only between -1 and 1"""

    t = sonic_array
    if n.all(sonic_array==0):
        return sonic_array
    else:
        return ( (t-t.min()) / (t.max() -t.min()) )*2.-1.

def __s(sonic_array=n.random.uniform(size=100000), filename="asound.wav", f_s=44100):
    """A minimal approach to writing 16 bit WAVE files.
    
    One can also use, for example:
        import sounddevice as S
        S.play(array) # the array must have values between -1 and 1"""

    # to write the file using XX bits per sample
    # simply use s = n.intXX(__n(sonic_array)*(2**(XX-1)-1))
    s = n.int16(__n(sonic_array)*32767)
    w.write(filename, f_s, s)


f_s = 44100  # Hz, sample rate

############## Sec. 3.1 Lookup table (LUT)
# at least 1024 samples in the table
Lambda_tilde = Lt = 1024

# Sinusoid
foo = n.linspace(0, 2*n.pi, Lt, endpoint=False)
S = n.sin(foo)  # a sinusoidal period with T samples

# Square:
Q = n.hstack((n.ones(Lt/2)*-1, n.ones(Lt/2)))

# Triangular:
foo = n.linspace(-1, 1, Lt/2, endpoint=False)
Tr = n.hstack((foo, foo*-1))

# Sawtooth:
D = n.linspace(-1, 1, Lt)

# real sound, import period and
# use the number of samples in the period
Rf = w.read("22686__acclivity__oboe-a-440_periodo.wav")[1]

f = 110.  # Hz
Delta = 3.4  # seconds
Lambda = int(Delta*f_s)

# Samples:
ii = n.arange(Lambda)

### Eq. 31 LUT
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
# It is possible to use S, Q, D or any other period of a real sound
# with a sufficient length
L = Tr
TfD = L[Gamma % Lt]


############## Sec. 3.2 Incremental variations of frequency and intensity
# == FREQUENCY VARIATIONS ==
f_0 = 100.  # initial freq in Hz
f_f = 300.  # final freq in Hz
Delta = 2.4  # duration

Lambda = int(f_s*Delta)
ii = n.arange(Lambda)
### Eq. 32 linear variation
f_i = f_0+(f_f-f_0)*ii/(float(Lambda)-1)
### Eq. 33 coefficients for LUT
D_gamma = f_i*Lt/f_s
Gamma = n.cumsum(D_gamma)
Gamma = n.array(Gamma, dtype=n.int)
### Eq. 34 resulting sound
Tf0ff = L[Gamma % Lt]

### Eq. 35 exponential variation
f_i = f_0*(f_f/f_0)**(ii/(float(Lambda)-1))
### Eq. 36 coefficients for the LUT
D_gamma = f_i*Lt/f_s
Gamma = n.cumsum(D_gamma)
Gamma = n.array(Gamma, dtype=n.int)
### Eq. 37 resulting sound
Tf0ff = L[Gamma % Lt]


# == INTENSITY VARIATIONS ==
# First, make/have an arbitrary sound to
# apply the variations in amplitude
f = 220.  # Hz
Delta = 3.9  # seconds
Lambda = int(Delta*f_s)

# Sample indexes:
ii = n.arange(Lambda)

# (as in Eq. 31)
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
L = Tr
T = TfD = L[Gamma % Lt]

a_0 = 1.  # starting fraction of the amplitude
a_f = 12.  # ending fraction of the amplitude
alpha = 1.  # index of transition smoothing

### Eq. 38 exponential transition of amplitude
A = a_0*(a_f/a_0)**((ii/float(Lambda))**alpha)
### Eq. 39 applying envelope A to the sound
T2 = A*T

### Eq. 40 linear transition of amplitude
A = a_0+(a_f-a_0)*(ii/float(Lambda))

### Eq. 41 exponential transition of V_dB decibels
V_dB = 31.
T2 = T*((10*(V_dB/20.))**((ii/float(Lambda))**alpha))


############## Sec 3.3 Application of digital filters
# See src/aux/delays.py for generating Fig. 17
# See src/aux/filters/iir.py for generating Fig. 18

# synthetic impulse response (for a "reverb", a better reverb is bellow in: Reverberation)
H = (n.random.random(10)*2-1)*n.e**(-n.arange(10))

### Eq. 42 Convolution (application of a FIR filter)
T2 = n.convolve(T, H)  # T from above

### Eq. 43  difference equation
A = n.random.random(2)  # arbitrary coefficients
B = n.random.random(3)  # arbitrary coefficients

def applyIIR(signal, A, B):
    signal_ = []
    for i, sample in enumerate(signal):
        samples_A = signal[i::-1][:len(A)]
        A_coeffs = A[:i+1]
        A_contrib = (samples_A*A_coeffs).sum()

        samples_B = signal_[-1:-1-i:-1][:len(B)-1]
        B_coeffs = B[1:i+1]
        B_contrib = (samples_B*B_coeffs).sum()
        t_i = (A_contrib + B_contrib)/B[0]
        signal_.append(t_i)
    return signal_

fc = .1
### Eq. 44 low-pass IIR filter with a single pole
x = n.e**(-2*n.pi*fc)  # fc => cutoff frequency where the resulting signal has -3dB
# coefficients
a0 = 1-x
b1 = x
# applying the filter
T2 = [T[0]]
for t_i in T[1:]:
    T2.append(t_i*a_0+T2[-1]*b1)

### Eq. 45 high-pass filter with a single pole
x = n.e**(-2*n.pi*fc)  # fc => cutoff frequency where the resulting signal has -3dB
# coefficients
a0 = (1+x)/2
a1 = -(1+x)/2
b1 = x

# applying the filter
T2 = [a0*T[0]]
last = T[0]
for t_i in T[1:]:
    T2 += [a0*t_i + a1*last + b1*T2[-1]]
    last = n.copy(t_i)


fc = .1  # now fc is the center frequency
bw = .05
### Eq. 46 Auxiliary variables for the notch filters
r = 1-3*bw
k = (1-2*r*n.cos(2*n.pi*fc)+r**2)/(2-2*n.cos(2*n.pi*fc))

### Eq. 47 band-pass filter coefficients
a0 = 1-k
a1 = -2*(k-r)*n.cos(2*n.pi*fc)
a2 = r**2 - k
b1 = 2*r*n.cos(2*n.pi*fc)
b2 = -r**2

# applying the filter
T2 = [a0*T[0]]
T2 += [a0*T[1]+a1*T[0]+b1*T2[-1]]
last1 = T[1]
last2 = T[0]
for t_i in T[2:]:
    T2 += [a0*t_i+a1*last1+a2*last2+b1*T2[-1]+b2*T2[-2]]
    last2 = n.copy(last1)
    last1 = n.copy(t_i)

### Eq. 48 band-reject filter coefficients
a0 = k
a1 = -2*k*n.cos(2*n.pi*fc)
a2 = k
b1 = 2*r*n.cos(2*n.pi*fc)
b2 = -r**2

# applying the filter
T2 = [a0*T[0]]
T2 += [a0*T[1]+a1*T[0]+b1*T2[-1]]
last1 = T[1]
last2 = T[0]
for t_i in T[2:]:
    T2 += [a0*t_i+a1*last1+a2*last2+b1*T2[-1]+b2*T2[-2]]
    last2 = n.copy(last1)
    last1 = n.copy(t_i)


############## Sec. 3.4 Noise
# See src/filters/ruidos.py for rendering Figure 19
Lambda = 100000  # Use an even Lambda for compliance with the following snippets
# Separation between frequencies of neighbor spectral coefficients:
df = f_s/float(Lambda)

### Eq. 49 White noise
# uniform moduli of spectrum and random phase
coefs = n.exp(1j*n.random.uniform(0, 2*n.pi, Lambda))

f0 = 15.  # minimum frequency which we want in the sound
i0 = n.floor(f0/df)  # first coefficient to be considered
coefs[:i0] = n.zeros(i0)

# coefficients have real part even and imaginary part odd
coefs[Lambda/2+1:] = n.real(coefs[1:Lambda/2])[::-1] - 1j * \
    n.imag(coefs[1:Lambda/2])[::-1]
coefs[0] = 0.  # no bias (no offset)
coefs[Lambda/2] = 1.  # max freq is only real (as explained in Sec. 2.5)

# Achievement of the temporal samples of the noise
ruido = n.fft.ifft(coefs)
r = n.real(ruido)
__s(r, 'white.wav')

# auxiliary variables to all the following noises
fi = n.arange(coefs.shape[0])*df # frequencies related to the coefficients
f0 = fi[i0] # first frequency to be considered 

### Eq. 50 Pink noise
# the volume decreases by 3dB at each octave
factor = 10.**(-3/20.)
alphai = factor**(n.log2(fi[i0:]/f0))

c = n.copy(coefs)
c[i0:] = coefs[i0:]*alphai
# real is even, imaginary is odd
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
__s(r, 'pink.wav')


### Eq. 51 Brown(ian) noise
# the volume decreases by 6dB at each octave
fator = 10.**(-6/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real is even, imaginary is odd
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
__s(r, 'brown.wav')

ruido_marrom = n.copy(r) # it will be used for reverberation


### Eq. 52 Blue noise
# the volume increases by 3dB at each octave
fator = 10.**(3/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real is even, imaginary is odd
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
__s(r, 'blue.wav')


### Eq. 53 Violet noise
# the volume increses by 6dB at each octave
fator = 10.**(6/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real is even, imaginary is odd
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
__s(r, 'violet.wav')

### Eq.54 Black noise
# the volume decreases more than 6dB at each octave
fator = 10.**(-12/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real is even, imaginary is odd
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
__s(r, 'black.wav')


############## Sec. 3.5 Tremolo e vibrato, AM e FM
# See src/aux/vibrato.py and src/aux/tremolo.py for rendering Figures 20 and 21
f = 220.
Lv = 2048  # size of the table for the vibrato
fv = 1.5  # vibrato frequency
nu = 1.6  # maximum semitone deviation (vibrato depth)
Delta = 5.2  # sound duration
Lambda = int(Delta*f_s)

# Vibrato table
x = n.linspace(0, 2*n.pi, Lv, endpoint=False)
tabv = n.sin(x)  # sinusoidal vibrato

ii = n.arange(Lambda)  # índices
### Eq. 55 indexes of the LUT for the vibrato
Gammav = n.array(ii*fv*float(Lv)/f_s, n.int)
### Eq. 56 samples of the oscillatory pattern of the vibrato
Tv = tabv[Gammav % Lv]
### Eq. 57 frequency at each sample
F = f*(2.**(Tv*nu/12.))
### Eq. 58 indexes of the LUT for the sound
D_gamma = F*(Lt/float(f_s))  # displacement in the table for each sample
Gamma = n.cumsum(D_gamma)  # total displacement at each sample
Gamma = n.array(Gamma, dtype=n.int)  # final indexes
### Eq. 59 the samples of the sound
T = Tr[Gamma % Lt]  # Lookup

__s(T, "vibrato.wav")


Tt = n.copy(Tv)  # same oscillatory pattern from the vibrato
### Eq. 60 Envelope of the tremolo
V_dB = 12.  # decibels variation involved in the tremolo (tremolo depth)
A = 10**((V_dB/20)*Tt)  # amplitude multiplicative factors for each sample
### Eq. 61 Application of the amplitude envelope to the original sample sequence T
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
T = Tr[Gamma % Lt]
T = T*A
__s(T, "tremolo.wav")


# the following equations are not used to synthesize sounds,
# but only to express the spectrum resulting from FM and AM synthesis
### Eq. 62 - FM spectrum, implemented in Eqs. 65-69
### Eq. 63 - Bessel function
### Eq. 64 - AM spectrum, implemented in Eqs. 70,71

fv = 60.  # typically, fv > 20Hz (otherwise one might want to use the equations above for the vibrato)
### Eq. 65 indexes of the LUT for the FM modulator
Gammav = n.array( ii*fv*float(Lv)/f_s, n.int )
### Eq. 66 oscillatory pattern (sample-by-sample) of the modulator
Tfm = tabv[Gammav % Lv]
f = 330.
mu = 40.
### Eq. 67 frequency at each sample
F = f+Tfm*mu
### Eq. 68 indexes of the LUT
D_gamma = f_i*(Lt/float(f_s))  # displacement in the lookup between each sample
Gamma = n.cumsum(D_gamma)  # total displacement in the lookup at each sample
Gamma = n.array(Gamma, dtype=n.int)  # indexes
### Eq. 69 FM
T = S[Gamma % Lt]  # final samples

# writing the sound file
__s(T, "fm.wav")


# AM
Tam = n.copy(Tfm)
V_dB = 12.  # am depth in decibels
alpha = 10**(V_dB/20.)  # AM depth in amplitude
### 2.71 AM envelope
A = 1+alpha*Tam
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
### 2.70 AM
T = Tr[Gamma % Lt]*A
__s(T, "am.wav")


############## Sec. 3.6 Usos musicais
### Eq. 72 Relations between characteristics
# See the musical piece Tremolos, vibratos and the frequency
# in src/pieces3/bonds.py TremolosVibratosEaFrequencia.py

# Doppler effect
v_r= 10 # receptor moves in the direction of the source with velocity v_r m/s
v_s=-80. # source moves in the direction of receptor with velocity v_s m/s
v_som=343.2
f_0=1000 # frequency of the source

### Eq. 73 Frequency resulting from the Doppler effect
f=((v_som + v_r) / (v_som + v_s)) * f_0
# after crossing of source and receptor:
f_=((v_som - v_r) / (v_som - v_s)) * f_0

# initial distances:
x_0=0 # source at front of x_0
y_0=200 # height of y_0 metros

Delta=5. # duration in seconds
Lambda=Delta*f_s # number of samples
# posições ao longo do tempo, X_i=n.zeros(Lambda)
Y=y_0 - ((v_r-v_s)*Delta) * n.linspace(0,1,Lambda)

# At each sample, calculating ITD and IID as explained in the last section
# In this case, ITD e IID are == 0 because the source is centered
### Eq. 74 Amplitude resulting from the Doppler effect
# Assume z_0 meters above receptor:
z_0=2.
D=( z_0**2+Y**2  )**0.5 # distance at each PCM sample
# Amplitude of sound related to the distance:
A_=z_0/D
### Amplitude change factor resulting from the Doppler effect:
A_DP=( (v_r-v_s)/343.2+1 )**0.5
A_DP_=( (-v_r+v_s)/343.2+1 )**0.5
A_DP=(Y>0)*A_DP+(Y<0)*A_DP_
A=A_ * A_DP

# Upon crossing, the velocities change sign:
### Eq. 75 Frequency progression
coseno=(Y)/((Y**2+z_0**2)**0.5)
F=( ( 343.2+v_r*coseno ) / ( 343.2+v_s*coseno ) )*f_0
# coefficients of the LUT
D_gamma = F*Lt/f_s
Gamma = n.cumsum(D_gamma)
Gamma = n.array(Gamma, dtype=n.int)

L = Tr  # Triangular wave
# Resulting sound:
Tdoppler = L[Gamma % Lt]
Tdoppler*=A

# normalizing and writing sound
__s(Tdoppler, 'doppler.wav')


######## Reverberation
# First reverberation period:
Delta1 = 0.15 # typically E [0.1,0.2]
Lambda1= int(Delta1*f_s)
Delta = 1.9 # total duration of reverberation
Lambda=int(Delta*f_s)

# Sound reincidence probability probability in the first period:
ii=n.arange(Lambda)
P = (ii[:Lambda1]/float(Lambda1))**2.
# incidences:
R1_=n.random.random(Lambda1)<P
A=10.**((-50./20)*(ii/Lambda))
### Eq. 76 First period of reverberation:
R1=R1_*A[:Lambda1]*ruido_marrom[:Lambda1] # first incidences

# Brown noise with exponential decay (of amplitude) for the second period:
### Eq. 77 Second period of reverberation:
Rm=ruido_marrom[Lambda1:Lambda]
R2=Rm*A[Lambda1:Lambda]
### Eq. 78 Impulse response of the reverberation
R=n.hstack((R1,R2))
R[0]=1.

# Making an arbitrary sound to apply the reverberation:
f_0 = 100.  # starting freq (Hz)
f_f = 700.  # final freq (Hz)
Delta = 2.4  # duration
Lambda = int(f_s*Delta)
ii = n.arange(Lambda)

# (using Eq. 35 for exponential variation)
F = f_0*(f_f/f_0)**(ii/(float(Lambda)-1))
# (using Eq. 36 for the LUT indexes)
D_gamma = F*Lt/f_s
Gamma = n.cumsum(D_gamma)
Gamma = n.array(Gamma, dtype=n.int)
# (using Eq. 2.37 for making the sound)
Tf0ff = L[Gamma % Lt]

# Applying the reverberation
T_=Tf0ff
T=n.convolve(T_,R)
__s(T, "reverb.wav")


### Eq. 79 ADSR - linear variation
Delta = 5.  # total duration in seconds
Delta_A = 0.1  # Attack
Delta_D = .3  # Decay
Delta_R = .2  # Release
a_S = .1  # Sustain level

Lambda = int(f_s*Delta)
Lambda_A = int(f_s*Delta_A)
Lambda_D = int(f_s*Delta_D)
Lambda_R = int(f_s*Delta_R)

# Achievement of the ADRS envelope: A_
ii = n.arange(Lambda_A, dtype=n.float)
A = ii/(Lambda_A-1)
A_ = A
ii = n.arange(Lambda_A, Lambda_D+Lambda_A, dtype=n.float)
D = 1-(1-a_S)*((ii-Lambda_A)/(Lambda_D-1))
A_ = n.hstack((A_, D))
S = a_S*n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D), dtype=n.float)
A_ = n.hstack((A_, S))
ii = n.arange(Lambda-Lambda_R, Lambda, dtype=n.float)
R = a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
A_ = n.hstack((A_, R))

### Eq. 80 Achievement of a sound with the ADSR envelope
ii = n.arange(Lambda, dtype=n.float)
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
T = Tr[Gamma % Lt]*(A_)

__s(T, "adsr.wav")


### Eq. 79 ADSR - exponential variation
xi = 1e-2  # -180dB for starting fade in and ending in the fade out
De = 2*100.  # total duration 
DA = 2*20.  # attack duration
DD = 2*20.  # decay duration
DR = 2*20.  # release duration
SS = .4  # fraction of amplitude in which sustain occurs

Lambda = int(f_s*De)
Lambda_A = int(f_s*DA)
Lambda_D = int(f_s*DD)
Lambda_R = int(f_s*DR)

A = xi*(1./xi)**(n.arange(Lambda_A)/(Lambda_A-1))  # attack samples
A = n.copy(A)
D = a_S**((n.arange(Lambda_A, Lambda_A+Lambda_D)-Lambda_A)/(Lambda_D-1)) # decay samples
A = n.hstack((A, D))
S = a_S*n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D))  # sustain samples
A = n.hstack((A, S))
R = (SS)*(xi/SS)**((n.arange(Lambda-Lambda_R, Lambda)+Lambda_R-Lambda)/(Lambda_R-1))  # release
A = n.hstack((A,  R))

### Eq. 80 Achievement of sound with ADSR envelope
ii = n.arange(Lambda, dtype=n.float)
Gamma = n.array(ii*f*Lt/f_s, dtype=n.int)
T = Tr[Gamma % Lt]*(A)

__s(T, "adsr_exp.wav")
