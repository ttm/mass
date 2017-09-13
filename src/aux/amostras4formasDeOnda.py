#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n
f=n.fft.fft

#n4=n.random.rand(4)*2-1
n4=n.array([ 0.58003705, -0.30828309, -0.29797696, -0.99219078])
T=4
#T=1024
l=n.linspace(0,2*n.pi,T,endpoint=False)
senoide=n.sin(l)
dente=n.linspace (-1,1,T) # dente de serra
triangular=n.hstack ((n.linspace(-1,1,T/2,endpoint=False),n.linspace(1,-1,T/2,endpoint=False)))
quadrada=n.hstack ((n.ones(T/2),n.ones(T/2)* -1))

ondas=[senoide,dente,triangular,quadrada]
ondas_n=[u"sinusoid","sawtooth","triangle","square"]

fig=p.figure(figsize=(12.,6.))
fig.subplots_adjust(left=0.04,bottom=0.13,right=0.99,top=0.95,wspace=0.14, hspace=0.37)
subs=[]
for i in range(4):
    subs.append(fig.add_subplot(int("22"+str(i+1))))
    p.title(ondas_n[i])
    n4=ondas[i]
    p.plot(n4,"bo")

    ff=f(n4)

    # Primeiro componente, 0Hz
    a0=n.real(ff[0]) 
    b0=n.imag(ff[0]) # sempre zero

    # Segundo componente, t_a/N Hz
    ab1=n.abs(ff[1]) # (a**2+b**2)**0.5
    a1=n.real(ff[1])
    b1=n.imag(ff[1])
    fas=n.arctan(b1/a1) # fase fas=n.angle(f[1])
    if a1<0: fas+=n.pi # segundo e terceiro quadrantes somam pi
    print("abs: %s, a1: %s, b1: %s, fas: %s" % (ab1,a1,b1,fas))

    # Segundo componente, t_a/N Hz
    ab2=n.abs(ff[2]) # (a**2+b**2)**0.5
    a2=n.real(ff[2])
    b2=n.imag(ff[2])
    if a2: fas2=n.arctan(b2/a2) # fase fas=n.angle(f[1])
    else: fas2=0
    if a2<0: fas2+=n.pi # segundo e terceiro quadrantes somam pi
    print("abs: %s, a2: %s, b2: %s, fas2: %s" % (ab2,a2,b2,fas2))

    fr1=(2*n.pi/4)/2 #ciclo em 4 * \delta_a, metade do intervalo angular 
    fr2=1/2. # metade de \delta_a
    #fr1=fr2=0
    ii=n.linspace(0-fr1,2*n.pi-fr1,200) # [0,2*pi] ciclo completo
    iii=n.linspace(0-fr2,4-fr2,200) # [0,3] == 3 \delta_a, período

    s=(1/4.)*ab2*n.cos(2*ii+fas2)+(2/4.)*ab1*n.cos(ii+fas)+a0/4
    p.plot(iii,s,"m", linewidth=3, label=r"$\oplus$")
    ss=(1/4.)*ab2*n.cos(2*ii+fas2)
    sss=(2/4.)*ab1*n.cos(ii+fas)
    p.plot(iii,[a0/4]*200,"k:", label=r"$\frac{a_0}{4}$")
    p.plot(iii,sss,"g-.",label=r"$\frac{2}{4}\sqrt{a_1^2+b_1^2}cos\left(\frac{2\pi . 1 }{\Lambda}i - tg^{-1}\left(\frac{b_1}{a_1}\right)\right)$")
    p.plot(iii,ss,"r--", label=r"$\frac{1}{4}\sqrt{a_2^2 + b_2^2}cos\left(\frac{2\pi . 2 }{\Lambda}i - tg^{-1}\left(\frac{b_2}{a_2}\right)\right)$")

    #p.legend(loc="upper right")
    if i ==1:
        p.xlim(-1.2,4.2)
        p.ylim(-1.2,1.2)
    elif i ==3:
        p.xlim(-1.2,4.2)
        p.ylim(-1.5,1.5)
    else:
        p.xlim(-1.2,4.2)
        p.ylim(-1.1,1.1)

    p.xlim(-1.2,4.2)
    p.ylim(-1.49,1.49)
    p.yticks((),())
    p.xticks((-1,0,1,2,3,4),(r"$-\delta_a$",r"$0$",r"$\delta_a$",r"$2\delta_a$",r"$3\delta_a$",r"$4\delta_a$"),
            size=17)
subs[0].set_ylabel(r"amplitude $\rightarrow$",
            {"y": -.1, "fontsize": 20})
subs[2].set_xlabel(r"time $\rightarrow$", {"x": 1.11, "fontsize": 20})
p.savefig("../figures/amostras4formas___.png")
p.show()
