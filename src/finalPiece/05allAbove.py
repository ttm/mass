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
ADS = M.utils.ADS
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
    
# make 1 long sound.
# it morphs into the fv=100 and back
# uses also tremolo.
# after a while, divides two voices in stereo with oscilating fv, fa, nu and db
# after a while, also f and slower vibratos are divided in the voices.

# stops.
# enters bbperm

# bp=Being() # simple for permutation
# #bp.perms = M.structures.peals.PlainChanges(3).peal_direct
# # bp.f_ = [200, 200*2**(4/12), 200*2**(8/12)]
# # bp.domain = [1, 2, 3]
# #bp.domain = [200, 200*2**(4/12), 200*2**(8/12)]
# bp.f_ = [200]
# bp.fv_ = [3,10,100]
# bp.d_ = [1/4, 1/4, 1/2]
# bp.curseq = 'f_'
# bp.stay(21)
# bp.render(21, 'permBaby.wav')
# tr1 = bp.render(21)

s = M.utils.PV_
t = M.utils.T_
l = M.utils.L_
Tr = T.triangle
S = T.sine

ss = s(f=[220, 440, 330], d=[[2,3],[2,5], [2,5,6,1]],
      fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]],
      alpha=[[1, 1] , [1, 1], [1, 1, 1, 1]],
      tab=[[Tr,Tr], [S,Tr,S], [S,S,S,S,S]], nsamples=0, fs=44100)

M.utils.W(ss,'metav.wav')

f = [200,200.]
d = [[30],[3.]]
fv = [[0, 200.]]
nu = [[0,10.]]
alpha = [[1],[1]]
tab = [[Tr],[S]]
ss2 = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss2,'metav0.wav')



f = [300,200.]
d = [[30],[1.,4]]
fv = [[10, 20]]
nu = [[10,10]]
alpha = [[1],[1,1]]
tab = [[Tr],[S,S]]
ss2 = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss2,'test.wav')


############ 
# second strategy: make both sounds and crossfade them

f = [200,4000.]
d = [[60],[60]]
fv = [[.05]]
nu = [[5]]
alpha = [[1],[1]]
tab = [[Tr],[S]]
ss = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss,'s200.wav')

f = [203.,4030.]*2
d = [[60],[60]]
fv = [[10.]]
nu = [[.4]]
alpha = [[1],[1]]
tab = [[Tr],[S]]
ss_ = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss_,'s200_.wav')

ll = l(d=[5,10,5,7,3+30], dev=[1,0.01,1,100,1],alpha = [1]*5, method=['lin']*5)
# def L_(d=[2,4,2], dev=[5,-10,20], alpha=[1,.5, 20], method=["exp", "exp", "exp"],
#         nsamples=0, sonic_vector=0, fs=44100):

s_ = ss*ll + ss_*(1-ll)

tt = t(d=[[3,5,2,5,5,10], [5,5,7,3,10]], fa=[[2,6,20,50,150,10],[.5,3,4,1,10]], dB=[[5,5,5,5,5,0],[20,10,7,15,0]], alpha=[[1,1,1,1,1,1],[1,1,1,1,1]], taba=[[S,S,S,S,S,S],[S,S,S,S,S]])
# def T_(d=[[3,4,5],[2,3,7,4]], fa=[[2,6,20],[5,6.2,21,5]],
#         dB=[[10,20,1],[5,7,9,2]], alpha=[[1,1,1],[1,1,1,9]],
#             taba=[[S,S,S],[Tr,Tr,Tr,S]],
#         nsamples=0, sonic_vector=0, fs=44100):

s_[-len(tt):] *= tt

M.utils.W(s_,'ssomething.wav')

fs = 44100
ll = l(d=[10], dev=[0],alpha = [1], method=['lin'])
s_l = s_[:]
s_r = s_[:]
s_l[-len(ll):] *= ll
s_l[-len(ll):] += ss[:len(ll)]*(1-ll)
s_l_ = H(s_l, ss[len(ll):len(ll)+fs*20])

s_r[-len(ll):] *= ll
s_r[-len(ll):] += ss_[:len(ll)]*(1-ll)
s_r_ = H(s_r, ss_[len(ll):len(ll)+fs*20])

tl = t(d=[[3,5,2,5,5], [5,5,7,3]], fa=[[2,6,20,50,150],[.5,3,4,1]], dB=[[5,5,5,5,5],[20,10,7,15]], alpha=[[1,1,1,1,1],[1,1,1,1]], taba=[[S,T.saw,S,T.triangle,S],[S,T.square,S,T.saw]])

tr = t(d=[[10,3,5,2], [5,7,3,5]], fa=[[6,20,50,150,10],[3,4,1,10]], dB=[[7]*5,[20,10,7,15]], alpha=[[1,1,1,1,1],[1,1,1,1]], taba=[[T.saw,S,T.triangle,S,T.square],[S,S,T.square,S]])

s_l_[-len(tl):] *= tl
s_r_[-len(tr):] *= tr
fd = F(d=10,method='lin')
s_l_[-len(fd):] *= fd
s_r_[-len(fd):] *= fd
s__ = (AD(sonic_vector=s_l_, S=0), AD(sonic_vector=s_r_, S=0))

M.utils.WS(s__,'ssom.wav')

bp=Being() # simple for permutation
bp.perms = M.structures.peals.PlainChanges(4).peal_direct
# bP.F_ = [200, 200*2**(4/12), 200*2**(8/12)]
# bp.domain = [1, 2, 3]
bp.domain = [200, 200*2**(3/12), 200*2**(6/12), 200*2**(9/12)]
bp.f_ = []
bp.fv_ = [3,10,50, 100]
bp.d_ = [1/6, 1/6, 1/6, 1/2]
bp.curseq = 'f_'
nnotes = 4*3*2*4
bp.stay(nnotes)
qd1 = H(*bp.render(nnotes))

silence = n.zeros(fs*4)


bp=Being() # simple for permutation
bp.perms = M.structures.peals.PlainChanges(4).peal_direct
# bp.f_ = [200, 200*2**(4/12), 200*2**(8/12)]
# bp.domain = [1, 2, 3]
bp.domain = [100, 100*2**(3/12), 100*2**(6/12), 100*2**(9/12)]
bp.f_ = []
bp.fv_ = [200, 100, 20, 10] # [3,10,50, 100]
bp.d_ = [1/2, 1/6, 1/6, 1/6]
bp.curseq = 'f_'
nnotes = 4*3*2*4
bp.stay(nnotes)
qd2 = H(*bp.render(nnotes))

sv = H(n.array(s__)*.2, silence, F(sonic_vector=qd1, out=False, method='lin'), qd1+qd2)

M.utils.WS(sv,'ssom2.wav')








f = [200,200.*2**(9/12)]
d = [[30],[30]]
fv = [[100]]
nu = [[1]]
alpha = [[1],[1]]
tab = [[Tr],[S]]
ss2 = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss2,'s200_la.wav')

f = [200.*2**(9/12)]*2
d = [[30],[30]]
fv = [[100]]
nu = [[1]]
alpha = [[1],[1]]
tab = [[Tr],[S]]
ss2 = s(f=f, d=d, fv=fv, nu=nu, alpha=alpha, tab=tab)
M.utils.W(ss2,'sla.wav')





