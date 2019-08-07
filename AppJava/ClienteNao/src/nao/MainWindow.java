package nao;

import java.awt.EventQueue;
import javax.swing.JFrame;
import javax.swing.JTextField;
import thread.Manager;
import javax.swing.JButton;
import ventanas.VentanaControl;
import ventanas.VentanaVisualizacion;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class MainWindow {

	private JFrame frmClienteNao;
	private JTextField textIP;
	private JTextField textPuerto;
	
	private ConectaGCloud gcloud;
	private ClienteTCP cliente;
	private VentanaControl vc;
	private VentanaVisualizacion vv;
	private Manager manager;
	private JLabel statuslabel;
	
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

	public MainWindow() {
		initialize();
	}

	private void mostarPanelError(String texto){
		final JPanel panel = new JPanel();
		JOptionPane.showMessageDialog(panel, texto, "Error", JOptionPane.ERROR_MESSAGE);
	}

	private void initialize() {
		frmClienteNao = new JFrame();
		frmClienteNao.setTitle("Cliente GCloud");
		frmClienteNao.setResizable(false);
		frmClienteNao.setBounds(100, 100, 399, 140);
		frmClienteNao.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		frmClienteNao.getContentPane().setLayout(null);
		
		textIP = new JTextField();
		textIP.addKeyListener(new KeyAdapter() {
			@Override
			public void keyPressed(KeyEvent arg0) {
				if(arg0.getKeyCode() == KeyEvent.VK_ENTER) {
					conectar();
				   }
			}
		});
		textIP.setText("34.76.240.69");
		textIP.setBounds(10, 36, 125, 20);
		frmClienteNao.getContentPane().add(textIP);
		textIP.setColumns(10);
		
		/*textPuerto = new JTextField();
		textPuerto.setText("6666");
		textPuerto.setBounds(145, 36, 89, 20);
		frmClienteNao.getContentPane().add(textPuerto);
		textPuerto.setColumns(10);*/
		
		JButton btmConectar = new JButton("Conectar");
		btmConectar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				conectar();
			}
		});
		btmConectar.setBounds(255, 35, 89, 23);
		frmClienteNao.getContentPane().add(btmConectar);
		
		JLabel lblNewLabel = new JLabel(" IP simulador (GCE)");
		lblNewLabel.setBounds(10, 11, 200, 14);
		frmClienteNao.getContentPane().add(lblNewLabel);
		
		statuslabel = new JLabel("");
		statuslabel.setBounds(10, 70, 200, 14);
		frmClienteNao.getContentPane().add(statuslabel);
		
		/*JLabel lblNewLabel_1 = new JLabel(" Puerto nao");
		lblNewLabel_1.setBounds(148, 11, 86, 14);
		frmClienteNao.getContentPane().add(lblNewLabel_1);*/
	}

	private void conectar(){
		String ip = textIP.getText();
		if (ip != null && validateIP(ip) == true) {
			//statuslabel.setText("Verificando que Google Pub/Sub está a punto...");
			gcloud = new ConectaGCloud(ip);
			//statuslabel.setText("Verificando que Google Compute Engine está conectado...");
			if (gcloud.verificaConexionGCE()) {
				System.out.println("Conexion verificada");
				//System.out.println("Resultado de testPublicador de PAHO" + gcloud.testPahoDemo());
				
				vv = new VentanaVisualizacion();
				vc = new VentanaControl(gcloud,vv);
				
				gcloud.setVentanaVisualizacion(vv);
				gcloud.setVentanaControl(vc);
				
				manager = new Manager(vc, vv, gcloud);
				manager.start();

				vc.setVisible(true);
				vv.setVisible(true);
				
				frmClienteNao.dispose();
			} else {
				mostarPanelError("Error al conectar a Google Compute Engine");
			}
		} else {
			mostarPanelError("Error al introducir la ip o el puerto");
			return;
		}		
	}

	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					MainWindow window = new MainWindow();
					window.frmClienteNao.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}
}
