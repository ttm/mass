import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c
H = M.utils.H
V_ = M.utils.V_
AD = M.utils.AD
F = M.utils.F
T = M.tables.Basic()
n_ = n

def ADV(note_dict={}, adsr_dict={}):
    return AD(sonic_vector=V_(**note_dict), **adsr_dict)

class Being:
    def __init__(self):
        rhythm = [1.] # repetition of one second
        rhythm2 = [1/2, 1/2] # repetition of one second
        rhythm3 = [1/3, 1/3, 1/3] # repetition of one second
        rhythm4 = [1/4, 1/4, 1/3] # repetition of one second

        # assume duration = 1 (be 1 second, minute or whatnot):
        rhythmic_spectrum = [ [1./i]*i for i in range(1,300) ]    

        # pitch or frequency sequences (to be used at will)
        f = 110
        freqs = [220]
        freq_spectrum = [i*f for i in range(1, 300)]
        neg_spec = [f/i for i in range(2,300)]
        
        freq_sym = [[f*2**((i*j)/12) for i in range(j)] for j in [2,3,4,6]]
        freq_sym_ = [[f*2**((i*j)/12) for i in range(300)] for j in [2,3,4,6]]

        dia = [2,2,1,2,2,2,1]
        notes_diatonic = [[dia[(j+i)%7] for i in range(7)] for j in range(7)]
        notes_diatonic_ = [sum(notes_diatonic[i]) for i in range(7)]
        freq_diatonic = [[f*2**( (12*i + notes_diatonic_[j])/12) for i in range(30)] for j in range(7)]

        intensity_octaves = [[10**((i*10)/(j*20)) for i in range(300)] for j in range(1,20)] # steps of 10db - 1/2 dB
        db0=10**(-120/20)
        intensity_spec = [[db0*i for i in j] for j in intensity_octaves]
        
        # diatonic noise, noises derived from the symmetric scales etc: one sinusoid or other basic waveform in each note.
        # Synth on the freq domain to optimize and simplify the process

        # make music of the spheres using ellipses and relations recalling gravity
        self.resources = locals()
        self.startBeing()

    def walk(self, n, method='straight'):
        # walk n steps up (n<0 => walk |n| steps down, n==0 => don't move, return []
        if method == 'straight':
            # ** TTM
            sequence = [self.grid[self.pointer + i] for i in range(n)]
            self.pointer += n
        elif method == 'low-high':
            sequence = [ self.grid[ self.pointer + i % (self.seqsize + 1) + i // self.seqsize ] for i in range(n*self.seqsize) ]
        elif method == 'perm-walk':
            # restore walk from 02peal
            pass
        self.addSeq(sequence)

    def setPar(self, par='f'):
        # set parameter to be developed in walks and stays
        if par == 'f':
            self.grid = self.fgrid
            self.pointer = self.fpointer

    def setSize(self, ss):
        self.seqsize = ss
    def setPerms(self, perms):
        self.perms = perms

    def stay(self, n, method='perm'):
        # stay somewhere for n notes (n<0 => stay for n cycles or n permutations)
        if method == 'straight':
            sequence = [self.grid[(self.pointer + i) % self.seqsize] for i in range(n)]
        elif method == 'perm':
            # ** TTM
            sequence = []
            if type(self.domain) != n_.ndarray:
                if not self.domain:
                    domain = self.grid[self.pointer : self.pointer + self.seqsize]
                else:
                    domain = n_.array(self.domain)
                    print("Implemented OK?? TTM")
            else:
                domain = self.domain
            # nel = self.perms[0].size  # should match self.seqsize ?
            count = 0
            while len(sequence) < n:
                perm = self.perms[count % len(self.perms)]
                seq = perm(domain)
                sequence.extend(seq)
                count += 1
            sequence = sequence[:n]
        self.addSeq(sequence)
        self.total_notes += n

    def addSeq(self, sequence):
        if type(self.__dict__[self.curseq]) == list:
            self.__dict__[self.curseq].extend(sequence)
        else:
            self.__dict__[self.curseq] = H(self.__dict__[self.curseq], sequence)

    def render(self, nn, fn=False):
        # Render nn notes of the Being!
        # Render with legatto, with V__ or whatever it is called
        self.mkArray()
        ii = n.arange(nn)
        d = self.d_[ii%len(self.d_)]*self.dscale
        f = self.f_[ii%len(self.f_)]
        tab = self.tab_[ii%len(self.tab_)]
        fv = self.fv_[ii%len(self.fv_)]
        nu = self.nu_[ii%len(self.nu_)]
        A = self.A_[ii%len(self.A_)]
        D = self.D_[ii%len(self.D_)]
        S = self.S_[ii%len(self.S_)]
        R = self.R_[ii%len(self.R_)]
        notes = [ADV({'f':ff, 'd':dd, 'fv':fvv, 'nu':nuu, 'tab': tabb}, {'A':AA, 'D': DD, 'S': SS, 'R':RR}) for ff,dd,fvv,nuu,tabb,AA,DD,SS,RR in zip(f, d, fv, nu, tab, A, D, S, R)]
        if fn:
            if type(fn) != str:
                fn = 'abeing.wav'
            if fn[-4:] != '.wav':
                fn += '.wav'
            M.utils.W(H(*notes), fn)
        else:
            return notes

    def startBeing(self):
        self.dscale = 1
        self.d_ = [1]
        self.f_ = [220]
        self.fv_ = [3]
        self.nu_ = [1]
        self.tab_ = [T.triangle]
        self.A_ = [20]
        self.D_ = [20]
        self.S_ = [-5]
        self.R_ = [50]
        self.mkArray()
        self.total_notes = 0

    def mkArray(self):
        self.d_  = n.array(self.d_ )
        self.f_  = n.array(self.f_ )
        self.fv_ = n.array(self.fv_)
        self.nu_ = n.array(self.nu_)
        self.tab_ = n.array(self.tab_)
        self.A_ =  n.array(self.A_) 
        self.D_ =  n.array(self.D_) 
        self.S_ =  n.array(self.S_) 
        self.R_ =  n.array(self.R_) 
    def howl(self):
        # some sound ressembing a toki pona mu, a grown or any other animal noise.
        pass
    def freeze(self):
        # a long sound/note with the parameters set into the being
        pass
    # use sequences of parameters to be iterated though with or without permutations.
    # use the fact that sequences of different sizes might yield longer cycles 
    
N = nsteps = 5
f1 = 220

ff = f1*2**(n.arange(N)/N)

from sympy.combinatorics import Permutation as P

# pr1 = P(range(N))  # anticlockwise
pr1 = P(list(range(1,N))+[0])
pr2 = P([N-1] + list(range(N-1)))  # clockwise

pr1_ = [pr1**i for i in range(N)]
pr2_ = [pr2**i for i in range(N)]
prF = [pr2**0 for i in range(N)]

pr1m = P(list(range(1,N-1))+[0])
pr2m = P([N-2] + list(range(N-2)))  # clockwise

pr1_m = [pr1m**i for i in range(N-1)]
pr2_m = [pr2m**i for i in range(N-1)]
prFm = [pr2m**0 for i in  range(N-1)]

D=.1

# each octave alternates emptiness and a circle
f_ = [55*2**(3/12)*2**i for i in range(8)]
f0_ = n.array(f_[::2])

# f__ = f0_*2**(n.arange(20)/20)
# f__ = n.array(n.matrix(f0_).T*2**(n.arange(20)/20))
f__ = f0_[:, None]*2**(n.arange(N)/N)

b = Being()
b.d_ = [D]
b.tab_ = [T.sine, T.saw, T.triangle, T.square]
b.tab_ = [T.square,T.saw]
b.fv_ = [2*i**3 for i in range(N)]
b.nu_ = [.5*i**3 for i in range(N)]
b.curseq = 'f_'

nnotes = N*N  # number of notes in the cycle: N perms, N freqs

b.perms = prF
b.f_ = []
b.domain = f__[0]
b.stay(nnotes)
c1 = H(*b.render(nnotes))




c1_ = H(*[c1]*5)

b.perms = pr2_
b.f_ = []
b.stay(nnotes)
c1A = H(*b.render(nnotes)) # anticlockwise
c1A_ = H(*[c1A]*5)


b.perms = pr1_
b.f_ = []
b.stay(nnotes)
c1C = H(*b.render(nnotes))  # clockwise
c1C_ = H(*[c1C]*5)

opening = H(c1_, c1A_, c1C_+c1_, c1C_)

# b.render(nnotes, "circle0.wav")

M.utils.W(opening, "circle0_.wav")

################
b.tab_ = [T.square,T.saw]
b.fv_ = [2*i**3 for i in range(N)]
b.nu_ = [.5*i**3 for i in range(N)]

b.tab_ = [T.square]
b.fv_ = [2*i for i in range(N)]
b.nu_ = [.5*i for i in range(N)]

pr_ = [prF, pr1_, pr2_]
f__Yes = [f__[i][::(-1)**i] for i in range(len(f__))]
c_ = []
for perm in pr_:
    b.perms = perm
    c_.append([])
    for ff in f__Yes:
        b.f_ = []
        b.domain = ff
        b.stay(nnotes)
        c1 = H(*b.render(nnotes))
        c_[-1].append(c1)

def r(a,n):
    """Repeat array a n times"""
    return H(*[a]*n)

# c_[i] is for repeat, cw or acw.
# c_[i][j] is the octave being played
# c_ binds each octave to a desc/asc order as f__Yes
opening = H(r(c_[0][0], 5),
            r(c_[2][0],5), 
            r(c_[1][0],5) + r(c_[0][0],5), 
            r(c_[1][0],5)
            )

C = n.array(c_)
op1 = H(
        sum([r(sv,5) for sv in C[0,:]]),
        sum([r(sv,5) for sv in C[2,:]]),
        sum([r(sv,5) for sv in C[0,:]+C[1,:]]),
        sum([r(sv,5) for sv in C[1,:]]),
        )


M.utils.W(H(opening, op1), "circle0b.wav")


b.tab_ = [T.square]
b.fv_ = [2*i for i in range(N)]
nu_ = [.5*i for i in range(N)]

b.tab_ = [T.square,T.saw]
b.fv_ = [2*i**7 for i in range(1,N-1)]
nu_ = [.5*i**4 for i in range(1,N)]

pr_ = [prF, pr1_, pr2_]
pr_m = [prFm, pr1_m, pr2_m]
f__Yes = [f__[i][::(-1)**i] for i in range(len(f__))]
c_X = []
for perm, perm_m in zip(pr_, pr_m):
    c_X.append([])
    for ff in f__Yes:
        b.perms = perm
        b.curseq = 'f_'
        b.f_ = []
        b.domain = ff
        b.stay(nnotes)
        b.perms = perm_m
        b.domain = nu_
        b.nu_ = []
        b.curseq = 'nu_'
        b.stay(nnotes)
        c1 = H(*b.render(nnotes))
        c_X[-1].append(c1)
CX = n.array(c_X)


dev1 = H(
        [sum([r(sv,3) for sv in CX[0,:1]]), sum([r(sv,3) for sv in CX[0,-1:]])],
        sum([r(sv,3) for sv in CX[2,1:3]]),
        [sum([r(sv,5) for sv in CX[:,0]]), sum([r(sv,5) for sv in CX[:,-1]])],
        [F(sonic_vector=sum([r(sv,5) for sv in CX[1,:]]),out=True), F(sonic_vector=sum([r(sv,5) for sv in CX[2,:]]), out=False)],
        )

s_ = H(opening, op1, dev1)
M.utils.WS(s_, "circle0c.wav")


N=25
D2 = .05
nnotes = N*N
cycle_duration = nnotes*D2
b2 = Being()
b2.A_ = [3]
b2.R_ = [3]
b2.S_ = [-4]
b2.D_ = [1]
b2.d_ = [D2]
b2.tab_ = [T.sine]
b2.fv_ = [0]
b2.nu_ = [0]
b2.curseq = 'f_'
b2.f_ = []

nnotes = N*N  # number of notes in the cycle: N perms, N freqs

# pr1 = P(range(N))  # anticlockwise
pr120 = P(list(range(1,N))+[0])
pr220 = P([N-1] + list(range(N-1)))  # clockwise

pr1_20 = [pr120**i for i in range(N)]
pr2_20 = [pr220**i for i in range(N)]
prF20 = [pr220**0 for i in range(N)]

pr1m20 = P(list(range(1,N-1))+[0])
pr2m20 = P([N-2] + list(range(N-2)))  # clockwise

pr1_m20 = [pr1m20**i for i in range(N-1)]
pr2_m20 = [pr2m20**i for i in range(N-1)]
prFm20 = [pr2m20**0 for i in  range(N-1)]

b2.perms = [i**11 for i in pr2_20]

f_ = 55*2**(n.arange(N)/(N/4)) # three octaves each N

nnotes = N*N

b2.fv_=n.linspace(0,3500, int(N*2.3))
b2.nu_=n.linspace(0,35, int(N*7))
b2.domain = f_
b2.curseq = 'f_'
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.square]
cc = H(*b2.render(nnotes))

b2.domain = f_[::-1]*4**2
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.saw]
cc2 = H(*b2.render(nnotes))

N=100
nnotes=N*N
D2 = .1
b2.fv_=n.linspace(0,3500, N*2)
b2.nu_=n.linspace(0,35, N*N)

pr120 = P(list(range(1,N))+[0])
pr220 = P([N-1] + list(range(N-1)))  # clockwise

pr1_20 = [pr120**i for i in range(N)]
pr2_20 = [pr220**i for i in range(N)]
prF20 = [pr220**0 for i in range(N)]

pr1m20 = P(list(range(1,N-1))+[0])
pr2m20 = P([N-2] + list(range(N-2)))  # clockwise

pr1_m20 = [pr1m20**i for i in range(N-1)]
pr2_m20 = [pr2m20**i for i in range(N-1)]
prFm20 = [pr2m20**0 for i in  range(N-1)]

b2.perms = [i**7 for i in pr1_20]


f_ = 55*2**(n.arange(N)/(N/6)) # three octaves each N
b2.domain = f_
b2.curseq = 'f_'
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.sine]
cc_ = H(*b2.render(nnotes))

b2.domain = f_[::-1]*4**2
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.square]
cc2_ = H(*b2.render(nnotes))
cc_ = AD(sonic_vector=cc_[len(cc_)/2:])
cc2_ = AD(sonic_vector=cc2_[len(cc2_)/2:])

nnotes = N*6
l=list(range(N))
ref = P(l[len(l)//2:][::-1] + l[:len(l)//2][::-1])
ref_ = [ref**2, ref]

b2.perms = ref_
b2.domain = f_*2
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.saw]
cc_M = H(*b2.render(nnotes))

b2.domain = f_[::-1]*4
b2.f_ = []
b2.stay(nnotes)
b2.tab_ = [T.triangle]
cc2_M = H(*b2.render(nnotes))



def a(sv):
    return AD(sonic_vector=sv)
ss = H(
    (cc*.6+a(cc2_[:len(cc)]), cc2*.6+cc_[:len(cc)]),
    (cc2_[len(cc):len(cc)+len(cc_M)] + cc_M, cc_[len(cc):len(cc)+len(cc_M)] + cc2_M),
    )

s_ = H(s_, ss)
M.utils.WS(s_, "circled.wav")

M.utils.WS(ss, "circlec.wav")
