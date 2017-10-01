import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
W = fun.W
H = n.hstack
V = n.vstack
f_s = 44100

### standard values
# ADSR
A_ = 10.
D = 20.
S = -20.
R = 100.

# Tremolo:
fa = 2.
V_dB = 3.

# Vibrato:
fv = 6.
nu = .5

allV = [A_, D, S, R, fa, V_dB, fv, nu]

def note(interval=0, duration=2, base_freq=220, nvoices = 20, dev = 0.03, fs=44100):
    f = base_freq*2**(interval/12)
    allV_ = [f] + allV

    s = n.zeros(int(fs*duration))
    for voice in range(nvoices):
        p = allV_*n.random.normal(1,dev,9)
        sa = v(p[0], duration, fv=p[-2], nu=p[-1])
        sa = sa*A(p[-4], p[-3], duration)
        sa = adsr(sa, p[1], p[2], p[3], p[4])
        s += sa

    return s

### melodies, chords...
# melody
m1 = [0,   7, 8,   7, 11,   12, 0,    2, 0]
d1 = [1,   2, 1,   2, 1,    2, 1,     1, 3] 
s = H([note(i, j) for i,j in zip(m1, d1)])
W(s, "childChoir_.wav")

# chords
c1 = [0, 3, 7]
c2 = [7, 11, 2]
c2_ = [7, 11, 2,5]
c3 = [5, 8, 0]
dc = [2,   2, 1,   2, 1,    2, 1,     1, 3]
c =  [c1,  c2,c3,  c2,c2_,  c1,c3,    c2,c1]
def chord(intervals=[0, 4, 7], duration=2, base_freq=220, nvoices = 20, dev = 0.05):
    s = n.zeros(int(f_s*duration))
    for i in intervals:
      s += note(i, duration, base_freq, nvoices, dev)
    return s

s2 = H([chord(i, j, base_freq=220, dev=0.001) for i,j in zip(c, dc)])
W(s2, "childChoir_2.wav")

sh = H([note(i, j, base_freq=440, dev = 0.02) for i,j in zip(m1, d1)])
s_ = H( (n.zeros(f_s), sh))
mixed = s_*5+s2
final = H( (s*5, mixed) )
W(final, "childChoir_3.wav")
