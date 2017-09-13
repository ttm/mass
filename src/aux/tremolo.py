#-*- coding: utf-8 -*-
import numpy as n, pylab as p# , scikits.audiolab as a

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.17,bottom=0.15,right=0.97,top=0.97)

fa=44100
Dv=2048 # tamanho da tabela do tremolo
fv=1.5 # frequência do tremolo
mu=12. # desvio maximo em dB do tremolo (profundidade)
f=40. # freq do som em si
D=1024 # tamanho da tabela do som
dur=2 # duração

x=n.linspace(0,2*n.pi,Dv,endpoint=False)
tabv=n.sin(x) # tabela senoidal para o tremolo

# Padrao do vibrato
ii=n.arange(fa * dur) # amostras em dur segundos
gv=n.array(ii*fv*float(D)/fa, n.int) # indices para pegar na tabela

### Som em si
tab=n.linspace(-1,1,D) # dente de serra
tv=10**(tab[gv%D]*mu/20) # desvio instantaneo de amplitude para cada amostra

gi=n.array(ii*f*(Dv/float(fa)), n.int) # a movimentacao na tabela total, jah inteiro
ti=tabv[gi%Dv]*tv
p.plot(ti,label=r"$T_i^{tr(f'=1,5Hz)}=\{t_i.a_i\}_0^{\Lambda-1}$", linewidth=2)
ti=((ti-ti.min())/(ti.max()-ti.min()))*2-1 # normalizando
# a.wavwrite(ti,"tremolo.wav",fa)

gi=n.array(  ii * (D/float(fa)) * f  , n.int ) % D
t=tab[ gi ]
# a.wavwrite(t,"original.wav",fa)

p.ylabel(r"amplitude $\quad \rightarrow $", fontsize=20)
p.xlabel(r"samples $\quad \rightarrow$",fontsize=20)

p.xlim(-2000,ii[-1]+2000)
p.ylim(-4.1,8.2)
p.xticks((0,20000,40000,60000,80000,88200),(r"0",20000,40000,60000,80000),
        fontsize=16)

p.plot(tv, label =r"$a_i=10^{t_i'\,\frac{V_{dB}}{20}};\;\; V_{dB}=12$", linewidth=4 )
p.legend(loc="upper left")
ltext = p.gca().get_legend().get_texts()
p.setp(ltext[0], fontsize = 24)
p.setp(ltext[1], fontsize = 24)
p.savefig("../figures/tremolo_.png")
p.show()
