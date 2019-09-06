from collections import deque
from AccionesNAO import AccionesNAO
from SimuladorRemoto import SimuladorRemoto
from DatosCompartidos import DatosCompartidos
import random
import time
from threading import Thread

class Interaccion(object):
    def __init__(self, d, ac, r, mqtt):
        self.dmqtt = mqtt
        self.ac = ac
        self.datos = d
        self.simremoto = r
        self.glucosa = deque((-1, -1, -1, -1, -1))
        self.contador = 1
        self.wordlist = list()
        self.ultimaPalabra = None
        self.ultimaPostura = None

    def actualizarContador(self):
        self.contador = self.contador + 1
        if self.contador == 5:
            self.contador = 1
    
    def setDatosCompartidos(self, datos):    
        if datos != None:        
            self.datos = datos
            return 1
        return -1
    
    def setAccionesNAO(self, ac):
        if ac != None:
            self.ac = ac
            return 1
        return -1
        
    def startThread(self):
        self.hilo = Thread(target=self.run)
        self.hilo.start()
        self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,CORRIENDO")
    
    def pararThread(self):
        self.pararLoop = False
        print 'Interaccion # pararThread: Antes de self.ac.pararEsperaPalabra()'
        self.ac.pararEsperaPalabra()
        print 'Interaccion # pararThread: hasattr(self, "hilo") = ' + str(hasattr(self, "hilo"))
        if hasattr(self, "hilo"):
            print 'Interaccion # pararThread: Antes del join'
            self.hilo.join()
            print 'Interaccion # pararThread: Antes del publicaInterfazHilosMQTT'
            self.dmqtt.publicaInterfazHilosMQTT("INTERACCION,PARADO")
            print 'Interaccion # pararThread: Se hace el join'
    
    def pausar(self):
        print 'En INTERACCION el metodo PAUSAR No hace nada'
    
    def desPausar(self):
        print 'En INTERACCION el metodo DESPAUSAR No hace nada'
    
    def mirarGlucosa(self):
        glucosaAux = self.simremoto.getGlucosaRemoto()
        glucosastr = '%.2f'%(glucosaAux)
        self.glucosa.appendleft(glucosaAux)
        self.glucosa.pop()
        return glucosastr
        
    def run(self):
        self.pararLoop = True
        exac = 0
        self.wordlist = ["hola", "adios", "como te llamas", "que tal estás",
                         "sientate", "levantate", "choca el puño", "salta",
                         "tumbate", "dime tu glucosa"]
        self.ac.setThreadBlock(True)
        self.ac.accionLevantarse()
        
        # Hilo
        while(self.pararLoop):
            self.exact = self.datos.getData("EXACPALABRA")
            probability = random.randint(0,10)
            print 'Interaccion # Probability: ' + str(probability)
#            msg = "exac:" + str(self.exact) + "prob:" + str(probability)
#            self.datos.modifyData("INTERACCION","exac:" + str(self.exact) + "prob:" + str(probability))
            self.mirarGlucosa()
    
            if self.glucosa[0] > 75 and self.glucosa[0] < 150:            
                self.ac.setLedsOjosBlue(False)
                self.ac.setLedsOjosGreen(True)
                self.ac.setLedsOjosRed(False)
                if probability <= 3:
                    self.ac.decirFrase("Mi glucosa esta bien")
            elif self.glucosa[0] < 75 :
                self.ac.setLedsOjosRed(False)
                self.ac.setLedsOjosGreen(False)
                self.ac.setLedsOjosBlue(True)
                if probability <= 3:
                    self.ac.decirFrase("Mi glucosa es baja")
            elif self.glucosa[0] >= 300 :            
                self.ac.setLedsOjosRed(True)
                self.ac.setLedsOjosGreen(False)
                self.ac.setLedsOjosBlue(False)
                if probability <= 3:
                    self.ac.decirFrase("Mi glucosa es alta")    
    
            # Esperamos palabra
            if self.ac != None:
                (respEspera,exac,palabraRec) = self.ac.esperarPalabra(self.wordlist,10)
                
            # Switch de la respuesta (escuchada)
            if respEspera == -1 or respEspera == -2:
                pass
            elif respEspera == 1:
                # Si no se entiende bien...
                if exac < self.exact:
                    self.ac.decirFrase("Perdona, no te he entendido, repítemelo más despacito por favor.")
                # Si se entiende bien...
                else:
                    if palabraRec == "hola":                    
                        self.ac.accionSaludo(self.contador)
                        self.actualizarContador()
                        self.ultimaPalabra = "hola"
                        
                    if palabraRec == "adios":                    
                        self.ac.accionDespedida(self.contador)
                        self.actualizarContador()
                        self.ultimaPalabra = "adios"
                        
                    if palabraRec == "como te llamas":                    
                        self.ac.decirFrase("Mi nombre es Andy, soy el robot humanoide con diabetes del instituto aídos de la Universidad Politécnica de Valencia.")
                        self.ultimaPalabra = "como te llamas"
                        time.sleep(1)
                        
                    if  palabraRec == "que tal estas":                    
                        self.ac.accionQUETALESTAS(self.contador)
                        self.actualizarContador()
                        self.ultimaPalabra = "que tal estas"
                        
                    if  palabraRec == "sientate":                    
                        if self.ultimaPostura == "sientate":                        
                            self.ac.decirFrase("Pero si ya estoy sentado...")
                        else:
                            if self.contador == 1:
                                self.ac.decirFrase("Hora de descansar un rato. ¿Listos?")
                            elif self.contador == 2:
                                self.ac.decirFrase("Otra vez me estás haciendo hacer deporte.")
                            elif self.contador == 3:
                                self.ac.decirFrase("Me dispongo a tomar asiento. Allá voy.")
                            elif self.contador == 4:
                                self.ac.decirFrase("Me sentaré en el suelo porque veo que no me habéis traido una silla.")
    
                        #self.ac.accionSentarse()
                        self.actualizarContador()
                        self.ultimaPostura = "sientate"
                        time.sleep(1)
                        
                    if palabraRec == "levantate":                    
                        if self.ultimaPostura == "sientate":                        
                            self.ac.decirFrase("Pero si me acabo de sentar...")
                            self.ac.accionLevantarse()
                            self.ultimaPostura = "levantate"
                            time.sleep(1)
                        elif self.ultimaPostura == "tumbate":                        
                            self.ac.decirFrase("Con lo bien que estoy aquí tumbado...")
                            self.ac.accionLevantarse()
                            self.ultimaPostura = "levantate"
                            time.sleep(1)
                        else:
                            self.ac.decirFrase("Pero si ya estoy en pie...")
                    
                    if palabraRec == "choca el puño":                    
                        self.ac.decirFrase("Choca ese puño colega.")
                        self.ac.accionChocarMano()
                        self.ultimaPalabra = "choca el puño"
    
                    if palabraRec == "salta":                    
                        if self.ultimaPalabra=="salta":                        
                            self.ac.decirFrase("Estás pesadíto con el tema...")
                        else:
                            self.ac.decirFrase("¿Estás loco? Si salto seguro que me hago daño, en otra ocasión.")
                            self.ultimaPalabra = "salta"
                            
                    if palabraRec == "tumbate":                    
                        if self.ultimaPostura == "tumbate":                        
                            self.ac.decirFrase("Pero si ya estoy tumbado...")
                        else:
                            if self.contador == 1:
                                self.ac.decirFrase("Me voy a la cama que hay que descansar.")
                            elif self.contador == 2:
                                self.ac.decirFrase("Voy a tumbarme un ratito.")
                            elif self.contador == 3:
                                self.ac.decirFrase("Ya era hora de un descanso.")
                            elif self.contador == 4:
                                self.ac.decirFrase("Solo me falta una cama.")
                            #self.ac.accionTumbarse()
                            self.actualizarContador()
                        self.ultimaPostura = "tumbate"
                        self.ac.decirFrase("Despiertame dentro de 5 minutitos.")
    
                    if palabraRec == "dime tu glucosa" and exac > 0.45:                    
                        self.ac.accionMedirGlucosa()
                        glu = str(self.mirarGlucosa())
                        self.ac.decirFrase("Ahora mismo mi glucosa es de valor " + glu)
    
        # Cuando se sale del bucle...
        self.ac.posicionParada()
        self.ac.setThreadBlock(False)