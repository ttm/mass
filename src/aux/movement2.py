import numpy as n
# from scipy.io import wavfile as w
import imp
fun = imp.load_source("functions","./functions.py")
for i in dir(fun):
    locals()[i] = eval("fun."+i)

sonic_vector=V(d=5)
zeta=0.215
temp=20
fs=44100
Lambda = len(sonic_vector)
L_ = Lambda-1
speed = 331.3 + .606*temp

x1 = -10
x2 = 10
y1 = 5
y2 = 5
x = x1 + (x2 - x1)*n.arange(Lambda)/L_
y = y1 + (y2 - y1)*n.arange(Lambda)/L_

dl = n.sqrt( (x+zeta/2)**2 + y**2 )
dr = n.sqrt( (x-zeta/2)**2 + y**2 )

IID_al = 1/dl
IID_ar = 1/dr

# only with IID_a
TL = sonic_vector*IID_al
TR = n.copy(sonic_vector)*IID_ar

s = n.vstack(( TL, TR ))
WS(ADS(sonic_vector=s), filename="better_stereo.wav")


dl_ = (dl[1:] - dl[:-1])/speed
dr_ = (dr[1:] - dr[:-1])/speed
dl_ = -dl_
dr_ = -dr_

dl__ = n.cumsum(dl_*fs).astype(n.int)
dr__ = n.cumsum(dr_*fs).astype(n.int)

il = n.arange(Lambda)
ir = n.arange(Lambda) 
il[1:] += dl__
ir[1:] += dr__

il_ = il[il<Lambda]
ir_ = ir[ir<Lambda]

ITD = (dl-dr)/speed
Lambda_ITD = ITD*fs
if x1 > 0:
    TL = n.zeros(int(Lambda_ITD[0]))
    TR = n.array([])
else:
    TL = n.array([])
    TR = n.zeros(-int(Lambda_ITD[0]))

TL = n.hstack(( TL, (sonic_vector*IID_al)[il_], (sonic_vector*IID_al)[il_[-1]+1:]))
TR = n.hstack(( TR, (sonic_vector*IID_ar)[ir_], (sonic_vector*IID_ar)[ir_[-1]+1:]))

amax = max(len(TL), len(TR))
TL = n.hstack(( TL, n.zeros(amax - len(TL)) ))
TR = n.hstack(( TR, n.zeros(amax - len(TR)) ))
s2 = n.vstack(( TL, TR ))
WS(ADS(A=50,S=0, R=50, sonic_vector=s2), filename="better_stereo2.wav")

####################
# using a LUT to avoid downwsampling
# mono
f = 220*8
vs = fs*(dl[1:]-dl[:-1])
f_ = f*speed/(speed+vs)
dur = 5

tab = Tr
tab = n.array(tab)
nsamples = int(dur*fs)

samples = n.arange(nsamples)[:-1]
l = len(tab)

Gamma = (samples*f_*l/fs).astype(n.int)
s = tab[ Gamma % l ]
W(s, "dopplerLUT.wav")

####################
# using a LUT to avoid downwsampling
# stereo
dur = 5
f = 220*8
Lambda = int(fs*dur)
L_ = Lambda-1
x1, x2 = -10, 10
y1, y2 = 5, 5

x = x1 + (x2 - x1)*n.arange(Lambda)/L_
y = y1 + (y2 - y1)*n.arange(Lambda)/L_

dl = n.sqrt( (x+zeta/2)**2 + y**2 )
dr = n.sqrt( (x-zeta/2)**2 + y**2 )

IID_al = 1/dl
IID_ar = 1/dr

vsl = fs*(dl[1:]-dl[:-1])
vsr = fs*(dr[1:]-dr[:-1])
fl = f*speed/(speed+vsl)
fr = f*speed/(speed+vsr)

tab = Tr
tab = n.array(tab)

nsamples = int(Lambda-1)

samples = n.arange(nsamples)
l = len(tab)

Gamma = (samples*fl*l/fs).astype(n.int)
sl = tab[ Gamma % l ]*IID_al[:-1]

Gamma = (samples*fr*l/fs).astype(n.int)
sr = tab[ Gamma % l ]*IID_ar[:-1]

ITD0 = (dl[0]-dr[0])/speed
Lambda_ITD = ITD0*fs

if x1 > 0:
    TL = n.hstack(( n.zeros(int(Lambda_ITD)), sl ))
    TR = n.hstack(( sr, n.zeros(int(Lambda_ITD)) ))
else:
    TL = n.hstack(( sl, n.zeros(-int(Lambda_ITD)) ))
    TR = n.hstack(( n.zeros(-int(Lambda_ITD)), sr ))

s = n.vstack(( TL, TR ))

WS(s, "dopplerLUTstereo.wav")

