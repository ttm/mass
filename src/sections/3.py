#-*- coding: utf-8 -*-
import numpy as n
from scipy.io import wavfile as w

f_a = 44100  # Hz, sample rate

############## 2.2.1 Wave table (LUT)
# table size: use even to do not end in conflict
# and at least 1024
Lambda_tilde = Lt = 1024

# Sinusoid
foo = n.linspace(0, 2*n.pi, Lt, endpoint=False)
S_i = n.sin(foo)  # a sinusoid period with T samples

# Square:
Q_i = n.hstack((n.ones(Lt/2)*-1, n.ones(Lt/2)))

# Triangular:
foo = n.linspace(-1, 1, Lt/2, endpoint=False)
Tr_i = n.hstack((foo, foo*-1))

# Sawtooth:
D_i = n.linspace(-1, 1, Lt)

# real sound, import period and
# use the right T: number of samples in the period
Rf_i = w.read("22686__acclivity__oboe-a-440_periodo.wav")[1]

f = 110.  # Hz
Delta = 3.4  # seconds
Lambda = int(Delta*f_a)

# Samples:
ii = n.arange(Lambda)

### 2.32 LUT
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
# It is possible to use S_i, Q_i, D_i or any other period of the real sound
# with a sufficient length
L_i = Tr_i
TfD_i = L_i[Gamma_i % Lt]


############## 2.2.2 Incremental variations of frequency and amplitude
# FREQUENCY VARIATIONS
f_0 = 100.  # initial freq in Hz
f_f = 300.  # final freq in Hz
Delta = 2.4  # duration

Lambda = int(f_a*Delta)
ii = n.arange(Lambda)
### 2.33 - linear variation
f_i = f_0+(f_f-f_0)*ii/(float(Lambda)-1)
### 2.34 coefficients for wavetable
D_gamma_i = f_i*Lt/f_a
Gamma_i = n.cumsum(D_gamma_i)
Gamma_i = n.array(Gamma_i, dtype=n.int)
### 2.35 resulting sound
Tf0ff_i = L_i[Gamma_i % Lt]

#### 2.36 - exponential variation
f_i = f_0*(f_f/f_0)**(ii/(float(Lambda)-1))
### 2.37 coefficients for wavetable
D_gamma_i = f_i*Lt/f_a
Gamma_i = n.cumsum(D_gamma_i)
Gamma_i = n.array(Gamma_i, dtype=n.int)
### 2.38 resulting sound
Tf0ff_i = L_i[Gamma_i % Lt]


# VARIAÇÕES DE AMPLITUDE
# sintetizando um som qualquer para
# a variação de amplitude
f = 220.  # Hz
Delta = 3.9  # segundos
Lambda = int(Delta*f_a)

# Amostras:
ii = n.arange(Lambda)

# (como em 2.30)
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
L_i = Tr_i  # pode-se usar igualmente S_i, Q_i, D_i ou
# qualquer período de som real suficientemente grande
T_i = TfD_i = L_i[Gamma_i % Lt]

a_0 = 1.  # razão da amplitude em que é iniciada a sequência
a_f = 12.  # razão da amplitude em que é finalizada
alpha = 1.  # índice de suavidade da transição
### 2.39 envoltória exponencial para transição de amplitude
A_i = a_0*(a_f/a_0)**((ii/float(Lambda))**alpha)
### 2.40 aplicação da envoltória no som T_i
T2_i = A_i*T_i

### 2.41 envoltória linear de amplitude
A_i = a_0+(a_f-a_0)*(ii/float(Lambda))

### 2.42 transição exponencial de V_dB
V_dB = 31.
T2_i = T_i*((10*(V_dB/20.))**((ii/float(Lambda))**alpha))


############## 2.2.3 Aplicação de filtros digitais
# VEJA iir.py para a geraçào da figura 2.17
# T_i herdado
# resposta ao impulso sintética (reverb)
H_i = (n.random.random(10)*2-1)*n.e**(-n.arange(10))

### 2.43 Convolução
T2_i = n.convolve(T_i, H_i)

### 2.44 veja linhas seguintes para aplicação da
### equação a diferenças :-)

fc = .1
### 2.45 passa baixas de polo simples
x = n.e**(-2*n.pi*fc)  # fc  = > freq de corte em 3dB
# coeficientes
a0 = 1-x
b1 = x
# aplicação do filtro
T2_i = [T_i[0]]
for t_i in T_i[1:]:
    T2_i.append(t_i*a_0+T2_i[-1]*b1)

### 2.46 passa altas de polo simples
x = n.e**(-2*n.pi*fc)  # fc = > freq de corte em 3dB
a0 = (1+x)/2
a1 = -(1+x)/2
b1 = x

# aplicação do filtro
T2_i = [a0*T_i[0]]
last = T_i[0]
for t_i in T_i[1:]:
    T2_i += [a0*t_i + a1*last + b1*T2_i[-1]]
    last = n.copy(t_i)


fc = .1
bw = .05
### 2.47 Variáveis auxiliares para os filtros nó
r = 1-3*bw
k = (1-2*r*n.cos(2*n.pi*fc)+r**2)/(2-2*n.cos(2*n.pi*fc))

### 2.48 passa banda
# coefs passa banda
a0 = 1-k
a1 = -2*(k-r)*n.cos(2*n.pi*fc)
a2 = r**2 - k
b1 = 2*r*n.cos(2*n.pi*fc)
b2 = -r**2

# aplicacao do filtro em T_i resultando em T2_i
T2_i = [a0*T_i[0]]
T2_i += [a0*T_i[1]+a1*T_i[0]+b1*T2_i[-1]]
last1 = T_i[1]
last2 = T_i[0]
for t_i in T_i[2:]:
    T2_i += [a0*t_i+a1*last1+a2*last2+b1*T2_i[-1]+b2*T2_i[-2]]
    last2 = n.copy(last1)
    last1 = n.copy(t_i)

### 2.49 rejeita banda
# coeficientes
a0 = k
a1 = -2*k*n.cos(2*n.pi*fc)
a2 = k
b1 = 2*r*n.cos(2*n.pi*fc)
b2 = -r**2

# aplicacao do filtro em T_i resultando em T2_i
T2_i = [a0*T_i[0]]
T2_i += [a0*T_i[1]+a1*T_i[0]+b1*T2_i[-1]]
last1 = T_i[1]
last2 = T_i[0]
for t_i in T_i[2:]:
    T2_i += [a0*t_i+a1*last1+a2*last2+b1*T2_i[-1]+b2*T2_i[-2]]
    last2 = n.copy(last1)
    last1 = n.copy(t_i)


############## 2.2.4 Ruídos
# VEJA ruidos.py para o script que gerou a figura 2.18
Lambda = 100000  # Lambda sempre par
# diferença das frequências entre coeficiêntes vizinhos:
df = f_a/float(Lambda)

### 2.50 Ruido branco
# geração de espectro com módulo 1 uniforme
# e fase aleatória
coefs = n.exp(1j*n.random.uniform(0, 2*n.pi, Lambda))
# real par, imaginaria impar
coefs[Lambda/2+1:] = n.real(coefs[1:Lambda/2])[::-1] - 1j * \
    n.imag(coefs[1:Lambda/2])[::-1]
coefs[0] = 0.  # sem bias
coefs[Lambda/2] = 1.  # freq max eh real simplesmente

# as frequências relativas a cada coeficiente
# acima de Lambda/2 nao vale
fi = n.arange(coefs.shape[0])*df
f0 = 15.  # iniciamos o ruido em 15 Hz
i0 = n.floor(f0/df)  # primeiro coef a valer
coefs[:i0] = n.zeros(i0)
f0 = fi[i0]

# obtenção do ruído em suas amostras temporais
ruido = n.fft.ifft(coefs)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('branco.wav', f_a, r)


### 2.51 Ruído rosa
# a cada oitava, perde-se 3dB
fator = 10.**(-3/20.)
alphai = fator**(n.log2(fi[i0:]/f0))

c = n.copy(coefs)
c[i0:] = coefs[i0:]*alphai
# real par, imaginaria impar
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('rosa.wav', f_a, r)


### 2.52 Ruído marrom
# a cada oitava, perde-se 6dB
fator = 10.**(-6/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

# realizando amostras temporais do ruído marrom
ruido = n.fft.ifft(c)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('marrom.wav', f_a, r)

ruido_marrom=n.copy(r) # será usado para a reverberação


### 2.53 Ruído azul
# para cada oitava, ganhamos 3dB
fator = 10.**(3/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

# realizando amostras temporais do ruído azul
ruido = n.fft.ifft(c)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('azul.wav', f_a, r)


### 2.54 Ruido violeta
# a cada oitava, ganhamos 6dB
fator = 10.**(6/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('violeta.wav', f_a, r)

### 2.55 Ruído preto
# a cada oitava, perdemos mais que 6dB
fator = 10.**(-12/20.)
alphai = fator**(n.log2(fi[i0:]/f0))
c = n.copy(coefs)
c[i0:] = c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:] = n.real(c[1:Lambda/2])[::-1] - 1j * \
    n.imag(c[1:Lambda/2])[::-1]

ruido = n.fft.ifft(c)
r = n.real(ruido)
r = ((r-r.min())/(r.max()-r.min()))*2-1
w.write('preto.wav', f_a, r)


############## 2.2.5 Tremolo e vibrato, AM e FM
# VEJA: vibrato.py e tremolo.py para as figuras 2.19 e 2.20
f = 220.
Lv = 2048  # tamanho da tabela do vibrato
fv = 1.5  # frequência do vibrato
nu = 1.6  # desvio maximo em semitons do vibrato (profundidade)
Delta = 5.2  # duração do som
Lambda = int(Delta*f_a)

# tabela do vibrato
x = n.linspace(0, 2*n.pi, Lv, endpoint=False)
tabv = n.sin(x)  # o vibrato será senoidal

ii = n.arange(Lambda)  # índices
### 2.56 índices da LUT para o vibrato
Gammav_i = n.array(ii*fv*float(Lv)/f_a, n.int)  # índices para a LUT
### 2.57 padrão de oscilação do vibrato para cada amostra
Tv_i = tabv[Gammav_i % Lv]
### 2.58 frequência em cada amostra
F_i = f*(2.**(Tv_i*nu/12.))
### 2.59 índices para LUT do som
D_gamma_i = F_i*(Lt/float(f_a))  # movimentação na tabela por amostra
Gamma_i = n.cumsum(D_gamma_i)  # a movimentação na tabela total
Gamma_i = n.array(Gamma_i, dtype=n.int)  # já os índices
### 2.60 som em si
T_i = Tr_i[Gamma_i % Lt]  # busca dos índices na tabela

w.write("vibrato.wav", f_a, T_i)  # escrita do som


Tt_i = n.copy(Tv_i)
### 2.61 Envoltória do tremolo
V_dB = 12.  # decibels envolvidos na variação
A_i = 10**((V_dB/20)*Tt_i)
### 2.62 Aplicação na sequência T_i
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
T_i = Tr_i[Gamma_i % Lt]
T_i = T_i*A_i
w.write("tremolo.wav", f_a, T_i)  # escrita do som


### 2.63 - Espectro da FM, implementada em 2.66-70
### 2.64 - Função de Bessel, foge ao escopo
### 2.65 - Espectro da AM, implementada em 2.70,71 abaixo

fv = 60.  # > 20Hz
### 2.66 índices para a LUT da moduladora da FM
Gammav_i = n.array(ii*fv*float(Lv)/f_a, n.int)
### 2.67 padrão de oscilação da moduladora
Tfm_i = tabv[Gammav_i % Lv]
f = 330.
mu = 40.
### 2.68 Frequência em cada amostra na FM
f_i = f+Tfm_i*mu
### 2.69 índices da LUT para síntese do som
D_gamma_i = f_i*(Lt/float(f_a))  # movimentação na tabela por amostra
Gamma_i = n.cumsum(D_gamma_i)  # a movimentação na tabela total
Gamma_i = n.array(Gamma_i, dtype=n.int)  # já os índices
### 2.70 FM
T_i = S_i[Gamma_i % Lt]  # busca dos índices na tabela

w.write("fm.wav", f_a, T_i)  # escrita do som


Tam_i = n.copy(Tfm_i)
V_dB = 12.
alpha = 10**(V_dB/20.)  # profundidade da AM
### 2.71 Envoltória para AM
A_i = 1+alpha*Tam_i
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
### 2.70 AM
T_i = Tr_i[Gamma_i % Lt]*(A_i)
w.write("am.wav", f_a, T_i)  # escrita do som


############## 2.2.5 Usos musicais
### 2.73 Veja peça Tremolos, Vibratos e a Frequência

### Efeito Doppler
v_r= 10 # receptor se move em direção à fonte com v_r m/s
v_s=-80. # emissor se move em direção ao receptor com -v_s m/s
v_som=343.2
f_0=1000 # frequencia do emissor
# frequência com o efeito Doppler:
### 2.74 Frequência por efeito Doppler
f=((v_som + v_r) / (v_som + v_s)) * f_0
# a partir do cruzamento entre o emissor e o receptor:
f_=((v_som - v_r) / (v_som - v_s)) * f_0

# distâncias iniciais:
x_0=0 # emissor à frente
y_0=200 # distante y_0 metros

Delta=5. # duração em segundos
Lambda=Delta*f_a # número de amostras
# posições ao longo do tempo, X_i=n.zeros(Lambda)
Y_i=y_0 - ((v_r-v_s)*Delta) * n.linspace(0,1,Lambda)

# A cada amostra, é preciso calcular a DTI e a DII com X_i e Y_i
# No caso, DTI e DII são == 0 pois a fonte está no meio.
### 2.75 Amplitude relativa ao efeito Doppler
# Assumindo z_0 metros acima da cabeça:
z_0=2.
D_i=( z_0**2+Y_i**2  )**0.5 # distância a cada amostra
# Amplitude relativa do som em cada amostra devido à distância:
A_i_=z_0/D_i 
### Alteração da amplitude devido ao efeito Doppler:
A_DP_i=( (v_r-v_s)/343.2+1 )**0.5
A_DP_i_=( (-v_r+v_s)/343.2+1 )**0.5
A_DP_i=(Y_i>0)*A_DP_i+(Y_i<0)*A_DP_i_
A_i=A_i_ * A_DP_i

# Os sinais das velocidades se invertem
# no caso da fonte passar o receptor.
# Portanto:
### 2.76 Progressão de frequência do efeito Doppler
coseno_i=(Y_i)/((Y_i**2+z_0**2)**0.5)
F_i=( ( 343.2+v_r*coseno_i ) / ( 343.2+v_s*coseno_i ) )*f_0
# coeficientes para a LUT
D_gamma_i = F_i*Lt/f_a
Gamma_i = n.cumsum(D_gamma_i)
Gamma_i = n.array(Gamma_i, dtype=n.int)

L_i = Tr_i  # Onda triangular
# Som:
Tdoppler_i = L_i[Gamma_i % Lt]
Tdoppler_i*=A_i

# Normalizando e gravando:
Tdoppler_i=((Tdoppler_i-Tdoppler_i.min()) / \
            (Tdoppler_i.max()-Tdoppler_i.min()))*2.-1
w.write('doopler.wav', f_a, Tdoppler_i)


######## Reverberação
# O primeiro período da reverberação:
Delta1 = 0.15 # tipicamente E [0.1,0.2]
Lambda1= int(Delta1*f_a)
Delta = 1.9 # duração total da reverberação
Lambda=int(Delta*f_a)

# Probabilidades de reincidência do som no primeiro período:
ii=n.arange(Lambda)
P_i = (ii[:Lambda1]/float(Lambda1))**2.
# incidências:
R1_i_=n.random.random(Lambda1)<P_i
A_i=10.**((-50./20)*(ii/Lambda))
### 2.77 - Primeiro período da reverberação:
R1_i=R1_i_*A_i[:Lambda1]*ruido_marrom[:Lambda1] # Primeiras incidências

# Ruído marrom em decaimento exponencial para o segundo período:
# -120dB até o final:
### 2.78 - Segundo período da reverberação:
Rm_i=ruido_marrom[Lambda1:Lambda]
R2_i=Rm_i*A_i[Lambda1:Lambda]
### 2.79 - Resposta ao impulso da reverberação
R_i=n.hstack((R1_i,R2_i))
R_i[0]=1. # resposta ao impulso está pronta

# Realização de um som para aplicar a reverberação:
f_0 = 100.  # freq inicial em Hz
f_f = 700.  # freq final em Hz
Delta = 2.4  # duração
Lambda = int(f_a*Delta)
ii = n.arange(Lambda)

# (usando 2.36 - variação exponencial)
f_i = f_0*(f_f/f_0)**(ii/(float(Lambda)-1))
# (usando 2.37 coeficientes para a LUT)
D_gamma_i = f_i*Lt/f_a
Gamma_i = n.cumsum(D_gamma_i)
Gamma_i = n.array(Gamma_i, dtype=n.int)
# (usando 2.38 som resultante)
Tf0ff_i = L_i[Gamma_i % Lt]

# Aplicação da reverberação
T_i_=Tf0ff_i
T_i=n.convolve(T_i_,R_i)
T_i=(T_i-T_i.min())/(T_i.max()-T_i.min())
w.write('reverb.wav', f_a, T_i)
w.write('RI_reverb.wav', f_a, R_i)


### 2.80 ADSR - variação linear
Delta = 5.  # duração total em segundos
Delta_A = 0.1  # Ataque
Delta_D = .3  # Decay
Delta_R = .2  # Release
a_S = .1  # nível de sustentação

Lambda = int(f_a*Delta)
Lambda_A = int(f_a*Delta_A)
Lambda_D = int(f_a*Delta_D)
Lambda_R = int(f_a*Delta_R)

# Realização da envoltória ADSR: A_i
ii = n.arange(Lambda_A, dtype=n.float)
A = ii/(Lambda_A-1)
A_i = A
ii = n.arange(Lambda_A, Lambda_D+Lambda_A, dtype=n.float)
D = 1-(1-a_S)*((ii-Lambda_A)/(Lambda_D-1))
A_i = n.hstack((A_i, D))
S = a_S*n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D), dtype=n.float)
A_i = n.hstack((A_i, S))
ii = n.arange(Lambda-Lambda_R, Lambda, dtype=n.float)
R = a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
A_i = n.hstack((A_i, R))

### 2.81 Realização do som com a envoltória
ii = n.arange(Lambda, dtype=n.float)
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
T_i = Tr_i[Gamma_i % Lt]*(A_i)

w.write("adsr.wav", f_a, T_i)  # escrita do som em disco


### 2.80 ADSR - variação Exponencial
xi = 1e-2  # -180dB para iniciar o fade in e finalizar o fade out
De = 2*100.  # duracao total (\Delta)
DA = 2*20.  # duracao do ataque \Delta_A
DD = 2*20.  # duracao do decay \Delta_D
DR = 2*20.  # duracao do release \Delta_R
SS = .4  # fração da amplitude em que ocorre o sustain

Lambda = int(f_a*De)
Lambda_A = int(f_a*DA)
Lambda_D = int(f_a*DD)
Lambda_R = int(f_a*DR)

A = xi*(1./xi)**(n.arange(Lambda_A)/(Lambda_A-1))  # amostras do ataque
A_i = n.copy(A)
# amostras do decay
D = a_S**((n.arange(Lambda_A, Lambda_A+Lambda_D)-Lambda_A)/(Lambda_D-1))
A_i = n.hstack((A_i, D))
S = a_S*n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D))  # amostras do sustain
A_i = n.hstack((A_i, S))
R = (SS)*(xi/SS)**((n.arange(Lambda-Lambda_R, Lambda)+Lambda_R-Lambda)/(Lambda_R-1))  # release
A_i = n.hstack((A_i,  R))

### 2.81 Realização do som com a envoltória
ii = n.arange(Lambda, dtype=n.float)
Gamma_i = n.array(ii*f*Lt/f_a, dtype=n.int)
T_i = Tr_i[Gamma_i % Lt]*(A_i)

w.write("adsr_exp.wav", f_a, T_i)  # escrita do som em disco
