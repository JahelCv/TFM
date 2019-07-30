# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:15:01 2019

@author: Jahel
"""
from threading import Lock, Condition

class AccionesNAO():
    def __init__(self, proxytts, proxysr, proxymem, proxyleds):
        self.mutex = Lock()
        self.mutHablar = Lock()
        self.cond = Condition()
        # TODO: Borrar
        print 'Acciones NAO creado'
        self.tts = proxytts
        self.sr = proxysr
        self.mem = proxymem
        self.leds = proxyleds
        self.configurarGruposLeds()
        # Flags
        self.isWaitingWord = False
        self.isTalking = False
        self.isMoving = False
        self.isThreadBlock = False
        self.exact = -1
        self.palabra = None
        
    def palabraReconocida(self, p, e):
        self.mutex.acquire()
        if self.isWaitingWord and (not self.isTalking):
            self.isWaitingWord = False
            self.exact = e
            self.palabra = self.palabra + p
            print 'Palabra reconocida: ' + self.palabra
            self.cond.acquire()
            self.cond.notifyAll()
            self.cond.release()
        self.mutex.release()
        
    def decirFrase(self, frase):
        try:
            self.mutHablar.acquire()
            self.isTalking = True
            self.tts.say(frase)
            self.isTalking = False
            self.mutHablar.release()
            return True
        except Exception as e:
            print 'Exception en decirFrase: ' + str(e)
            self.mutHablar.release()
            
    def setLedsOjosBlue(self, onoff):
        if onoff:
            self.leds.on("LedsOjosAzul")
        else:
            self.leds.off("LedsOjosAzul")

    def setLedsOjosRed(self, onoff):
        if onoff:
            self.leds.on("LedsOjosRojo")
        else:
            self.leds.off("LedsOjosRojo")

    def setLedsOjosGreen(self, onoff):
        if onoff:
            self.leds.on("LedsOjosVerde")
        else:
            self.leds.off("LedsOjosVerde")
            
    def configurarGruposLeds(self):
        names1 = [
        "Face/Led/Red/Left/0Deg/Actuator/Value",
        "Face/Led/Red/Left/45Deg/Actuator/Value",
        "Face/Led/Red/Left/90Deg/Actuator/Value",
        "Face/Led/Red/Left/135Deg/Actuator/Value",
        "Face/Led/Red/Left/180Deg/Actuator/Value",
        "Face/Led/Red/Left/225Deg/Actuator/Value",
        "Face/Led/Red/Left/270Deg/Actuator/Value",
        "Face/Led/Red/Left/315Deg/Actuator/Value",
        "Face/Led/Red/Right/0Deg/Actuator/Value",
        "Face/Led/Red/Right/45Deg/Actuator/Value",
        "Face/Led/Red/Right/90Deg/Actuator/Value",
        "Face/Led/Red/Right/135Deg/Actuator/Value",
        "Face/Led/Red/Right/180Deg/Actuator/Value",
        "Face/Led/Red/Right/225Deg/Actuator/Value",
        "Face/Led/Red/Right/270Deg/Actuator/Value",
        "Face/Led/Red/Right/315Deg/Actuator/Value"]
        self.leds.createGroup("LedsOjosRojo",names1)

        names2 = [
        "Face/Led/Blue/Left/0Deg/Actuator/Value",
        "Face/Led/Blue/Left/45Deg/Actuator/Value",
        "Face/Led/Blue/Left/90Deg/Actuator/Value",
        "Face/Led/Blue/Left/135Deg/Actuator/Value",
        "Face/Led/Blue/Left/180Deg/Actuator/Value",
        "Face/Led/Blue/Left/225Deg/Actuator/Value",
        "Face/Led/Blue/Left/270Deg/Actuator/Value",
        "Face/Led/Blue/Left/315Deg/Actuator/Value",
        "Face/Led/Blue/Right/0Deg/Actuator/Value",
        "Face/Led/Blue/Right/45Deg/Actuator/Value",
        "Face/Led/Blue/Right/90Deg/Actuator/Value",
        "Face/Led/Blue/Right/135Deg/Actuator/Value",
        "Face/Led/Blue/Right/180Deg/Actuator/Value",
        "Face/Led/Blue/Right/225Deg/Actuator/Value",
        "Face/Led/Blue/Right/270Deg/Actuator/Value",
        "Face/Led/Blue/Right/315Deg/Actuator/Value"]
        self.leds.createGroup("LedsOjosAzul",names2)

        names3 = [
        "Face/Led/Green/Left/0Deg/Actuator/Value",
        "Face/Led/Green/Left/45Deg/Actuator/Value",
        "Face/Led/Green/Left/90Deg/Actuator/Value",
        "Face/Led/Green/Left/135Deg/Actuator/Value",
        "Face/Led/Green/Left/180Deg/Actuator/Value",
        "Face/Led/Green/Left/225Deg/Actuator/Value",
        "Face/Led/Green/Left/270Deg/Actuator/Value",
        "Face/Led/Green/Left/315Deg/Actuator/Value",
        "Face/Led/Green/Right/0Deg/Actuator/Value",
        "Face/Led/Green/Right/45Deg/Actuator/Value",
        "Face/Led/Green/Right/90Deg/Actuator/Value",
        "Face/Led/Green/Right/135Deg/Actuator/Value",
        "Face/Led/Green/Right/180Deg/Actuator/Value",
        "Face/Led/Green/Right/225Deg/Actuator/Value",
        "Face/Led/Green/Right/270Deg/Actuator/Value",
        "Face/Led/Green/Right/315Deg/Actuator/Value"]
        self.leds.createGroup("LedsOjosVerde",names3)