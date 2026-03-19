# Proyecto Cobertura Indoor de Campus - Resumen Ejecutivo

## 📋 Descripción

Ejercicio práctico interactivo de ingeniería de telecomunicaciones que permite analizar la cobertura celular en un edificio de varias plantas y proponer soluciones de mejora de cobertura indoor. 

**Tecnologías utilizadas:** Python 3, Jupyter Notebook, Pandas, NumPy, Matplotlib

## 🎯 Objetivos Educativos

Los alumnos aprenderán a:

1. **Calcular pérdidas de propagación** usando modelo Friis (espacio libre)
2. **Evaluar penetración de señal** a través de elementos constructivos (hormigón, ladrillo, forjados)
3. **Determinar necesidad de refuerzo indoor** comparando múltiples tecnologías
4. **Generar presupuestos** de soluciones DAS, Small Cell o Repetidor
5. **Comparar viabilidad** según diferentes bandas de frecuencia

## 📁 Estructura del Proyecto

```
Cobertura-indoor-de-campus/
│
├── README.md                          # Guía general del proyecto
├── requirements.txt                   # Dependencias Python
├── demo.py                            # Script de demostración rápida
│
├── notebooks/
│   └── Ejercicio_Cobertura_Indoor.ipynb   # ⭐ NOTEBOOK PRINCIPAL
│
├── src/                               # Módulos Python reutilizables
│   ├── __init__.py
│   ├── propagation.py                 # Cálculos de propagación RF
│   └── visualization.py               # Gráficos y visualizaciones
│
├── data/
│   └── building_model.py              # Modelo del edificio y parámetros
│
└── docs/
    ├── GUIA_ESTUDIANTE.md             # Paso a paso con tareas prácticas
    ├── TECNICA.md                     # Fundamentos teóricos completos
    └── QGIS_INTEGRACION.md            # Exportación a herramientas GIS
```

## 🚀 Inicio Rápido

### Opción 1: Script de Demostración (Sin Jupyter)

```bash
cd /workspaces/Cobertura-indoor-de-campus

# Instalar dependencias (primera vez)
pip install -r requirements.txt

# Ejecutar demostración
python3 demo.py
```

**Salida esperada:**
```
✓ Entrada Principal        -85.7 dBm (margen 14.3 dB)
✓ Aula Segunda Planta      -94.6 dBm (margen 5.4 dB)
✗ Semiótano Técnico        -105.4 dBm (margen -5.4 dB) ← Necesita refuerzo
```

### Opción 2: Notebook Interactivo (Recomendado)

```bash
# En VS Code
code /workspaces/Cobertura-indoor-de-campus/notebooks/Ejercicio_Cobertura_Indoor.ipynb

# O en Jupyter Lab
jupyter lab --allow-root
# Navegar a: notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

## 📊 Contenido del Notebook

| Sección | Actividad | Salida |
|---------|-----------|--------|
| 1-2 | Importar librerías y definir parámetros | Confirmación ✓ |
| 3-4 | Calcular pérdidas de propagación exterior | Tabla de pérdidas |
| 5 | Modelar penetración interior | Tabla de penetración |
| 6-7 | Evaluar cobertura en 3 puntos | Tabla de evaluación |
| 8-9 | Visualizar plano y gráficos | Mapas + gráficos |
| 10-11 | Análisis de soluciones de mejora | Tabla de opciones |
| 12 | Comparativa de frecuencias (700-2600 MHz) | Tabla + gráfico comparativo |
| 13 | Resumen ejecutivo | Recomendación final |

## 🏢 Escenario de Estudio

### Edificio Modelo

- **Nombre:** Rectorado del Campus Universitario
- **Estructura:** 4 plantas + semiótano técnico
- **Materiales:** Hormigón armado y ladrillo

### Puntos de Evaluación

| Punto | Ubicación | Elevación | Motivo |
|-------|-----------|-----------|--------|
| **Entrada Principal** | Planta baja, acceso | 0 m | Servicios básicos |
| **Aula Segunda Planta** | Interior, 2ª planta | +7 m | Videoconferencia |
| **Semiótano Técnico** | Subterráneo | -5 m | Infraestructura, datos |

### Parámetros de Antena

- **Ubicación:** ~45 metros del edificio, posición (-15, -10)
- **Altura:** 25 metros (macro celda estándar)
- **Potencia:** 43 dBm (20 W)
- **Ganancia:** 17 dBi (panel típico)
- **EIRP:** 60 dBm

## 📈 Resultados Típicos

### Cobertura LTE 1800 MHz (Principal)

```
COBERTURA:
├─ Entrada Principal:        -85.7 dBm  ✓ BUENA   (margen 14.3 dB)
├─ Aula Segunda Planta:      -94.6 dBm  ✓ BUENA   (margen 5.4 dB, marginal)
└─ Semiótano Técnico:       -105.4 dBm  ✗ CRÍTICA (margen -5.4 dB)

DECISIÓN: Refuerzo necesario en semiótano
SOLUCIÓN RECOMENDADA: Small Cell o Repetidor (10-15 dB)
PRESUPUESTO ESTIMADO: 15k-30k€ (Small Cell)
PLAZO: 2-4 semanas
```

### Comparativa de Frecuencias

```
                700 MHz    1800 MHz   2600 MHz
Entrada:      -77.5 dBm  -85.7 dBm  -91.9 dBm  ✓
Aula 2ª:      -86.3 dBm  -94.6 dBm -100.9 dBm  ⚠
Semiótano:    -97.2 dBm -105.4 dBm -111.6 dBm  ✗

Ventaja de 700 MHz: ~8 dB mejor que 1800 MHz
Ventaja en penetración interior clara
```

## 🔧 Módulos Principales

### `src/propagation.py`

**Clases:**
- `Frequency`: Definición de portadora (frecuencia, potencia, tecnología)
- `PropagationModel`: Cálculo de pérdidas Friis y métodos de propagación
- `ServiceThreshold`: Umbrales de recepción por servicio
- `IndoorMeasurementPoint`: Punto de medida con coordenadas y pérdidas

**Métodos clave:**
```python
# Calcular pérdida en espacio libre
loss = PropagationModel.free_space_loss(frequency, distance_m)

# Sumar pérdidas de penetración
indoor_signal, details = PropagationModel.add_penetration_losses(
    outdoor_signal, {'facade': 15, 'wall': 4, 'floor': 15}
)

# Verificar umbral de servicio
result = ServiceThreshold.check_service(signal_dbm, 'voice', 'LTE')
```

### `src/visualization.py`

**Clases:**
- `BuildingVisualization`: Gráficos de plano del edificio y cobertura
- `ReportGenerator`: Generación de tablas y reportes

**Métodos clave:**
```python
# Visualizar plano del edificio
visualizer.plot_building_layout(building_data, points, tx_position)

# Gráficos de nivel de señal
visualizer.plot_signal_levels(measurements, services)

# Crear tablas de pérdidas
table = ReportGenerator.create_loss_table(points)
```

### `data/building_model.py`

Exporta:
- `BUILDING_MODEL`: Geometría del edificio (perimeter, walls, floors)
- `MEASUREMENT_POINTS`: 3 puntos de prueba con coordenadas
- `FREQUENCIES`: Portadoras a estudiar (700-2600 MHz)
- `SERVICE_REQUIREMENTS`: Umbrales por tecnología
- `COVERAGE_SOLUTIONS`: Opciones de mejora (DAS, SC, repetidor)

## 📚 Documentación

### Para Alumnos
- **[docs/GUIA_ESTUDIANTE.md](docs/GUIA_ESTUDIANTE.md)** - Explicaciones paso a paso, tareas prácticas

### Para Docentes
- **[docs/TECNICA.md](docs/TECNICA.md)** - Fundamentos teóricos, ecuaciones, extensiones

### Para Análisis Avanzado
- **[docs/QGIS_INTEGRACION.md](docs/QGIS_INTEGRACION.md)** - Exportación a QGIS y herramientas GIS

## 🎓 Conceptos Cubiertos

### Teoría RF
- Fórmula de Friis (propagación en espacio libre)
- Pérdidas de penetración en edificios
- Presupuesto de enlace (link budget)
- Umbrales de servicio (3GPP)

### Prácticas de Ingeniería
- Análisis de cobertura interior
- Criterios de decisión para refuerzo indoor
- Estimación de costos y plazos
- Comparativa de tecnologías

### Herramientas
- Python para cálculos RF
- Notebook Jupyter para presentación interactiva
- Matplotlib/Seaborn para visualización
- Pandas para análisis de datos
- Exportación a QGIS (opcional)

## 🔍 Fórmulas Clave

### Pérdida de Propagación (Friis)

$$L_{fs} (dB) = 20 \log_{10}(f [MHz]) + 20 \log_{10}(d [m]) + 32.45$$

### Nivel Recibido

$$P_{rx} (dBm) = P_{tx} + G_{tx} - L_{propagación} - L_{penetración}$$

### Margen de Cobertura

$$\text{Margen} = P_{rx} - P_{umbral}$$

(positivo = OK, negativo = falla)

## 📦 Dependencias

- **pandas** (análisis de datos)
- **numpy** (cálculos numéricos)
- **matplotlib** (gráficos)
- **seaborn** (estilos gráficos)
- **jupyter** (notebook interactivo)

## ✅ Entregables Esperados

Como resultado del ejercicio, el alumno genera:

1. **Tabla de pérdidas por tramo**
   - Propagación exterior, penetración interior, total
   - Por cada punto de medida

2. **Croquis del edificio con puntos**
   - Plano con ubicación de antena exterior
   - Marcado de 3 puntos de evaluación
   - Niveles de señal anotados

3. **Evaluación de cobertura**
   - Tabla comparativa servicios (voz, datos)
   - Gráficos de nivel recibido
   - Márgenes vs. umbrales

4. **Recomendación final**
   - ¿Cobertura macro suficiente?
   - Si no: ¿Qué solución (DAS/SC/repetidor)?
   - Presupuesto aproximado
   - Plazo de implementación

5. **Análisis de frecuencias alternativas** (extensión)
   - Tabla 700 vs 1800 vs 2600 MHz
   - Gráfico comparativo
   - Conclusión sobre mejor banda

## 🎯 Caso de Uso Realista

Este ejercicio simula situaciones reales como:

- Auditoría de cobertura en oficinas/hoteles
- Planeamiento de banda ancha rural
- Evaluación de necesidad de refuerzo indoor
- Justificación de inversión en DAS/small cells
- Optimización de recursos de red

## 🔗 Integración Posterior

El proyecto permite extensiones:

1. **Integración con QGIS** (ver QGIS_INTEGRACION.md)
2. **Análisis con Radio Mobile** (simulator profesional)
3. **Machine Learning** para predicción en otros puntos
4. **Análisis de interferencias** entre operadores
5. **Casos de estudio alternativos** (cambiar alturas, potencias, etc.)

## 📞 Reporte de Errores

Si encuentras problemas:

1. Verificar que las librerías están instaladas: `pip install -r requirements.txt`
2. Consultar docstrings del código: `python3 -c "from src import propagation; help(propagation.PropagationModel)"`
3. Revisar GUIA_ESTUDIANTE.md (sección "Solución de Problemas")
4. Ejecutar demo.py primero para validar instalación

## 📊 Estadísticas del Proyecto

- **Líneas de código:** ~1000 (sin documentación)
- **Celdas Notebook:** 13 (con markdown y código)
- **Módulos Python:** 3 (propagation, visualization, building_model)
- **Documentación:** 4 archivos .md (~200 KB)
- **Casos de uso practicados:** 5+

## 🎓 Nivel de Dificultad

- **Principiante:** Ejecutar notebook y interpretar resultados
- **Intermedio:** Modificar parámetros y analizar cambios
- **Avanzado:** Implementar nuevos modelos de propagación o integrar QGIS

## 📝 Licencia y Uso

**Uso Educativo:** Libre para aulas, trabajos prácticos y fines educativos

**Atribución:** Campus Indoor Coverage Lab, 2026

## 🚀 Conclusión

Este proyecto proporciona una herramienta educativa completa para que los alumnos de ingeniería de telecomunicaciones entiendan y practiquen el análisis de cobertura celular en espacios interiores, desde cálculos teóricos hasta recomendaciones prácticas de mejora.

---

**Versión:** 1.0  
**Creado:** 2026  
**Estado:** ✓ Funcional y Completado
