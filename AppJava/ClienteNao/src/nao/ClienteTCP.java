package nao;

import java.io.BufferedReader;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.ConnectException;
import java.net.Socket;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class ClienteTCP{

	private Socket clientSocket;
	private String ipServer;
	private int puertoServer;
	
	private static final String IPADDRESS_PATTERN =
			"^([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
			"([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
			"([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\." +
			"([01]?\\d\\d?|2[0-4]\\d|25[0-5])$";
	
	
	public static boolean validateIP(final String ip) {
		Pattern pattern;
		Matcher matcher;
		pattern = Pattern.compile(IPADDRESS_PATTERN);
		matcher = pattern.matcher(ip);
		return matcher.matches();
	}
	
	public ClienteTCP(String _ipServer, int _puertoServer) {
		this.ipServer = _ipServer;
		this.puertoServer = _puertoServer;
	}

	public int checkServer(){
		 try {
			DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
			outToServer.writeBytes("ping");
		} catch (IOException e) {
			e.printStackTrace();
			return -1;
		}
		 
		return 1;
	}
	
	public int conectar(){
		
		try {
			clientSocket = new Socket(ipServer, puertoServer);
			String respuesta = read();
			if(respuesta.equals("error"))
				return -2;
			return 1;
		} catch (ConnectException e) {
			return -1;
		} catch (IOException e) {
			return -1;
		}
		
	}
	
	public String read(){
		BufferedReader br = null;
	    String total = "";
		try {
			br = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));
		    while ( total.endsWith(";") == false) 
		    { 
		    	
		        int c = br.read(); 
		        if(c == -1) {
		        	System.out.println(total);
		        	return "error"; 
		        }
		        total += (char)c;
		    }
		    //System.out.println(total);
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		return total;
	}
	
	public void send(String msg){
		DataOutputStream outToClient;
		try {
			outToClient = new DataOutputStream(clientSocket.getOutputStream());
			outToClient.writeBytes(msg);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}
	
	public void cerrarSocket(){
		try {
			clientSocket.close();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
}
