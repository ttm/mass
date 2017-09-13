#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

H=n.hstack
V=n.vstack

f_a = 44100. # Hz, frequência de amostragem

Lambda_tilde=Lt=1024.*16

# Senoide
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras

# Quadrada:
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )

# Triangular:
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

# Dente de Serra:
D_i=n.linspace(-1,1,Lt)


def v(f=200,d=2.,tab=S_i,fv=2.,nu=2.,tabv=S_i):
    Lambda=n.floor(f_a*d)
    ii=n.arange(Lambda)
    Lv=float(len(tabv))

    Gammav_i=n.floor(ii*fv*Lv/f_a) # índices para a LUT
    Gammav_i=n.array(Gammav_i,n.int)
    # padrão de variação do vibrato para cada amostra
    Tv_i=tabv[Gammav_i%int(Lv)] 

    # frequência em Hz em cada amostra
    F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
    # a movimentação na tabela por amostra
    D_gamma_i=F_i*(Lt/float(f_a))
    Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
    Gamma_i=n.floor( Gamma_i) # já os índices
    Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
    return tab[Gamma_i%int(Lt)] # busca dos índices na tabela

def A(fa=2.,V_dB=10.,d=2.,taba=S_i):
    Lambda=n.floor(f_a*d)
    ii=n.arange(Lambda)
    Lt=float(len(taba))
    Gammaa_i=n.floor(ii*fa*Lt/f_a) # índices para a LUT
    Gammaa_i=n.array(Gammaa_i,n.int)
    # variação da amplitude em cada amostra
    A_i=taba[Gammaa_i%int(Lt)] 
    A_i=A_i*10.**(V_dB/20.)
    return A_i

def adsr(som,A=10.,D=20.,S=-20.,R=100.,xi=1e-2):
    a_S=10**(S/20.)
    Lambda=len(som)
    Lambda_A=int(A*f_a*0.001)
    Lambda_D=int(D*f_a*0.001)
    Lambda_R=int(R*f_a*0.001)

    ii=n.arange(Lambda_A,dtype=n.float)
    A=ii/(Lambda_A-1)
    A_i=A
    ii=n.arange(Lambda_A,Lambda_D+Lambda_A,dtype=n.float)
    D=1-(1-a_S)*(   ( ii-Lambda_A )/( Lambda_D-1) )
    A_i=n.hstack(  (A_i, D  )   )
    S=n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D),dtype=n.float)*a_S
    A_i=n.hstack( ( A_i, S )  )
    ii=n.arange(Lambda-Lambda_R,Lambda,dtype=n.float)
    R=a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
    A_i=n.hstack(  (A_i,R)  )

    return som*A_i

triadeM=[0.,4.,7.]
def ac(f=200.,notas=[0.,4.,7.,12.],tab=S_i):
    acorde=adsr(v(tab=tab,f=f*2.**(notas[-1]/12.),nu=0))
    for na in notas[:-1]:
        acorde+=adsr(v(tab=tab,f=f*2**(na/12.),nu=0))
    
    return acorde


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


Emf_i=[0.,1.,3.,5.,7.,8.,10.]
E=Emf_i+Emf_i[::-1]

bb=contraNotaNotaSup(E)

s=H(([adsr(v(f=200*2**(b/12.),d=.2)) for b in bb   ]))

s1=H(([adsr(v(f=200.*2.**(b/12.),d=.2))+\
       adsr(v(f=200*2.**(ee/12.),d=.2)) for b,ee in zip(bb,E)   ]))

m=[0,7,7,7,2,7,7,5,3,5,1,0,7,1,0,0]
cc=contraNotaNotaSup(m)

s2=H(([adsr(v(f=200.*2.**(b/12.),d=.2))+\
       adsr(v(f=200*2.**(ee/12.),d=.2)) for b,ee in zip(cc,m)   ]))

s=H((s,s1,s2,s2,s1,s1))

s=((s-s.min())/(s.max()-s.min()))*2.-1.

# most music players read only 16-bit wav files, so let's convert the array
s = n.int16(s * float(2**15))

w.write("contaPonto.wav",f_a,s) # escrita do som


