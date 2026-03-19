"""
Módulo de visualización para análisis de cobertura indoor.
Genera croquis del edificio, gráficos de nivel de señal y comparativas.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd
from matplotlib.patches import Rectangle, Polygon, FancyBboxPatch
from matplotlib.collections import PatchCollection
import seaborn as sns
from typing import List, Dict, Optional


class BuildingVisualization:
    """Visualiza la geometría del edificio y puntos de medida."""
    
    def __init__(self, figsize: tuple = (14, 10)):
        """Inicializa figura para visualización."""
        self.fig = None
        self.ax = None
        self.figsize = figsize
        sns.set_style("whitegrid")
    
    def plot_building_layout(self, building_data: Dict, 
                            measurement_points: List = None,
                            tx_position: tuple = None,
                            title: str = "Plano del Edificio"):
        """
        Dibuja el plano del edificio con puntos de medida.
        
        Args:
            building_data: Dict con 'floors', 'walls', 'dimensions'
            measurement_points: Lista de puntos IndoorMeasurementPoint
            tx_position: Posición de antena (x, y)
            title: Título del gráfico
        """
        self.fig, self.ax = plt.subplots(figsize=self.figsize)
        
        # Dibujar paredes exteriores (fachada)
        building = building_data.get('building', {})
        if 'perimeter' in building:
            perimeter = building['perimeter']
            rect = Rectangle((perimeter['x'], perimeter['y']), 
                            perimeter['width'], perimeter['height'],
                            linewidth=3, edgecolor='black', 
                            facecolor='lightgray', alpha=0.3)
            self.ax.add_patch(rect)
        
        # Dibujar paredes interiores
        if 'interior_walls' in building:
            for wall in building['interior_walls']:
                if wall['type'] == 'vertical':
                    self.ax.plot([wall['x'], wall['x']], 
                               [wall['y_start'], wall['y_end']],
                               'k-', linewidth=2, label='Pared interior' if wall == building['interior_walls'][0] else '')
                elif wall['type'] == 'horizontal':
                    self.ax.plot([wall['x_start'], wall['x_end']], 
                               [wall['y'], wall['y']],
                               'k-', linewidth=2)
        
        # Dibujar forjados (pisos)
        if 'floors' in building:
            for floor in building['floors']:
                self.ax.axhline(y=floor['y_position'], 
                              color='brown', linestyle='--', 
                              linewidth=1.5, alpha=0.6)
                self.ax.text(-1, floor['y_position'] + 0.5, 
                           f"Piso {floor['level']}", 
                           fontsize=9, style='italic')
        
        # Dibujar puntos de medida
        if measurement_points:
            for i, point in enumerate(measurement_points):
                color = ['#FF6B6B', '#4ECDC4', '#45B7D1'][i % 3]
                self.ax.scatter(point.x, point.y, s=300, c=color, 
                              marker='o', edgecolors='black', linewidth=2,
                              zorder=5, label=f"{i+1}. {point.name}")
                self.ax.annotate(f"{point.name}\n({point.x:.1f}, {point.y:.1f})",
                               xy=(point.x, point.y), xytext=(5, 5),
                               textcoords='offset points', fontsize=9,
                               bbox=dict(boxstyle='round', facecolor=color, alpha=0.7))
        
        # Dibujar antena exterior
        if tx_position:
            self.ax.scatter(*tx_position, s=400, marker='^', 
                          c='gold', edgecolors='red', linewidth=2,
                          zorder=6, label='Antena TX')
            self.ax.annotate('Antena\nExterior\n(25m)', xy=tx_position, 
                           xytext=(10, 10), textcoords='offset points',
                           fontsize=9, color='red', weight='bold',
                           bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))
        
        # Líneas de vista
        if tx_position and measurement_points:
            for point in measurement_points:
                self.ax.plot([tx_position[0], point.x], 
                           [tx_position[1], point.y],
                           'r--', alpha=0.3, linewidth=1)
        
        self.ax.set_xlabel('Distancia X (metros)', fontsize=11, weight='bold')
        self.ax.set_ylabel('Distancia Y (metros)', fontsize=11, weight='bold')
        self.ax.set_title(title, fontsize=13, weight='bold')
        self.ax.legend(loc='upper right', fontsize=9)
        self.ax.grid(True, alpha=0.3)
        self.ax.set_aspect('equal')
        
        return self.fig, self.ax
    
    def plot_signal_levels(self, measurement_data: pd.DataFrame,
                          services: List[str] = None):
        """
        Gráfico de comparación de niveles de señal por punto y servicio.
        
        Args:
            measurement_data: DataFrame con medidas
            services: Lista de servicios a mostrar
        """
        if services is None:
            services = ['voice', 'data_basic', 'data_medium']
        
        fig, axes = plt.subplots(1, len(services), figsize=(15, 5))
        if len(services) == 1:
            axes = [axes]
        
        for ax, service in zip(axes, services):
            # Datos simulados para visualización
            points = ['Entrada', 'Aula 2ª Planta', 'Semiótano']
            signal_dbm = [-95, -105, -115]
            
            colors = ['green' if s > -100 else 'orange' if s > -110 else 'red' 
                     for s in signal_dbm]
            
            bars = ax.barh(points, signal_dbm, color=colors, alpha=0.7, 
                          edgecolor='black', linewidth=1.5)
            ax.axvline(x=-100, color='blue', linestyle='--', linewidth=2, 
                      label='Umbral (ej.)')
            ax.set_xlabel('Nivel de Señal (dBm)', fontweight='bold')
            ax.set_title(f'Servicio: {service.upper()}', fontweight='bold')
            ax.grid(True, alpha=0.3, axis='x')
            ax.legend()
        
        plt.tight_layout()
        return fig
    
    def plot_frequency_comparison(self, frequencies: List['Frequency'],
                                 measurement_points: List = None):
        """
        Compara cobertura a diferentes frecuencias.
        
        Args:
            frequencies: Lista de objetos Frequency
            measurement_points: Puntos de medida
        """
        fig, ax = plt.subplots(figsize=(12, 6))
        
        freq_names = [f"{f.frequency_mhz:.0f} MHz\n({f.technology})" 
                     for f in frequencies]
        
        # Datos simulados como ejemplo
        point_names = ['Entrada', 'Aula 2ª', 'Semiótano']
        x = np.arange(len(point_names))
        width = 0.25
        
        for i, freq_name in enumerate(freq_names):
            # Simulación: frecuencias menores penetran mejor
            base_signal = -95
            penalty = (frequencies[i].frequency_mhz - 700) / 100
            signals = [base_signal, base_signal - 10 - penalty, 
                      base_signal - 20 - penalty]
            
            ax.bar(x + i * width, signals, width, label=freq_name,
                  alpha=0.8, edgecolor='black', linewidth=1)
        
        ax.set_ylabel('Nivel de Señal Interior (dBm)', fontweight='bold')
        ax.set_title('Comparativa de Cobertura por Frecuencia', fontweight='bold')
        ax.set_xticks(x + width)
        ax.set_xticklabels(point_names)
        ax.axhline(y=-100, color='red', linestyle='--', linewidth=2, alpha=0.7)
        ax.legend(loc='lower right', fontsize=9)
        ax.grid(True, alpha=0.3, axis='y')
        
        return fig


class ReportGenerator:
    """Genera reportes en formato tabular y textual."""
    
    @staticmethod
    def create_loss_table(measurement_points: List) -> pd.DataFrame:
        """
        Crea tabla resumen de pérdidas por punto.
        
        Args:
            measurement_points: Lista de puntos IndoorMeasurementPoint
            
        Returns:
            DataFrame con tabla de pérdidas
        """
        rows = []
        for point in measurement_points:
            row = {
                'Punto': point.name,
                'Ubicación': point.location,
                'Distancia Exterior (m)': point.distance_outdoor,
                'Fachada (dB)': point.penetration_losses.get('facade', 0),
                'Pared (dB)': point.penetration_losses.get('wall', 0),
                'Forjado (dB)': point.penetration_losses.get('floor', 0),
                'Total Penetración (dB)': sum(point.penetration_losses.values()),
                'Coordenadas (m)': f"({point.x:.1f}, {point.y:.1f}, {point.z:.1f})"
            }
            rows.append(row)
        
        return pd.DataFrame(rows)
    
    @staticmethod
    def create_service_coverage_table(measurements: pd.DataFrame,
                                     thresholds: Dict) -> pd.DataFrame:
        """
        Crea tabla de cobertura de servicios.
        
        Args:
            measurements: DataFrame con medidas
            thresholds: Dict con umbrales por servicio
            
        Returns:
            DataFrame con estado de servicios
        """
        rows = []
        for idx, row in measurements.iterrows():
            for service, threshold in thresholds.items():
                status = '✓' if row['indoor_signal_dbm'] >= threshold else '✗'
                rows.append({
                    'Punto': row['point_name'],
                    'Servicio': service,
                    'Umbral (dBm)': threshold,
                    'Señal (dBm)': row['indoor_signal_dbm'],
                    'Margen (dB)': row['indoor_signal_dbm'] - threshold,
                    'Estado': status
                })
        
        return pd.DataFrame(rows)
    
    @staticmethod
    def print_recommendations(measurements: pd.DataFrame) -> str:
        """
        Genera recomendaciones de mejora.
        
        Args:
            measurements: DataFrame con medidas
            
        Returns:
            String con recomendaciones
        """
        recommendations = []
        recommendations.append("=" * 70)
        recommendations.append("RECOMENDACIONES DE MEJORA DE COBERTURA")
        recommendations.append("=" * 70)
        
        # Analizar puntos críticos
        critical_points = measurements[measurements['indoor_signal_dbm'] < -110]
        
        if len(critical_points) > 0:
            recommendations.append("\n[CRÍTICO] Puntos sin cobertura:")
            for idx, point in critical_points.iterrows():
                recommendations.append(f"  • {point['point_name']}: {point['indoor_signal_dbm']:.1f} dBm")
                recommendations.append(f"    → Considerar DAS (Distributed Antenna System)")
        
        weak_points = measurements[
            (measurements['indoor_signal_dbm'] >= -110) & 
            (measurements['indoor_signal_dbm'] < -100)
        ]
        
        if len(weak_points) > 0:
            recommendations.append("\n[DÉBIL] Puntos con cobertura insuficiente:")
            for idx, point in weak_points.iterrows():
                recommendations.append(f"  • {point['point_name']}: {point['indoor_signal_dbm']:.1f} dBm")
                recommendations.append(f"    → Considerar repetidor de interior")
        
        good_points = measurements[measurements['indoor_signal_dbm'] >= -100]
        if len(good_points) > 0:
            recommendations.append(f"\n[BUENO] {len(good_points)} punto(s) con cobertura aceptable")
        
        recommendations.append("\n" + "=" * 70)
        
        return "\n".join(recommendations)
