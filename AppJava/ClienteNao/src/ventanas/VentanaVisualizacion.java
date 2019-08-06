package ventanas;


import java.awt.Dimension;
import javax.swing.JFrame;
import javax.swing.JPanel;
import javax.swing.border.EmptyBorder;
import org.jfree.chart.ChartFactory;
import org.jfree.chart.ChartPanel;
import org.jfree.chart.JFreeChart;
import org.jfree.chart.axis.NumberAxis;
import org.jfree.chart.plot.PlotOrientation;
import org.jfree.chart.plot.XYPlot;
import org.jfree.chart.renderer.xy.XYLineAndShapeRenderer;
import org.jfree.data.xy.XYDataset;
import org.jfree.data.xy.XYSeries;
import org.jfree.data.xy.XYSeriesCollection;
import org.jfree.util.ShapeUtilities;
import javax.swing.JLabel;
import java.awt.GridBagLayout;
import java.awt.GridBagConstraints;
import java.awt.Insets;
import java.text.DecimalFormat;
import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import javax.swing.border.EtchedBorder;
import java.awt.BorderLayout;
import java.awt.FlowLayout;



public class VentanaVisualizacion extends JFrame {

	private static final long serialVersionUID = 1L;
	//---------Paneles---------
	private JPanel panelPrincipal;
	private JPanel panelCentral;

	private XYSeries datosGLucosa;
	private  XYSeriesCollection data;
	private JFreeChart chart1;
	private ChartPanel chartPanel;
	private JLabel lbl1;

	private int i = 0;
	private JLabel lblNivelDeGlucosa;
	private JLabel labelGlucosa;
	private JPanel panel_1;
	
	private ChartPanel chartPanel_1;
	private JFreeChart chart1_1;
	private JLabel lblGluText;


	
	@SuppressWarnings("serial")
	public VentanaVisualizacion() {	
		setTitle("VentanaVisualizacion");
		setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		setBounds(700, 100, 804, 355);
		this.setMinimumSize(new Dimension(820, 350));
		
		
		panelPrincipal = new JPanel();
		panelPrincipal.setBorder(new EmptyBorder(5, 5, 5, 5));
		setContentPane(panelPrincipal);
		GridBagLayout gbl_panelPrincipal = new GridBagLayout();
		gbl_panelPrincipal.columnWidths = new int[]{75, 878, 0};
		gbl_panelPrincipal.rowHeights = new int[]{0, 100, 100, 100, 0};
		gbl_panelPrincipal.columnWeights = new double[]{10.0, 100.0, Double.MIN_VALUE};
		gbl_panelPrincipal.rowWeights = new double[]{0.0, 1.0, 1.0, 1.0, Double.MIN_VALUE};
		panelPrincipal.setLayout(gbl_panelPrincipal);
		
		datosGLucosa = new XYSeries("Glucosa");
		data = new XYSeriesCollection(datosGLucosa);
		chart1  = createChart(data);
		chart1_1  = createChart1(data);
        
        labelGlucosa = new JLabel("0");
        GridBagConstraints gbc_labelGlucosa = new GridBagConstraints();
        gbc_labelGlucosa.insets = new Insets(0, 0, 5, 5);
        gbc_labelGlucosa.gridx = 0;
        gbc_labelGlucosa.gridy = 0;
        panelPrincipal.add(labelGlucosa, gbc_labelGlucosa);
        
        lblNivelDeGlucosa = new JLabel("Nivel de Glucosa");
        lblNivelDeGlucosa.setFont(new Font("Tahoma", Font.BOLD, 26));
        GridBagConstraints gbc_lblNivelDeGlucosa = new GridBagConstraints();
        gbc_lblNivelDeGlucosa.insets = new Insets(0, 0, 5, 0);
        gbc_lblNivelDeGlucosa.gridx = 1;
        gbc_lblNivelDeGlucosa.gridy = 0;
        panelPrincipal.add(lblNivelDeGlucosa, gbc_lblNivelDeGlucosa);
        
        panel_1 = new JPanel();
        panel_1.setBorder(new EtchedBorder(EtchedBorder.RAISED, null, null));
        GridBagConstraints gbc_panel_1 = new GridBagConstraints();
        gbc_panel_1.gridheight = 2;
        gbc_panel_1.insets = new Insets(0, 0, 5, 5);
        gbc_panel_1.fill = GridBagConstraints.BOTH;
        gbc_panel_1.gridx = 0;
        gbc_panel_1.gridy = 1;
        panelPrincipal.add(panel_1, gbc_panel_1);
        panel_1.setLayout(new BorderLayout(0, 0));
        
        lbl1 = new JLabel(""){
            protected void paintComponent(Graphics g)
            {
                g.setColor( getBackground() );
                g.fillRect(0, 0, getWidth(), getHeight());
                super.paintComponent(g);
            }
        };
        panel_1.add(lbl1);
        lbl1.setBackground(Color.WHITE);
        
        lbl1.setBackground(new Color(0, 255, 0, 255/3));
        lbl1.setOpaque(false);
        
        panelCentral = new JPanel();
        panelCentral.setBorder(new EtchedBorder(EtchedBorder.RAISED, null, null));
        panelCentral.setMinimumSize(new Dimension(620, 350));
        GridBagConstraints gbc_panelCentral = new GridBagConstraints();
        gbc_panelCentral.gridheight = 3;
        gbc_panelCentral.fill = GridBagConstraints.BOTH;
        gbc_panelCentral.gridx = 1;
        gbc_panelCentral.gridy = 1;
        panelPrincipal.add(panelCentral, gbc_panelCentral);
        GridBagLayout gbl_panelCentral = new GridBagLayout();
        gbl_panelCentral.columnWidths = new int[]{300, 300, 0};
        gbl_panelCentral.rowHeights = new int[]{302, 0};
        gbl_panelCentral.columnWeights = new double[]{1.0, 1.0, Double.MIN_VALUE};
        gbl_panelCentral.rowWeights = new double[]{1.0, Double.MIN_VALUE};
        panelCentral.setLayout(gbl_panelCentral);
        chartPanel = new ChartPanel(chart1);
        FlowLayout flowLayout = (FlowLayout) chartPanel.getLayout();
        flowLayout.setVgap(0);
        flowLayout.setHgap(0);
        GridBagConstraints gbc_chartPanel = new GridBagConstraints();
        gbc_chartPanel.insets = new Insets(0, 0, 0, 5);
        gbc_chartPanel.fill = GridBagConstraints.BOTH;
        gbc_chartPanel.gridx = 0;
        gbc_chartPanel.gridy = 0;
        panelCentral.add(chartPanel, gbc_chartPanel);
        chartPanel.setPreferredSize(new Dimension(670, 350));
        
        chartPanel_1 = new ChartPanel(chart1_1);
        chartPanel_1.setPreferredSize(new Dimension(670, 350));
        GridBagConstraints gbc_chartPanel_1 = new GridBagConstraints();
        gbc_chartPanel_1.fill = GridBagConstraints.BOTH;
        gbc_chartPanel_1.gridx = 1;
        gbc_chartPanel_1.gridy = 0;
        panelCentral.add(chartPanel_1, gbc_chartPanel_1);
        
        lblGluText = new JLabel("");
        GridBagConstraints gbc_lblGluText = new GridBagConstraints();
        gbc_lblGluText.anchor = GridBagConstraints.NORTH;
        gbc_lblGluText.insets = new Insets(0, 0, 0, 5);
        gbc_lblGluText.gridx = 0;
        gbc_lblGluText.gridy = 3;
        panelPrincipal.add(lblGluText, gbc_lblGluText);
	}
	
	public void setEstadoLabelGlucosa(double glucosa){
		
        lbl1.setBackground(new Color(0, 255, 0, 255));

		if(glucosa > 175){
	        lbl1.setBackground(new Color(255, 0, 0, 255)); 
	        lblGluText.setText("Alta");
		}
		if( glucosa > 75 && glucosa < 175){
	        lbl1.setBackground(new Color(0, 255, 0, 255));	   
	        lblGluText.setText("Estable");
		}
		if(glucosa < 75){
			lbl1.setBackground(new Color(0, 0, 255, 255));
			lblGluText.setText("Baja");
		}
		
		DecimalFormat df = new DecimalFormat("#.0000");
	    String angleFormated = df.format(glucosa);
		labelGlucosa.setText(angleFormated);
	}

	public void addDotGraf(float glucosa){
		try{
	        if(glucosa != -999 && glucosa != -1000) {
	        	this.datosGLucosa.add(i, glucosa);
	        	i = i+1;
	        	setEstadoLabelGlucosa(glucosa);
	        }
	        if( glucosa == -1000)
	        	resetChart();
		} catch (Exception e) {
		}
	}
	
	public void resetChart(){
		this.datosGLucosa.clear();
		this.i = 0;
	}
	
    private JFreeChart createChart(final XYDataset dataset) {
        final JFreeChart result = ChartFactory.createXYLineChart(
            "",  "", "",dataset, PlotOrientation.VERTICAL,
            false,false,false
        );
        XYPlot plot = result.getXYPlot();

        NumberAxis axis = (NumberAxis) plot.getDomainAxis();
        axis.setRange(0, 91.0); 
        axis.setAutoRangeIncludesZero(false);
        axis.setAutoRange(true);
        axis.setAutoRange(true);
        NumberAxis axis1 = (NumberAxis) plot.getRangeAxis();
        axis1.setRange(90.0, 91.0); 
        axis1.setAutoRange(true);
        axis1.setAutoRangeIncludesZero(false);

        XYLineAndShapeRenderer r = (XYLineAndShapeRenderer) plot.getRenderer();
        r.setSeriesShape(0, ShapeUtilities.createDiamond(2));
        r.setSeriesShapesVisible(0, true);
        


        return result;
    }
    
    private JFreeChart createChart1(final XYDataset dataset) {
        final JFreeChart result = ChartFactory.createXYLineChart(
            "", "", "",dataset, PlotOrientation.VERTICAL,
            false,false,false
        );
        XYPlot plot = result.getXYPlot();
        NumberAxis axis = (NumberAxis) plot.getDomainAxis();
        axis.setRange(0, 100); 
        axis.setAutoRange(true);
        axis.setAutoRangeIncludesZero(false);
        axis.setFixedAutoRange(0.0);  // 60 seconds
        NumberAxis axis1 = (NumberAxis) plot.getRangeAxis();
        axis1.setRange(0, 400); 
        axis1.setAutoRangeIncludesZero(false);

        XYLineAndShapeRenderer r = (XYLineAndShapeRenderer) plot.getRenderer();
        r.setSeriesShape(0, ShapeUtilities.createDiamond(2));
        r.setSeriesShapesVisible(0, true);
        


        return result;
    }

}
