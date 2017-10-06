import numpy as n
from functions import *


##############################
# Study the Fourier components of these sequences
# using a number of normalization routines
# 4 is one simple compass
d1 = n.random.random(4) # qualquer media, em qualquer escala
###### each item can be uderstood as different things
# durations, a quantity:
d2 = [4, 2, 4, 2]  # valsa, 4 duracoes, 2 duracoes
# number of items in a slot, notes per beat:
d2 = [1, 4, 1, 4] # seminima + 4 semicolcheis x 2
d2 = [0, 2, 6, 10, 12]
# any data:
d2 = n.random.power(4) # qualquer media, em qualquer escala
# frequencies
d2 = [2, 4, 2, 4]  # seminima, minima, seminima, things.
d2 = [200, 4000, 20, 44]  # sinusoids, things.
d2 = n.random.power(4) # qualquer media, em qualquer escala


A = n.array
H = n.hstack
def fractalize(d1=A([2, 4, 2, 4]), d2=A([1, 3, 1, 3]),
        d3=A([4,1,1,1,1, 2,2, 4]),
        d4=A([2,8,8,8,8, 4,4, 2]),
        d5=A([3,1, 3,1, 1,1,1,1, 2,2]),
        d6=A([3,1, 3,1, 1,1,1,1, 2,2, 1,3, 1,3]),
        d7=A([3,1, 3,1, 1,1,1,1, 2,2, 1,3]),
        d8=A([2,1, 2,1, 1,1,1, 1,2, 1,2, 3]),
        ):
    """
    Find the relevant frequencies in the data sequences
    
    dX can be any one dimensional numeric sequence.
    If durations, notice that the inverse of durations
    are fequencies:
    >>> d = [3, 1,   3, 1,  1, 1, 1, 1, 4]
    >>> f = [1/i for i in d]
    >>> f_ = [220*i for i in f]

    Half the durations can be regarded as an octave higher:
    >>> d2 = [i/2 for i in d]
    >>> f2_ = [220*1/i for i in d2]

    For artistic purposes, one might relate also longer durations
    with higher pitches:
    >>> d3 = [i*2 for i in d]
    >>> f3 = [f*2 for f in f_]

    """
    adi = locals().copy()
    for i in adi:
        if i.startswith("d"):
            foo = adi[i]
            # attacks through times
            signal = n.zeros(n.sum(foo))
            attacks = H(( [0], n.cumsum(foo)[:-1] ))
            signal[attacks] = 1
            locals()[i+"S"] = signal
            locals()[i+"A"] = attacks
    adi = locals().copy()
    for i in adi:
        if i.startswith("d"):
            foo = adi[i]
            locals()[i+"_"] = (foo-foo.min())/(foo.max() - foo.min())
            locals()[i+"_b"] = 2*(foo-foo.min())/(foo.max() - foo.min()) -1
            locals()[i+"_a"] = n.log(foo - foo.min())
            locals()[i+"_c"] = (foo-foo.mean())/foo.std()
    adi = locals().copy()
    for i in adi:
        if i.startswith("d"):
            foo = n.sort(adi[i])
            locals()[i+"s"] = foo
    adi = locals().copy()
    for i in adi:
        if i.startswith("d"):
            foo = adi[i][1:] - adi[i][:-1]
            locals()[i+"d"] = foo

    adi = locals().copy()
    d = {"wnan" : {}, "wonan" : {}}
    for i in adi:
        if i.startswith("d"):
            fft = n.fft.fft(locals()[i])
            if n.nan in adi[i]:
                # print(i, di[i], fft, n.abs(fft), n.angle(fft), "\n\n")
                d["wnan"][i] = [adi[i], fft, n.abs(fft), n.angle(fft)]
            else:
                # print(i, di[i], fft, n.abs(fft), n.angle(fft), "\n\n")
                d["wonan"][i] = [adi[i], fft, n.abs(fft), n.angle(fft)]
    return d


dd=fractalize()["wonan"]

# 4 samples, tempos per second, 4 Hz
# 4 can be sum of adjacent values
# or total value of the sequence

# What are the frequencies in f = fft(dd)?
# They have pairs (f[1:n.ceil(L//2-1)] because d is real.
# L = len(f) = f.shape[0]
# f[0] and f[L//2] (if l//2) are alone.
# f[0] can be, f[L//2] and possibly is, only if it is even (L%2 == 0)

# f[0] is zero times per second. The mean of the signal, be it ordered or not.
# It is zero if dd is nomalized with dd=dd.mim().
# f[1] is once in the period
# f[2] is twice in the period
# f[3] is once in the period

# f[1] and f[3] both have the same amplitude
# and are related to the same phase:
# c.sin(x+t) = a.cos( x + t1 ) b.sin(x + t2)

# c.cos(x+t) = a.cos( x + t1 ) b.sin(x + t2)
# (a^2 + b^2)^.5 x cos(x+atan(t2, t1)) = a.cos( x + t1 ) b.sin(x + t2)

# c.cos(x+t) = a.cos( x + t(L-1) ) b.sin(x + t[L-1])

# N can be 100 samples or fs = 100
# Uses the resolution of number of samples samples per second:
# frequency goes all the way from no oscilation
# to 2*pi : the nyquist frequency = fs/2

# to number of beats = fs = 2 => greatest frequency = 1
# tau = 0
# f = zero and 1

# to number of beats = fs = 4 => greatest frequency = 2
# tau = 2
# f = zero, fs/4, 2*fs/4

# to number of beats = fs = 4 => greatest frequency = 2
# fs = 6 => fn = 6/2= 3 (zero and 3)
# fs = 8 => fn = 8/2= 4 (zero 2 and 4)
# fs = 9 => fn = 9/2= 4 (zero 1.5, )

N = 10
freqs_da_base_ = n.arange(0,N)  # freqs in number of samples
freqs_da_base = 2*n.pi*freqs_da_base_/N  # freqs in radians
# The normalized base is actually (cos + sin)/N.
# For now, we are sticking to the description in MASS article
# where the normalization is performed in the reconstruction.
base = [(n.cos(f*n.arange(N)), -n.sin(f*n.arange(N))) for f in freqs_da_base]
# base[i] is an axis, a dimension in the spectral base

signal = n.sin(n.arange(N)*2*n.pi/N)
signal2 = n.random.random(N)
signal3 = n.arange(N)%2 # sawtooth
signal3 = list(range(N)) # sawtooth

ds = locals().copy()
sines = {}
samples = n.arange(N)
reconst = {}
reconst_ = {}
for si in ds:
    if si.startswith("s"):
        foo = si
        sines[si] = []
        reconst[si] = n.zeros(N)
        reconst_[si] = n.zeros(N)
        for freq in range(N):
            component_cos = n.sum(base[freq][0]*ds[si])
            component_sin = n.sum(base[freq][1]*ds[si])
            amplitude = (component_cos**2+component_sin**2)**.5
            phase = n.arctan2(component_sin, component_cos)
            # print(
            # component_cos,
            # component_sin,
            # sines_amplitude,
            # sines_phase
            # )
            sines[si].append((
            component_cos,
            component_sin,
            # amplitude,
            # phase
            ))
            reconst[si] += (component_cos * base[freq][0] + component_sin * base[freq][1])/N
            reconst_[si] += amplitude * n.cos(freqs_da_base[freq] * n.arange(N) + phase)/N

# reconstruct the signal using all coefficients and only the ones <= N/2
for si in ds:
    if si.startswith("s"):
        # reconst[si] = []
        for freq in range(N):
            freq_ = freqs_da_base[freq]
            pass

# usar como bases trechos arbitrarios de algum compositor.
# Usar as mesmas amplitudes, mas mudar as fases
# Isso para o ritmo e para as frequencias
# medir a quantidade que encontrou daquele trecho.
# Usar tambem como base mas no espectro
# tipo: medidas do mozart em numeros midi e duracoes:
# [0, 4, 7, 4, 7, 8, 7, 0, 2, 0]
# [1, 1, 1, 1, 3, 1, 3, 2, 2, 4]
# usar de base para processar scarlatti no beethoven
# usar as componentes de um no outro para sintetizar
# melodias.

# extract sonorities from data by using its fourier
# constituents to synthesize sounds and musical
# structures and mix them together.
# make it dwelve structures e.g. by input of a string
# such as the name of the user.
