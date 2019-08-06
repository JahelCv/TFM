package thread;


import java.util.Vector;

import nao.ClienteTCP;
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
		
		// Damos de alta el hilo del simulador porque si ha respondido a la
		// primera llamada es que está en activo. Consultamos cómo está.
		// Posibles valores: "PARADO", "CORRIENDO", "PAUSADO"
		HiloServidor aux = new HiloServidor("SIMULACION");
		aux.setEstado(gcloud.GETEstadoHiloSimulador_GCE());
		hilosNao.add(aux);
		vControl.addEstadoHilos(hilosNao);
		
		vEscenario = new VentanaEscenario();
	}
	
	@Override
	public void run() {
		while(parar){
			// Consultamos glucosa
			vVisualizacion.addDotGraf((float)gcloud.GETGlucosa_GCE());
			
			// Consultamos el estado del simulador y actualizamos si es diferente
			String estado = gcloud.GETEstadoHiloSimulador_GCE();
			boolean actualizar = false;
			for(int i = 0; i < hilosNao.size(); i++) {
				HiloServidor aux = hilosNao.get(i);
				// Si encontramos a simulador...
				if (aux.getNombre().equals("SIMULADOR")) {
					// Y su estado no es como lo consultamos en HTTP...
					if (!aux.getEstado().equals(estado)) {
						// System.out.println("Estado de GCE: " + estado + " # Estado de aux: " + aux.getEstado());
						hilosNao.get(i).setEstado(estado);
						actualizar = true;
					}
				}
			}
			
			if (actualizar) {
				// System.out.println("Refresca ventana de control");
				vControl.addEstadoHilos(hilosNao);
				actualizar = false;
			}
			
			try {
				Thread.sleep(1000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
		
	}

	/*@Override
	public void run() {
		String comando;

		while(parar){
			comando = cliente.read();
			System.out.println(comando);
			if(comando == null)
				return;
			vControl.addStringRecivido(comando);
			comando = comando.substring(0, comando.length()-1);
			String[] parts1 = comando.split("#");
			if(parts1.length != 2)
				continue;
			
			if (parts1[0].compareTo("PER") == 0) {
				String[] parts = parts1[1].split("/");
				
				for (int i = 0; i < parts.length; i++) {
					String[] partes = parts[i].split("~");
					if(partes.length != 2)
						continue;
					if (partes[0].compareTo("GLUCOSA") == 0) {
						vVisualizacion.addDotGraf(Float.parseFloat(partes[1]));
					}
					
					if (partes[0].compareTo("ESTADOHILOS") == 0) {
							procesarHilosServidor(partes[1]);
					}
					if (partes[0].compareTo("ESCENARIO") == 0) {
						vEscenario.addDatos(partes[1]);
					}
				}

			}
			
			if(parts1[0].compareTo("RES") == 0){
				vControl.addTextPane(parts1[1]);
			}


		}
		
	}*/
	
	/*private void procesarHilosServidor(String hilos){
		boolean update = false;

		//separamos hilos excluyentes de los no excluyentes
		String[] hilosTipo = hilos.split("%");

		
		String[] parts = hilosTipo[0].split(",");
		for (int i = 0; i< parts.length; i++) {
			String[] split = parts[i].split(":");
			HiloServidor aux = new HiloServidor(split[0]);
			aux.setEstado(Integer.parseInt(split[1]));
			
			//mirar si es hilo nuevo o no, si ya existe actualizar estado si es necesario
			if(hilosNao.contains(aux)){
				if( hilosNao.get(hilosNao.indexOf(aux)).getEstado() != aux.getEstado() ){
					hilosNao.get(hilosNao.indexOf(aux)).setEstado(aux.getEstado());	
					update = true;
				}
			} else {
				hilosNao.add(aux);
				update = true;
			}			
		}
		
		if(hilosTipo.length == 2){
			String[] parts1 = hilosTipo[1].split(",");
			for (int i = 0; i< parts1.length; i++) {
				String[] split = parts1[i].split(":");
				HiloServidor aux1 = new HiloServidor(split[0]);
				aux1.setEstado(Integer.parseInt(split[1]));
				aux1.setExcluyente(true);
				//mirar si es hilo nuevo o no, si ya existe actualizar estado si es necesario
				if(hilosNao.contains(aux1)){
					if( hilosNao.get(hilosNao.indexOf(aux1)).getEstado() != aux1.getEstado() ){
						hilosNao.get(hilosNao.indexOf(aux1)).setEstado(aux1.getEstado());	
						update = true;
					}
				} else {
					hilosNao.add(aux1);
					update = true;
				}			
			}
		}
		
		if(update == true)
			vControl.addEstadoHilos(hilosNao);
	}*/
	
	public void paraManager(){
		this.parar = false;
	}
}
