#-*- coding: utf-8 -*-
import pylab as p, numpy as n
fig=p.figure(figsize=(10.,5.))
ax=fig.add_subplot(111)

T=2**7
#p.xlabel(r"$\gamma_i=i.f\frac{\widetilde{\Lambda}}{f_a}$", fontsize=26)
p.xlabel(r"samples $\rightarrow$", fontsize=26)
p.ylabel(r"amplitude $\rightarrow$", fontsize=26)
p.plot(n.sin(n.linspace(0,2*n.pi,T, endpoint=False)),"ro",ms=3,label=r"$\{ \; \widetilde{l}_i \; \}_0^{ \widetilde{\Lambda} -1 }$")
#int(155*f*T/fa)%T

p.xlim(-3,T+3)
p.ylim(-1.05,1.05)

p.xticks((0,T-1),(0,r"$\widetilde{\Lambda}-1$"),fontsize=26)
p.yticks(fontsize=15)

# p.text(15,-.7,r"$t_i^{f}=\widetilde{l}_{\left\lfloor i.f\frac{\widetilde{\Lambda}}{f_a} \right\rfloor \%\,\widetilde{\Lambda}}$",fontsize=38)

ax.annotate(r"$t_{5023}^{200}=\widetilde{l}_{\left\lfloor 5023 \times\, 200\frac{128}{44100} \right\rfloor \% 128 }=\widetilde{l}_{99}$", xy=(99, n.sin(99.)),  xycoords='data',
                xytext=(T,.3), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top',
                fontsize=24
                )
p.legend(loc="upper right",numpoints=5, prop={'size':20})
p.subplots_adjust(left=0.11,bottom=0.19,right=0.97,top=0.97)
p.savefig("../figures/lut_.png")
p.show()
