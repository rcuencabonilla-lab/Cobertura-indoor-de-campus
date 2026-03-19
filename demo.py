#!/usr/bin/env python3
"""
Script de demostración rápida del análisis de cobertura indoor.
Ejecutar: python3 demo.py
"""

import sys
import warnings
warnings.filterwarnings('ignore')

# Importar módulos del proyecto
sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')

from src.propagation import (
    Frequency, PropagationModel, ServiceThreshold, 
    IndoorMeasurementPoint
)
from data.building_model import (
    get_building, get_measurement_points, get_frequencies, 
    get_service_requirements, get_coverage_solutions
)

def print_header(title):
    """Imprime encabezado formateado."""
    print(f"\n{'='*70}")
    print(f" {title.upper()}")
    print(f"{'='*70}\n")

def main():
    """Función principal de demostración."""
    
    print_header("DEMO: Análisis de Cobertura Indoor en Campus")
    
    # 1. Cargar datos del edificio
    building = get_building()
    points = get_measurement_points()
    
    print(f"Edificio: {building['name']}")
    print(f"Altura antena: {building['antenna']['height_m']} m")
    print(f"Puntos de evaluación: {len(points)}\n")
    
    # 2. Definir portadora principal
    freq_1800 = Frequency(
        name='LTE 1800 MHz',
        frequency_mhz=1800,
        technology='LTE',
        bandwidth_mhz=20,
        power_dbm=43
    )
    
    print(f"Portadora: {freq_1800.name}")
    print(f"Longitud onda: {freq_1800.wavelength_m:.4f} m")
    print(f"Potencia: {freq_1800.power_dbm} dBm\n")
    
    # 3. Calcular cobertura en cada punto
    print_header("CÁLCULOS DE COBERTURA")
    
    results = []
    tx_pos = (building['antenna']['position_x_m'],
              building['antenna']['position_y_m'])
    tx_height = building['antenna']['height_m']
    
    for point in points:
        # Distancia 3D
        dx = point['x_m'] - tx_pos[0]
        dy = point['y_m'] - tx_pos[1]
        dz = point['z_m'] - tx_height
        distance_3d = (dx**2 + dy**2 + dz**2) ** 0.5
        
        # Pérdida propagación
        loss_prop = PropagationModel.free_space_loss(freq_1800, distance_3d)
        
        # Pérdida penetración
        loss_penet = sum(point['penetration_losses'].values())
        
        # Nivel recibido (EIRP - pérdidas)
        eirp = 43 + 17  # power + gain
        rx_level = eirp - loss_prop - loss_penet
        
        # Comprobar servicio voz
        voz_ok = rx_level >= -100
        
        result = {
            'punto': point['name'],
            'distancia': distance_3d,
            'loss_prop': loss_prop,
            'loss_penet': loss_penet,
            'rx_level': rx_level,
            'voz_ok': voz_ok,
        }
        results.append(result)
        
        # Mostrar resultado
        status = "✓" if voz_ok else "✗"
        print(f"{status} {point['name']:25}")
        print(f"   Distancia: {distance_3d:.1f} m")
        print(f"   Pérdida propagación: {loss_prop:.1f} dB")
        print(f"   Pérdida penetración: {loss_penet:.1f} dB")
        print(f"   Nivel recibido: {rx_level:.1f} dBm")
        print(f"   Margen voz (-100 dBm): {rx_level - (-100):.1f} dB")
        print()
    
    # 4. Resumen
    print_header("RESUMEN EJECUTIVO")
    
    cobertura_ok = sum(1 for r in results if r['voz_ok'])
    cobertura_total = len(results)
    
    print(f"Puntos con cobertura OK: {cobertura_ok}/{cobertura_total}")
    
    if cobertura_ok == cobertura_total:
        print("\n✓ CONCLUSIÓN: Cobertura macro suficiente.")
        print("  No se requiere DAS, Small Cell o Repetidor.")
    else:
        print("\n⚠ CONCLUSIÓN: Se detectan puntos débiles.")
        print("  Considerar refuerzo indoor (Small Cell o Repetidor).")
    
    # 5. Comparativa de frecuencias
    print_header("COMPARATIVA: 700 MHz vs 1800 MHz vs 2600 MHz")
    
    frequencies = {
        '700': Frequency('LTE 700 MHz', 700, 'LTE', 10, 43),
        '1800': Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43),
        '2600': Frequency('5G 2600 MHz', 2600, '5G NR', 100, 40),
    }
    
    for point in points[:1]:  # Mostrar solo para primer punto
        print(f"\n{point['name']}:")
        dx = point['x_m'] - tx_pos[0]
        dy = point['y_m'] - tx_pos[1]
        dz = point['z_m'] - tx_height
        distance_3d = (dx**2 + dy**2 + dz**2) ** 0.5
        
        for band, freq in frequencies.items():
            loss_prop = PropagationModel.free_space_loss(freq, distance_3d)
            loss_penet = sum(point['penetration_losses'].values())
            rx_level = freq.power_dbm + 17 - loss_prop - loss_penet
            
            voz_ok = "✓" if rx_level >= -100 else "✗"
            print(f"  {freq.name:20} {rx_level:6.1f} dBm {voz_ok}")
    
    print("\n" + "="*70)
    print(" Para análisis completo, ejecuta:")
    print(" jupyter notebook notebooks/Ejercicio_Cobertura_Indoor.ipynb")
    print("="*70 + "\n")

if __name__ == '__main__':
    main()
