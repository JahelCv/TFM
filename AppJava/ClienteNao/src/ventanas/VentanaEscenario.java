package ventanas;

import java.awt.BorderLayout;

import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import javax.swing.JLabel;
import javax.swing.JTextArea;
import javax.swing.JScrollPane;

import java.awt.Font;

import javax.swing.SwingConstants;

import org.eclipse.wb.swing.FocusTraversalOnArray;

import java.awt.Component;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;

import javax.swing.border.EtchedBorder;

public class VentanaEscenario extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	private JTextArea textArea;
	private JLabel lblFase;
	private boolean auxEscenario;

	public VentanaEscenario() {
		ImageIcon img = new ImageIcon("icono.jpg");
		this.setIconImage(img.getImage());
		setAutoRequestFocus(false);
		setResizable(false);
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				e.getWindow().setVisible(false);
				e.getWindow().dispose();
				auxEscenario = false;
			}
		});
		this.auxEscenario = false;
		setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		setBounds(100, 100, 208, 302);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		contentPane.setLayout(new BorderLayout(0, 0));
		
		JPanel panel = new JPanel();
		panel.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		contentPane.add(panel, BorderLayout.NORTH);
		panel.setLayout(new BorderLayout(0, 0));
		
		lblFase = new JLabel("Datos Escenario");
		lblFase.setHorizontalAlignment(SwingConstants.CENTER);
		lblFase.setFont(new Font("Tahoma", Font.BOLD, 14));
		panel.add(lblFase);
		
		JPanel panel_1 = new JPanel();
		panel_1.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
		contentPane.add(panel_1, BorderLayout.CENTER);
		panel_1.setLayout(new BorderLayout(0, 0));
		
		JScrollPane scrollPane = new JScrollPane();
		panel_1.add(scrollPane);
		
		textArea = new JTextArea();
		scrollPane.setViewportView(textArea);
		panel_1.setFocusTraversalPolicy(new FocusTraversalOnArray(new Component[]{scrollPane, textArea}));
	}
	
	public void addDatos(String datos){
		setVisible(true);
		setEscenarioFlag(true);
		textArea.setText(datos);
	}
	
	public boolean getEscenarioFlag(){
		return this.auxEscenario;
	}
	
	public void setEscenarioFlag(boolean aux){
		this.auxEscenario = aux;
	}

}
