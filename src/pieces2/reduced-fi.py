#! /usr/bin/python

# Rode com:
# ./reduced-fi.py
# ou
# python reduced-fi.py

import math as m
import random as r

def p(freq):
    return 2*m.pi*freq/44100

def d(dur):
    return int(dur*44100)

def s(freq,dur):
    return [m.sin(p(freq)*i) for i in xrange(d(dur))]

ss=(s(100,.1)+s(200,.1)+s(400,.1)+s(800,.1))*4
ss+=(s(100,.1)+s(200,.1)+s(400,.1)+s(800,.1))*4
ss+=(s(200,.05)+s(100,.05)+s(3200,.05)+s(800,.05))*8
ss+=(s(200,.05)+s(100,.05)+s(3200,.05)+s(800,.05))*8

ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(200,.005)+s(100,.005)+s(3200,.005)+s(800,.005))*8
ss+=(s(200,.005)+s(100,.005)+s(3200,.005)+s(800,.005))*8
ss+=s(300,2)

ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(100,.01)+s(200,.01)+s(4000,.01)+s(800,.01))*4
ss+=(s(200,.005)+s(100,.005)+s(6400,.005)+s(800,.005))*8
ss+=(s(200,.005)+s(100,.005)+s(3200,.005)+s(800,.005))*8
ss+=s(300,2)

foo=ss[:int(44100*1)]; r.shuffle(foo); ss+=[i*.1 for i in foo]
ss+=s(300,2)


foo=ss[:int(44100*.5)]; r.shuffle(foo); ss+=[i*.1 for i in foo]
ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(200,.005)+s(100,.005)+s(3200,.005)+s(800,.005))*8
ss+=(s(200,.005)+s(100,.005)+s(3200,.005)+s(800,.005))*8

ss+=(s(100,.01)+s(200,.01)+s(400,.01)+s(800,.01))*4
ss+=(s(100,.01)+s(200,.01)+s(4000,.01)+s(800,.01))*4
ss+=(s(200,.005)+s(100,.005)+s(6400,.005)+s(800,.005))*8
ss+=(s(2000,.005)+s(100,.005)+s(10000,.005)+s(800,.005))*8
ss+=s(300,2)

ss+=(s(50,.1)+s(200,.1)+s(400,.1)+s(800,1))*1
ss+=(s(50,1)+s(200,.1)+s(400,.1)+s(800,.1))*1
ss+=(s(100,.5)+s(100,.05)+s(3200,.05)+s(800,.05))*1
ss+=(s(200,.05)+s(100,.05)+s(3200,.05)+s(400,.5))*1
foo=ss[:int(44100*.25)]; r.shuffle(foo); ss+=[i*.1 for i in foo]

ss+=s(400,.2)
ss+=s(200,.8)
ss+=s(150,.5)
ss+=s(100,1.5)


#############################
seq=ss
#### Gravando em disco
import wave, struct
smin=min(seq); smax=max(seq)
seq= [(-.5+(i-smin)/(smax-smin)) for i in seq] # normalizando
sound = wave.open('musica.wav','w')
sound.setframerate(44100)
sound.setsampwidth(2) # sempre 16bit/sample (2 bytes)
sound.setnchannels(1) # mono
sonic_vector=[i*(2**15-1) for i in seq] # 16 bit com sinal
sound.writeframes(struct.pack('h'*len(sonic_vector),\
                      *[int(i) for i in sonic_vector]))
sound.close()
print "arquivo musica.wav gravado"
