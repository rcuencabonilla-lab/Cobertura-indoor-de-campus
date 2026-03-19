"""
Definición de datos del edificio modelo para el ejercicio práctico.
Incluye geometría, puntos de medida y parámetros de antena.
"""

import json
from typing import Dict, List

# Configuración del edificio modelo
BUILDING_MODEL = {
    'name': 'Edificio Rectorado - Campus Universitario',
    'description': 'Edificio de 4 plantas + semiótano técnico',
    'building': {
        'perimeter': {
            'x': 0,
            'y': 0,
            'width': 40,      # 40 metros de ancho
            'height': 60      # 60 metros de largo
        },
        'floors': [
            {
                'level': -1,
                'name': 'Semiótano técnico',
                'z_position': -5,
                'y_position': 20,
                'is_technical': True
            },
            {
                'level': 0,
                'name': 'Planta baja',
                'z_position': 0,
                'y_position': 30
            },
            {
                'level': 1,
                'name': 'Primera planta',
                'z_position': 3.5,
                'y_position': 40
            },
            {
                'level': 2,
                'name': 'Segunda planta',
                'z_position': 7,
                'y_position': 50
            }
        ],
        'interior_walls': [
            # Pared vertical central
            {'type': 'vertical', 'x': 20, 'y_start': 0, 'y_end': 60},
            # Paredes horizontales (dividen aulas)
            {'type': 'horizontal', 'x_start': 0, 'x_end': 40, 'y': 15},
            {'type': 'horizontal', 'x_start': 0, 'x_end': 40, 'y': 45},
        ],
        'construction_materials': {
            'facade': {
                'type': 'hormigón armado',
                'thickness_cm': 25,
                'loss_dB': 15  # Pérdida típica fachada
            },
            'interior_walls': {
                'type': 'ladrillo con yeso',
                'thickness_cm': 12,
                'loss_dB': 4   # Pérdida típica pared interior
            },
            'floor': {
                'type': 'hormigón + cerámica',
                'thickness_cm': 25,
                'loss_dB': 15  # Pérdida típica forjado
            }
        }
    },
    'antenna': {
        'position_x_m': -15,      # Fuera del edificio
        'position_y_m': -10,      # Fuera del edificio
        'height_m': 25,           # 25 metros altura
        'type': 'macro_cell',
        'gain_dbi': 17,
        'power_dbm': 43,          # 20W de potencia de salida
        'bearing': 45             # Orientación en grados
    },
    'reference_distances': {
        'to_facade': 45,          # Distancia aproximada a la fachada más cercana
        'to_building_center': 70  # Distancia al centro del edificio
    }
}

# Puntos de medida definidos por el alumno
MEASUREMENT_POINTS = [
    {
        'id': 1,
        'name': 'Entrada Principal',
        'location': 'Planta baja, vestigio externo',
        'x_m': 20,       # Centro del edificio en X
        'y_m': 5,        # Cerca de la entrada
        'z_m': 0,        # Planta baja
        'floor_level': 0,
        'description': 'Puerta de acceso principal. Señal debe permitir llamadas de emergencia.',
        'penetration_losses': {
            'facade': 15,  # Pared fachada
            'wall': 0,     # Sin pared interior
            'floor': 0     # Sin forjado
        }
    },
    {
        'id': 2,
        'name': 'Aula Segunda Planta',
        'location': 'Segunda planta, aula docente',
        'x_m': 35,       # Lado derecho del edificio
        'y_m': 50,       # Ala posterior
        'z_m': 7,        # Segunda planta (7 m de altura)
        'floor_level': 2,
        'description': 'Aula donde se imparten clases. Necesita cobertura para videollamadas.',
        'penetration_losses': {
            'facade': 0,   # No ve directamente exterior
            'wall': 4,     # Una pared interior
            'floor': 15    # Dos forjados (planta baja + primera)
        }
    },
    {
        'id': 3,
        'name': 'Semiótano Técnico',
        'location': 'Nivel -1, sala de servidores',
        'x_m': 10,       # Lado izquierdo
        'y_m': 20,       # Central
        'z_m': -5,       # Semiótano
        'floor_level': -1,
        'description': 'Sala técnica de armarios y servidores. Debe permitir acceso a plataformas.',
        'penetration_losses': {
            'facade': 15,  # Puede tener fachada cercana
            'wall': 4,     # Paredes perimetrales
            'floor': 15    # Un forjado arriba
        }
    }
]

# Portadoras de prueba (frecuencias)
FREQUENCIES = [
    {
        'band': '700 MHz',
        'frequency_mhz': 700,
        'technology': 'LTE',
        'bandwidth_mhz': 10,
        'power_dbm': 43,
        'notes': 'Baja pérdida de penetración, mejor cobertura'
    },
    {
        'band': 'LTE 800 MHz',
        'frequency_mhz': 800,
        'technology': 'LTE',
        'bandwidth_mhz': 10,
        'power_dbm': 43,
        'notes': 'Banda de cobertura, buena penetración'
    },
    {
        'band': 'LTE 1800 MHz',
        'frequency_mhz': 1800,
        'technology': 'LTE',
        'bandwidth_mhz': 20,
        'power_dbm': 43,
        'notes': 'Banda recomendada para el ejercicio'
    },
    {
        'band': 'UMTS 2100 MHz',
        'frequency_mhz': 2100,
        'technology': 'UMTS',
        'bandwidth_mhz': 5,
        'power_dbm': 43,
        'notes': 'Banda de respaldo con más pérdida'
    },
    {
        'band': '5G mmWave 26 GHz',
        'frequency_mhz': 26000,
        'technology': '5G NR',
        'bandwidth_mhz': 100,
        'power_dbm': 35,
        'notes': 'Altísimas pérdidas, casi sin penetración'
    }
]

# Parámetros de servicio y umbrales
SERVICE_REQUIREMENTS = {
    'voice': {
        'technology': 'VoLTE/CS',
        'min_signal_dbm': -100,
        'required_snir_db': 5,
        'services': ['LTE', 'UMTS'],
        'description': 'Voz (llamadas de emergencia, comunicaciónes normales)'
    },
    'sms': {
        'min_signal_dbm': -105,
        'required_snir_db': 2,
        'services': ['LTE', 'UMTS'],
        'description': 'Mensajería de texto'
    },
    'data_basic': {
        'min_signal_dbm': -95,
        'min_throughput_mbps': 0.5,
        'services': ['LTE', 'UMTS', '5G'],
        'description': 'Datos móviles básicos (notificaciones, mapas)'
    },
    'data_medium': {
        'min_signal_dbm': -85,
        'min_throughput_mbps': 5,
        'services': ['LTE', '5G'],
        'description': 'Videoconferencia, streaming'
    },
    'data_high': {
        'min_signal_dbm': -75,
        'min_throughput_mbps': 25,
        'services': ['LTE', '5G'],
        'description': 'Descarga/upload rápido'
    }
}

# Soluciones de mejora de cobertura
COVERAGE_SOLUTIONS = {
    'macro_cell': {
        'name': 'Macro celda exterior',
        'cost': 'Alto (50k-100k€)',
        'deployment_time': '2-3 meses',
        'coverage_area': 'Todo el edificio',
        'improvement_db': '15-25',
        'suitability': 'Para zonas grandes con múltiples edificios'
    },
    'das': {
        'name': 'DAS (Distributed Antenna System)',
        'cost': 'Muy alto (100k-300k€)',
        'deployment_time': '3-6 meses',
        'coverage_area': 'Todo el edificio uniformemente',
        'improvement_db': '20-30',
        'suitability': 'Para edificios grandes con múltiples plantas y zonas débiles'
    },
    'small_cell': {
        'name': 'Small cell (femto/pico)',
        'cost': 'Medio (15k-30k€)',
        'deployment_time': '2-4 semanas',
        'coverage_area': 'Zonas específicas',
        'improvement_db': '15-20',
        'suitability': 'Para puntos críticos específicos'
    },
    'repeater': {
        'name': 'Repetidor de interior',
        'cost': 'Bajo (3k-8k€)',
        'deployment_time': '1-2 semanas',
        'coverage_area': 'Zonas locales',
        'improvement_db': '10-15',
        'suitability': 'Para mejorar cobertura puntual sin complicar red'
    },
    'no_action': {
        'name': 'Sin mejora (solo cobertura macro)',
        'cost': '0€',
        'deployment_time': '0',
        'coverage_area': 'Limitado',
        'improvement_db': '0',
        'suitability': 'Si la cobertura macro es suficiente'
    }
}

def get_building():
    """Retorna configuración del edificio."""
    return BUILDING_MODEL

def get_measurement_points():
    """Retorna lista de puntos de medida."""
    return MEASUREMENT_POINTS

def get_frequencies():
    """Retorna lista de frecuencias a probar."""
    return FREQUENCIES

def get_service_requirements():
    """Retorna requisitos de servicio."""
    return SERVICE_REQUIREMENTS

def get_coverage_solutions():
    """Retorna soluciones de mejora disponibles."""
    return COVERAGE_SOLUTIONS

# Exportar como JSON para uso en QGIS o herramientas externas
def export_to_json(filename: str = 'building_model.json'):
    """Exporta el modelo del edificio a JSON."""
    data = {
        'building': BUILDING_MODEL,
        'measurement_points': MEASUREMENT_POINTS,
        'frequencies': FREQUENCIES,
        'service_requirements': SERVICE_REQUIREMENTS,
        'coverage_solutions': COVERAGE_SOLUTIONS
    }
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Modelo exportado a {filename}")
