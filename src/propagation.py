"""
Módulo de cálculos de propagación para cobertura indoor.
Implementa modelos de pérdida de camino y penetración en edificios.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass
from typing import Dict, List, Tuple


@dataclass
class Frequency:
    """Definición de una portadora celular."""
    name: str
    frequency_mhz: float
    technology: str  # LTE, UMTS, 5G
    bandwidth_mhz: float
    power_dbm: float
    
    @property
    def wavelength_m(self) -> float:
        """Calcula la longitud de onda en metros."""
        c = 3e8  # velocidad de la luz
        return c / (self.frequency_mhz * 1e6)
    
    @property
    def path_loss_coefficient(self) -> float:
        """Coeficiente para cálculo de pérdida de propagación.
        
        Fórmula de Friis simplificada para f en MHz, d en m:
        L = 20*log10(f) + 20*log10(d) + 32.45
        
        Este método retorna: 20*log10(f) + 32.45
        """
        return 20 * np.log10(self.frequency_mhz) + 32.45


class PropagationModel:
    """Modelo de propagación en espacios libres y con obstáculos."""
    
    @staticmethod
    def free_space_loss(frequency: Frequency, distance_m: float) -> float:
        """
        Calcula la pérdida en espacio libre (Friis).
        
        Args:
            frequency: Objeto Frequency con parámetros de la portadora
            distance_m: Distancia en metros
            
        Returns:
            Pérdida en dB (positiva)
        """
        if distance_m <= 0:
            return 0
        
        # L = 20*log10(f_MHz) + 20*log10(d_m) + 20*log10(4π/c)
        loss = frequency.path_loss_coefficient + 20 * np.log10(distance_m)
        return loss
    
    @staticmethod
    def okumura_hata(frequency: Frequency, distance_m: float, 
                     tx_height_m: float = 25, rx_height_m: float = 1.5,
                     urban_factor: float = 1.0) -> float:
        """
        Modelo Okumura-Hata para propagación en entorno urbano.
        Válido para frecuencias 150-1500 MHz y distancias 1-20 km.
        
        Args:
            frequency: Objeto Frequency
            distance_m: Distancia en metros
            tx_height_m: Altura de la antena transmisora (m)
            rx_height_m: Altura de la antena receptora (m)
            urban_factor: Factor de corrección urbana (1.0 = urbano denso)
            
        Returns:
            Pérdida en dB
        """
        f_mhz = frequency.frequency_mhz
        d_km = distance_m / 1000
        
        # Modelo base Hata
        loss = (69.55 + 26.16 * np.log10(f_mhz) - 13.82 * np.log10(tx_height_m) +
                (44.9 - 6.55 * np.log10(tx_height_m)) * np.log10(d_km))
        
        # Corrección por altura de receptor
        a_hm = (1.1 * np.log10(f_mhz) - 0.7) * rx_height_m - (1.56 * np.log10(f_mhz) - 0.8)
        loss = loss - a_hm
        
        # Factor urbano
        loss = loss + (6 if urban_factor > 0.8 else -2)
        
        return loss
    
    @staticmethod
    def add_penetration_losses(outdoor_signal: float, 
                              losses_dict: Dict[str, float]) -> Tuple[float, Dict]:
        """
        Suma las pérdidas de penetración a la señal exterior.
        
        Args:
            outdoor_signal: Nivel de señal exterior en dBm
            losses_dict: Diccionario con pérdidas en dB
                Ej: {'facade': 15, 'wall': 4, 'floor': 15}
                
        Returns:
            Tupla (nivel_interior_dbm, diccionario_con_detalles)
        """
        total_penetration_dB = sum(losses_dict.values())
        indoor_signal = outdoor_signal - total_penetration_dB
        
        details = {
            'outdoor_signal_dbm': outdoor_signal,
            'total_penetration_dB': total_penetration_dB,
            'indoor_signal_dbm': indoor_signal,
            'penetration_breakdown': losses_dict.copy()
        }
        
        return indoor_signal, details


class ServiceThreshold:
    """Umbrales de recepción para diferentes servicios."""
    
    # Umbrales típicos en dBm
    THRESHOLDS = {
        'voice': {
            'lte': -100,      # LTE voz (VoLTE)
            'umts': -98,      # UMTS voz (CS)
            '5g': -102        # 5G NR voz
        },
        'data_basic': {
            'lte': -95,       # Datos móviles básicos
            'umts': -95,
            '5g': -95
        },
        'data_medium': {
            'lte': -85,       # Streaming, videoconferencia
            'umts': -85,
            '5g': -85
        },
        'data_high': {
            'lte': -75,       # Descarga/upload rápido
            'umts': -75,
            '5g': -75
        }
    }
    
    @classmethod
    def check_service(cls, signal_dbm: float, service: str, 
                     technology: str) -> Dict:
        """
        Verifica si se alcanza servicio para señal recibida.
        
        Args:
            signal_dbm: Nivel de señal en dBm
            service: 'voice', 'data_basic', 'data_medium', 'data_high'
            technology: 'lte', 'umts', '5g'
            
        Returns:
            Diccionario con resultado
        """
        if service not in cls.THRESHOLDS:
            raise ValueError(f"Servicio desconocido: {service}")
        
        threshold = cls.THRESHOLDS[service][technology]
        is_ok = signal_dbm >= threshold
        margin = signal_dbm - threshold
        
        return {
            'service': service,
            'technology': technology,
            'threshold_dbm': threshold,
            'signal_dbm': signal_dbm,
            'is_ok': is_ok,
            'margin_dB': margin,
            'status': '✓ OK' if is_ok else '✗ FALLA'
        }


class IndoorMeasurementPoint:
    """Define un punto de medida dentro del edificio."""
    
    def __init__(self, name: str, location: str, 
                 x_m: float, y_m: float, z_m: float,
                 distance_outdoor_m: float,
                 penetration_losses: Dict[str, float]):
        """
        Args:
            name: Nombre del punto (ej: "Entrada")
            location: Descripción (ej: "Planta baja, acceso principal")
            x_m, y_m, z_m: Coordenadas en metros
            distance_outdoor_m: Distancia a antena exterior en metros
            penetration_losses: Dict con pérdidas por obstáculos
        """
        self.name = name
        self.location = location
        self.x = x_m
        self.y = y_m
        self.z = z_m
        self.distance_outdoor = distance_outdoor_m
        self.penetration_losses = penetration_losses
        self.measurements = pd.DataFrame()
    
    def add_measurement(self, frequency: Frequency, 
                       outdoor_signal_dbm: float):
        """Registra una medida en este punto."""
        # Calcular señal interior
        indoor_signal, details = PropagationModel.add_penetration_losses(
            outdoor_signal_dbm, self.penetration_losses
        )
        
        measurement = {
            'frequency_mhz': frequency.frequency_mhz,
            'technology': frequency.technology,
            'outdoor_signal_dbm': outdoor_signal_dbm,
            'indoor_signal_dbm': indoor_signal,
            'total_loss_dB': outdoor_signal_dbm - indoor_signal,
            'penetration_loss_dB': sum(self.penetration_losses.values())
        }
        
        self.measurements = pd.concat([
            self.measurements, 
            pd.DataFrame([measurement])
        ], ignore_index=True)
    
    def to_dict(self):
        """Convierte a diccionario para reporting."""
        return {
            'name': self.name,
            'location': self.location,
            'coordinates': (self.x, self.y, self.z),
            'distance_outdoor_m': self.distance_outdoor,
            'penetration_losses': self.penetration_losses,
            'measurements_count': len(self.measurements)
        }
