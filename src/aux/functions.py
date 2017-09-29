import numpy as n
from scipy.io import wavfile as w
import doctest

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

H = n.hstack
#####################
# IO
def __n(sonic_vector, remove_bias=True):
    """Normalize mono sonic_vector.
    
    The final array will have values only between -1 and 1.
    
    Parameters
    ----------
    sonic_vector : array_like
        A (nsamples,) shaped array.
    remove_bias : boolean
        Whether to remove or not the bias (or offset)
    
    Returns
    -------
    s : ndarray
        A numpy array with values between -1 and 1.
    remove_bias : boolean
        Whether to remove or not the bias (or offset)
    """

    t = n.array(sonic_vector)
    if n.all(t==0):
        return t
    else:
        s = ( (t-t.min()) / (t.max() -t.min()) )*2. -1.
        f = n.fft.fft(s)
        if remove_bias:
            f[0] = 0  # removing bias (or offset)
            s = n.fft.ifft(f).real
        return s


def __ns(sonic_vector, remove_bias=True, normalize_sep=False):
    """Normalize a stereo sonic_vector.
    
    The final array will have values only between -1 and 1.
    
    Parameters
    ----------
    sonic_vector : array_like
        A (2, nsamples) shaped array.
    remove_bias : boolean
        Whether to remove or not the bias (or offset)
    normalize_sep : boolean
        Set to True if each channel should be normalized
        separately. If False (default), the arrays will be
        rescaled in the same proportion
        (preserves loudness proportion).
    
    Returns
    -------
    s : ndarray
        A numpy array with values between -1 and 1.
    """

    t = n.array(sonic_vector)
    if n.all(t==0):
        return t
    else:
        if not normalize_sep:
            amb1 = t[0].max() - t[0].min()
            amb2 = t[1].max() - t[1].min()
            amb = max(amb1, amb2)
            t[0] = (t[0] - t[0].min())/amb
            t[1] = (t[1] - t[1].min())/amb
            s = t*2 - 1
        else:
            amb1 = t[0].max() - t[0].min()
            amb2 = t[1].max() - t[1].min()
            t[0] = (t[0] - t[0].min())/amb1
            t[1] = (t[1] - t[1].min())/amb2
            s = t*2 - 1
        if remove_bias:
            f = n.fft.fft(s[0])
            f[0] = 0  # removing bias (or offset)
            s[0] = n.fft.ifft(f)
            f = n.fft.fft(s[1])
            f[0] = 0  # removing bias (or offset)
            s[1] = n.fft.ifft(f)
        return s


monos = n.random.uniform(size=100000) 
def W(sonic_vector=monos, filename="asound.wav", fs=44100,
        fades=0, bit_depth=16, remove_bias=True):
    """Write a mono WAV file for a numpy array.
    
    One can also use, for example:
        import sounddevice as S
        S.play(__n(array))
    
    Parameters
    ----------
    sonic_vector : array_like
        The PCM samples to be written as a WAV sound file.
        The samples are always normalized by __n(sonic_vector)
        to have samples between -1 and 1.
    filename : string
        The filename to use for the file to be written.
    fs : scalar
        The sample frequency.
    fades : integer
        Set to number of milliseconds you want for the
        fade in and out (to avoid clicks).
    bit_depth : integer
        The number of bits in each sample of the final file.
    remove_bias : boolean
        Whether to remove or not the bias (or offset)

    See Also
    --------
    __n : Normalizes an array to [-1,1]
    W_ : Writes an array with the same arguments
    and order of them as scipy.io.wavfile.
    WS ; Write a stereo file.
    
    """
    s = __n(sonic_vector)*(2**(bit_depth-1)-1)
    if fades:
        s = AD(A=fades, S=0, R=fades, sonic_vector=s)
    if bit_depth not in (8, 16, 32, 64):
        print("bit_depth values allowed are only 8, 16, 32 and 64")
        print("File {} not written".format(filename))
    nn = eval("n.int"+str(bit_depth))
    s = nn(s)
    w.write(filename, fs, s)


stereos = n.vstack((n.random.uniform(size=100000), n.random.uniform(size=100000)))

def WS(sonic_vector=stereos, filename="asound.wav", fs=44100,
        fades=0, bit_depth=16, remove_bias=True, normalize_sep=False):
    """Write a stereo WAV files for a numpy array.
    
    Parameters
    ----------
    sonic_vector : array_like
        The PCM samples to be written as a WAV sound file.
        The samples are always normalized by __n(sonic_vector)
        to have samples between -1 and 1 and remove the offset.
        Use array of shape (nchannels, nsamples).
    filename : string
        The filename to use for the file to be written.
    fs : scalar
        The sample frequency.
    fades : integer
        Set to number of milliseconds you want for the
        fade in and out (to avoid clicks).
    bit_depth : integer
        The number of bits in each sample of the final file.
    remove_bias : boolean
        Whether to remove or not the bias (or offset)
    normalize_sep : boolean
        Set to True if each channel should be normalized
        separately. If False (default), the arrays will be
        rescaled in the same proportion.

    See Also
    --------
    __ns : Normalizes a stereo array to [-1,1]
    W ; Write a mono file.
    
    """
    s = __ns(sonic_vector, remove_bias, normalize_sep)*(2**(bit_depth-1)-1)
    if fades:
        s = ADS(A=fades, S=0, R=fades, sonic_vector=s)
    if bit_depth not in (8, 16, 32, 64):
        print("bit_depth values allowed are only 8, 16, 32 and 64")
        print("File {} not written".format(filename))
    nn = eval("n.int"+str(bit_depth))
    s = nn(s)
    w.write(filename, fs, s.T)


def W_(fn, fs, sa): 
    """To mimic scipy.io.wavefile input"""
    W(sa, fn, fs=44100)


###################
# Synthesis
fs = 44100  # Hz, standard sample rate

# very large tables, we are not worried about real time
# use Lt = 1024 if in need of better performance
Lambda_tilde = Lt = 1024*16

# Sine
foo = n.linspace(0, 2*n.pi,Lt, endpoint=False)
S = n.sin(foo)  # one period of a sinusoid with Lt samples

# Square
Q = n.hstack(  ( n.ones(int(Lt/2))*-1, n.ones(int(Lt/2)) )  )

# Triangular
foo = n.linspace(-1, 1, Lt/2, endpoint=False)
Tr = n.hstack(  ( foo, foo[::-1] )   )

# Sawtooth
D = n.linspace(-1, 1, Lt)


def N(f=220, d=2, tab=Tr, nsamples=0, fs=44100):
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
    nsamples : integer
        The number of samples in the sound.
        If not 0, d is ignored.
    fs : integer
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the note.

    See Also
    --------
    V : A note with vibrato.
    T : A tremolo envelope.

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
    tab = n.array(tab)
    if not nsamples:
        nsamples = int(d*fs)
    samples = n.arange(nsamples)
    l = len(tab)

    Gamma = (samples*f*l/fs).astype(n.int)
    s = tab[ Gamma % l ]
    return s


def V(f=220, d=2, fv=4, nu=2, tab=Tr, tabv=S,
        alpha=1, nsamples=0, fs=44100):
    """
    Synthesize a musical note with a vibrato.
    
    Set fv=0 or nu=0 (or use N()) for a note without vibrato.
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
        An index to distort the vibrato [1]. 
        If alpha != 1, the vibrato is not of linear pitch.
    nsamples : integer
        The number of samples in the sound.
        If supplied, d is ignored.
    fs : integer
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the note.

    See Also
    --------
    N : A basic musical note without vibrato.
    T : A tremolo, an oscillation of loudness.
    FM : A linear oscillation of the frequency (not linear pitch).
    AM : A linear oscillation of amplitude (not linear loudness).
    V_ : A shorthand to render a note with vibrato using
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
    tab = n.array(tab)
    tabv = n.array(tabv)
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


def T(d=2, fa=2, dB=10, alpha=1, taba=S, nsamples=0, sonic_vector=0, fs=44100):
    """
    Synthesize a tremolo envelope or apply it to a sound.
    
    Set fa=0 or dB=0 for a constant envelope with value 1.
    A tremolo is an oscillatory pattern of loudness [1].
    
    Parameters
    ----------
    d : scalar
        The duration of the envelope in seconds.
    fa : scalar
        The frequency of the tremolo oscillations in Hertz.
    dB : scalar
        The maximum deviation of loudness in the tremolo in decibels.
    alpha : scalar
        An index to distort the tremolo pattern [1].
    taba : array_like
        The table with the waveform for the tremolo oscillatory pattern.
    nsamples : integer
        The number of samples of the envelope. If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the tremolo to be applied to.
        If supplied, d and nsamples are ignored.
    fs : integer
        The sample rate.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a PCM sample
        of the envelope.
        if sonic_vector is 0.
        If sonic_vector is input,
        T is the sonic vector with the tremolo applied to it.

    See Also
    --------
    V : A musical note with an oscillation of pitch.
    FM : A linear oscillation of fundamental frequency.
    AM : A linear oscillation of amplitude.

    Examples
    --------
    >>> W(V()*T())  # writes a WAV file of a note with tremolo
    >>> s = H( [V()*T(fa=i, dB=j) for i, j in zip([6, 15, 100], [2, 1, 20])] )  # OR
    >>> s = H( [T(fa=i, dB=j, sonic_vector=V()) for i, j in zip([6, 15, 100], [2, 1, 20])] )
    >>> envelope2 = T(440, 1.5, 60)  # a lengthy envelope

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

    taba = n.array(taba)
    if type(sonic_vector) in (n.ndarray, list):
        Lambda = len(sonic_vector)
    elif nsamples:
        Lambda = nsamples
    else:
        Lambda = n.floor(fs*d)
    samples = n.arange(Lambda)

    l = len(taba)
    Gammaa = (samples*fa*l/fs).astype(n.int)  # indexes for LUT
    # amplitude variation at each sample
    Ta = taba[ Gammaa % Lt ] 
    if alpha != 1:
        T = 10.**((Ta*dB/20)**alpha)
    else:
        T = 10.**(Ta*dB/20)
    if type(sonic_vector) in (n.ndarray, list):
        return T*sonic_vector
    else:
        return T


def AD(d=2, A=20, D=20, S=-5, R=50, trans="exp", alpha=1,
        dB=-80, to_zero=1, nsamples=0, sonic_vector=0, fs=44100):
    """
    Synthesize an ADSR envelope.
    
    ADSR (Atack, Decay, Sustain, Release) is a very traditional
    loudness envelope in sound synthesis [1].
    
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
        Ignored it transitions="linear" or alpha=1.
        If it is an array_like, it should hold three values to be used
        in Attack, Decay and Release.
    dB : scalar or array_like
        The decibels deviation to reach before using a linear fade
        to reach zero amplitude.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Ignored if trans="linear".
    to_zero : scalar or array_like
        The duration in milliseconds for linearly departing from zero
        in the Attack and reaching the value of zero at the end
        of the Release.
        If it is an array_like, it should hold two values,
        one for Attack and another for Release.
        Is ignored if trans="linear".
    nsamples : integer
        The number of samples of the envelope.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the ADSR envelope to be applied to.
        If supplied, d and nsamples are ignored.
    fs : integer
        The sample rate.

    Returns
    -------
    AD : ndarray
        A numpy array where each value is a value of
        the envelope for the PCM samples if sonic_vector is 0.
        If sonic_vector is input,
        AD is the sonic vector with the ADSR envelope applied to it.

    See Also
    --------
    T : An oscillation of loudness.
    L : A loudness transition.
    F : A fade in or fade out.

    Examples
    --------
    >>> W(V()*AD())  # writes a WAV file of a note with ADSR envelope
    >>> s = H( [V()*AD(A=i, R=j) for i, j in zip([6, 50, 300], [100, 10, 200])] )  # OR
    >>> s = H( [AD(A=i, R=j, sonic_vector=V()) for i, j in zip([6, 15, 100], [2, 2, 20])] )
    >>> envelope = AD(d=440, A=10e3, D=0, R=5e3)  # a lengthy envelope

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) in (n.ndarray, list):
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

    a_S = 10**(S/20.)
    S = n.ones( Lambda - (Lambda_A+Lambda_R+Lambda_D) )*a_S

    perc = 100*to_zero/R
    R = F(method=trans, alpha=alpha, dB=dB, perc=perc, nsamples=Lambda_R)*a_S

    AD = n.hstack((A,D,S,R))
    if type(sonic_vector) in (n.ndarray, list):
        return sonic_vector*AD
    else:
        return AD


def L(d=2, dev=10, alpha=1, to=True, method="exp",
        nsamples=0, sonic_vector=0, fs=44100):
    """
    An envelope for linear or exponential transition of amplitude.

    An exponential transition of loudness yields a linean
    transition of loudness (theoretically).

    Parameters
    ----------
    d : scalar
        The duration of the envelope in seconds.
    dev : scalar
        The deviation of the transition.
        If method="exp" the deviation is in decibels.
        If method="linear" the deviation is an amplitude proportion.
    alpha : scalar
        An index to make the transition slower or faster [1].
        Ignored it method="linear".
    to : boolean
        If True, the transition ends at the deviation.
        If False, the transition starts at the deviation.
    method : string
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    nsamples : integer
        The number of samples of the envelope.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the envelope to be applied to.
        If supplied, d and nsamples are ignored.
    fs : integer
        The sample rate.
        Only used if nsamples and sonic_vector are not supplied.

    Returns
    -------
    E : ndarray
        A numpy array where each value is a value of the envelope 
        for the PCM samples.
        If sonic_vector is supplied,
        ai is the sonic vector with the envelope applied to it.

    See Also
    --------
    L_ : An envelope with an arbitrary number of transitions.
    F : Fade in and out.
    AD : An ADSR envelope.
    T : An oscillation of loudness.

    Examples
    --------
    >>> W(V()*L())  # writes a WAV file of a loudness transition
    >>> s = H( [V()*L(dev=i, method=j) for i, j in zip([6, -50, 2.3], ["exp", "exp", "linear"])] )  # OR
    >>> s = H( [L(dev=i, method=j, sonic_vector=V()) for i, j in zip([6, -50, 2.3], ["exp", "exp", "linear"])] )
    >>> envelope = L(d=10, dev=-80, to=False, alpha=2)  # a lengthy fade in 

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) in (n.ndarray, list):
        N = len(sonic_vector)
    elif nsamples:
        N = nsamples
    else:
        N = int(fs*d)
    samples = n.arange(N)
    N_ = N-1
    if method == "linear":
        if to:
            a0 = 1
            al = dev
        else:
            a0 = dev
            al = 1
        E = a0 + (al - a0)*samples/N_
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
        E = 10**(samples_*dev/20)
    if type(sonic_vector) in (n.ndarray, list):
        return E*sonic_vector
    else:
        return E
        

def F(d=2, out=True, method="exp", dB=-80, alpha=1, perc=1,
        nsamples=0, sonic_vector=0, fs=44100):
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
        "exp" for an exponential transition of amplitude (linear loudness).
        "linear" for a linear transition of amplitude.
    dB : scalar
        The decibels from which to reach before using
        the linear transition to reach zero.
        Not used if method="linear".
    alpha : scalar
        An index to make the exponential fade slower or faster [1].
        Ignored it transitions="linear". 
    perc : scalar
        The percentage of the fade that is linear to assure it reaches zero.
        Has no effect if method="linear".
    nsamples : integer
        The number of samples of the fade. If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the fade to be applied to.
        If supplied, d and nsamples are ignored.
    fs : integer
        The sample rate. Only used if nsamples and sonic_vector are not supplied.

    Returns
    -------
    T : ndarray
        A numpy array where each value is a value of the envelope for the PCM samples.
        If sonic_vector is input, T is the sonic vector with the fade applied to it.

    See Also
    --------
    AD : An ADSR envelope.
    L : A transition of loudness.
    L_ : An envelope with an arbitrary number or loudness transitions.
    T : An oscillation of loudness.

    Examples
    --------
    >>> W(V()*F())  # writes a WAV file with a fade in
    >>> s = H( [V()*F(out=i, method=j) for i, j in zip([1, 0, 1], ["exp", "exp", "linear"])] )  # OR
    >>> s = H( [F(out=i, method=j, sonic_vector=V()) for i, j in zip([1, 0, 1], ["exp", "exp", "linear"])] )
    >>> envelope = F(d=10, out=0, perc=0.1)  # a lengthy fade in 

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) in (n.ndarray, list):
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
    if type(sonic_vector) in (n.ndarray, list):
        return ai*sonic_vector
    else:
        return ai


def P(f1=220, f2=440, d=2, alpha=1, tab=S, nsamples=0, fs=44100):
    """
    A note with a pitch transition: a glissando.

    Parameters
    ----------
    f1 : scalar
        The starting frequency.
    f2 : scalar
        The final frequency.
    d : scalar
        The duration of the sound in seconds.
    alpha : scalar
        An index to begin the transition faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
    tab : array_like
        The table with the waveform to synthesize the sound.
    nsamples : integer
        The number of samples of the sound.
        If supplied, d is not used.
    fs : integer
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    N : A basic musical note without vibrato or pitch transition.
    V : A musical note with an oscillation of pitch.
    T : A tremolo, an oscillation of loudness.
    L : A transition of loudness.
    F : Fade in or out.

    Examples
    --------
    >>> W(P())  # writes file with a glissando
    >>> s = H( [P(i, j) for i, j in zip([220, 440, 4000], [440, 220, 220])] )
    >>> W(s)  # writes a file with glissandi

    """
    tab = n.array(tab)
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


def PV(f1=220, f2=440, d=2, fv=4, nu=2, alpha=1,
        alphav=1, tab=S, tabv=S, nsamples=0, fs=44100):
    """
    A note with a pitch transition (a glissando) and a vibrato.

    Parameters
    ----------
    f1 : scalar
        The starting frequency.
    f2 : scalar
        The final frequency.
    d : scalar
        The duration of the sound in seconds.
    fv : scalar
        The frequency of the vibrato oscillations in Hertz.
    nu : scalar
        The maximum deviation of pitch of the vibrato in semitones.
    alpha : scalar
        An index to begin the transitions faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
    alphav : scalar
        An index to distort the pitch deviation of the vibrato. 
    tab : array_like
        The table with the waveform to synthesize the sound.
    tabv : array_like
        The table with the waveform for the vibrato oscillatory pattern.
    nsamples : integer
        The number of samples of the sound.
        If supplied, d is not used.
    fs : integer
        The sample rate.

    Returns
    -------
    s : ndarray
        A numpy array where each value is a PCM sample of the sound.

    See Also
    --------
    P : A glissando.
    V : A musical note with an oscillation of pitch.
    N : A basic musical note without vibrato.
    T : A tremolo, an oscillation of loudness.
    F : Fade in and out.
    L : A transition of loudness.

    Examples
    --------
    >>> W(PV())  # writes file with a glissando and vibrato
    >>> s = H( [AD(sonic_vector=PV(i, j)) for i, j in zip([220, 440, 4000], [440, 220, 220])] )
    >>> W(s)  # writes a file with glissandi and vibratos

    """
    tab = n.array(tab)
    tabv = n.array(tabv)
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


def VV(f=220, d=2, fv1=2, fv2=6, nu1=2, nu2=4, alphav1=1,
        alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100):
    """
    A note with a vibrato that also has a secondary oscillatory pattern.

    Parameters
    ----------
    f : scalar
        The frequency of the note.
    d : scalar
        The duration of the sound in seconds.
    fv1 : scalar
        The frequency of the vibrato.
    fv2 : scalar
        The frequency of the secondary pattern of the vibrato.
    nu1 : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    nu2 : scalar
        The maximum deviation in semitones of pitch in the
        secondary pattern of the vibrato.
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
    PV : A note with a glissando and a vibrato.
    PVV : A note with a glissando and a vibrato with two oscillatory patterns.
    N : A basic musical note without vibrato.
    V : A musical note with an oscillation of pitch.
    T : A tremolo, an oscillation of loudness.
    F : Fade in and out.
    L : A transition of loudness.

    Examples
    --------
    >>> W(VV())  # writes file with a two simultaneous vibratos
    >>> s = H( [AD(sonic_vector=VV(fv1=i, fv2=j)) for i, j in zip([2, 6, 4], [8, 10, 15])] )
    >>> W(s)  # writes a file with two vibratos

    """
    tab = n.array(tab)
    tabv1 = n.array(tabv1)
    tabv2 = n.array(tabv2)
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


def PVV(f1=220, f2=440, d=2, fv1=2, fv2=6, nu1=2, nu2=.5, alpha=1,
        alphav1=1, alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100):
    """
    A note with a glissando and a vibrato that also has a secondary oscillatory pattern.

    Parameters
    ----------
    f1 : scalar
        The starting frequency.
    f2 : scalar
        The final frequency.
    d : scalar
        The duration of the sound in seconds.
    fv1 : scalar
        The frequency of the vibrato.
    fv2 : scalar
        The frequency of the secondary pattern of the vibrato.
    nu1 : scalar
        The maximum deviation of pitch in the vibrato in semitones.
    nu1 : scalar
        The maximum deviation in semitones of pitch in the
        secondary pattern of the vibrato.
    alpha : scalar
        An index to begin the transitions faster or slower. 
        If alpha != 1, the transition is not of linear pitch.
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
    PV : A note with a glissando and a vibrato.
    VV : A note with a vibrato with two oscillatory patterns.
    PV_ : A note with arbitrary pitch transitions and vibratos.
    V : a musical note with an oscillation of pitch.
    N : a basic musical note without vibrato.
    T : a tremolo, an oscillation of loudness.
    F : fade in or out.
    L : a transition of loudness.

    Examples
    --------
    >>> W(PVV())  # writes file with a two simultaneous vibratos and a glissando
    >>> s = H( [AD(sonic_vector=PVV(fv2=i, nu1=j)) for i, j in zip([330, 440, 100], [8, 2, 15])] )
    >>> W(s)  # writes a file with two vibratos and a glissando

    """
    tab = n.array(tab)
    tabv1 = n.array(tabv1)
    tabv2 = n.array(tabv2)
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

def PV_(f=[220, 440, 330], d=[[2,3],[2,5,3], [2,5,6,1,.4]],
        fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]],
        alpha=[[1, 1] , [1, 1, 1], [1, 1, 1, 1, 1]],
        tab=[[Tr,Tr], [S,Tr,S], [S,S,S,S,S]], nsamples=0, fs=44100):
    """
    A note with an arbitrary sequence of pitch transition and a meta-vibrato.

    A meta-vibrato consists in multiple vibratos.
    The sequence of pitch transitions is a glissandi.

    Parameters
    ----------
    f : list of lists of scalars
        The frequencies of the note at each end of the transitions.
    d : list of lists of scalars
        The durations of the transitions and then of the vibratos.
    fv :  list of lists of scalars
        The frequencies of each vibrato.
    nu : list of lists of scalars
        The maximum deviation of pitch in the vibratos in semitones.
    alpha : list of lists of scalars
        Indexes to distort the pitch deviations of the transitions
        and the vibratos.
    tab : list of lists of array_likes
        The tables with the waveforms to synthesize the sound
        and for the oscillatory patterns of the vibratos.
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
    PV : A note with a glissando and a vibrato.
    PVV : A note with a glissando and two vibratos.
    VV : A note with a vibrato with two oscillatory patterns.
    N : a basic musical note without vibrato.
    V : a musical note with an oscillation of pitch.
    T : a tremolo, an oscillation of loudness.
    F : fade in and out.
    L : a transition of loudness.

    Examples
    --------
    >>> W(PV_())  # writes file with glissandi and vibratos

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


def L_(d=[2,4,2], dev=[5,-10,20], alpha=[1,.5, 20], method=["exp", "exp", "exp"],
        nsamples=0, sonic_vector=0, fs=44100):
    """
    An envelope with linear or exponential transitions of amplitude.

    See L() for more details.

    Parameters
    ----------
    d : iterable
        The durations of the transitions in seconds.
    dev : iterable
        The deviation of the transitions.
        If method="exp" the deviation is in decibels.
        If method="linear" the deviation is an amplitude proportion.
    alpha : iterable
        Indexes to make the transitions slower or faster [1].
        Ignored it method[1]="linear".
    method : iterable
        Methods for each transition.
        "exp" for exponential transitions of amplitude (linear loudness).
        "linear" for linear transitions of amplitude.
    nsamples : interable
        The number of samples of each transition.
        If supplied, d is ignored.
    sonic_vector : array_like
        Samples for the envelope to be applied to.
        If supplied, d or nsamples is used, the final
        sound has the greatest duration of sonic_array
        and d (or nsamples) and missing samples are
        replaced with silence (if sonic_vector is shorter)
        or with a constant value (if d or nsamples yield shorter
        sequences).
    fs : integer
        The sample rate.
        Only used if nsamples and sonic_vector are not supplied.

    Returns
    -------
    E : ndarray
        A numpy array where each value is a value of the envelope
        for the PCM samples.
        If sonic_vector is supplied,
        E is the sonic vector with the envelope applied to it.

    See Also
    --------
    L : An envelope for a loudness transition.
    F : Fade in and out.
    AD : An ADSR envelope.
    T : An oscillation of loudness.

    Examples
    --------
    >>> W(V(d=8)*L_())  # writes a WAV file with a loudness transitions

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if type(sonic_vector) in (n.ndarray, list):
        N = len(sonic_vector)
    elif nsamples:
        N = nsamples
    else:
        N = int(fs*sum(d))
    samples = n.arange(N)
    s = []
    fact = 1
    if nsamples:
        for i, ns in enumerate(nsamples):
            s_ = L(dev[i], alpha[i], nsamples=ns, 
                    method=method[i])*fact
            s.append(s_)
            fact = s_[-1]
    else:
        for i, dur in enumerate(d):
            s_ = L(dur, dev[i], alpha[i],
                    method=method[i], fs=fs)*fact
            s.append(s_)
            fact = s_[-1]
    E = n.hstack(s)
    if type(sonic_vector) in (n.ndarray, list):
        if len(E) < len(sonic_vector):
            s = n.hstack((E, n.ones(len(sonic_vector)-len(E))*E[-1]))
        if len(E) > len(sonic_vector):
            sonic_vector = n.hstack((sonic_vector, n.ones(len(E)-len(sonic_vector))*E[-1]))
        return sonic_vector*E
    else:
        return E


def T_(d=[[3,4,5],[2,3,7,4]], fa=[[2,6,20],[5,6.2,21,5]],
        dB=[[10,20,1],[5,7,9,2]], alpha=[[1,1,1],[1,1,1,9]],
            taba=[[S,S,S],[Tr,Tr,Tr,S]],
        nsamples=0, sonic_vector=0, fs=44100):
    for i in range(taba):
        for j in range(i):
            taba[i][j] = n.array(taba[i][j])
    T_ = []
    if nsamples:
        for i, ns in enumerate(nsamples):
            T_.append([])
            for j, ns_ in enumerate(ns):
                s = T(fa=fa[i][j], dB=dB[i][j], alpha=alpha[i][j],
                    taba=taba[i][j], nsamples=ns_)
                T_[-1].append(s)
    else:
        for i, durs in enumerate(d):
            T_.append([])
            for j, dur in enumerate(durs):
                s = T(dur, fa[i][j], dB[i][j], alpha[i][j],
                    taba=taba[i][j])
                T_[-1].append(s)
    amax = 0
    if type(sonic_vector) in (n.ndarray, list):
        amax = len(sonic_vector)
    for i in range(len(T_)):
        T_[i] = n.hstack(T_[i])
        amax = max(amax, len(T_[i]))
    for i in range(len(T_)):
        if len(T_[i]) < amax:
            T_[i] = n.hstack((T_[i], n.ones(amax-len(T_[i]))*T_[i][-1]))
    if type(sonic_vector) in (n.ndarray, list):
        if len(sonic_vector) < amax:
            sonic_vector = n.hstack(( sonic_vector, n.zeros(amax-len(sonic_vector)) ))
        T_.append(sonic_vector)
    s = n.prod(T_, axis=0)
    return s


def mix(sonic_vectors, end=False, offset=0, fs=44100):
    """
    Mix sonic vectors.
    
    The operation consists in summing sample by sample [1].
    This function helps when the sonic_vectors are not
    of the same size.
    
    Parameters
    ----------
    sonic_vectors : list of sonic_arrays
        The sonic vectors to be summed.
    end : boolean
        If True, sync the final samples.
        If False (default) sync the initial samples.
    offset : list of scalars
        A list of the offsets for each sonic vectors
        in seconds.
    fs : integer
        The sample rate. Only used if offset is supplied.

    Returns
    -------
    S : ndarray
        A numpy array where each value is a PCM sample of
        the resulting sound.

    Examples
    --------
    >>> W(mix(sonic_vectors=[V(), N()]))  # writes a WAV file with nodes

    Notes
    -----
    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the 
    discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    if offset:
        for i, o in enumerate(offset):
            sonic_vectors[i] = n.hstack(( n.zeros(offset*fs), sonic_vectors[i] ))
            
    amax = 0
    for s in sonic_vectors:
        amax = max(amax, len(s))
    for i in range(len(sonic_vectors)):
        if len(sonic_vectors[i]) < amax:
            if end:
                sonic_vectors[i] = n.hstack(( n.zeros(amax-len(sonic_vectors[i])), sonic_vectors[i] ))
            else:
                sonic_vectors[i] = n.hstack(( sonic_vectors[i], n.zeros(amax-len(sonic_vectors[i])) ))
    s = n.sum(sonic_vectors, axis=0)
    return s


def trill(f=[220,330,440], ft=7, d=5, fs=44100):
    """Make a trill.

    This is just a simple function for exemplifying
    the synthesis of trills.
    The user is encouraged to make its own functions
    for trills and set e.g. ADSR envelopes, tremolos
    and vibratos as intended.

    Parameters
    ----------
    f : iterable of scalars
        Frequencies to the iterated.
    ft : scalar
        The number of notes per second.
    d : scalar
        The maximum duration of the trill in seconds.
    fs : integer
        The sample rate.

    Returns
    -------
    s : ndarray
        The PCM samples of the resulting sound.

    Examples
    --------
    >>> W(trill())

    """
    nsamples = 44100/ft
    pointer = 0
    i = 0
    s = []
    while pointer+nsamples < d*44100:
        ns = int(nsamples*(i+1) - pointer)
        note = N(f[i%len(f)], nsamples=ns,
                tab=Tr, fs=fs)
        s.append(AD(sonic_vector=note))
        pointer += ns
        i += 1
    trill = n.hstack(s)
    return trill


if __name__ == "__main__":
    doctest.testmod()