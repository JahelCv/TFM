package nao;

public class HiloServidor {

	private String nombre;
	private String estado;
	private boolean excluyente;
	

	public HiloServidor(String nombre){
		this.nombre = nombre;
		this.excluyente = false;
	}
	
	public boolean isExcluyente() {
		return excluyente;
	}


	public void setExcluyente(boolean excluyente) {
		this.excluyente = excluyente;
	}
	
	public String getNombre() {
		return nombre;
	}

	public String getEstado() {
		return estado;
	}


	public void setEstado(String string) {
		this.estado = string;
	}
	
	@Override
	public boolean equals(Object v) {

		HiloServidor aux = (HiloServidor) v;

		if(this.nombre.equals(aux.getNombre()))
			return true;
		
		return false;
	}
	
	@Override
	public String toString() {
		if(excluyente){
			return " + "+nombre;
		} else {
			return "   "+nombre;
	    }
	}
}
