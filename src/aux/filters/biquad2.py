#-*- coding: utf8 -*-

import numpy as n, pylab as p
N=n




def biquad(Fs, f0, ftype='LPF', Q=1., BW=None, dBgain=0.):
    """ Generates some common filter types for a biquad IIR filter.
  
    Implemented after
    "Cookbook formulae for audio EQ biquad filter coefficients"
    by Robert Bristow-Johnson
    http://www.musicdsp.org/files/Audio-EQ-Cookbook.txt
  
    Fs       the sampling frequency
    f0       "wherever it's happenin', man."  Center Frequency or
             Corner Frequency, or shelf midpoint frequency, depending
             on which filter type.  The "significant frequency".
    ftype    filter type, must be a string out of: "LPF", "HPF", "BPF",
             "notch", "APF", "peakingEQ", "lowShelf", "highShelf"
    Q        the EE kind of definition, except for peakingEQ in which A*Q is
             the classic EE Q.  That adjustment in definition was made so that
             a boost of N dB followed by a cut of N dB for identical Q and
             f0/Fs results in a precisely flat unity gain filter or "wire".
    BW       can be used _instead_ of Q to set the bandwidth in octaves
             (between -3 dB frequencies for BPF and notch or between midpoint
             (dBgain/2) gain frequencies for peaking EQ)
    dBgain   used for peaking and shelving filters to set the gain in dB
  
    returns  B,A for scipy.signal.lfilter
  
    All filter transfer functions were derived from analog prototypes
    and had been digitized using the Bilinear Transform.
  
    2007,
    Georg Holzmann
    """
  
    #some checks
    filtertypes = ["LPF", "HPF", "BPF", "notch", "APF", "peakingEQ",
                   "lowShelf", "highShelf"]
    if( ftype not in filtertypes ):
        raise ValueError, "Wrong filter type !"
  
    # some intermediate variables
    A = 10**(dBgain/40.)
    w0 = 2 * N.pi * f0 / Fs
    if( BW != None ):
        #print BW
        alpha = N.sin(w0)*N.sinh( N.log(2)/2 * BW * w0/N.sin(w0) )
        #Q = ( 2*N.sinh(N.log(2)/2*BW*w0/N.sin(w0)) )**(-1)
        #print Q
    else:
        # calc with Q
        alpha = N.sin(w0)/(2.*Q)
  
    # parameter arrays
    Bfilt = N.zeros(3)    # forward path
    Afilt = N.zeros(3)    # feedback path
  
    if( ftype=='LPF' ):
        Bfilt[0] = (1 - N.cos(w0)) / 2.
        Bfilt[1] = 1 - N.cos(w0)
        Bfilt[2] = (1 - N.cos(w0)) / 2.
        Afilt[0] = 1 + alpha
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha
    elif( ftype=='HPF' ):
        Bfilt[0] = (1 + N.cos(w0))/2.
        Bfilt[1] = -(1 + N.cos(w0))
        Bfilt[2] = (1 + N.cos(w0))/2.
        Afilt[0] = 1 + alpha
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha
    elif( ftype=='BPF' ):
        # constant 0dB peak gain
        Bfilt[0] = alpha
        Bfilt[1] = 0
        Bfilt[2] = -alpha
        Afilt[0] = 1 + alpha
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha
    elif( ftype=='notch' ):
        Bfilt[0] = 1.
        Bfilt[1] = -2*N.cos(w0)
        Bfilt[2] = 1.
        Afilt[0] = 1 + alpha
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha
    elif( ftype=='APF' ):
        Bfilt[0] = 1 - alpha
        Bfilt[1] = -2*N.cos(w0)
        Bfilt[2] = 1 + alpha
        Afilt[0] = 1 + alpha
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha
    elif( ftype=='peakingEQ' ):
        Bfilt[0] = 1 + alpha*A
        Bfilt[1] = -2*N.cos(w0)
        Bfilt[2] = 1 - alpha*A
        Afilt[0] = 1 + alpha/A
        Afilt[1] = -2*N.cos(w0)
        Afilt[2] = 1 - alpha/A
    elif( ftype=='lowShelf' ):
        Bfilt[0] = A*((A+1)-(A-1)*N.cos(w0) + 2*N.sqrt(A)*alpha)
        Bfilt[1] = 2*A*( (A-1) - (A+1)*N.cos(w0) )
        Bfilt[2] = A*((A+1)-(A-1)*N.cos(w0)-2*N.sqrt(A)*alpha)
        Afilt[0] = (A+1)+(A-1)*N.cos(w0)+2*N.sqrt(A)*alpha
        Afilt[1] = -2*( (A-1) + (A+1)*N.cos(w0))
        Afilt[2] = (A+1) + (A-1)*N.cos(w0)-2*N.sqrt(A)*alpha
    elif( ftype=='highShelf' ):
        Bfilt[0] = A*((A+1)+(A-1)*N.cos(w0)+2*N.sqrt(A)*alpha)
        Bfilt[1] = -2*A*( (A-1) + (A+1)*N.cos(w0) )
        Bfilt[2] = A*( (A+1) + (A-1)*N.cos(w0)-2*N.sqrt(A)*alpha )
        Afilt[0] = (A+1) - (A-1)*N.cos(w0) + 2*N.sqrt(A)*alpha
        Afilt[1] = 2*( (A-1) - (A+1)*N.cos(w0) )
        Afilt[2] = (A+1) - (A-1)*N.cos(w0) - 2*N.sqrt(A)*alpha
    else:
        raise ValueError, "Wrong filter type !"
  
    return Bfilt, Afilt



b,a=biquad(44100,4.,"HPF")

sinal=[b[0]]
sinal+=[b[1]-sinal[-1]*a[1]]
sinal+=[b[2]-sinal[-1]*a[1]-sinal[-2]*a[2]]
for i in xrange(44100): # for 1 second
    sinal.append(-sinal[-1]*a[1]-sinal[-2]*a[2])
fft=n.fft.fft(sinal)
m=n.abs(fft)
p.plot(m)
p.show()
