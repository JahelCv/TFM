package nao;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttClient;
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
			mqttc = new MqttClient("tcp://iot.eclipse.org:1883", "PublicadorJava");
			System.out.println("Crea mqtt object");
			mqttc.setCallback(this);
			mqttc.connect();
			mqttc.subscribe("interfaz/hilos");
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
	public void messageArrived(String arg0, MqttMessage msg) throws Exception {
		//System.out.println("Topic: "+ arg0 + " # Message: " + arg1);
		String[] msgsplitted = new String(msg.getPayload()).split(",");
		m.setHiloNAO(msgsplitted[0], msgsplitted[1]);
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
		MqttMessage mq = new MqttMessage();
		mq.setPayload(message.getBytes());
		try {
			mqttc.publish("nao/hilos", mq);
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
