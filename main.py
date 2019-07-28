# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from flask import Flask, request, jsonify
from gevent.pywsgi import WSGIServer
from flask_restful import Resource, Api
from Simulador import Simulador
from threading import Thread

app = Flask(__name__)
api = Api(app)
s = Simulador()    

class HelloWorld(Resource):
    def get(self):
        return "Bienvenido!"
        
class ModoSimulador(Resource):
    def get(self):
        return s.getModo()
    def put(self):
        return s.setModo(request.form['data'])
        
class Glucosa(Resource):
    def get(self):
        return s.getGlucosa()
    def put(self):
        return s.setGlucosa(request.form['data'])
        
class ArrancaHilo(Resource):
    def get(self):
        t = Thread(target=s.run)
        t.start()
        return 'Ok'
        
class ParaHilo(Resource):
    def get(self):
        return s.pararSimulador()
        
class PausaHilo(Resource):
    def get(self):
        return s.pausarSimulador()
        
class DespausaHilo(Resource):
    def get(self):
        return s.despausarSimulador()
        
class DatosSimulacion(Resource):
    def get(self):
        return s.getDatosSimulacion()
    def put(self):
        content = request.json
        print(content, file=sys.stdout)
        s.setDatosSimulacion(content)
        return jsonify({"result":True})

api.add_resource(HelloWorld, '/')
api.add_resource(ArrancaHilo, '/ArrancaHilo/')
api.add_resource(ParaHilo, '/ParaHilo/')
api.add_resource(PausaHilo, '/PausaHilo/')
api.add_resource(DespausaHilo, '/DespausaHilo/')
api.add_resource(ModoSimulador, '/ModoSimulador/')
api.add_resource(Glucosa, '/Glucosa/')
api.add_resource(DatosSimulacion, '/DatosSimulacion/')

if __name__ == '__main__':
    # Debug/Development
#    app.run(host="0.0.0.0", port=80, debug=True)
    http_server = WSGIServer(('', 80), app)
    http_server.serve_forever()