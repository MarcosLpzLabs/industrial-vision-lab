# Graph Report - industrial-vision-lab  (2026-11-06)

## Corpus Check
- 6 files · ~29,661 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 200 nodes · 263 edges · 19 communities (11 shown, 8 thin omitted)
- Extraction: 86% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 37 edges (avg confidence: 0.87)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Contexto del curso y persistencia
- CameraService y pipeline PDI
- RenderService y paquete services
- Configuración OpenCode
- Renderizado y refactor 6.3
- Agentes Teacher y Sumary
- Referencias graphify
- Tracking de piezas
- Arquitectura y proyecto
- Inspección de forma
- Persistencia de producción
- Plugin graphify
- Esquema OpenCode
- Resúmenes de contexto
- Excepción de cámara
- Fase 1 Python
- Fase 2 Computer Vision

## God Nodes (most connected - your core abstractions)
1. `Informe de avance y conocimientos adquiridos` - 20 edges
2. `Contexto general del curso de vision artificial industrial` - 18 edges
3. `CameraService` - 17 edges
4. `StorageService` - 14 edges
5. `apps/camera_info.py (orquestador fino; delega el renderizado)` - 10 edges
6. `Teacher (agente profesor primario)` - 9 edges
7. `graphify skill (/graphify pipeline)` - 9 edges
8. `RenderService` - 9 edges
9. `RenderService` - 8 edges
10. `Cierre de tareas pendientes del 6.3 (evaluación 7/10)` - 8 edges

## Surprising Connections (you probably didn't know these)
- `RenderService: servicio dedicado de renderizado HMI (implementado)` --semantically_similar_to--> `RenderService`  [INFERRED] [semantically similar]
  avance.md → general_context.md
- `Ciclo de vida de la UI en OpenCV (namedWindow)` --semantically_similar_to--> `Multiples ventanas de renderizado simultaneas`  [INFERRED] [semantically similar]
  avance.md → general_context.md
- `Arquitectura limpia y principios SOLID` --conceptually_related_to--> `Arquitectura de capas de servicios independientes`  [INFERRED]
  avance.md → README.md
- `Pipeline de PDI clasico` --references--> `CameraService`  [INFERRED]
  README.md → general_context.md
- `Persistencia cada 30 frames` --references--> `StorageService`  [INFERRED]
  README.md → general_context.md

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **Flujo Teacher -> Sumary de actualizacion de contexto** — opencode_agents_teacher_agente_teacher, opencode_agents_teacher_invocar_sumary, opencode_agents_sumary_agente_sumary, opencode_agents_sumary_cierre_de_punto [EXTRACTED 1.00]
- **Reglas industriales de diseño del curso** — general_context_regla_oro_renderizado, general_context_persistencia_30_frames [EXTRACTED 1.00]

## Communities (19 total, 8 thin omitted)

### Community 0 - "Contexto del curso y persistencia"
Cohesion: 0.08
Nodes (43): Transformacion de coordenadas con broadcasting NumPy, Calificacion Git y GitHub 5/10, Calificacion Linux CachyOS 6/10, Calificación Python 7/10, Cierre de tareas pendientes del 6.3 (evaluación 7/10), Limpieza de código muerto (completada: text_cnt_*, ar = None, comentarios, threshold_roi), Fricción: mezclar responsabilidades al refactorizar, Fricción: fallo silencioso de cv2.imwrite (+35 more)

### Community 1 - "CameraService y pipeline PDI"
Cohesion: 0.08
Nodes (10): Exception, CameraConectionError, CameraService, Excepción personalizada para errores de conexión de la cámara., Aplica filtros de suavizado para eliminar el ruido electrónico de la ROI., Detecta los contornos de la pieza usando el algoritmo de Canny., Encuentra los contornos en la imagen de bordes y los filtra por tamaño., Calcula el rectángulo delimitador de un contorno dado. (+2 more)

### Community 2 - "RenderService y paquete services"
Cohesion: 0.13
Nodes (11): csv, cv2, dataclasses, datetime, logging, math, numpy, os (+3 more)

### Community 3 - "Configuración OpenCode"
Cohesion: 0.12
Nodes (18): agent, sumary, teacher, default_agent, bash, edit, read, skill (+10 more)

### Community 4 - "Renderizado y refactor 6.3"
Cohesion: 0.17
Nodes (15): Ciclo de vida de la UI en OpenCV (namedWindow), Derivación de geometría configurada sin números mágicos, Opción A: el renderer desconoce la ROI y recibe coordenadas globales, Punto 6.3: Desacoplamiento estricto de binarización y dibujado (completado), RenderablePiece (dataclass: contour, is_ok), RenderService: servicio dedicado de renderizado HMI (implementado), Sintaxis OOP: parámetro self y dataclasses, Eliminación de valores cableados 200/500 en draw_line (completada) (+7 more)

### Community 5 - "Agentes Teacher y Sumary"
Cohesion: 0.19
Nodes (15): Finalizacion: actualizar grafo graphify, Sumary (subagente de mantenimiento de contexto), avance.md (informe de avance del alumno), Operacion 1: Cierre de punto, Operacion 2: Desviacion de indice, general_context.md (contexto del curso), indice.md (hoja de ruta del curso), Teacher (agente profesor primario) (+7 more)

### Community 6 - "Referencias graphify"
Cohesion: 0.18
Nodes (11): graphify reference: add URL and watch folder, graphify reference: extra exports and benchmark, graphify reference: extraction subagent prompt spec, graphify reference: GitHub clone and cross-repo merge, graphify reference: commit hook and CLAUDE.md integration, graphify reference: query, path, explain traversals, graphify reference: transcribe video and audio, graphify reference: incremental update and cluster-only (+3 more)

### Community 7 - "Tracking de piezas"
Cohesion: 0.27
Nodes (4): Recibe los centroides del frame actual [(cx, cy), (cx, cy)...] Actualiza los…, Registra un nuevo objeto. Si se pasa `container`, el nuevo objeto se añadirá…, TrackedObject, TrackingService

### Community 8 - "Arquitectura y proyecto"
Cohesion: 0.25
Nodes (9): Arquitectura limpia y principios SOLID, CameraConnectionError (excepcion publica), CameraService, apps/test_camera.py (verificacion rapida), Arquitectura de capas de servicios independientes, CameraConectionError (typo historico), industrial-vision-lab (proyecto), Pipeline de PDI clasico (+1 more)

### Community 9 - "Inspección de forma"
Cohesion: 0.25
Nodes (4): ndarray, InspectionService, Calcula la relación de aspecto (w / h) de un contorno dado. Retorna float si el…, Determina si el aspect ratio calculado entra dentro del rango de tolerancia.…

### Community 11 - "Plugin graphify"
Cohesion: 0.40
Nodes (3): IMPORTANT: keep the reminder string free of backticks and $(...) constructs., ref_fs, ref_path

## Knowledge Gaps
- **39 isolated node(s):** `$schema`, `CameraConectionError (typo historico)`, `Stack tecnologico (Python, OpenCV, NumPy, Git, Linux)`, `resumen_y_avance.txt (resumen técnico transferible)`, `Sacar contexto.txt (prompt de transferencia de contexto)` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 89 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **8 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Contexto general del curso de vision artificial industrial` connect `Contexto del curso y persistencia` to `Renderizado y refactor 6.3`, `Agentes Teacher y Sumary`?**
  _High betweenness centrality (0.065) - this node is a cross-community bridge._
- **Why does `Teacher (agente profesor primario)` connect `Agentes Teacher y Sumary` to `Contexto del curso y persistencia`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 8 inferred relationships involving `StorageService` (e.g. with `Fricción: mezclar responsabilidades al refactorizar` and `Fricción: fallo silencioso de cv2.imwrite`) actually correct?**
  _`StorageService` has 8 INFERRED edges - model-reasoned connections that need verification._
- **Are the 4 inferred relationships involving `apps/camera_info.py (orquestador fino; delega el renderizado)` (e.g. with `Transformacion de coordenadas con broadcasting NumPy` and `Separación captura/renderizado pendiente (preparación multihilo)`) actually correct?**
  _`apps/camera_info.py (orquestador fino; delega el renderizado)` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `CameraConectionError (typo historico)`, `Stack tecnologico (Python, OpenCV, NumPy, Git, Linux)` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Contexto del curso y persistencia` be split into smaller, more focused modules?**
  _Cohesion score 0.08194905869324474 - nodes in this community are weakly interconnected._
- **Should `CameraService y pipeline PDI` be split into smaller, more focused modules?**
  _Cohesion score 0.07977207977207977 - nodes in this community are weakly interconnected._