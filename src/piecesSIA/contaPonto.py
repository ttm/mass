import numpy as n
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
W = fun.W
Tr_i = fun.Tr
Q_i = fun.Q
D_i = fun.Sa
S_i = fun.S
H = n.hstack
V = n.vstack
def A(fa=2.,V_dB=10.,d=2.,taba=fun.S):
    return fun.T(d, fa, V_dB, taba=taba)
def adsr(s, A=20, D=20, S=-10, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
def T(f1, f2, dur, ttype="exp", tab=S_i, alpha=1.):
    return adsr(fun.P(f1, f2, dur, alpha, tab, ttype))
f_a = 44100 # Hz, sample rate

############## 2.3.2 Rudimentos de contraponto
def contraNotaNotaSup(alturas=[0,2,4,5,5,0,2,0,2,2,2,0,7,\
                                     5,4,4,4,0,2,4,5,5,5]):
    """Realiza rotina de independência das vozes
    
    Limitado em 1 oitava acima da nota"""
    primeiraNota=alturas[0]+(7,12)[n.random.randint(2)]
    contra=[primeiraNota]

    i=0
    cont=0 # contador de paralelas
    reg=0 # registrador de intervalo em que se fez a paralela
    for al in alturas[:-1]:
        mov_cf=alturas[i:i+2]
        atual_cf,seguinte_cf=mov_cf
        if seguinte_cf-atual_cf>0:
            mov="asc"
        elif seguinte_cf-atual_cf<0:
            mov="des"
        else:
            mov="obl"

        # possibilidades por consonancia
        possiveis=[seguinte_cf+interval for interval in\
                                    [0,3,4,5,7,8,9,12]]
        movs=[]
        for pos in possiveis:
            if pos -contra[i] < 0:
                movs.append("desc")
            if pos - contra[i] > 0:
                movs.append("asc")
            else:
                movs.append("obl")

        movt=[]
        for m in movs:
            if 'obl' in (m,mov):
                movt.append("obl")
            elif m==mov:
                movt.append("direto")
            else:
                movt.append("contrario")
        blacklist=[]
        for nota,mt in zip(possiveis,movt):

            if mt == "direto": # mov direto
                # n aceita intervalo perfeito
                if nota-seguinte_cf in (0,7,12):
                    possiveis.remove(nota)
        ok=0
        while not ok:
            nnota=possiveis[n.random.randint(len(possiveis))]
            if nnota-seguinte_cf==contra[i]-atual_cf: # paralelo
                intervalo=contra[i]-atual_cf
                novo_intervalo=nnota-seguinte_cf
                if abs(intervalo-novo_intervalo)==1: # do mesmo tipo 3 ou 6
                    if cont==2: # se já teve 2 paralelas
                        pass # outro intrevalo
                    else:
                        cont+=1
                        ok=1
            else: # mov obl ou contrario
                cont=0 # zera paralelos
                ok=1
        contra.append(nnota)
        i+=1
    return contra


Emf_i=[0.,1.,3.,5.,7.,8.,10.]*2
E=Emf_i+Emf_i[::-1]

bb=contraNotaNotaSup(E)

# s=H(([adsr(v(f=200*2**(b/12.),d=.2)) for b in bb   ]))
s=H(([adsr(v(f=200*2**(b/12.),d=.2)) for b in E   ]))

s1=H(([adsr(v(f=200.*2.**(b/12.),nu=1,d=.2))+\
       adsr(v(f=400*2.**(ee/12.),nu=1,d=.2)) for b,ee in zip(bb,E)   ]))

m=[0,7,7,7,2,7,7,5,3,5,1,0,7,1,0,0]
cc=contraNotaNotaSup(m)

s2=H(([adsr(v(f=400.*2.**(b/12.),nu=.2,d=.2))+\
       adsr(v(f=200*2.**(ee/12.),nu=.2,d=.2)) for b,ee in zip(cc,m)   ]))

sf=adsr(v(f=200.*2.**(bb[-1]/12.),nu=.2,fv=9,d=2))+\
     adsr(v(f=200*2.**(E[-1]/12.),nu=.2,fv=9,d=2))

s=H((s,s1,s2,s2,s1,s1,sf))

W(s, "contaPonto.wav")


