#-*- coding: utf-8 -*-
import numpy as n, pylab as p

fig=p.figure(figsize=(10.,5.8))
p.subplots_adjust(left=0.05,bottom=0.065,right=0.96,top=0.59, hspace=0.34)
sub1=fig.add_subplot(311)
fa=4410
dx=7

# Som curto
sdur=0.003 # segundos
f=200. #hz
ii=int(fa*sdur)
s=n.sin(n.linspace(0,2*400*2*n.pi*sdur,ii, endpoint=False))

# resposta ao impulso com um pulso
ddur=0.020
iii=int(fa*ddur)
xi=(1.5*iii)//3
hi=n.zeros(iii)
hi[xi]=1
som = n.convolve(s,hi)

p1=sub1.plot(s+6,'bo', label=r"$\{t_i\}_0^{\Lambda-1}$", ms=3)
p2=sub1.plot(hi+3,'ro', label=r"$\{h_i=\delta_{\xi-i}\}_0^{\Lambda_h-1}$",
        ms=3)
p3=sub1.plot(som,'go', label=r"$\{(t*h)_i\}_0^{\Lambda+\Lambda_h-2}$", ms=3)
# p.legend(loc="upper right",numpoints=5)
p.xticks((0,ii-1,xi,xi+ii-1,ii+iii-2, iii-1),(r"0",
    r"$\Lambda-1$",r"$\xi$", r"$\xi + \Lambda-1$",
    r"$\Lambda+\Lambda_h-2$", r"$\Lambda_h-1$"),fontsize='16')
p.yticks((),())
p.ylim(-1.6,7.6)
p.xlim(-dx,ii+iii-2+dx)
p.plot([ii-1,ii-1],[-2,9],"y", linewidth=5,alpha=.4)
p.plot([len(hi)-1,len(hi)-1],[-2,9],"y", linewidth=5,alpha=.4)
p.plot([xi ,xi ],[-2,9],"y", linewidth=5,alpha=.4)
p.plot([xi +ii-1,xi +ii-1],[-2,9],"y", linewidth=5,alpha=.4)
p.plot([iii +ii-2,iii +ii-2],[-2,9],"y", linewidth=5,alpha=.4)

ax2 = sub1.twinx()
ax2.set_yticks((),())
ax2.set_ylabel(r"offset", fontsize=14, fontweight='bold')


############## SUB 2
sub2 = fig.add_subplot(312)
ax2 = sub2.twinx()
ax2.set_yticks((),())
ax2.set_ylabel(r"rhythm", fontsize=14, fontweight='bold')

# ddur=0.2
# iii=fa*ddur
hi=n.zeros(iii)
# pulsos=iii*2/100 # percentagem de incidencias no delay
# xis=n.random.randint(0,iii-iii*3/100,pulsos)
xis=n.array([2, 20, 45, 67])
hi[xis]=n.ones(xis.shape[0])
som = n.convolve(hi,s)

p.plot(hi+3,'ro',
        label=r"$\{h_i=\sum_{j=0}^{\Lambda_j-1}\delta_{\xi_j-i}\}_0^{\Lambda_h-1}$",
        ms=3)
p.plot(som,'go', label=r"$\{(t*h)_i\}_0^{\Lambda+\Lambda_h-2}$", ms=3)
# p.legend(loc="upper right",numpoints=5)


p.ylim(-2.4,5.)

# p.xticks([0]+list(xis)+[ii+iii-2],[0]+[r"$\delta$"  for i in xis]+[r"$\Lambda+\Lambda_h-2$"],fontsize='16')
p.xticks((),())
p.yticks((),())

sub2.set_ylabel(r"amplitude $\rightarrow$", fontsize=20)
sub2.set_yticks((),())
# p.xlim(-10,ii+iii-2+50+345)
sub2.set_xlim(-dx,ii+iii-2+dx)
# ax2.set_xlim(-2,ii+iii-2+25)

############## SUB 3
sub3 = fig.add_subplot(313)
ax2 = sub3.twinx()
ax2.set_yticks((),())


# ddur=0.2
# iii=fa*ddur
hi=n.zeros(iii)
pulsos=iii*30/100 # percentagem de incidencias no delay
xis=n.random.randint(0,iii-iii*3/100,pulsos)
hi[xis]=n.ones(pulsos)
som = n.convolve(hi,s)

p.plot(hi*1.5+4,'ro',
        label=r"$\{h_i=\sum_{j=0}^{\Lambda_j-1}\delta_{\xi_j-i}\}_0^{\Lambda_h-1}$", ms=3)
p.plot(som,'go', label=r"$\{(t*h)_i\}_0^{\Lambda+\Lambda_h-2}$",
        markersize=3)
# p.legend(loc="upper right",numpoints=5)


# p.ylim(-5.7,11.3)
p.ylim(-2.2,7.)
# p.xlim(-10,ii+iii-2+50)

# p.xticks([0]+list(xis)+[ii+iii-2],[0]+[r"$\delta$"  for i in xis]+[r"$\Lambda+\Lambda_h-2$"],fontsize='16')
p.xticks((),())
sub3.set_xlim(-dx,ii+iii-2+dx)
sub3.set_yticks((),())

# p.ylabel(u"amalgam", fontsize=16, fontweight='bold')
ax2.set_ylabel(r"amalgam", fontsize=14, fontweight='bold')
sub3.set_xlabel(r"samples $\quad \rightarrow$",fontsize=20)

fig.legend((*p1,*p2,*p3),(r"$\{t_i\}_0^{\Lambda-1}$",r"$\{h_i=\sum_{j=0}^{\Lambda_h-1}\delta_{\xi_j-i}\}_0^{\Lambda_h-1}$",r"$\{(t*h)_i\}_0^{\Lambda+\Lambda_h-2}$"),"upper center",numpoints=5, fontsize=20)
p.savefig("../figures/delays_.png")
p.show()
