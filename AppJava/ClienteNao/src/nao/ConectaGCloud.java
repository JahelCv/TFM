package nao;

import com.google.api.core.ApiFuture;
import com.google.cloud.pubsub.v1.AckReplyConsumer;
import com.google.cloud.pubsub.v1.MessageReceiver;
import com.google.cloud.pubsub.v1.Publisher;
import com.google.cloud.pubsub.v1.Subscriber;
import com.google.cloud.pubsub.v1.SubscriptionAdminClient;
import com.google.cloud.pubsub.v1.TopicAdminClient;
import com.google.cloud.pubsub.v1.TopicAdminClient.ListTopicSubscriptionsPagedResponse;
import com.google.cloud.pubsub.v1.TopicAdminClient.ListTopicsPagedResponse;
import com.google.protobuf.ByteString;
import com.google.pubsub.v1.ListTopicSubscriptionsRequest;
import com.google.pubsub.v1.ListTopicsRequest;
import com.google.pubsub.v1.ProjectName;
import com.google.pubsub.v1.ProjectSubscriptionName;
import com.google.pubsub.v1.ProjectTopicName;
import com.google.pubsub.v1.PubsubMessage;
import com.google.pubsub.v1.PushConfig;
import com.google.pubsub.v1.Subscription;
import com.google.pubsub.v1.Topic;

import ventanas.VentanaControl;
import ventanas.VentanaVisualizacion;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.UnsupportedEncodingException;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.ProtocolException;
import java.net.URL;
import java.net.URLEncoder;
import java.util.concurrent.TimeUnit;

import org.json.JSONArray;

public class ConectaGCloud {

	static String projectname = "servernao";

	// Topics para nao pub/sub
	static String topic_d = "naodecir";
	static String topic_m = "naomover";
	static String topic_h = "naohilos";
	static String topic_l = "naoleds";
	static String topic_e = "naoexacpalabra";
	static ProjectTopicName topic_naodecir = ProjectTopicName.of(projectname, topic_d);
	static ProjectTopicName topic_naomover = ProjectTopicName.of(projectname, topic_m);
	static ProjectTopicName topic_naohilos = ProjectTopicName.of(projectname, topic_h);
	static ProjectTopicName topic_naoleds = ProjectTopicName.of(projectname, topic_l);
	static ProjectTopicName topic_naoexacpalabra = ProjectTopicName.of(projectname, topic_e);

	// Rutas para el simulador del GCE
	String urlmod = "ModoSimulador/";
	String urlglu = "Glucosa/";
	String urlpara = "ParaHilo/";
	String urldats = "DatosSimulacion/";
	String urlarranca = "ArrancaHilo/";
	String urlpausa = "PausaHilo/";
	String urldespausa = "DespausaHilo/";
	String urlestadohilo = "EstadoHilo/";

	private String gce_rootip = null;

	private VentanaVisualizacion vv;
	private VentanaControl vc;

	Subscriber subscriber_esc = null;
	Subscriber subscriber_int = null;
	Subscriber subscriber_glu = null;
	Subscriber subscriber_hil = null;
	Subscriber subscriber_res = null;

	public ConectaGCloud(String ip) {
		// Verifica que existen los topics
		if (!this.existsTopic(topic_naodecir)) {
			this.createTopic(topic_naodecir);
		}
		if (!this.existsTopic(topic_naomover)) {
			this.createTopic(topic_naomover);
		}
		if (!this.existsTopic(topic_naohilos)) {
			this.createTopic(topic_naohilos);
		}
		if (!this.existsTopic(topic_naoleds)) {
			this.createTopic(topic_naoleds);
		}
		if (!this.existsTopic(topic_naoexacpalabra)) {
			this.createTopic(topic_naoexacpalabra);
		}
		// Verifica que existen las subscripciones
		/*
		 * if (!this.existsSubscription(topicescenario, "escenariosub")) {
		 * this.createSubscription(topicescenario, "escenariosub"); } if
		 * (!this.existsSubscription(topicinteraccion, "interaccionsub")) {
		 * this.createSubscription(topicinteraccion, "interaccionsub"); } if
		 * (!this.existsSubscription(topicglucosa, "glucosasub")) {
		 * this.createSubscription(topicglucosa, "glucosasub"); } if
		 * (!this.existsSubscription(topichilos, "hilossub")) {
		 * this.createSubscription(topichilos, "hilossub"); } if
		 * (!this.existsSubscription(topicres, "ressub")) {
		 * this.createSubscription(topicres, "ressub"); } if
		 * (!this.existsSubscription(topicacciones, "accionessub")) {
		 * this.createSubscription(topicacciones, "accionessub"); }
		 */
		// Establece la IP de la máquina virtual
		gce_rootip = "http://" + ip + ":80/";
		urlmod = gce_rootip + urlmod;
		urlglu = gce_rootip + urlglu;
		urlpara = gce_rootip + urlpara;
		urldats = gce_rootip + urldats;
		urlarranca = gce_rootip + urlarranca;
		urlpausa = gce_rootip + urlpausa;
		urldespausa = gce_rootip + urldespausa;
		urlestadohilo = gce_rootip + urlestadohilo;
	}

	public void setVentanaVisualizacion(VentanaVisualizacion v) {
		this.vv = v;
	}

	public void setVentanaControl(VentanaControl v) {
		this.vc = v;
	}

	/**
	 * FUNCIONES PARA GOOGLE PUB/SUB
	 * 
	 * @param projectTopicName
	 */
	public void createTopic(ProjectTopicName projectTopicName) {
		try (TopicAdminClient topicAdminClient = TopicAdminClient.create()) {
			topicAdminClient.createTopic(projectTopicName);
		} catch (Exception e) {
			System.err.println("Error al crear un topic: " + e.toString());
		}
	}

	public boolean existsTopic(ProjectTopicName projectTopicName) {
		try (TopicAdminClient topicAdminClient = TopicAdminClient.create()) {
			ListTopicsRequest listTopicsRequest = ListTopicsRequest.newBuilder()
					.setProject(ProjectName.format(projectname)).build();
			ListTopicsPagedResponse response = topicAdminClient.listTopics(listTopicsRequest);
			Iterable<Topic> topics = response.iterateAll();
			for (Topic topic : topics) {
				if (topic.getName().equals(projectTopicName.toString())) {
					return true;
				}
			}
		} catch (Exception e) {
			System.err.println("Error al listar topics: " + e.toString());
		}
		return false;
	}

	/**
	 * Publish message to pub/sub en topic naodecir
	 * 
	 * @param message
	 * @return
	 */
	public String publishMessageNaoDecir(String message) {
		Publisher publisher = null;
		String ret = null;

		try {
			publisher = Publisher.newBuilder(topic_naodecir).build();
			ByteString data = ByteString.copyFromUtf8(message);
			PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
			ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
			// System.out.println("published with message ID: " + messageIdFuture.get());
			ret = messageIdFuture.get();
		} catch (Exception e) {
			// System.err.println("Error al publicar mensaje: " + e.toString());
			e.printStackTrace();
			ret = null;
		}
		if (publisher != null) {
			// When finished with the publisher, shutdown to free up resources.
			publisher.shutdown();
			try {
				publisher.awaitTermination(1, TimeUnit.MINUTES);
			} catch (InterruptedException e) {
				e.printStackTrace();
				ret = null;
			}
		}
		return ret;
	}

	public String publishMessageNaoMover(String message) {
		Publisher publisher = null;
		String ret = null;
		try {
			publisher = Publisher.newBuilder(topic_naomover).build();
			ByteString data = ByteString.copyFromUtf8(message);
			PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
			ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
			// System.out.println("published with message ID: " + messageIdFuture.get());
			ret = messageIdFuture.get();
		} catch (Exception e) {
			System.err.println("Error al publicar mensaje: " + e.toString());
			ret = null;
		}
		if (publisher != null) {
			// When finished with the publisher, shutdown to free up resources.
			publisher.shutdown();
			try {
				publisher.awaitTermination(1, TimeUnit.MINUTES);
			} catch (InterruptedException e) {
				e.printStackTrace();
				ret = null;
			}
		}
		return ret;
	}

	public String publishMessageNaoHilos(String message) {
		Publisher publisher = null;
		String ret = null;
		try {
			publisher = Publisher.newBuilder(topic_naohilos).build();
			ByteString data = ByteString.copyFromUtf8(message);
			PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
			ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
			// System.out.println("published with message ID: " + messageIdFuture.get());
			ret = messageIdFuture.get();
		} catch (Exception e) {
			System.err.println("Error al publicar mensaje: " + e.toString());
			ret = null;
		}
		if (publisher != null) {
			// When finished with the publisher, shutdown to free up resources.
			publisher.shutdown();
			try {
				publisher.awaitTermination(1, TimeUnit.MINUTES);
			} catch (InterruptedException e) {
				e.printStackTrace();
				ret = null;
			}
		}
		return ret;
	}

	public String publishMessageNaoLeds(String message) {
		Publisher publisher = null;
		String ret = null;
		try {
			publisher = Publisher.newBuilder(topic_naoleds).build();
			ByteString data = ByteString.copyFromUtf8(message);
			PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
			ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
			// System.out.println("published with message ID: " + messageIdFuture.get());
			ret = messageIdFuture.get();
		} catch (Exception e) {
			System.err.println("Error al publicar mensaje: " + e.toString());
			ret = null;
		}
		if (publisher != null) {
			// When finished with the publisher, shutdown to free up resources.
			publisher.shutdown();
			try {
				publisher.awaitTermination(1, TimeUnit.MINUTES);
			} catch (InterruptedException e) {
				e.printStackTrace();
				ret = null;
			}
		}
		return ret;
	}

	public String publishMessageNaoExacpalabra(String message) {
		Publisher publisher = null;
		String ret = null;
		try {
			publisher = Publisher.newBuilder(topic_naoexacpalabra).build();
			ByteString data = ByteString.copyFromUtf8(message);
			PubsubMessage pubsubMessage = PubsubMessage.newBuilder().setData(data).build();
			ApiFuture<String> messageIdFuture = publisher.publish(pubsubMessage);
			// System.out.println("published with message ID: " + messageIdFuture.get());
			ret = messageIdFuture.get();
		} catch (Exception e) {
			System.err.println("Error al publicar mensaje: " + e.toString());
			ret = null;
		}
		if (publisher != null) {
			// When finished with the publisher, shutdown to free up resources.
			publisher.shutdown();
			try {
				publisher.awaitTermination(1, TimeUnit.MINUTES);
			} catch (InterruptedException e) {
				e.printStackTrace();
				ret = null;
			}
		}
		return ret;
	}

	public boolean existsSubscription(ProjectTopicName topicName, String subscriptionId) {
		String subscriptionId_s = (ProjectSubscriptionName.of(projectname, subscriptionId)).toString();
		try (TopicAdminClient topicAdminClient = TopicAdminClient.create()) {
			ListTopicSubscriptionsRequest request = ListTopicSubscriptionsRequest.newBuilder()
					.setTopic(topicName.toString()).build();
			ListTopicSubscriptionsPagedResponse response = topicAdminClient.listTopicSubscriptions(request);
			Iterable<String> subscriptionNames = response.iterateAll();
			for (String subscriptionName : subscriptionNames) {
				// System.out.println("exists subscription: " + subscriptionName);
				if (subscriptionId_s.equals(subscriptionName))
					return true;
			}
			return false;
		} catch (IOException e) {
			e.printStackTrace();
			return false;
		}
	}

	public Subscription createSubscription(ProjectTopicName topicName, String subscriptionId) {
		try (SubscriptionAdminClient subscriptionAdminClient = SubscriptionAdminClient.create()) {
			ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subscriptionId);
			// create a pull subscription with default acknowledgement deadline
			return subscriptionAdminClient.createSubscription(subscriptionName, topicName,
					PushConfig.getDefaultInstance(), 0);
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
	}

	public void subscribeEscenario(String subs) {
		ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subs);
		MessageReceiver receiver = new MessageReceiver() {
			@Override
			public void receiveMessage(PubsubMessage message, AckReplyConsumer consumer) {
				// handle incoming message, then ack/nack the received message
				System.out.println("Id : " + message.getMessageId());
				System.out.println("Data : " + message.getData().toStringUtf8());
				consumer.ack();
			}
		};
		subscriber_esc = Subscriber.newBuilder(subscriptionName, receiver).build();
		subscriber_esc.startAsync();
	}

	public void subscribeInteraccion(String subs) {
		ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subs);
		MessageReceiver receiver = new MessageReceiver() {
			@Override
			public void receiveMessage(PubsubMessage message, AckReplyConsumer consumer) {
				// handle incoming message, then ack/nack the received message
				System.out.println("Id : " + message.getMessageId());
				System.out.println("Data : " + message.getData().toStringUtf8());
				consumer.ack();
			}
		};
		subscriber_int = Subscriber.newBuilder(subscriptionName, receiver).build();
		subscriber_int.startAsync();
	}

	public void subscribeGlucosa(String subs) {
		ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subs);
		MessageReceiver receiver = new MessageReceiver() {
			@Override
			public void receiveMessage(PubsubMessage message, AckReplyConsumer consumer) {
				// handle incoming message, then ack/nack the received message
				System.out.println("Id : " + message.getMessageId());
				System.out.println("Data : " + message.getData().toStringUtf8());
				consumer.ack();
				vv.addDotGraf(Float.parseFloat(message.getData().toStringUtf8()));
			}
		};
		subscriber_glu = Subscriber.newBuilder(subscriptionName, receiver).build();
		subscriber_glu.startAsync();
	}

	public void subscribeHilos(String subs) {
		ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subs);
		MessageReceiver receiver = new MessageReceiver() {
			@Override
			public void receiveMessage(PubsubMessage message, AckReplyConsumer consumer) {
				// handle incoming message, then ack/nack the received message
				System.out.println("# subscribeHilos # Id : " + message.getMessageId());
				System.out.println("# subscribeHilos # Data : " + message.getData().toStringUtf8());
				consumer.ack();
				// TODO: procesarHilosServidor (Manager)
			}
		};
		subscriber_hil = Subscriber.newBuilder(subscriptionName, receiver).build();
		subscriber_hil.startAsync();
	}

	public void subscribeRes(String subs) {
		ProjectSubscriptionName subscriptionName = ProjectSubscriptionName.of(projectname, subs);
		MessageReceiver receiver = new MessageReceiver() {
			@Override
			public void receiveMessage(PubsubMessage message, AckReplyConsumer consumer) {
				// handle incoming message, then ack/nack the received message
				System.out.println("Id : " + message.getMessageId());
				System.out.println("Data : " + message.getData().toStringUtf8());
				consumer.ack();
				vc.addTextPane(message.getData().toStringUtf8());
			}
		};
		subscriber_res = Subscriber.newBuilder(subscriptionName, receiver).build();
		subscriber_res.startAsync();
	}

	/**
	 * Operaciones sobre el simulador Google Compute Engine
	 * 
	 * @return
	 */
	public boolean verificaConexionGCE() {
		HttpURLConnection con = null;
		boolean ret = false;
		try {
			URL url = new URL(gce_rootip);
			con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				content.append(inputLine);
			}
			in.close();
			System.out.println("Recibido de " + gce_rootip + ": " + content);
			// Si contiene algo, que devuelva true
			if (content.length() > 0) {
				ret = true;
			}
			con.disconnect();
		} catch (ConnectException e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		}
		return ret;
	}

	public boolean GETArranca_GCE() {
		return this.simpleGET(urlarranca);
	}

	public boolean GETPara_GCE() {
		return this.simpleGET(urlpara);
	}

	public boolean GETPausa_GCE() {
		return this.simpleGET(urlpausa);
	}

	public boolean GETDespausa_GCE() {
		return this.simpleGET(urldespausa);
	}

	public boolean simpleGET(String urlp) {
		HttpURLConnection con = null;
		boolean ret = false;
		try {
			URL url = new URL(urlp);
			con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				content.append(inputLine);
			}
			in.close();

			System.out.println("Recibido de " + gce_rootip + ": " + content);
			System.out.println("Codigo respuesta de PUT: " + con.getResponseCode());

			con.disconnect();
			ret = true;
		} catch (ConnectException e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		}
		return ret;
	}

	public double GETGlucosa_GCE() {
		HttpURLConnection con = null;
		double ret = 0;
		try {
			URL url = new URL(urlglu);
			con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				content.append(inputLine);
			}
			in.close();
			// System.out.println("Recibido de " + urlglu + ": " + content);
			// Si contiene algo, que devuelva true
			if (content.length() > 0) {
				ret = Double.parseDouble(content.toString());
			}
			con.disconnect();
		} catch (ConnectException e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		}
		return ret;
	}
	
	public String GETEstadoHiloSimulador_GCE() {
		HttpURLConnection con = null;
		String ret = null;
		try {
			URL url = new URL(urlestadohilo);
			con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				content.append(inputLine);
			}
			in.close();
			// System.out.println("Recibido de " + urlestadohilo + ": " + content);
			// Si contiene algo, que devuelva true
			if (content.length() > 0) {
				ret = content.toString();
			}
			con.disconnect();
		} catch (ConnectException e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		} catch (Exception e) {
			e.printStackTrace();
			if (con != null)
				con.disconnect();
		}
		return ret;
	}

	public boolean PUTSimulationParams_GCE(double bolus, double cho, boolean ejer, double ejerT, double ejerD,
			double ejerI) {
		HttpURLConnection httpCon = null;
		boolean ret = false;
		String urlParameters = "";
		String json = "{\'bolus\' : "+bolus+", \'cho\' : "+cho+", \'ejercicio\' :"+ejer
						+", \'exercise\' : ["+ejerT+","+ejerD+","+ejerI+"]}";
		//String json = "{\'bolus\' : "+bolus+", \'cho\' : "+cho+", \'ejercicio\' : "+ejer+"}";
		/*String json = "{ \"data\": { \"bolus\" : " + bolus + ", \"cho\" : " + cho + ", \"ejercicio\" : " + aux
				+ ", \"exercise\" : [" + ejerT + "," + ejerD + "," + ejerI + "]}}";*/
		try {
			urlParameters = "data=" + URLEncoder.encode(json, "UTF-8");
			URL url = new URL(urldats);
			httpCon = (HttpURLConnection) url.openConnection();
			httpCon.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
			httpCon.setRequestProperty("Content-Length", "" + Integer.toString(urlParameters.getBytes().length));
			httpCon.setDoOutput(true);
			httpCon.setDoInput(true);
			httpCon.setUseCaches(false);
			httpCon.setRequestMethod("PUT");

			// Send request
			DataOutputStream wr = new DataOutputStream(httpCon.getOutputStream());
			wr.writeBytes(urlParameters);
			wr.flush();
			wr.close();

			// Get response
			InputStream is = httpCon.getInputStream();
			BufferedReader rd = new BufferedReader(new InputStreamReader(is));
			String line;
			StringBuffer response = new StringBuffer();
			while ((line = rd.readLine()) != null) {
				response.append(line);
				response.append('\r');
			}
			rd.close();
			System.out.println("Respuesta de Flask: " + response.toString());
			System.out.println("Codigo respuesta de PUT: " + httpCon.getResponseCode());
			httpCon.disconnect();
			ret = true;

		} catch (UnsupportedEncodingException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return ret;
	}

	public boolean PUTSimulationMode_GCE(String s) {
		boolean ret = false;
		String urlParameters = "";
		HttpURLConnection httpCon = null;
		try {
			urlParameters = "data=" + URLEncoder.encode(s, "UTF-8");
			System.out.println("URL a enviar: " + urlmod);
			URL url = new URL(urlmod);
			httpCon = (HttpURLConnection) url.openConnection();
			httpCon.setRequestProperty("Content-Type", "application/x-www-form-urlencoded");
			httpCon.setRequestProperty("Content-Length", "" + Integer.toString(urlParameters.getBytes().length));
			httpCon.setDoOutput(true);
			httpCon.setDoInput(true);
			httpCon.setUseCaches(false);
			httpCon.setRequestMethod("PUT");

			// Send request
			DataOutputStream wr = new DataOutputStream(httpCon.getOutputStream());
			wr.writeBytes(urlParameters);
			wr.flush();
			wr.close();

			// Get response
			InputStream is = httpCon.getInputStream();
			BufferedReader rd = new BufferedReader(new InputStreamReader(is));
			String line;
			StringBuffer response = new StringBuffer();
			while ((line = rd.readLine()) != null) {
				response.append(line);
				response.append('\r');
			}
			rd.close();
			System.out.println("Respuesta de Flask: " + response.toString());
			System.out.println("Codigo respuesta de PUT: " + httpCon.getResponseCode());
			httpCon.disconnect();
			ret = true;

		} catch (UnsupportedEncodingException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

		return ret;
	}
}