# http://www.alglib.net/translator/man/manual.cpython.html
from Runnable import Runnable
from DatosCompartidos import DatosSimulador, DatosCompartidos
import xalglib
from time import time

# def ode_function_1_diff(self, &x, t, &dx, *ptr):
PATHNAO = "/home/nao/naoqi/simulador.txt"
PATHMIPC = "C:\Users\Jahel\Documents\TFM\PythonNAO\pythonserver27\simulador.txt"

PARADO = 0
CORRIENDO = 1
PAUSADO = 2 

class Simulador(Runnable):
    def __init__(self):
        super().__init__()  
        self.modo = 2  #modo por defecto
        self.bw = 70
        self.tmaxG = 40                 # min
        self.vg = 0.16 * self.bw            # L
        self.egp0 = 0.0161 * self.bw        # mmol/min
        self.f01 = 0.0097 * self.bw         # mmol/min    
        self.fcorreccion = 0.027/6      #factor de correccion del bolus implementado
    
        #condiciones normales de simulacion
        self.bolus = 0
        self.cho = 0
        self.ejercicio = False
        self.exercise = list([0,0,0])
        self.flagThread = True
        self.flagPausar = False
        self.datosC = None
    
        self.t = []
        self.x = []
        self.SimVolGlucosaTotal = []
        
        #creamos dato compartido para la glucosa, marcamos como enviable y añadimos referencia a datoscompartidos
        self.d = {'bw' : self.bw,
                  'tmaxG' : self.tmaxG,
                  'vg' : self.vg,
                  'egp0' : self.egp0,
                  'f01' : self.f01,
                  'bolus' : None,
                  'cho' : None,
                  'exercise' : list([0,0,0]),
                  'ejercicio' : None}

    def setDatosCompartidos(self, d):    
        if d != None:        
            self.datosC = d
            self.datosC.setData("GLUCOSA",float(-1000),True)
            self.datosC.setData("MODOSIMU",int(2),False)
            return 1
        return-1
    
    ### De Runnable
    def pararThread(self):
        self.flagThread = False
        if self.flagPausar == True:        
            self.flagPausar = False
            self.liberarCondicion()
        
    ### De Runnable
    def pausar(self):
        self.flagPausar = True
        self.setEstadoHilo(PAUSADO)
    
    ### De Runnable
    def desPausar(self):
        if self.flagPausar == True:        
            self.flagPausar = False
            self.liberarCondicion()

    def setModo(self, modo):
        self.modo = modo
    
    def ConfigurarSimulador(self):
        if self.modo == 1:
            self.pasosSimulacion = 60
            self.marcaLimite=60
        elif self.modo == 2:
            self.pasosSimulacion = 96
            self.marcaLimite=96
        elif self.modo == 3:
            self.pasosSimulacion = 120
            self.marcaLimite=120
        else:
            print '%%%%ERROR en void Simular: Modo no seleccionado correctamente, de tiempos mal.'
    
        #Construir vector de tiempos que usaremos
        f = open(PATHMIPC, "a+")
        f.write(str(self.pasosSimulacion)+'\n')
        f.close()
        valort = 0
        for i in range(0,self.pasosSimulacion):
            self.t.append(valort)
            valort = valort + 5
        
        #estadoInicial del simulador (para la primera simulacion)
        self.x = [0,0, 366.6667,366.6667, 5.7511,0.0294,0.0047,0.2991,56.5688, 23.5554]
    
        self.tiempoIniPausado = 0
        self.tiempoTotalPausado = 0
        time.sleep(0.5)
    
    def run(self):
        try:
            modoAux = self.datosC.getData("MODOSIMU")
            if modoAux == 1:            
                self.modo = modoAux
            else:
                self.modo = 2
            self.ConfigurarSimulador()
            self.simular()
            self.calcularGlucosa()
            self.tiempoUltimaSimu = time()
    
            while (self.flagThread):
               #mirar pausa
               if self.flagPausar == True:               
                   self.tiempoIniPausado = time()
                   if  self.datosC != None:
                       self.datosC.modifyData("GLUCOSA",float(-999))
                   self.esperarCondicion()
                   self.tiempoTotalPausado = self.tiempoTotalPausado + (time() - self.tiempoIniPausado)
    
               #miramos si tenemos nuevos datos para realizar la simulacion
               if self.datosC != None:
                   self.datosSimu = self.datosC.getDatosSimulacion()
    
               if self.datosSimu.bolus == 0 and self.datosSimu.cho == 0 and self.datosSimu.ejercicio == False:
                   #obtenemos marca altual del simulador
                   self.calcularMarcaActual()
                   if self.datosC != None:
                        self.datosC.modifyData("GLUCOSA",float(self.SimVolGlucosaTotal[self.marca]))
                   #Se ejecutará una simulacion sin entradas si pasan 5 minutos y no hay eventos.                   
                   if self.marca >= self.marcaLimite:
                       self.actualizarEstadoInicial(len(self.xtbl)-1)
                       self.simular()
                       self.calcularGlucosa()
                       self.tiempoUltimaSimu = time()
                       self.tiempoIniPausado = 0
                       self.tiempoTotalPausado = 0
                   else:
                       time.sleep(1)
    
               else:
                   #valores de bolus, o ejercicio nuevos, actualizamos
                   self.bolus = self.datosSimu.bolus
                   self.cho = self.datosSimu.cho
                   self.ejercicio = self.datosSimu.ejercicio
                   self.exercise[0] = self.datosSimu.ejercicioTiempo; #ejeTiempo
                   self.exercise[1] = self.datosSimu.ejercicioIntesidad; #ejeIntensidad
                   self.exercise[2] = self.datosSimu.ejercicioDuracion; #ejeDuracion
                   self.actualizarEstadoInicial(self.marca)
                   self.simular()
                   self.calcularGlucosa()
                   self.tiempoUltimaSimu = time()
                   self.tiempoIniPausado = 0
                   self.tiempoTotalPausado = 0
    
            # Fuera del while
            self.flagThread = True
            if  self.datosC != None:
                self.datosC.modifyData("GLUCOSA",float(-1000))
        except Exception as e:
            f = open(PATHMIPC, "a+")
            f.write('error :'+str(e)+'\n')
            f.close()
            return
    
    def simular(self):
        eps = 0.00001
        h = 0
        
        #actualizamos parametros que le pasamos al modelo
        self.d['bolus'] = self.bolus
        self.d['cho'] = self.cho
        self.d['ejercicio']  = self.ejercicio
        if self.ejercicio == True:        
            self.d['exercise'][0] = self.exercise[0]
            self.d['exercise'][1] = self.exercise[1]
            self.d['exercise'][2] = self.exercise[2]
    
    
        s = xalglib.odesolverrkck(self.x, self.t, eps, h)
        xalglib.odesolversolve(s, ode_function_1_diff, self.d)
        m, self.ttbl, self.xtbl, rep = xalglib.odesolverresults(s)
    
        self.bolus = 0
        self.cho = 0
        self.ejercicio = False
        self.exercise[0] = 0
        self.exercise[1] = 0
        self.exercise[2] = 0
    
    def calcularGlucosa(self):    
        for i in range(0,len(self.xtbl)):
            self.SimVolGlucosaTotal[i] = float(18 * self.xtbl[i][8] / self.vg)
    
    def calcularMarcaActual(self):
        tiempo = (time() - self.tiempoUltimaSimu) - self.tiempoTotalPausado
        if self.pasosSimulacion == 60:
            self.marca = tiempo/4.918
        if self.pasosSimulacion == 96:
            self.marca = tiempo/3.09
        if self.pasosSimulacion == 120:
            self.marca = tiempo/2.479
    
    def actualizarEstadoInicial(self, marca):
        self.x[0] = self.xtbl[marca,0]
        self.x[1] = self.xtbl[marca,1]
        self.x[2] = self.xtbl[marca,2]
        self.x[3] = self.xtbl[marca,3]
        self.x[4] = self.xtbl[marca,4]
        self.x[5] = self.xtbl[marca,5]
        self.x[6] = self.xtbl[marca,6]
        self.x[7] = self.xtbl[marca,7]
        self.x[8] = self.xtbl[marca,8]
        self.x[9] = self.xtbl[marca,9]
    
#la funcion que necesita odesolversolve tiene que ser una funcion normal (no mienbro de la clase) ya que odesolversolve espera un un puntero a funcion (*)(void)
#en caso de que esta funcion fuera mienbro de la clase tendriamos (Simulador.*)(void) y nos daria un error
def ode_function_1_diff(x, t, dx, ptr):

#    data_struct *datos
#    datos = (data_struct*) ptr
    datos = ptr

    #***** PARAMETROS SIMULADOR ------------------
    gamma2 = 1                 # factor to change patient's insulin sensitivity (to make the patient more insulin sensitive or insulin resistant)
    #  Model parameters (Hovorka)
    ag = 0.8                  # unitless
    ka1 = 0.006               # 1/min
    ka2 = 0.06                # 1/min
    ka3 = 0.03                # 1/min
    sit = gamma2 * 0.00512    # min^(-1) per mU/L
    sid = gamma2 * 0.00082    # min^(-1) per mU/L
    sie = gamma2 * 0.052      # per mU/L
    k12 = 0.066               # 1/min
    ke = 0.138                # 1/min
    vi = 0.12 * datos.bw            # L
    tmaxI = 55                 # min
    #  BASAL
    basal = 0.4/60
    #----------------------------------------------

    g1 = x[0]
    g2 = x[1]
    s1 = x[2]
    s2 = x[3]
    I  = x[4]
    X1 = x[5]
    X2 = x[6]
    X3 = x[7]
    Q1 = x[8]
    Q2 = x[9]

    meal_duration = 1
    u_cho = (datos.cho / meal_duration) * 1000 / 180
    if (t > meal_duration):
        u_cho = 0

    u_ins_basal = basal
    u_ins_bolus = datos.bolus
    if (t > 1):
        u_ins_bolus = 0
    u_ins = 1000 * (u_ins_basal + u_ins_bolus)   # mIU / min

    #/ ACTIVIDAD FISICA #############/
    # change of insulin sensitiviy due to exercise
    if datos.ejercicio ==True:        
        exercise_factor=1      # standard sensitivity
        alpha = 1.25*3.29   # according to Schiavon paper; it may require tuning for Hovorka model
        #filasejercicio = 1; #por ahora solo metemos 1 actividad fisica cada simulacion
        texercise=datos.exercise[0]
        dexercise=datos.exercise[2]

        if (t >= texercise) and (t < (texercise+dexercise)):            
            exercise_factor = alpha    # factor for a 50% VO2max.... for different intensity we could change proportionally, not validated
        elif (t >= (texercise+dexercise)) and (t < (texercise+dexercise+180)):            # generate slope: line equation (y-y0)=m*(x-x0);  y=y0+m*(x-x0)
            exercise_factor = alpha+((1-alpha)/180)*(t-(texercise+dexercise));   # factor will return to 1 after 180 minutes

        sid = sid*exercise_factor

    #########################/

    # glucose rate of appearance
    Ug = g2 / datos.tmaxG
    # insulin rate of appearance
    Ui = s2 / tmaxI
    # non - insulin - dependent consumption
    if Q1 / datos.vg >= 4.5:
        F01c = datos.f01
    else:
        F01c = datos.f01 * Q1 / (datos.vg * 4.5)
    # renal execretion
    if Q1 / datos.vg >= 9:        
        Fr = 0.003 * (Q1 - 9 * datos.vg)
    else:
        Fr = 0


    dx[0] = ag * u_cho - (1 / datos.tmaxG) * g1
    dx[1] = (1 / datos.tmaxG) * g1 - (1 / datos.tmaxG) * g2
    dx[2] = u_ins - s1 / tmaxI
    dx[3] = s1 / tmaxI - s2 / tmaxI
    dx[4] = Ui / vi - ke * I
    dx[5] = -ka1 * X1 + ka1 * sit * I
    dx[6] = -ka2 * X2 + ka2 * sid * I
    dx[7] = -ka3 * X3 + ka3 * sie * I
    dx[8] = -F01c - X1 * Q1 + k12 * Q2 - Fr + Ug + max((float(datos.egp0 * (1 - X3)), float(0)))
    dx[9] = X1 * Q1-(k12 + X2) * Q2
    return