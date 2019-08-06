# -*- coding: utf-8 -*-
import time
from google.cloud import pubsub_v1

project_id = "servernao"
subscription_name = "escenariosub"
topic_name = "escenario"

subscriber = pubsub_v1.SubscriberClient()
# The `subscription_path` method creates a fully qualified identifier
# in the form `projects/{project_id}/subscriptions/{subscription_name}`
subscription_path = subscriber.subscription_path(project_id, subscription_name)

def existsSubscriber(subs):
    project_path = subscriber.project_path(project_id)
    for subscription in subscriber.list_subscriptions(project_path):
        if subscription.name == subs:
            print 'Ya existe la suscripcion: ' + str(subscription.name)            
            return True
    return False
    
def createSubscriber(subs):
    topic_path = subscriber.topic_path(project_id, topic_name)
    subscription = subscriber.create_subscription(subs, topic_path)
    print('Subscription created: {}'.format(subscription))    
    
def deleteSubscriber(subs):
    subscriber.delete_subscription(subs)
    print('Subscription deleted: {}'.format(subscription_path))

def callback(message):
    print('Received message, data: ' + message.data)
    message.ack()

# "Main"
#if existsSubscriber(subscription_path):
#    deleteSubscriber(subscription_path)
#    createSubscriber(subscription_path)
#else:
#    createSubscriber(subscription_path)
    
subscriber.subscribe(subscription_path, callback=callback)

# The subscriber is non-blocking. We must keep the main thread from
# exiting to allow it to process messages asynchronously in the background.
print('Listening for messages on {}'.format(subscription_path))
while True:
    time.sleep(60)