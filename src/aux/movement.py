import numpy as n
# from scipy.io import wavfile as w
import imp
fun = imp.load_source("functions","./functions.py")
for i in dir(fun):
    locals()[i] = eval("fun."+i)

sonic_vector=V(d=5)
theta1=180
theta2=0
dist1=.1
dist2=.1
zeta=0.215
temp=20
fs=44100

theta1_ = 2*n.pi*theta1/360
x1 = n.cos(theta1_)*dist1
y1 = n.sin(theta1_)*dist1
theta2_ = 2*n.pi*theta2/360
x2 = n.cos(theta2_)*dist2
y2 = n.sin(theta2_)*dist2
speed = 331.3 + .606*temp

Lambda = len(sonic_vector)
L_ = Lambda-1
xpos = x1 + (x2 - x1)*n.arange(Lambda)/L_
ypos = y1 + (y2 - y1)*n.arange(Lambda)/L_
dl = n.sqrt( (xpos+zeta/2)**2 + ypos**2 )
dr = n.sqrt( (xpos-zeta/2)**2 + ypos**2 )

# IID_a = d/d2
# IID_a2 = 1/IID_a
IID_al = 1/dl
IID_ar = 1/dr

# only with IID_a
TL = sonic_vector*IID_al
TR = n.copy(sonic_vector)*IID_ar

s = n.vstack(( TL, TR ))
WS(ADS(sonic_vector=s))

ITD = (dl-dr)/speed
Lambda_ITD = ITD*fs

if x1 > 0:
    TL = n.zeros(int(Lambda_ITD[0]))
    TR = n.array([])
else:
    TL = n.array([])
    TR = n.zeros(-int(Lambda_ITD[0]))

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

TL = n.hstack(( TL, (sonic_vector*IID_al)[il_], (sonic_vector*IID_al)[il_[-1]+1:]))
TR = n.hstack(( TR, (sonic_vector*IID_ar)[ir_], (sonic_vector*IID_ar)[ir_[-1]+1:]))

amax = max(len(TL), len(TR))
TL = n.hstack(( TL, n.zeros(amax - len(TL)) ))
TR = n.hstack(( TR, n.zeros(amax - len(TR)) ))
s2 = n.vstack(( TL, TR ))
WS(s2)




#############################
# constant radius, linear change of theta
dist = .05
theta1_ = 2*n.pi*theta1/360
theta2_ = 2*n.pi*theta2/360
theta = theta1_ + (theta2_ - theta1_)*n.arange(Lambda)/L_
x = n.cos(theta)*dist
y = n.sin(theta)*dist

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
dl_ = dl_
dr_ = dr_

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
WS(ADS(A=50, R=50, sonic_vector=s2), filename="better_stereo2.wav")

#############################
# varying radius, linear change of theta
# dist1 = .05
# dist2 = .05
# dist = dist1 + (dist2 - dist1)*n.arange(Lambda)/L_
# theta1 = 2*n.pi*theta1/360
# theta2 = 2*n.pi*theta2/360
# theta = theta1 + (theta2 - theta1)*n.arange(Lambda)/L_
# x = n.cos(theta)*dist
# y = n.sin(theta)*dist
x1 = -100
x2 = 100
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
