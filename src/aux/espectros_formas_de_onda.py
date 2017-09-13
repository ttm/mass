#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.09,bottom=0.15,right=0.96,top=0.96, hspace=0.4)

T=30
#T=1024
l=n.linspace(0,2*n.pi,T,endpoint=False)
senoide=n.sin(l)


dente=n.linspace (-1,1,T) # dente de serra
triangular=n.hstack ((n.linspace(-1,1,T/2,endpoint=False),n.linspace(1,-1,T/2,endpoint=False)))
quadrada=n.hstack ((n.ones(T/2),n.ones(T/2)* -1))


T2=T*1000
indices=n.arange(T2)

s_=senoide[indices%T]
s_s=n.fft.fft(s_)
s_a=n.abs(s_s)

d_=dente[indices%T]
d_s=n.fft.fft(d_)
d_a=n.abs(d_s)

t_=triangular[indices%T]
t_s=n.fft.fft(t_)
t_a=n.abs(t_s)

q_=quadrada[indices%T]
q_s=n.fft.fft(q_)
q_a=n.abs(q_s)


i=indices
foo=(s_a>50).nonzero()
p.plot(i[foo],s_a[foo],"o", label=u"sinusoid", markersize=9)
foo=(d_a>50).nonzero()
p.plot(i[foo],d_a[foo],"*", label=r"sawtooth", markersize=9)
ii=list(i[foo])
foo=(t_a>50).nonzero()
p.plot(i[foo],t_a[foo],"^", label=r"triangular", markersize=9)
#p.plot(i[foo],t_a[foo],"^", label=r"triangular")
foo=(q_a>50).nonzero()
p.plot(i[foo],q_a[foo],"s", label="square", markersize=9)
l=p.legend(loc="upper right")
for t in l.get_texts():
    t.set_fontsize('x-large')

p.yticks((0,20000),(0,"20k"), fontsize=17)
#p.xticks((0,15000),(0,"15k"))
# pop untill they leave f15 out of the game
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ii.pop()
ticks=[r"$f%i$" % (3*i,) for i in range(len(ii[::3]))]
ticks_=[]
for i in ticks:
    ticks_+=[i]+[""]*2
p.xticks([0] + ii , [0] + ticks_ , fontsize=18)

p.xlim(0,16500)
#p.xlim(0,T2*.56)
p.ylim(-300,20000)
p.ylabel(r'absolute value $\rightarrow$', fontsize=19)
p.xlabel(r'spectral component $\rightarrow$', fontsize=19)

p.savefig("../figures/waveSpectrum_.png")
p.show()
