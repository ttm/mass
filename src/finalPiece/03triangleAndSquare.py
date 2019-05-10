import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c
def H(*x): return M.core.H((x))
V_ = M.core.V
AD = M.core.AD
T = M.tables.Basic()

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
        self.__dict__[self.curseq].extend(sequence)

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
            M.core.W(H(*notes), fn)
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
    
f1 = 220
f2 = 220*2**(6/12)

bb=Being()
# bb.fv_ = [1,20]
# bb.nu_ = [.1,.5, 3]
bb.fv_ = [80]
bb.nu_ = [.5]
bb.tab_ = [T.sine] # , T.triangle, T.square, T.saw]
bb.d_ = [1/2, 1/4, 1/4]
bb.f_ = [f1]
bb1_ = H(*bb.render(12))

bb.d_ = [1/2]
bb.f_ = [f1, f2]
bb2_ = H(*bb.render(8))

bb.d_ = [1/2, 1/4, 1/4]
bb.f_ = [f1, f2]
bb3_ = H(*bb.render(12))

ss1 = H(bb1_, bb2_, bb3_)
M.core.W(ss1, 'firstTri.wav')
        

###############
f2_ = 220*2**(4/12)
f3_ = 220*2**(8/12)

bb.d_ = [2/3, 1/3]
bb.f_ = [f1]
bb1_ = H(*bb.render(8))

bb.d_ = [1/3, 1/3, 1/3]
bb.f_ = [f1, f2_, f3_]
bb2_ = H(*bb.render(12))

bb.f_ = [f1, f2, f2]
bb2_b = H(*bb.render(12))

bb.d_ = [2/3, 1/3]
bb.f_ = [f1, f2_, f3_]
bb3_ = H(*bb.render(12))

bb.f_ = [f1, f2, f2]
bb3_b = H(*bb.render(12))

ss2 = H(bb1_, bb2_, bb3_)
M.core.W(ss2, 'secondTri.wav')
        
ss2_b = H(bb1_, bb2_b, bb3_b)
M.core.W(ss2_b, 'secondTri_b.wav')

###############
f2b = 220*2**(3/12)
f3b = 220*2**(6/12)
f4b = 220*2**(9/12)

bb.d_ = [2/3, 1/3]
bb.f_ = [f1]
bb1_ = H(*bb.render(8))

bb.d_ = [1/4, 1/4, 1/4, 1/4]
bb.f_ = [f1, f2b, f3b, f4b]
bb2_ = H(*bb.render(16))

bb.f_ = [f1, f2, f2, f2]
bb2_b = H(*bb.render(16))

bb.d_ = [2/3, 1/3]
bb.f_ = [f1, f2b, f3b, f4b]
bb3_ = H(*bb.render(8))

bb.f_ = [f1, f2, f2, f2]
bb3_b = H(*bb.render(8))

ss3 = H(bb1_, bb2_, bb3_)
M.core.W(ss3, 'firstSqua.wav')
        
ss3_b = H(bb1_, bb2_b, bb3_b)
M.core.W(ss3_b, 'firstSqua_b.wav')

###############
bb.d_ = [1/2, 1/4, 1/4]
bb.f_ = [f1]
bb1_ = H(*bb.render(12))

bb.d_ = [1/4, 1/4, 1/4, 1/4]
bb.f_ = [f1, f2b, f3b, f4b]
bb2_ = H(*bb.render(16))

bb.f_ = [f1, f2, f2, f2]
bb2_B = H(*bb.render(16))

bb.d_ = [1/2, 1/4, 1/4]
bb.f_ = [f1, f2b, f3b, f4b]
bb3_ = H(*bb.render(12))

bb.f_ = [f1, f2, f2, f2]
bb3_b = H(*bb.render(12))

ss4 = H(bb1_, bb2_, bb3_)
M.core.W(ss4, 'secondSqua.wav')
        
ss4_b = H(bb1_, bb2_b, bb3_b)
M.core.W(ss4_b, 'secondSqua_b.wav')

###############
bb.d_ = [1/2, 1/6, 1/6, 1/6]
bb.f_ = [f1]
bb1_ = H(*bb.render(16))

bb.d_ = [1/2, 1/2]
bb.f_ = [f1, f2]
bb2_ = H(*bb.render(8))

bb.d_ = [1/2, 1/6, 1/6, 1/6]
bb.f_ = [f1, f2]
bb3_ = H(*bb.render(16))

ss5 = H(bb1_, bb2_, bb3_)
M.core.W(ss5, 'firstSquaB.wav')
        

###############
bb.d_ = [1/2, 1/6, 1/6, 1/6]
bb.f_ = [f1]
bb1_ = H(*bb.render(16))

bb.d_ = [1/3, 1/3, 1/3]
bb.f_ = [f1, f2_, f3_]
bb2_ = H(*bb.render(12))

bb.f_ = [f1, f2, f2]
bb2_b = H(*bb.render(12))

bb.d_ = [1/2, 1/6, 1/6, 1/6]
bb.f_ = [f1, f2_, f3_]
bb3_ = H(*bb.render(48))

bb.f_ = [f1, f2, f2]
bb3_b = H(*bb.render(48))

ss6 = H(bb1_, bb2_, bb3_)
M.core.W(ss6, 'secondSquaB.wav')

ss6_b = H(bb1_, bb2_b, bb3_b)
M.core.W(ss6_b, 'secondSquaB_b.wav')

#######################
        
final = H(ss1, ss2, ss2_b, ss3, ss3_b, ss4, ss4_b, ss5, ss6, ss6_b)
M.core.W(final, 'triSq0.wav')


#############################
# Only on the vibratos!
# fv = f, nu = d

bb=Being()
# bb.fv_ = [1,20]
# bb.nu_ = [.1,.5, 3]
bb.fv_ = [2]
bb.nu_ = [1, 3, 5]
bb.tab_ = [T.triangle] # , T.triangle, T.square, T.saw]
bb.d_ = [1/3]
bb.f_ = [f1]
bb1_ = H(*bb.render(12))

bb.nu_ = [5]
bb.fv_ = [2, 7]
bb.d_ = [1/2]
bb2_ = H(*bb.render(8))

bb.nu_ = [1, 3, 5]
bb.fv_ = [2, 7]
bb.d_ = [1/2]
bb3_ = H(*bb.render(8))

bb.d_ = [1/3]
bb3_S = H(*bb.render(12))

ss1 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss1, 'firstTriV.wav')
        

###############
bb.nu_ = [1, 5]
bb.fv_ = [2]
bb.d_ = [1/2]
bb1_ = H(*bb.render(8))

bb.nu_ = [1]
bb.fv_ = [2, 7, 15]
bb.d_ = [1/3]
bb2_ = H(*bb.render(12))

bb.nu_ = [1, 5]
bb.fv_ = [3, 7, 15]
bb.d_ = [1/2]
bb3_ = H(*bb.render(8))

bb.d_ = [1/3]
bb3_S = H(*bb.render(12))

ss2 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss2, 'secondTriV.wav')
        

###############
bb.nu_ = [1, 5]
bb.fv_ = [3]
bb.d_ = [1/2]
bb1_ = H(*bb.render(8))

bb.nu_ = [1]
bb.fv_ = [1, 7, 15, 50]
bb.d_ = [1/4]
bb2_ = H(*bb.render(16))

bb.nu_ = [1, 5]
bb.fv_ = [1, 7, 15, 50]
bb.d_ = [1/2]
bb3_ = H(*bb.render(8))

bb.d_ = [1/4]
bb3_S = H(*bb.render(16))

ss3 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss3, 'firstSquaV.wav')
        

###############
bb.nu_ = [1, 5, 15]
bb.fv_ = [3]
bb.d_ = [1/3]
bb1_ = H(*bb.render(12))

bb.nu_ = [3]
bb.fv_ = [1, 5, 15, 50]
bb.d_ = [1/4]
bb2_ = H(*bb.render(16))

bb.nu_ = [1, 5, 15]
bb.fv_ = [1, 5, 15, 50]
bb.d_ = [1/3]
bb3_ = H(*bb.render(12))

bb.d_ = [1/4]
bb3_S = H(*bb.render(16))

ss4 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss4, 'secondSquaV.wav')
        

###############
bb.nu_ = [1,5,15,50]
bb.fv_ = [3]
bb.d_ = [1/4]
bb1_ = H(*bb.render(16))

bb.nu = [3]
bb.fv_ = [1,5]
bb.d_ = [1/2]
bb2_ = H(*bb.render(8))

bb.nu_ = [1,5,15,50]
bb.fv_ = [1,5]
bb.d_ = [1/2]
bb3_ = H(*bb.render(8))

bb.d_ = [1/4]
bb3_S = H(*bb.render(16))

ss5 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss5, 'firstSquaBV.wav')
        

###############
bb.nu_ = [1, 5, 15, 50]
bb.fv_ = [3]
bb.d_ = [1/4]
bb1_ = H(*bb.render(16))

bb.nu_ = [3]
bb.fv_ = [3, 7, 15]
bb.d_ = [1/3]
bb2_ = H(*bb.render(12))

bb.nu_ = [1, 5, 15, 50]
bb.fv_ = [3, 7, 15]
bb.d_ = [1/3]
bb3_ = H(*bb.render(12))

bb.d_ = [1/4]
bb3_S = H(*bb.render(16))

ss6 = H(bb1_, bb2_, bb3_, bb3_S)
M.core.W(ss6, 'secondSquaBV.wav')

#######################
        
final = H(ss1, ss2, ss3, ss4, ss5, ss6)
M.core.W(final, 'triSq0V.wav')

import itertools
# lst = range(1,5)
# list(itertools.chain.from_iterable(itertools.repeat(x, 3) for x in lst))
def rep(xx, n):
    return list(itertools.chain.from_iterable(itertools.repeat(x, n) for x in xx))

final = H(*rep([ss1, ss2, ss3, ss4, ss5, ss6], 4))
M.core.W(final, 'triSq0V_.wav')

