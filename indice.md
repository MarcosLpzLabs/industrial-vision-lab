# ROADMAP DE FORMACIÓN — INGENIERO DE SISTEMAS INTELIGENTES INDUSTRIALES [14]

Este índice de contenidos estructura la ruta formativa diseñada para adquirir capacidades en diseño, desarrollo y despliegue de soluciones completas de visión artificial e inteligencia artificial aplicada en el sector industrial [1, 21]. Los módulos prácticos del proyecto de desarrollo `industrial-vision-lab` se integran y relacionan directamente con sus fases teóricas correspondientes [6, 22, 33].

---

## FASE 0 — Fundamentos de desarrollo profesional [14]
* **Objetivo:** Sentar las bases técnicas de desarrollo de software profesional, abandonando la creación de scripts aislados para comenzar a construir sistemas estructurados [14].
* **Proyecto Práctico Asociado:** `industrial-vision-lab` (Estado actual: En curso) [15].

### 0.1 Git y GitHub [14]
* **Contenido:** Uso profesional del control de versiones [14]. Comprende la gestión de repositorios, creación de commits, ramificación (branches), fusión de código (merge), resolución de conflictos, Pull Requests y un flujo de trabajo básico con Git Flow [14].

### 0.2 Linux práctico [14]
* **Contenido:** Adquisición de soltura en entornos de terminal [3]. Uso de la shell, administración de permisos de archivos, control de procesos del sistema, conexiones remotas seguras por SSH, monitorización de logs, gestión de servicios con Systemd y fundamentos de direccionamiento y networking básico [14].

### 0.3 Entornos Python [14]
* **Contenido:** Gestión moderna de proyectos de desarrollo en Python utilizando la herramienta `uv` [14]. Configuración mediante `pyproject.toml`, resolución e instalación de dependencias y aislamiento mediante entornos virtuales [14].

### 0.4 Arquitectura básica [14]
* **Contenido:** Introducción al diseño de software limpio [14]. Separación de responsabilidades, definición y uso de clases, implementación de servicios específicos, centralización de configuraciones y estructuración profesional de proyectos de software [14].

---

## FASE 1 — Python profesional [15]
* **Objetivo:** Aprender a construir software industrial mantenible, desacoplado y preparado para arquitecturas robustas [15, 31].
* **Proyecto Práctico Asociado:** Refactorización completa de `industrial-vision-lab` [16].
* **Módulos Prácticos Relacionados:**
  * **Módulo 5 (Completado):** Aplicación práctica del diseño orientado a objetos y modularización a través de la creación de las capas de servicios independientes `CameraService` y `StorageService` [24, 25, 29].
  * **Módulo 6 - Punto 6.3 (Pendiente de integración):** Refactorización para trasladar y encapsular la lógica de binarización y dibujo del script principal `camera_info.py` hacia los servicios dedicados, preparando el sistema para arquitecturas multihilo avanzadas [31, 32].

### 1.1 Arquitectura Python [15]
* **Contenido:** Organización avanzada del código mediante la creación de paquetes de software, resolución óptima de imports, modularización y creación de servicios independientes con responsabilidades claras [15, 26].

### 1.2 Diseño orientado a objetos [15]
* **Contenido:** Diseño de APIs y estructuración interna de clases [4]. Separación estricta de responsabilidades, uso de la composición en lugar de herencia, definición de interfaces y minimización del acoplamiento entre servicios [10, 11, 15].

### 1.3 Gestión de errores [15]
* **Contenido:** Robustez en entornos de planta mediante el manejo de excepciones personalizadas de bajo nivel (como `CameraConnectionError`), logging de eventos y validación estricta de entradas y flujos de datos [15, 24].

### 1.4 Configuración [15]
* **Contenido:** Externalización de parámetros de ejecución mediante el uso de variables de entorno y archivos de configuración desacoplados del código fuente [15].

### 1.5 Testing [15]
* **Contenido:** Aseguramiento de la calidad del software utilizando el framework de pruebas `pytest` [16]. Creación de mocks para simular hardware o servicios de persistencia, y análisis de cobertura de test (code coverage) [16].

---

## FASE 2 — Computer Vision clásica [16]
* **Objetivo:** Dominar el procesamiento digital de imágenes clásico para fundamentar el análisis visual antes de integrar modelos de Inteligencia Artificial [16].
* **Proyecto Práctico Asociado:** Toolkit reutilizable de visión industrial [16].
* **Módulos Prácticos Relacionados:**
  * **Módulo 6 - Punto 6.1 (Pendiente de integración):** Filtro de forma utilizando la Relación de Aspecto (Aspect Ratio) del bounding box de contornos para identificar piezas deformadas bajo tolerancias de inspección industriales de entre 0.8 y 1.2 [30].
  * **Módulo 6 - Punto 6.2 (Pendiente de integración):** Diseño de un servicio de seguimiento (`TrackingService`) de centroides con máquina de estados para el conteo de piezas acumuladas al cruzar una línea virtual [30, 32].

### 2.1 OpenCV [16]
* **Contenido:** Fundamentos de manipulación de matrices de imágenes, flujos de vídeo en tiempo real, conversión entre espacios de color y aplicación de filtros digitales de reducción de ruido [16].

### 2.2 Procesamiento [16]
* **Contenido:** Técnicas clave de segmentación [16]. Umbralización fija (thresholding) y binarización adaptativa gaussiana, operaciones morfológicas de limpieza (opening y closing), detección de bordes mediante Canny y análisis topológico de contornos [24, 27].

### 2.3 Geometría [16]
* **Contenido:** Corrección espacial de imágenes [16]. Transformaciones de perspectiva, calibración de lentes y cámaras, y cálculo de homografías para medición espacial precisa [16].

### 2.4 OCR clásico [16]
* **Contenido:** Reconocimiento óptico de caracteres clásico mediante algoritmos de segmentación y comparación de plantillas [16].

---

## FASE 3 — Sistemas de adquisición industrial [17]
* **Objetivo:** Conectar y capturar imágenes desde sensores y cámaras reales empleando protocolos industriales [17].
* **Proyecto Práctico Asociado:** Capturador industrial de datasets [17].

### 3.1 Cámaras [17]
* **Contenido:** Características e integración de cámaras bajo conexión directa USB, flujos de streaming de red bajo protocolo RTSP e introducción a los estándares de comunicación de alta velocidad GigE Vision [17].

### 3.2 Gestión de vídeo [17]
* **Contenido:** Grabación de secuencias de vídeo, gestión y sincronización de múltiples streams simultáneos y optimización de renderizado para eliminar latencias de visualización [17, 27].

### 3.3 Dataset management [17]
* **Contenido:** Estrategias automatizadas para capturar, etiquetar, almacenar y organizar colecciones de imágenes en disco estructuradas para el entrenamiento posterior de modelos [17].

---

## FASE 4 — IA aplicada a visión [17]
* **Objetivo:** Diseñar y entrenar pipelines completos de aprendizaje profundo orientados a tareas de control de calidad e inspección visual [17, 18].
* **Proyecto Práctico Asociado:** Sistema industrial de inspección visual [18].

### 4.1 PyTorch [17]
* **Contenido:** Fundamentos de deep learning [17]. Manipulación de tensores, diseño de datasets y dataloaders personalizados, e implementación de bucles de entrenamiento completos (training loops) [17].

### 4.2 YOLO [17]
* **Contenido:** Inferencia y entrenamiento supervisado de la familia de modelos YOLO, fine-tuning con datasets propios y optimización de hiperparámetros [17].

### 4.3 Clasificación [17]
* **Contenido:** Arquitecturas de redes neuronales para categorización automática de productos y defectos en imágenes individuales [17].

### 4.4 Detección [18]
* **Contenido:** Localización de objetos múltiples e identificación de regiones defectuosas dentro de una imagen mediante bounding boxes predictivos [18].

### 4.5 Segmentación [18]
* **Contenido:** Clasificación píxel a píxel de piezas y defectos para análisis métricos y geométricos avanzados de alta precisión [18].

---

## FASE 5 — Edge AI [18]
* **Objetivo:** Desplegar y ejecutar modelos de Deep Learning directamente en hardware embebido de planta de bajos recursos garantizando la mínima latencia [18].
* **Proyecto Práctico Asociado:** Nodo Edge AI autónomo [18].

### 5.1 ONNX [18]
* **Contenido:** Exportación, estandarización e interoperabilidad de modelos entrenados en PyTorch u otros frameworks hacia un formato común de representación optimizado [17, 18].

### 5.2 TensorRT [18]
* **Contenido:** Optimización de modelos mediante el compilador de NVIDIA para aceleración drástica de la inferencia en tarjetas gráficas de consumo y dispositivos embebidos [18].

### 5.3 Optimización [18]
* **Contenido:** Técnicas de poda de redes neuronales (pruning), simplificación de capas y fusión de operaciones matemáticas para reducir el tamaño del modelo y acelerar la ejecución [18].

### 5.4 Cuantización [18]
* **Contenido:** Reducción de la precisión matemática de los pesos del modelo (por ejemplo, de FP32 a FP16 o INT8) para maximizar la velocidad de cálculo con una pérdida mínima de precisión [18].

### 5.5 Jetson [18]
* **Contenido:** Configuración, despliegue físico y optimización de pipelines de visión artificial en la plataforma de hardware embebido industrial NVIDIA Jetson [2, 18].

---

## FASE 6 — Backend industrial [18]
* **Objetivo:** Construir servicios y capas de software robustas alrededor de los modelos de visión artificial para exponerlos y consumirlos [18].
* **Proyecto Práctico Asociado:** Backend de Industrial Vision Platform [19].

### 6.1 FastAPI [18]
* **Contenido:** Creación de APIs REST de alto rendimiento y asíncronas para el control de los servicios de visión y el envío de peticiones de inferencia [18].

### 6.2 PostgreSQL [18]
* **Contenido:** Diseño de bases de datos relacionales para almacenar configuraciones de inspección, registros históricos, alarmas y logs de producción de forma persistente y segura [18].

### 6.3 Redis [18]
* **Contenido:** Uso de bases de datos en memoria para caché rápida, almacenamiento temporal de estados de línea y colas de tareas de alta velocidad [18].

### 6.4 WebSockets [19]
* **Contenido:** Canales de comunicación bidireccional en tiempo real para retransmitir métricas instantáneas, eventos de inspección y vídeo procesado directamente a interfaces de usuario HMI [19, 23].

### 6.5 APIs industriales [19]
* **Contenido:** Diseño de contratos de API robustos adaptados para interactuar con sistemas SCADA, HMI locales de fábrica y pasarelas de enlace de datos de planta [19].

---

## FASE 7 — Comunicaciones industriales [19]
* **Objetivo:** Integrar la inteligencia de software con la red física de automatización de planta y sistemas de control clásicos [19].
* **Proyecto Práctico Asociado:** IA conectada a sistemas industriales [19].

### 7.1 MQTT [19]
* **Contenido:** Protocolo de mensajería ligero basado en publicación/suscripción, ideal para topologías IoT, reporte de alarmas rápidas y telemetría de Edge AI hacia servidores locales o en la nube [2, 19].

### 7.2 OPC-UA [19]
* **Contenido:** Estándar de comunicación industrial interoperable, orientado a objetos, seguro y extensible para el intercambio de datos entre el software de visión artificial y sistemas SCADA/PLCs [2, 19].

### 7.3 Modbus [19]
* **Contenido:** Protocolo clásico de comunicación industrial para lectura y escritura directa de registros de sensores, actuadores y controladores de planta [19].

### 7.4 PLC Integration [19]
* **Contenido:** Sincronización física de disparos (triggers) de cámara, recepción de señales de sincronización de cinta y envío de comandos de expulsión o descarte a controladores lógicos programables (PLCs) [2, 19].

---

## FASE 8 — LLMs industriales [19]
* **Objetivo:** Implementar modelos de lenguaje natural y visión multimodal localmente para interactuar con la información técnica y de control de planta [19, 20].
* **Proyecto Práctico Asociado:** Copiloto industrial local [20].

### 8.1 Ollama [19]
* **Contenido:** Ejecución local y privada de modelos de lenguaje de gran tamaño (LLMs) sin dependencia de servidores externos de internet, garantizando la privacidad de los datos industriales [2, 20].

### 8.2 Embeddings [20]
* **Contenido:** Conversión de textos técnicos, manuales de maquinaria e históricos de fallos en vectores semánticos para búsquedas inteligentes rápidas [20].

### 8.3 RAG [20]
* **Contenido:** Implementación de sistemas de Generación Aumentada por Recuperación (Retrieval-Augmented Generation) para conectar los LLMs a la documentación técnica interna de la planta [20].

### 8.4 Multimodalidad [20]
* **Contenido:** Integración de modelos de visión-lenguaje que permiten analizar visualmente una pieza o un fallo mecánico a partir de una foto y responder preguntas de diagnóstico en lenguaje natural [20].

### 8.5 Asistentes técnicos [20]
* **Contenido:** Desarrollo de agentes conversacionales inteligentes entrenados para guiar paso a paso a los operadores y mantenedores de planta en la resolución de incidencias en maquinaria [20].

---

## FASE 9 — Arquitectura distribuida [20]
* **Objetivo:** Escalar, monitorizar y gestionar múltiples celdas de inspección en diferentes líneas o fábricas [20].
* **Proyecto Práctico Asociado:** Industrial AI Platform [20].

### 9.1 Docker [20]
* **Contenido:** Contenedorización de servicios individuales (captura, inferencia, almacenamiento, frontend) para garantizar la portabilidad y homogeneidad entre el ordenador de desarrollo y el hardware de planta [20].

### 9.2 Docker Compose [20]
* **Contenido:** Orquestación local de múltiples contenedores interconectados mediante una configuración centralizada [20].

### 9.3 Observabilidad [20]
* **Contenido:** Integración de herramientas de telemetría, trazabilidad de logs centralizados, monitorización de recursos de hardware (CPU/GPU) y alertas de caída de servicios en producción [20].

### 9.4 Despliegue [20]
* **Contenido:** Estrategias seguras y eficientes para instalar y actualizar software industrial en caliente sin detener procesos de producción [20].

### 9.5 Edge + Cloud [20]
* **Contenido:** Arquitecturas híbridas que combinan procesamiento crítico en tiempo real de baja latencia en el Edge (planta) y consolidación histórica, analítica agregada y reentrenamiento en la nube [20].

---

## FASE 10 — Producto real [20]
* **Objetivo:** Convertir los conocimientos técnicos y arquitectónicos en un modelo de negocio de base tecnológica escalable y comercializable [1, 20].
* **Resultado Final del Roadmap:** Capacidad autónoma para diseñar, desarrollar, certificar y desplegar productos de IA industrial completos de extremo a extremo [21].

### 10.1 Portfolio [20]
* **Contenido:** Documentación profesional y exposición del código limpio desarrollado en plataformas públicas como GitHub para demostrar capacidad técnica avanzada ante clientes e inversores [5, 20].

### 10.2 Demos [21]
* **Contenido:** Creación de prototipos rápidos interactivos y funcionales (interfaces web locales o simulaciones visuales) para mostrar el potencial de la tecnología a posibles clientes sin necesidad de instalación física [21, 23].

### 10.3 Casos de uso [21]
* **Contenido:** Estudio, documentación y cuantificación del retorno de inversión (ROI) de aplicaciones industriales reales resueltas mediante visión artificial e IA [21].

### 10.4 MVPs [21]
* **Contenido:** Construcción de Productos Mínimos Viables robustos y estables orientados a solventar un problema industrial real específico [21, 22].

### 10.5 Comercialización [21]
* **Contenido:** Fundamentos de empaquetado del software, licenciamiento, planes de mantenimiento técnico, escalabilidad comercial y estrategias de venta para startups tecnológicas de automatización inteligente [1, 21].
