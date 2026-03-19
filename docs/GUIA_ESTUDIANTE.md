# Guía de Ejercicio: Análisis de Cobertura Indoor en Campus

## Descripción General

Este ejercicio práctico simula el análisis de cobertura celular en un edificio real de varias plantas. Los alumnos aprenderán a:

- Calcular pérdidas de propagación en espacio libre
- Evaluar penetración de señal a través de elementos constructivos
- Determinar si se necesita refuerzo indoor (DAS, Small Cell, Repetidor)
- Comparar viabilidad según diferentes frecuencias

## Escenario

**Edificio modelo:** Rectorado del Campus - 4 plantas + semiótano técnico

**Puntos de evaluación:**
1. **Entrada Principal** (Planta baja) - Acceso desde exterior
2. **Aula de Segunda Planta** - Zona interior, múltiples forjados
3. **Semiótano Técnico** - Zona subterránea

**Parámetros de antena exterior:**
- Altura: 25 metros (macro celda)
- Potencia: 43 dBm (20W)
- Ganancia: 17 dBi
- Distancia edificio: ~45 metros

## Conceptos Teóricos

### 1. Pérdida de Propagación (Espacio Libre)

Fórmula de Friis:
```
L_fs = 20·log₁₀(f) + 20·log₁₀(d) + 20·log₁₀(4π/c)
```

Donde:
- f = Frecuencia en MHz
- d = Distancia en metros
- c = Velocidad luz (3×10⁸ m/s)

**Ejemplo LTE 1800 MHz a 70 metros:**
- L = 20·log₁₀(1800) + 20·log₁₀(70) + 20·log₁₀(4π/3e8)
- L ≈ 65.1 + 36.9 - 21.98 = 80 dB

### 2. Pérdidas de Penetración Interior

Se acumulan según el trayecto del rayo:

| Elemento | Pérdida Típica |
|----------|---|
| Fachada (hormigón 25cm) | 12-18 dB |
| Pared interior (ladrillo) | 3-5 dB |
| Forjado (hormigón 25cm) | 12-18 dB |

**Entrada:** 15 dB (1 fachada)
**Aula 2ª:** 49 dB (1 fachada + 1 pared + 2 forjados)
**Semiótano:** 34 dB (1 fachada + 1 pared + 1 forjado)

### 3. Nivel Recibido

```
P_rx = P_tx + G_tx - L_propagación - L_penetración
```

Ejemplo Entrada:
```
P_rx = 43 + 17 - 80 - 15 = -35 dBm ✓ EXCELENTE
```

### 4. Umbrales de Servicio

| Servicio | Umbral (dBm) |
|----------|---|
| Voz/SMS | -100 |
| Datos básicos | -95 |
| Videoconferencia | -85 |
| Descarga rápida | -75 |

## Tareas del Alumno

### Tarea 1: Verificar Cálculos

Ejecuta las celdas del notebook en orden y verifica:

1. ¿Qué frecuencia tiene mejor penetración en interior?
2. ¿Cuál es el punto más crítico (menos cobertura)?
3. ¿En cuántos puntos falta cobertura para voz?

**Respuesta esperada:**
- 700 MHz penetra mejor (menos pérdida)
- Semiótano es más crítico
- Normalmente 0-1 puntos sin cobertura completa

### Tarea 2: Proponer Solución

Si algún punto no alcanza umbral de voz (-100 dBm):

1. Calcula ganancia faltante: `G_req = -100 - P_rx_actual`
2. Propone tecnología:
   - G_req < 10 dB → Repetidor
   - 10-15 dB → Small Cell
   - > 15 dB → DAS

**Ejemplo:** Si P_rx = -110 dBm en semiótano
- G_req = 10 dB
- Solución: Repetidor Interior (10-15 dB)
- Costo aprox: 3k-8k€

### Tarea 3: Análisis Comparativo

Ejecuta la sección de comparativa de frecuencias y completa tabla:

| Punto | 700 MHz | 1800 MHz | 2600 MHz | ¿Frecuencia óptima? |
|-------|---------|----------|----------|---|
| Entrada | ? | ? | ? | |
| Aula 2ª | ? | ? | ? | |
| Semiótano | ? | ? | ? | |

**Pauta:** A menor frecuencia, mejor penetración interior

## Procedimiento Práctico

### Paso 1: Preparar Ambiente

```bash
cd /workspaces/Cobertura-indoor-de-campus
python3 -m jupyter notebook notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

### Paso 2: Ejecutar de Izquierda a Derecha

Presiona `Shift+Enter` en cada celda, descendiendo con orden.

**Celdas críticas:**
- Celda 2: Importaciones
- Celda 4: Parámetros portadora
- Celda 8: Cálculo propagación
- Celda 10: Evaluación cobertura
- Celda 15: Comparativa frecuencias

### Paso 3: Interpretar Resultados

Revisa tablas y gráficos:
- ✓ Verde = Cobertura OK
- ⚠ Naranja = Marginal
- ✗ Rojo = Falla

### Paso 4: Completar Informe

Usa el resumen ejecutivo para redactar conclusiones

## Preguntas de Reflexión

1. **¿Por qué el semiótano tiene peor cobertura?**
   - Está enterrado → señal atraviesa forjados
   - Apantallamiento de estructuras de hormigón

2. **¿Qué pasaría si la antena estuviera a 50m de altura?**
   - Menos pérdida de propagación
   - Mejor cobertura en altura (aulas superiores)

3. **¿Es viable usar solo cobertura macro?**
   - Depende del margen calculado
   - Necesidad de refuerzo si margen < 5 dB en servicios críticos

4. **¿A qué frecuencia cambiarías si necesitas más capacidad?**
   - 2600 MHz tiene ancho de banda mayor pero penetra peor
   - Solución: Combinar 1800 MHz (cobertura) + 2600 MHz (capacidad en entrada)

## Entregables

1. **Tabla de Pérdidas**
   - Captura de salida anterior a gráficos

2. **Croquis con Puntos de Medida**
   - Imagen generada por matplotlib

3. **Recomendación Final** (1 página)
   - Cobertura macro ¿suficiente?
   - Necesidad de DAS/Small Cell/Repetidor
   - Presupuesto y plazo

4. **Apéndice: Comparativa de Frecuencias**
   - Tabla de niveles por banda
   - Gráfico comparativo

## Extensión Opcional

**Análisis de Interferencias:**

Si dos edificios próximos tienen antenas en misma banda:
- Estima distancia entre antenas
- Calcula C/I (Carrier/Interference ratio) requerido
- ¿Cómo coordinar frecuencias?

**Mejora de Propagación:**

- Cambia altura de antena a 30m → ¿Mejora?
- Cambia potencia a 50 dBm → ¿Cuántos dB adicionales?

## Referencias Teóricas

### Modelos de Propagación

1. **Espacio Libre (Friis)**
   - Aplicable: > 100m, line-of-sight
   - Fórmula: L = 20·log₁₀(f·d) + 20·log₁₀(4π/c)

2. **Okumura-Hata** (150-1500 MHz, 1-20 km)
   - Incluye factores urbanos
   - Más preciso que Friis

3. **2-Ray Ground** (multipath)
   - Cuando hay reflexión significativa

### Estándares

- **3GPP:** Define umbrales de servicio
- **ITU-R P.526:** Propagación en edificios
- **GSMA IR.34:** Requisitos de cobertura

## Herramientas Adicionales

- **QGIS:** Mapear puntos y antenas
- **Radio Mobile:** Simulación completa de cobertura
- **Python + Cartopy:** Mapas con cobertura predicha

## Contacto y Dudas

Revisa docstrings en módulos:
```python
from src.propagation import PropagationModel
help(PropagationModel.free_space_loss)
```

---

**Edición:** 2026
**Versión:** 1.0
**Autor:** Campus Indoor Coverage Lab
