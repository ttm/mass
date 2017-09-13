#-*- coding: utf-8 -*-
import numpy as n, pylab as p

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.04,bottom=0.06,right=0.99,top=0.99)
c1=n.hstack(( n.linspace(0,1,1000,endpoint=False),n.linspace(1,0,1000)    )) # simetrico
c2=n.hstack(( n.linspace(0,1,500,endpoint=False), n.linspace(1,0,1500)    ))
c3=n.hstack(( n.linspace(0,1,1500,endpoint=False),n.linspace(1,0,500)    ))
c4=n.linspace(1,0,2000)
c5=n.linspace(0,1,2000)

p.plot(c1,label=u"climax at middle",lw=5)
p.plot(c2,label=u"climax at first half",lw=5)
p.plot(c3,label=u"climax at second half", lw=5)
p.plot(c4,label=u"climax at beginning",         lw=5)
p.plot(c5,label=u"climax at end",            lw=5)
p.legend(loc="lower center",prop={'size':16})

p.xlim(-50,2050)
p.ylim(-.18,1.02)

p.xticks((),())
p.yticks((),())

p.xlabel(r"time $\rightarrow$", fontsize=19)
p.ylabel(u"parameter"+r"$\rightarrow$", fontsize=19)

p.savefig("../figures/climax_.png")
p.show()

