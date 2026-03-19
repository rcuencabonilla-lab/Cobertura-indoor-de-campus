# Integración con QGIS - Guía de Uso

## Descripción

Este documento explica cómo exportar los datos del análisis de cobertura indoor a QGIS para visualización espacial.

## Pasos de Configuración

### 1. Exportar Datos a CSV

Ejecuta desde Python:

```python
import sys
sys.path.insert(0, '/workspaces/Cobertura-indoor-de-campus')

from data.building_model import get_measurement_points
import pandas as pd

# Cargar puntos
points = get_measurement_points()

# Crear DataFrame
data = {
    'Punto': [p['name'] for p in points],
    'Ubicación': [p['location'] for p in points],
    'Lat': [p['x_m'] for p in points],  # Usar como coordenada Y
    'Lon': [p['y_m'] for p in points],  # Usar como coordenada X
    'Altura': [p['z_m'] for p in points],
    'Fachada_dB': [p['penetration_losses'].get('facade', 0) for p in points],
    'Pared_dB': [p['penetration_losses'].get('wall', 0) for p in points],
    'Forjado_dB': [p['penetration_losses'].get('floor', 0) for p in points]
}

df = pd.DataFrame(data)
df.to_csv('puntos_medida.csv', index=False)
print("Exportado: puntos_medida.csv")
```

### 2. Importar en QGIS

1. Abre QGIS
2. Menú: `Layer → Add Layer → Add Delimited Text Layer`
3. Selecciona `puntos_medida.csv`
4. Configurar:
   - X field: `Lon`
   - Y field: `Lat`
   - CRS: EPSG:4326 (WGS84)
5. Hacer clic en "Add"

### 3. Visualizar Puntos

- Los puntos aparecerán en el mapa
- Puedes ajustar estilos (colores, símbolos) en `Layer Properties → Symbology`
- Añadir etiquetas: `Layer → Labeling`

## Generación de Mapas de Calor

### Opción 1: Usando Plugin QGIS

1. Instalar plugin "Heatmap"
2. Menú: `Raster → Heatmap → Heatmap`
3. Configurar weights del nivel de señal recibido

### Opción 2: Usando Python + Folium

```python
import folium
from folium.plugins import HeatMap

# Datos de cobertura
points_coverage = [
    {'lat': 20, 'lon': 25, 'signal': -85.7, 'name': 'Entrada'},
    {'lat': 50, 'lon': 35, 'signal': -94.6, 'name': 'Aula 2ª'},
    {'lat': 20, 'lon': 10, 'signal': -105.4, 'name': 'Semiótano'}
]

# Crear mapa
m = folium.Map(
    location=[30, 20],
    zoom_start=17,
    tiles='OpenStreetMap'
)

# Añadir puntos
for point in points_coverage:
    color = 'green' if point['signal'] > -100 else 'red'
    folium.CircleMarker(
        location=[point['lat'], point['lon']],
        radius=10,
        popup=f"{point['name']}: {point['signal']:.1f} dBm",
        color=color
    ).add_to(m)

m.save('cobertura_mapa.html')
```

## Exportar Edificio a SHP (Shapefile)

```python
import geopandas as gpd
from shapely.geometry import box, LineString

# Crear polígono del edificio
building = get_building()
perimeter = building['building']['perimeter']

# Caja del edificio
building_box = box(
    perimeter['x'], 
    perimeter['y'],
    perimeter['x'] + perimeter['width'],
    perimeter['y'] + perimeter['height']
)

# Crear GeoDataFrame
gdf = gpd.GeoDataFrame(
    {'name': ['Building'], 'type': ['rectangular']},
    geometry=[building_box],
    crs='EPSG:4326'
)

# Guardar como shapefile
gdf.to_file('edificio.shp')

# También exportar puntos
points_gdf = gpd.GeoDataFrame(
    {'name': [p['name'] for p in points]},
    geometry=[Point(p['x_m'], p['y_m']) for p in points],
    crs='EPSG:4326'
)
points_gdf.to_file('puntos_medida.shp')
```

## Creación de Mapas de Cobertura Predicha

### Software recomendado (open source)

1. **Radio Mobile** (Windows/Linux con Wine)
   - Simulator profesional
   - Soporta múltiples tipos de terreno
   - Export de imágenes PNG

2. **QGIS + Radio Tools** (si disponible)
   - Plugin para cálculos de radiación
   - Integración con datos raster

3. **Python Basemap/Cartopy**
   ```python
   import matplotlib.pyplot as plt
   import numpy as np
   
   # Grid de puntos
   x = np.linspace(0, 40, 50)
   y = np.linspace(0, 60, 50)
   X, Y = np.meshgrid(x, y)
   
   # Calcular cobertura predicha en cada punto
   Z = np.zeros_like(X)
   for i, xi in enumerate(x):
       for j, yj in enumerate(y):
           # Calcular nivel en (xi, yj)
           distance = np.sqrt((xi + 15)**2 + (yj + 10)**2)
           loss = PropagationModel.free_space_loss(freq, distance)
           Z[j, i] = EIRP - loss - 15  # Pérdida típica
   
   # Graficar
   plt.contourf(X, Y, Z, levels=15, cmap='RdYlGn')
   plt.colorbar(label='Nivel de Señal (dBm)')
   plt.title('Mapa de Cobertura Predicha - LTE 1800 MHz')
   plt.show()
   ```

## Datos TIF para Ortofoto

Si disponible ortofoto del campus:

```python
import rasterio
from rasterio.plot import show

# Cargar ortofoto
with rasterio.open('campus_ortofoto.tif') as src:
    plt.imshow(src.read([1,2,3]).transpose((1,2,0)))
    
# Superponer puntos
plt.scatter(puntos_x, puntos_y, c=cobertura_color)
plt.show()
```

## Integración con PostGIS

Si tienes instalado PostGIS + PostgreSQL:

```sql
CREATE TABLE edificio_puntos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100),
    ubicacion VARCHAR(200),
    geom GEOMETRY(POINT, 4326),
    nivel_signal FLOAT,
    margen_db FLOAT
);

INSERT INTO edificio_puntos (nombre, ubicacion, geom, nivel_signal, margen_db)
VALUES 
    ('Entrada', 'Planta baja', ST_Point(25, 20), -85.7, 14.3),
    ('Aula 2ª', 'Segunda planta', ST_Point(35, 50), -94.6, 5.4),
    ('Semiótano', 'Nivel -1', ST_Point(10, 20), -105.4, -5.4);

SELECT nombre, nivel_signal, ST_AsText(geom) FROM edificio_puntos;
```

## Checklist de Integración

- [ ] Exportar CSV de puntos
- [ ] Importar en QGIS
- [ ] Verificar CRS (EPSG:4326)
- [ ] Añadir capas de referencia (ortofoto si disponible)
- [ ] Aplicar simbología según nivel de señal
- [ ] Etiquetizar puntos
- [ ] Generar mapa de cobertura predicha
- [ ] Exportar PDF del mapa (File → Export)

## Referencias

- **QGIS Manual:** https://docs.qgis.org/
- **PostGIS Documentation:** https://postgis.net/documentation/
- **Folium Examples:** https://python-visualization.github.io/folium/

---

**Nota:** Para casos simples, la exportación CSV + QGIS es suficiente. Para análisis avanzados de cobertura predicha, considerar Radio Mobile o simuladores especializados.
