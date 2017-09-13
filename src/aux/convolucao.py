#-*- coding: utf-8 -*-
import numpy as n, pylab as p

ax=p.subplot(111)
ax.annotate(r"$t_{12}'=\sum_{j=3}^{12} \, t_j.h_{12-j}$", xy=(12.2, -2.65),  xycoords='data',
                xytext=(23, -3.75), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top', fontsize=20
                )

ax.annotate(r"$t_{32}'=\sum_{j=24}^{32} \, t_j.h_{32-j}$", xy=(32.2, -1.75),  xycoords='data',
                xytext=(43, -3.75), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top', fontsize=20
                )





x=n.linspace(0,3*2*n.pi,50)
t=n.sin(x)
t=n.hstack((n.hstack((n.linspace(-1,1,16),n.linspace(-1,1,16))),n.linspace(-1,1,16)))
t*=.5

p.plot(t,'bo', label=r'sonic signal $\{t_i\}_0^{47}$')

#h=1./x[1:11]**.5
h=n.random.random(10)
h=n.array([ 0.5591728 ,  0.59152829,  0.43285462,  0.8870076 ,  0.44892785,0.33476906,  0.8808893 ,  0.39040725,  0.56887214,  0.54278373])
p.plot(range(3,13),h[::-1]+1,'ro',label=r'retrograde of impulse response $\{h_{i-j}\}_{j\; =\; max(i+1-\Lambda_h,0)}^i$')
for i in range(3,12):
    p.plot([i,i],[-1,2],'y-.')
p.plot([12,12],[-5,2], 'y-.',linewidth=3)


p.plot(range(23,33),h[::-1]+1,'ro')
for i in range(23,32):
    p.plot([i,i],[-1,2],'y-.')
p.plot([32,32],[-5,2], 'y-.',linewidth=3)

c=n.convolve(t,h)
p.plot(c-2.5,'go', label=u'convoluted signal ' + r'$\{\, (t*h)_{i}=\sum_{j=max(i+1-\Lambda_h,0)}^{i} t_j .  h_{i-j}\;\}_{0}^{48+10-2=56}$')


#p.xlim(-1.2,4.2)
p.ylim(-5.6,6.5)

p.yticks((),())
p.xticks((),())
p.legend(loc="upper right", fontsize=20)
#p.legend(loc="upper right",prop={'size':18})
p.xlabel(r"i $\rightarrow$", fontsize=26)
p.ylabel(r"amplitude $\rightarrow$", fontsize=26)

p.show()
