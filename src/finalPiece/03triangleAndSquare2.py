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
F = M.core.F

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

# rotate 4 in [3 1]
# rhythm fv_ 3 nu_ 4 in [1 1 1 1]
# complement to rotate f 2 in [1 2]

pe = M.structures.permutations.InterestingPermutations(4)
# pe.rotations

bp=Being() # simple for permutation
bp.perms = pe.rotations[:1] + pe.rotations[1:][::-1]
bp.perms = pe.rotations
# bp.f_ = [200, 200*2**(4/12), 200*2**(8/12)]
# bp.domain = [1, 2, 3]
bp.domain = [f1, f1*2**(3/12), f1*2**(6/12), f1*2**(9/12)]
bp.f_ = []
bp.fv_ = [25]
bp.nu_ = [30]
bp.tab_ = [T.sine]
bp.d_ = [1/6, 1/6, 1/6, 1/2]
bp.curseq = 'f_'
nnotes = 4*4
bp.stay(nnotes)
bp.render(nnotes, 'rotate4.wav')
rot1 = H(*bp.render(nnotes))*.5

bp_r=Being() # simple for permutation
bp_r.f_ = [f1/2]
bp_r.nu_ = [1, 5, 15, 50]
bp_r.fv_ = [3, 7, 5500, 50, 100, 1000,15000]
bp_r.d_ = [1/4]
rhy1 = H(*bp_r.render(48))

bp_c=Being() # simple for permutation
bp_c.d_ = [1/2, 1/4, 1/4]
bp_c.f_ = [f1*2, f1*2*2**(6/12)]
bp_c.fv_ = [20,50,100,300]
bp_c.nu_ = [2,5,20,100]
compl1 = H(*bp_c.render(12))*.4

s = H(rot1, rhy1, rhy1+H(rot1, rot1, rot1), *[compl1]*3,H(*[compl1]*3)+rhy1, H(*[compl1]*3)+H(*[rot1]*3)+rhy1[::-1])
# s = H(rot1, rhy1, rhy1+H(rot1, rot1, rot1), H(*[compl1]*3)+H(*[rot1]*3)+rhy1[::-1])
M.core.W(s, 'triSq1.wav')

#######################

nnotes = 4*4
bp.stay(nnotes)
bp.fv_ = [150]
bp.nu_ = [10]
bp.tab_ = [T.triangle]
rot2 = H(*bp.render(nnotes))*.5

bp_r.f_ = [f1/2]
bp_r.nu_ = [10, 50, 150, 500]
bp_r.fv_ = [.1, .5, 1, 3, 7, 5500, 50, 100, 1000,15000]
bp_r.d_ = [.5] + [1/4]*5 + [1/8]*2
rhy2 = H(*bp_r.render(48))

bp_c.d_ = [1/2, 1/4, 1/4]
bp_c.f_ = [f1*2, f1*2*2**(6/12)]
bp_c.fv_ = [20,50,10,3]
bp_c.nu_ = [2,5,20,10]
compl2 = H(*bp_c.render(12))*.4

s_ = H(s, *[rot2]*3, rhy2, H(*[rot2]*3)[:len(rhy2)] + rhy2, *[compl2]*3,H(*[compl2]*3)[:len(rhy2)]+rhy2, H(*[compl2]*3)[:len(rhy2)]+H(*[rot2]*3)[:len(rhy2)]+rhy2[::-1])

dur = s_.shape[0]/44100
durf = 10
pace = int(dur/durf)
coda = s_[::pace]
s_ = H(s_, coda)
M.core.W(s_, 'triSq1_.wav')




#################
pe3 = M.structures.permutations.InterestingPermutations(3)
bpt=Being()
bpt.perms = pe3.rotations
bpt.domain = [f1, f1*2**(4/12), f1*2**(8/12)]
bpt.f_ = []
bpt.fv_ = [1250]
bpt.nu_ = [5]
bpt.tab_ = [T.sine]
bpt.d_ = [1/2, 1/4, 1/4]
bpt.curseq = 'f_'
nnotes = 3*4
bpt.stay(nnotes)
bpt.render(nnotes, 'rotate3.wav')
rot3 = H(*bpt.render(nnotes))

bp_r3=Being() # simple for permutation
bp_r3.f_ = [f1/3]
bp_r3.nu_ = [1, 7, 15, .2]
bp_r3.fv_ = [3, 7, 5500, 50, 100]
bp_r3.d_ = [1/3]
rhy3 = H(*bp_r3.render(12*3))

bp_c3=Being() # simple for permutation
bp_c3.d_ = [1/3, 1/3, 1/6, 1/6]
bp_c3.f_ = [f1*2*2**(2*i/12) for i in range(6)]
bp_c3.fv_ = [20,50,300]
bp_c3.nu_ = [2,20,100]
compl3 = H(*bp_c3.render(16))*.4

s_ = H(s_, rot3, rhy3, H(*[rot3]*3) + rhy3, *[compl3]*3, H(*[compl3]*3) + rhy3, H(*[compl3]*3) + H(*[rot3]*3) + rhy3[::-1])
M.core.W(s_, 'triSq1_.wav')

##########################
# silence 4 s note 4s, silence 2s, note 2s
# coda + 3 (trian) + 4 (square)

# d = [1 3] for square notes: dim
# d = [2 1] for triang notes: aum (triang aum might walk chromaticaly)
# presents them, enters coda making patterns with rhy
# ends piece

bp=Being() # simple for permutation
bp.domain = [f1*3, f1*3*2**(3/12), f1*3*2**(6/12), f1*3*2**(9/12)]
bp.perms = pe.rotations[:1] + pe.rotations[1:][::-1]
bp.f_ = []
bp.fv_ = [0]
bp.nu_ = [0]
bp.d_ = [1/2, 1/6, 1/6, 1/6]
bp.tab_ = [T.square]

nnotes = 4*4
bp.curseq = 'f_'
bp.stay(nnotes)
rot4_dev = H(*bp.render(nnotes))*.5


bp=Being() # simple for permutation
bp.domain = [f1/2, f1/2*2**(4/12), f1/2*2**(8/12)]
bp.perms = pe3.rotations[:1] + pe3.rotations[1:][::-1]
bp.f_ = []
bp.fv_ = [0]
bp.nu_ = [0]
bp.d_ = [1/4, 1/4, 1/2]
bp.tab_ = [T.saw]

nnotes = 3*3
bp.curseq = 'f_'
bp.stay(nnotes)
rot3_dev = H(*bp.render(nnotes))*.5

fs = 44100
silence = n.zeros(fs*4)
note = AD(sonic_vector=V_(f=220, d=4, tabv=T.saw[::-1], tab=T.sine, fv=.5, nu=10))
silence2 = n.zeros(fs*2)
note2 = AD(sonic_vector=V_(f=330, d=2,tabv=T.saw, tab=T.square, fv=2, nu=100))

s2 = H(silence, note, silence2, note2, H(*[rot4_dev]*3) + H(*[rot3_dev]*4))

s_ = H(s_, s2)

def sc(start, dur):
    return AD(sonic_vector=coda[ int(start*fs) : int((start+dur)*fs) ], R=10)


bpp=Being()
bpp.domain = [sc(3,1/4), sc(7,1/4), sc(9, 1/4), sc(0,1/4)]
bpp.perms = pe.rotations
nnotes = 4*4
bpp.temp_ = []
bpp.curseq = 'temp_'
bpp.stay(nnotes)
rotC = H(*bpp.temp_)

s_ = H(s_, rotC)


bpp=Being()
bpp.domain = [sc(3,1/4), sc(7, 1/2), sc(9, 1/4)]
bpp.perms = pe3.rotations
nnotes = 3*3
bpp.temp_ = []
bpp.curseq = 'temp_'
bpp.stay(nnotes)
rotC2 = H(*bpp.temp_)

bp=Being() # simple for permutation
bp.perms = pe.rotations[:1] + pe.rotations[1:][::-1]
bp.perms = pe.rotations
# bp.f_ = [200, 200*2**(4/12), 200*2**(8/12)]
# bp.domain = [1, 2, 3]
bp.domain = [f1, f1*2**(3/12), f1*2**(6/12), f1*2**(9/12)]
bp.f_ = []
bp.fv_ = [20]
bp.nu_ = [10]
bp.tab_ = [T.sine]
bp.d_ = [1/6, 1/6, 1/6, 1/2]
bp.curseq = 'f_'
nnotes = 4*4
bp.stay(nnotes)
rot1_ = H(*bp.render(nnotes))*.5

s_ = H(s_, H(*[rotC2]*4) + H(*[rot1_]*3))

#########################

bp_c3=Being()
bp_c3.d_ = [1/3, 1/3, 1/6, 1/6]
bp_c3.f_ = [f1/4*2**(10*i/12) for i in range(6)]
bp_c3.fv_ = [20,5,300]
bp_c3.nu_ = [2,20,100]
compl3F = H(*bp_c3.render(12))*.4  # 3 seconds

bp_r=Being()
bp_r.f_ = [f1/2]
bp_r.nu_ = [10, 50, 150, 500]
bp_r.fv_ = [5500, 500, 10000, 1000,15000]
bp_r.d_ = [.5] + [1/4]*3 + [1/8]*2 +[1/2]  # 2 seconds in 7 notes
rhy2F = H(*bp_r.render(7*5*4))  # 40 seconds to finish cycle

bp_n=Being()
# bp_n.f_ = []
# bp_n.domain = [f1*4, 0, 0, f1*4, 0, 0, 0, 0, 0, f1*4]
bp_n.f_ = [f1*4]
bp_n.fv_ = [5]
foo = [f1*4, 0, 0, f1*4, 0, 0, 0, 0, 0, f1*4] 
bp_n.S_ = []
bp_n.domain = [-5 if i else -40 for i in foo]
bp_n.d_ = [.5] + [1/4]*3 + [1/8]*2 +[1/2]  # 2 seconds in 7 notes
pe7 = M.structures.permutations.InterestingPermutations(7)
bp_n.perms = pe7.alternations
bp_n.curseq = 'S_'
nnotes = 7*20
bp_n.stay(nnotes)
note_funky = H(*bp_n.render(nnotes))*.5

bp_n=Being()
bp_n.f_ = [f1*3]
bp_n.d_ = [40]
bp_n.nu_ = [4]
bp_n.fv_ = [.3]
nnotes = 1
note_steady = H(*bp_n.render(nnotes))*.5

F = M.core.F
sf = H( H(*[compl3F]*13, n.zeros(fs))[:len(note_funky)] + F(sonic_vector=rhy2F,out=True, method='lin') + note_funky + F(sonic_vector=note_steady, out=False, method='lin')[:len(note_funky)])

s_ = H(s_, sf)

M.core.W(s_, 'triSq2.wav')



