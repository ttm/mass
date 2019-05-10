import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c

peal = M.structures.symmetry.PlainChanges(3, 1)
semi = 2**(1/12)
f0 = 110*2
notes = [f0, f0*semi**4, f0*semi**8]


class IteratorSynth(M.synths.CanonicalSynth):
    def renderIterate(self, **statevars):
        self.absorbState(**statevars)
        self.iterateElements()
        return self.render()

    def iterateElements(self):
        sequences = [var for var in dir(self) if var.endswith("_sequence")]
        state_vars = [i[:-9] for i in sequences]
        positions = [i+"_position" for i in sequences]
        for sequence, state_var, position in zip(sequences, state_vars, positions):
            if position not in dir(self):
                self.__dict__[position] = 0
            self.__dict__[state_var] = self.__dict__[sequence][self.__dict__[position]]
            self.__dict__[position] += 1
            self.__dict__[position] %= len(self.__dict__[sequence])
isynth = IteratorSynth()
isynth.fundamental_frequency_sequence = []
isynth.table = isynth.tables.sine
for perm in peal.peal_direct:
    isynth.fundamental_frequency_sequence.extend(perm(notes))
sounds = []
for i in range(36):
    sounds += [isynth.renderIterate(duration=1/3)]
# M.utils.write(M.H(*sounds),"./sandsounds/ra.wav")
c('finished rendering peal')
M.utils.write(M.H(*sounds), "./apeal.wav")

# grave e agudo
f0_ = f0/4
notes_ = [f0_, f0_*semi**4, f0_*semi**8]
silence = n.zeros(int(44100*2/3))
bass = []
count = 0
sy = M.synths.CanonicalSynth()
sy.table = sy.tables.saw
for i in range(6):
    asound = [sy.render(fundamental_frequency=notes_[(2+count)%3], duration=1/3),
              silence] * 2
    bass.extend(asound)
    count += 1
bass_ = M.H(*bass)
mid = M.H(*sounds)
M.utils.write(mid + bass_, "./apeal_.wav")

# cycle has 18 beats, 3 compass with 6 beats each (2 x 3 beats)
# 2s per compass, 6s per cycle

# treble starts
f2 = f0*5
notes = [f2*semi, f2, (f2/2)/semi, f2/2]

# 2 notes per compass: anacruze
treble = []
sy.duration=2/3
silence = n.zeros(int((1- sy.duration)*44100))
count = 0
sy.table = sy.tables.triangle
for i in range(6):
    asound = [silence, sy.render(fundamental_frequency=notes[count%4]),
              sy.render(fundamental_frequency=notes[(count+1)%4]), silence]
    treble.extend(asound)
    count += 2
# treble.append(n.zeros(44100*(1/3)*6-sy.duration))
asound = [silence, sy.render(fundamental_frequency=notes[count%4])]
treble.extend(asound)
treble_ = M.H(*treble)

music = M.H(*[M.H(*sounds) + M.H(*bass)]*2)
# music = M.H([sounds, music])
treble__ = M.H(*treble_)
silence_  = n.zeros(len(music)-len(treble__))
treble___ = M.H(*[silence_, treble__])

music += treble___
music = M.H(*[*sounds, music])
M.utils.write(music, "./apeal__.wav")
M.utils.write(treble_, "./treble.wav")

###########
# Second session
# pattern with triangle
# bass with triangle and making the peal using cycles of 3 compass

pulse = 1
sub = pulse/3
compass = pulse*2
cycle = compass*3

isynth = IteratorSynth()
isynth.fundamental_frequency_sequence = []
isynth.table = isynth.tables.triangle
f0 = 110*2
notes = [f0, f0*semi**4, f0*semi**8]
notes_ = [f0_, f0_*semi**4, f0_*semi**8]
silence = n.zeros(int(44100*2*sub))

sy = M.synths.CanonicalSynth()
sy.table = sy.tables.square
syp = M.synths.CanonicalSynth()
syp.table = syp.tables.triangle

asound = [sy.render(fundamental_frequency=notes_[0], duration=sub),
             silence] * 2
asound_ = [sy.render(fundamental_frequency=notes[0], duration=sub),
           sy.render(fundamental_frequency=notes[1], duration=sub),
           sy.render(fundamental_frequency=notes[2], duration=sub), 
           sy.render(fundamental_frequency=notes[0], duration=sub),
           sy.render(fundamental_frequency=notes[2], duration=sub),
           sy.render(fundamental_frequency=notes[1], duration=sub) 
           ]

asound += [sy.render(fundamental_frequency=notes_[1], duration=sub),
             silence] * 2
asound_ += [sy.render(fundamental_frequency=notes[1], duration=sub),
           sy.render(fundamental_frequency=notes[0], duration=sub),
           sy.render(fundamental_frequency=notes[2], duration=sub), 
           sy.render(fundamental_frequency=notes[1], duration=sub),
           sy.render(fundamental_frequency=notes[2], duration=sub),
           sy.render(fundamental_frequency=notes[0], duration=sub) 
           ]

asound += [sy.render(fundamental_frequency=notes_[2], duration=sub),
             silence] * 2
asound_ += [sy.render(fundamental_frequency=notes[2], duration=sub),
           sy.render(fundamental_frequency=notes[0], duration=sub),
           sy.render(fundamental_frequency=notes[1], duration=sub), 
           sy.render(fundamental_frequency=notes[2], duration=sub),
           sy.render(fundamental_frequency=notes[1], duration=sub),
           sy.render(fundamental_frequency=notes[0], duration=sub) 
           ]

asound__ = M.H(*asound)+M.H(*asound_)
fa = 44100
compass__ = fa*2
def getCompass(x):
    """x in 0, 1, 2."""
    return asound__[compass__*x:compass__*(x+1)]

comp = [0,1,2]  # number of the compass in asound__
comps = []  # all the compass, each an array in list comps
for perm in peal.peal_direct:
    comp_ = perm(comp)
    for c in comp_:
        comps.append(getCompass(c))

apeal_sec = M.H(*comps)
M.utils.write(apeal_sec, "./apealSec.wav")


f2 = f0*5
notes = [f2*semi, f2, (f2/2)/semi, f2/2]

f = notes * 9  # 36 seconds = 2 seconds * 3 compass * 6 comp setting

tables = M.tables.Basic(1024*16)
Tr = tables.triangle
S = tables.sine
treble = M.core.D_(f=f+[f[-1]],
        d=[[1]*36, [2,5,6], [10,5,5,5,5], [4,6,2]*3],
        fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]],
        alpha=[[1]*36 , [1,1,1], [1,1,1,1,1], [1,1,1]*3],
        x=[-10,10,5,3]*3+[5], y=[1,1,.1,.1]*3+[.1], method=['lin','lin','lin']*3,
        tab=[[S]*36, [S,Tr,S], [S,S,S,S,S]], stereo=True)

treble = treble[:,:len(apeal_sec)]   
music_ = [apeal_sec+treble[0], apeal_sec+treble[1]]
M.core.WS(music_, 'apealSec_.wav')
music__ = M.H([music,music], music_)
M.core.WS(music_, 'apealSec__.wav')

# alternate the sequences of presence and absence
# Presence: 1 0 0, 0 1 0, 0 0 1
# Absence: 0 1 1, 1 0 1, 1 1 0

# Pattern P1
# 100, 101,
# 001, 110, 
# 010, 011

# P2:
# 100, 101, 001,
# 110, 010, 011

# 1 is presence of the voice bass-mid-treble
# (0 is absence)

# use bass_ mid treble music_

p = pulse_ = pulse*44100

S = M.utils.mixS
sound = [
        S(bass_[p*0:p*1])
        ]
sound += [
        S(bass_[p*1:p*2], treble[:, p*1:p*2])
        ]
sound += [
        S(treble[:, p*2:p*3],[])
        ]
sound += [
        S(bass_[p*3:p*4], mid[p*3:p*4])
        ]
sound += [
        S(mid[p*4:p*5],[])
        ]
sound += [
        S(treble[:, p*5:p*6], mid[p*5:p*6])
        ]

### second cycle
# same pattern (P1), but interpreted as treble, mid, bass
sound += [
        S(treble[:, p*6:p*7])
        ]
sound += [
        S(bass_[p*7:p*8], treble[:, p*7:p*8])
        ]
sound += [
        S(bass_[p*8:p*9],[])
        ]
sound += [
        S(treble[:, p*9:p*10], mid[p*9:p*10])
        ]
sound += [
        S(mid[p*10:p*11],[])
        ]
sound += [
        S(bass_[p*11:p*12], mid[p*11:p*12])
        ]

# another cycle and then repeats the beginning with the dual-note treble

S = M.utils.mixS
sound += [
        S(bass_[::12][p*0:p*1])
        ]
sound += [
        S(bass_[::6][p*1:p*2], treble[:, ::18][:, p*1:p*2])
        ]
sound += [
        S(treble[:, ::12][:, p*2:p*3],[])
        ]
sound += [
        S(bass_[::3][p*3:p*4], mid[::3][p*3:p*4])
        ]
sound += [
        S(mid[::2][p*4:p*5],[])
        ]
sound += [
        S(treble[:, ::6][:, p*5:p*6], mid[:6][p*5:p*6])
        ]

### second cycle
# same pattern (P1), but interpreted as treble, mid, bass
sound += [
        S(treble[:, ::5][:, p*6:p*7])
        ]
sound += [
        S(bass_[p*7:p*8], treble[:, ::4][:, p*7:p*8])
        ]
sound += [
        S(bass_[p*8:p*9],[])
        ]
sound += [
        S(treble[:, :3][:, p*9:p*10], mid[p*9:p*10])
        ]
sound += [
        S(mid[p*10:p*11],[])
        ]
sound += [
        S(bass_[p*11:p*12], mid[p*11:p*12])
        ]

#################
## coda
coda = [
        M.core.F(sonic_vector=M.core.AM(sonic_vector=music__[0],fm=55), d=24, method='linear'),
        M.core.F(sonic_vector=M.core.AM(sonic_vector=music__[1],fm=55), d=24, method='linear')]

mfade = M.core.F(sonic_vector=music, out=False, d=24, method='linear') 
coda_ = S(mfade,coda, end=True)
music___ = M.H(music__, *sound, coda_) 
m = music___

def sequenceOfStretches(x, s=[1,4,8,12], fs=44100):
    """
    Makes a sequence of squeezes of the fragment in x.

    Parameters
    ----------
    x : array_like
        The samples made to repeat as original or squeezed.
        Assumed to be in the form (channels, samples),
        i.e. x[1][120] is the 120th sample of the second channel.
    s : list of numbers
        Durations in seconds for each repeat of x.

    Examples
    --------
    >>> asound = H(*[V(f=i, fv=j) for i, j in zip([220,440,330,440,330],
                                                  [.5,15,6,5,30])])
    >>> s = sequenceOfStretches(asound)
    >>> s = sequenceOfStretches(asound,s=[.2,.3]*10+[.1,.2,.3,.4]*8+[.5,1.5,.5,1.,5.,.5,.25,.25,.5, 1., .5]*2)
    >>> W(s, 'stretches.wav')
    Notes
    -----
    This function is useful to render musical sequences given any material.

    """
    x = n.array(x)

    s_ = s*fs
    if len(x.shape) == 1:
        l = x.shape[0]
        stereo = False
    else:
        l = x.shape[1]
        stereo = True
    ns = l/fs
    ns_ = [ns/i for i in s]
    # x[::ns] (mono) or x[:, ::ns] stereo is the sound in one second
    # for any duration s[i], use ns_ = ns//s[i]
    # x[n.arange(0, len(x), ns_[i])]
    sound = []
    for ss in s:
        indexes = n.arange(0, l, ns/ss).round().astype(n.int)
        if stereo:
            segment = x[:, indexes]
        else:
            segment = x[indexes]
        sound.append(segment)
    sound_ = H(*sound)
    return sound_
    
final_sound = M.H(m[:,::168], m[:,::int(168//2)], m[:,::int(168//6)], m[:,::int(168//12)])
final_sound_ = M.synths.sequenceOfStretches(music___, [1,2,6,12])
final_sound2_ = M.synths.sequenceOfStretches(music___, [21])
final_sound__ = final_sound_ + final_sound2_

final_sound3_ = M.synths.sequenceOfStretches(music___, [168*2])
final_sound4_ = M.synths.sequenceOfStretches(music___, [168*5])
foo = 44100*30*2
foo2 = 44100*90*5
alen = final_sound__.shape[1]
final_sound___ = (final_sound__ + final_sound3_[:, :alen]
        + final_sound4_[:, foo:foo+alen]
        + final_sound4_[:, foo2:foo2+alen]
        )
codal = (32-21)*44100
final_sound___ = M.H(final_sound___,
        final_sound4_[:, foo+alen: foo+alen+codal] + 
        final_sound4_[:, foo2+alen: foo2+alen+codal]+
        final_sound3_[:, foo*2+alen: foo*2+alen+codal]
        )
music____ = M.H(music___, final_sound___*.8) # DEPRECATED
music____[:, -44100*4:] *= M.core.F(d=4)  # method = 'lin')
music_____ = M.utils.CF(music___, final_sound___*.6, 400, 'lin')
music_____[:, -44100*4:] *= M.core.F(d=4, method='lin')  # method = 'lin')
M.core.WS(music_____, '01peal.wav')
M.core.WS(final_sound,  'final.wav')
M.core.WS(final_sound_, 'final_.wav')
M.core.WS(final_sound__, 'final__.wav')
M.core.WS(final_sound___, 'final___.wav')

# for perm in peal.peal_direct:
#     isynth.fundamental_frequency_sequence.extend(perm(notes))
# sounds = []
# for i in range(36):
#     sounds += [isynth.renderIterate(duration=1/3)]
# # M.utils.write(M.H(*sounds),"./sandsounds/ra.wav")
# c('finished rendering peal')
# f0 = 110*2
# M.utils.write(M.H(*sounds), "./apealSec.wav")
# 
# # grave e agudo
# f0_ = f0/8
# notes_ = [f0_, f0_*semi**4, f0_*semi**8]
# silence = n.zeros(44100*2/3)
# bass = []
# count = 0
# sy = M.synths.CanonicalSynth()
# sy.table = sy.tables.square
# for i in range(6*len(peal.peal_direct)):
#     if i%6 == 0:
#         perm = peal.peal_direct[(i//6)%len(peal.peal_direct)]
#     notes_ = perm(notes_)
#     asound = [sy.render(fundamental_frequency=notes_[(1+count)%3], duration=1/3),
#               silence] * 2
#     bass.extend(asound)
#     count += 1
# M.utils.write(M.H(music, M.H(*(sounds*6)) + M.H(*bass)), "./apealSec_.wav")

