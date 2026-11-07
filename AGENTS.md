# AGENTS.md — industrial-vision-lab

## Qué es este repo

Proyecto de **curso guiado** de visión artificial industrial (simula una celda de inspección en planta). No es desarrollo convencional: existe un agente profesor (`teacher`, ver `opencode.json`) que guía con método socrático.

- **Leer antes de actuar**: `indice.md` (roadmap), `general_context.md` (contexto y reglas del curso), `avance.md` (estado del alumno). El idioma de trabajo es **español**.
- Regla clave del curso: **no escribir código del alumno** salvo petición explícita (permisos de `opencode.json`: edit = ask).

## Entorno y ejecución

- Python **3.14** en `.venv/` (intérprete: `.venv/bin/python`). Solo hay instalados `numpy` y `opencv-python`; **no existe `requirements.txt`** ni pip dentro del venv.
- App principal (desde la raíz del repo, obligatoriamente):

  ```bash
  .venv/bin/python -m apps.camera_info
  ```

  Ejecutar `python apps/camera_info.py` directamente rompe con `ModuleNotFoundError: No module named 'services'` (la carpeta `apps/` pasa a ser la raíz de `sys.path`).
- Test rápido de cámara: `python apps/test_camera.py` (sale con 'q').
- **Se necesita webcam**. `CameraService` prueba el índice 0 y rescanea 0–4 si falla.
- Ejecutar siempre desde la raíz: las rutas `datasets/` (CSV, log) son relativas y el `FileHandler` escribe en `datasets/app_vision.log`.

## Arquitectura

- `apps/` = scripts ejecutables. `camera_info.py` es el orquestador: bucle `while True`, UI del operador, coordina los servicios.
- `services/` = paquete importable. `__init__.py` re-exporta todo: `CameraService`, `StorageService`, `InspectionService`, `TrackingService`, `TrackedObject`.
  - `CameraService`: ciclo de vida de `cv2.VideoCapture` + pipeline PDI (ROI, gris, mediana, umbral fijo/adaptativo, morfología, Canny, contornos, bounding boxes).
  - `StorageService`: única capa que toca disco (`datasets/reporte_produccion.csv`, autogenera cabeceras).
  - `InspectionService`: reglas de calidad (aspect ratio).
  - `TrackingService`: tracking de centroides y conteo único al cruzar una línea virtual.

## Gotchas

- La excepción pública se llama **`CameraConectionError`** (con una sola "n"; typo histórico ya exportado en `services/__init__.py`). Usar ese nombre exacto al importarla.
- Sin tests, lint ni CI. Verificación = ejecutar la app y comprobar CSV/log/HMI.
- `datasets/` contiene salidas en runtime: el CSV y el log sí se versionan; `.jpg`/`.png` están en `.gitignore`.

## Reglas de diseño del curso (validar en revisión de código)

- **Regla de oro de renderizado**: toda la lógica sobre matrices primero; un único `cv2.imshow` al final del ciclo de frame.
- **Constructores limpios**: `__init__` solo inicializa atributos; nada de I/O, ventanas ni bucles.
- **Persistencia cada 30 frames** al CSV (no en cada frame).
- **Tolerancia de aspect ratio 0.8–1.2**: fuera de rango la pieza es NOK.
- La capa de persistencia recibe solo tipos primitivos (int/float/str), nunca matrices ni texto formateado para UI.

## Git

- Rama `main` (push a `origin/main`). Mensajes cortos en inglés, p. ej. "CSV REPORT", "Centroids tracking service has been implemented".

## graphify

This project has a knowledge graph at graphify-out/ with god nodes, community structure, and cross-file relationships.

When the user types `/graphify`, use the installed graphify skill or instructions before doing anything else.

Rules:
- For codebase questions, first run `graphify query "<question>"` when graphify-out/graph.json exists. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts. These return a scoped subgraph, usually much smaller than GRAPH_REPORT.md or raw grep output.
- Dirty graphify-out/ files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip graphify if the task is about stale or incorrect graph output, or the user explicitly says not to use it.
- If graphify-out/wiki/index.md exists, use it for broad navigation instead of raw source browsing.
- Read graphify-out/GRAPH_REPORT.md only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying code, run `graphify update .` to keep the graph current (AST-only, no API cost).
