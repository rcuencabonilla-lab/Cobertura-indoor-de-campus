# Análisis de Cobertura Indoor en Campus

## Descripción

**Ejercicio interactivo de ingeniería de telecomunicaciones** para evaluar cobertura celular en un edificio multiplanta y proponer soluciones de mejora de cobertura indoor.

### Objetivo

Que los alumnos aprendan a:
- Calcular pérdidas de propagación en espacio libre
- Evaluar penetración de señal en elementos constructivos
- Determinar necesidad de refuerzo indoor (DAS, Small Cell, Repetidor)
- Comparar viabilidad según diferentes frecuencias (700 MHz - 2600 MHz)
- Generar presupuestos y recomendaciones técnicas

## Escenario

**Edificio modelo:** Campus Universitario Rectorado (4 plantas + semiótano)

**3 puntos de evaluación:**
1. **Entrada Principal** (planta baja) - Acceso desde exterior
2. **Aula Segunda Planta** - Zona interior profunda  
3. **Semiótano Técnico** - Zona subterránea

**Antena exterior:** Macro celda a 25 metros de altura, ~45m del edificio

## Estructura del Proyecto

```
Cobertura-indoor-de-campus/
├── README.md                          ← Este archivo
├── notebooks/
│   └── Ejercicio_Cobertura_Indoor.ipynb  ← NOTEBOOK PRINCIPAL (EJECUTAR)
├── src/
│   ├── __init__.py
│   ├── propagation.py                 ← Cálculos de propagación
│   └── visualization.py               ← Gráficos y visualizaciones
├── data/
│   └── building_model.py              ← Modelo del edificio y parámetros
└── docs/
    ├── GUIA_ESTUDIANTE.md             ← Guía paso a paso
    └── TECNICA.md                     ← Fundamentos teóricos
```

## Inicio Rápido

### Opción 1: VS Code (Recomendado)

```bash
# 1. Abrir el proyecto
cd /workspaces/Cobertura-indoor-de-campus

# 2. Abrir notebook en VS Code
code notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

Luego:
1. Abre la paleta de comandos (`Ctrl+Shift+P`)
2. Busca "Jupyter: Select Kernel" y elige Python 3.x
3. Presiona `Shift+Enter` en cada celda para ejecutarla

### Opción 2: Jupyter Lab

```bash
# En el contenedor
python3 -m pip install jupyter -q
python3 -m jupyter lab --allow-root --ip=0.0.0.0

# Abre navegador en: http://localhost:8888
# Navega a: notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

## Contenido del Notebook

El notebook ejecutable guía paso a paso:

| Sección | Descripción |
|---------|---|
| 1. Importaciones | NumPy, Pandas, Matplotlib, módulos propios |
| 2. Parámetros | Portadoras (700-2600 MHz), umbrales de servicio |
| 3. Propagación Exterior | Cálculo de pérdidas en espacio libre (Friis) |
| 4. Penetración Interior | Acumulación de pérdidas por elementos constructivos |
| 5. Evaluación Cobertura | Nivel recibido vs. umbrales en cada punto |
| 6. Visualización | Mapas del edificio y gráficos de nivel de señal |
| 7. Soluciones Mejora | Análisis de DAS, Small Cell, Repetidor |
| 8. Comparativa Frecuencias | Tabla y gráficos con 700-2600 MHz |
| 9. Conclusiones | Resumen ejecutivo y recomendaciones |

## Requisitos Técnicos

### Software Requerido
- Python 3.8+
- Jupyter Notebook o VS Code con extensión Jupyter
- Librerías: pandas, numpy, matplotlib, seaborn

### Instalación de Dependencias

```bash
# En el contenedor dev (generalmente ya instalado)
pip install pandas numpy matplotlib seaborn dataclasses -q

# Verificar importaciones
python3 -c "import pandas, numpy, matplotlib; print('✓ OK')"
```

## Documentación

### Para Estudiantes
Lee **[docs/GUIA_ESTUDIANTE.md](docs/GUIA_ESTUDIANTE.md)** para:
- Explicación paso a paso
- Tareas prácticas
- Preguntas de reflexión
- Cómo completar el informe

### Para Docentes
Consulta **[docs/TECNICA.md](docs/TECNICA.md)** para:
- Fundamentos teóricos completos
- Ecuaciones y derivaciones
- Criterios de decisión
- Extensiones avanzadas

## Parámetros Principales

| Parámetro | Valor | Notas |
|-----------|-------|-------|
| Frecuencia Principal | 1800 MHz (LTE) | Banda recomendada |
| Frecuencias Alternativas | 700, 800, 2100, 2600 MHz | Para comparativa |
| Potencia Transmisora | 43 dBm (20W) | Macro celda estándar |
| Ganancia Antena TX | 17 dBi | Panel típico |
| Altura Antena | 25 metros | Altura de mástil |
| Distancia al Edificio | ~45 metros | Fachada cercana |
| Umbral Voz | -100 dBm | 3GPP estándar |
| Umbral Datos | -95 dBm | Para servicios básicos |
| Pérdida Fachada | 15 dB | Hormigón 25cm |
| Pérdida Pared Interior | 4 dB | Ladrillo 12cm |
| Pérdida Forjado | 15 dB | Hormigón 25cm |

## Flujo de Trabajo Típico

```
1. PREPARAR
   ├─ Leer GUIA_ESTUDIANTE.md
   └─ Revisar conceptos en TECNICA.md

2. EJECUTAR NOTEBOOK
   ├─ Importar librerías (Celda 1-2)
   ├─ Definir parámetros (Celda 3-4)
   ├─ Cálculos propagación (Celda 5-8)
   ├─ Resultados cobertura (Celda 9-10)
   ├─ Visualizaciones (Celda 11-13)
   └─ Análisis soluciones (Celda 14-16)

3. ANALIZAR RESULTADOS
   ├─ Revisar tablas de pérdidas
   ├─ Interpretar gráficos
   └─ Evaluar margen de cobertura

4. ESCRIBIR INFORME
   ├─ Tabla de pérdidas (captura)
   ├─ Croquis con puntos (imagen)
   ├─ Recomendación: ¿Cobertura macro suficiente?
   └─ Si no: Proponer solución (DAS/SC/Repetidor)

5. EXTENSIÓN OPCIONAL
   ├─ Cambiar altura de antena
   ├─ Variar potencia
   ├─ Analizar interferencias
   └─ Investigar nuevas frecuencias
```

## Resultados Esperados

### Salida Típica

```
==== RESUMEN EJECUTIVO ====

FRECUENCIA PRINCIPAL: LTE 1800 MHz
POTENCIA: 43 dBm | ALTURA: 25m

COBERTURA:
1. Entrada Principal:        -35 dBm ✓ BUENA
2. Aula Segunda Planta:      -70 dBm ✓ BUENA  
3. Semiótano Técnico:        -50 dBm ✓ BUENA

DECISIÓN: Cobertura macro suficiente.
Sin necesidad de DAS/Small Cell/Repetidor.

NOTA: Monitorear margen en semiótano si 
      se requieren videollamadas.
```

## Extensiones Avanzadas

### 1. Casos de Estudio Alternativos
- Cambiar a **700 MHz** → Mejor penetración
- Cambiar a **2600 MHz** → Analizar trade-off con capacidad
- Duplicar altura antena → Mayor cobertura

### 2. análisis de Interferencias
- Estimar C/I entre edificios próximos
- Coordinar frecuencias
- Evaluar impacto en margen

### 3. Integración con QGIS
- Exportar coordenadas de puntos
- Superponer ortofoto del campus
- Generar mapas de cobertura predicha

### 4. Modelos Avanzados
- Incorporar ray-tracing (WinProp simulator)
- Análisis de fading (Rayleigh/Rician)
- Predicción con machine learning

## Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'src'"

**Solución:** Ejecuta desde carpeta raíz y verifica que `sys.path` incluya el proyecto:

```python
import sys
sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')
```

### Error: "No plot display"

**Solución:** En Jupyter, añade al inicio:

```python
%matplotlib notebook
# o
%matplotlib inline
```

### Los gráficos son muy pequeños

**Solución:** Aumenta tamaño de figura en celda:

```python
import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (16, 10)
```

## Características Principales del Código

### Módulo `src/propagation.py`

**Clases:**
- `Frequency`: Define portadora (f, BW, potencia, tecnología)
- `PropagationModel`: Cálculo Friis y Okumura-Hata
- `ServiceThreshold`: Umbrales por tecnología
- `IndoorMeasurementPoint`: Punto de medida con ubicación y pérdidas

**Métodos clave:**
```python
PropagationModel.free_space_loss(frequency, distance_m)
PropagationModel.add_penetration_losses(outdoor_signal, losses_dict)
ServiceThreshold.check_service(signal_dbm, service, technology)
```

### Módulo `src/visualization.py`

**Clases:**
- `BuildingVisualization`: Gráficos de plano y señal
- `ReportGenerator`: Tablas y reportes

**Métodos clave:**
```python
BuildingVisualization.plot_building_layout(building_data, points, tx_pos)
BuildingVisualization.plot_signal_levels(measurements, services)
ReportGenerator.create_loss_table(measurement_points)
```

### Módulo `data/building_model.py`

Exporta:
- `BUILDING_MODEL`: Geometría y materiales
- `MEASUREMENT_POINTS`: 3 puntos de prueba
- `FREQUENCIES`: Portadoras a estudiar
- `SERVICE_REQUIREMENTS`: Umbrales
- `COVERAGE_SOLUTIONS`: Opciones de mejora

## Casos de Uso Reales

Este ejercicio simula:

1. **Audit de cobertura interior en oficina/hotel**
   - Determinar si se necesita refuerzo
   - Comparar costo DAS vs Small Cells

2. **Planeamiento de banda ancha rural**
   - Evaluar si antena exterior alcanza edificios
   - Identificar zonas de sombra

3. **Optimización de micro redes (SON)**
   - Comparar estrategias de frecuencia
   - Justificar inversión en mejoras

## Créditos y Referencias

- **Inspiración:** Problemas prácticos de ingeniería RF
- **Fundamentos:** 3GPP, ITU-R, libros de propagación
- **Librerías:** NumPy, Pandas, Matplotlib, Seaborn

## Licencia

Material educativo. Libre para uso en aulas y trabajos prácticos.

## Contacto

Para dudas sobre el ejercicio, consulta:
1. `docs/GUIA_ESTUDIANTE.md` (conceptos)
2. `docs/TECNICA.md` (fundamentos)
3. Docstrings en `src/` (código)

---

**Versión:** 1.0  
**Última actualización:** 2026  
**Autor:** Campus Indoor Coverage Lab  
**Alcance:** Educativo - Ingeniería de Telecomunicaciones