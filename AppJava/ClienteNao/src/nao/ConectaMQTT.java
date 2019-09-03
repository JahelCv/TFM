package nao;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.eclipse.paho.client.mqttv3.MqttPersistenceException;

import thread.Manager;

public class ConectaMQTT implements MqttCallback{
	
	private MqttClient mqttc;
	private Manager m;
	
	public ConectaMQTT(Manager m) {
		this.m = m;
		try {
			mqttc = new MqttClient("tcp://34.76.240.69:1883", MqttClient.generateClientId());
			mqttc.setCallback(this);
			MqttConnectOptions connOpts = new MqttConnectOptions();
		    connOpts.setCleanSession(true);
		    connOpts.setUserName("nao");
		    connOpts.setPassword("nao".toCharArray());
			mqttc.connect(connOpts);
			String[] topicsubs = {"hilos","interfaz/ventanaescenario"};
			mqttc.subscribe(topicsubs);
			System.out.println("MQTT Conectado exitosamente");
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	@Override
	public void connectionLost(Throwable arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void deliveryComplete(IMqttDeliveryToken arg0) {
		// TODO Auto-generated method stub
		
	}

	@Override
	public void messageArrived(String topic, MqttMessage msg) throws Exception {
		System.out.println("Topic: "+ topic + " # Message: " + new String(msg.getPayload()));
		if (topic.equals("hilos")) {
			String[] msgsplitted = new String(msg.getPayload()).split(",");
			m.setHiloNAO(msgsplitted[0], msgsplitted[1]);
		} else if (topic.equals("interfaz/ventanaescenario")) {
			m.setDatosVentanaEscenario(new String(msg.getPayload()));
		}
		
	}
	
	/**
	 * FUNCIONES PARA MQTT
	 * 
	 * @param projectTopicName
	 */
	public void publishMessageNaoDecir(String message) {
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("nao/decir", mq);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	public void publishMessageNaoMover(String message) {
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("nao/mover", mq);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	public void publishMessageNaoHilos(String message) {
		System.out.println("ConectaMQTT # publishMessageNaoHilos(): " + message);
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("hilos", mq);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	public void publishMessageNaoLeds(String message) {
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("nao/leds", mq);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	public void publishMessageNaoExacpalabra(String message) {
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("nao/exacpalabra", mq);
		} catch (MqttPersistenceException e) {
			e.printStackTrace();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}

	public void desconectarMQTT() {
		try {
			mqttc.disconnect();
		} catch (MqttException e) {
			e.printStackTrace();
		}
	}
	
}
