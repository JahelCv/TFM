# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:15:01 2019

@author: Jahel
"""
from threading import Lock, Condition
import time

class AccionesNAO():
    def __init__(self, proxytts, proxysr, proxymem, proxyleds, proxyposture, 
                 proxymotion, proxyautomov, proxyaspeech, parentname):
        self.nombreModuloPadre = parentname
        self.mutex = Lock()
        self.mutBlock = Lock()
        self.mutHablar = Lock()
        self.mutexAcciones = Lock()
        self.cond = Condition()
        
        self.tts = proxytts
        self.asr = proxysr
        self.asr.pause(True)
        self.asr.setLanguage("Spanish")
        self.mem = proxymem
        self.leds = proxyleds
        self.posture = proxyposture
        self.motion = proxymotion
        self.automov = proxyautomov
        self.aspeech = proxyaspeech
        self.configurarGruposLeds()
        # Flags
        self.isWaitingWord = False
        self.isTalking = False
        self.isMoving = False
        self.isThreadBlock = False
        self.exact = -1
        self.palabra = None

    def getThreadBlock(self):
        self.mutBlock.acquire()
        aux = self.isThreadBlock
        self.mutBlock.release()
        return aux
        
    def setThreadBlock(self, b):
        self.mutBlock.acquire()
        self.isThreadBlock= b
        self.mutBlock.release()
        
    def getDCMCycleTime(self):
        return self.mem.getData("DCM/CycleTime")
        
    ########################################################################
    ###################### RECONOCIMIENTO DE VOZ ###########################
    ########################################################################
        
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

    def pararEsperaPalabra(self):
        self.mutex.acquire()
        if self.isWaitingWord:
            self.isWaitingWord = False
            self.palabra = "PARADA_OBLIGADA"
            self.cond.acquire()
            self.cond.notifyAll()
            self.cond.release()
        self.mutex.release()
    
    ########################################################################
    ###################### TEXT TO SPEECH ##################################
    ########################################################################    
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

    ########################################################################
    ###################### MOVIMIENTO ######################################
    ########################################################################    
    def accionMedirGlucosa(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.automov.setExpressiveListeningEnabled(False)
                self.motion.closeHand("LHand")
                self.posture.goToPosture("Stand", 0.9)
                # Movimiento 1 (brazo izquierdo)
                fractionMaxSpeed = 0.15
                names = ["HeadPitch","LShoulderPitch","LElbowRoll",
                         "LShoulderRoll","LElbowYaw","LWristYaw",
                         "RShoulderPitch","RElbowRoll","RElbowYaw"]
                namesstiff = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
                angles = [0.4, 0.5, -1.0, -0.3, 0.3, -1.7, 1.3, 1.5, 0.8]
                self.motion.setStiffnesses(names, namesstiff)
                self.motion.setAngles(names, angles, fractionMaxSpeed)
                self.motion.waitUntilMoveIsFinished()
                self.motion.openHand("LHand")
                self.motion.openHand("RHand")
                self.motion.closeHand("RHand")
                self.motion.waitUntilMoveIsFinished()
                # Cabeza recta
                self.motion.setAngles("HeadPitch", 0.0, fractionMaxSpeed)
                self.posture.goToPosture("Stand", 0.2)
                # Termina
                self.automov.setExpressiveListeningEnabled(True)
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def accionComer(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.automov.setExpressiveListeningEnabled(False)
                self.posture.goToPosture("Stand", 0.5)
                # Movimiento 1
                names = ["HeadPitch","LShoulderPitch","LElbowRoll",
                         "LShoulderRoll","LElbowYaw","RShoulderPitch",
                         "RElbowRoll","RShoulderRoll","RElbowYaw"]
                namesstiff = [0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9, 0.9]
                angles = [0.4, 1.0, -1.54, -0.3, -1.25, 1.0, +1.54, +0.3, +1.25]
                fractionMaxSpeed  = 0.15
                self.motion.setStiffnesses(names,namesstiff)
                self.motion.setAngles(names, angles, fractionMaxSpeed)
                # Cabeza recta
                self.motion.waitUntilMoveIsFinished()
                time.sleep(2)
                self.motion.setAngles("HeadPitch", 0.0, fractionMaxSpeed)
                self.posture.goToPosture("Stand", 0.2)
                # Vuelve a inicio
                self.automov.setExpressiveListeningEnabled(True)
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def accionPinchate(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.automov.setExpressiveListeningEnabled(False)
                self.posture.goToPosture("Stand", 0.9)
                self.motion.openHand("LHand")
                # Movimiento 1
                names = ["HeadPitch","LShoulderPitch","LElbowRoll",
                         "LShoulderRoll","LElbowYaw"]
                namesstiff = [1.0, 1.0, 1.0, 1.0, 1.0]
                angles = [0.4, 1.0, -1.5, -0.3, 0.3]
                fractionMaxSpeed  = 0.18
                self.motion.setStiffnesses(names,namesstiff)
                self.motion.setAngles(names, angles, fractionMaxSpeed)
                self.motion.waitUntilMoveIsFinished()
                self.motion.closeHand("LHand")
                # Movimiento 2
                names = ["RShoulderPitch","RShoulderRoll","RElbowRoll",
                         "RElbowYaw"]
                namesstiff = [1.0, 1.0, 1.0, 1.0]
                angles = [1.7, -0.8, 1.5, 1.0]
                fractionMaxSpeed  = 0.13
                self.motion.setStiffnesses(names,namesstiff)
                self.motion.setAngles(names, angles, fractionMaxSpeed)
                self.motion.waitUntilMoveIsFinished()
                # Movimiento 3
                angles = [1.7, -0.0, 1.5, 1.0]
                self.motion.setAngles(names, angles, fractionMaxSpeed)
                self.motion.waitUntilMoveIsFinished()
                self.motion.openHand("RHand")
                self.motion.closeHand("RHand")
                self.motion.closeHand("LHand")
                time.sleep(1)
                # Cabeza recta
                self.motion.setAngles("HeadPitch", 0.0, fractionMaxSpeed)
                self.posture.goToPosture("Stand", 0.2)
                # Vuelve a inicio
                self.automov.setExpressiveListeningEnabled(True)
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def accionLevantarse(self):
        if self.isMoving or self.isWaitingWord:
            print "AccionesNAO # No se levanta porque self.isMoving = " + str(self.isMoving) + " y self.isWaitingWord = " + str(self.isWaitingWord)
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.posture.goToPosture("Stand", 0.7)
                self.motion.waitUntilMoveIsFinished()
                self.isMoving = False
                self.mutexAcciones.release()
                print "AccionesNAO # Se levanta"
                return True
            except Exception:
                self.isMoving = False
                print "AccionesNAO # EXCEPTION en se levanta"
                self.mutexAcciones.release()
                return False
    
    def accionSentarse(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.posture.goToPosture("Sit", 1.0)
                self.motion.waitUntilMoveIsFinished()
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False

    def accionCorrer(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.automov.setExpressiveListeningEnabled(False)
                self.posture.goToPosture("Stand", 0.2)
                self.motion.moveTo(0,0,1.57)
                self.motion.moveTo(0.35,0.35,1.57)
                self.motion.moveTo(0.35,0.35,1.57)
                self.motion.moveTo(0.35,0.35,1.57)
                self.motion.moveTo(0.35,0.35,1.57)
                self.motion.moveTo(0,0,-1.57)
                self.posture.goToPosture("Stand", 0.2)
                self.automov.setExpressiveListeningEnabled(True)
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def posicionParada(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.posture.goToPosture("Crouch", 0.7)
                self.motion.waitUntilMoveIsFinished()
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False

    def accionSaludo(self, num):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                if num == 1:
                    self.aspeech.say("Hola ^start(animations/Stand/Gestures/Hey_1) encantado de conocerte ^wait(animations/Stand/Gestures/Hey_1)")
                elif num == 2:
                    self.aspeech.say("Hola, ^start(animations/Stand/Gestures/Hey_2) siempre es un placer conocer gente nueva. ^wait(animations/Stand/Gestures/Hey_1)")
                elif num == 3:
                    self.aspeech.say("Hola humano ^start(animations/Stand/Gestures/Hey_3) el robot te saluda ^wait(animations/Stand/Gestures/Hey_1)")
                elif num == 4:
                    self.aspeech.say("Buenas! ^start(animations/Stand/Gestures/Hey_1) espero que estés teniendo un buen día. ^wait(animations/Stand/Gestures/Hey_2)")
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def accionDespedida(self, num):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                if num == 1:
                    self.aspeech.say("Adios. ^start(animations/Stand/Gestures/Hey_6) Espero que nos veamos pronto.^wait(animations/Stand/Gestures/Hey_6)")
                elif num == 2:
                    self.aspeech.say("Nos vemos ^start(animations/Stand/Gestures/Hey_5) ha sido un placer ^wait(animations/Stand/Gestures/Hey_1)")
                elif num == 3:
                    self.aspeech.say("Hasta luego humano ^start(animations/Stand/Gestures/Hey_6) abrígate que luego hará frío. ^wait(animations/Stand/Gestures/Hey_1)")
                elif num == 4:
                    self.aspeech.say("¿Ya te vas? ^start(animations/Stand/Gestures/Hey_4) deberías pensartelo, lo estamos pasando bien. ^wait(animations/Stand/Gestures/Hey_6)")
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False

    def accionQUETALESTAS(self, num):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                if num == 1:
                    self.aspeech.say("Estoy genial, hoy me siento con mucha energía, creo que han cargado mi batería.")
                elif num == 2:
                    self.aspeech.say("Muy bien, ^start(animations/Stand/Gestures/Explain_1) la verdad es que me siento genial.")
                elif num == 3:
                    self.aspeech.say("Estoy muy contento de estar aquí. ^start(animations/Stand/Gestures/Explain_2) Ojalá me invitaran más. ^wait(animations/Stand/Gestures/Explain3)")
                elif num == 4:
                    self.aspeech.say("Muy bien, ^start(animations/Stand/Gestures/Hey_4) aunque me duele un poco la cabeza de tanto ruido.")
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
    
    def accionChocarMano(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.automov.setExpressiveListeningEnabled(False)
                self.posture.goToPosture("Stand", 0.9)
                names = ["LShoulderPitch","LShoulderRoll","LElbowRoll"]
                fractionMaxSpeed  = 0.3
                self.motion.setStiffnesses(names,[1.0, 1.0, 1.0])
                self.motion.openHand("LHand")
                # Movimiento 1
                self.motion.setAngles(names, [0.2 ,1.3 ,-1.5], fractionMaxSpeed)
                self.motion.closeHand("LHand")
                # Movimiento 2
                self.motion.setAngles(names, [0.0 ,0.0 ,-0.1], fractionMaxSpeed)
                self.tts.say("Choca")
                time.sleep(1)
                self.tts.say("BUM")
                self.motion.openHand("LHand")
                # Movimiento 3
                self.motion.setAngles(names, [1.3 ,0.0 ,0.1], fractionMaxSpeed)
                self.tts.say("Ahora somos amigos, recuérdalo.")
                # Termina
                time.sleep(3)
                self.motion.closeHand("LHand")
                self.posture.goToPosture("Stand", 0.2)
                self.automov.setExpressiveListeningEnabled(True)               
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False

    def accionTumbarse(self):
        if self.isMoving or self.isWaitingWord:
            return False
        else:
            try:
                self.mutexAcciones.acquire()
                self.isMoving = True
                self.posture.goToPosture("LyingBack", 0.6)
                self.motion.waitUntilMoveIsFinished()
                self.isMoving = False
                self.mutexAcciones.release()
                return True
            except Exception:
                self.isMoving = False
                self.mutexAcciones.release()
                return False
        
    ########################################################################
    ###################### LUCES ###########################################
    ########################################################################
            
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
    def setRotateEyes(self):
        return self.leds.rotateEyes(0x03FCA9, 1, 3)
            
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