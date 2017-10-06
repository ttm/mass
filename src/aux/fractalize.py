import numpy as n

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


# normalize as quanted
def fractalize(numbers=[2, 4, 2, 4], numbers2=[1, 3, 1, 3]):
    d1 = n.array(numbers)
    d2 = n.array(numbers2)
    d1_ = (d1-d1.min())/(d1.max() - d1.min())
    d2_ = (d2-d2.min())/(d2.max() - d2.min())
    d1_a = n.log(d1_ - d1.min())
    d2_a = n.log(d2_ - d2.min())

    # do not need to be ordered
    d1s =  n.sort(d1)
    d2s =  n.sort(d2)
    d1__ =  n.sort(d1_)
    d2__ =  n.sort(d2_)
    d1_a_ = n.sort(d1_a)
    d2_a_ = n.sort(d2_a)

    # if sorted, distances might be more meaningful
    # just as strong beats in measures or
    # attacks of notes
    d1d = d1__[1:] - d1__[:-1] 
    d2d = d2__[1:] - d2__[:-1] 

    d1__d = d1__[1:] - d1__[:-1] 
    d2__d_ = d2__[:-1] - d2__[1:] 

    # print(locals())
    di = locals().copy()
    d = {"wnan" : {}, "wonan" : {}}
    for i in di:
        if i.startswith("d"):
            fft = n.fft.fft(locals()[i])
            if n.nan in di[i]:
                # print(i, di[i], fft, n.abs(fft), n.angle(fft), "\n\n")
                d["wnan"][i] = [di[i], fft, n.abs(fft), n.angle(fft)]
            else:
                # print(i, di[i], fft, n.abs(fft), n.angle(fft), "\n\n")
                d["wonan"][i] = [di[i], fft, n.abs(fft), n.angle(fft)]
    return d
    # fft=

    # take the Fourier of them, whatch the frequencies

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
# It is zero if dd is nomalized.
# f[1] is 2 times per second
# f[2] is 4 times per second
# f[3] is 2 times per second

# f[1] and f[3] both have the same amplitude
# and is related to the same phase:
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

N = 4
freqs_da_base=base = 2*n.pi*n.arange(0,N)/(N-1)  # real
base = [(n.cos(f), n.sin(f)) for f in freqs_da_base]
# base[i] is an axis, a dimension in the spectral base

signal = n.sin(100*2*n.pi)
signal2 = n.random.random(100)
signal3 = n.arange(100)%20 # sawtooth
signal3 = list(range(N)) # sawtooth

ds = locals().copy()
sines = {}
samples = n.arange(N)
for si in ds:
    if si.startswith("s"):
        sines[si] = []
        for freq in range(N):
            sine = n.sin(
            cos  = 
            component_cos = n.sum(base[freq][0]*ds[si])
            component_sin = n.sum(base[freq][1]*ds[si])
            sines_amplitude = (component_cos**2+component_sin**2)**.5
            sines_phase = n.arctan2(component_sin, component_cos)
            # print(
            # component_cos,
            # component_sin,
            # sines_amplitude,
            # sines_phase
            # )
            sines[si].append((
            component_cos,
            component_sin,
            sines_amplitude,
            sines_phase
            ))

# usar como bases trechos arbitrarios de algum compositor.
# Usar as mesmas amplitudes, mas mudar as fases
# Isso para o ritmo e para as frequencias
# medir a quantidade que encontrou daquele trecho.
# Usar tambem como base mas no espectro
# tipo: meldia do mozart em numeros midi e duracoes:
# [0, 4, 7, 4, 7, 8, 7, 0, 2, 0]
# [1, 1, 1, 1, 3, 1, 3, 2, 2, 4]
# usar de base para processar scarlatti no beethoven
# usar as componentes de um no outro para sintetizar
# melodias.










