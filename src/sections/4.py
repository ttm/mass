import numpy as n

# auxiliary functions __n and __s.
# These only normalize the sonic vectors and
# write them as 16 bit, 44.1kHz WAV files.
def __n(sonic_array):
    """Normalize sonic_array to have values only between -1 and 1"""

    t = sonic_array
    if n.all(sonic_array==0):
        return sonic_array
    else:
        return ( (t-t.min()) / (t.max() -t.min()) )*2.-1.

def __s(sonic_array=n.random.uniform(size=100000), filename="asound.wav", f_s=44100):
    """A minimal approach to writing 16 bit WAVE files.
    
    One can also use, for example:
        import sounddevice as S
        S.play(array) # the array must have values between -1 and 1"""

    # to write the file using XX bits per sample
    # simply use s = n.intXX(__n(sonic_array)*(2**(XX-1)-1))
    s = n.int16(__n(sonic_array)*32767)
    w.write(filename, f_s, s)

f_s = 44100.  # Hz, sample rate
Lambda_tilde = Lt = 1024.
foo = n.linspace(0, 2*n.pi, Lt, endpoint=False)
S_i = n.sin(foo)  # a sinusoid period of T samples

H = n.hstack

# using the content from the previous sections,
# this is a very simple synthesizer of notes
def v(f=200, d=1., tab=S_i, fv=2., nu=2., tabv=S_i):
    Lambda = n.floor(f_s*d) ii = n.arange(Lambda)
    Lv = float(len(T))

    Gammav_i = n.floor(ii*fv*Lv/f_s)  # indexes for LUT
    Gammav_i = n.array(Gammav_i, n.int)
    # variation pattern of vibrato for each sample
    Tv_i = tabv[Gammav_i % int(Lv)]

    # frequency in Hz for each sample
    F_i = f*(2.**(Tv_i*nu/12.))
    # movement inside table for each sample
    D_gamma_i = F_i*(Lt/float(f_s))
    Gamma_i = n.cumsum(D_gamma_i)  # movement in the total table
    Gamma_i = n.floor(Gamma_i)  # the indexes
    Gamma_i = n.array(Gamma_i, dtype=n.int)  # the indexes
    return tab[Gamma_i % int(Lt)]  # looking for indexes in table


############## Sec. 4.1 Tuning, intervals, scales and chords
just_ratios = [1, 9/8, 5/4, 4/3, 3/2, 5/3, 15/3, 2]
pythagorean_ratios = [1, 9/8, 81/64, 4/3, 3/2, 27/16, 243/128, 2]
equal_temperament_ratios = [2**(i/12) for i in range(12)]

f = 220  # an arbitrary frequency
just_scale = [i*f for i in just_intonations]
pythagorean_scale = [i*f for i in pythagorean_ratios]
equal_temperament_scale = [i*f for i in equal_temperament_ratios]

js = H([v(i) for i in just_scale])
__s(js, "just_scale.wav")
ps = H([v(i) for i in pythagorean_scale])
__s(js, "pythagorean_scale.wav")
es = H([v(i) for i in equal_temperament_scale])
__s(js, "equal_temperament_scale.wav")

### Microtonality
# quarter tones
epslon = 2**(1/12.)
s1 = [0., 1.25, 1.75, 2., 2.25, 4., 5., 5.25]
factors = [epslon**i for i in s1]
scale = H([v(f*i) for i in factors])
__s(scale, "quarter_tones1.wav")

epslon = 2**(1/24.)
factors = [epslon**i for i in range(24)]
scale = H([v(f*i) for i in factors])
__s(scale, "quarter_tones2.wav")

# Octave sevenths
epslon_ = 2**(1/7.)
s2 = [0., 1., 2., 3., 4., 5., 6., 7.]
factors = [epslon_**i for i in s2]
scale = H([v(f*i) for i in factors])
__s(scale, "octave_sevenths.wav")

### Eq. 81 relating note grids
# expressing octave sevenths in the quarter tone grid:
s2_ = [i*24/7 for i in s2]

### Table 1: Intervals
# using epsilon = 2**(1/12)
I1j = 0.
I2m = 1.
I2M = 2.
I3m = 3.
I3M = 4.
I4J = 5.
ITR = 6.
I5J = 7.
I6m = 8.
I6M = 9.
I7m = 10.
I7M = 11.
I8J = 12.
I_i = n.arange(13.)

perfect_consonances = [0, 7, 12]
imperfect_consonances = [3, 4, 8, 9]
weak_dissonances = [2, 10]
strong_dissonances = [1, 11]
special_cases = [5, 6]

# the interval sums nine for inversion by traditional nomenclature
# fifth is inverted into a fourth (5+4 = 9)
# but always sums 12
# at inversions of semitones
# fifth (7) is inverted into a fourth (5) (7+5 = 12)
def inv(I):
    """Returns inversed interval of I: 0< =  I < = 12"""
    return 12-I


# harmonic interval
def intervaloHarmonico(f, I):
    return (v(f)+v(f*2.**(I/12.)))*0.5


# melodic interval
def intervaloMelodico(f, I):
    return n.hstack((v(f), v(f*2.**(I/12.))))

### Eq. 82 Symmetric scales
Ec = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11.]
Ewt = [0., 2., 4., 6., 8., 10.]
Etm = [0., 3., 6., 9.]
EtM = [0., 4., 8.]
Ett = [0., 6.]

### Eq. 83 Diatonic scales
Em = [0., 2., 3., 5., 7., 8., 10.]
Emlo = [1., 3., 5., 6., 8., 10.]
EM = [0., 2., 4., 5., 7., 9., 11.]
Emd = [0., 2., 3., 5., 7., 9., 10.]
Emf = [0., 1., 3., 5., 7., 8., 10.]
Eml = [0., 2., 4., 6., 7., 9., 11.]
Emmi = [0., 2., 4., 5., 7., 8., 10.]

### Eq. 84 Diatonic pattern
E_ = n.roll(n.array([2.,2.,1.,2.,2.,2.,1.]), n.random.randint(7.))
E = n.cumsum(E_)-E_[0.]


### Eq. 85 Harmonic and melodic minor scales
Em = [0., 2., 3., 5., 7., 8., 10.]
Emh = [0., 2., 3., 5., 7., 8., 11.]
Emm = [0.,2.,3.,5.,7.,9.,11.,12.,10.,8.,7.,5.,3.,2.,0.]

### Eq. 86 Harmonic series
H = [ 0, 12, 19+0.02, 24, 28-0.14, 31+0.2, 34-0.31,
      36, 38+0.04, 40-0.14, 42-0.49, 43+0.02,
      44+0.41, 46-0.31, 47-0.12,
      48, 49+0.05, 50+0.04, 51-0.02, 52-0.14 ]

### Eq. 86 Triads
AM = [0., 4., 7.]
Am = [0., 3., 7.]
Ad = [0., 3., 6.]
Aa = [0., 4., 8.]

def withMinorSeventh(A): return A+[10.]
def withMajorSeventh(A): return A+[11.]


############## Sec. 4.2 Atonal and tonal harmonies, harmonic expansion and modulation
### Table 2.23
def relativa(TT):
    """Returns the relative chord.
    
    TT is a major or minor triad at a closed and fundamental position."""
    T = n.copy(TT)
    if T[1]-T[0] == 4:  # TT is major
        T[2] = 9.  # returns minor chord a minor third bellow
    elif T[1]-T[0] == 3:  # TT is minor
        T[0] = 10.  # returns major chord a major third above
    else:
        print("send me only minor or major perfect triads")
    return T


def antiRelativa(TT):
    """Returns the anti-relative chord."""
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[0] = 11.  # returns up minor
    if T[1]-T[0] == 3.:  # menor
        T[2] = 8.  # returns down major
    return T

### Medians
def sup(TT):
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[0] = 11.
        T[2] = 8.  # returns major
    if T[1]-T[0] == 3.:  # minor
        T[0] = 10.
        T[2] -= 1.  # returns minor
    return T

def inf(TT):
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[2] = 9
        T[0] = 1.  # returns major
    if T[1]-T[0] == 3.:  # minor
        T[2] = 8.
        T[0] = 11.  # returns minor
    return T

def supD(TT):
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[0] = 10.
        T[1] = 3.  # returns major
    if T[1]-T[0] == 3.:  # minor
        T[0] = 11.
        T[1] = 4.  # returns minor
    return T

def infD(TT):
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[1] = 3.
        T[2] = 8.  # returns major
    if T[1]-T[0] == 3.:  # minor
        T[1] = 4.
        T[2] = 9.  # returns minor
    return T

### Main tonal functions
tonicM = [0., 4., 7.]
tonicm = [0., 3., 7.]
subM = [0., 5., 9.]
subm = [0., 5., 8.]
dominant = [2., 7., 11.]
Vm = [2., 7., 10.]  # minor chord is not dominant


############## Sec. 4.3 Counterpoint
def contraNotaNotaSup(alturas=[0,2,4,5,5,0,2,0,2,2,2,0,7,\
                                     5,4,4,4,0,2,4,5,5,5]):
    """Returns a melody given input melody
    
    Limited in 1 octave"""
    first_note = alturas[0]+(7,12)[n.random.randint(2)]
    contra = [first_note]

    i=0
    cont=0 # parallels counter
    reg=0 # interval register where the parallel was done
    for al in alturas[:-1]:
        mov_cf=alturas[i:i+2]
        atual_cf,seguinte_cf=mov_cf
        if seguinte_cf-atual_cf>0:
            mov="asc"
        elif seguinte_cf-atual_cf<0:
            mov="asc"
        else:
            mov="obl"

        # possibilities by consonances
        possiveis=[seguinte_cf+interval for interval in\
                                    [0,3,4,5,7,8,9,12]]
        movs=[]
        for pos in possiveis:
            if pos -contra[i] < 0:
                movs.append("desc")
            if pos - contra[i] > 0:
                movs.append("asc")
            else:
                movs.append("obl")

        movt=[]
        for m in movs:
            if 'obl' in (m,mov):
                movt.append("obl")
            elif m==mov:
                movt.append("direto")
            else:
                movt.append("contrario")
        blacklist=[]
        for nota,mt in zip(possiveis,movt):

            if mt == "direto": # direct movement
                # does not accept perfect consonances
                if nota-seguinte_cf in (0,7,8,12):
                    possiveis.remove(nota)
        ok=0
        while not ok:
            nnota=possiveis[n.random.randint(len(possiveis))]
            if nnota-seguinte_cf==contra[i]-atual_cf: # parallel
                intervalo=contra[i]-atual_cf
                novo_intervalo=nnota-seguinte_cf
                if abs(intervalo-novo_intervalo)==1: # same 3 or 6 type
                    if cont==2: # if already had 2 parallels
                        pass # another interval
                    else:
                        cont+=1
                        ok=1
            else: # oblique or opposite movement
                cont=0 # make parallels equal to zero
                ok=1
        contra.append(nnota)
        i+=1
    return contra


############## Sec. 4.4 Rhythm
### See Poli Hit Mia musical piece


############## Sec 4.5 Repetition and variation: motifs and larger units
### Ubiquitous concepts
# examples
S = [1, 2, 1.5, 3]  # a sequence of parameters, e.g. durations
S1 = S[::-1]  # reversion
S2 = [i*4 for i in S]  # expansion
S3 = [i*.5 for i in S]  # contraction
S4 = S[2:] + S[:2]

# now suppose that S is a sequence of pitches
S5 = [i+7 for i in S]  # transposition
S6 = [i-12 for i in S]  # interval inversion


############## Sec 4.6 Directional structures
### See Dirracional musical piece


############## Sec. 4.7 Cyclic structures
### See 3 Trios musical pieces
### and the PPEPPS
