package nao;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.ConnectException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;

public class ConectaGCloud {

	// Rutas para el simulador del GCE
	String urlmod = "Simulador/Modo/";
	String urlglu = "Simulador/Glucosa/";
	String urldats = "Simulador/DatosSimulacion/";
	String urlhilo = "Hilo/";
	private String gce_rootip = null;
	
	public ConectaGCloud(String ip) {
		gce_rootip = "http://" + ip + ":8080/";
		urlmod = gce_rootip + urlmod;
		urlglu = gce_rootip + urlglu;
		urldats = gce_rootip + urldats;
		urlhilo = gce_rootip + urlhilo;

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

	public boolean PUTArranca_GCE() {
		return this.simplePUT("CORRIENDO");
	}

	public boolean PUTPara_GCE() {
		return this.simplePUT("PARADO");
	}

	public boolean PUTPausa_GCE() {
		return this.simplePUT("PAUSADO");
	}

	public boolean PUTDespausa_GCE() {
		return this.simplePUT("CORRIENDO");
	}

	public boolean simplePUT(String s) {
		System.out.println("Inicia PUT a HILO");
		boolean ret = false;
		String urlParameters = "";
		HttpURLConnection httpCon = null;
		try {
			urlParameters = "data=" + URLEncoder.encode(s, "UTF-8");
			URL url = new URL(urlhilo);
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
			/*System.out.println("Respuesta de Flask: " + response.toString());
			System.out.println("Codigo respuesta de PUT: " + httpCon.getResponseCode());*/
			httpCon.disconnect();
			ret = true;
			System.out.println("Termina PUT a HILO");

		} catch (UnsupportedEncodingException e1) {
			e1.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
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
				try {
					ret = Double.parseDouble(content.toString());
				} catch (NumberFormatException e) {
					ret = -1000;
				}
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
			URL url = new URL(urlhilo);
			con = (HttpURLConnection) url.openConnection();
			con.setRequestMethod("GET");
			BufferedReader in = new BufferedReader(new InputStreamReader(con.getInputStream()));
			String inputLine;
			StringBuffer content = new StringBuffer();
			while ((inputLine = in.readLine()) != null) {
				//System.out.println("Recibido de " + urlestadohilo + ": " + inputLine);
				content.append(inputLine);
			}
			in.close();
			// System.out.println("Recibido de " + urlestadohilo + ": " + content);
			// Si contiene algo, que devuelva true
			if (content.length() > 0) {
				ret = content.toString();
				ret = ret.replace("\"", "");
				//System.out.println("Manager # GETEstadoHiloSimulador_GCE: Recibido de " + urlestadohilo + ": " + ret);
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
		String json = "{\'bolus\' : " + bolus + ", \'cho\' : " + cho + ", \'ejercicio\' :" + ejer + ", \'exercise\' : ["
				+ ejerT + "," + ejerD + "," + ejerI + "]}";
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