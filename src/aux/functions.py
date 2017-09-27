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

def __s(sonic_array=n.random.uniform(size=100000), filename="asound.wav", f_s=44100, adsr=True):
    """A minimal approach to writing 16 bit WAVE files.
    
    One can also use, for example:
        import sounddevice as S
        S.play(array) # the array must have values between -1 and 1"""

    # to write the file using XX bits per sample
    # simply use s = n.intXX(__n(sonic_array)*(2**(XX-1)-1))
    s = n.int16(AD(sonic_vector=__n(sonic_array), S=0)*32767)
    w.write(filename, f_s, s)

def W(fn, fs, sa): 
    """To mimic scipy.io.wavefile input"""
    __s(sa, fn, f_s=44100)


###################
# Synthesis
f_s = 44100  # Hz, standard sample rate

# very large tables, we are not worried about real time
# use Lt = 1024 if in need of better performance
Lambda_tilde=Lt=1024*16

# Sine
foo = n.linspace(0, 2*n.pi,Lt, endpoint=False)
S = n.sin(foo)  # um período da senóide com T amostras

# Square
Q = n.hstack(  ( n.ones(Lt/2)*-1, n.ones(Lt/2) )  )

# Triangular
foo = n.linspace(-1, 1, Lt/2, endpoint=False)
Tr = n.hstack(  ( foo, foo[::-1] )   )

# Sawtooth
D = n.linspace(-1, 1, Lt)


def N(f=220, d=2, tab=Tr, dB=0, nsamples=0, fs=44100):
    """
    Synthesize a basic musical note.

    Parameters
    ----------
    f : scalar
        The frequency of the note in Hertz.
    d : scalar
        The duration of the note in seconds.
    tab : array_like
        The table with the waveform to synthesize the sound.
    nsamples : scalar
        The number of samples in the sound.
        If not 0, d is ignored.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    V : a note with vibrato.

    Examples
    --------
    >>> W(N())  # writes a WAV file of a note
    >>> s = H( [N(i, j) for i, j in zip([200, 500, 100], [2, 1, 2])] )
    >>> s2 = N(440, 1.5, tab=D)

    Notes
    -----
    In the MASS framework implementation,
    for a sound with a vibrato (or FM) to be synthesized using LUT,
    the vibrato pattern is considered when performing the lookup calculations.

    The tremolo and AM patterns are implemented as separate amplitude envelopes.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if not nsamples:
        nsamples = int(d*fs)
    samples = n.arange(nsamples)
    l = len(tab)
    Gamma = (samples*f*l/fs).astype(n.int)
    s = tab[ Gamma % l ]
    return s


def V(f=220, d=2, fv=4, nu=2, alpha=1, tab=Tr, tabv=S, nsamples=0, fs=44100):
    """
    Synthesize a musical note with a vibrato.
    
    Set fv=0 (or use N()) for a note without vibrato.
    A vibrato is an oscillatory pattern of pitch [1].
    
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
        The table with the waveform for the vibrato oscillatory pattern.
    alpha : scalar
        An index to begin the transitions faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
    nsamples : scalar
        The number of samples in the sound.
        If supplied, d is ignored.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    T : a tremolo, an oscillation of loudness.
    FM : a linear oscillation of the fundamental frequency.
    AM : a linear oscillation of amplitude.
    V_ : a shorthand to render a note with vibrato using
        a reference frequency and a pitch interval.

    Examples
    --------
    >>> W(V())  # writes a WAV file of a note
    >>> s = H( [V(i, j) for i, j in zip([200, 500, 100], [2, 1, 2])] )
    >>> s2 = V(440, 1.5, 6, 1)

    Notes
    -----
    In the MASS framework implementation,
    for a sound with a vibrato (or FM) to be synthesized using LUT,
    the vibrato pattern is considered when performing the lookup calculations.

    The tremolo and AM patterns are implemented as separate amplitude envelopes.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if nsamples:
        Lambda = nsamples
    else:
        Lambda = int(fs*d)
    samples = n.arange(Lambda)
    lv = len(tabv)

    Gammav = (samples*fv*lv/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv = tabv[ Gammav % lv ] 

    # frequency in Hz at each sample
    if alpha == 1:
        F = f*2.**(  Tv*nu/12  ) 
    else:
        F = f*2.**(  (Tv*nu/12)**alpha  ) 
    l = len(tab)
    D_gamma = F*(l/fs)  # shift in table between each sample
    Gamma = n.cumsum(D_gamma).astype(n.int)  # total shift at each sample
    s = tab[ Gamma % l ]  # final sample lookup
    return s


def T(d=2, fa=2, dB=10, taba=S, nsamples=0, sonic_vector=0, fs=44100):
    """
    Synthesize a tremolo envelope or apply it to a sound.
    
    Set fa=0 for a constant envelope with value 1.
    A tremolo is an oscillatory pattern of loudness [1].
    
    Parameters
    ----------
    d : scalar
        The duration of the envelope in seconds.
    fa : scalar
        The frequency of the tremolo oscillations in Hertz.
    dB : scalar
        The maximum deviation of loudness in the tremolo in decibels.
    taba : array_like
        The table with the waveform for the tremolo oscillatory pattern.
    nsamples : scalar
        The number of samples of the envelope. If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the tremolo to be applied ob.
        If supplied, d and nsamples are ignored.
    fs : scalar
        The sample rate.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a PCM sample of the envelope
        if sonic_vector is 0.
        If sonic_vector is input, s is the sonic vector with the tremolo applied to it.

    See Also
    --------
    V : a musical note with an oscillation of pitch.
    FM : a linear oscillation of fundamental frequency.
    AM : a linear oscillation of amplitude.

    Examples
    --------
    >>> W(V()*A())  # writes a WAV file of a note with tremolo
    >>> s = H( [V()*A(fa=i, dB=j) for i, j in zip([6, 15, 100], [2, 1, 20])] )
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
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """

    if type(sonic_vector) == n.ndarray:
        Lambda = len(sonic_vector)
    elif nsamples:
        Lambda = nsamples
    else:
        Lambda = n.floor(fs*d)
    ii = n.arange(Lambda)
    l = len(taba)
    Gammaa = (ii*fa*l/fs).astype(n.int)  # indexes for LUT
    # amplitude variation in each sample
    Ta = taba[ Gammaa % Lt ] 
    T = 10.**(Ta*dB/20)
    if type(sonic_vector) == n.ndarray:
        return T*sonic_vector
    else:
        return T


def AD(d=2, A=10, D=20, S=-10, R=100, trans="exp", alpha=1, dB=-80, to_zero=1, nsamples=0, sonic_vector=0, fs=44100):
    """
    Synthesize an ADSR envelope [1].
    
    ADSR (Atack, Decay, Sustain, Release) is a very traditional
    loudness envelope in sound synthesis.
    
    Parameters
    ----------
    d : scalar
        The duration of the envelope in seconds.
    A : scalar
        The duration of the Attack in milliseconds.
    D : scalar
        The duration of the Decay in milliseconds.
    S : scalar
        The Sustain level after the Decay in decibels.
        Usually negative.
    R : scalar
        The duration of the Release in milliseconds.
    trans : string
        "exp" for exponential transitions of amplitude 
        (linear loudness).
        "linear" for linear transitions of amplitude.
    alpha : scalar or array_like
        An index to make the exponential fade slower or faster [1].
        Ignored it transitions="linear".
        If it is an array_like, it should hold three values to be used
        in Attack, Decay and Release.
    dB ; scalar or array_like
        The decibels deviation to reach before using a linear fade to reach zero amplitude.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Ignored if trans="linear".
    to_zero : scalar or array_like
        The duration in milliseconds for linearly departing from zero
        in the Attack and reaching the value of zero at the end
        of the Release.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Is ignored if transitions="linear".
    nsamples : scalar
        The number of samples of the envelope.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the tremolo to be applied to.
        If supplied, d and nsamples are ignored.
    fs : scalar
        The sample rate.

    Returns
    -------
    AD : ndarray
        A numpy array where each value is a value of
        the envelope for the PCM samples if sonic_array is 0.
        If sonic_vector is input,
        AD is the sonic vector with the tremolo applied to it.

    See Also
    --------
    T : an oscillation of loudness.
    L : a loudness transition.
    F : a fade in or fade out.

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
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) == n.ndarray:
        Lambda = len(sonic_vector)
    elif nsamples:
        Lambda = nsamples
    else:
        Lambda = int(d*fs)
    Lambda_A = int(A*fs*0.001)
    Lambda_D = int(D*fs*0.001)
    Lambda_R = int(R*fs*0.001)

    perc = 100*to_zero/A
    A = F(out=0, method=trans, alpha=alpha, dB=dB, perc=perc, nsamples=Lambda_A)
    D = L(dev=S, method=trans, alpha=alpha, nsamples=Lambda_D)
    perc = 100*to_zero/R
    a_S = 10**(S/20.)
    S = n.ones(Lambda-(Lambda_A+Lambda_R+Lambda_D))*a_S
    R = F(method=trans, alpha=alpha, dB=dB, perc=perc, nsamples=Lambda_R)*a_S

    AD = n.hstack((A,D,S,R))
    if type(sonic_vector) == n.ndarray:
        return sonic_vector*AD
    else:
        return AD


def L(d=2, dev=10, alpha=1, to=True, method="exp", nsamples=0, sonic_vector=0, fs=44100):
    """
    An envelope for linear or exponential (linean loudness) transition of amplitude.

    Parameters
    ----------
    d : scalar
        The duration of the sound in samples.
    dev : scalar
        The deviation of the transition.
        If method="exp" the deviation is in decibels.
        If method="linear" the deviation is amplitude proportion.
    alpha : scalar or array_like
        An index to make the exponential fade slower or faster [1].
        Ignored it method="linear".
    to : boolean
        If True, the transition ends at the deviation.
        If False, the transition starts at the deviation.
    method : string
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    nsamples : scalar
        The number of samples of the envelope.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the envelope to be applied to.
        If supplied, d and nsamples are ignored.
    fs : scalar
        The sample rate. Only used if nsamples and sonic_array are not supplied.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a value of the envelope for the PCM samples.
        If sonic_vector is supplied,
        T is the sonic vector with the tremolo applied to it.

    See Also
    --------
    T : an oscillation of loudness.
    AD : an ADSR envelope.
    F : fade in and out.

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
    if type(sonic_vector) == n.ndarray:
        N = len(sonic_vector)
    elif nsamples:
        N = nsamples
    else:
        N = int(fs*d)
    N_ = N-1
    samples = n.arange(N)
    if method == "linear":
        if to:
            a0 = 1
            al = dev
        else:
            a0 = dev
            al = 1
        ai = a0 + (al - a0)*samples/N_
    if method == "exp":
        if to:
            if alpha != 1:
                samples_ = (samples/N_)**alpha
            else:
                samples_ = (samples/N_)
        else:
            if alpha != 1:
                samples_ = ( (N_-samples)/N_)**alpha
            else:
                samples_ = ( (N_-samples)/N_)
        ai = 10**(samples_*dev/20)
    if type(sonic_vector) == n.ndarray:
        return ai*sonic_vector
    else:
        return ai
        

def F(d=2, out=True, method="exp", dB=-80, alpha=1, perc=1, nsamples=0, sonic_vector=0, fs=44100):
    """
    A fade in or out.

    Implements the loudness transition and asserts that it reaches
    zero amplitude.

    Parameters
    ----------
    d : scalar
        The duration in seconds of the fade.
    out : boolean
        If True, the fade is a fade out, else it is a fade in.
    method : string
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    dB : scalar
        The decibels from which to use the linear transition to reach zero.
        Not used if method="linear"
    alpha : scalar
        An index to make the exponential fade slower or faster [1].
        Ignored it transitions="linear". 
    perc : scalar
        The percentage of the fade that is linear to assure it reaches zero.
        Has no effect if method="linear".
    nsamples : scalar
        The number of samples of the fade. If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the fade to be applied to.
        If supplied, d and nsamples are ignored.
    fs : scalar
        The sample rate. Only used if nsamples and sonic_array are not supplied.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a value of the envelope for the PCM samples.
        If sonic_vector is input, T is the sonic vector with the fade applied to it.

    See Also
    --------
    T : an oscillation of loudness.
    AD : an ADSR envelope.
    L : a transition of loudness.

    Examples
    --------
    >>> W(V()*F())  # writes a WAV file with a fade in
    >>> s = H( [V()*F(out=i, method=j) for i, j in zip([1, 0, 1], ["exp", "exp", "linear"])] )
    # OR
    >>> s = H( [F(out=i, method=j, sonic_vector=V()) for i, j in zip([1, 0, 1], ["exp", "exp", "linear"])] )
    >>> envelope = F(d=10, out=0, perc=0.1)  # a lengthy fade in 

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) == n.ndarray:
        N = len(sonic_vector)
    elif nsamples:
        N = nsamples
    else:
        N = int(fs*d)
    if method == "linear":
        if out:
            ai = L(method="linear", dev=0, nsamples=N)
        else:
            ai = L(method="linear", to=0, dev=0, nsamples=N)
    if method == "exp":
        N0 = int(N*perc/100)
        N1 = N - N0
        if out:
            ai1 = L(dev=dB, alpha=alpha, nsamples=N1)
            if N0:
                ai0 = L(method="linear", dev=0, nsamples=N0)*ai1[-1]
            else:
                ai0 = []
            ai = n.hstack((ai1, ai0))
        else:
            ai1 = L(dev=dB, to=0, alpha=alpha, nsamples=N1)
            if N0:
                ai0 = L(method="linear", to=0, dev=0, nsamples=N0)*ai1[0]
            else:
                ai0 = []
            ai = n.hstack((ai0, ai1))
    if type(sonic_vector) == n.ndarray:
        return ai*sonic_vector
    else:
        return ai


def P(f1=220, f2=440, d=2, alpha=1, tab=S, nsamples=0, fs=44100):
    """
    A note with a pitch transition, a glissando.

    Parameters
    ----------
    f1 : scalar
        The starting frequency.
    f2 : scalar
        The final frequency.
    d : scalar
        The duration of the sound.
    nsamples : scalar
        The number of samples of the sound.
        If supplied, d is not used.
    alpha : scalar
        An index to begin the transitions faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
    tab : array_like
        The table with the waveform to synthesize the sound.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    """
    if nsamples:
        Lambda = nsamples
    else:
        Lambda = int(fs*d)
    samples = n.arange(Lambda)
    if alpha != 1:
        F = f1*(f2/f1)**( (samples / (Lambda-1))**alpha )
    else:
        F = f1*(f2/f1)**( samples / (Lambda-1) )
    l = len(tab)
    Gamma = n.cumsum( F*l/fs ).astype(n.int)
    s = tab[ Gamma % l ]
    return s


def PV(f1=220, f2=440, d=2, fv=4, nu=2, alpha=1, alphav=1, tab=S, tabv=S, nsamples=0, fs=44100):
    """
    A note with a pitch transition (a glissando) and a vibrato.

    Parameters
    ----------
    f1 : scalar
        The starting frequency.
    f2 : scalar
        The final frequency.
    d : scalar
        The duration of the sound.
    fv : scalar
        The frequency of the vibrato oscillations in Hertz.
    nu : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    tab : array_like
        The table with the waveform to synthesize the sound.
    tabv : array_like
        The table with the waveform for the vibrato oscillatory pattern.
    alpha : scalar
        An index to begin the transitions faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
    alphav : scalar
        An index to distort the pitch deviation of the vibrato. 
    nsamples : scalar
        The number of samples of the sound.
        If supplied, d is not used.
    tab : array_like
        The table with the waveform to synthesize the sound.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    """
    if nsamples:
        Lambda = nsamples
    else:
        Lambda = int(fs*d)
    samples = n.arange(Lambda)

    lv = len(tabv)

    Gammav = (samples*fv*lv/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv = tabv[ Gammav % lv ] 

    if alpha != 1 or alphav != 1:
        F = f1*(f2/f1)**( (samples / (Lambda-1))**alpha )*2.**( (Tv*nu/12)**alphav )
    else:
        F = f1*(f2/f1)**( samples / (Lambda-1) )*2.**( (Tv*nu/12)**alpha )
    l = len(tab)
    Gamma = n.cumsum( F*l/fs ).astype(n.int)
    s = tab[ Gamma % l ]
    return s


def VV(f=220, d=2, fv1=2, fv2=6, nu1=2, nu2=.5, alphav1=1, alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100):
    """
    A note with a vibrato that also has a secondary oscillatory pattern.

    Parameters
    ----------
    f : scalar
        The frequency of the note.
    d : scalar
        The duration of the sound.
    fv1 : scalar
        The frequency of the vibrato.
    fv2 : scalar
        The secondary of the vibrato.
    nu1 : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    nu1 : scalar
        The maximum deviation in semitones of pitch in the
        secondary pattern of the vibrato.
    tab : array_like
        The table with the waveform to synthesize the sound.
    alphav1 : scalar
        An index to distort the pitch deviation of the vibrato. 
    alphav2 : scalar
        An index to distort the pitch deviation of the 
        secondary pattern of the vibrato. 
    tab : array_like
        The table with the waveform to synthesize the sound.
    tabv1 : array_like
        The table with the waveform for the vibrato oscillatory pattern.
    tabv2 : array_like
        The table with the waveform for the
        secondary pattern of the vibrato.
    nsamples : scalar
        The number of samples of the sound.
        If supplied, d is not used.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    """
    if nsamples:
        Lambda = nsamples
    else:
        Lambda = int(fs*d)
    samples = n.arange(Lambda)

    lv1 = len(tabv1)
    Gammav1 = (samples*fv1*lv1/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv1 = tabv1[ Gammav1 % lv1 ] 

    lv2 = len(tabv2)
    Gammav2 = (samples*fv2*lv2/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv2 = tabv1[ Gammav2 % lv2 ] 

    if alphav1 != 1 or alphav2 != 1:
        F = f*2.**( (Tv1*nu1/12)**alphav1 )*2.**( (Tv2*nu2/12)**alphav2 )
    else:
        F = f*2.**( (Tv1*nu1/12))*2.**( (Tv2*nu2/12))
    l = len(tab)
    Gamma = n.cumsum( F*l/fs ).astype(n.int)
    s = tab[ Gamma % l ]
    return s


def PVV(f1=220, f2=440, d=2, fv1=2, fv2=6, nu1=2, nu2=.5, alpha=1, alphav1=1, alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100):
    """
    A note with a vibrato that also has a secondary oscillatory pattern.

    Parameters
    ----------
    f : scalar
        The frequency of the note.
    d : scalar
        The duration of the sound.
    fv1 : scalar
        The frequency of the vibrato.
    fv2 : scalar
        The secondary of the vibrato.
    nu1 : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    nu1 : scalar
        The maximum deviation in semitones of pitch in the
        secondary pattern of the vibrato.
    tab : array_like
        The table with the waveform to synthesize the sound.
    alphav1 : scalar
        An index to distort the pitch deviation of the vibrato. 
    alphav2 : scalar
        An index to distort the pitch deviation of the 
        secondary pattern of the vibrato. 
    tab : array_like
        The table with the waveform to synthesize the sound.
    tabv1 : array_like
        The table with the waveform for the vibrato oscillatory pattern.
    tabv2 : array_like
        The table with the waveform for the
        secondary pattern of the vibrato.
    nsamples : scalar
        The number of samples of the sound.
        If supplied, d is not used.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    """
    if nsamples:
        Lambda = nsamples
    else:
        Lambda = int(fs*d)
    samples = n.arange(Lambda)

    lv1 = len(tabv1)
    Gammav1 = (samples*fv1*lv1/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv1 = tabv1[ Gammav1 % lv1 ] 

    lv2 = len(tabv2)
    Gammav2 = (samples*fv2*lv2/fs).astype(n.int)  # LUT indexes
    # values of the oscillatory pattern at each sample
    Tv2 = tabv1[ Gammav2 % lv2 ] 

    if alpha !=1 or alphav1 != 1 or alphav2 != 1:
        F = f1*(f2/f1)**( (samples / (Lambda-1))**alpha )*2.**( (Tv1*nu1/12)**alphav1 )*2.**( (Tv2*nu2/12)**alphav2 )
    else:
        F = f1*(f2/f1)**( samples / (Lambda-1) )*2.**( (Tv1*nu1/12))*2.**( (Tv2*nu2/12))
    l = len(tab)
    Gamma = n.cumsum( F*l/fs ).astype(n.int)
    s = tab[ Gamma % l ]
    return s

# def PV_(f=[220, 440, 330], d=[[2,3],[2,5,3], [2,5,6,1,.4]], fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]], alpha=[[1, 1] , [1, 1, 1], [1, 1, 1, 1, 1]], tab=[[Tr,Tr], [S,Tr,S], [S,S,S,S,S]], nsamples=0, fs=44100):
# def PV_(f=[220,440,440,220,440,220], d=[[2,9,4,.5,4],[5],[7,4]], fv=[[6],[2,11]], nu=[[2],[3,3]], alpha=[[1,1,1,1,.3],[1],[1,1]], tab=[[Tr,Tr,Tr,Tr,Tr],[S],[S, S]], nsamples=0, fs=44100):
# def PV_(f=[220,440,220,440,220,440,220], d=[[2,2,2,2,2]], fv=[], nu=[], alpha=[[1,2.5,.2,10,.1]], tab=[[Tr,Tr,Tr,Tr,Tr]], nsamples=0, fs=44100):
# def PV_(f=[220,440,220,440,220,440,220], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.1,1]], tab=[[Tr,Tr,Tr,Tr,Tr]], nsamples=0, fs=44100):
# def PV_(f=[220,440,220,440,220,440,220], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.2,1]], tab=[[S]*6], nsamples=0, fs=44100):
def PV_(f=[440,220,440,220,440,220, 440], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.2,1]], tab=[[Tr]*6], nsamples=0, fs=44100):
# def PV_(f=[220,440], d=[[2]], fv=[], nu=[], alpha=[[1]], tab=[[Tr]], nsamples=0, fs=44100):
    """
    A note with an arbitrary sequence of pitch transition and meta-vibrato.

    A meta-vibrato consists in multiple vibratos.

    Parameters
    ----------
    f : array_like
        The frequencies of the note at each point.
    d : array_like
        The durations transisions and then of the vibratos.
    fv :  array_like
        The frequencies of each vibrato.
    nu : array_like
        The maximum deviation of pitch in the vibratos in semitones.
    tab : array_like
        The tables with the waveforms to synthesize the sound
        and for the oscillatory patterns of the vibratos.
    alpha : scalar
        An index to distort the pitch deviations of the transitions
        and the vibratos
    nsamples : scalar
        The number of samples of the sound.
        If supplied, d is not used.
    fs : scalar
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    """
    # transition contributions
    F_ = []
    for i, dur in enumerate(d[0]):
        Lambda_ = int(fs*dur)
        samples = n.arange(Lambda_)
        f1, f2 = f[i:i+2]
        if alpha[0][i] != 1:
            F = f1*(f2/f1)**( (samples / (Lambda_-1))**alpha[0][i] )
        else:
            F = f1*(f2/f1)**( samples / (Lambda_-1) )
        F_.append(F)
    Ft = n.hstack(F_)

    # vibrato contributions
    V_=[]
    for i, vib in enumerate(d[1:]):
        v_=[]
        for j, dur in enumerate(vib):
            samples = n.arange(dur*fs)
            lv = len(tab[i+1][j])
            Gammav = (samples*fv[i][j]*lv/fs).astype(n.int)  # LUT indexes
            # values of the oscillatory pattern at each sample
            Tv = tab[i+1][j][ Gammav % lv ] 
            if alpha[i+1][j] != 0:
                F = 2.**( (Tv*nu[i][j]/12)**alpha[i+1][j] )
            else:
                F = 2.**( Tv*nu[i][j]/12 )
            v_.append(F)

        V=n.hstack(v_)
        V_.append(V)

    # find maximum size, fill others with ones
    V_ = [Ft] + V_
    amax = max([len(i) for i in V_])
    for i, contrib in enumerate(V_[1:]):
        V_[i+1] = n.hstack(( contrib, n.ones(amax - len(contrib)) ))
    V_[0] = n.hstack(( V_[0], n.ones(amax - len(V_[0]))*f[-1] ))

    F = n.prod(V_, axis=0)
    l = len(tab[0][0])
    Gamma = n.cumsum( F*l/fs ).astype(n.int)
    s_ = []
    pointer = 0
    for i, t in enumerate(tab[0]):
        l = len(t)
        Lambda = int(fs*d[0][i])
        s = t[ Gamma[pointer:pointer+Lambda] % l ]
        pointer += Lambda
        s_.append(s)
    s =  t[ Gamma[pointer:] % l ]
    s_.append(s)
    s = n.hstack(s_)
    return s

