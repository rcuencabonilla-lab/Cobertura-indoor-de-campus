# INICIO RÁPIDO - Ejercicio de Cobertura Indoor

## ⚡ En 5 Minutos

### 1️⃣ Instalar Dependencias

```bash
cd /workspaces/Cobertura-indoor-de-campus
pip install -q -r requirements.txt
```

### 2️⃣ Ejecutar Demostración

```bash
python3 demo.py
```

**Resultado esperado:**
```
✓ Entrada Principal          -85.7 dBm (Margen: 14.3 dB)
✓ Aula Segunda Planta        -94.6 dBm (Margen: 5.4 dB)
✗ Semiótano Técnico         -105.4 dBm (Margen: -5.4 dB)

CONCLUSIÓN: Refuerzo necesario en semiótano
```

### 3️⃣ Abrir Notebook Completo

**En VS Code:**
```bash
code notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

Luego presiona `Shift+Enter` en cada celda.

**En Jupyter:**
```bash
jupyter lab --allow-root
# Abre http://localhost:8888
# Navega a: notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

---

## 📂 Estructura de Archivos

```
.
├── README.md                              ← Descripción general
├── PROYECTO_RESUMEN.md                    ← Este proyecto en detalle
├── requirements.txt                       ← Dependencias (pip)
│
├── demo.py                                ← Script rápido (sin Jupyter)
├── ejemplos_avanzados.py                  ← Casos de uso avanzados
│
├── notebooks/
│   └── Ejercicio_Cobertura_Indoor.ipynb   ⭐ NOTEBOOK PRINCIPAL
│
├── src/                                   ← Módulos reutilizables
│   ├── propagation.py                     # Cálculos RF
│   └── visualization.py                   # Gráficos
│
├── data/
│   └── building_model.py                  # Modelo del edificio
│
└── docs/
    ├── GUIA_ESTUDIANTE.md                 # Paso a paso
    ├── TECNICA.md                         # Fundamentos teoría
    ├── QGIS_INTEGRACION.md                # Exportar a QGIS
    └── INICIO_RAPIDO.md                   ← Este archivo
```

---

## 🎯 Principales Casos de Uso

### Caso 1: Solo Ver Resultados (5 minutos)

```bash
python3 demo.py
```

✓ Cálculos inmediatos  
✓ Sin instalación de Jupyter  
✓ Salida textual clara

### Caso 2: Análisis Interactivo (30 minutos)

```bash
jupyter lab --allow-root
# Abrir notebook y ejecutar celdas interactivamente
```

✓ Visualizaciones gráficas  
✓ Tablas formateadas  
✓ Modificar parámetros sobre la marcha

### Caso 3: Análisis Avanzado (Personalizado)

```bash
python3 ejemplos_avanzados.py 3  # Calcular ganancia requerida
python3 ejemplos_avanzados.py 4  # Superficie 3D
python3 ejemplos_avanzados.py 6  # Exportar reportes
```

✓ Análisis paramétricos  
✓ Optimización  
✓ Exportación a múltiples formatos

---

## 📊 Lo Que Aprenderás

| Tema | Actividad | Tiempo |
|------|-----------|--------|
| Propagación RF | Calcular pérdidas Friis | 5 min |
| Penetración Interior | Modelar obstáculos | 5 min |
| Evaluación Cobertura | Comparar con umbrales | 5 min |
| Mejora de Cobertura | DAS vs Small Cell vs Repetidor | 10 min |
| Comparativa Frecuencias | Analizar 700-2600 MHz | 10 min |
| **TOTAL** | | **35 min** |

---

## 🔧 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'pandas'"

**Solución:**
```bash
pip install -r requirements.txt
```

### Error: "The notebook is not signed"

(Solo en Jupyter, si ves alerta de seguridad)

**Solución:** Hacer clic en "Trust Notebook" o ejecutar:
```bash
jupyter trust notebooks/Ejercicio_Cobertura_Indoor.ipynb
```

### Los gráficos no aparecen en Jupyter

**Solución:** Añadir al inicio del notebook:
```python
%matplotlib inline
# o
%matplotlib notebook
```

### El script demo.py se ejecuta pero no muestra nada

**Solución:** Verificar que estás en la carpeta correcta:
```bash
cd /workspaces/Cobertura-indoor-de-campus
python3 demo.py
```

---

## 📚 Documentación Recomendada

| Tipo de Usuario | Leer | Tiempo |
|---|---|---|
| **Estudiante principiante** | `docs/GUIA_ESTUDIANTE.md` | 20 min |
| **Estudiante intermedio** | `docs/TECNICA.md` | 30 min |
| **Profesor/Investigador** | `docs/QGIS_INTEGRACION.md` | 15 min |
| **Desarrollador** | Docstrings en `src/*.py` | 10 min |

---

## 🚀 Próximos Pasos

### Nivel 1: Entender Conceptos
1. Correr `python3 demo.py`
2. Leer `docs/GUIA_ESTUDIANTE.md`
3. Ejecutar cada celda del notebook

### Nivel 2: Experimentar
1. Modificar parámetros en notebook
2. ¿Qué pasa si cambias frecuencia a 700 MHz?
3. ¿Qué pasaría si la antena estuviera a 40 metros?

### Nivel 3: Profundizar
1. Ejecutar `python3 ejemplos_avanzados.py 2` (optimizar altura)
2. Generar reportes: `python3 ejemplos_avanzados.py 6`
3. Integrar con QGIS (ver `docs/QGIS_INTEGRACION.md`)

### Nivel 4: Extender
1. Implementar nuevo modelo de propagación
2. Añadir desvanecimiento (fading)
3. Modelar interferencia multiusuario

---

## 💡 Preguntas Tipo Examen

Después de usar este proyecto, deberías poder responder:

1. **¿Cuál es la pérdida de propagación a 1800 MHz a 100 metros?**
   - Resp: ~120 dB (usando Friis)

2. **¿Qué elemento constructivo causa más pérdida?**
   - Resp: Forjados y fachada (~15 dB cada uno)

3. **¿Qué frecuencia penetra mejor en interiores?**
   - Resp: 700 MHz (~8 dB mejor que 1800 MHz)

4. **¿Cuándo se necesita DAS en lugar de Small Cell?**
   - Resp: Cuando margen < -10 dB o necesitas uniformidad en múltiples plantas

5. **¿Qué es el margen de cobertura?**
   - Resp: P_rx - P_umbral (debe ser > 5 dB típicamente)

---

## 📞 Contacto y Dudas

**Para dudas sobre conceptos:**
- Lee `docs/TECNICA.md` (fundamentos)

**Para dudas sobre tareas:**
- Consulta `docs/GUIA_ESTUDIANTE.md` (paso a paso)

**Para dudas sobre código:**
```python
from src.propagation import PropagationModel
help(PropagationModel.free_space_loss)  # Ver documentación
```

---

## ✅ Checklist de Finalización

- [ ] Ejecuté `python3 demo.py` exitosamente
- [ ] Instalé dependencias: `pip install -r requirements.txt`
- [ ] Abrí notebook en Jupyter/VS Code
- [ ] Ejecuté al menos 5 celdas del notebook
- [ ] Entendí cómo se calcula la cobertura
- [ ] Interpreté los gráficos de resultado
- [ ] Completé el análisis de los 3 puntos
- [ ] Propuse una solución de mejora (DAS/SC/Repetidor)
- [ ] Comparé al menos 2 frecuencias diferentes
- [ ] Redacté mi conclusión

**Si marcaste todo:** ¡FELICIDADES! Has completado el ejercicio 🎓

---

## 📈 Próximas Extensiones

- [ ] Exportar a QGIS y generar mapas
- [ ] Implementar desvanecimiento log-normal
- [ ] Raytacing simulado con multipath
- [ ] Análisis de interferencia entre operadores
- [ ] Optimización de ubicación de Small Cells con algoritmos genéticos
- [ ] Integración con bases de datos geoespaciales

---

## 📝 Control de Versiones

- **v1.0** (2026-03): Versión inicial completa
  - ✓ Notebook funcional
  - ✓ 3 puntos de evaluación
  - ✓ Comparativa de frecuencias
  - ✓ Documentación completa

---

**¡Que comience el análisis! 🚀**

Para empezar:
```bash
cd /workspaces/Cobertura-indoor-de-campus
python3 demo.py
```

O si prefieres Jupyter:
```bash
jupyter lab --allow-root
```

---

*Última actualización: 2026*  
*Campus Indoor Coverage Lab*
