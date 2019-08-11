# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 20:15:01 2019

@author: Jahel
"""
from threading import Lock, Condition
import time

class AccionesNAO():
    def __init__(self):
        self.mutex = Lock()
        self.mutBlock = Lock()
        self.mutHablar = Lock()
        self.mutexAcciones = Lock()
        self.cond = Condition()
        
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
        self.isThreadBlock = b
        self.mutBlock.release()
        
    def getDCMCycleTime(self):
        return True
        
    ########################################################################
    ###################### RECONOCIMIENTO DE VOZ ###########################
    ########################################################################
        
    def esperarPalabra(self, palabraretorno, tiempoespera):
        time.sleep(tiempoespera)
        return (1, 0.95, palabraretorno)
        
    def palabraReconocida(self, p, e):
        self.mutex.acquire()
        print 'AccionesNAO - Palabra reconocida'
        self.mutex.release()

    def pararEsperaPalabra(self):
        self.mutex.acquire()
        print 'AccionesNAO - Parar espera palabra'
        self.mutex.release()
    
    ########################################################################
    ###################### TEXT TO SPEECH ##################################
    ########################################################################    
    def decirFrase(self, frase):
        self.mutHablar.acquire()
        print 'AccionesNAO - DecirFrase: ' + frase
        self.mutHablar.release()

    ########################################################################
    ###################### MOVIMIENTO ######################################
    ########################################################################    
    def accionMedirGlucosa(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - AccionMedirGlucosa IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - AccionMedirGlucosa'
            self.mutexAcciones.release()
    
    def accionComer(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionComer IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionComer'
            self.mutexAcciones.release()
    
    def accionPinchate(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionPinchate IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionPinchate'
            self.mutexAcciones.release()
    
    def accionLevantarse(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionLevantarse IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionLevantarse'
            self.mutexAcciones.release()
    
    def accionSentarse(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionSentarse IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionSentarse'
            self.mutexAcciones.release()

    def accionCorrer(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionCorrer IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionCorrer'
            self.mutexAcciones.release()
    
    def posicionParada(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - posicionParada IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - posicionParada'
            self.mutexAcciones.release()

    def accionSaludo(self, num):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionSaludo IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionSaludo, y dice: '
            if num == 1:
                print 'Hola, encantado de conocerte'
            elif num == 2:
                print 'Hola, siempre es un placer conocer gente nueva.'
            elif num == 3:
                print 'Hola humano, el robot te saluda'
            elif num == 4:
                print 'Buenas!, espero que estés teniendo un buen día.'
            self.mutexAcciones.release()
    
    def accionDespedida(self, num):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionDespedida IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionDespedida, y dice: '
            if num == 1:
                print 'Adios, espero que nos veamos pronto'
            elif num == 2:
                print 'Nos vemos, ha sido un placer.'
            elif num == 3:
                print 'Hasta luego humano, abrígate que luego hará frío'
            elif num == 4:
                print '¿Ya te vas?, deberías pensartelo, lo estamos pasando bien'
            self.mutexAcciones.release()
        
    def accionQUETALESTAS(self, num):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionQUETALESTAS IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionQUETALESTAS, y dice: '
            if num == 1:
                print 'Estoy genial, hoy me siento con mucha energía, creo que han cargado mi batería.'
            elif num == 2:
                print 'Muy bien, la verdad es que me siento genial.'
            elif num == 3:
                print 'Estoy muy contento de estar aquí, ojalá me invitaran más.'
            elif num == 4:
                print 'Muy bien, aunque me duele un poco la cabeza de tanto ruido'
            self.mutexAcciones.release()
        
    def accionChocarMano(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionChocarMano IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionChocarMano'
            self.mutexAcciones.release()
            return True

    def accionTumbarse(self):
        if self.isMoving or self.isWaitingWord:
            print 'AccionesNAO - accionTumbarse IS MOVING OR WAITING WORD'
            return False
        else:
            self.mutexAcciones.acquire()
            print 'AccionesNAO - accionTumbarse'
            self.mutexAcciones.release()
            return True
        
    ########################################################################
    ###################### LUCES ###########################################
    ########################################################################
            
    def setLedsOjosBlue(self, onoff):
        print 'AccionesNAO - setLedsOjosBlue ' + str(onoff)

    def setLedsOjosRed(self, onoff):
        print 'AccionesNAO - setLedsOjosRed ' + str(onoff)
    def setLedsOjosGreen(self, onoff):
        print 'AccionesNAO - setLedsOjosGreen ' + str(onoff)
            
    def configurarGruposLeds(self):
        print 'AccionesNAO - configurarGruposLeds'