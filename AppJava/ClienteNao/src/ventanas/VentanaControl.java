package ventanas;


import java.awt.Dimension;

import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.JPopupMenu;

import nao.ConectaGCloud;
import nao.ConectaMQTT;
import nao.HiloServidor;

import java.awt.GridBagLayout;

import javax.swing.JList;
import javax.swing.JMenuItem;

import java.awt.GridBagConstraints;

import javax.swing.DefaultListModel;
import javax.swing.ImageIcon;
import javax.swing.JButton;

import java.awt.Insets;
import java.awt.Point;
import java.awt.event.ActionListener;
import java.util.Vector;
import java.awt.event.ActionEvent;

import javax.swing.JLabel;
import javax.swing.SwingConstants;
import javax.swing.SwingUtilities;

import java.awt.Color;

import javax.swing.JTextArea;
import javax.swing.JTextField;
import javax.swing.DefaultListCellRenderer;
import javax.swing.JScrollPane;

import net.miginfocom.swing.MigLayout;

import java.awt.Component;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;

import javax.swing.JMenuBar;
import javax.swing.JMenu;

import java.awt.event.KeyAdapter;
import java.awt.event.KeyEvent;

import javax.swing.JRadioButton;
import javax.swing.JComboBox;
import javax.swing.DefaultComboBoxModel;

import java.awt.Font;

import javax.swing.border.SoftBevelBorder;
import javax.swing.border.BevelBorder;
import javax.swing.border.EtchedBorder;
import javax.swing.JSeparator;
//import javax.swing.JSpinner;
//import javax.swing.SpinnerNumberModel;
import javax.swing.Box;

public class VentanaControl extends JFrame {

	private VentanaSimulacion vSimulacion;
	
	private static final long serialVersionUID = 1L;
	private JPanel panelPrincipal;
	private JPanel panelDerecha;
	
	final JPopupMenu pop = new JPopupMenu();
	private int index;
	
	private ConectaGCloud gcloud;
	private ConectaMQTT c;
	//private VentanaVisualizacion vv;
	
	private JList<HiloServidor> list;
	private DefaultListModel<HiloServidor> modeloHilosNao;
	private JPanel panelCentral;
	private JTextArea textPane;
	private JPanel panelInferior;
	private JTextField textoDecir;
	private JButton buttonDecir;
	private JPanel panelDerecho;
	private JScrollPane scrollPane;
	private JLabel lblNewLabel;
	private JTextField txtdatosPeriodicos;
	private JScrollPane scrollPane_1;
	private JMenuBar menuBar;
	private JMenu mnInicio;

	
	private JMenuItem pausar = new JMenuItem("Pausar");
	private JMenuItem despausar = new JMenuItem("Despausar");
	private JMenuItem arrancar = new JMenuItem("Arrancar");
	private JMenuItem parar = new JMenuItem("Parar");
	private JButton btnParada;
	private JRadioButton rdbtnledVerde;
	private JPanel panel;
	private JComboBox<String> comboBox;
	private JButton btnNewButton_4;
	private JLabel lblNewLabel_1;
	private JPanel panel_1;
	private JRadioButton rdbtnLedsAzules;
	private JRadioButton rdbtnLedsRojos;
	private JMenu mnSimulacion;
	private JMenuItem mntmSimulacion_1;
	private JMenuItem mntmNewMenuItem;
	private JSeparator separator_1;
	private JMenuItem mntmNewMenuItem_1;
	private JSeparator separator_2;
	private JMenuItem menuItemModo3;
	private JMenuItem menuItemModo2;
	private JMenuItem menuItemModo1;
	private Component verticalGlue;
	private JMenu menuExat;
	private JMenuItem mntmAlta;
	private JMenuItem mntmMedia;
	private JMenuItem mntmBaja;
	
	public VentanaControl(ConectaGCloud gcloud) {
		
		this.gcloud = gcloud;
		ImageIcon img = new ImageIcon("icono.jpg");
		this.setIconImage(img.getImage());
		
		textPane = new JTextArea();
		vSimulacion = new VentanaSimulacion(gcloud,textPane);
		vSimulacion.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		
		modeloHilosNao = new DefaultListModel<HiloServidor>();
		setTitle("VentanaControl");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(100, 100, 860, 370);
		this.setMinimumSize(new Dimension(860, 370));
		
		menuBar = new JMenuBar();
		setJMenuBar(menuBar);
		
		mnInicio = new JMenu("Inicio");
		mnInicio.setForeground(Color.BLACK);
		mnInicio.setBackground(Color.RED);
		menuBar.add(mnInicio);
		
		mnSimulacion = new JMenu("Simulacion");
		mnSimulacion.setForeground(Color.BLACK);
		menuBar.add(mnSimulacion);
		
		mntmSimulacion_1 = new JMenuItem("Simulacion 1");
		mntmSimulacion_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//String aux = "NAO#SIMULAR:0,0,true,0,50,60;";
				// cambiar por llamada http -> gcloud.send(aux);
				gcloud.PUTSimulationParams_GCE(0, 0, true, 0.0, 50.0, 60.0);
				textPane.append("Enviado SIMULAR: 0,0,true,0,50,60\n");
			}
		});
		mnSimulacion.add(mntmSimulacion_1);
		
		mntmNewMenuItem = new JMenuItem("Simulacion 2");
		mntmNewMenuItem.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				gcloud.PUTSimulationParams_GCE(0, 60, false, 0.0, 0.0, 0.0);
				textPane.append("Enviado SIMULAR: 0,60,false,0,0,0\n");
			}
		});
		mnSimulacion.add(mntmNewMenuItem);
		
		separator_2 = new JSeparator();
		mnSimulacion.add(separator_2);
		
		menuItemModo1 = new JMenuItem("Modo 1");
		menuItemModo1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String aux = "NAO#MODOSIMU:1;";
				gcloud.PUTSimulationMode_GCE("1");
				textPane.append("Enviado: "+ aux +"\n");
			}
		});
		mnSimulacion.add(menuItemModo1);
		
		menuItemModo2 = new JMenuItem("Modo 2");
		menuItemModo2.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String aux = "NAO#MODOSIMU:2;";
				gcloud.PUTSimulationMode_GCE("2");
				textPane.append("Enviado: "+ aux +"\n");
			}
		});
		mnSimulacion.add(menuItemModo2);
		
		menuItemModo3 = new JMenuItem("Modo 3");
		menuItemModo3.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				String aux = "NAO#MODOSIMU:3;";
				gcloud.PUTSimulationMode_GCE("3");
				textPane.append("Enviado: "+ aux +"\n");
			}
		});
		mnSimulacion.add(menuItemModo3);
		
		separator_1 = new JSeparator();
		mnSimulacion.add(separator_1);
		
		mntmNewMenuItem_1 = new JMenuItem("Personalizada");
		mntmNewMenuItem_1.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				vSimulacion.setVisible(true);
			}
		});
		mnSimulacion.add(mntmNewMenuItem_1);
		
		menuExat = new JMenu("Exactitud Palabra");
		menuExat.setForeground(Color.BLACK);
		menuExat.setBackground(Color.RED);
		menuBar.add(menuExat);
		
		mntmAlta = new JMenuItem("Alta");
		mntmAlta.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//String aux = "NAO#EXACPALABRA:0.7;";
				//String aux = "EXACPALABRA:0.7;";
				//gcloud.send(aux);
				c.publishMessageNaoExacpalabra("0.7");
				textPane.append("Enviado EXACPALABRA: 0.7\n");
			}
		});
		menuExat.add(mntmAlta);
		
		mntmMedia = new JMenuItem("Media");
		mntmMedia.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//String aux = "NAO#EXACPALABRA:0.4;";
				//String aux = "EXACPALABRA:0.4;";
				//gcloud.send(aux);
				c.publishMessageNaoExacpalabra("0.4");
				textPane.append("Enviado EXACPALABRA: 0.4\n");
			}
		});
		menuExat.add(mntmMedia);
		
		mntmBaja = new JMenuItem("Baja");
		mntmBaja.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//String aux = "NAO#EXACPALABRA:0.1;";
				//String aux = "EXACPALABRA:0.1;";
				//gcloud.send(aux);
				c.publishMessageNaoExacpalabra("0.1");
				textPane.append("Enviado EXACPALABRA: 0.1\n");
			}
		});
		menuExat.add(mntmBaja);
		
		
		
		panelPrincipal = new JPanel();
		panelPrincipal.setForeground(Color.BLACK);
		panelPrincipal.setBackground(Color.WHITE);
		setContentPane(panelPrincipal);
		GridBagLayout gbl_panelPrincipal = new GridBagLayout();
		gbl_panelPrincipal.columnWidths = new int[]{127, 550, 167, 0};
		gbl_panelPrincipal.rowHeights = new int[]{279, 31, 0};
		gbl_panelPrincipal.columnWeights = new double[]{10.0, 100.0, 10.0, Double.MIN_VALUE};
		gbl_panelPrincipal.rowWeights = new double[]{20.0, 0.0, Double.MIN_VALUE};
		panelPrincipal.setLayout(gbl_panelPrincipal);
				
				panelDerecho = new JPanel();
				panelDerecho.setBorder(new SoftBevelBorder(BevelBorder.RAISED, null, null, null, null));
				GridBagConstraints gbc_panelDerecho = new GridBagConstraints();
				gbc_panelDerecho.fill = GridBagConstraints.BOTH;
				gbc_panelDerecho.gridx = 0;
				gbc_panelDerecho.gridy = 0;
				panelPrincipal.add(panelDerecho, gbc_panelDerecho);
				GridBagLayout gbl_panelDerecho = new GridBagLayout();
				gbl_panelDerecho.columnWidths = new int[]{100, 0};
				gbl_panelDerecho.rowHeights = new int[]{40, 40, 0, 0, 0};
				gbl_panelDerecho.columnWeights = new double[]{1.0, Double.MIN_VALUE};
				gbl_panelDerecho.rowWeights = new double[]{0.0, 0.0, 1.0, 0.0, Double.MIN_VALUE};
				panelDerecho.setLayout(gbl_panelDerecho);
				
				panel = new JPanel();
				panel.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
				GridBagConstraints gbc_panel = new GridBagConstraints();
				gbc_panel.insets = new Insets(3, 3, 5, 3);
				gbc_panel.fill = GridBagConstraints.BOTH;
				gbc_panel.gridx = 0;
				gbc_panel.gridy = 0;
				panelDerecho.add(panel, gbc_panel);
				GridBagLayout gbl_panel = new GridBagLayout();
				gbl_panel.columnWidths = new int[]{111, 0};
				gbl_panel.rowHeights = new int[]{17, 25, 20, 0};
				gbl_panel.columnWeights = new double[]{1.0, Double.MIN_VALUE};
				gbl_panel.rowWeights = new double[]{1.0, 1.0, 1.0, Double.MIN_VALUE};
				panel.setLayout(gbl_panel);
				
				btnNewButton_4 = new JButton("Enviar");
				btnNewButton_4.setFont(new Font("Tahoma", Font.PLAIN, 12));
				btnNewButton_4.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent arg0) {
						String ac = (String) comboBox.getSelectedItem();
						//String aux = "NAO#MOVER:"+ac+";";
						//String aux = "MOVER:"+ac+";";
						//gcloud.send(aux);
						c.publishMessageNaoMover(ac);
						textPane.append("Enviado MOVER: "+ ac +"\n");
					}
				});
				
				lblNewLabel_1 = new JLabel("Accion");
				lblNewLabel_1.setFont(new Font("Tahoma", Font.BOLD, 14));
				lblNewLabel_1.setHorizontalAlignment(SwingConstants.CENTER);
				GridBagConstraints gbc_lblNewLabel_1 = new GridBagConstraints();
				gbc_lblNewLabel_1.fill = GridBagConstraints.BOTH;
				gbc_lblNewLabel_1.insets = new Insets(0, 0, 1, 0);
				gbc_lblNewLabel_1.gridx = 0;
				gbc_lblNewLabel_1.gridy = 0;
				panel.add(lblNewLabel_1, gbc_lblNewLabel_1);
				
				comboBox = new JComboBox<String>();
				comboBox.setFont(new Font("Tahoma", Font.PLAIN, 14));
				comboBox.setModel(new DefaultComboBoxModel<String>(new String[] {"Pincharse", "Sentarse", "Comer", "MedirGlucosa", "Correr"}));
				comboBox.setToolTipText("");
				GridBagConstraints gbc_comboBox = new GridBagConstraints();
				gbc_comboBox.insets = new Insets(0, 1, 1, 1);
				gbc_comboBox.fill = GridBagConstraints.BOTH;
				gbc_comboBox.gridx = 0;
				gbc_comboBox.gridy = 1;
				panel.add(comboBox, gbc_comboBox);
				GridBagConstraints gbc_btnNewButton_4 = new GridBagConstraints();
				gbc_btnNewButton_4.insets = new Insets(0, 0, 1, 0);
				gbc_btnNewButton_4.fill = GridBagConstraints.BOTH;
				gbc_btnNewButton_4.gridx = 0;
				gbc_btnNewButton_4.gridy = 2;
				panel.add(btnNewButton_4, gbc_btnNewButton_4);
				
				panel_1 = new JPanel();
				panel_1.setBorder(new EtchedBorder(EtchedBorder.LOWERED, null, null));
				GridBagConstraints gbc_panel_1 = new GridBagConstraints();
				gbc_panel_1.insets = new Insets(3, 3, 5, 3);
				gbc_panel_1.fill = GridBagConstraints.BOTH;
				gbc_panel_1.gridx = 0;
				gbc_panel_1.gridy = 1;
				panelDerecho.add(panel_1, gbc_panel_1);
				GridBagLayout gbl_panel_1 = new GridBagLayout();
				gbl_panel_1.columnWidths = new int[]{83, 0};
				gbl_panel_1.rowHeights = new int[]{23, 0, 0, 0};
				gbl_panel_1.columnWeights = new double[]{0.0, Double.MIN_VALUE};
				gbl_panel_1.rowWeights = new double[]{0.0, 0.0, 0.0, Double.MIN_VALUE};
				panel_1.setLayout(gbl_panel_1);
				
				rdbtnledVerde = new JRadioButton("Leds Verdes");
				GridBagConstraints gbc_rdbtnledVerde = new GridBagConstraints();
				gbc_rdbtnledVerde.anchor = GridBagConstraints.WEST;
				gbc_rdbtnledVerde.insets = new Insets(0, 0, 5, 0);
				gbc_rdbtnledVerde.gridx = 0;
				gbc_rdbtnledVerde.gridy = 0;
				panel_1.add(rdbtnledVerde, gbc_rdbtnledVerde);
				
				rdbtnLedsRojos = new JRadioButton("Leds Rojos");
				rdbtnLedsRojos.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent arg0) {
						String aux;
						if (rdbtnLedsRojos.isSelected()) {
							//aux = "NAO#LED:rojo,on;";	 
							aux = "rojo,on";
						} else {			 
							//aux = "NAO#LED:rojo,off;";
							aux = "rojo,off";
						}
						//gcloud.send(aux);
						c.publishMessageNaoLeds(aux);
						textPane.append("Enviado LED: "+ aux +"\n");
					}
				});
				GridBagConstraints gbc_rdbtnLedsRojos = new GridBagConstraints();
				gbc_rdbtnLedsRojos.anchor = GridBagConstraints.WEST;
				gbc_rdbtnLedsRojos.insets = new Insets(0, 0, 5, 0);
				gbc_rdbtnLedsRojos.gridx = 0;
				gbc_rdbtnLedsRojos.gridy = 1;
				panel_1.add(rdbtnLedsRojos, gbc_rdbtnLedsRojos);
				
				rdbtnLedsAzules = new JRadioButton("Leds Azules");
				rdbtnLedsAzules.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						String aux;
						if (rdbtnLedsAzules.isSelected()) {
							//aux = "NAO#LED:azul,on;";	 
							aux = "azul,on";
						} else {			 
							//aux = "NAO#LED:azul,off;";	
							aux = "azul,off";
						}
						c.publishMessageNaoLeds(aux);
						//gcloud.send(aux);
						textPane.append("Enviado LED: "+ aux +"\n");
					}
				});
				GridBagConstraints gbc_rdbtnLedsAzules = new GridBagConstraints();
				gbc_rdbtnLedsAzules.anchor = GridBagConstraints.WEST;
				gbc_rdbtnLedsAzules.gridx = 0;
				gbc_rdbtnLedsAzules.gridy = 2;
				panel_1.add(rdbtnLedsAzules, gbc_rdbtnLedsAzules);
				rdbtnledVerde.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent arg0) {
						String aux;
						if (rdbtnledVerde.isSelected()) {
							//aux = "NAO#LED:verde,on;";	 
							aux = "verde,on";
						} else {			 
							//aux = "NAO#LED:verde,off;";	
							aux = "verde,off";
						}
						//gcloud.send(aux);
						c.publishMessageNaoLeds(aux);
						textPane.append("Enviado LED: "+ aux +"\n");
					}
				});
				
				btnParada = new JButton("Parada");
				btnParada.addActionListener(new ActionListener() {
					public void actionPerformed(ActionEvent e) {
						//String aux = "NAO#MOVER:Parada;";
						//gcloud.send(aux);
						c.publishMessageNaoMover("Parada");
						textPane.append("Enviado MOVER: Parada\n");
					}
				});
				
				verticalGlue = Box.createVerticalGlue();
				GridBagConstraints gbc_verticalGlue = new GridBagConstraints();
				gbc_verticalGlue.insets = new Insets(0, 0, 5, 0);
				gbc_verticalGlue.gridx = 0;
				gbc_verticalGlue.gridy = 2;
				panelDerecho.add(verticalGlue, gbc_verticalGlue);
				GridBagConstraints gbc_btnParada = new GridBagConstraints();
				gbc_btnParada.insets = new Insets(0, 3, 0, 3);
				gbc_btnParada.fill = GridBagConstraints.BOTH;
				gbc_btnParada.gridx = 0;
				gbc_btnParada.gridy = 3;
				panelDerecho.add(btnParada, gbc_btnParada);
		
				
				panelCentral = new JPanel();
				panelCentral.setBorder(new SoftBevelBorder(BevelBorder.RAISED, null, null, null, null));
				GridBagConstraints gbc_panelCentral = new GridBagConstraints();
				gbc_panelCentral.fill = GridBagConstraints.BOTH;
				gbc_panelCentral.gridx = 1;
				gbc_panelCentral.gridy = 0;
				panelPrincipal.add(panelCentral, gbc_panelCentral);
				GridBagLayout gbl_panelCentral = new GridBagLayout();
				gbl_panelCentral.columnWidths = new int[]{537, 0};
				gbl_panelCentral.rowHeights = new int[]{39, 142, 0};
				gbl_panelCentral.columnWeights = new double[]{100.0, Double.MIN_VALUE};
				gbl_panelCentral.rowWeights = new double[]{0.0, 1.0, Double.MIN_VALUE};
				panelCentral.setLayout(gbl_panelCentral);
				
				txtdatosPeriodicos = new JTextField();
				txtdatosPeriodicos.setText("'Datos periodicos'");
				txtdatosPeriodicos.setToolTipText("");
				
				GridBagConstraints gbc_txtdatosPeriodicos = new GridBagConstraints();
				gbc_txtdatosPeriodicos.fill = GridBagConstraints.BOTH;
				gbc_txtdatosPeriodicos.insets = new Insets(3, 3, 3, 3);
				gbc_txtdatosPeriodicos.gridx = 0;
				gbc_txtdatosPeriodicos.gridy = 0;
				panelCentral.add(txtdatosPeriodicos, gbc_txtdatosPeriodicos);
				txtdatosPeriodicos.setColumns(5);
				
				scrollPane_1 = new JScrollPane();
				GridBagConstraints gbc_scrollPane_1 = new GridBagConstraints();
				gbc_scrollPane_1.insets = new Insets(3, 3, 3, 3);
				gbc_scrollPane_1.fill = GridBagConstraints.BOTH;
				gbc_scrollPane_1.gridx = 0;
				gbc_scrollPane_1.gridy = 1;
				panelCentral.add(scrollPane_1, gbc_scrollPane_1);

				scrollPane_1.setViewportView(textPane);
				textPane.setTabSize(5);
		
		panelDerecha = new JPanel();
		panelDerecha.setBorder(new SoftBevelBorder(BevelBorder.RAISED, null, null, null, null));
		GridBagConstraints gbc_panelDerecha = new GridBagConstraints();
		gbc_panelDerecha.fill = GridBagConstraints.BOTH;
		gbc_panelDerecha.gridx = 2;
		gbc_panelDerecha.gridy = 0;
		panelPrincipal.add(panelDerecha, gbc_panelDerecha);
		panelDerecha.setLayout(new MigLayout("", "[147.00px,grow 200,fill]", "[fill][266px,grow,fill]"));
		
		lblNewLabel = new JLabel("Estado hilos :");
		lblNewLabel.setHorizontalAlignment(SwingConstants.LEFT);
		panelDerecha.add(lblNewLabel, "cell 0 0,growx,aligny center");
		
		scrollPane = new JScrollPane();
		panelDerecha.add(scrollPane, "cell 0 1,alignx center,aligny center");
		

		list = new JList<HiloServidor>(modeloHilosNao){
            private static final long serialVersionUID = 1L;

            @Override
            public int locationToIndex(Point location) {
                int index = super.locationToIndex(location);
                if (index != -1 && !getCellBounds(index, index).contains(location)) {
                    clearSelection();
                    return -1;
                }
                else {
                    return index;
                }
            }
        };
		list.addMouseListener(new MouseAdapter() {
			@Override
			public void mouseClicked(MouseEvent arg0) {
				int aux = list.locationToIndex(new Point(arg0.getX(), arg0.getY()));
				if(aux == -1)
					return;
				list.setSelectedIndex(aux);
				index = list.getSelectedIndex();
				HiloServidor hilo = list.getSelectedValue();
				if(hilo.getEstado().equals("CORRIENDO")){ //corriendo
					pausar.setEnabled(true);
					despausar.setEnabled(false);
					parar.setEnabled(true);
					arrancar.setEnabled(false);
				}
				if(hilo.getEstado().equals("PARADO")){
					pausar.setEnabled(false);
					despausar.setEnabled(false);
					parar.setEnabled(false);
					arrancar.setEnabled(true);
				}
				if(hilo.getEstado().equals("PAUSADO")){ //pausado
					pausar.setEnabled(false);
					despausar.setEnabled(true);
					parar.setEnabled(true);
					arrancar.setEnabled(false);
				}
				if(SwingUtilities.isRightMouseButton(arg0) && index == list.locationToIndex(arg0.getPoint())){
					if(!list.isSelectionEmpty()){
						pop.show(list, arg0.getX(), arg0.getY());
					}
				}
			}
		});
		list.setCellRenderer( new CellRenderer() );
		scrollPane.setViewportView(list);
		
		panelInferior = new JPanel();
		panelInferior.setBorder(new SoftBevelBorder(BevelBorder.RAISED, null, null, null, null));
		GridBagConstraints gbc_panelInferior = new GridBagConstraints();
		gbc_panelInferior.fill = GridBagConstraints.BOTH;
		gbc_panelInferior.gridwidth = 3;
		gbc_panelInferior.gridx = 0;
		gbc_panelInferior.gridy = 1;
		panelPrincipal.add(panelInferior, gbc_panelInferior);
		GridBagLayout gbl_panelInferior = new GridBagLayout();
		gbl_panelInferior.columnWidths = new int[]{608, 57, 0};
		gbl_panelInferior.rowHeights = new int[]{23, 0};
		gbl_panelInferior.columnWeights = new double[]{1.0, 0.0, Double.MIN_VALUE};
		gbl_panelInferior.rowWeights = new double[]{0.0, Double.MIN_VALUE};
		panelInferior.setLayout(gbl_panelInferior);
		
		textoDecir = new JTextField();
		textoDecir.addKeyListener(new KeyAdapter() {
			@Override
			public void keyPressed(KeyEvent arg0) {
				if(arg0.getKeyCode() == KeyEvent.VK_ENTER) {
					//String aux = "NAO#DECIR:"+textoDecir.getText()+";";
					//String aux = "DECIR:"+textoDecir.getText()+";";
					//gcloud.send(aux);
					c.publishMessageNaoDecir(textoDecir.getText());
					textPane.append("Enviado DECIR: "+ textoDecir.getText() +"\n");
			   }
			}
		});
		GridBagConstraints gbc_textoDecir = new GridBagConstraints();
		gbc_textoDecir.insets = new Insets(0, 2, 0, 2);
		gbc_textoDecir.fill = GridBagConstraints.HORIZONTAL;
		gbc_textoDecir.gridx = 0;
		gbc_textoDecir.gridy = 0;
		panelInferior.add(textoDecir, gbc_textoDecir);
		textoDecir.setColumns(10);
		
		buttonDecir = new JButton("    Decir    ");
		buttonDecir.setAlignmentX(Component.CENTER_ALIGNMENT);
		buttonDecir.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				//String aux = "NAO#DECIR:"+textoDecir.getText()+";";
				//String aux = "DECIR:"+textoDecir.getText()+";";
				//gcloud.send(aux);
				c.publishMessageNaoDecir(textoDecir.getText());
				textPane.append("Enviado DECIR: "+ textoDecir.getText() +"\n");
			}
		});
		GridBagConstraints gbc_buttonDecir = new GridBagConstraints();
		gbc_buttonDecir.insets = new Insets(1, 1, 1, 1);
		gbc_buttonDecir.fill = GridBagConstraints.HORIZONTAL;
		gbc_buttonDecir.gridx = 1;
		gbc_buttonDecir.gridy = 0;
		panelInferior.add(buttonDecir, gbc_buttonDecir);
		addPopup();
	}
	
	public void setConectaMQTT(ConectaMQTT c) {
		this.c = c;
	}
	
	private void addPopup(){
		pop.add(pausar);
		pop.add(despausar);
		pop.add(parar);
		pop.add(arrancar);
		
		pausar.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				HiloServidor hilo =list.getSelectedValue();
				if(hilo!= null ){
					//String aux = "NAO#THREAD:"+hilo.getNombre()+",2;";
					if (hilo.getNombre() != "SIMULACION") {
						c.publishMessageNaoHilos(hilo.getNombre()+",PAUSADO");
					}
					else gcloud.GETPausa_GCE();
				}
			}
		});
		
		despausar.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				HiloServidor hilo =list.getSelectedValue();
				if(hilo!= null ){
					//String aux = "NAO#THREAD:"+hilo.getNombre()+",3;";
					if (hilo.getNombre() != "SIMULACION") {
						c.publishMessageNaoHilos(hilo.getNombre()+",CORRIENDO");
					}
					else gcloud.GETDespausa_GCE();
				}
			}
		});
		
		parar.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				HiloServidor hilo =list.getSelectedValue();
				if(hilo!= null ){
				//String aux = "NAO#THREAD:"+hilo.getNombre()+",0;";
					if (hilo.getNombre() != "SIMULACION") {
						c.publishMessageNaoHilos(hilo.getNombre()+",PARADO");
					}
					else gcloud.GETPara_GCE();
				}
			}
		});
		
		arrancar.addActionListener(new ActionListener() {
			@Override
			public void actionPerformed(ActionEvent e) {
				HiloServidor hilo = list.getSelectedValue();
				if(hilo!= null ){
					System.out.println("Pulsa arrancar con HiloServidor ID: " + hilo.getNombre());
				//String aux = "NAO#THREAD:"+hilo.getNombre()+",1;";
					if (hilo.getNombre() != "SIMULACION") {
						c.publishMessageNaoHilos(hilo.getNombre()+",CORRIENDO");
					}
					else gcloud.GETArranca_GCE();
				}
			}
		});
	}
	
	public void addEstadoHilos(Vector<HiloServidor> estadoHilos) {
		modeloHilosNao.clear();
	    for(int i=0; i< estadoHilos.size(); i++){
	    	modeloHilosNao.addElement(estadoHilos.get(i));
	    }
	}
	
	public void addStringRecivido(String estdohilos){
		txtdatosPeriodicos.setText(estdohilos);
	}

	public void addTextPane(String txt){
		textPane.append("RECIVIDO: "+ txt +"\n");
	}
	
	
    private static class CellRenderer extends DefaultListCellRenderer {
		private static final long serialVersionUID = 1L;
	
		public Component getListCellRendererComponent( JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus ) {
			HiloServidor aux = (HiloServidor) value;
            Component c = super.getListCellRendererComponent( list, value, index, isSelected, cellHasFocus );
            String e = aux.getEstado();
            
            if ( e.equals("CORRIENDO")) {
            	c.setBackground( new Color(0, 255, 0, 180) );
            }
            if ( e.equals("PARADO")) {
            	c.setBackground( new Color(255, 0, 0, 180) );
            }
            if ( e.equals("PAUSADO")) {
            	c.setBackground( new Color(255, 255, 0, 180) );
            }
            return c;
        }
    }
}


