#-*- coding: utf-8 -*-

import numpy as n, pylab as p

# nao utilizado na dissertacao por enquanto
# comparando duas transicoes de amplitudes
# fade in, mas feitas em grandezas diferentes
a0=10.
al=11.

a0_=1.
al_=2.

a0__=1e-6 # -120 dB
al__=1 # 0dB

alpha=1

L=1000. # mil amostras para a transicao
iis=n.arange(L)

ai=a0*(al/a0)**(iis/(L-1))-a0
ai_=a0_*(al_/a0_)**(iis/(L-1))-a0_
ai__=a0__*(al__/a0__)**(iis/(L-1))


p.plot(n.log(ai  ))
p.plot(n.log(ai_ ))
p.plot(n.log(ai__))
p.show()
