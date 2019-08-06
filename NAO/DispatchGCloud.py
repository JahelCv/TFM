# -*- coding: utf-8 -*-
from google.cloud import pubsub_v1

class DispatchGCloud(object):
    def __init__(self, ac):
        self.acNAO = ac

        # Crea cliente de Pub/Sub
        self.subscriber = pubsub_v1.SubscriberClient()
        
        # Nombre del proyecto GCloud
        project_id = "servernao"
        project_path = self.subscriber.project_path(project_id)
        
        # Topics a los que se subscribe
        topic_decir = "naodecir"
        topic_exacpalabra = "naoexacpalabra"
        topic_hilos = "naohilos"
        topic_leds = "naoleds"
        topic_mover = "naomover"
        
        # Nombres de subscripciones
        sub_decir = "subnaodecir"
        sub_exacpalabra = "subnaoexacpalabra"
        sub_hilos = "subnaohilos"
        sub_leds = "subnaoleds"
        sub_mover = "subnaomover"

        # Rutas completas de las subscripciones
        subpath_decir = self.subscriber.subscription_path(self.project_id, sub_decir)
        subpath_exacpalabra = self.subscriber.subscription_path(self.project_id, sub_exacpalabra)
        subpath_hilos = self.subscriber.subscription_path(self.project_id, sub_hilos)
        subpath_leds = self.subscriber.subscription_path(self.project_id, sub_leds)
        subpath_mover = self.subscriber.subscription_path(self.project_id, sub_mover)
        
        dictsub = {'topic' : [topic_decir, topic_exacpalabra, topic_hilos, topic_leds, topic_mover],
                   'subname': [sub_decir, sub_exacpalabra, sub_hilos, sub_leds, sub_mover],
                   'subpath': [subpath_decir, subpath_exacpalabra, subpath_hilos, subpath_leds, subpath_mover]}
#        lsub = [subpath_decir, subpath_exacpalabra, subpath_hilos, subpath_leds, subpath_mover]
        
        # Listamos las subscripciones actuales y si no estan creadas, las creamos
        lcreatedsubs = self.subscriber.list_subscriptions(project_path)
        
        for i in range(0,dictsub['subpath'].len()):
            if dictsub['subpath'][i] in lcreatedsubs:
                pass
            else:
                topic_path = self.subscriber.topic_path(project_id, dictsub['topic'][i])
                self.subscriber.create_subscription(dictsub['subpath'][i], topic_path)
                
        self.subscriber.subscribe(subpath_decir, callback=self.callbackDecir)
        self.subscriber.subscribe(subpath_exacpalabra, callback=self.callbackExacpalabra)
        self.subscriber.subscribe(subpath_hilos, callback=self.callbackHilos)
        self.subscriber.subscribe(subpath_leds, callback=self.callbackLeds)
        self.subscriber.subscribe(subpath_mover, callback=self.callbackMover)
        """for sub in lsub:
            if sub in lcreatedsubs:
                pass
            else:
                self.subscriber.create_subscription(sub, topic_path)"""
    
    def callbackDecir(self, message):
        print('callbackDecir # Received message, data: ' + message.data)
        message.ack()
        
    def callbackExacpalabra(self, message):
        print('callbackExacpalabra # Received message, data: ' + message.data)
        message.ack()
    
    def callbackHilos(self, message):
        print('callbackHilos # Received message, data: ' + message.data)
        message.ack()
        
    def callbackLeds(self, message):
        print('callbackLeds # Received message, data: ' + message.data)
        message.ack()
        
    def callbackMover(self, message):
        print('callbackMover # Received message, data: ' + message.data)
        message.ack()
        
    def setDatosCompartidos(self, d):
        self.datos = d
        
    def setAccionesNAO(self, ac):
        self.acNAO = ac