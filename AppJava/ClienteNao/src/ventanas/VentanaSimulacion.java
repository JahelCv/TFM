package ventanas;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;

import nao.ConectaGCloud;

import java.awt.GridBagLayout;

import javax.swing.JLabel;

import java.awt.GridBagConstraints;
import java.awt.Insets;

import javax.swing.JSpinner;
import javax.swing.JSeparator;
import javax.swing.JTextArea;
import javax.swing.SwingConstants;
import javax.swing.JCheckBox;
import javax.swing.ImageIcon;
import javax.swing.JButton;
import javax.swing.SpinnerNumberModel;

import java.awt.Font;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;

public class VentanaSimulacion extends JFrame {

	private static final long serialVersionUID = 1L;
	private JPanel contentPane;
	SpinnerNumberModel model ;
	
	private JCheckBox chckEjercicio;
	private JSpinner spinnerTiempo;
	private JSpinner spinnerIntensidad;
	private JSpinner spinnerDuracion;
	private JSpinner spinnerBolus;
	private JSpinner spinnerCho;
	private JButton botonEnviar;

	private ConectaGCloud gcloud;
	JTextArea textControl;

	public VentanaSimulacion(ConectaGCloud _gcloud,JTextArea textPane) {
		ImageIcon img = new ImageIcon("icono.jpg");
		this.setIconImage(img.getImage());
		this.gcloud = _gcloud;
		this.textControl = textPane;
		addWindowListener(new WindowAdapter() {
			@Override
			public void windowClosing(WindowEvent e) {
				e.getWindow().setVisible(false);
				e.getWindow().dispose();
			}
		});

		
		setResizable(false);
		setTitle("Simulacion");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 466, 144);
		contentPane = new JPanel();
		contentPane.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(contentPane);
		GridBagLayout gbl_contentPane = new GridBagLayout();
		gbl_contentPane.columnWidths = new int[]{70, 0, 70, 0, 70, 0, 70, 0, 70, 0, 70, 0};
		gbl_contentPane.rowHeights = new int[]{25, 25, 25, 25, 0};
		gbl_contentPane.columnWeights = new double[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		gbl_contentPane.rowWeights = new double[]{0.0, 0.0, 0.0, 0.0, Double.MIN_VALUE};
		contentPane.setLayout(gbl_contentPane);
		
		JLabel lblNewLabel = new JLabel("Par\u00E1metros Simulaci\u00F3n");
		lblNewLabel.setFont(new Font("Tahoma", Font.BOLD, 11));
		GridBagConstraints gbc_lblNewLabel = new GridBagConstraints();
		gbc_lblNewLabel.fill = GridBagConstraints.HORIZONTAL;
		gbc_lblNewLabel.gridwidth = 11;
		gbc_lblNewLabel.insets = new Insets(0, 0, 5, 0);
		gbc_lblNewLabel.gridx = 0;
		gbc_lblNewLabel.gridy = 0;
		contentPane.add(lblNewLabel, gbc_lblNewLabel);
		
		
		JLabel lblBolus = new JLabel("Bolus");
		GridBagConstraints gbc_lblBolus = new GridBagConstraints();
		gbc_lblBolus.insets = new Insets(0, 0, 5, 5);
		gbc_lblBolus.gridx = 0;
		gbc_lblBolus.gridy = 1;
		contentPane.add(lblBolus, gbc_lblBolus);
		
		JLabel lblCho = new JLabel("Cho");
		GridBagConstraints gbc_lblCho = new GridBagConstraints();
		gbc_lblCho.insets = new Insets(0, 0, 5, 5);
		gbc_lblCho.gridx = 2;
		gbc_lblCho.gridy = 1;
		contentPane.add(lblCho, gbc_lblCho);
		
		JLabel lblEjercicio = new JLabel("Ejercicio");
		GridBagConstraints gbc_lblEjercicio = new GridBagConstraints();
		gbc_lblEjercicio.insets = new Insets(0, 0, 5, 5);
		gbc_lblEjercicio.gridx = 4;
		gbc_lblEjercicio.gridy = 1;
		contentPane.add(lblEjercicio, gbc_lblEjercicio);
		
		JLabel lblTiempo = new JLabel("Tiempo");
		lblTiempo.setEnabled(false);
		GridBagConstraints gbc_lblTiempo = new GridBagConstraints();
		gbc_lblTiempo.insets = new Insets(0, 0, 5, 5);
		gbc_lblTiempo.gridx = 6;
		gbc_lblTiempo.gridy = 1;
		contentPane.add(lblTiempo, gbc_lblTiempo);
		
		JLabel lblIntensidad = new JLabel("Intensidad");
		lblIntensidad.setEnabled(false);
		GridBagConstraints gbc_lblIntensidad = new GridBagConstraints();
		gbc_lblIntensidad.insets = new Insets(0, 0, 5, 5);
		gbc_lblIntensidad.gridx = 8;
		gbc_lblIntensidad.gridy = 1;
		contentPane.add(lblIntensidad, gbc_lblIntensidad);
		
		JLabel lblDuracion = new JLabel("Duracion");
		lblDuracion.setEnabled(false);
		GridBagConstraints gbc_lblDuracion = new GridBagConstraints();
		gbc_lblDuracion.insets = new Insets(0, 0, 5, 0);
		gbc_lblDuracion.gridx = 10;
		gbc_lblDuracion.gridy = 1;
		contentPane.add(lblDuracion, gbc_lblDuracion);
		

		spinnerBolus = new JSpinner();
		spinnerBolus.setModel(new SpinnerNumberModel(new Double(0), null, null,0.1));
		GridBagConstraints gbc_spinnerBolus = new GridBagConstraints();
		gbc_spinnerBolus.fill = GridBagConstraints.HORIZONTAL;
		gbc_spinnerBolus.insets = new Insets(0, 0, 5, 5);
		gbc_spinnerBolus.gridx = 0;
		gbc_spinnerBolus.gridy = 2;
		contentPane.add(spinnerBolus, gbc_spinnerBolus);
		
		JSeparator separator = new JSeparator();
		separator.setOrientation(SwingConstants.VERTICAL);
		GridBagConstraints gbc_separator = new GridBagConstraints();
		gbc_separator.insets = new Insets(0, 0, 5, 5);
		gbc_separator.gridx = 1;
		gbc_separator.gridy = 2;
		contentPane.add(separator, gbc_separator);
		
		spinnerCho = new JSpinner();
		spinnerCho.setModel(new SpinnerNumberModel(new Double(0), null, null,0.1));
		GridBagConstraints gbc_spinnerCho = new GridBagConstraints();
		gbc_spinnerCho.fill = GridBagConstraints.HORIZONTAL;
		gbc_spinnerCho.insets = new Insets(0, 0, 5, 5);
		gbc_spinnerCho.gridx = 2;
		gbc_spinnerCho.gridy = 2;
		contentPane.add(spinnerCho, gbc_spinnerCho);
		
		JSeparator separator_1 = new JSeparator();
		separator_1.setOrientation(SwingConstants.VERTICAL);
		GridBagConstraints gbc_separator_1 = new GridBagConstraints();
		gbc_separator_1.insets = new Insets(0, 0, 5, 5);
		gbc_separator_1.gridx = 3;
		gbc_separator_1.gridy = 2;
		contentPane.add(separator_1, gbc_separator_1);
		
		chckEjercicio = new JCheckBox("");
		chckEjercicio.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				if(chckEjercicio.isSelected())
				{
					spinnerDuracion.setEnabled(true);
					spinnerIntensidad.setEnabled(true);
					spinnerTiempo.setEnabled(true);
					lblDuracion.setEnabled(true);
					lblTiempo.setEnabled(true);
					lblIntensidad.setEnabled(true);
				} else {
					spinnerDuracion.setEnabled(false);
					spinnerIntensidad.setEnabled(false);
					spinnerTiempo.setEnabled(false);
					lblDuracion.setEnabled(false);
					lblTiempo.setEnabled(false);
					lblIntensidad.setEnabled(false);
				}
			}
		});
		GridBagConstraints gbc_chckEjercicio = new GridBagConstraints();
		gbc_chckEjercicio.insets = new Insets(0, 0, 5, 5);
		gbc_chckEjercicio.gridx = 4;
		gbc_chckEjercicio.gridy = 2;
		contentPane.add(chckEjercicio, gbc_chckEjercicio);
		
		JSeparator separator_2 = new JSeparator();
		separator_2.setOrientation(SwingConstants.VERTICAL);
		GridBagConstraints gbc_separator_2 = new GridBagConstraints();
		gbc_separator_2.insets = new Insets(0, 0, 5, 5);
		gbc_separator_2.gridx = 5;
		gbc_separator_2.gridy = 2;
		contentPane.add(separator_2, gbc_separator_2);
		
		spinnerTiempo = new JSpinner();
		spinnerTiempo.setEnabled(false);
		spinnerTiempo.setModel(new SpinnerNumberModel(new Double(0), null, null,0.1));
		GridBagConstraints gbc_spinnerTiempo = new GridBagConstraints();
		gbc_spinnerTiempo.fill = GridBagConstraints.HORIZONTAL;
		gbc_spinnerTiempo.insets = new Insets(0, 0, 5, 5);
		gbc_spinnerTiempo.gridx = 6;
		gbc_spinnerTiempo.gridy = 2;
		contentPane.add(spinnerTiempo, gbc_spinnerTiempo);
		
		JSeparator separator_3 = new JSeparator();
		separator_3.setOrientation(SwingConstants.VERTICAL);
		GridBagConstraints gbc_separator_3 = new GridBagConstraints();
		gbc_separator_3.insets = new Insets(0, 0, 5, 5);
		gbc_separator_3.gridx = 7;
		gbc_separator_3.gridy = 2;
		contentPane.add(separator_3, gbc_separator_3);
		
		spinnerIntensidad = new JSpinner();
		spinnerIntensidad.setEnabled(false);
		spinnerIntensidad.setModel(new SpinnerNumberModel(new Double(0), null, null,0.1));
		GridBagConstraints gbc_spinnerIntensidad = new GridBagConstraints();
		gbc_spinnerIntensidad.fill = GridBagConstraints.HORIZONTAL;
		gbc_spinnerIntensidad.insets = new Insets(0, 0, 5, 5);
		gbc_spinnerIntensidad.gridx = 8;
		gbc_spinnerIntensidad.gridy = 2;
		contentPane.add(spinnerIntensidad, gbc_spinnerIntensidad);
		
		JSeparator separator_4 = new JSeparator();
		separator_4.setOrientation(SwingConstants.VERTICAL);
		GridBagConstraints gbc_separator_4 = new GridBagConstraints();
		gbc_separator_4.insets = new Insets(0, 0, 5, 5);
		gbc_separator_4.gridx = 9;
		gbc_separator_4.gridy = 2;
		contentPane.add(separator_4, gbc_separator_4);
		
		botonEnviar = new JButton("       Enviar       ");
		botonEnviar.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				
				//String aux = "NAO#SIMULAR:";
				
				double bolus = (double) spinnerBolus.getValue();
				double cho = (double) spinnerCho.getValue();
				double ejerT = 0.0;
				double ejerD = 0.0;
				double ejerI = 0.0;
				boolean ejer = chckEjercicio.isSelected();
				if(ejer){
					ejerT = (double) spinnerTiempo.getValue();
					ejerD = (double) spinnerDuracion.getValue();
					ejerI = (double) spinnerIntensidad.getValue();
				} 
				gcloud.PUTSimulationParams_GCE(bolus, cho, ejer, ejerT, ejerD, ejerI);
				textControl.append("Envia a GCE Params de Simulacion: "+bolus+","+cho+","+ejer+",["+ejerT+","+ejerD+","+ejerI+"]\n");
			}
		});
		
		spinnerDuracion = new JSpinner();
		spinnerDuracion.setEnabled(false);
		spinnerDuracion.setModel(new SpinnerNumberModel(new Double(0), null, null,0.1));
		GridBagConstraints gbc_spinnerDuracion = new GridBagConstraints();
		gbc_spinnerDuracion.fill = GridBagConstraints.HORIZONTAL;
		gbc_spinnerDuracion.insets = new Insets(0, 0, 5, 0);
		gbc_spinnerDuracion.gridx = 10;
		gbc_spinnerDuracion.gridy = 2;
		contentPane.add(spinnerDuracion, gbc_spinnerDuracion);
		GridBagConstraints gbc_botonEnviar = new GridBagConstraints();
		gbc_botonEnviar.anchor = GridBagConstraints.EAST;
		gbc_botonEnviar.gridwidth = 3;
		gbc_botonEnviar.gridx = 8;
		gbc_botonEnviar.gridy = 3;
		contentPane.add(botonEnviar, gbc_botonEnviar);
	}

}
