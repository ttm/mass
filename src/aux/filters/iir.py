#-*- coding: utf8 -*-
import numpy as n, pylab as p

def lp(fc, npoints=1000):
    x=n.e**(-2*n.pi*fc) # fc=> freq de corte em 3dB
    # coeficientes
    a0=1-x
    b1=x
    # aplicação da equação a diferenças
    sinal=[a0]
    for i in range(npoints):
        sinal.append(sinal[-1]*b1)
    # cálculo do espectro
    fft=n.fft.fft(sinal)
    m=n.abs(fft)
    return m

def hp(fc, npoints=1000):
    x=n.e**(-2*n.pi*fc) # fc=> freq de corte em 3dB
    a0=(1+x)/2
    a1=-(1+x)/2
    b1=x
    sinal=[a0]
    sinal+=[a1+sinal[-1]*b1]
    # aplicação da equação a diferenças
    for i in range(npoints):
        sinal.append(sinal[-1]*b1)
    # cálculo do espectro
    fft=n.fft.fft(sinal)
    m=n.abs(fft)
    return m

def notch(f,bw,ftype='bs'):
    """Use ftype=='bp' para filtro passa banda """
    if ftype=='bs':
        r=1-3*bw
        k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))
        
        # coefs rejeita banda
        a0=k
        a1=-2*k*n.cos(2*n.pi*f)
        a2=k
        b1=2*r*n.cos(2*n.pi*f)
        b2=-r**2
        
        sinal=[a0]
        sinal+=[a1+sinal[-1]*b1]
        sinal+=[a2+sinal[-1]*b1+sinal[-2]*b2]
        for i in range(44100):
            sinal.append(sinal[-1]*b1+sinal[-2]*b2)
        fft=n.fft.fft(sinal)
        m=n.abs(fft)
        return m
    else:
        r=1-3*bw
        k=(1-2*r*n.cos(2*n.pi*f)+r**2)/(2-2*n.cos(2*n.pi*f))
        
        # coefs passa banda
        a0=1-k
        a1=-2*(k-r)*n.cos(2*n.pi*f)
        a2=r**2 -k
        b1=2*r*n.cos(2*n.pi*f)
        b2=-r**2
        
        sinal=[a0]
        sinal+=[a1+sinal[-1]*b1]
        sinal+=[a2+sinal[-1]*b1+sinal[-2]*b2]
        for i in range(44100):
            sinal.append(sinal[-1]*b1+sinal[-2]*b2)
        fft=n.fft.fft(sinal)
        m=n.abs(fft)
        return m
fa=44100.

fig=p.figure(figsize=(12.,6.))
fig.subplots_adjust(left=0.06,bottom=0.15,right=0.97,top=0.95,wspace=0.06, hspace=0.39)

ax=p.subplot(221)
#ax.set_xscale('log')
fcs=[0.005,0.05,0.1,0.2,0.3,0.4]
N=10000
poss=[(.1*(N/2),0.15),(0.25*(N/2.),0.40),(.37*(N/2.),0.53),(.5*(N/2),0.7),(0.6*(N/2.),0.82),(0.7*(N/2.),0.90)]
ds=fa/N
fs=[i*ds for i in range(1,N//2+1)]
fs=n.log2(fs)
fs=n.hstack(([2*fs[0]-fs[1]],fs))
#p.plot((fs[0],fs[0]),(-100,100),'c',linewidth=3)
i=0
for fc,pos in zip(fcs,poss):
    m=lp(fc,N)
    p.plot(m[:len(m)/2+1])
    if i == 0:
        p.text(pos[0],pos[1]-.01,r"$f_c=%s$" % (fc,), fontsize=20)
        i=1
    else:
        p.text(pos[0],pos[1]-.01,r"%s" % (fc,), fontsize=16)
#    p.plot([fc*len(m),fc*len(m)],[-1000,1000])
ii=range(1,11)
# p.ylabel(u"amplitude"+r"$\; \rightarrow$", fontsize=16)
# p.xlabel(u"frequency "+r"$  \; \rightarrow$", fontsize=16)
p.xticks((0,len(m)/8,len(m)/4,3*len(m)/8,len(m)/2),(r"0",r"$\frac{f_a}{8}$",
    r"$\frac{f_a}{4}$", r"$\frac{3 f_a}{8}$",
    r"$\frac{f_a}{2}$"),fontsize='20')
p.ylim(0,1.2)
p.title("(a) First order low-pass filter")
ax.set_ylabel(r"amplitude $\rightarrow$",
            {"y": -.1, "fontsize": 20})
#p.xlim(xvals[0]-1,n.log2(fa/2))
#p.ylim(-123,3)

s2=p.subplot(222)
fcs=[0.005,0.05,0.1,0.2,0.49999]
poss=[(13,1.035),(39,0.85),(80,0.75),(120,0.67),(200,0.52)]
i=0
for fc,pos in zip(fcs,poss):
    m=hp(fc)
    #p.plot(m[:len(m)/2])
    p.plot(m[:len(m)/2])
    if i==0:
        p.text(pos[0],pos[1]-.005,r"$f_c=%s$" % (fc,), fontsize=20)
        i=1
    else:
        p.text(pos[0],pos[1]-.009,r"$%s$" % (fc,), fontsize=16)
p.xticks((0,len(m)/8,len(m)/4,3*len(m)/8,len(m)/2),(r"0",r"$\frac{f_a}{8}$",
    r"$\frac{f_a}{4}$", r"$\frac{3 f_a}{8}$",
    r"$\frac{f_a}{2}$"), size=20)
#    p.plot([fc*len(m),fc*len(m)],[-1000,1000])
#p.ylim(-30,0)
p.ylim(0,1.2)
s2.set_yticks((),())
ax2 = s2.twinx()
ax2.set_yticks((0,0.2,0.4,0.6,0.8,1.0,1.2))
# p.ylabel(u"amplitude "+r"$\; \rightarrow$", fontsize=16)
# p.xlabel(u"frequency "+r"$  \; \rightarrow$", fontsize=16)
p.title("(b) First order high-pass filter")


##########
# Notch Rejeita Banda
ax=p.subplot(223)
f=0.05
bw=f/150;  m=notch(f,bw); p.plot(m[:len(m)/2],'r', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c)/150 $ ")
bw=f/10;  m=notch(f,bw); p.plot(m[:len(m)/2], 'g', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c)/10 $ ")
bw=f; m=notch(f,bw); p.plot(m[:len(m)/2], 'b', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c) $ ")

f=0.25
bw=f/150;  m=notch(f,bw); p.plot(m[:len(m)/2], 'r')
bw=f/10;  m=notch(f,bw); p.plot(m[:len(m)/2], 'g')
bw=f; m=notch(f,bw); p.plot(m[:len(m)/2], 'b')

f=0.45
bw=(0.5 - f)/150;  m=notch(f,bw); p.plot(m[:len(m)/2], 'r')
bw=(0.5 - f)/10;  m=notch(f,bw); p.plot(m[:len(m)/2], 'g')
bw=(0.5 - f); m=notch(f,bw); p.plot(m[:len(m)/2], 'b')

p.xticks((0,int(0.05*len(m)),int(0.25*len(m)),int(0.45*len(m))),(r"0",r"$f_c=\frac{f_a}{20}$",
    r"$f_c=\frac{f_a}{4}$", r"$f_c=\frac{9 f_a}{20}$"),fontsize='20')
p.yticks((0,0.5,1,1.5),(0,0.5,1,1.5))
p.xlim(0,len(m)/2)
p.ylim(0,4.5)
p.title("(c) Two pole band-reject filter")
p.legend(loc="upper left", labelspacing=0,prop={'size':16})

ax.set_xlabel(r"frequency $\rightarrow$",
            {"x": 1.11, "fontsize": 20})
# p.ylabel(u"amplitude "+r"$\; \rightarrow$", fontsize=16)
# p.xlabel(u"frequency "+r"$  \; \rightarrow$", fontsize=16)


##########
# Notch Passa Banda

s4=fig.add_subplot(224)
p.ylim(0,4.5)
f=0.05
bw=f/(5*150);  m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2],'r', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c)/750 $ ")
bw=f/(5*10);   m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2], 'g', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c)/50 $ ")
bw=f/5;      m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2], 'b', label=r" $ bw=min(f_c,\frac{f_a}{2}-f_c)/5 $ ")

f=0.25
bw=f/(5*150);  m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2], 'r')
bw=f/(5*10);   m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2], 'g')
bw=f/5;      m=notch(f,bw, 'bp'); p.plot(m[:len(m)/2], 'b')

f=0.45
bw=(0.5 - f)/(5*150);  m=notch(f,bw,'bp'); p.plot(m[:len(m)/2], 'r')
bw=(0.5 - f)/(5*10);   m=notch(f,bw,'bp'); p.plot(m[:len(m)/2], 'g')
bw=(0.5 - f)/5;      m=notch(f,bw,'bp'); p.plot(m[:len(m)/2], 'b')

p.xticks((0,int(0.05*len(m)),int(0.25*len(m)),int(0.45*len(m))),(r"0",r"$f_c=\frac{f_a}{20}$",
    r"$f_c=\frac{f_a}{4}$", r"$f_c=\frac{9 f_a}{20}$"),fontsize='20')
# p.yticks((0,0.5,1,1.5,2),(0,0.5,1,1.5,2))
s4.set_yticks((),())
ax2 = s4.twinx()
ax2.set_yticks((0,0.5,1,1.5,2))
p.xlim(0,len(m)/2)
#p.ylim(0,2.5)
p.title("(d) Two pole band-pass filter")
s4.legend(loc="upper right", labelspacing=0,prop={'size':16})
p.ylim(0,4.5)

# p.ylabel(u"amplitude "+r"$\; \rightarrow$", fontsize=16)
# p.xlabel(u"frequency "+r"$  \; \rightarrow$", fontsize=16)

p.savefig("../../figures/iir__.png")
p.show()
