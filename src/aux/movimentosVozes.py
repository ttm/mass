#-*- coding: utf-8 -*-
import numpy as n, pylab as p

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.04,bottom=0.08,right=0.95,top=0.99)
ax = p.subplot(111)

##### movimentos discernidos no contraponto

# movimento direto
voz1=[1,2.5,0,1]
voz2=[0,0.5,-1,0]

x=0
for n1,n2 in zip(voz1,voz2):
    if x==0:
        n1_=n1
        n2_=n2
    else:
        p.arrow(x-0.3,n1_+(n1-n1_)*.2,0.2,(n1-n1_)*.6,head_width=.1,length_includes_head=True,color="b")
        p.arrow(x-0.3,n2_+(n2-n2_)*.2,0.2,(n2-n2_)*.6,head_width=.1,length_includes_head=True,color="g")
        n1_=n1
        n2_=n2
    p.plot((x,x+0.6),(n1,n1),'b',lw=6)
    p.plot((x,x+0.6),(n2,n2),'g',lw=6)
    x+=1

p.plot((-10,10),(-2,-2),"r--")

# movimento contrario
voz1=[-3,-4,-3.5,-4]
voz2=[-5,-4.5,-4.8,-3.9]

x=0
for n1,n2 in zip(voz1,voz2):
    if x==0:
        n1_=n1
        n2_=n2
    else:
        p.arrow(x-0.3,n1_+(n1-n1_)*.2,0.2,(n1-n1_)*.6,head_width=.1,length_includes_head=True,color="b")
        p.arrow(x-0.3,n2_+(n2-n2_)*.2,0.2,(n2-n2_)*.6,head_width=.1,length_includes_head=True,color="g")
        n1_=n1
        n2_=n2
    p.plot((x,x+0.6),(n1,n1),'b',lw=6)
    p.plot((x,x+0.6),(n2,n2),'g',lw=6)
    x+=1

p.plot((-10,10),(-6,-6),"r--")

# movimento oblíquo
voz1=[-7,-8,-8,-8]
voz2=[-9,-9,-8.5,-9.5]

x=0
for n1,n2 in zip(voz1,voz2):
    if x==0:
        n1_=n1
        n2_=n2
    else:
        p.arrow(x-0.3,n1_+(n1-n1_)*.2,0.2,(n1-n1_)*.6,head_width=.1,length_includes_head=True,color="b")
        p.arrow(x-0.3,n2_+(n2-n2_)*.2,0.2,(n2-n2_)*.6,head_width=.1,length_includes_head=True,color="g")
        n1_=n1
        n2_=n2
    p.plot((x,x+0.6),(n1,n1),'b',lw=6)
    p.plot((x,x+0.6),(n2,n2),'g',lw=6)
    x+=1



p.plot((1000,1000),(n1,n1),'b',lw=6, label=u"voice 1")
p.plot((1000,1000),(n2,n2),'g',lw=6, label=u"voice 2")
p.legend(loc="upper right",prop={'size':14})

p.ylim(-10,3.6)
p.xlim(-0.2,3.8)

p.yticks((-8,-4,1),(u"oblique",u"contrary","direct"),rotation="90",fontsize=16, fontweight='bold')

p.text(2.8,-1.6,"parallel\nmovement",fontsize="14")

for line in ax.get_xticklines() + ax.get_yticklines():
    line.set_markersize(0)

p.xticks(())
p.xlabel(r"time $\rightarrow$",fontsize=26)

ax2=ax.twinx()
ax2.set_ylabel(r"$\log(freq)$ $\rightarrow$",fontsize=26)
p.ylim(-10,3.6)
p.yticks(())

p.savefig("../figures/movContraponto_.png")
p.show()

