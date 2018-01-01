import sys, time
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c
H = M.H
T = M.tables.Basic()

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

def v(m,**kargs):
    return M.utils.V_(M.utils.midi2Hz(m), **kargs)
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

def J_(*args):
    i = 0
    s = []
    while i < len(args):
        a = args[i]
        b = args[i+1]
        if type(a) in (n.ndarray, list):
            if n.isscalar(b):
                s = J(s, a, d=b)
                i += 2
            else:
                s = J(s, a)
                i += 1
        else:
            i += 1
    return s
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

s_ = J(s_, s_4, d=-5)

## D.1.1
# Only one voice remains, maybe static or stops walking
# The voice starts to move to one side (right?) until it
# is completely on one channel.
# Then its timbre varies (it can be an AM)
# and it starts to move, and morph timbre.

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







