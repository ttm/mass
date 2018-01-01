def spectrum(c=[134,230,70]):
    # for the most different in each RGB value
    c1 = [256*( i >= 256/2 ) for i in c]  # first harmonic
    c_ = [c, c1]
    for i in range(3):
        vals = [cc[i] for cc in c_]
    c2 =  # second harmonic

def maxRGBdist(c_=[(124,255,20), (0,200,100)]):
    # for the most different in each RGB from the first color
    s = spectrum(c_[0])

def wobble(d=2,n_wobbles=2, fv_ = 15, fa_ = 25, taba=**kargs):
    """
    two vibrato and tremollo patterns:
    one gives the undulation,
    the other gives the rugosity

    """
    if n_wobbles == 'fv':
        pass
    else:
        fv = d/n_wobbles
        ft = d/n_wobbles
    d = kargs.copy()
    d['d'] = d

