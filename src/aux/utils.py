import numpy as n
from scipy.io import wavfile as w

__doc__ = """This file holds minimal implementations
to avoid repetitions in the
musical pieces of the MASS framework:
    https://github.com/ttm/mass

See the music Python Package 
(in the music/ directory of the same repository)
for a further documented implementation
with many useful routines."""

### In this file are functions (only) for:
# IO
# Vibrato and Tremolo
# ADSR

#####################
# IO
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

def W(fn, fs, sa): 
     """To mimic scipy.io.wavefile input"""
    __s(sa, fn, f_s=44100)


###################
# Synthesis
f_s = 44100.  # Hz, standard sample rate

# very large tables, we are not worried about real time
# use Lt = 1024 if in need of better performance
Lambda_tilde=Lt=1024.*16

# Sine
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras

# Square
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )

# Triangular
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

# Sawtooth
D_i=n.linspace(-1,1,Lt)


def V(f=220, d=2, fv=2, nu=2, tab=Tr_i, tabv=S_, nsamples=0):
    """
    Synthesize a musical note with a vibrato.
    
    Set fv=0 for a note without vibrato.
    A vibrato is an oscillation of the pitch [1].
    
    Parameters
    ----------
    f : scalar
        The frequency of the note in Hertz.
    d : scalar
        The duration of the note in seconds.
    fv : scalar
        The frequency of the vibrato oscillations in Hertz.
    nu : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    tab : array_like
        The table with the waveform to synthesize the sound.
    tabv : array_like
        The table with the waveform of the vibrato oscillatory pattern.
    nsamples : scalar


    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    T : an oscillation of loudness.
    FM : a linear oscillation of fundamental frequency.
    AM : a linear oscillation of amplitude.
    V_ : a shorthand to render a note with vibrato using
        a reference frequency and a pitch interval.
    raw.vibrato : a very slim implementation of this function.

    Examples
    --------
    >>> W(V())  # writes a WAV file of a note
    >>> s = H( [V(i, j) for i, j in zip([200, 500, 100], [2, 1, 2])] )
    >>> s2 = V(440, 1.5, 6, 1)

    Notes
    -----
    In the MASS framework implementation, for a sound with a vibrato (or FM) to be synthesized using LUT,
    the vibrato pattern is considered when performing the lookup calculations.

    The tremolo and AM patterns are implemented as separate amplitude envelopes.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    Lambda = n.floor(f_s*d)
    ii = n.arange(Lambda)
    Lv = len(tabv)

    Gammav_i = n.floor(ii*fv*Lv/f_s)  # LUT indexes
    Gammav_i = n.array(Gammav_i, n.int)
    # values of the oscillatory pattern at each sample
    Tv_i = tabv[Gammav_i%Lv] 

    # frequency in Hz at each sample
    F_i=f*2**(  Tv_i*nu/12  ) 
    # shift in table at each sample
    D_gamma_i=F_i*(Lt/f_s)
    Gamma_i=n.cumsum(D_gamma_i)  # total shift in LUT at each sample
    Gamma_i=n.floor( Gamma_i ).astype(n.int)  # final indexes
    return tab[Gamma_i%Lt]  # final sample lookup


def T(d=2, fa=2, V_dB=10, taba=S_i, nsamples = 0, sonic_vector = 0):
    """
    Synthesize a tremolo envelope or apply it to a sound.
    
    Set fa=0 for a constant envelope with value 1.
    A tremolo is an oscillation of the intensity [1].
    
    Parameters
    ----------
    d : scalar
        The duration of the note in seconds.
    fa : scalar
        The frequency of the tremolo oscillations in Hertz.
    V_dB : scalar
        The maximum deviation of loudness in the tremolo in decibels.
    taba : array_like
        The table with the waveform of the tremolo oscillatory pattern.
    nsamples : scalar
        The number of samples of the envelope. If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the tremolo to be applied ob. If supplied, d and nsamples are ignored.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a PCM sample of the envelope
        if sonic_vector is not 0.
        If sonic_vector is input, s is the sonic vector with the tremolo applied to it.

    See Also
    --------
    V : an oscillation of pitch.
    FM : a linear oscillation of fundamental frequency.
    AM : a linear oscillation of amplitude.

    Examples
    --------
    >>> W(V()*A())  # writes a WAV file of a note with tremolo
    >>> s = H( [V()*A(fa=i, V_dB=j) for i, j in zip([6, 15, 100], [2, 1, 20])] )
    # OR
    >>> s = H( [A(fa=i, V_dB=j, sonic_vector=V()) for i, j in zip([6, 15, 100], [2, 1, 20])] )
    >>> envelope2 = A(440, 1.5, 60)  # a lengthy envelope

    Notes
    -----
    In the MASS framework implementation, for obtaining a sound with a tremolo (or AM),
    the tremolo pattern is considered separately from a synthesis of the sound.

    The vibrato and FM patterns are considering when synthesizing the sound.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    Lambda = n.floor(f_s*d)
    ii = n.arange(Lambda)
    Lt = float(len(taba))
    Gammaa = n.floor(ii*fa*Lt/f_s).astype(n.int)  # indexes for LUT
    # amplitude variation in each sample
    T = taba[Gammaa_i%int(Lt)] 
    T = 10.**(T*V_dB/20.)
    return T


def AD(d=2, A=10, D=20, S=-20, R=100, xi=1e-2, transisions="exp", alpha=1, to_zero=0, nsamples=0, sonic_vector=0):
    """
    Synthesize a ADSR envelope
    
    ADSR (Atack, Decay, Sustain, Release) is a very traditional
    loudness envelope in sound synthesis.
    
    Parameters
    ----------
    d : scalar
        The duration of the envelope in milliseconds.
    A : attack
        The duration of the Attack in milliseconds.
    D : scalar
        The duration of the Decay in milliseconds.
    S : scalar
        The Sustain level after the Decay in decibels. (Usually negative.)
    R : scalar
        The duration of the Release in milliseconds.
    transitions : string
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    alpha : scalar or array_like
        An index to make the logarithmic fade slower or faster [1].
        Ignored it transitions="linear".
        If it is an array_like, it should hold three values to be used
        in Attack, Decay and Release.
    to_zero : scalar
        The duration in seconds for linearly departing from zero
        in the Attack and reaching the value of zero at the end
        of the Release.
        Is ignored if transitions="linear".
    nsamples : scalar
        The number of samples of the envelope. If supplied, d is ignired.
    sonic_vector : array_like
        Samples for the tremolo to be applied ob. If supplied, d and nsamples are ignored.

    Returns
    -------
    AD : ndarray
        A numpy array where each value is a value of the envelope for the PCM samples.
        If sonic_vector is input, AD is the sonic vector with the tremolo applied to it.

    See Also
    --------
    T : an oscillation of loudness.

    Examples
    --------
    >>> W(V()*AD())  # writes a WAV file of a note with ADSR envelope
    >>> s = H( [V()*AD(A=i, R=j) for i, j in zip([6, 50, 300], [100, 10, 200])] )
    # OR
    >>> s = H( [AD(A=i, R=j, sonic_vector=V()) for i, j in zip([6, 15, 100], [2, 1, 20])] )
    >>> envelope = AD(d=440, A=10e3, D=0, R=5e3)  # a lengthy envelope

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    a_S=10**(S/20.)
    Lambda=len(som)
    Lambda_A=int(A*f_s*0.001)
    Lambda_D=int(D*f_s*0.001)
    Lambda_R=int(R*f_s*0.001)

    ii=n.arange(Lambda_A,dtype=n.float)
    A=ii/(Lambda_A-1)
    A_i=A
    ii=n.arange(Lambda_A,Lambda_D+Lambda_A,dtype=n.float)
    D=1-(1-a_S)*(   ( ii-Lambda_A )/( Lambda_D-1) )
    A_i=n.hstack(  (A_i, D  )   )
    S=n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D),dtype=n.float)*a_S
    A_i=n.hstack( ( A_i, S )  )
    ii=n.arange(Lambda-Lambda_R,Lambda,dtype=n.float)
    R=a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
    A_i=n.hstack(  (A_i,R)  )

    return som*A_i


def L(d=2, dB=10, to = True, method="exp", dev=0, alpha):
    """
    An envelope for loudness transition.

    Parameters
    ----------
    dev : scalar
        The deviation of the transition.
        If method="exp" the deviation is in decibels.
        If method="linear" the deviation is in terms of amplitude.
    to : boolean
        If True, the transition ends at the deviation.
        If False, the transition starts at the deviation.
    method : string
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    alpha : scalar or array_like
        An index to make the logarithmic fade slower or faster [1].
        Ignored it transitions="linear".
    Returns
    -------
    T : ndarray
        A numpy array where each value is a value of the envelope for the PCM samples.
        If sonic_vector is input, T is the sonic vector with the tremolo applied to it.

    See Also
    --------
    T : an oscillation of loudness.
    AD : an ADSR envelope.

    Examples
    --------
    >>> W(V()*L())  # writes a WAV file of a loudness transition
    >>> s = H( [V()*L(dev=i, method=j) for i, j in zip([6, -50, 2.3], ["exp", "exp", "linear"])] )
    # OR
    >>> s = H( [L(dev=i, method=j, sonic_vector=V()) for i, j in zip([6, -50, 2.3], ["exp", "exp", "linear"])] )
    >>> envelope = L(d=10, dev=-80, to=False, alpha=2)  # a lengthy fade in 

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)



    """
    if method == "linear":
        


def F():
    """
    A fade in or out.

    Implements the loudness transitions and asserts that it reaches
    zero amplitude.
    """
