import numpy as n
# from scipy.io import wavfile as w
import imp
fun=imp.load_source("functions","../aux/functions.py")

v = fun.V
A = fun.T
def adsr(s, A=10, D=20, S=-20, R=100):
    return fun.AD(A=A, D=D, S=S, R=R, sonic_vector=s)
W = fun.W
H=n.hstack
V=n.vstack

f_a = 44100 # Hz, frequência de amostragem
Lambda_tilde=Lt=1024.

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

T=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)
T_i=n.hstack((n.zeros(f_a),adsr(v(tabv=Tr_i ,d=2.,fv=10.,nu=7.0),10,10,-5.),T))

W(T_i, "ADa_e_SaRa.wav")


############
T=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)
T1=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,10,-10.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,5,-10.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=1.,nu=0.),2,10,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr(v(tabv=Tr_i ,d=2.,fv=3.,  nu=3.),10,10,-10.)
T1=adsr(v(tabv=Tr_i ,d=2.,fv=1., nu=3.),5,10,-10.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=6., nu=3.),5,5,-10.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.),2,10,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))

W(T_i, "ADa_e_SaRa2.wav")


############
T= adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),10,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,10,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),5,5,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),2,10,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),10,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.),5,10,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.),5,5,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.),2,10,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))

W(T_i, "ADa_e_SaRa3.wav")


############
T= adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),2.,10,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),1.,10.,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),0.5, 5.,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1.,nu=0.),0.2,10.,-10.)

T_i=n.hstack((n.zeros(f_a),T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  5.,-10.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  2,-10.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1.,-10.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,0.5,-10.)

T_i=n.hstack((T_i,T,T1,T2,T3))

W(T_i, "ADa_e_SaRa4.wav")


##########
T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  5.,-10,1000.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  2,-5,500.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1.,-20,200.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,0.5,-30,1500.)

T_i=n.hstack((T,T1,T2,T3))

T=adsr( v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=3.,  nu=3.),2,  50.,-10,1000.)
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=1., nu=3.) ,1,  200,-2,500.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,0.5,1000.,-15,200.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,0.2,300.,-25,1500.)

T_i=n.hstack((T_i,T,T1,T2,T3))

W(T_i, "ADa_e_SaRa5.wav")


###########
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)

T_i=n.hstack((n.zeros(f_a),T1,T2,T3,T4))

W(T_i, "ADa_e_SaRa6.wav")


##################
T1=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tab=Tr_i,tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)

T_i=n.hstack((n.zeros(f_a),T1,T2,T3,T4))

T1=adsr(v(tabv=Tr_i ,d=2.,fv=6., nu=3.) ,1.,1.,-20,200.)
T2=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,5.,5.,-30,1500.)
T3=adsr(v(tabv=Tr_i ,d=2.,fv=16., nu=6.) ,1.,2.,-10,200.)
T4=adsr(v(tabv=Tr_i ,d=2.,fv=19.,nu=3.) ,7.,7.,-30,1500.)

T_i=n.hstack((T_i,T1,T2,T3,T4))

W(T_i, "ADa_e_SaRa7.wav")
