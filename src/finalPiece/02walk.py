import sys, time
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c
H = M.H
T = M.tables.Basic()
fs = 44100

scale = s = n.array([0,2,4,5,7,9,11])
scale_grid = sg = H(*[s+12*i for i in range(12)])
scale_ = [2,2,1,2,2,2,1]
scale_grid_b = [0] + scale_*12
scale_grid_ = n.cumsum(scale_grid_b)

# value of 69 is 440Hz, A4, 60 in C4
# f = M.utils.midi2Hz(scale[i])

# both scale_grid and scale_grid_ are grids for
# the C major scale, represented by
# sequences of midi nodes which starts from
# C-1 = 0 to beyond our hearing (20kHz ~ 135 midi note, Eb10).

pivots = [7*i for i in range(3,8)]
pivots_m = [scale_grid[i] for i in pivots]
pivots_f = [M.utils.midi2Hz(i) for i in pivots_m]

peal2 = M.structures.symmetry.PlainChanges(2)
peal3 = M.structures.symmetry.PlainChanges(3)
peal4 = M.structures.symmetry.PlainChanges(4)
peal5 = M.structures.symmetry.PlainChanges(5)
t = time.time()
peal6 = M.structures.symmetry.PlainChanges(6,4)
print(time.time()-t); t = time.time()
peal7 = M.structures.symmetry.PlainChanges(7,5)
print(time.time()-t); t = time.time()
# takes too long, maybe save as a pickle file:
# peal12 = M.structures.symmetry.PlainChanges(12,10)
# If only part of interesting permutations are intended,
# one might also do:
# >>> R = M.structures.permutations.InterestingPermutations
# >>> R.nelements=12
# >>> R.method='dimino'
# >>> R.getRotations()
# >>> R.getRotations(R)
# >>> R.rotations
# which is very fast


def walk(p1=57, p2=0, scale_grid=scale_grid, perms=peal3.peal_direct, method='swap', step=1, domain=None):
    """
    """
    foo = [abs(i-p1) for i in scale_grid]
    m = min(foo)
    p1_ = foo.index(m)
    if p2:
        print('needs to calculate step, not implemented')
        return
    else:
        foo = [abs(i-p2) for i in scale_grid]
        m = min(foo)
        p2_ = foo.index(m)
    nel = perms[0].size
    if not domain:
        domain = list(range(nel))
    values = []
    for perm in perms:
        values.append(perm(domain))
    # make the walk
    values_ = []
    if step >= 0:
        pointer = nel -1 + step
    else:
        pointer = step
    swap = False
    domain_ = domain[:]
    for perm in perms:
        if swap:
            if step >= 0:
                domain_[domain_.index(min(domain_))] = pointer
            else:
                domain_[domain_.index(max(domain_))] = pointer
            v_ = perm(domain_)
            pointer += step
        else:
            v_ = domain_[:]
            swap = True
        values_.append(v_)
    values__ = []
    values_m = []
    values_f = []
    for v in values_:
        v_ = [i+p1_ for i in v]
        v_ = [i for i in v_ if abs(i)<len(scale_grid)]
        v_m = [scale_grid[i] for i in v_]
        v_f = [M.utils.midi2Hz(i) for i in v_m]
        values__.append(v_)
        values_m.append(v_m)
        values_f.append(v_f)
    return locals()

def walk2(p1=57, p2=0, scale_grid=scale_grid, perms=peal3.peal_direct, method='swap', step=1, domain=None, rhy=[.5], tabs=[T.triangle]):
    d = locals().copy()
    del d['rhy'], d['tabs']
    values_m = H(*walk(**d)['values_m'])
    samples = H(*v__(values_m, d_=rhy, t_=tabs))
    return samples

    
# sequence = walk(pivot[0],pivot[-1],scale_grid, peal6)
# sequence = walk(pivots[0], 0, scale_grid, peal3.peal_direct)
# sequence should have all the notes in the peal,
# starting at p1, ending at p2, walking on the sg
# it might climb from p1 replacing:
# 1) the lowest bell with the highest or vice-versa
# 2) with all the notes might being shifted one unit per peal row

# match the number of elements in the peal with the symmetric scales:
# p3 -> 3M/4, p2 -> 4A/6, p4 -> 3m/3, p6 -> 2M/2, p12 -> 2m/1

s6 = n.arange(0,12,6)
sg6 = H(*[s6+12*i for i in range(12)])
s4 = n.arange(0,12,4)
sg4 = H(*[s4+12*i for i in range(12)])
s3 = n.arange(0,12,3)
sg3 = H(*[s3+12*i for i in range(12)])
s2 = n.arange(0,12,2)
sg2 = H(*[s2+12*i for i in range(12)])

# use exotic scales, such as with 2A/3,
# messiaen's modes, or favourites
t = time.time()
seq7 = walk(pivots_m[0], 0, scale_grid, peal7.peal_direct*3)
seq6 = walk(pivots_m[-1], 0, sg6, peal2.peal_direct*3,step=-1, domain=[1,0])
seq4 = walk(pivots_m[1], 0, sg4, peal3.peal_direct*3)
seq3 = walk(pivots_m[-2], 0, sg3, peal4.peal_direct*3,step=-1, domain=[3,2,1,0])
seq2 = walk(pivots_m[2], 0, sg2, peal6.peal_direct*3)
print(time.time()-t); t = time.time()
# seq1 takes too long because of peal12 (pickle it?)
seq7_ = H(*seq7['values_m'])
seq6_ = H(*seq6['values_m'])
seq4_ = H(*seq4['values_m'])
seq3_ = H(*seq3['values_m'])
seq2_ = H(*seq2['values_m'])


# still, no permutation, only swapping of highest and lowest
sti7 = walk(pivots_m[0], 0, scale_grid, [peal7.peal_direct[0]]*25)
sti6 = walk(pivots_m[-1], 0, sg6, [peal2.peal_direct[0]]*25, step=-1, domain=[1,0])
sti4 = walk(pivots_m[1], 0, sg4, [peal3.peal_direct[0]]*25)
sti3 = walk(pivots_m[-2], 0, sg3, [peal4.peal_direct[0]]*25,step=-1, domain=[3,2,1,0])
sti2 = walk(pivots_m[2], 0, sg2, [peal6.peal_direct[0]]*25)

sti7_ = H(*sti7['values_m'])
sti6_ = H(*sti6['values_m'])
sti4_ = H(*sti4['values_m'])
sti3_ = H(*sti3['values_m'])
sti2_ = H(*sti2['values_m'])

D = M.utils.AD
def v(m,**kargs):
    return D(sonic_vector=M.utils.V_(M.utils.midi2Hz(m), **kargs), R=30)
def v_(m_, size=36, **kargs):
    return [v(m, **kargs) for m in m_[:size]]
def v__(m_, d_, t_, size=36, **kargs):  # used only in a further section
    if len(m_) < size:
        size = len(m_)
    nrep = 1+int(size/len(d_))
    d__ = d_ * nrep
    nrept = 1+int(size/len(t_))
    t__ = t_ * nrept
    return [v(m, d=d, tab=t, **kargs) for m,d,t in zip(m_[:size],d__[:size],t__[:size])]

# s = v_(seq2_, d=1) 
seq_ = [seq7_, seq6_, seq4_, seq3_, seq2_,
        sti7_, sti6_, sti4_, sti3_, sti2_]

print('mark: ', time.time()-t); t = time.time()
s01_ = [H(*v_(i, d=.1)) for i in seq_]
s0125_ = [H(*v_(i, d=.125)) for i in seq_]
s025_ = [H(*v_(i, d=.25)) for i in seq_]
s05_ = [H(*v_(i, d=.5)) for i in seq_]
print('mark: ', time.time()-t); t = time.time()
s1_ = [H(*v_(i[:36], d=1.)) for i in seq_]
print('mark: ', time.time()-t); t = time.time()

# seq_[n] and sXX_[n] hold walks with n notes
  
J = M.utils.J
### Opening:
s_ = J(s1_[1], s0125_[4], d=7)

### Exposition of the material
# walks, all mono,
# all with the same timbre
# all perfectly matched the symmetric scale with the peal size
# all using the cannonic peal
# all with unitary step
# all with equivalent duration and within the same 1s binary grid
# exception for s01_ which is a division of 1s in 2*5
s1 = s01_[3]+s01_[4]
s1_ = s01_[3][::-1]+s01_[4][::-1]
s1__ = H(s1, s1_, s1)

s2 = J(s05_[1], s0125_[4])

s_ = H(s_, J(s1__, s2))

### Development
# introduction of the interesting permutation groups
# explorar caminhar stereo, efeito doppler, hrtf
# timbres, ritmos, escalas, passos, tamanhos dos peals e sequencias
# maintain the theme: mixing scales and peals in walking patterns

## D.0
# a rotation group starts low and slow and rises
# three static rotation groups start on the treble
# after a while, each one walks on the frequency and desapears
ip = []
for i in [2,3,4,6]:
    locals()['i'+str(i)]=M.structures.symmetry.InterestingPermutations(i)
# iX has X elements
# i4 = M.structures.symmetry.InterestingPermutations(4)
r1 = walk(pivots_m[0], 0, sg3 ,i4.rotations*9)  # maybe fade it in and out
r1_ = H(*r1['values_m'])
s_2 = H(*v_(r1_, d=.1, tab=T.saw))

treble_m = pivots_m[-3:]
ds = .1,.125,.25,.5,1
tabs = T.sine, T.triangle, T.square
perms = [i4.rotations*15, i3.dihedral*9, i6.mirrors*9]
scale_grids = [sg4, sg3, sg2]
count = 0
trebles = []
for t in treble_m:
    t1 = walk(t, 0, scale_grids[count], perms[count], step=0)
    t1_m = H(*t1['values_m'])
    t_ = H(*v_(t1_m, d=ds[count], tab=tabs[count]))
    trebles.append(t_)
    count += 1
# s_2_ = J(J(trebles[0], trebles[1]), trebles[2])
s_2_ = trebles[0][:44100*3] + trebles[1][:44100*3] + trebles[2][:44100*3]

count = 0
steps = 1, -2, 7
trebles_ = []
for t in treble_m:
    t1 = walk(t, 0, scale_grids[count], perms[count], step=steps[count])
    t1_m = H(*t1['values_m'])
    t_ = H(*v_(t1_m, d=ds[count], tab=tabs[count]))
    trebles_.append(t_)
    count += 1
s_2__ = trebles_[0][:44100*3] + trebles_[1][:44100*3] + trebles_[2][:44100*3]

s_2_c = H(s_2_, s_2_, s_2__)
s_2_c[-44100*4:] *= M.utils.F(d=4, method='lin')

s_ = H(s_, J(s_2, s_2_c, d=7))


## D.0.1
# one of them comes back with a rhythm
# the rhythm is varied in many voices
rhy = [.5,.25,.25]
rhy_ = [.5]+[1/(4*3)]*3
rhy__ = [2/3]+[1/(3*2)]*2

rhy2 = [i/2 for i in rhy]
count=0
s_3 = walk(treble_m[0], 0, scale_grids[count], perms[count], step=0)
s_3_m = H(*s_3['values_m'])
s_3 = H(*v__(s_3_m, d_=rhy, t_=[tabs[count]]))
# s_3B = s_3.copy()

s_3[:44100*8] *= M.utils.F(d=8, method='lin', out=False)

s_3_ = walk2(treble_m[0], 0, scale_grids[count], perms[count], step=steps[count],rhy=rhy)

s_3__ = walk2(treble_m[-1]+7, 0, scale_grids[count], perms[count], step=0,rhy=rhy2)

s_3___ = walk2(pivots_m[1], 0, sg2, perms[count], step=2, rhy=rhy__)

s_3____ = walk2(pivots_m[3], 0, sg2, perms[1], step=2, rhy=rhy_[::-1], tabs=[T.sine])

J_ = M.utils.J_
s_3_c = J_(s_3, 0,
           s_3_, 5,
           s_3__, 8,
           s_3___, 9,
           s_3____, 11)

s_ = H(s_, s_3_c)

## D.1
# the timbre starts to toggle in all the patterns at the same time
# at the same time, various timbre qualities are spread in the voices
s_4_ = s_3_c
A = M.utils.AM
D = M.utils.AD
s_4_[3*44100:4*44100] *= D(d=1, S=0)*A(d=1)
s_4_[6*44100:7.5*44100] *= D(d=1.5, S=0)*A(d=1.5, fm=150)
s_4_[10*44100:12*44100] *= D(d=2, S=0)*A(d=2, fm=350,a=.7)
s_4__ = [A(sonic_vector=s_3___),
        A(sonic_vector=s_3____,fm=150),
        A(sonic_vector=s_3__,fm=350, a=.7),
        A(sonic_vector=s_3_,fm=20),
        A(sonic_vector=s0125_[2],fm=150),
        A(sonic_vector=s01_[-2],fm=70),
        A(sonic_vector=s0125_[4],fm=22, a=.9),
        ]
s_4___ = []
for s in s_4__:
    s_4___ = J(s_4___, s)
s_4 = H(s_4_, s_4___)

s_ = J(s_, s_4*.01, d=-5)

## D.1.1
# Only one voice remains, maybe static or stops walking
# The voice starts to move to one side (right?) until it
# is completely on one channel.
# Then its timbre varies (it can be an AM)
# and it starts to move, and morph timbre.
s_5_ = A(sonic_vector=s_3____,fm=150)
s_5__ = s_3____
s_5___ = s_5_+s_5__

L_ = M.utils.L_
fade0 = L_(d=[6.75], dev=[0], method=['lin'])

s_5____ = n.array(( s_5___*fade0, s_5___*(1-fade0) ))
s_ = J_(s_,0, s_5___,-6.75, s_5____,-6.75)

fade1 = L_(nsamples=[len(s_5_)],
    dev=[-80, 0], method=['lin']*2)
s_5 = s_5_*fade1 + s_5__*(1-fade1)
s_5b = n.array(( n.zeros(s_5.shape[0]), s_5 ))
s_ = H(s_, s_5b*3)

M.utils.WS(s_, '02walk_foo.wav')

s6 = n.zeros(2*fs)
s6_ = walk2(pivots_m[-2], 0, scale_grid=sg2, perms=i6.rotations, step=0, rhy=[.15])
s6 = H(s6, s6_)

perms = i6.rotations
step = 2
s6__ = walk2(pivots_m[-2], 0, scale_grid=sg2, perms=perms, step=step, rhy=[.12])
center = step*len(perms)/2
step = 6
perms = i2.rotations
s6___ = walk2(pivots_m[-2]+center, 0, scale_grid=sg6, perms=perms, step=step, rhy=[.5])
center2 = step*len(perms)/2
perms = i6.rotations
step = -2
s6____ = walk2(pivots_m[-2]+center+center2, 0, scale_grid=sg2, perms=perms, step=step, rhy=[.1])

center3 = step*len(perms)/2
perms = i6.rotations
step = 0
s6_____ = walk2(pivots_m[-2]+center+center2+center3, 0, scale_grid=sg2, perms=perms, step=step, rhy=[.1])
s6______ = walk2(pivots_m[-2]+center+center2+center3, 0, scale_grid=sg2, perms=perms, step=step, rhy=[.1*(i+1) for i in range(5)])
s6_______ = walk2(pivots_m[-2]+center+center2+center3, 0, scale_grid=scale_grid, perms=perms, step=step, rhy=[.1*(i+1) for i in range(5)])

step = 2
s6________ = walk2(pivots_m[-2]+center+center2+center3, 0, scale_grid=scale_grid, perms=perms, step=step, rhy=[.7+.12*(i) for i in range(5)])
center4 = step*len(perms)/2
s6 = H(s6, s6__, s6___, s6____,
        s6_____, s6______, s6________, s6________)
s_ = H(s_, s6)

center = pivots_m[-2]+center+center2+center3+center4
# P = M.utils.panTransitions
step = 3
s7 = walk2(center, 0, scale_grid=sg3, perms=perms, step=step, rhy=[.15])
s7M = walk2(center, 0, scale_grid=scale_grid, perms=perms, step=0, rhy=[.15])

s7I = walk2(center+24, 0, scale_grid=sg3, perms=perms, step=-step, rhy=[.15])
s7MI = walk2(center+24, 0, scale_grid=scale_grid, perms=perms, step=0, rhy=[.15])
# s7 transitions to the left channel
# stops again in major scale
# transitions from left to right
# with same scale but oposite step
# all mix with AM and/or tremolo
s7_ = n.array(( n.zeros(len(s7M)), s7M ))
P = M.utils.panTransitions
pantrans = P(p=[(0, 1), (1, 0)], d=[4], method=['lin'], fs=fs)
s7__ = J(s7, pantrans)[:44100*4]
s7___ = n.array(( s7M, n.zeros(len(s7M)) ))
s7b = H( s7_, s7__, s7___ )

s_ = H(s_, s7b)

# silence,
# two almost equal deep and heavy
# sequences of 1 tempo
# is repeated several times
# while s7 transits back and forth
pantrans2 = P(p=[(0, 1), (1, 0), (0, 1)], d=[1,1], method=['lin'], fs=fs)
s8 = J(s7, pantrans2)
s8M = J(s7M, pantrans2)
s8I = J(s7I, pantrans2)
s8MI = J(s7MI, pantrans2)



s8[ :, 3*fs:4*fs] = s8M[ :, 3*fs:4*fs]
s8[ :, 6*fs:7*fs] = s8M[ :, 6*fs:7*fs]
s8I[:, 3*fs:4*fs] = s8MI[:, 3*fs:4*fs]
s8I[:, 6*fs:7*fs] = s8MI[:, 6*fs:7*fs]

for i in range(s8.shape[1]//(3*fs)):
    s8[ :, i*3*fs:(i*3+1)*fs] = s8M[ :, i*3*fs:(i*3+1)*fs]
    s8I[:, i*3*fs:(i*3+1)*fs] = s8MI[:, i*3*fs:(i*3+1)*fs]

for i in range(s8.shape[1]//fs):
    if (i+1)%2:
        s8[:, i*fs:(i+1)*fs] = s8I[:, i*fs:(i+1)*fs] 



# deep and heavy: slow pattens around bass notes.
# this center-note synthesis might be used to make 
# melodies and other patterns

# 20 notes around and including 110Hz, A2, spaced by 10 cents
scale_bass1 = [110*2**((i/12)/10) for i in range(-10,10)]
# Ab minor triad of seconds 2m, 2M, 
minor_triad_2 = scale_bass2 = [220*2**((i/12)/10) for i in (-1,0,2)]
major_triad_2 = scale_bass3 = [330*2**((i/12)/10) for i in (-2,0,1)]
dim_triad_2 = scale_bass4 = [110*2**((i/12)/10) for i in (-1,0,1)]
aum_triad_2 = scale_bass5 = [2*880*2**((i/12)/10) for i in (-2,0,2)]

sb1 = [i/10-.5 for i in range(10)]
smt2 = [-1,0,2]
sMt2 = [-2,0,1]
sdt2 = [-1,0,1]
sAt2 = [-2,0,2]

T2 = [
      sb1,
      smt2,
      sMt2,
      sdt2,
      sAt2,
     ]
pivs = [pivots[i] for i in (0,1,2,0,-1)]
p=.5
rs = [  (p,),
        (p/4, p/2, p/4),
        (p/2, p/4, p/4),
        (p/4, p/4, p/2),
        (p/4, p/4, p/4, p/4)
     ]
ss = [1,3,4,2,1]
s8_ = []
A = n.array
for t2, piv, r, s in zip(T2, pivs, rs, ss):
    # make grid
    grid = H(*[A(t2)+12*i for i in range(12)])
    # make walk with walk and walk2
    s8__ = walk2(piv, 0, scale_grid=grid, perms=peal5.peal_direct, step=s, rhy=r)
    s8_.append(s8__)

s8___ = H(*s8_)
env = D(d=.5)

i = 0
while i*fs < len(s8):
    s8[:, i*fs:(i+.5)*fs] += s8___[i*fs:(i+.5)*fs]*env
    i += 1

s_ = H(s_, s8)

# silence,
# same pattern but varied
# mix with
# glissandi and walks,
# that fall from here to there and from treble to bass
silence = n.zeros(fs*2)

pantrans2 = P(p=[(0, 1), (1, 0), (0, 1)], d=[1,1], method=['lin'], fs=fs)
s9 = s7      # moves up
s9M = s7M    # static bottom
s9I = s7I    # moves down
s9MI = s7MI  # static top

s9_ = walk2(center, 0, scale_grid=sg3, perms=perms, step=0, rhy=[.15])
s9_M = walk2(center, 0, scale_grid=scale_grid, perms=perms, step=3, rhy=[.15])

s9_I = walk2(center+24, 0, scale_grid=sg3, perms=perms, step=-0, rhy=[.15])
s9_MI = walk2(center+24, 0, scale_grid=scale_grid, perms=perms, step=-3, rhy=[.15])

r =  D(d=1)*n.array(( n.zeros(fs), n.ones(fs) ))
l =  D(d=1)*n.array(( n.ones(fs), n.zeros(fs) ))
rl = D(d=1)*pantrans2[:, -fs:]                     
lr = D(d=1)*pantrans2[:, :fs]                      

s9y = H(s9[:fs]*r,
        s9_I[fs*1:fs*2]*rl,
         s9I[fs*2:fs*3]*l,
         s9_[fs*3:fs*4]*lr)

s9y_ = H(s9_MI[:fs]*l,
        s9M[fs*1:fs*2]*lr,
         s9_M[fs*2:fs*3]*r,
         s9MI[fs*3:fs*4]*rl)

s9y__ = H(
         s9MI[fs*0:fs*1]*lr,
        s9_MI[fs*1:fs*2]*r,
        s9M[fs*2:fs*3]*rl,
         s9_M[fs*3:fs*4]*l,
         )

s9yy = H(s9y, s9y+s9y_, s9y+s9y_, s9y__, s9y__)
s9 = s9yy

# s9[3*fs:4*fs] = s9M[3*fs:4*fs]
# s9[6*fs:7*fs] = s9M[6*fs:7*fs]
# s9I[3*fs:4*fs] = s9MI[3*fs:4*fs]
# s9I[6*fs:7*fs] = s9MI[6*fs:7*fs]

for i in range(s9.shape[1]//(3*fs)):
    indices = n.arange(i*3*fs,(i*3+1)*fs)
    ii = indices % len(s9M)
    s9[ :, i*3*fs:(i*3+1)*fs] =  s9M[ii]
    s9I[i*3*fs:(i*3+1)*fs] = s9MI[i*3*fs:(i*3+1)*fs]

for i in range(s9.shape[1]//fs):
    if (i+1)%2:
        indices = n.arange(i*fs, (i+1)*fs)
        ii = indices % len(s9I)
        s9[:, i*fs:(i+1)*fs] = s9I[ii] 


rs = [  (p,),
        (p/6, p/6, p/2, p/6),
        (p/2, p/6, p/6, p/6),
        (p/6, p/6, p/6, p/2),
        (p/6, p/6, p/6, p/6, p/6, p/6)
     ]
ss = [1,3,4,2,1]
s9_ = []
tabs = [T.square, T.triangle, T.sine, T.sine, T.saw]
for t2, piv, r, s in zip(T2, pivs, rs, ss):
    # make grid
    grid = H(*[A(t2)+12*i for i in range(12)])
    # make walk with walk and walk2
    s9__ = walk2(piv, 0, scale_grid=grid, perms=peal5.peal_direct, tabs=tabs,  step=s, rhy=r)
    s9_.append(s9__)

s9___ = H(*s9_)
env = D(d=.5)

i=0
while i*fs < s9.shape[1]:
    indices = n.arange(i*fs, (i+.5)*fs)
    ii = indices % len(s9I)
    s9[:, i*fs:(i+.5)*fs] += s9___[i*fs:(i+.5)*fs]*env
    i += 1


# 5 glissandi of 2s
ff = [
        (pivots_f[-1], pivots_f[0]),
        (pivots_f[-2], pivots_f[1]),
        (pivots_f[-1], pivots_f[1]),
        (pivots_f[-2], pivots_f[0]),
        (pivots_f[-1], pivots_f[-2]),
     ]

fv = [2,4,8,16,1]
nu = [8,4,2,1,16]
tab = [T.sine, T.triangle, T.square, T.saw, T.sine]

gs = []
for ff_, fv_, nu_, tab_ in zip(ff,fv,nu,tab):
    gg = M.utils.PV(ff_[0], ff_[1], d=2, fv=fv_,
            nu=nu_)
    gs.append(gg)

s9 = M.utils.mix2([s9]+gs, offset=[0,0,4,5, 11,16])


s_ = H(s_, silence, s9)
M.utils.WS(s_, '02walk_foo2.wav')
# def L_(d=[2,4,2], dev=[5,-10,20], alpha=[1,.5, 20], method=["exp", "exp", "exp"],
#         nsamples=0, sonic_vector=0, fs=44100):



## D.1.2
# while the voice goes on on solo
# other voices start at positions given by HRTF
# some resemble the solo, the walking patterns or a mix

## D.2
# rhythm entangles with the spatialization
# reverb starts to get used here and there

## D.2.1
# scales are explored

## D.2.2
# scales and patterns are used very closely related
# to create an undivisible pattern
# these patterns are used in poliphony with each other.

## D.3
# Use all at will to the glory
# Explore Doppler Effect, explore noises

## D.3.1
# a more well behaved reexposition
# mix material from the Exposition with the development

### Coda
# maybe finish with a solo voice walking around
# and in different rhythms, in positions, scales, timbres
# that ends up stuck in a left-right, up-down, far-close
# trajectory in space, in a fixed peal, a fixed scale,
# a fixed walking pattern (which note gets shifted to which note:
# lowest to highest, first in peal to highest,
# all notes one step up, random note one step up,
# all notes random step up or down,
# bottom X notes to highest notes (gallop),
# spreading each subsequent dimension/pitch/loudness in one direction
# over and over again or back and forth.
# Walk might imply in a note or a cluster/range being played.
# Might imply hiccup dynamics, such as alternating
# a stable higher or lower note with an ascending or
# descending trajectory.
# Walks benefit from any function or sequence of values,
# such as catalogued [MASS].
# 
# 
# ), a fixed rhythm.
# little by little comes to this stable form,
# and then fades out when completely stable.






# make the line walk realy
# start with only sg2

# the voice on the left stops
# it starts again in sg2, rotating fast but not walking
# step is the interval with the walking
# just change d=.5, d=1,