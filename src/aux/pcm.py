#-*- coding: utf-8 -*-
import numpy as n, pylab as p, string

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.11,bottom=0.13,right=0.99,top=0.99)

# plotando um som em PCM de 4 bits de profundidade

# grade de variacao de amplitude
p.grid(True, axis='y',ls='-.',lw=2)


aa=n.linspace(0,2*2*n.pi,500)[:250]
b=n.sin(aa)+n.sin(4*aa)
b*=.5
b*=2**3-1 # 4 bits

p.plot(aa,b,"g",lw=6,label=u"analog signal")

c=n.round(b)
p.plot(aa[::10],c[::10],'ro',ms=9,label="digital samples")

def bits(i,n):
    return tuple(("0","1")[i>>j & 1] for j in range(n-1,-1,-1)) 

foo=[bits(i,4) for i in range(2**4)]
bar=["".join(ii) for ii in foo]
p.yticks(range(-7,9),bar, fontsize=16)

xlabs=[r"$\lambda_s$"]*len(aa[::50])
xlabs=[str(5*i)+xlabs[i] for i in range(len(xlabs))]
xlabs[0]=0
# xlabs[1]=r"$\lambda_a$"
xlabs_=[]
for i in xlabs:
    xlabs_+=[i]+[""]*4
p.xticks((aa[::10]),xlabs_, fontsize=16)

p.xlim(-.3,aa[::10][-1]+0.5)
p.ylim(-8,9)

p.legend(prop={'size':26})

p.xlabel(r"time $\rightarrow$",fontsize=20)
p.ylabel(r"amplitude $\rightarrow$",fontsize=24)

p.savefig("../figures/pcm_.png")
p.show()
