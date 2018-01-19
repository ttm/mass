import sys
keys=tuple(sys.modules.keys())
for key in keys:
    if "music" in key:
        del sys.modules[key]
import music as M, numpy as n
from percolation.rdf import c

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

    def walk(self, n):
        # walk n steps up (n<0 => walk |n| steps down, n==0 => don't move, return []

    def stay(self, n):
        # stay somewhere for n notes (n<0 => stay for n cycles or n permutations)

    def howl(self):
    def freeze(self):

    # use sequences of parameters to be iterated though with or without permutations.
    # use the fact that sequences of different sizes might yield longer cycles 
    
        

