import numpy as n, os
from scipy.signal import fftconvolve as convolve
from scipy.interpolate import interp1d as interp
from functions import *

def readHRTF(elev=10, azim=90, strict=0):
    """
    Return the impulse responses for a HRTF.

    At a fixed distance of 1.4 meters.
    More information about the HRTF dataset at:
    http://sound.media.mit.edu/resources/KEMAR.html

    Parameters
    ----------
    elev : scalar
        The elevation angle in degrees between -40 and 90.
        90 is vertically up.
    azim : scalar
        The azimuthal angle in degrees between 0 and 360.
        0 is to the right and azim increases counter-clockwise.
    stric : scalar
        Only return the impulse responses if the requested
        angles are matched in the database by a difference
        smaller than strict.
        Set to 0 (default) to return the impulse response
        available for the nearest angle.

    Returns
    -------
    el : scalar
        The elevation angle of the impulse response being returned.
    az : scalar
        The azimuthal angle of the impulse response being returned.
    L : ndarray
        The impulse response for the left ear.
    R : ndarray
        The impulse response for the right ear.

    See Also
    --------
    applyHRTF : Applies a HRTF to an input sonic vector.
    movingHRTF : Experimental implementations for
                 simulating a moving sound source through HRTF.

    Examples
    --------
    >>> readHRTF()

    Notes
    -----
    The dataset comprises generalized HRTFs (non-personalized)
    and is not distance-dependant.
    It was obtained through measures performed at about
    5 degrees apart and a fixed distance of 1.4 meters.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)

    """
    elev_ = int(n.round(elev/10)*10)
    if (azim < 0) or (azim > 360):
        print('azimuth must be between 0 and 360 degrees')
        return
    if (elev_ < -40) or (elev_ > 90):
        print('elevation must be between -40 and 90 degrees')
        return

    adir = os.path.join('.', 'hrtf')
    if len(os.listdir(adir)) == 1:
        fname = os.path.join('.', 'hrtf', 'MIT-HRTF.tar.gz')
        import tarfile
        tar = tarfile.open(fname, "r:gz")
        tar.extractall(path=adir)
        tar.close()
        
    adir = os.path.join(adir, 'full', 'elev'+str(elev_))
    # print(elev_, azim)
    angles = [int(i[-8:-5]) for i in os.listdir(adir)]

    # MASS use counter-clockwise convention, MIT uses clockwise
    # MASS starts with 0 degree to the right
    # MIT starts with zero degree straight ahead
    azim = (360 - azim + 90) % 360
    az = min(angles, key=lambda x:abs(x-azim))
    if strict:
        if (elev_ - elev) > strict or (az - azim) > strict:
            return 0, 0, 0, 0

    fname = os.path.join(adir, 'L{elev}e{az:03d}a.dat'.format(
                                        elev=elev_, az=az))
    L = n.fromfile(fname , dtype=data_type)/2**15
    fname = os.path.join(adir, 'R{elev}e{az:03d}a.dat'.format(
                                    elev=elev_, az=az))
    R = n.fromfile(fname , dtype=data_type)/2**15

    # return angles used and impulse responses
    az_ = (360 - az + 90) % 360
    return elev_, az_, L, R

def applyHRTF(sonic_vector, el=10, az=90):
    """
    Apply a HRTF to a sonic vector.

    Parameters
    ----------
    sonic_vector : array_like
        A one dimensional array with the PCM samples of a sound.
    el : scalar
        The elevation angle in degrees between -40 and 90.
        90 is vertically up.
    az : scalar
        The azimuthal angle in degrees between 0 and 360.
        0 is to the right and azim increases counter-clockwise.

    See Also
    --------
    readHRTF : Returns the HRTF impulse responses for the ears.
    movingHRTF : Experimental implementations for
                 simulating a moving sound source through HRTF.

    Examples
    --------
    >>> s = readHRTF(V())
    >>> WS(s)

    Notes
    -----
    See readHRTF() for more information.

    Cite the following article whenever you use this function.

    References
    ----------
    .. [1] Fabbri, Renato, et al. "Musical elements in the discrete-time representation of sound." arXiv preprint arXiv:abs/1412.6853 (2017)


    """
    e, a, L, R = readHRTF(el, az)
    if len(L) < len(sonic_vector):
        L_ = convolve(sonic_vector, L)
    else:
        L_ = convolve(L, sonic_vector)
    if len(R) < len(sonic_vector):
        R_ = convolve(sonic_vector, R)
    else:
        R_ = convolve(R, sonic_vector)
    s = n.vstack(( L_, R_ ))
    return s


def movingHRTF(sonic_vector, el1=70, el2=-30, az1=0, az2=290,
        idom=None, imet='lin'):
    """
    Simulates a moving target using HRTFs. (Experimental)

    Parameters
    ----------
    sonic_vector : array_like
        A one dimensional array with the PCM samples of a sound.
    el1 : scalar
        The starting elevation angle in degrees between -40 and 90.
        90 is vertically up.
    el2 : scalar
        The final elevation angle in degrees between -40 and 90.
        90 is vertically up.
    az1 : scalar
        The starting azimuthal angle in degrees between 0 and 360.
        0 is to the right and azim increases counter-clockwise.
    az2 : scalar
        The final azimuthal angle in degrees between 0 and 360.
        0 is to the right and azim increases counter-clockwise.
    idom : string
        The domain in which the interpolation is performed:
            'time' for interpolating the samples of the impulse
                response directly.
            'freq' for interpolating the magnitude and phase
                of the impulse response.
            None for no interpolation; just use the impulse
                response of the nearest angle available.
    imet : string
        The interpolation method. Only linear interpolation
        is implemented ('lin').

    See Also
    --------
    readHRTF : Returns the HRTF impulse responses for the ears.
    applyHRTF : Applies a HRTF to an input sonic vector.

    Examples
    --------
    >>> s = movingHRTF(V(), idom=None)
    >>> WS(s)

    Notes
    -----
    The option 'time' and 'freq' for idom are not delivering
    satifactory results in this initial and experimental
    implementation.

    This implementation attempts to simulate a moving sound
    source by interpolating the HRTF impulse responses and
    convolving them in the time domain to preserve the
    localization of the source along time.

    In a finished implementation,
    the Doppler effect should also be taken into account.
    This implies that it should be a part of the synthesis
    method because the frequential variations need to
    be considered in the LUT indexing.

    One good approach is to understand how the Web Audio API
    is performing the interpolations of the HRTF and see
    if there are reasonable implementations in CSound, Puredata
    and SuperCollider.

    See readHRTF() and applyHRTF() for more information.

    Cite the following article whenever you use this function.
                
    """
    l = len(sonic_vector)
    el = el1 + (el2 - el1)*n.arange(l)/(l+1)
    az = az1 + (az2 - az1)*n.arange(l)/(l+1)
    e, a, L0, R0 = readHRTF(el[0], az[0])
    x = [0]
    if idom in ('time', None):
        yl = [L0]
        yr = [R0]
    elif idom == 'freq':
        L0_ = n.fft.fft(L0)[:len(L0)//2]
        ylm = [n.abs(L0_)  ]
        ylp = [n.angle(L0_)]

        R0_ = n.fft.fft(R0)[:len(R0)//2]
        yrm = [n.abs(R0_)  ]
        yrp = [n.angle(R0_)]
    i = 0
    strict = max(abs(el[0]-el[1])*0.5+1e-10, abs(az[0]-az[1])*0.5+1e-10)
    for e_, a_ in zip(el, az):
        if idom:
            e, a, ll, rr = readHRTF(e_, a_, strict=strict)
        else:
            e, a, ll, rr = readHRTF(e_, a_)
            yl.append(ll)
            yr.append(rr)
            x.append(i)
        if n.any(ll):
            x.append(i)
            if idom == 'time':
                yl.append(ll)
                yr.append(rr)
            elif idom == 'freq':
                L0_ = n.fft.fft(ll)[:len(L0)//2]
                ylm += [n.abs(L0_)  ]
                ylp += [n.angle(L0_)]

                R0_ = n.fft.fft(rr)[:len(R0)//2]
                yrm += [n.abs(R0_)  ]
                yrp += [n.angle(R0_)]
            print(e, a)
        i+=1
    if x[-1] != len(el)-1:
        e, a, L_, R_ = readHRTF(el[-1], az[-1])
        if idom == 'time':
            yl.append(L_)
            yr.append(R_)
        elif idom == 'freq':
            L0_ = n.fft.fft(L_)[:len(L0)//2]
            ylm += [n.abs(L0_)  ]
            ylp += [n.angle(L0_)]

            R0_ = n.fft.fft(R_)[:len(R0)//2]
            yrm += [n.abs(R0_)  ]
            yrp += [n.angle(R0_)]
        x.append(i-1)

    LL, RR = [], []
    xx = n.arange(l)
    if idom == 'time':
        for i in range(len(yl[0])):
            yyl = [yy[i] for yy in yl]
            f = interp(x=x, y=yyl)
            ll = f(xx)
            LL.append(ll)

            yyr = [yy[i] for yy in yl]
            f = interp(x=x, y=yyr)
            rl = f(xx)
            RR.append(rl)
    elif idom == 'freq':
        for i in range(len(ylm[0])):
            yylm = [yy[i] for yy in ylm]
            f = interp(x=x, y=yylm)
            llm = f(xx)
            yylp = [yy[i] for yy in ylp]
            f = interp(x=x, y=yylp)
            llp = f(xx)

            coefsl1 = llm*n.e**(llp*1j)
            coefsl2 = llm*n.e**(-llp*1j)
            if l % 2 == 0:
                coeffsl = n.hstack(( coefsl1, coefsl2[1:-1][::-1] ))
            else:
                coeffsl = n.hstack(( coefsl1, coefsl2[1:][::-1] ))
            ll = n.fft.ifft(coeffsl).real
            LL.append(ll)

            yyrm = [yy[i] for yy in yrm]
            f = interp(x=x, y=yyrm)
            rrm = f(xx)
            yyrp = [yy[i] for yy in yrp]
            f = interp(x=x, y=yyrp)
            rrp = f(xx)

            coefsr1 = rrm*n.e**(rrp*1j)
            coefsr2 = rrm*n.e**(-rrp*1j)
            if l % 2 == 0:
                coeffsr = n.hstack(( coefsr1, coefsr2[1:-1][::-1] ))
            else:
                coeffsr = n.hstack(( coefsr1, coefsr2[1:][::-1] ))
            rr = n.fft.ifft(coeffsr).real
            RR.append(rr)
    if idom not in ('time', 'freq'):
        LL = n.vstack((yl)).T
        RR = n.vstack((yr)).T
    else:
        LL = n.vstack(LL)  # each column is an impulse response
        RR = n.vstack(RR)

    lim = LL.shape[0]
    sl = n.zeros( len(sonic_vector) + lim - 1 )
    sr = n.zeros( len(sonic_vector) + lim - 1 )
    for i in range(l):
        # get impulse response (im)
        # make it not larger than past samples in the sound +1
        # get chunck of sound no larger than the im
        # multiply the reversed samples by the sound
        im = LL[:, i][:i+1]
        s_ = sonic_vector[:i+1][::-1][:lim]
        sl[i] += (s_*im).sum()

        im = RR[:, i][:i+1]
        sr[i] += (s_*im).sum()
    s = n.vstack(( sl, sr, ))
    return s


