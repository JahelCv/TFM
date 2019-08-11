# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
import json
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from flask_restful import Resource, Api
from Simulador import Simulador

app = Flask(__name__)
api = Api(app)
s = None 

class HelloWorld(Resource):
    def get(self):
        return "Bienvenido!"
        
class ModoSimulador(Resource):
    def get(self):
        global s
        return s.getModo()
    def put(self):
        global s
        #print('Put sobre modosimulador: ',file=sys.stdout)
        #print(str(request.form))
        return s.setModo(request.form['data'])
        
class Glucosa(Resource):
    def get(self):
        global s
        if s != None:
            return s.getGlucosa()
        else:
            return False
    def put(self):
        global s
        print('Hace un put con dato: ', file=sys.stdout)
        print(str(request.form['data']),file=sys.stdout)
        return s.setGlucosa(request.form['data'])
        
class ArrancaHilo(Resource):
    def get(self):
        global s
#        print("Tipo de S: " + str(type(s)), file=sys.stdout)
        s = Simulador()
        return s.arrancarSimulador()
        
class ParaHilo(Resource):
    def get(self):
        global s
        if s != None:
#            print("Tipo de S: " + str(type(s)), file=sys.stdout)
#            print("ParaHilo: S no es none por tanto paro y borro", file=sys.stdout)
            return s.pararSimulador()
            del s
            s = None
        else:
            return False
        
class PausaHilo(Resource):
    def get(self):
        global s
        if s != None:
            return s.pausarSimulador()
        else:
            return False
        
class DespausaHilo(Resource):
    def get(self):
        global s
        if s != None:
            return s.despausarSimulador()
        else:
            return False
        
class DatosSimulacion(Resource):
    def get(self):
        global s
        return s.getDatosSimulacion()
    def put(self):
        global s
        content = request.form['data']
        print(content, file=sys.stdout)
        jsoncont = json.loads(content.replace("'", "\""))
        if s != None:
            return s.setDatosSimulacion(jsoncont)
        else:
            return False
        
class EstadoHilo(Resource):
    def get(self):
        global s
#        print("Tipo de S: " + str(type(s)), file=sys.stdout)
        if s == None:
            return "PARADO"
        else:
            return s.getEstadoHilo()

api.add_resource(HelloWorld, '/')
api.add_resource(ArrancaHilo, '/ArrancaHilo/')
api.add_resource(ParaHilo, '/ParaHilo/')
api.add_resource(PausaHilo, '/PausaHilo/')
api.add_resource(DespausaHilo, '/DespausaHilo/')
api.add_resource(ModoSimulador, '/ModoSimulador/')
api.add_resource(Glucosa, '/Glucosa/')
api.add_resource(DatosSimulacion, '/DatosSimulacion/')
api.add_resource(EstadoHilo, '/EstadoHilo/')

if __name__ == '__main__':
    # Debug/Development
    app.run(host="0.0.0.0", port=80, debug=True)
    #http_server = WSGIServer(('', 80), app)
    #http_server.serve_forever()
