#-*- coding: utf-8 -*-
import numpy as n, pylab as p#, scikits.audiolab as a

fa=44100 # frequência de amostragem
Dv=2048 # tamanho da tabela do vibrato
fv=1.5 # frequência do vibrato
nu=12. # desvio maximo em semitons do vibrato (profundidade)
f=1040. # freq do som em si
D=1024 # tamanho da tabela do som
dur=2 # duração em segundos

x=n.linspace(0,2*n.pi,Dv,endpoint=False)
tabv=n.sin(x) # tabela senoidal para o vibrato

# Padrao do vibrato
ii=n.arange(fa * dur) # 2 segundos
gv=n.array(ii*fv*float(Dv)/fa, n.int) # indices
tv=tabv[gv%Dv]*nu # desvio instantaneo de semitons para cada amostra
fi=f*(  2.**(  tv/12.  )   ) # frequência em Hz em cada amostra

### Som em si
tab=n.linspace(-1,1,D) # dente de serra

dD=fi*(D/float(fa)) # a movimentação na tabela por amostra
gi=n.cumsum(dD,0,n.int) # a movimentação na tabela total, já os índices
ti=tabv[gi%D] # busca dos índices na tabela
# a.wavwrite(ti,"vibrato.wav",fa) # escrita do som

gi=n.array(  ii * (D/float(fa)) * f  , n.int ) % Dv
t=tabv[ gi ]
# a.wavwrite(t,"original.wav",fa)

p.figure(figsize=(10.,5.))
p.subplots_adjust(left=0.17,bottom=0.15,right=0.97,top=0.97)
p.specgram(ti-ti.mean())
p.colorbar()
p.xlim(-2000,46100)
p.xticks((0,10000,20000,30000,44000),(r"0",10000,20000,30000,44100),
        fontsize=16)
p.yticks(fontsize=16)
p.ylabel(u"frequency "+r"$ \in \; [0,\,\frac{f_a=44100}{2}=22050] \, \rightarrow $", fontsize=19)
p.xlabel(r"samples $\quad \rightarrow$",fontsize=21)
p.savefig("../figures/vibrato_.png")
p.show()
