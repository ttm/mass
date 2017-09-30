import numpy as n
import imp
io.__s = imp.load_source("io","../aux/io.py").__s
H=n.hstack
V=n.vstack

f_s = 44100. # Hz, frequência de amostragem

Lambda_tilde=Lt=1024.*16

# Sine
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senóide com T amostras

# Quadrada:
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )

# Triangular:
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

# Dente de Serra:
D_i=n.linspace(-1,1,Lt)


def v(f=200,d=2.,tab=Tr_i,fv=2.,nu=2.,tabv=S_i):
    Lambda=n.floor(f_s*d)
    ii=n.arange(Lambda)
    Lv=float(len(tabv))

    Gammav_i=n.floor(ii*fv*Lv/f_s) # índices para a LUT
    Gammav_i=n.array(Gammav_i,n.int)
    # padrão de variação do vibrato para cada amostra
    Tv_i=tabv[Gammav_i%int(Lv)] 

    # frequência em Hz em cada amostra
    F_i=f*(   2.**(  Tv_i*nu/12.  )   ) 
    # a movimentação na tabela por amostra
    D_gamma_i=F_i*(Lt/float(f_s))
    Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
    Gamma_i=n.floor( Gamma_i) # já os índices
    Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
    return tab[Gamma_i%int(Lt)] # busca dos índices na tabela

def A(fa=2.,V_dB=10.,d=2.,taba=S_i):
    Lambda=n.floor(f_s*d)
    ii=n.arange(Lambda)
    Lt=float(len(taba))
    Gammaa_i=n.floor(ii*fa*Lt/f_s) # índices para a LUT
    Gammaa_i=n.array(Gammaa_i,n.int)
    # variação da amplitude em cada amostra
    A_i=taba[Gammaa_i%int(Lt)] 
    A_i=A_i*10.**(V_dB/20.)
    return A_i

def adsr(som,A=10.,D=20.,S=-20.,R=100.,xi=1e-2):
    a_S=10**(S/20.)
    Lambda=len(som)
    Lambda_A=int(A*f_s*0.001)
    Lambda_D=int(D*f_s*0.001)
    Lambda_R=int(R*f_s*0.001)

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

### standard values
# ADSR
A_ = 10.
D = 20.
S = -20.
R = 100.

# Tremolo:
fa = 2.
V_dB = 3.

# Vibrato:
fv = 6.
nu = .5

allV = [A_, D, S, R, fa, V_dB, fv, nu]

def note(interval=0, duration=2, base_freq=220, nvoices = 20, dev = 0.05):
    f = base_freq*2**(interval/12)
    allV_ = [f] + allV

    s = n.zeros(n.floor(f_s*duration))
    for voice in range(nvoices):
        p = allV_*n.random.normal(1,dev,9)
        sa = v(p[0], duration, fv=p[-2], nu=p[-1])
        sa = sa*A(p[-4], p[-3], duration)
        sa = adsr(sa, p[1], p[2], p[3], p[4])
        s += sa

    return s


### melodies, chords...
# melody
m1 = [0,   7, 8,   7, 11,   12, 0,    2, 0]
d1 = [1,   2, 1,   2, 1,    2, 1,     1, 3] 
s = H([note(i, j) for i,j in zip(m1, d1)])
W("childChoir_.wav",f_s, s) # escrita do som

# chords
c1 = [0, 3, 7]
c2 = [7, 11, 2]
c2_ = [7, 11, 2,5]
c3 = [5, 8, 0]
dc = [2,   2, 1,   2, 1,    2, 1,     1, 3]
c =  [c1,  c2,c3,  c2,c2_,  c1,c3,    c2,c1]
def chord(intervals=[0, 4, 7], duration=2, base_freq=220, nvoices = 20, dev = 0.05):
    s = n.zeros(n.floor(f_s*duration))
    for i in intervals:
      s += note(i, duration, base_freq, nvoices, dev)
    return s

s2 = H([chord(i, j, base_freq=220, dev=0.001) for i,j in zip(c, dc)])
W("childChoir_2.wav",f_s, s2)  # escrita do som

sh = H([note(i, j, base_freq=440, dev = 0.02) for i,j in zip(m1, d1)])
s_ = H( (n.zeros(f_s), sh))
mixed = s_*5+s2
final = H( (s*5, mixed) )
W("childChoir_3.wav",f_s, final)  # escrita do som
