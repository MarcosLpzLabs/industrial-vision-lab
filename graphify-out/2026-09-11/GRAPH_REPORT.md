# Graph Report - industrial-vision-lab  (2026-08-15)

## Corpus Check
- Corpus is ~21,198 words - fits in a single context window. You may not need a graph.

## Summary
- 111 nodes · 131 edges · 12 communities (8 shown, 4 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Pipeline PDI de CameraService
- Tracking y conteo de piezas
- Config de agentes OpenCode
- Docs del curso y skill graphify
- Contexto y reglas del curso
- Inspección de calidad (aspect ratio)
- Persistencia CSV StorageService
- Plugin graphify (hook)
- Regla constructor limpio
- Regla de oro de renderizado

## God Nodes (most connected - your core abstractions)
1. `CameraService` - 19 edges
2. `graphify skill (/graphify pipeline)` - 10 edges
3. `StorageService` - 7 edges
4. `TrackingService` - 7 edges
5. `CameraConectionError` - 6 edges
6. `InspectionService` - 6 edges
7. `permission` - 5 edges
8. `permission` - 5 edges
9. `TrackedObject` - 5 edges
10. `Teacher agent (profesor-mentor)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `resumen_y_avance.txt (resumen técnico transferible)` --semantically_similar_to--> `avance.md (informe de avance del alumno)`  [INFERRED] [semantically similar]
  resumen_y_avance.txt → avance.md
- `CameraConectionError (typo histórico exportado en services/__init__.py)` --semantically_similar_to--> `CameraConnectionError (excepción personalizada de pérdida de cámara)`  [INFERRED] [semantically similar]
  AGENTS.md → general_context.md
- `README.md — Industrial Vision Lab` --conceptually_related_to--> `general_context.md (contexto general del curso)`  [INFERRED]
  README.md → general_context.md
- `Sacar contexto.txt (prompt de transferencia de contexto)` --conceptually_related_to--> `resumen_y_avance.txt (resumen técnico transferible)`  [INFERRED]
  Sacar contexto.txt → resumen_y_avance.txt
- `Pureza de datos en capas de persistencia (solo tipos primitivos, nunca matrices ni texto de UI)` --rationale_for--> `StorageService (única capa de persistencia en disco, CSV + JPG)`  [INFERRED]
  avance.md → general_context.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Teacher-Sumary course context update flow** — _opencode_agents_teacher, _opencode_agents_sumary, indice, general_context, avance [EXTRACTED 1.00]
- **industrial-vision-lab service-oriented architecture** — general_context_camera_info_app, general_context_camerasservice, general_context_storageservice, general_context_inspectionservice, general_context_trackingservice [EXTRACTED 1.00]
- **Reglas industriales de diseño del curso** — general_context_regla_oro_renderizado, general_context_constructor_limpio, general_context_persistencia_30_frames, general_context_tolerancia_aspect_ratio, avance_pureza_datos_persistencia [EXTRACTED 1.00]

## Communities (12 total, 4 thin omitted)

### Community 0 - "Pipeline PDI de CameraService"
Cohesion: 0.10
Nodes (7): CameraService, Aplica filtros de suavizado para eliminar el ruido electrónico de la ROI., Detecta los contornos de la pieza usando el algoritmo de Canny., Encuentra los contornos en la imagen de bordes y los filtra por tamaño., Calcula el rectángulo delimitador de un contorno dado., Calcula el área de un contorno dado., Convierte la ROI a escala de grises UNA sola vez.

### Community 1 - "Tracking y conteo de piezas"
Cohesion: 0.17
Nodes (7): Exception, CameraConectionError, Excepción personalizada para errores de conexión de la cámara., Recibe los centroides del frame actual [(cx, cy), (cx, cy)...] Actualiza los…, Registra un nuevo objeto. Si se pasa `container`, el nuevo objeto se añadirá…, TrackedObject, TrackingService

### Community 2 - "Config de agentes OpenCode"
Cohesion: 0.14
Nodes (16): agent, sumary, teacher, default_agent, bash, edit, read, skill (+8 more)

### Community 3 - "Docs del curso y skill graphify"
Cohesion: 0.18
Nodes (16): Sumary agent (subagente de contexto), Teacher agent (profesor-mentor), graphify reference: add URL and watch folder, graphify reference: extra exports and benchmark, graphify reference: extraction subagent prompt spec, graphify reference: GitHub clone and cross-repo merge, graphify reference: commit hook and CLAUDE.md integration, graphify reference: query, path, explain traversals (+8 more)

### Community 4 - "Contexto y reglas del curso"
Cohesion: 0.15
Nodes (16): CameraConectionError (typo histórico exportado en services/__init__.py), Módulo 5: HMI, métricas y persistencia de producción (completado), Módulo 6: especialización avanzada (filtro de forma, conteo, refactor) — en proceso, Pureza de datos en capas de persistencia (solo tipos primitivos, nunca matrices ni texto de UI), apps/camera_info.py (orquestador principal, bucle while True), CameraConnectionError (excepción personalizada de pérdida de cámara), CameraService (servicio de cámara, cv2.VideoCapture + pipeline PDI), InspectionService (reglas de calidad por aspect ratio) (+8 more)

### Community 5 - "Inspección de calidad (aspect ratio)"
Cohesion: 0.22
Nodes (4): ndarray, InspectionService, Calcula la relación de aspecto (w / h) de un contorno dado. Retorna float si el…, Determina si el aspect ratio calculado entra dentro del rango de tolerancia.…

## Knowledge Gaps
- **20 isolated node(s):** `$schema`, `default_agent`, `description`, `mode`, `webfetch` (+15 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CameraService` connect `Pipeline PDI de CameraService` to `Tracking y conteo de piezas`, `Inspección de calidad (aspect ratio)`?**
  _High betweenness centrality (0.152) - this node is a cross-community bridge._
- **Why does `InspectionService` connect `Inspección de calidad (aspect ratio)` to `Tracking y conteo de piezas`?**
  _High betweenness centrality (0.051) - this node is a cross-community bridge._
- **What connects `$schema`, `default_agent`, `description` to the rest of the system?**
  _20 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Pipeline PDI de CameraService` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `Config de agentes OpenCode` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._