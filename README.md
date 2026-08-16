# Industrial Vision Lab

Sistema educativo de **visión artificial industrial** que simula una celda de inspección automatizada en planta. No es un tutorial más de programación: es un **curso práctico de ingeniería de software** construido con el método "aprender construyendo", en el que cada línea de código responde a un problema real de automatización industrial.

---

## 🎯 ¿Qué es este proyecto?

El objetivo no es escribir scripts aislados, sino diseñar un **sistema de software estructurado, desacoplado y mantenible** capaz de:

- Capturar vídeo en tiempo real desde una cámara web (con reconexión automática ante fallos de puerto).
- Aplicar un pipeline clásico de **Procesamiento Digital de Imágenes (PDI)**: ROI, escala de grises, filtro de mediana, umbralización fija y adaptativa, morfología matemática, detección de bordes Canny y análisis de contornos.
- Inspeccionar piezas por **relación de aspecto** (tolerancia industrial 0.8–1.2): fuera de rango, NOK.
- Seguir centroides de piezas y **contarlas de forma única** al cruzar una línea virtual de activación.
- Persistir métricas de producción de forma síncrona y estructurada en CSV y log, **únicamente cada 30 frames** para no saturar I/O.

El resultado es la base técnica para el roadmap completo de formación: desde visión clásica hasta Edge AI, comunicaciones industriales (MQTT, OPC-UA, Modbus) y despliegue en NVIDIA Jetson.

---

## 🧠 Filosofía de aprendizaje: el LLM como profesor, no como fábrica de código

Este repositorio existe gracias a un asistente de código (LLM) que actúa como **`teacher`**: un agente que guía con método socrático, plantea preguntas, señala errores y exige razonar antes de escribir.

La regla clave del curso es explícita:

> **No se escribe código del alumno** salvo petición explícita. El LLM no genera la solución: [la acompaña](opencode.json).

Esto marca la diferencia entre dos usos radicalmente distintos de la inteligencia artificial:

| | **IA generativa / "vibe coding"** | **LLM como aprendizaje guiado** |
|---|---|---|
| Quién escribe el código | El modelo, automáticamente | El alumno, razonando |
| Rol del LLM | Sustituto del programador | Profesor, orientador y revisor |
| Resultado | Código que se *"parece que funciona"* | Conocimiento que se consolida |
| Riesgo | Dependencia, huecos conceptuales | Ninguno mientras se mantenga la disciplina |
| Métrica de éxito | La app "compila" | Entender *por qué* y *cómo* funciona |

**Por qué importa en un entorno industrial:** en planta no existe un LLM que corrija un fallo de producción a medianoche. El ingeniero debe entender cada decisión arquitectónica —por qué la binarización vive en el servicio y no en el HMI, por qué la persistencia recibe solo tipos primitivos, por qué el `__init__` de una clase no abre ventanas ni bucles. El LLM, bien usado, acelera ese entendimiento; mal usado, lo anula.

> "El LLM no debe ser la respuesta automática al problema, sino la guía que enseña a encontrar la respuesta uno mismo."

---

## 🏗️ Arquitectura

Separación estricta de responsabilidades en capas de servicios independientes:

```
industrial-vision-lab/
├── apps/
│   ├── camera_info.py      # Orquestador: bucle principal, UI del operador, coordinación
│   └── test_camera.py      # Verificación rápida de la cámara
├── services/
│   ├── camera_service.py   # Ciclo de vida de la cámara + pipeline de PDI
│   ├── storage_service.py  # Única capa que toca disco (CSV, log, frames)
│   ├── inspection.py       # Reglas de calidad (aspect ratio)
│   ├── tracking.py         # Seguimiento de centroides y conteo único
│   └── __init__.py         # Re-exporta todos los servicios
├── datasets/               # Salidas en runtime: reporte_produccion.csv, app_vision.log
├── indice.md               # Roadmap completo del curso
├── general_context.md      # Contexto, pila tecnológica y arquitectura detallada
└── avance.md               # Estado del alumno e informe de progreso
```

**Servicios principales:**

- **`CameraService`** — Encapsula `cv2.VideoCapture`: escanea índices 0–4 si falla el puerto principal y lanza la excepción pública `CameraConectionError` (typo histórico intencional) ante pérdida total. Expone el pipeline completo: `roi_matrix`, `roi_to_gray`, `noise_filter`, `threshold_roi`, `adaptive_threshold_roi`, `morph_clean`, `detect_edges`, `find_and_filter_contours`.
- **`StorageService`** — Toda la persistencia pasa por aquí: frames JPG, `registrar_metricas` (autogenera cabeceras CSV) y `save_log`. Recibe solo tipos primitivos, nunca matrices ni texto formateado para la HMI.
- **`InspectionService`** — `calculate_aspect_ratio` e `is_valid_shape` con tolerancia 0.8–1.2.
- **`TrackingService`** — Máquina de estados sobre centroides para contar cada pieza **una sola vez** al cruzar la línea virtual.

**Reglas de diseño del curso:**

- **Regla de oro de renderizado:** toda la lógica se aplica sobre matrices en memoria; un único `cv2.imshow` al final del ciclo de frame (sin parpadeos ni latencia).
- **Constructores limpios:** `__init__` solo inicializa atributos; nada de I/O, ventanas ni bucles.
- **Persistencia cada 30 frames**, no en cada frame.
- **Pureza de datos:** la capa de persistencia recibe solo `int`/`float`/`str`.

---

## 🛠️ Stack tecnológico

Python 3.14 · OpenCV (`cv2`) · NumPy · Git/GitHub · Linux (CachyOS/Arch)

Roadmap previsto: PyTorch/YOLO → FastAPI/PostgreSQL/Redis → ONNX/TensorRT/Jetson → Docker → MQTT/OPC-UA/Modbus → Ollama/RAG → arquitectura distribuida.

---

## 🚀 Ejecución

Requiere una **webcam**. Ejecutar siempre **desde la raíz del repositorio**:

```bash
.venv/bin/python -m apps.camera_info
```

> ⚠️ No ejecutar `python apps/camera_info.py` directamente: rompe con `ModuleNotFoundError: No module named 'services'`. La app debe lanzarse como módulo para que `services/` quede en el `sys.path`.

Prueba rápida de cámara: `.venv/bin/python -m apps.test_camera` (salir con `q`).

Los datos de producción se generan en `datasets/`: `reporte_produccion.csv` y `app_vision.log`.

---

## 📚 Documentación del curso

| Documento | Contenido |
|---|---|
| [`indice.md`](indice.md) | Roadmap de formación: 10 fases, de fundamentos a producto real |
| [`general_context.md`](general_context.md) | Contexto, objetivos, arquitectura detallada y problemas resueltos |
| [`avance.md`](avance.md) | Estado del alumno, conocimientos adquiridos y puntos de fricción |

---

## 🧑‍🏫 Para quien quiera aprender igual

Si este enfoque te llama la atención:

1. **Escribe tú el código.** Copiar y pegar lo que otro genera no deja aprendizaje.
2. **Usa el LLM como sparring:** que te haga preguntas, no que te dé respuestas.
3. **Razona en voz alta** tus decisiones de arquitectura antes de implementar.
4. **Acepta el error** como material de estudio: cada bug del proyecto está documentado como hito de aprendizaje.

La industria no paga por el que genera más código con IA: paga por el que entiende por qué un sistema crítico no puede fallar.