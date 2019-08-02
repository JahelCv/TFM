# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:15:01 2019

@author: Jahel
"""
from threading import Lock, Condition
import time

class AccionesNAO():
    def __init__(self, proxytts, proxysr, proxymem, proxyleds, parentname):
        self.nombreModuloPadre = parentname
        self.mutex = Lock()
        self.mutHablar = Lock()
        self.cond = Condition()
        # TODO: Borrar
        print 'Acciones NAO creado'
        self.tts = proxytts
        self.asr = proxysr
        self.asr.pause(True)
        self.asr.setLanguage("Spanish")
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
        
    def esperarPalabra(self, wordlist, seconds):
        # Se arranca la callback para que recoja self.palabra y self.exactitud
        if not self.isWaitingWord:
            try:
                self.isWaitingWord = True
                self.palabra = None
                self.leds.on("EarLeds")
                self.asr.setVocabulary(wordlist,False)
                self.asr.subscribe(self.nombreModuloPadre)
                self.mem.subscribeToEvent("WordRecognized", self.nombreModuloPadre, "onWordRecognized")
                self.asr.pause(False)
            except Exception:
                self.palabra = None
                self.isWaitingWord = False
        # Esperamos con el condition a que haya una respuesta
        # Si self.palabra = None es porque ha vencido el timeout
        # Si self.palabra != None es porque palabraReconocida ha enviado notifyAll()
        self.cond.acquire()
        self.cond.wait(seconds)
        self.cond.release()
        if self.palabra != None:
            if self.palabra == "PARADA_OBLIGADA":
                self.isWaitingWord = False
                self.leds.off("EarLeds")
                self.asr.pause(True)
                self.mem.unsubscribeToEvent("WordRecognized", self.nombreModuloPadre)
                self.asr.unsubscribe(self.nombreModuloPadre)
                return (-1, None, None)
        else:
            self.isWaitingWord = False
            self.leds.off("EarLeds")
            self.asr.pause(True)
            self.mem.unsubscribeToEvent("WordRecognized", self.nombreModuloPadre)
            self.asr.unsubscribe(self.nombreModuloPadre)
            return (-1, None, None)
        
        self.isWaitingWord = False
        self.leds.off("EarLeds")
        self.asr.pause(True)
        self.mem.unsubscribeToEvent("WordRecognized", self.nombreModuloPadre)
        self.asr.unsubscribe(self.nombreModuloPadre)
        return (1, self.exact, self.palabra)
        
    def palabraReconocida(self, p, e):
        self.mutex.acquire()
        if self.isWaitingWord and (not self.isTalking):
            self.isWaitingWord = False
            self.exact = e
            self.palabra = p
            print 'Palabra reconocida: ' + str(self.palabra)
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