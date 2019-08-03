from Runnable import Runnable
from collections import deque
from AccionesNAO import AccionesNAO
from DatosCompartidos import DatosCompartidos
import random
from time import time

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class Interaccion(Runnable):
    def __init__(self, d, ac):
        super().__init__()
        self.ac = ac
        self.datos = d
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
    
    def pararThread(self):
        self.pararLoop = False
        self.ac.pararEsperaPalabra()
    
    def pausar(self):
        pass
    
    def desPausar(self):
        pass
    
    def guardarGlucosa(self, glu):
        # insertamos nuevo
        self.glucosa.appendleft(glu)
        # quitamos antiguo
        self.glucosa.pop()    
    
    def mirarGlucosa(self):
        glucosaAux = self.datos.getData("GLUCOSA")
        self.guardarGlucosa(glucosaAux)
        return glucosaAux
        
    def populateWordList(self):
        self.wordlist.append('hola')
        self.wordlist.append('adios')
        self.wordlist.append('como te llamas')
        self.wordlist.append('que tal estás')
        self.wordlist.append('sientate')
        self.wordlist.append('levantate')
        self.wordlist.append('choca el puño')
        self.wordlist.append('salta')
        self.wordlist.append('tumbate')
        self.wordlist.append('dime tu glucosa')
    
    def run(self):
        if self.datos == None or self.ac == None:
            self.setEstadoHilo(PARADO)
            return
    
        self.pararLoop = True
        exac = 0
    
        populateWordList()
        self.datos.setData("INTERACCION","-",True)
    
        self.ac.setThreadBock(True)
        self.ac.accionLevantarse()
        
        # Hilo
        while(self.pararLoop):
            self.exact = self.datos.getData("EXACPALABRA")
            probability = random.randint(0,10)
            msg = "exac:" + str(self.exact) + "prob:" + str(probability)
            self.datos.modifyData("INTERACCION","exac:" + str(self.exact) + "prob:" + str(probability))
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
                (respEspera,palabraRec,exac) = self.ac.esperarPalabra(wordlist,10)
                
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
                        sleep(1)
                        
                    if  palabraRec == "que tal estas":                    
                        self.ac.accionQUETALESTAS(self.contador)
                        self.actualizarContador()
                        self.ultimaPalabra = "que tal estas"
                        
                    if  palabraRec == "sientate":                    
                        if self.ultimaPostura == "sientate":                        
                            self.ac.decirFrase("Pero si ya estoy sentado...")
                        else:
                            if self.contador == 1:
                                ac.decirFrase("Hora de descansar un rato. ¿Listos?")
                            elif self.contador == 2:
                                ac.decirFrase("Otra vez me estás haciendo hacer deporte.")
                            elif self.contador == 3:
                                ac.decirFrase("Me dispongo a tomar asiento. Allá voy.")
                            elif self.contador == 4:
                                ac.decirFrase("Me sentaré en el suelo porque veo que no me habéis traido una silla.")
    
                        self.ac.accionSentarse()
                        self.actualizarContador()
                        self.ultimaPostura = "sientate"
                        sleep(1)
                        
                    if palabraRec == "levantate":                    
                        if self.ultimaPostura == "sientate":                        
                            self.ac.decirFrase("Pero si me acabo de sentar...")
                            self.ac.accionLevantarse()
                            self.ultimaPostura = "levantate"
                            sleep(1)
                        elif self.ultimaPostura == "tumbate":                        
                            self.ac.decirFrase("Con lo bien que estoy aquí tumbado...")
                            self.ac.accionLevantarse()
                            self.ultimaPostura = "levantate"
                            sleep(1)
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
                            self.ac.accionTumbarse()
                            self.actualizarContador()
                        self.ultimaPostura.assign("tumbate")
                        self.ac.decirFrase("Despiertame dentro de 5 minutitos.")
    
                    if palabraRec == "dime tu glucosa" and exac > 0.45:                    
                        self.ac.accionMedirGlucosa()
                        self.ac.decirFrase("Ahora mismo mi glucosa es de valor " + str(self.mirarGlucosa()))
    
        # Cuando se sale del bucle...
        self.ac.posicionParada()
        self.ac.setThreadBock(False)
        if self.datos != None:
            self.datos.deleteData("INTERACCION")
    
    def populateWordList(self):
        self.wordlist = ["hola", "adios", "como te llamas", "que tal estás",
                         "sientate", "levantate", "choca el puño", "salta",
                         "tumbate", "dime tu glucosa"]