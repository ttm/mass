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

def ADV(note_dict={}, adsr_dict={}):
    return AD(sonic_vector=V_(**note_dict), **adsr_dict)

# 19h30

# focus on making the pattern walk.
# then try to make sense in any other way with prefixes and suffixes.

# # Modes envisioned
# In the frequency domain, the sound might be:
# * Moving:
#   - lower pitch voice gets updated to higher pitch
#   - just make an ascendent sequence.
#     1 2 3
#       2 1 3
#       2 3 1 1+ 1++ 1+++ ... 
# assume 3 2 1
#       3 1 2
#       1 3 2
#       ,,,,
# is: static, moving up, static

def pS(permutations=0, bells=0, **kw):
    if not permutations:
        # peal 3
        pass
    if not bells:
        interval = 220*2**(12/len(permutations[0]))
    for permutation in permutations:
        # asound = V(
        pass
    return asound


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
        self.AddSeq(sequence)

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
            if not self.domain:
                domain = self.grid[self.pointer : self.pointer + self.seqsize]
            else:
                domain = self.domain
            nel = self.perms[0].size  # should match self.seqsize ?
            count = 0
            while len(sequence) < n:
                perm = self.perms[count % nel]
                seq = perm(domain)
                sequence.extend(seq)
                count += 1
            sequence = sequence[:n]
        self.addSeq(sequence)
        self.total_notes += n

    def addSeq(self, sequence):
        self.__dict__[self.curseq].extend(sequence)

    def render(self, nn, fn=False):
        # Render nn notes of the Being!
        # Render with legatto, with V__ or whatever it is called
        self.mkArray()
        ii = n.arange(nn)
        d = self.d_[ii%len(self.d_)]*self.dscale
        f = self.f_[ii%len(self.f_)]
        fv = self.fv_[ii%len(self.fv_)]
        nu = self.nu_[ii%len(self.nu_)]
        A = self.A_[ii%len(self.A_)]
        D = self.D_[ii%len(self.D_)]
        S = self.S_[ii%len(self.S_)]
        R = self.R_[ii%len(self.R_)]
        notes = [ADV({'f':ff, 'd':dd, 'fv':fvv, 'nu':nuu}, {'A':AA, 'D': DD, 'S': SS, 'R':RR}) for ff,dd,fvv,nuu,AA,DD,SS,RR in zip(f, d, fv, nu, A, D, S, R)]
        if fn:
            if type(fn) != str:
                fn = 'abeing.wav'
            if fn[-4] != '.wav':
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
    
bb=Being()
bb.d_ = [1/3, 1/6, 1/6]
bb.d_ = [1/2, 1/4, 1/4]
bb.f_ = [220, 330, 220*2**(11/12), 440]
bb.fv_ = [3, 50, 75, 100, 8]
bb.nu_ = [2, 10, 30, 50, 6, 15]
bb.dscale = .5
bb.render(20*3, True)
bb_ = H(*bb.render(20*3))
        
bb2=Being()
bb2.d_ = [1/3, 1/3, 1/6, 1/6]
bb2.f_ = [220, 330, 220*2**(11/12)]
bb2.fv_ = [3, 50, 75, 100, 8]
bb2.nu_ = [2, 10, 30, 50, 6, 15]
bb2.R_ = [10]
bb2.dscale = .5
bb2.render(20*3, 'another')
bb2_ = H(*bb2.render(20*3))


b=Being()
b.d_ = [1, 1/2, 1/2]
b.fv_ = [3, 50, 75, 100, 8]
b.nu_ = [2, 10, 30, 50, 6, 15]
b.render(20*3, 'yetAn')
b_ = H(*b.render(20*3))

fs = 44100
s0 = b_[:fs*8]
s0_ = b_[:fs*7]
s1 = bb_[:fs*4]
s1_= H(n.zeros(fs*4), bb_[:fs*3])
s2 = bb2_[:fs*7]

ss = H(s0, s1, s2+s0_+s1_)
M.utils.W(ss, 'borotega.wav')

bp=Being() # simple for permutation
bp.perms = M.structures.peals.PlainChanges(3).peal_direct
# bp.f_ = [200, 200*2**(4/12), 200*2**(8/12)]
bp.domain = [200, 200*2**(4/12), 200*2**(8/12)]
bp.f_ = []
bp.curseq = 'f_'
bp.stay(21)
bp.render(21, 'permBaby.wav')

# Use peals on rhythms:
# 1 = quarter note or figure (e.x. quarter, eigth, eigth)
# 2 = half note or figure
# 3 = eigth note or figure
# play: 1 2 3  2 1 3  2 3 1  3 2 1  3 1 2  1 3 2  [1 2 3]
