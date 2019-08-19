package thread;



import java.util.Vector;

import nao.ConectaGCloud;
import nao.HiloServidor;
import ventanas.VentanaControl;
import ventanas.VentanaEscenario;
import ventanas.VentanaVisualizacion;

public class Manager extends Thread{
	
	private VentanaControl vControl;
	private VentanaVisualizacion vVisualizacion;
	private ConectaGCloud gcloud;
	private VentanaEscenario vEscenario;
	
	private Vector<HiloServidor> hilosNao = new Vector<HiloServidor>();
	private boolean parar;
	
	
	
	public Manager(VentanaControl vControl, VentanaVisualizacion vVisualizacion, ConectaGCloud gcloud) {
		
		
		this.vControl = vControl;
		this.vVisualizacion = vVisualizacion;
		this.gcloud = gcloud;
		this.parar = true; 
		this.vEscenario = new VentanaEscenario();
		
		// Damos de alta el hilo del simulador porque si ha respondido a la
		// primera llamada es que está en activo. Consultamos cómo está.
		// Posibles valores: "PARADO", "CORRIENDO", "PAUSADO"
		HiloServidor aux = new HiloServidor("SIMULACION");
		aux.setEstado(gcloud.GETEstadoHiloSimulador_GCE());
		hilosNao.add(aux);
		vControl.addEstadoHilos(hilosNao);
		
		vEscenario = new VentanaEscenario();
	}
	
	public void setDatosVentanaEscenario(String msg) {
		System.out.println("Manager # DE CALLBACK MQTT interfaz/ventanaescenario (setDatosVentanaEscenario): " + msg);
		vEscenario.addDatos(msg);
	}
	
	public synchronized void setHiloNAO(String id, String estado) {
		boolean actualizar = false;
		boolean encontrado = false;
		
		for(int i = 0; i < hilosNao.size(); i++) {
			HiloServidor aux = hilosNao.get(i);
			if (aux.getNombre().equals(id)) {
				encontrado = true;
				if (!aux.getEstado().equals(estado)) {
					hilosNao.get(i).setEstado(estado);
					actualizar = true;
				}
			}
		}
		
		// Si es un hilo nuevo (no se ha encontrado)
		if (!encontrado) {
			HiloServidor aux = new HiloServidor(id);
			if (aux.getNombre().equals("SIMULACION")) {
				aux.setEstado(gcloud.GETEstadoHiloSimulador_GCE());
			} else {
				aux.setEstado(estado);
			}
			hilosNao.add(aux);
			actualizar = true;
		}
		
		// Si hay que actualizar la lista
		if (actualizar) vControl.addEstadoHilos(hilosNao);
		System.out.println("DE CALLBACK (setHiloNAO) # ID Hilo: "+ id + " # Estado: " + estado
				+ " # Flag encontrado:" + encontrado + " Flag actualizar: " + actualizar);
	}
	
	public synchronized void checkHiloSimulador(String estado) {
		boolean actualizar = false;
		
		for(int i = 0; i < hilosNao.size(); i++) {
			HiloServidor aux = hilosNao.get(i);
			if (aux.getNombre().equals("SIMULACION")) {
				//System.out.println("Manager # checkHiloSimulador: Encuentra en lista al simulador con param estado: " + estado);
				if (!aux.getEstado().equals(estado)) {
					//System.out.println("Manager # checkHiloSimulador: Actualiza su estado en lista");
					hilosNao.get(i).setEstado(estado);
					actualizar = true;
				}
			}
		}
		
		if (actualizar) {
			vControl.addEstadoHilos(hilosNao);
			actualizar = false;
		}
	}
	
	@Override
	public void run() {
		while(parar){
			// Consultamos glucosa
			vVisualizacion.addDotGraf((float)gcloud.GETGlucosa_GCE());
			
			// Consultamos el estado del simulador y actualizamos si es diferente
			String estado = gcloud.GETEstadoHiloSimulador_GCE();
			this.checkHiloSimulador(estado);
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
	
	public void paraManager(){
		this.parar = false;
	}
}
