#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n
f=n.fft.fft
p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.17,bottom=0.15,right=0.97,top=0.97)
#a=[-1,1]
#n2=n.random.rand(2)*2-1 # 2 amostras quaisquer E [-1,1]
n2=n.array([-0.45599766,  0.77080613])
ff=f(n2)
#-1 * cos(n.pi*l)
p.plot([0,1],n2,"bo")

# Primeira componente, 0Hz
a0=n.real(ff[0]) 
b0=n.imag(ff[0]) # sempre zero

# Segundo componente, t_a/N Hz
ab1=n.abs(ff[1]) # (a**2+b**2)**0.5 = a1 neste caso
a1=n.real(ff[1]) # eh o modulo ab1 tambem neste caso
b1=n.imag(ff[1]) # zero para o caso de somente 2 amostras pois a fase eh nula e isen(0)=0
#fas=n.arctan(b1/a1) # fase fas=n.angle(f[1])
fas=0 # não há adição de fase para este caso de 2 amostras
# mas o sinal do a_1 => sinal da senóide, inversão pi
# ou seja, se a1<0, n2[0] > n2[1]
if a1<0: fas+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a1: %s, b1: %s, fas: %s" % (ab1,a1,b1,fas))


ii=n.linspace(-0.5*n.pi,1.5*n.pi,200) # período de oscilação pura
iii=n.linspace(-0.5,1.5,200) # domínio temporal das amostras 
s=(ab1/2)*n.cos(ii+fas)+a0/2 # Reconstruindo senóide para o domínio dado
p.plot(iii,s,"m--") # plotada a senóide passando pelas amostras

p.xticks((-1,0,1,2),(r"$-\delta_a$",r"$0$",r"$\delta_a$",r"$2\delta_a$"), size=20)
# valores cruciais em y
p.yticks((a0/2-ab1/2,a0/2,a0/2+ab1/2),
        (r'$\frac{a_0-|a_1|}{2}$',r'$\frac{a_0}{2}$',r'$\frac{a_0+|a_1|}{2}$'),
        color = 'k', size = 33)
p.plot((-10,10),(a0/2,)*2,"k--")
p.plot((-10,10),(a0/2-ab1/2,)*2,"k--")
p.plot((-10,10),(a0/2+ab1/2,)*2,"k--")

# Para legendas aa direita
#p.text(2.05, 0.5, r"\bf{level set} $\phi$", {'color' : 'g', 'fontsize' : 20},
        #horizontalalignment = 'left',
        #verticalalignment = 'center',
        #rotation = 90,
        #clip_on = False)
#p.text(2.01,a0/2-ab1/2, r'$\frac{a_0-\sqrt{a_1^2+b_1^2}}{2}$', {'color' : 'k', 'fontsize' : 20})
#p.text(2.01, a0/2, r"$\frac{a_0}{2}$", {'color' : 'k', 'fontsize' : 20})
#p.text(2.01,a0/2+ab1/2, r'$\frac{a_0+\sqrt{a_1^2+b_1^2}}{2}$', {'color' : 'k', 'fontsize' : 20})

p.text(0,-.8,r"$t_0<t_1 \Leftrightarrow a_1<0$",fontsize=17)

p.xlim(-1.2,2)
#p.xlim(0,T2*.56)
p.ylim(-1.1,1.1)

p.ylabel(r"amplitude $\rightarrow$", fontsize=19)
p.xlabel(r"time $\rightarrow$", fontsize=19)
p.savefig("../figures/amostras2c___.png")
p.show()
