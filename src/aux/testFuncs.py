import numpy as n
# from scipy.io import wavfile as w
import imp
fun = imp.load_source("functions","./functions.py")
PV_ = fun.PV_
W = fun.W
for i in dir(fun):
    locals()[i] = eval("fun."+i)

s = PV_(f=[220, 440, 330], d=[[2,3],[2,5,3], [2,5,6,1,.4]], fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]], alpha=[[1, 1] , [1, 1, 1], [1, 1, 1, 1, 1]], tab=[[Tr,Tr], [S,Tr,S], [S,S,S,S,S]], nsamples=0, fs=44100)
W(s, "metavibrato1.wav")

s = PV_(f=[220,440,440,220,440,220], d=[[2,9,4,.5,4],[5],[7,4]], fv=[[6],[2,11]], nu=[[2],[3,3]], alpha=[[1,1,1,1,.3],[1],[1,1]], tab=[[Tr,Tr,Tr,Tr,Tr],[S],[S, S]], nsamples=0, fs=44100)
W(s, "metavibrato2.wav")

s = PV_(f=[220,440,220,440,220,440,220], d=[[2,2,2,2,2]], fv=[], nu=[], alpha=[[1,2.5,.2,10,.1]], tab=[[Tr,Tr,Tr,Tr,Tr]], nsamples=0, fs=44100)
W(s, "metavibrato2.wav")

s = PV_(f=[220,440,220,440,220,440,220], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.1,1]], tab=[[Tr,Tr,Tr,Tr,Tr]], nsamples=0, fs=44100)
W(s, "metavibrato3.wav")

s = PV_(f=[220,440,220,440,220,440,220], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.2,1]], tab=[[S]*6], nsamples=0, fs=44100)
W(s, "metavibrato4.wav")

s = PV_(f=[440,220,440,220,440,220, 440], d=[[2,.1,2,.1,2,.1]], fv=[], nu=[], alpha=[[1,1,5,1,.2,1]], tab=[[Tr]*6], fs=44100)
W(s, "metavibrato5.wav")

s = PV_(f=[220,440], d=[[2]], fv=[], nu=[], alpha=[[1]], tab=[[Tr]], nsamples=0, fs=44100)
W(s, "metavibrato6.wav")
s = D_(f=[220,220], d=[[2],[2]], fv=[], nu=[], alpha=[[1],[1]], x=[-10,10], y=[1,1], method=["lin"], tab=[[Tr]], nsamples=0, fs=44100)
WS(s, "dop2.wav")

s = H( [N(i, j) for i, j in zip([200, 500, 100], [2, 1, 2])] )
# test writing stereo WS()
# test each function
# W_(fn, fs, sa)
stereo = n.vstack((V(), V()*T()))
W(N(f=220, d=2, tab=Tr, nsamples=0, fs=44100), "as35.wav")
W(V(f=220, d=2, fv=4, nu=2, tab=Tr, tabv=S, alpha=1, nsamples=0, fs=44100), "as36.wav")
W(V()*T(d=2, fa=2, dB=10, alpha=1, taba=S, nsamples=0, sonic_vector=0, fs=44100), "as37.wav")
W(V()*AD(d=2, A=20, D=20, S=-5, R=50, trans="exp", alpha=1, dB=-80, to_zero=1, nsamples=0, sonic_vector=0, fs=44100), "as38.wav")
WS(stereo*ADS(d=2, A=20, D=20, S=-5, R=50, trans="exp", alpha=1, dB=-80, to_zero=1, nsamples=0, sonic_vector=0, fs=44100), "as39.wav")
W(V()*L(d=2, dev=10, alpha=1, to=True, method="exp", nsamples=0, sonic_vector=0, fs=44100), "as40.wav")
W(V()*F(d=2, out=True, method="exp", dB=-80, alpha=1, perc=1, nsamples=0, sonic_vector=0, fs=44100), "as41.wav")
W(P(f1=220, f2=440, d=2, alpha=1, tab=S, nsamples=0, fs=44100), "as42.wav")
W(PV(f1=220, f2=440, d=2, fv=4, nu=2, alpha=1, alphav=1, tab=S, tabv=S, nsamples=0, fs=44100), "as43.wav")
W(VV(f=220, d=2, fv1=2, fv2=6, nu1=2, nu2=4, alphav1=1, alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100), "as44.wav")
W(PVV(f1=220, f2=440, d=2, fv1=2, fv2=6, nu1=2, nu2=.5, alpha=1, alphav1=1, alphav2=1, tab=Tr, tabv1=S, tabv2=S, nsamples=0, fs=44100), "as45.wav")
W(PV_(f=[220, 440, 330], d=[[2,3],[2,5,3], [2,5,6,1,.4]], fv=[[2,6,1], [.5,15,2,6,3]], nu=[[2,1, 5], [4,3,7,10,3]], alpha=[[1, 1] , [1, 1, 1], [1, 1, 1, 1, 1]], tab=[[Tr,Tr], [S,Tr,S], [S,S,S,S,S]], nsamples=0, fs=44100), "as46.wav")
W(V(d=8)*L_(d=[2,4,2], dev=[5,-10,20], alpha=[1,.5, 5], method=["exp", "exp", "exp"], nsamples=0, sonic_vector=0, fs=44100), "as47.wav")
W(V(d=16)*T_(d=[[3,4,5],[2,3,7,4]], fa=[[2,6,20],[5,6.2,21,5]], dB=[[10,20,1],[5,7,9,2]], alpha=[[1,1,1],[1,1,1,9]], taba=[[S,S,S],[Tr,Tr,Tr,S]], nsamples=0, sonic_vector=0, fs=44100), "as48.wav")
W(mix([V(f=330), V()*T(),V(f=220*2**(4/12))], end=False, offset=0, fs=44100), "as49.wav")
W(trill(f=[220,330,440], ft=17, d=5, fs=44100), "as50.wav")
W(trill(f=[220*2,220*2*2**(2/12)], ft=17, d=5, fs=44100), "as50_.wav")
W(trill(f=[440,440*2**(2/12)], ft=17, d=5, fs=44100))
