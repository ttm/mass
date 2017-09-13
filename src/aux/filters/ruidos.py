#-*- coding: utf8 -*-
import numpy as n, pylab as p#, scikits.audiolab as a

N = 100000 # N sempre par
fa=44100.

# diferença das frequências entre coeficiêntes vizinhos:
df=fa/N

# geracao de espectro com modulo 1 uniforme
# e fase aleatoria
coefs=n.exp(1j*n.random.uniform(0, 2*n.pi, N))

# real par, imaginaria impar
coefs[N/2+1:]=n.real(coefs[1:N/2])[::-1] - 1j*n.imag(coefs[1:N/2])[::-1]

coefs[0]=0. # sem bias
coefs[N/2]=1 # freq max eh real simplesmente


# as frequências relativas a cada coeficiente
fi=n.arange(coefs.shape[0])*df # acima de N/2 nao vale
f0=15. # iniciamos o ruido em 15 Hz
i0=n.floor(f0/df) # primeiro coeff a valer
coefs[:i0]=n.zeros(i0)
f0=fi[i0]


# para plotar:
ii=1000
ie=1200

fig=p.figure(figsize=(10.,8.))
p.subplots_adjust(left=0.09,bottom=0.08,right=0.98,top=0.96, wspace=0.33, hspace=0.6)

###########
# Ruido Violeta:
# a cada oitava, ganhamos 6dB
fator=10.**(6/20.)

alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai
# real par, imaginaria impar


c[N/2+1:]=n.real(c[1:N/2])[::-1] - 1j*n.imag(c[1:N/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
# a.wavwrite(r,'violeta.wav',44100)

p.subplot(521)
p.title(u'violet noise')
p.ylim(-10,220)
p.plot(n.log10(fi[i0:len(fi)/2]),20*n.log2(n.abs(c[i0:len(c)/2])))
p.subplot(522)
p.plot(r[ii:ie])
p.plot(r[ii:ie],'ro', markersize=4)

#############
# Ruido Azul

# para cada oitava, ganhamos 3dB
fator=10.**(3/20.)

alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai
# real par, imaginaria impar


c[N/2+1:]=n.real(c[1:N/2])[::-1] - 1j*n.imag(c[1:N/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
# a.wavwrite(r,'azul.wav',fa)

p.subplot(523)
p.title(u'blue noise')
p.ylim(-10,220)
p.plot(n.log10(fi[i0:len(fi)/2]),20*n.log2(n.abs(c[i0:len(c)/2])))
p.subplot(524)
p.plot(r[ii:ie],'ro', markersize=4)
p.plot(r[ii:ie])


################
# geracao do ruido branco


ruido=n.fft.ifft(coefs)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
# a.wavwrite(r,'branco.wav',fa)

p.subplot(525)
p.title(u'white noise')
p.ylim(-10,10)
#p.ylabel(r"$ 20 \log (\frac{\lVert c_i \rVert }{c_{\text{min}}}) $")
p.ylabel(r"$ 20 \log ( | c_i |  / | c_{min} |    ) \rightarrow $", fontsize=20)
p.plot(n.log10(fi[i0:len(fi)/2]),20*n.log2(n.abs(coefs[i0:len(coefs)/2])))
p.subplot(526)
p.plot(r[ii:ie],'ro', markersize=4)
p.plot(r[ii:ie])
p.ylabel(r"amplitude $ \rightarrow $", fontsize=20)


################
# Ruido rosa

# para cada oitava, perde 3dB, i.e. cai para ~0.707 da amplitude
fator=10.**(-3/20.)

alphai=fator**(n.log2(fi[i0:]/f0))

c=n.copy(coefs)
c[i0:]=coefs[i0:]*alphai
# real par, imaginaria impar
c[N/2+1:]=n.real(c[1:N/2])[::-1] - 1j*n.imag(c[1:N/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
# a.wavwrite(r,'rosa.wav',fa)

p.subplot(527)
p.title(u'pink noise')
p.ylim(-220,10)
p.plot(n.log10(fi[i0:len(fi)/2]),20*n.log2(n.abs(c[i0:len(c)/2])))
p.subplot(528)
p.plot(r[ii:ie],'ro', markersize=4)
p.plot(r[ii:ie])


################3
# Ruido marrom

# para cada oitava, perde 6dB, i.e. cai para ~0.501 da amplitude
fator=10.**(-6/20.)

alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[N/2+1:]=n.real(c[1:N/2])[::-1] - 1j*n.imag(c[1:N/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
# a.wavwrite(r,'marrom.wav',fa)

p.subplot(529)
p.title(u'brown noise')
p.ylim(-220,10)
p.plot(n.log10(fi[i0:len(fi)/2]),20*n.log2(n.abs(c[i0:len(c)/2])))
p.xlabel(r"$\log(freq) \rightarrow$", fontsize=18)
p.subplot(5,2,10)
p.plot(r[ii:ie],'ro', markersize=4)
p.plot(r[ii:ie])
p.xlabel(r"samples $ \rightarrow$", fontsize=16)
p.savefig("../../figures/ruidos_.png")
p.show()
