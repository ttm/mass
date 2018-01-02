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


def mediumColor():
    """
    Returns color with equal RGB distance from both black and white
    """
    found = False
    total = 256+128
    while not found:
        c1 = n.random.randint(0,256)
        limit = total - c1
        l = min(limit, 256)
        c2 = n.random.randint(0, l)
        limit = total - c1 -c2
        if limit <= 255:
            c3 = limit
            founf = True
    rgb = n.random.permutation([c1,c2,c3])
    return rgb

special_medium_colors = [
        '#888888',  # gray
        '#FF8800',  # red green
        '#FF0088',  # red blue
        '#88FF00',  # green red
        '#00FF88',  # green blue
        '#8800FF',  # blue red
        '#0088FF',  # blue green
        ]

# color pallete of a medium color:
# - all permutations of values RGB
# - all colors has its RGB complement [255-c for c in RGB]
# if rgb values are different, the resulting colors
# are more easely perceived.
# The special medim colors above have maximal rgb differences
# except for gray.
# They are the only colors with such maximal distance.
# They are among the best colors to use with black and white.
# Total size of pallete for non-special color:
# 6 permutations + 6 complements + black and white =  14 colors!
# For a special color, the complements are among the permutations, resulting:
# 6 permutations + black and white = 8 colors!
# The pallete is the same no matter which of such special colors was used to derive
# the pallete.

# the nucleus is B/W, color and its complement, then the rotations, the complement of the rotations.
# One might further extend the pallete by finding other maximal RGB distances.
# and pure RGB presences and absence (R,G,B,C,M,Y)

#    0              2          2
# 255,128,0 -> 0,255,128 -> 128,0,255
# 0,128,255 -> 255,0,128 -> 128,255,0
#    2            1             1

# each of color schemes holds the same colors
# but might be taken to have a main color
# which is better distinguished against
# three other colors (rotations and the complement),
# then against black and white,
# then against 2 last colors 
# (rotations of the complement or the complement of each rotation)

def whitenize(color):
    """
    Notes
    -----
    There are a number of ways to make a color more white.
    They are centered in the resemblance white has with gray
    and with the fact that white has high RGB values:
      * one might increase the amount of rgb proportionaly or adding a constant
      * one might increace the value of the color with the lowest value
      * one might make the color values closer to the mean
      * one might combine all these methods at once.

    """
    pass





