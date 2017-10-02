import numpy as n, os
from scipy.signal import fftconvolve as convolve
data_type = n.dtype('int16').newbyteorder ('>')
x = n.fromfile ("./hrtf/full/elev10/L10e000a.dat" , dtype=data_type)/2**15

def readHRTF(elev=10, azim=90):
    """
    Return the impulse responses for a HRTF.

    At a fixed distance of 1.4 meters.
    More information at:
    http://sound.media.mit.edu/resources/KEMAR.html
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
    print(elev_, azim)
    angles = [int(i[-8:-5]) for i in os.listdir(adir)]

    # MASS use counter-clockwise convention, MIT uses clockwise
    # MASS starts with 0 degree to the right
    # MIT starts with zero degree straight ahead
    azim = (360 - azim + 90) % 360
    az = min(angles, key=lambda x:abs(x-azim))

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
