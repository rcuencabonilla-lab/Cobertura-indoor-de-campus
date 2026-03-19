"""
Ejemplos Avanzados de Uso del Módulo de Cobertura Indoor

Estos scripts demuestran usos prácticos más allá del notebook principal.
"""

# ============================================================================
# EJEMPLO 1: Análisis Paramétrico - Variando Altura de Antena
# ============================================================================

def ejemplo_variacion_altura():
    """Analiza cómo cambia cobertura al variar altura de antena."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    from data.building_model import get_measurement_points, get_building
    import numpy as np
    import matplotlib.pyplot as plt
    
    freq = Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43)
    points = get_measurement_points()
    building = get_building()
    
    heights = [15, 20, 25, 30, 35, 40]
    results = {point['name']: [] for point in points}
    
    tx_pos = (building['antenna']['position_x_m'],
              building['antenna']['position_y_m'])
    
    for h in heights:
        for point in points:
            dx = point['x_m'] - tx_pos[0]
            dy = point['y_m'] - tx_pos[1]
            dz = point['z_m'] - h
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            
            loss = PropagationModel.free_space_loss(freq, distance)
            penetration = sum(point['penetration_losses'].values())
            rx_level = 60 - loss - penetration
            results[point['name']].append(rx_level)
    
    # Graficar
    plt.figure(figsize=(10, 6))
    for point_name in results:
        plt.plot(heights, results[point_name], marker='o', label=point_name)
    
    plt.axhline(y=-100, color='red', linestyle='--', label='Umbral Voz')
    plt.xlabel('Altura Antena (metros)')
    plt.ylabel('Nivel Recibido (dBm)')
    plt.title('Análisis de Cobertura vs. Altura de Antena')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('/tmp/altura_analysis.png', dpi=100)
    print("✓ Gráfico guardado: /tmp/altura_analysis.png")


# ============================================================================
# EJEMPLO 2: Optimización - Buscar Altura Mínima para Cobertura Total
# ============================================================================

def ejemplo_optimizacion_altura():
    """Encuentra la altura mínima de antena para cobertura completa."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    from data.building_model import get_measurement_points, get_building
    import numpy as np
    
    freq = Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43)
    points = get_measurement_points()
    building = get_building()
    
    tx_pos = (building['antenna']['position_x_m'],
              building['antenna']['position_y_m'])
    
    # Búsqueda binaria para altura mínima
    min_height = 5
    max_height = 50
    threshold_voz = -100
    
    while max_height - min_height > 0.5:
        mid_height = (min_height + max_height) / 2
        all_ok = True
        
        for point in points:
            dx = point['x_m'] - tx_pos[0]
            dy = point['y_m'] - tx_pos[1]
            dz = point['z_m'] - mid_height
            distance = np.sqrt(dx**2 + dy**2 + dz**2)
            
            loss = PropagationModel.free_space_loss(freq, distance)
            penetration = sum(point['penetration_losses'].values())
            rx_level = 60 - loss - penetration
            
            if rx_level < threshold_voz:
                all_ok = False
                break
        
        if all_ok:
            max_height = mid_height
        else:
            min_height = mid_height
    
    print(f"\n✓ Altura mínima para cobertura total: {max_height:.1f} metros")
    return max_height


# ============================================================================
# EJEMPLO 3: Análisis de Ganancia Requerida Por Punto
# ============================================================================

def ejemplo_ganancia_requerida():
    """Calcula ganancia necesaria en cada punto para alcanzar servicio."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    from data.building_model import get_measurement_points, get_building
    import numpy as np
    import pandas as pd
    
    freq = Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43)
    points = get_measurement_points()
    building = get_building()
    
    tx_pos = (building['antenna']['position_x_m'],
              building['antenna']['position_y_m'])
    
    solutions = []
    
    for point in points:
        dx = point['x_m'] - tx_pos[0]
        dy = point['y_m'] - tx_pos[1]
        dz = point['z_m'] - building['antenna']['height_m']
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        
        loss = PropagationModel.free_space_loss(freq, distance)
        penetration = sum(point['penetration_losses'].values())
        rx_level = 60 - loss - penetration
        
        # Ganancia requerida para alcanzar -100 dBm (voz)
        gain_needed = max(0, -100 - rx_level)
        
        # Seleccionar solución
        if gain_needed == 0:
            solution = "Sin mejora"
            cost = "0€"
        elif gain_needed <= 10:
            solution = "Repetidor"
            cost = "3k-8k€"
        elif gain_needed <= 15:
            solution = "Small Cell"
            cost = "15k-30k€"
        else:
            solution = "DAS"
            cost = "100k-300k€"
        
        solutions.append({
            'Punto': point['name'],
            'Nivel Actual (dBm)': round(rx_level, 1),
            'Ganancia Requerida (dB)': round(gain_needed, 1),
            'Solución Recomendada': solution,
            'Costo Aprox.': cost
        })
    
    df = pd.DataFrame(solutions)
    print("\n" + "="*80)
    print("ANÁLISIS DE GANANCIA REQUERIDA Y SOLUCIONES")
    print("="*80)
    print(df.to_string(index=False))
    print("="*80 + "\n")


# ============================================================================
# EJEMPLO 4: Comparación Multiparamétrica (3D Surface Plot)
# ============================================================================

def ejemplo_superficie_cobertura():
    """Crea una superficie 3D de cobertura en función de frecuencia y distancia."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    import numpy as np
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    
    # Rango de parámetros
    frequencies_mhz = np.linspace(700, 2600, 20)
    distances_m = np.linspace(40, 150, 20)
    
    # Crear malla
    F, D = np.meshgrid(frequencies_mhz, distances_m)
    Z = np.zeros_like(F)
    
    # Calcular pérdida para cada combinación
    for i in range(len(frequencies_mhz)):
        for j in range(len(distances_m)):
            freq = Frequency(f'Test', frequencies_mhz[i], 'LTE', 20, 43)
            loss = PropagationModel.free_space_loss(freq, distances_m[j])
            Z[j, i] = 60 - loss - 25  # EIRP - pérdida - penetración típica
    
    # Graficar superficie
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    surf = ax.plot_surface(F, D, Z, cmap='RdYlGn', alpha=0.8)
    ax.set_xlabel('Frecuencia (MHz)')
    ax.set_ylabel('Distancia (m)')
    ax.set_zlabel('Nivel Recibido (dBm)')
    ax.set_title('Superficie de Cobertura: Frecuencia vs Distancia')
    
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.tight_layout()
    plt.savefig('/tmp/superficie_cobertura.png', dpi=100, bbox_inches='tight')
    print("✓ Superficie 3D guardada: /tmp/superficie_cobertura.png")


# ============================================================================
# EJEMPLO 5: Análisis de Interferencia Cochannel
# ============================================================================

def ejemplo_interferencia():
    """Analiza interferencia entre dos edificios en misma banda."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    import numpy as np
    
    # Edificio 1 (de interés)
    tx1_pos = (-15, -10)
    tx1_height = 25
    tx1_power = 43 + 17  # EIRP
    
    # Edificio 2 (interferente)
    tx2_pos = (-15 + 500, -10)  # A 500m de distancia
    tx2_height = 30
    tx2_power = 43 + 17  # EIRP
    
    freq = Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43)
    
    # Punto de interés (dentro edificio 1)
    point = (20, 30, 0)
    
    # Distancia a TX1 (deseado)
    d1 = np.sqrt((point[0]-tx1_pos[0])**2 + (point[1]-tx1_pos[1])**2 + 
                 (point[2]-tx1_height)**2)
    loss1 = PropagationModel.free_space_loss(freq, d1)
    rx_desired = tx1_power - loss1 - 25  # Con penetración
    
    # Distancia a TX2 (interferente)
    d2 = np.sqrt((point[0]-tx2_pos[0])**2 + (point[1]-tx2_pos[1])**2 + 
                 (point[2]-tx2_height)**2)
    loss2 = PropagationModel.free_space_loss(freq, d2)
    rx_interferer = tx2_power - loss2 - 25
    
    # Ratio C/I
    c_i_ratio = rx_desired - rx_interferer
    
    print(f"\n{'='*60}")
    print("ANÁLISIS DE INTERFERENCIA COCHANNEL")
    print(f"{'='*60}")
    print(f"Señal deseada (TX1): {rx_desired:.1f} dBm")
    print(f"Señal interferente (TX2): {rx_interferer:.1f} dBm")
    print(f"Distancia TX2: {d2:.0f} m")
    print(f"Ratio C/I: {c_i_ratio:.1f} dB")
    print(f"\nC/I requerido para LTE: típicamente > 0 dB")
    if c_i_ratio > 0:
        print("✓ Coexistencia VIABLE")
    else:
        print("✗ Necesario mejorar aislamiento o cambiar frecuencias")
    print(f"{'='*60}\n")


# ============================================================================
# EJEMPLO 6: Generar Reportes en Diferentes Formatos
# ============================================================================

def ejemplo_exportar_reportes():
    """Exporta resultados en CSV, JSON y TXT."""
    import sys
    sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
    
    from src.propagation import Frequency, PropagationModel
    from data.building_model import get_measurement_points, get_building
    import numpy as np
    import pandas as pd
    import json
    
    freq = Frequency('LTE 1800 MHz', 1800, 'LTE', 20, 43)
    points = get_measurement_points()
    building = get_building()
    
    tx_pos = (building['antenna']['position_x_m'],
              building['antenna']['position_y_m'])
    
    results = []
    
    for point in points:
        dx = point['x_m'] - tx_pos[0]
        dy = point['y_m'] - tx_pos[1]
        dz = point['z_m'] - building['antenna']['height_m']
        distance = np.sqrt(dx**2 + dy**2 + dz**2)
        
        loss = PropagationModel.free_space_loss(freq, distance)
        penetration = sum(point['penetration_losses'].values())
        rx_level = 60 - loss - penetration
        
        results.append({
            'punto': point['name'],
            'ubicacion': point['location'],
            'distancia_m': round(distance, 1),
            'nivel_dbm': round(rx_level, 1),
            'margen_voz_db': round(rx_level - (-100), 1)
        })
    
    # Exportar CSV
    df = pd.DataFrame(results)
    df.to_csv('/tmp/cobertura_results.csv', index=False)
    print("✓ CSV: /tmp/cobertura_results.csv")
    
    # Exportar JSON
    with open('/tmp/cobertura_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("✓ JSON: /tmp/cobertura_results.json")
    
    # Exportar TXT
    with open('/tmp/cobertura_results.txt', 'w') as f:
        f.write("RESULTADOS DE COBERTURA\n")
        f.write("="*60 + "\n\n")
        f.write(df.to_string(index=False))
    print("✓ TXT: /tmp/cobertura_results.txt")


# ============================================================================
# FUNCIÓN MAIN PARA EJECUTAR EJEMPLOS
# ============================================================================

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        example = sys.argv[1]
        
        if example == '1':
            print("Ejecutando: Variación de Altura")
            ejemplo_variacion_altura()
        elif example == '2':
            print("Ejecutando: Optimización de Altura")
            ejemplo_optimizacion_altura()
        elif example == '3':
            print("Ejecutando: Ganancia Requerida")
            ejemplo_ganancia_requerida()
        elif example == '4':
            print("Ejecutando: Superficie 3D")
            ejemplo_superficie_cobertura()
        elif example == '5':
            print("Ejecutando: Análisis de Interferencia")
            ejemplo_interferencia()
        elif example == '6':
            print("Ejecutando: Exportar Reportes")
            ejemplo_exportar_reportes()
        else:
            print(f"Ejemplo {example} no encontrado")
    else:
        print("""
Ejemplos Avanzados Disponibles:

python3 ejemplos_avanzados.py 1    # Variación de altura de antena
python3 ejemplos_avanzados.py 2    # Optimizar altura para cobertura total
python3 ejemplos_avanzados.py 3    # Calcular ganancia requerida por punto
python3 ejemplos_avanzados.py 4    # Generar superficie 3D de cobertura
python3 ejemplos_avanzados.py 5    # Análisis de interferencia entre operadores
python3 ejemplos_avanzados.py 6    # Exportar resultados en múltiples formatos

Ejemplo:
    python3 ejemplos_avanzados.py 1
        """)
