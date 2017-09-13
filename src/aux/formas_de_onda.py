#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n, matplotlib as m
from scipy.io import wavfile as w

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.12,bottom=0.13,right=0.99,top=0.99, hspace=0.4)

T=100
#T=1024
l=n.linspace(0,2*n.pi,T,endpoint=False)
senoide=n.sin(l)
dente=n.linspace (-1,1,T) # dente de serra
triangular=n.hstack ((n.linspace(-1,1,T/2,endpoint=False),n.linspace(1,-1,T/2,endpoint=False)))
quadrada=n.hstack ((n.ones(T/2),n.ones(T/2)* -1))

# onda=a.wavread("ondaReal.wav")[0] # onda real
onda = w.read("../../scripts/ondaReal.wav")[1].astype("float64")
onda=((onda-onda.min())/(onda.max()-onda.min()))*2-1 # normalizando
#onda2=a.wavread("22686__acclivity__oboe-a-440_periodo.wav")[0] # periodo do oboe
onda2 = w.read("../../scripts/22686__acclivity__oboe-a-440_periodo.wav")[1].astype("float64")
onda2=((onda2-onda2.min())/(onda2.max()-onda2.min()))*2-1 # normalizando


p.subplot(211)
#p.title("Formas de onda")
p.plot(senoide,'o',linewidth=3, label=u"sinusoid")
p.plot(dente,'o',linewidth=3, label="sawtooth")
p.plot(triangular,'o',linewidth=3, label="triangular")
p.plot(quadrada,'o',linewidth=3, label="square")
p.xlim(0,T)
p.ylim(-1.1,1.1)

foo=p.gca()
foo.axes.get_xaxis().set_ticks([])
#l=p.legend((u"senóide","dente de serra","triangular","quadrada"),bbox_to_anchor=(0., 1.02, 1., .102), loc=10,
       #ncol=2, mode="expand", borderaxespad=0.)
#l=p.legend((u"senóide","dente de serra","triangular","quadrada","som real (abaixo)"),bbox_to_anchor=(0., -.1, 1., .1), loc=1,
       #ncol=5, mode="expand", borderaxespad=0.)
l=p.legend(bbox_to_anchor=(0., -.1, 1., .1), loc=1,
       ncol=5, mode="expand", borderaxespad=0.)
for t in l.get_texts():
    t.set_fontsize('x-large')
frame  = l.get_frame()
frame.set_facecolor('0.80')
for ll in l.get_lines():
        ll.set_linewidth(1.5)  # the legend line width
#p.legend()
p.ylabel('synthesized\n'+r'amplitude',fontsize=17)

fig=p.subplot(212)
i=n.arange(len(onda))
p.plot(i,onda,"yo",linewidth=3, label="sampled real sound")
p.plot(i,onda,"y",linewidth=3)
i=n.linspace(0,len(onda),len(onda2),endpoint=False)
p.plot(i, onda2,"ko", linewidth=3, label=r"oboe period at $\approx 450 Hz$")
p.plot(i, onda2,"k", linewidth=3)
p.xlim(0,onda.shape[0])
p.ylim(-1.1,1.1)
foo=p.gca()
foo.axes.get_xaxis().set_ticks([])
l=p.legend(bbox_to_anchor=(0., -.1, 1., .1), loc=1,
       ncol=5, mode="expand", borderaxespad=0.)
for t in l.get_texts():
    t.set_fontsize('x-large')
frame  = l.get_frame()
frame.set_facecolor('0.80')
for ll in l.get_lines():
        ll.set_linewidth(1.5)  # the legend line width

#p.xlabel(r'\n\ntempo $\Delta$, amostras $\Lambda$ ou $i$$\rightarrow$', fontsize=15, verticalalignment='top')
#p.text=(10,0,r'tempo $\Delta$, amostras $\Lambda$ ou $i$$\rightarrow$')

left, width = len(onda)*.37, .5
bottom, height = 1.44, .5
right = left + width
top = bottom + height
atext=r'time $\Delta$, samples $\Lambda$ or sample $i$ $\rightarrow$'
fig.text(left, bottom, atext, horizontalalignment='left', verticalalignment='top', fontsize=19)

p.ylabel('sampled\n'+r'amplitude', fontsize=19)
#p.ylabel(r'amplitude amostrada', verticalalignment='top')
#p.xlabel(r'duração $\delta$, amostras $\lambda$ ou $i$ $\rightarrow$')
p.savefig("../figures/waveForms__.png")
p.show()
