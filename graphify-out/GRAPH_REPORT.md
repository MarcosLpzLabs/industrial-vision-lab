# Graph Report - industrial-vision-lab  (2026-09-11)

## Corpus Check
- 27 files · ~22,504 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 115 nodes · 135 edges · 13 communities (9 shown, 4 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 6 edges (avg confidence: 0.82)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `8b79cc47`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- CameraService
- TrackingService
- permission
- graphify skill (/graphify pipeline)
- Módulo 6: especialización avanzada (filtro de forma, conteo, refactor) — en proceso
- services/__init__.py
- StorageService
- graphify.js
- Constructores limpios (__init__ solo inicializa atributos, sin I/O ni bucles)
- Regla de oro de renderizado (matrices primero, un único cv2.imshow al final)
- .opencode/opencode.json

## God Nodes (most connected - your core abstractions)
1. `CameraService` - 19 edges
2. `graphify skill (/graphify pipeline)` - 10 edges
3. `TrackingService` - 8 edges
4. `StorageService` - 7 edges
5. `CameraConectionError` - 6 edges
6. `InspectionService` - 6 edges
7. `permission` - 5 edges
8. `permission` - 5 edges
9. `TrackedObject` - 5 edges
10. `Sumary agent (subagente de contexto)` - 5 edges

## Surprising Connections (you probably didn't know these)
- `resumen_y_avance.txt (resumen técnico transferible)` --semantically_similar_to--> `avance.md (informe de avance del alumno)`  [INFERRED] [semantically similar]
  resumen_y_avance.txt → avance.md
- `CameraConectionError (typo histórico exportado en services/__init__.py)` --semantically_similar_to--> `CameraConnectionError (excepción personalizada de pérdida de cámara)`  [INFERRED] [semantically similar]
  AGENTS.md → general_context.md
- `README.md — Industrial Vision Lab` --conceptually_related_to--> `general_context.md (contexto general del curso)`  [INFERRED]
  README.md → general_context.md
- `FASE 1 — Python profesional (refactorización de industrial-vision-lab)` --conceptually_related_to--> `Módulo 6: especialización avanzada (filtro de forma, conteo, refactor) — en proceso`  [INFERRED]
  indice.md → avance.md
- `Pureza de datos en capas de persistencia (solo tipos primitivos, nunca matrices ni texto de UI)` --rationale_for--> `StorageService (única capa de persistencia en disco, CSV + JPG)`  [INFERRED]
  avance.md → general_context.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Teacher-Sumary course context update flow** — _opencode_agents_teacher, _opencode_agents_sumary, indice, general_context, avance [EXTRACTED 1.00]
- **Reglas industriales de diseño del curso** — general_context_regla_oro_renderizado, general_context_constructor_limpio, general_context_persistencia_30_frames, general_context_tolerancia_aspect_ratio, avance_pureza_datos_persistencia [EXTRACTED 1.00]
- **industrial-vision-lab service-oriented architecture** — general_context_camera_info_app, general_context_camerasservice, general_context_storageservice, general_context_inspectionservice, general_context_trackingservice [EXTRACTED 1.00]

## Communities (13 total, 4 thin omitted)

### Community 0 - "CameraService"
Cohesion: 0.10
Nodes (7): CameraService, Aplica filtros de suavizado para eliminar el ruido electrónico de la ROI., Detecta los contornos de la pieza usando el algoritmo de Canny., Encuentra los contornos en la imagen de bordes y los filtra por tamaño., Calcula el rectángulo delimitador de un contorno dado., Calcula el área de un contorno dado., Convierte la ROI a escala de grises UNA sola vez.

### Community 1 - "TrackingService"
Cohesion: 0.23
Nodes (4): Recibe los centroides del frame actual [(cx, cy), (cx, cy)...] Actualiza los…, Registra un nuevo objeto. Si se pasa `container`, el nuevo objeto se añadirá…, TrackedObject, TrackingService

### Community 2 - "permission"
Cohesion: 0.14
Nodes (16): agent, sumary, teacher, default_agent, bash, edit, read, skill (+8 more)

### Community 3 - "graphify skill (/graphify pipeline)"
Cohesion: 0.18
Nodes (16): Sumary agent (subagente de contexto), Teacher agent (profesor-mentor), graphify reference: add URL and watch folder, graphify reference: extra exports and benchmark, graphify reference: extraction subagent prompt spec, graphify reference: GitHub clone and cross-repo merge, graphify reference: commit hook and CLAUDE.md integration, graphify reference: query, path, explain traversals (+8 more)

### Community 4 - "Módulo 6: especialización avanzada (filtro de forma, conteo, refactor) — en proceso"
Cohesion: 0.15
Nodes (16): CameraConectionError (typo histórico exportado en services/__init__.py), Módulo 5: HMI, métricas y persistencia de producción (completado), Módulo 6: especialización avanzada (filtro de forma, conteo, refactor) — en proceso, Pureza de datos en capas de persistencia (solo tipos primitivos, nunca matrices ni texto de UI), apps/camera_info.py (orquestador principal, bucle while True), CameraConnectionError (excepción personalizada de pérdida de cámara), CameraService (servicio de cámara, cv2.VideoCapture + pipeline PDI), InspectionService (reglas de calidad por aspect ratio) (+8 more)

### Community 5 - "services/__init__.py"
Cohesion: 0.16
Nodes (7): Exception, ndarray, CameraConectionError, Excepción personalizada para errores de conexión de la cámara., InspectionService, Calcula la relación de aspecto (w / h) de un contorno dado. Retorna float si el…, Determina si el aspect ratio calculado entra dentro del rango de tolerancia.…

### Community 12 - ".opencode/opencode.json"
Cohesion: 0.50
Nodes (3): plugin, $schema, .opencode/plugins/graphify.js

## Knowledge Gaps
- **22 isolated node(s):** `$schema`, `.opencode/plugins/graphify.js`, `$schema`, `default_agent`, `description` (+17 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **4 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `CameraService` connect `CameraService` to `TrackingService`, `services/__init__.py`?**
  _High betweenness centrality (0.142) - this node is a cross-community bridge._
- **Why does `InspectionService` connect `services/__init__.py` to `TrackingService`?**
  _High betweenness centrality (0.047) - this node is a cross-community bridge._
- **Why does `TrackingService` connect `TrackingService` to `services/__init__.py`?**
  _High betweenness centrality (0.044) - this node is a cross-community bridge._
- **What connects `$schema`, `.opencode/plugins/graphify.js`, `$schema` to the rest of the system?**
  _22 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `CameraService` be split into smaller, more focused modules?**
  _Cohesion score 0.09523809523809523 - nodes in this community are weakly interconnected._
- **Should `permission` be split into smaller, more focused modules?**
  _Cohesion score 0.13970588235294118 - nodes in this community are weakly interconnected._