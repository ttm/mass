# coding: utf-8
import numpy as n, pylab as p

tonica=n.array([0,4,7])
dominante=n.array([2,7,11])
subdominante=n.array([0,5,9])
aa=n.random.randint(0,3,2**16)
tonica[aa]
dominante[aa]
subdominante[aa]
trecho=n.hstack((tonica[aa],dominante[aa],subdominante[aa],dominante[aa],tonica[aa]))
p.specgram(trecho)
p.savefig("espectro_harmonia.png")

t_=440.*(2.**(trecho/12.))

p.specgram(t_)
p.savefig("espectro_harmonia2.png")
p.show()
