#-*- coding: utf-8 -*-
import numpy as n

f_a = 44100.  # Hz, sample rate
Lambda_tilde = Lt = 1024.
foo = n.linspace(0, 2*n.pi, Lt, endpoint=False)
S_i = n.sin(foo)  # a sinusoid period of T samples


def v(f=200, d=2., tab=S_i, fv=2., nu=2., tabv=S_i):
    Lambda = n.floor(f_a*d)
    ii = n.arange(Lambda)
    Lv = float(len(S_i))

    Gammav_i = n.floor(ii*fv*Lv/f_a)  # indexes for LUT
    Gammav_i = n.array(Gammav_i, n.int)
    # variation pattern of vibrato for each sample
    Tv_i = tabv[Gammav_i % int(Lv)]

    # frequency in Hz for each sample
    F_i = f*(2.**(Tv_i*nu/12.))
    # movement inside table for each sample
    D_gamma_i = F_i*(Lt/float(f_a))
    Gamma_i = n.cumsum(D_gamma_i)  # movement in the total table
    Gamma_i = n.floor(Gamma_i)  # the indexes
    Gamma_i = n.array(Gamma_i, dtype=n.int)  # the indexes
    return tab[Gamma_i % int(Lt)]  # looking for indexes in table


############## 2.3.1 Tuning, intervals, scales and chords

### Microtonality of tone quarters
### and octave sevenths
# with
epslon = 2**(1/12.)
s1 = [0., 0.25, 1.75, 2., 2.25, 4., 5., 5.25]
# or
epslon = 2**(1/7.)
s2 = [0., 1., 2., 3., 4., 5., 6.]

### Table 2.22: Intervals
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


# the interval sums nine nomenclature for inversion, but always sums 12
# at inversions of semitones
def inv(I):
    """Returns inversed interval of I: 0< =  I < = 12"""
    return 12-I


# harmonic interval
def intervaloHarmonico(f, I):
    return (v(f)+v(f*2.**(I/12.)))*0.5


# melodic interval
def intervaloMelodico(f, I):
    return n.hstack((v(f), v(f*2.**(I/12.))))

### 2.82 Symmetric scales
Ec_i = [0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10., 11.]
Et_i = [0., 2., 4., 6., 8., 10.]
Etm_i = [0., 3., 6., 9.]
EtM_i = [0., 4., 8.]
Ett_i = [0., 6.]

### 2.83 Diatonic scales
Em_i = [0., 2., 3., 5., 7., 8., 10.]
Emlo_i = [1., 3., 5., 6., 8., 10.]
EM_i = [0., 2., 4., 5., 7., 9., 11.]
Emd_i = [0., 2., 3., 5., 7., 9., 10.]
Emf_i = [0., 1., 3., 5., 7., 8., 10.]
Eml_i = [0., 2., 4., 6., 7., 9., 11.]
Emmi_i = [0., 2., 4., 5., 7., 8., 10.]

### 2.84 Diatonic pattern
E_i_ = n.roll(n.array([2.,2.,1.,2.,2.,2.,1.]), n.random.randint(7.))
E_i = n.cumsum(E_i_)-E_i_[0.]


### 2.85 Harmonic and melodic minor scales
Em_i = [0., 2., 3., 5., 7., 8., 10.]
Emh_i = [0., 2., 3., 5., 7., 8., 11.]
Emm_i = [0.,2.,3.,5.,7.,9.,11.,12.,10.,8.,7.,5.,3.,2.,0.]


### 2.86 Triads
AM_i = [0., 4., 7.]
Am_i = [0., 3., 7.]
Ad_i = [0., 3., 6.]
Aa_i = [0., 4., 8.]

def comSetimam(A): return A+[10.]
def comSetimaM(A): return A+[11.]



############## 2.3.2 Atonal and tonal harmonies, expansion and modulation
### Table 2.23
def relativa(TT):
    """TT is major and minor triad at closed and fundamental positions."""
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # ac is major
        T[2] = 9.  # returns down minor chord
    elif T[1]-T[0] == 3.:  # ac is minor
        T[0] = 10.  # returns up major chord
    else:
        print("send me only minor or major perfect triads")
    return T


def antiRelativa(TT):
    T = n.copy(TT)
    if T[1]-T[0] == 4.:  # major
        T[0] = 11.  # returns up minor
    if T[1]-T[0] == 3.:  # menor
        T[2] = 8.  # returns down major
    return T


class Mediana:
    def sup(self, TT):
        T = n.copy(TT)
        if T[1]-T[0] == 4.:  # major
            T[0] = 11.
            T[2] = 8.  # returns major
        if T[1]-T[0] == 3.:  # minor
            T[0] = 10.
            T[2] -= 1.  # returns minor
        return T

    def inf(self, TT):
        T = n.copy(TT)
        if T[1]-T[0] == 4.:  # major
            T[2] = 9
            T[0] = 1.  # returns major
        if T[1]-T[0] == 3.:  # minor
            T[2] = 8.
            T[0] = 11.  # returns minor
        return T

    def supD(self, TT):
        """Preserves the fifth and first triad in third."""
        T = n.copy(TT)
        if T[1]-T[0] == 4.:  # major
            T[0] = 10.
            T[1] = 3.  # returns major
        if T[1]-T[0] == 3.:  # minor
            T[0] = 11.
            T[1] = 4.  # returns minor
        return T

    def infD(self, TT):
        T = n.copy(TT)
        if T[1]-T[0] == 4.:  # major
            T[1] = 3.
            T[2] = 8.  # returns major
        if T[1]-T[0] == 3.:  # minor
            T[1] = 4.
            T[2] = 9.  # returns minor
        return T

### Main functions
tonicaM = [0., 4., 7.]
tonicam = [0., 3., 7.]
subM = [0., 5., 9.]
subm = [0., 5., 8.]
dom = [2., 7., 11.]
Vm = [2., 7., 10.]  # fifth minor grade is not dominant


############## 2.3.3 Counterpoint
def contraNotaNotaSup(alturas=[0,2,4,5,5,0,2,0,2,2,2,0,7,\
                                     5,4,4,4,0,2,4,5,5,5]):
    """Does the independence routine of voices
    
    Limited in 1 up and down octave"""
    primeiraNota=alturas[0]+(7,12)[n.random.randint(2)]
    contra=[primeiraNota]

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
                # does not accepts perfect intervals
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


############## 2.3.4 Rhythm
### See Poli Hit Mia music piece at Appendix B


############## 2.3.5 Repetition and variation: motifs and larger unities
### Ubique concepts


############## 2.3.6 Directional structures
### See Dirracional music piece at Appendix B


############## 2.3.7 Cyclic structures
### See 3 Trios music pieces at Appendix B
### and the PPEPPS at Appendix C
