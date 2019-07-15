# -*- coding: utf-8 -*-
from DatosCompartidos import DatosCompartidos
from AccionesComunicaNAO import AccionesComunicaNAO
from collections import deque
from time import time
import random
from Runnable import Runnable

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class Escenario(Runnable):
    def __init__(self):
        super().__init__()        
        self.pausa = False
        self.glucosa = deque((-1, -1, -1, -1, -1))
        self.exactitud = 0.3
        self.tiempoUltimaPeticionSimu = time()
        self.contador = 1
        self.datos = None
        self.acNAO = None
    
    def setDatosCompartidos(self, d):
        self.datos = d
        
    def setAccionesNAO(self, ac):
        self.acNAO = ac
        
    def guardarGlucosa(self, glu):
        # insertamos nuevo
        self.glucosa.appendleft(glu)
        # quitamos antiguo
        self.glucosa.pop()
        
    def mirarGlucosa(self):
        glucosaAux = self.datos.getData("GLUCOSA")
        self.guardarGlucosa(glucosaAux)
        return glucosaAux
        
    def pararThread(self):
        self.pararLoop = False
        self.acNAO.pararEsperaPalabra()
    
    def pausar(self):
        self.pausa = True
        
    def desPausar(self):
        self.pausa = False
        
    def actualizarContador(self):
        self.contador = self.contador + 1
        if self.contador == 5:
            self.contador = 1
    
    def getWordlistFase2(self):
        return deque(('vamos a hacer deporte', 'tienes hambre', 'avanza', 'dime tu glucosa', 'avanza'))
        
    def getWordlistFase3(self):
        auxlist = deque()
        if self.estado == 1:
            auxlist.append('hola')
            auxlist.append('adios')
            auxlist.append('como te llamas')
            auxlist.append('que tal estás')
            auxlist.append('sientate')
            auxlist.append('levantate')
            auxlist.append('choca el puño')
            auxlist.append('salta')
            auxlist.append('tumbate')
            auxlist.append('toma un zumo')
            auxlist.append('come un bocata')
            auxlist.append('come un pizza')
            auxlist.append('haz deporte')
        elif self.estado == 2:
            auxlist.append('si')
            auxlist.append('no')
        elif self.estado == 3:
            auxlist.append('toma un zumo')
            auxlist.append('come un bocata')
            auxlist.append('come una pizza')
            auxlist.append('haz deporte')
        # siempre:
        auxlist.append('dime tu glucosa')
        auxlist.append('avanza')
        return auxlist
        
    def fase3(self):
        cho = 0
        bolus = 0
        respEspera = 1
        self.datos.modifyData("ESCENARIO", self.fase)
        
        ################################################
        #### COMPROBACION DE GLUCOSA ###################
        ################################################
        
        # Se encuentra bien
        if self.glucosa[0] > 70 and self.glucosa[0] < 140:
            self.acNAO.setLedsOjosBlue(False)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            self.acNAO.decirFrase('Me encuentro perfectamente')
            if (time() - self.tiempoUltimaPeticionSimu) < 45:
                if self.iniFase3:
                    self.iniFase3 = False
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
            # case 1:
            if self.estado == 1:
                pass
            # case 2:
            elif self.estado == 2:
                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor')
                self.acNAO.accionMedirGlucosa();
                self.acNAO.decirFrase(str(self.mirarGlucosa()))
                if self.numerorandom == 1:
                    self.acNAO.decirFrase('El medico me recomienda tomarme un sobre de gel de 15 gramos, ¿crees que es la mejor opción?')
                    self.estado = 2
                elif self.numerorandom == 2: 
                    self.acNAO.decirFrase('El medico me recomienda que me pinche más insulina, ¿tú crees que es correcto?')
                    self.estado = 2
            # case 3:
            elif self.estado == 3:
                self.acNAO.decirFrase('Ahora debo esperar a que lo que me he hecho haga efecto en mi.')
                if (time() - self.tiempoUltimaPeticionSimu) < 60:
                    # Glucosa sube
                    if self.glucosa[0] > self.glucosa[3]:
                        self.acNAO.decirFrase('Mi glucosa está subiendo, aunque sigue siendo baja. Debo esperar un ratito más.')
                    # Glucosa baja
                    elif self.glucosa[0] < self.glucosa[3]:
                        self.acNAO.decirFrase('Algo va mal. Mi glucosa es baja y continua bajando. Debo tomar medidas.')
                        self.estado = 1
                        
                    # Glucosa normal ya?
                    if self.glucosa[0] > 70 and self.glucosa[0] < 140:
                        self.acNAO.decirFrase('Espera, ya me encuentro muy bien, me ha venido bien comer algo.')
                        self.estado = 1
                        
        # Glucosa alta, pero no mucho
        elif self.glucosa[0] > 140 and self.glucosa[0] < 180:
            self.acNAO.setLedsOjosBlue(False);
            self.acNAO.setLedsOjosGreen(True);
            self.acNAO.setLedsOjosRed(True);
            self.acNAO.decirFrase('Mi glucosa es alta.')
            
            # Variable local, comento porque al principio siempre es 1!!
#            if respEspera == 1:
#                pass
#            elif respEspera == 2:
#                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor')
#                self.acNAO.accionMedirGlucosa();
#                self.acNAO.decirFrase(str(self.mirarGlucosa()));
#
#                if self.numerorandom == 1:
#                    self.acNAO.decirFrase('El medico me recomienda queme pinche insulina, ¿crees que es la mejor opción?')
#                    self.estado = 2
#                elif self.numerorandom == 2:
#                    self.acNAO.decirFrase('El medico me recomienda comerme un bocata, ¿crees que es la mejor opción?')
#                    self.estado = 2
#            elif respEspera == 3:
#                self.acNAO.decirFrase('Ahora debo esperar a que la inyeccion de insulina haga efecto en mi y mi glucosa sea normal.')
#
#                if (time(), self.tiempoUltimaPeticionSimu) < 60:
#                    # Comprobacion de si la glucosa sube o baja
#                    if self.glucosa[0] > self.glucosa[2]:
#                        self.acNAO.decirFrase('Algo va mal. Mi glucosa debería estar bajando porque me he inyectado insulina, pero está subiendo. Debo tomar medidas')
#                        self.estado = 1
#                    elif self.glucosa[0] < self.glucosa[2]:
#                        self.acNAO.decirFrase('Mi glucosa está bajando debido a la inyección de insulina pero continua siendo alta. Debo esperar un poco más.')
#
#                    # Comprobacion de que estamos ya OK
#                    if self.glucosa[0] > 70 and self.glucosa[0] < 140:
#                        self.acNAO.decirFrase('Espera, ya me encuentro muy bien, la inyeccion de insulina me ha hecho efecto.')
#                        self.estado = 1
                        
        # Glucosa MUY alta
        elif self.glucosa[0] > 180:
            self.acNAO.setLedsOjosBlue(False);
            self.acNAO.setLedsOjosGreen(True);
            self.acNAO.setLedsOjosRed(True);
            self.acNAO.decirFrase('Tengo la glucosa peligrosamente alta.')
            
            # Si ha pasado >50 segundos desde la ultima actu...
            if (time() - self.tiempoUltimaPeticionSimu) > 50:
                # Y la insulina sigue creciendo...                
                if self.glucosa[0] > self.glucosa[2]:
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor')
                    self.acNAO.accionMedirGlucosa();
                    self.acNAO.decirFrase(str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Como es muy alta después de una hora desde que comí y además está subiendo voy a inyectarme insulina urgentemente.')
                    self.acNAO.accionPinchate()
                    self.estado = 3
                    cho = 0
                    # bolo prandial = ratio_insulina_carbohidratos * gramos de carbohidratos + factor de corrección*(glucemia actual - glucemia objetivo) - insulina a bordo
                    bolus = (cho/30)+(0.027/6)*(self.glucosa[0]-90)-0;
                    self.datos.setDatosSimulacion(bolus,cho,False,0,0,0);
                    self.tiempoUltimaPeticionSimu = time();
                
                # Si no sigue creciendo pero el tiempo que ha pasado es <50 sec
                elif (time() - self.tiempoUltimaPeticionSimu) < 50:
                    self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor')
                    self.acNAO.accionMedirGlucosa();
                    self.acNAO.decirFrase(str(self.mirarGlucosa()))
                    self.acNAO.decirFrase('Es muy alta pero como está disminuyendo voy a esperar un poco.')
                    self.estado = 3
            # Si no han pasado >50 segundos desde la ultima actu...
            else:
                self.acNAO.decirFrase('Ahora mismo mi glucosa es de valor')
                self.acNAO.accionMedirGlucosa();
                self.acNAO.decirFrase(str(self.mirarGlucosa()))
                self.acNAO.decirFrase('Es muy alta pero como acabo de intentar modificarla voy a esperar un ratito.')    
                
        
        ################################################
        #### ESPERAMOS RESPUESTA DE PERSONA ############
        ################################################
        (respEspera,palabraRec,exac)  = self.acNAO.esperarPalabra(self.getWordlistFase3(),15)
        
        # Interpretamos respuesta, que si es correcta actuamos
        if respEspera == -1 or respEspera == -2:
            pass
        elif respEspera == 1:
            # Acciones segun el estado en que estemos: 1,2,3
            # Case estado = 1
            if self.estado == 1:
                # Se mira que palabra (orden) se ha recibido
                if palabraRec == 'hola':
                    self.acNAO.accionSaludo(self.contador)
                    self.actualizarContador()
                    self.ultimaPalabra = 'hola'
                    
                if palabraRec == 'adios':
                    self.acNAO.accionDespedida(self.contador)
                    self.actualizarContador()
                    self.ultimaPalabra = 'adios'
                    
                if palabraRec == 'como te llamas':
                    self.acNAO.decirFrase('Mi nombre es Andy, y soy el robot humanoide con diabetes del instituto aídos de la Universidad Politécnica de Valencia.')
                    self.ultimaPalabra = 'como te llamas'
                    time.sleep(1)
                    
                if palabraRec == 'que tal estas':
                    self.acNAO.accionQUETALESTAS(self.contador);
                    self.actualizarContador()
                    self.ultimaPalabra = 'que tal estas'
                    
                if palabraRec == 'sientate':
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
                    self.acNAO.accionSentarse()
                    self.ultimaPostura = 'sientate'
                    time.sleep(1)
                    
                if palabraRec == 'levantate':
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
                        
                if palabraRec == 'choca el puño':
                    self.acNAO.decirFrase('Choca ese puño colega.')
                    self.acNAO.accionChocarMano()
                    self.ultimaPalabra = 'choca el puño'
                    
                if palabraRec == 'salta':
                    if self.ultimaPalabra == 'salta':
                        self.acNAO.decirFrase('Estás pesadíto con el tema...')
                    else:
                        self.acNAO.decirFrase('¿Estás loco? Si salto seguro que me hago daño, mejor en otra ocasión.')
                        self.ultimaPalabra = 'salta'
                        
                if palabraRec == 'tumbate':
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
                            
                        self.acNAO.accionTumbarse()
                        self.actualizarContador()
                    
                    self.ultimaPostura = 'tumbate'
                    self.acNAO.decirFrase('Despiertame dentro de 5 minutitos.')
                    
                if palabraRec == 'toma un zumo':
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
                    self.datos.setDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time()
                    
                if palabraRec == 'come un bocata':
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
                    self.datos.setDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time()
                    
                if palabraRec == 'come una pizza':
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
                    self.datos.setDatosSimulacion(bolus,cho,False,0,0,0)
                    self.tiempoUltimaPeticionSimu = time()
                    
                if palabraRec == 'haz deporte':
                    self.acNAO.decirFrase('Primero voy a medir mi glucosa.')
                    self.acNAO.accionMedirGlucosa()
                    self.acNAO.decirFrase('Ahora mismo es de valor ' + str(self.mirarGlucosa()))
                    
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
                    self.datos.setDatosSimulacion(bolus,cho,True,0,50,30)
                    self.tiempoUltimaPeticionSimu = time()
                    self.acNAO.accionCorrer()
                    
            # Case estado = 2
            elif self.estado == 2:
                if palabraRec == 'si':
                    # Si glucosa baja
                    if self.glucosa[0] < 70:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Es cierto, has acertado.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Meeeec, incorrecto amigo. No debo inyectarme porque mi glucosa bajaría aun más.')
                            
                        self.acNAO.decirFrase('Voy a tomarme un sobre de gel de 15 gramos para subir mi glucosa. No puedo permitir que siga tan baja. Si en un rato sigo igual me tomaré otro.')
                        self.acNAO.accionComer();
                        self.datos.setDatosSimulacion(0,15,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time()
                        self.estado = 3
                        time.sleep(1)
                    # Si glucosa alta
                    elif self.glucosa[0] > 140:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Creo que nos estamos equivocando. No debo comer nada porque mi glucosa subiría aun más.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Voy a inyectarme insulina para bajar mi glucosa. Es lo que realmente debo hacer en estos casos.')
                        
                        self.acNAO.decirFrase('Voy a inyectarme insulina para bajar mi glucosa. Es lo que realmente debo hacer en estos casos.')
                        self.acNAO.accionPinchate();
                        self.datos.setDatosSimulacion(1,0,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time()
                        self.estado = 3
                    # Si glucosa normal
                    else:
                        self.acNAO.decirFrase('¿De verdad crees que sí?. Lo cierto es que ya me encuentro mejor, creo que mi glucosa se está normalizando.')
                        self.estado = 1
                        
                if palabraRec == 'no':
                    # Si glucosa baja
                    if self.glucosa[0] < 70:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Meeeec, incorrecto amigo. No debo inyectarme porque mi glucosa bajaría aun más.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Es cierto, has acertado. Si ahora me pincho mi glucosa bajaría aun más.')
                        
                        self.acNAO.decirFrase('Voy a comerme un bocata para subir mi glucosa. No puedo permitir que siga tan baja.')
                        self.acNAO.accionComer()
                        self.datos.setDatosSimulacion(0,50,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time()
                        self.estado = 3
                    # Si glucosa alta
                    elif self.glucosa[0] > 140:
                        if self.numerorandom == 1:
                            self.acNAO.decirFrase('Creo que nos estamos equivocando. No debo comer nada porque mi glucosa subiría aun más.')
                        elif self.numerorandom == 2:
                            self.acNAO.decirFrase('Correcto. Debo hacer algo para bajar mi azucar, si como subirá.')
                        
                        self.acNAO.decirFrase('Voy a inyectarme insulina para bajar mi glucosa. Es lo que realmente debo hacer en estos casos.')
                        self.acNAO.accionPinchate()
                        self.datos.setDatosSimulacion(1,0,False,0,0,0)
                        self.tiempoUltimaPeticionSimu = time()
                        self.estado = 3
                    # Si glucosa normal
                    else:
                        self.acNAO.decirFrase('¿De verdad crees que no?. Lo cierto es que ya me encuentro mejor, creo que mi glucosa se está normalizando.')
                        self.estado = 1
                
            # Case estado = 3
            elif self.estado == 3:
                if palabraRec == 'toma un zumo' or palabraRec == 'come un bocata' or palabraRec == 'come una pizza':
                    self.acNAO.decirFrase('Si tomo algo me subirá más el azucar, debo esperar a que se normalice porque ya he tomado medidas.')
                elif palabraRec == 'haz deporte':
                    self.acNAO.decirFrase('Dame un respiro amigo, debo esperar a estar bien para poder hacer ejercicio de nuevo.')
        
    def fase2(self):
        cho = 0
        bolus = 0
        aux = 0
        msg = str(self.fase) + ',' + str(self.estadotaller) + ',' + str(self.numHambre) + ',' + str(self.numEjercicio) + ',' + str(self.ultimaPalabra)
        self.datos.modifyData("ESCENARIO",msg)

        ################################################
        #### SEGUN NIVEL DE GLUCOSA HACEMOS ############
        ################################################

        # Glucosa bien
        if self.glucosa[0] > 75 and self.glucosa[0] < 150:
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
                self.datos.setDatosSimulacion(0,15,False,0,0,0)
                self.acNAO.accionComer()
                self.estadotaller = 2
            elif self.estadotaller == 2 or self.estadotaller == 4:
                self.acNAO.decirFrase('Ahora debo esperar tranquilo a que mi glucosa vuelva a ser normal.')
            elif self.estadotaller == 3:
                self.acNAO.decirFrase('Voy a medirla para saber su valor.')
                self.acNAO.accionMedirGlucosa()
                self.acNAO.decirFrase('Ahora mismo tengo ' + str(self.mirarGlucosa()))
                self.acNAO.decirFrase('Voy a tomarme un zumo para subir mi glucosa. No puedo permitir que siga tan baja. Si en un rato sigo igual me tomaré otro.')
                self.datos.setDatosSimulacion(0,15,False,0,0,0)
                self.acNAO.accionComer()
                self.acNAO.decirFrase('No he sido previsor, y el bolo de insulina que me he puesto antes de comer ha sido demasiado grande al hacer ahora ejercicio. Otra vez, debería ponerme menos si voy a hacer deporte después.')
                self.estadotaller = 4
          
        # Glucosa alta      
        elif self.glucosa[0] >= 300:
            self.acNAO.setLedsOjosBlue(True)
            self.acNAO.setLedsOjosGreen(True)
            self.acNAO.setLedsOjosRed(False)
            self.acNAO.decirFrase('Mi glucosa es alta')
            
        ################################################
        #### ESPERAMOS RESPUESTA DE PERSONA ############
        ################################################
        (respEspera,palabraRec,exac) = self.acNAO.esperarPalabra(self.getWordlistFase2(),10)
    
        # Interpretamos respuesta, que si es correcta actuamos
        if respEspera == -1 or respEspera == -2:
            pass
        elif respEspera == 1:
            if exac < self.exactitud:
                self.acNAO.decirFrase('Perdona, no te he entendido, repítemelo más despacito por favor.')
            else:
                if palabraRec == 'vamos a hacer deporte':
                    self.ultimaPalabra = 'vamos a hacer deporte'
                    if self.numEjercicio == 1:
                        self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                        self.datos.setself.datosSimulacion(0,0,True,0,50,60)
                        self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Uff... Estoy agotado.')
                        self.numEjercicio = self.numEjercicio + 1
                    elif self.numEjercicio == 2:
                        self.acNAO.decirFrase('Primero debería medir mi glucosa media hora antes de empezar.')
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(self.mirarGlucosa()))
                        self.acNAO.decirFrase('Como mi glucosa es menor de 150 voy a comerme un snack para que no me baje tanto la glucosa durante el ejercicio.')
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Voy a correr un poco, abran hueco.')
                        self.datos.datosSimulacion(0,15,True,30,50,60)
                        self.acNAO.accionCorrer()
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
                        self.datos.setself.datosSimulacion(0,cho,True,30,50,60)
                        self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte.')
                        self.numEjercicio = self.numEjercicio + 1
                        
                elif palabraRec == 'tienes hambre':
                    self.ultimaPalabra = 'tienes hambre'
                    if self.numHambre == 1:
                        self.acNAO.decirFrase('Sí, la verdad es que estoy muerto de hambre. Dentro de dos horas tengo clase de gimnasia, así que voy a comer ahora lo que me han preparado en mi casa')
                        self.acNAO.decirFrase('Voy a medirme la glucosa.')
                        self.acNAO.accionMedirGlucosa()
                        aux = self.mirarGlucosa()
                        self.acNAO.decirFrase('Ahora mismo tengo ' + str(aux))
                        self.acNAO.decirFrase('Este plato tiene unas 6 raciones de carbohidratos. Me voy a inyectar ')
                        cho = 60
                        bolus = (cho/30)+(0.027/6)*(aux-90)-0
                        bolus = round(bolus*1000)/1000 
                        bolus = round(bolus*2)/2   
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina y luego voy a comer.')
                        self.acNAO.accionPinchate()
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Se me hace tarde, la clase de gimnasia empieza ahora.')
                        self.datos.setself.datosSimulacion(bolus,cho,True,120,50,60)
                        self.acNAO.accionCorrer()
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
                        bolus=(cho/30)+(0.027/6)*(aux-90)-0
                        bolus=0.5*bolus
                        bolus=round(bolus*1000)/1000
                        bolus=round(bolus*2)/2
                        self.acNAO.decirFrase(str(bolus) + ' unidades de insulina ')
                        self.acNAO.decirFrase('Es la mitad de lo recomendado porque voy a hacer deporte después de comer')
                        self.acNAO.accionPinchate()
                        self.acNAO.decirFrase('Ahora voy a comer.')
                        self.acNAO.accionComer()
                        self.acNAO.decirFrase('Se me hace tarde, la clase de gimnasia empieza ahora.')
                        self.datos.setself.datosSimulacion(bolus,cho,True,120,50,60)
                        self.acNAO.accionCorrer()
                        self.acNAO.decirFrase('Ya he acabado de hacer deporte. Me siento genial.')
                    else:
                        self.acNAO.decirFrase('No, la verdad es que no tengo hambre.')
                        
                elif palabraRec == 'avanza':
                    self.acNAO.decirFrase('Cambiamos a la fase 3')
                    self.fase = 3
            
    # El "run" de c++ runnable - TODO
    def run(self):
        if self.datos == None or self.acNAO == None:
            # NO SE QUE ES ESTO!! TODO: setEstadoHilo(PARADO)
            return
    
        self.acNAO.setThreadBock(True)
        self.acNAO.accionLevantarse()
        self.datos.setData('ESCENARIO',-1,True);

        self.ultimaPalabra = 'default'
        self.ultimaPostura = 'default'
        self.pararLoop = True
        self.fase = 2
        self.numHambre = 0
        self.numEjercicio = 1
        self.estadotaller = 1
        self.estado = 1
        self.contador=1
        self.iniFase3 = True
        
        while self.pararLoop :
            self.mirarGlucosa()
            self.exactitud = self.datos.getData('EXACPALABRA')
        
            if self.estado == 1:
                #Calcular numero aleatorio entre 1 y 2
                #- SI numerorandom = 1: el robot dará una recomendacion correcta
                #- SI numerorandom = 2: el robot dará una recomendacion incorrecta
                #srand(time(0)) //genera semilla basada en el reloj del sistema
                self.numerorandom = random.randint(1,2)
                
            if self.fase == 2:
                self.fase2()
            elif self.fase == 3:
                self.fase3()
        
        self.acNAO.posicionParada()
        self.acNAO.setThreadBock(False)
        self.datos.deleteData('ESCENARIO')