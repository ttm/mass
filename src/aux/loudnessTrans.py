import numpy as n, pylab as p

N = 1000
N_ = N-1
samples = n.arange(N)

dB = 30

# to +-db Ii
aI = 10**(samples*dB/(20*N_))
ai = 10**(-samples*dB/(20*N_))

# from +-db Ii_
aI_ = 10**((N_-samples)*dB/(20*N_))
ai_ = 10**(-(N_-samples)*dB/(20*N_))

p.plot(n.log(aI))
p.plot(n.log(ai))
p.plot(n.log(aI_))
p.plot(n.log(ai_))
p.show()
