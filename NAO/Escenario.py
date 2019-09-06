# -*- coding: utf-8 -*-
from DatosCompartidos import DatosCompartidos
from AccionesNAO import AccionesNAO
from SimuladorRemoto import SimuladorRemoto
from collections import deque
import time
import random
from threading import Thread

class Escenario(object):
    def __init__(self, d, ac, r, mqtt): 
        self.dmqtt = mqtt
        self.pausa = False
        self.glucosa = deque((-1, -1, -1, -1, -1))
        self.exactitud = 0.3
        self.tiempoUltimaPeticionSimu = time.time()
        self.contador = 1
        self.datos = d
        self.acNAO = ac
        self.simremoto = r
        self.respEspera = 1
        self.palabraRec = ""
    
    def setDatosCompartidos(self, d):
        self.datos = d
        
    def setAccionesNAO(self, ac):
        self.acNAO = ac
        
    def setSimuladorRemoto(self, r):
        self.simremoto = r
        
    def pararThread(self):
        self.pararLoop = False
        self.acNAO.pararEsperaPalabra()
        self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,PARADO")
        
    def startThread(self):
        hilo = Thread(target=self.run)
        hilo.start()
        self.dmqtt.publicaInterfazHilosMQTT("ESCENARIO,CORRIENDO")
    
    def pausar(self):
        print 'En ESCENARIO el metodo PAUSAR No hace nada'
        
    def desPausar(self):
        print 'En ESCENARIO el metodo DESPAUSAR No hace nada'
            
    def mirarGlucosa(self):
        glucosaAux = self.simremoto.getGlucosaRemoto()
        glucosastr = '%.2f'%(glucosaAux)
        self.glucosa.appendleft(glucosaAux)
        self.glucosa.pop()
        return glucosastr
        
    def actualizarContador(self):
        self.contador = self.contador + 1
        if self.contador == 5:
            self.contador = 1
    
    def getWordlistFase2(self):
        return ['vamos a hacer deporte', 'tienes hambre', 'avanza', 
                'dime tu glucosa']
        
    def getWordlistFase3(self):
        if self.estado == 1 or self.estado == 3:
            return ['hola','adios','como te llamas','que tal estás','sientate',
                    'levantate','choca el puño','salta','tumbate','toma un zumo',
                    'come un bocata','come una pizza','haz deporte',
                    'dime tu glucosa']
        elif self.estado == 2:
            return ['si','no','dime tu glucosa','hola','adios','como te llamas','que tal estás','sientate',
                    'levantate','choca el puño','salta','tumbate','toma un zumo',
                    'come un bocata','come una pizza','haz deporte']
#        elif self.estado == 3:
#            return ['hola','adios','como te llamas','que tal estás','sientate',
#                    'levantate','choca el puño','salta','tumbate','toma un zumo',
#                    'come un bocata','come una pizza','haz deporte','dime tu glucosa']
        return []
        
    def fase3(self):
        cho = 0
        bolus = 0
        probability = random.randint(0,10)
        self.dmqtt.publicaVentanaEscenarioMQTT("##### Principio del bucle ##### \nFase: 3 \nEstado: " 
            + str(self.estado) + " \nNumero random: " +str(self.numerorandom)
            + "\nPalabra recibida: " + str(self.palabraRec) + " \nPalabra anterior: "
            + str(self.ultimaPalabra) + " \nContador: " + str(self.contador))
        
        ################################################
        #### COMPROBACION DE GLUCOSA ###################
        ################################################
        
        # Se encuentra bien
        if self.glucosa[0] > 70 and self.glucosa[0] < 140:
            self.acNAO.setLedsOjosBlue(False)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            self.acNAO.decirFrase('Me encuentro perfectamente')
            if (time.time() - self.tiempoUltimaPeticionSimu) < 45:
                if self.iniFase3:
                    self.iniFase3 = False
                    self.estado = 1
                else:
                    if self.estadoprevio == 1:
                        self.estado = 1
                    else:
                        self.estado = 3
            else:
                self.estado = 1
                
        # Glucosa baja, se encuentra mal
        elif self.glucosa[0] < 70:
            self.acNAO.setLedsOjosBlue(True)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            self.acNAO.decirFrase('Mi glucosa es baja')
            
            # En C++ esto era un switch
            if self.estado == 1:
                pass
            elif self.estado == 2:
                self.acNAO.accionMedirGlucosa();
                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                if self.numerorandom == 1:
                    self.acNAO.decirFrase('El medico me recomienda tomarme un sobre de gel de 15 gramos, ¿crees que es la mejor opción?')
                    self.estado = 2
                elif self.numerorandom == 2: 
                    self.acNAO.decirFrase('El medico me recomienda que me pinche más insulina, ¿tú crees que es correcto?')
                    self.estado = 2
            elif self.estado == 3:
                self.acNAO.decirFrase('Ahora debo esperar a que lo que me he hecho haga efecto en mi.')
                if (time.time() - self.tiempoUltimaPeticionSimu) > 60:
                    # Glucosa sube
                    if self.glucosa[0] > self.glucosa[3]:
                        self.acNAO.decirFrase('Mi glucosa está subiendo, aunque sigue siendo baja. Debo esperar un ratito más.')
                    # Glucosa baja
                    elif self.glucosa[0] < self.glucosa[3]:
                        self.acNAO.decirFrase('Algo va mal. Mi glucosa es baja y continua bajando. Debo tomar medidas.')
                        self.estado = 1
                        
        # Glucosa alta, pero no mucho
        elif self.glucosa[0] > 140 and self.glucosa[0] < 180:
            self.acNAO.setLedsOjosBlue(False);
            self.acNAO.setLedsOjosGreen(True);
            self.acNAO.setLedsOjosRed(True);
            self.acNAO.decirFrase('Mi glucosa es alta.')
            
            if self.estado == 1:
                self.acNAO.accionMedirGlucosa();
                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                if self.numerorandom == 1:
                    self.acNAO.decirFrase('El medico me recomienda que me pinche insulina, ¿crees que es la mejor opción?')
                    self.estado = 2
                elif self.numerorandom == 2: 
                    self.acNAO.decirFrase('El medico me recomienda comerme un bocata, ¿crees que es la mejor opción?')
                    self.estado = 2
            elif self.estado == 3:
                self.acNAO.decirFrase('Ahora debo esperar a que lo que me he hecho haga efecto en mi.')
                if (time.time() - self.tiempoUltimaPeticionSimu) > 60:
                    # Glucosa sube
                    if self.glucosa[0] > self.glucosa[3]:
                        self.acNAO.decirFrase('Algo va mal. Mi glucosa es alta y continua subiendo. Debo tomar medidas.')
                        self.estado = 1
                    # Glucosa baja
                    elif self.glucosa[0] < self.glucosa[3]:
                        self.acNAO.decirFrase('Mi glucosa está bajando, aunque sigue siendo alta. Debo esperar un ratito más.')
                        
        # Glucosa MUY alta
        elif self.glucosa[0] > 180:
            self.acNAO.setLedsOjosBlue(False);
            self.acNAO.setLedsOjosGreen(True);
            self.acNAO.setLedsOjosRed(True);
            self.acNAO.decirFrase('Tengo la glucosa peligrosamente alta.')
            
            # Si ha pasado mas de 50 segundos desde la ultima actu...
            if (time.time() - self.tiempoUltimaPeticionSimu) > 45:
                # Y la insulina sigue creciendo...                
                if self.glucosa[0] > self.glucosa[2]:
                    self.acNAO.accionMedirGlucosa();
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Como es muy alta después de una hora desde que comí y además está subiendo voy a inyectarme insulina urgentemente.')
                    self.acNAO.accionPinchate()
                    self.estado = 3
                    cho = 0
                    # bolo prandial = ratio_insulina_carbohidratos * gramos de carbohidratos + factor de corrección*(glucemia actual - glucemia objetivo) - insulina a bordo
                    bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0
                    self.simremoto.enviaDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time.time()
                else:
                    self.acNAO.accionMedirGlucosa();
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Es muy alta pero como está disminuyendo voy a esperar un poco.')
                    self.estado = 3
            # Si han pasado menos de 50 segundos desde la ultima actu...
            else:
                self.acNAO.accionMedirGlucosa();
                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                self.acNAO.decirFrase('Es muy alta pero como acabo de intentar modificarla voy a esperar un ratito.')    
                
        self.estadoprevio = self.estado
		
        ################################################
        #### ESPERAMOS RESPUESTA DE PERSONA ############
        ################################################
        if self.respEspera == 1:
            self.ultimaPalabra == self.palabraRec
        (self.respEspera,exac,self.palabraRec) = self.acNAO.esperarPalabra(self.getWordlistFase3(),15)
        self.dmqtt.publicaVentanaEscenarioMQTT("##### Despues de esperarPalabra ##### \nFase: 3 \nEstado: " 
            + str(self.estado) + "\nNumero random: " +str(self.numerorandom)
            + "\nPalabra recibida: " + str(self.palabraRec) + " \nPalabra anterior: "
            + str(self.ultimaPalabra) + " \nContador: " + str(self.contador))
        
        # Interpretamos respuesta, que si es correcta actuamos
        if self.respEspera == -1 or self.respEspera == -2:
            pass
        elif self.respEspera == 1:
            # Acciones segun el estado en que estemos: 1,2,3
            # Case estado = 1
            if self.estado == 1:
                # Se mira que palabra (orden) se ha recibido
                if self.palabraRec == 'hola':
                    self.acNAO.accionSaludo(self.contador)
                    self.actualizarContador()
                    self.ultimaPalabra = 'hola'
                    
                if self.palabraRec == 'adios':
                    self.acNAO.accionDespedida(self.contador)
                    self.actualizarContador()
                    self.ultimaPalabra = 'adios'
                    
                if self.palabraRec == 'como te llamas':
                    self.acNAO.decirFrase('Mi nombre es Andy, y soy el robot humanoide con diabetes del instituto aídos de la Universidad Politécnica de Valencia.')
                    self.ultimaPalabra = 'como te llamas'
                    time.sleep(1)
                    
                if self.palabraRec == 'que tal estas':
                    self.acNAO.accionQUETALESTAS(self.contador);
                    self.actualizarContador()
                    self.ultimaPalabra = 'que tal estas'
                    
                if self.palabraRec == 'sientate':
                    if self.ultimaPalabra == 'sientate':
                        self.acNAO.decirFrase('Pero si ya estoy sentado...')
                    else:
                        if self.contador == 1:
                            self.acNAO.decirFrase('Hora de descansar un rato. ¿Listos?')
                        elif self.contador == 2:
                            self.acNAO.decirFrase('Otra vez me estás haciendo hacer deporte.')
                        elif self.contador == 3:
                            self.acNAO.decirFrase('Me dispongo a tomar asiento. Allá voy.')
                        elif self.contador == 4:
                            self.acNAO.decirFrase('Me sentaré en el suelo porque veo que no me habéis traido una silla.')
                    
                    self.actualizarContador()
                    #self.acNAO.accionSentarse()
                    self.ultimaPostura = 'sientate'
                    time.sleep(1)
                    
                if self.palabraRec == 'levantate':
                    if self.ultimaPostura == 'sientate':
                        self.acNAO.decirFrase('Pero si me acabo de sentar...')
                        self.acNAO.accionLevantarse()
                        self.ultimaPostura = 'levantate'
                        time.sleep(1)
                    elif self.ultimaPostura == 'tumbate':
                        self.acNAO.decirFrase('Con lo bien que estoy aquí tumbado...')
                        self.acNAO.accionLevantarse()
                        self.ultimaPostura = 'levantate'
                        time.sleep(1)
                    else:
                        self.acNAO.decirFrase('Pero si ya estoy en pie...')
                        
                if self.palabraRec == 'choca el puño':
                    self.acNAO.decirFrase('Choca ese puño colega.')
                    self.acNAO.accionChocarMano()
                    self.ultimaPalabra = 'choca el puño'
                    
                if self.palabraRec == 'salta':
                    if self.ultimaPalabra == 'salta':
                        self.acNAO.decirFrase('Estás pesadíto con el tema...')
                    else:
                        self.acNAO.decirFrase('¿Estás loco? Si salto seguro que me hago daño, mejor en otra ocasión.')
                        self.ultimaPalabra = 'salta'
                        
                if self.palabraRec == 'tumbate':
                    if self.ultimaPalabra == 'tumbate':
                        self.acNAO.decirFrase('Pero si ya estoy tumbado...')
                    else:
                        if self.contador == 1:
                            self.acNAO.decirFrase('Me voy a la cama que hay que descansar.')
                        elif self.contador == 2:
                            self.acNAO.decirFrase('Voy a tumbarme un ratito.')
                        elif self.contador == 3:
                            self.acNAO.decirFrase('Ya era hora de un descanso.')
                        elif self.contador == 4:
                            self.acNAO.decirFrase('Solo me falta una cama.')
                        #self.acNAO.accionTumbarse()
                        self.actualizarContador()
                    
                    self.ultimaPostura = 'tumbate'
                    self.acNAO.decirFrase('Despiertame dentro de 5 minutitos.')
                    
                if self.palabraRec == 'toma un zumo':
                    self.acNAO.decirFrase('Primero voy a medir mi glucosa.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo es de valor ' + str(self.mirarGlucosa()))
                    if self.numerorandom == 1:
                        cho = 30
                        bolus = 0
                        self.acNAO.decirFrase('No voy a pincharme insulina porque no me apetece. Voy a tomarme el zumo.')
                        self.acNAO.accionComer()
                    elif self.numerorandom == 2:
                        cho = 30
                        bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0;
                        bolus = round(bolus*1000)/1000
                        bolus = round(bolus*2)/2
                        self.acNAO.decirFrase('Antes de comer debo inyectarme insulina. Como voy a comer poco me inyectaré una cantidad de ')
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina')
                        self.acNAO.accionPinchate()
                        self.acNAO.decirFrase('Ahora voy a tomarme un zumo.')
                        self.acNAO.accionComer()
                        
                    self.estado = 3
                    self.simremoto.enviaDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time.time()
                    
                if self.palabraRec == 'come un bocata':
                    self.acNAO.decirFrase('Primero voy a medir mi glucosa.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo es de valor ' + str(self.mirarGlucosa()))
                    if self.numerorandom == 1:
                        cho = 60
                        bolus = 0
                        self.acNAO.decirFrase('No voy a pincharme insulina porque no me apetece. Voy a tomarme el bocata.')
                        self.acNAO.accionComer()
                    elif self.numerorandom == 2:
                        cho = 30
                        bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0;
                        bolus = round(bolus*1000)/1000
                        bolus = round(bolus*2)/2
                        self.acNAO.decirFrase('Antes de comer debo inyectarme insulina. Como voy a comer un bocata me inyectaré una cantidad de ')
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina')
                        self.acNAO.accionPinchate()
                        self.acNAO.decirFrase('Ahora voy a comerme mi estupendo bocata.')
                        self.acNAO.accionComer()
                        
                    self.estado = 3
                    self.simremoto.enviaDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time.time()
                    
                if self.palabraRec == 'come una pizza':
                    self.acNAO.decirFrase('Primero voy a medir mi glucosa.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo es de valor ' + str(self.mirarGlucosa()))
                    if self.numerorandom == 1:
                        cho = 90
                        bolus = 0
                        self.acNAO.decirFrase('No voy a pincharme insulina porque no me apetece. Voy a comerme la pizza que me muero de hambre.')
                        self.acNAO.accionComer()
                    elif self.numerorandom == 2:
                        cho = 30
                        bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0;
                        bolus = round(bolus*1000)/1000
                        bolus = round(bolus*2)/2
                        self.acNAO.decirFrase('Antes de comer debo inyectarme insulina. Como me voy a comer una pizza enorme me inyectaré una cantidad de ')
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina')
                        self.acNAO.accionPinchate()
                        self.acNAO.decirFrase('Ahora voy a comerme la pizza que si no se me enfría.')
                        self.acNAO.accionComer()
                        
                    self.estado = 3
                    self.simremoto.enviaDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time.time()
                    
                if self.palabraRec == 'haz deporte':
                    self.acNAO.decirFrase('Primero voy a medir mi glucosa.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo es de valor ' + str(self.mirarGlucosa()))
                    bolus = 0
                    # Si glucosa baja                    
                    if self.glucosa[0] < 150:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Como mi glucosa es menor de 150 voy a comerme un snack para compensar la bajada de glucosa del ejercicio.')
                            cho = 30
                            self.acNAO.accionComer()
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Como mi glucosa es menor de 150 debería a comerme un snack para compensar la bajada de glucosa del ejercicio, pero como estoy fuera de casa voy a hacer deporte sin comer nada.')
                            cho = 0                                
                    # Si glucosa alta                    
                    elif self.glucosa[0] >= 150:
                        self.acNAO.decirFrase('Como mi glucosa es mayor de 150 no es necesario que coma nada.')
                        cho = 0
                        
                    self.acNAO.decirFrase('Si quiero hacer ejercicio primero voy reducir mi insulina basal a la mitad durante el ejercicio.')
                    self.acNAO.accionPinchate()
                    self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                    self.estado = 3
                    self.simremoto.enviaDatosSimulacion(bolus,cho,True,0,50,30)
                    self.tiempoUltimaPeticionSimu = time.time()
                    #self.acNAO.accionCorrer()
                    
            # Case estado = 2
            elif self.estado == 2:
                if self.palabraRec == 'si':
                    # Si glucosa baja
                    if self.glucosa[0] < 70:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Es cierto, has acertado.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Meeeec, incorrecto amigo. No debo inyectarme porque mi glucosa bajaría aun más.')
                            
                        self.acNAO.decirFrase('Voy a tomarme un sobre de gel de 15 gramos para subir mi glucosa. No puedo permitir que siga tan baja. Si en un rato sigo igual me tomaré otro.')
                        self.acNAO.accionComer();
                        self.simremoto.enviaDatosSimulacion(0,15,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time.time()
                        self.estado = 3
                        time.sleep(1)
                    # Si glucosa alta
                    elif self.glucosa[0] > 140:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Correcto. Debo hacer algo para bajar mi azucar.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Creo que nos estamos equivocando. No debo comer nada porque mi glucosa subiría aun más.')                            
                        
                        self.acNAO.decirFrase('Voy a inyectarme insulina para bajar mi glucosa. Es lo que realmente debo hacer en estos casos.')
                        self.acNAO.accionPinchate();
                        self.simremoto.enviaDatosSimulacion(1,0,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time.time()
                        self.estado = 3
                    # Si glucosa normal
                    else:
                        self.acNAO.decirFrase('¿De verdad crees que sí?. Lo cierto es que ya me encuentro mejor, creo que mi glucosa se está normalizando.')
                        self.estado = 1
                        
                elif self.palabraRec == 'no':
                    # Si glucosa baja
                    if self.glucosa[0] < 70:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Meeeec, incorrecto amigo. No debo inyectarme porque mi glucosa bajaría aun más.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Es cierto, has acertado. Si ahora me pincho mi glucosa bajaría aun más.')
                        
                        self.acNAO.decirFrase('Voy a comerme un bocata para subir mi glucosa. No puedo permitir que siga tan baja.')
                        self.acNAO.accionComer()
                        self.simremoto.enviaDatosSimulacion(0,50,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time.time()
                        self.estado = 3
                    # Si glucosa alta
                    elif self.glucosa[0] > 140:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Creo que nos estamos equivocando. No debo comer nada porque mi glucosa subiría aun más.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Correcto. Debo hacer algo para bajar mi azucar, si como subirá.')
                        
                        self.acNAO.decirFrase('Voy a inyectarme insulina para bajar mi glucosa. Es lo que realmente debo hacer en estos casos.')
                        self.acNAO.accionPinchate()
                        self.simremoto.enviaDatosSimulacion(1,0,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time.time()
                        self.estado = 3
                    # Si glucosa normal
                    else:
                        self.acNAO.decirFrase('¿De verdad crees que no?. Lo cierto es que ya me encuentro mejor, creo que mi glucosa se está normalizando.')
                        self.estado = 1
                
                else:
                    self.acNAO.decirFrase('Espera, primero contesta a mi pregunta.')
                
            # Case estado = 3
            elif self.estado == 3:
                if self.palabraRec == 'toma un zumo' or self.palabraRec == 'come un bocata' or self.palabraRec == 'come una pizza':
                    self.acNAO.decirFrase('Si tomo algo me subirá más el azucar, debo esperar a que se normalice porque ya he tomado medidas.')
                elif self.palabraRec == 'haz deporte':
                    self.acNAO.decirFrase('Dame un respiro amigo, debo esperar a estar bien para poder hacer ejercicio de nuevo.')
                else:
                    self.acNAO.decirFrase('Debo esperar a que mi nivel de glucosa se normalice porque ya he tomado medidas.')                    
        
    def fase2(self):
        cho = 0
        bolus = 0
        aux = 0
#        palabraRec = ""
        print('Ejecuto fase2, glucosa actual: ' + str(self.glucosa[0]) )
        self.dmqtt.publicaVentanaEscenarioMQTT("##### Principio del bucle ##### \nFase: 2 \nNumero random: " 
            +str(self.numerorandom) + " \nPalabra recibida: " + str(self.palabraRec) 
            + " \nPalabra anterior: " + str(self.ultimaPalabra) + " \nContador: " 
            + str(self.contador))

        ################################################
        #### SEGUN NIVEL DE GLUCOSA HACEMOS ############
        ################################################

        # Glucosa bien
        if self.glucosa[0] > 75 and self.glucosa[0] < 150:
            print 'Glucosa correcta'
            self.acNAO.setLedsOjosBlue(False)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            if self.estadotaller == 2:
                    self.acNAO.decirFrase('Hey, ya me encuentro bien. Voy a medir mi glucosa para comprobarlo.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Ya me siento genial. Estoy listo para seguir. La próxima vez seré más cuidadoso antes de hacer ejercicio.')
                    self.estadotaller = 3
            elif self.estadotaller == 4:
                    self.acNAO.decirFrase('Hey, ya me encuentro bien. Voy a medir mi glucosa para comprobarlo.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor ' + str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Ya me siento genial. Estoy listo para seguir.')
                    self.estadotaller = 5
                    self.numHambre = 2
                    
        # Glucosa baja
        elif self.glucosa[0] < 75:
            print 'Glucosa baja'
            self.acNAO.setLedsOjosBlue(False)
            self.acNAO.setLedsOjosGreen(False)
            self.acNAO.setLedsOjosRed(True)
            self.acNAO.decirFrase('Mi glucosa es baja')
            
            # Segun estadotaller...
            if self.estadotaller == 1:
                self.acNAO.decirFrase('Me he puesto a correr sin medirme la glucosa y sin preocuparme por si debo comer algo, por eso ahora me encuentro mal.')
                self.acNAO.accionMedirGlucosa()
                self.acNAO.decirFrase('Ahora mismo tengo ' + str(self.mirarGlucosa()))
                self.acNAO.decirFrase('Voy a tomarme un zumo para subir mi glucosa. No puedo permitir que siga tan baja. Si en un rato sigo igual me tomaré otro.')
                self.simremoto.enviaDatosSimulacion(0,15,False,0,0,0)
                self.acNAO.accionComer()
                self.estadotaller = 2
            elif self.estadotaller == 2 or self.estadotaller == 4:
                self.acNAO.decirFrase('Ahora debo esperar tranquilo a que mi glucosa vuelva a ser normal.')
            elif self.estadotaller == 3:
                self.acNAO.decirFrase('Voy a medirla para saber su valor.')
                self.acNAO.accionMedirGlucosa()
                self.acNAO.decirFrase('Ahora mismo tengo ' + str(self.mirarGlucosa()))
                self.acNAO.decirFrase('Voy a tomarme un zumo para subir mi glucosa. No puedo permitir que siga tan baja. Si en un rato sigo igual me tomaré otro.')
                self.simremoto.enviaDatosSimulacion(0,15,False,0,0,0)
                self.acNAO.accionComer()
                self.acNAO.decirFrase('No he sido previsor, y el bolo de insulina que me he puesto antes de comer ha sido demasiado grande al hacer ahora ejercicio. Otra vez, debería ponerme menos si voy a hacer deporte después.')
                self.estadotaller = 4
          
        # Glucosa alta      
        elif self.glucosa[0] >= 300:
            print 'Glucosa muy alta'
            self.acNAO.setLedsOjosBlue(True)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            self.acNAO.decirFrase('Mi glucosa es alta')
            
        ################################################
        #### ESPERAMOS RESPUESTA DE PERSONA ############
        ################################################
        (self.respEspera,exac,self.palabraRec) = self.acNAO.esperarPalabra(self.getWordlistFase2(),10)
    
        # Interpretamos respuesta, que si es correcta actuamos
        if self.respEspera == -1 or self.respEspera == -2:
            print 'respEspera - Respuesta negativa'
        elif self.respEspera == 1:
            
            if exac < self.exactitud:
                print 'respEspera - Exactitud no suficiente'
                self.acNAO.decirFrase('Perdona, no te he entendido, repítemelo más despacito por favor.')
            else:
                self.dmqtt.publicaVentanaEscenarioMQTT("##### Palabra entendida ##### \nFase: 2 \nEstado: " 
                    + str(self.estado) + " \nNumero random: " +str(self.numerorandom) 
                    + " \nPalabra recibida: " + str(self.palabraRec) + " \nPalabra anterior: " 
                    + str(self.ultimaPalabra) + " \nContador: " + str(self.contador))
                print 'respEspera - Respuesta entendida' + self.palabraRec
                if self.palabraRec == 'vamos a hacer deporte':
                    self.ultimaPalabra = 'vamos a hacer deporte'
                    if self.numEjercicio == 1:
                        self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                        self.simremoto.enviaDatosSimulacion(0,0,True,0,50,60)
                        #self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Uff... Estoy agotado.')
                        self.numEjercicio = self.numEjercicio + 1
                    elif self.numEjercicio == 2:
                        self.acNAO.decirFrase('Primero debería medir mi glucosa media hora antes de empezar.')
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(self.mirarGlucosa()))
                        self.acNAO.decirFrase('Como mi glucosa es menor de 150 voy a comerme un snack para que no me baje tanto la glucosa durante el ejercicio.')
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                        self.simremoto.enviaDatosSimulacion(0,15,True,30,50,60)
                        #self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte, me siento bien.')
                        self.numEjercicio = self.numEjercicio + 1
                        self.numHambre = 1
                    else:
                        self.acNAO.decirFrase('Primero voy medir mi glucosa.')
                        aux = self.mirarGlucosa()
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(aux))
                        
                        if aux < 150:
                        	self.acNAO.decirFrase('Como mi glucosa es menor de 150 voy a comerme un snack para compensar la bajada de glucosa del ejercicio.')
                        	cho = 10
                        	self.acNAO.accionComer()
                        elif aux >= 150:
                        	self.acNAO.decirFrase('Como mi glucosa es mayor de 150 no es necesario que coma nada.')
                        	cho = 0
                        	
                        self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                        self.simremoto.enviaDatosSimulacion(0,cho,True,30,50,60)
                        #self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte.')
                        self.numEjercicio = self.numEjercicio + 1
                        
                elif self.palabraRec == 'dime tu glucosa':
                    print 'Escenario - Orden de decir glucosa'
                    self.acNAO.decirFrase('Voy medir mi glucosa.')
                    aux = self.mirarGlucosa()
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo tengo ' + str(aux))
                        
                elif self.palabraRec == 'tienes hambre':
                    self.ultimaPalabra = 'tienes hambre'
                    if self.numHambre == 1:
                        self.acNAO.decirFrase('Sí, la verdad es que estoy muerto de hambre. Dentro de dos horas tengo clase de gimnasia, así que voy a comer ahora lo que me han preparado en mi casa')
                        self.acNAO.decirFrase('Voy a medirme la glucosa.')
                        self.acNAO.accionMedirGlucosa()
                        aux = self.mirarGlucosa()
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(aux))
                        self.acNAO.decirFrase('Este plato tiene unas 6 raciones de carbohidratos. Me voy a inyectar ')
                        cho = 60
                        bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0
                        bolus = round(bolus*1000)/1000 
                        bolus = round(bolus*2)/2   
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina y luego voy a comer.')
                        self.acNAO.accionPinchate()
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Se me hace tarde, la clase de gimnasia empieza ahora.')
                        self.simremoto.enviaDatosSimulacion(bolus,cho,True,120,50,60)
                        #self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte.')
                        self.numHambre = 0
                    elif self.numHambre == 2:
                        self.acNAO.decirFrase('Sí, la verdad es que estoy muerto de hambre. Dentro de dos horas tengo clase de gimnasia, así que voy a comer ahora lo que me han preparado en mi casa')
                        self.acNAO.decirFrase('Voy a medirme la glucosa.')
                        self.acNAO.accionMedirGlucosa()
                        aux = self.mirarGlucosa()
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(aux))
                        cho = 60
                        self.acNAO.decirFrase('Este plato tiene unas 6 raciones de carbohidratos. Me voy a inyectar ')
                        bolus=(cho/30)+(0.027/6)*(self.glucosa[0]-90)-0
                        bolus=0.5*bolus
                        bolus=round(bolus*1000)/1000
                        bolus=round(bolus*2)/2
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina ')
                        self.acNAO.decirFrase('Es la mitad de lo recomendado porque voy a hacer deporte después de comer')
                        self.acNAO.accionPinchate()
                        self.acNAO.decirFrase('Ahora voy a comer.')
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Se me hace tarde, la clase de gimnasia empieza ahora.')
                        self.simremoto.enviaDatosSimulacion(bolus,cho,True,120,50,60)
                        #self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte. Me siento genial.')
                    else:
                        self.acNAO.decirFrase('No, la verdad es que no tengo hambre.')
                        
                elif self.palabraRec == 'avanza':
                    self.acNAO.decirFrase('Cambiamos a la fase 3')
                    self.fase = 3
            
    def run(self):
        print('Arranca Escenario')
        self.acNAO.setThreadBlock(True)
        self.acNAO.accionLevantarse()

        self.ultimaPalabra = 'default'
        self.ultimaPostura = 'default'
        self.pararLoop = True
        self.fase = 2
        self.numHambre = 0
        self.numEjercicio = 1
        self.estadotaller = 1
        self.estado = 1
        self.estadoprevio = 1
        self.contador = 1
        self.iniFase3 = True
        
        while self.pararLoop :
            self.mirarGlucosa()
            self.exactitud = self.datos.getData('EXACPALABRA')
        
            if self.estado == 1:
                #Calcular numero aleatorio entre 1 y 2
                #- SI numerorandom = 1: el robot dará una recomendacion correcta
                #- SI numerorandom = 2: el robot dará una recomendacion incorrecta
                self.numerorandom = random.randint(1,2)
                
            if self.fase == 2:
                self.fase2()
            elif self.fase == 3:
                self.fase3()
        self.acNAO.posicionParada()
        self.acNAO.setThreadBlock(False)