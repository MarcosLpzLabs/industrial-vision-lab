# CONTEXTO GENERAL DEL CURSO — PROYECTO INDUSTRIAL-VISION-LAB [22, 32]

Este documento recopila de manera detallada y estructurada el contexto completo, los objetivos formativos, la pila tecnológica, las metodologías de diseño y los problemas arquitectónicos resueltos durante el curso práctico de visión artificial industrial [22].

---

## 1. INTRODUCCIÓN Y OBJETIVOS DEL CURSO [22]

El enfoque de esta formación no corresponde al de un desarrollo de software guiado o tutorial de programación convencional [22]. Se trata de un **curso práctico de ingeniería de software para visión artificial industrial** [22]. La filosofía de aprendizaje es **"aprender construyendo"** [1, 22]. En lugar de implementar scripts de prueba aislados o modelos conceptuales simples, el alumno se enfrenta a la construcción de una solución de software reutilizable, robusta y estructuralmente limpia que simula una celda de inspección automatizada en una planta de fabricación real [22].

### Objetivos Profesionales a Corto y Medio Plazo:
* **Evolución del Perfil Técnico:** Adquirir capacidades sólidas en diseño arquitectónico de software, dejando atrás la programación heurística de scripts rápidos para desarrollar software industrial estructurado, desacoplado y de alta mantenibilidad en producción [14, 15].
* **Especialización Clave:** Profundizar en los campos de Visión de Computador (Computer Vision), Inteligencia Artificial aplicada en entornos productivos, Edge AI (procesamiento en hardware embebido), comunicaciones industriales y arquitectura de sistemas complejos [1].
* **Meta Comercial:** Sentar las bases técnicas y metodológicas para fundar, junto a otros tres socios, una empresa de base tecnológica (startup) orientada al despliegue de soluciones de Inteligencia Artificial para el sector industrial [1]. El objetivo es ser capaces de suministrar productos comerciales e industriales de extremo a extremo, no limitándose al diseño de modelos de IA, sino integrando la adquisición de imagen, el procesamiento matemático, la persistencia, las interfaces de usuario de planta y los protocolos de red industrial [1].

---

## 2. PERFIL DEL ALUMNO Y DISPONIBILIDAD [2]

El alumno cuenta con un trasfondo técnico de gran valor para la asimilación de conceptos industriales prácticos [26]:

* **Formación Académica:** Graduado en Ingeniería Electrónica Industrial y Automática [2].
* **Experiencia Previa:** Cuenta con experiencia en automatización industrial clásica, manejo y programación de controladores lógicos programables (PLCs Siemens), programación y configuración de robótica industrial (ABB y KUKA), desarrollo de aplicaciones VBA, fundamentos de visión artificial, lenguaje Python e IA básica aplicada [2].
* **Ventaja Competitiva:** Su profunda comprensión previa de los procesos físicos en planta, los tiempos de ciclo de maquinaria y la necesidad crítica de que el software en producción posea una robustez estructural excepcional, le otorgan una ventaja significativa para asimilar el diseño de arquitecturas de software orientadas a entornos reales de automatización [26].
* **Disponibilidad para el Curso:**
  * **Entre semana:** Aproximadamente 2 horas diarias de dedicación [3].
  * **Fines de semana:** Entre 4 y 5 horas diarias de dedicación [3].

---

## 3. PILA TECNOLÓGICA DEL ROADMAP [2]

El plan de estudios abarca un abanico completo de tecnologías modernas indispensables para el Ingeniero de Sistemas Inteligentes Industriales [1]:

* **Lenguaje Principal:** Python 3 [2, 23], incluyendo el uso de `dataclasses` estándar para contratos de transporte tipados entre capas [31, 32].
* **Entorno de Ejecución del Laboratorio:** Entorno virtual `.venv` recreado con Python 3.14.7, NumPy 2.5.2 y OpenCV-Python 5.0.0; la aplicación se lanza desde la raíz del repositorio con `.venv/bin/python -m apps.camera_info` [32].
* **Sistema de Desarrollo:** Linux clásico con la distribución Arch-Linux (CachyOS) bajo el entorno gráfico KDE, empleando nativamente Visual Studio Code como entorno de desarrollo unificado [3, 23].
* **Control de Versiones:** Git y la plataforma GitHub [2].
* **Visión Artificial y Procesamiento Digital:** OpenCV (`cv2`) y manipulación avanzada de matrices con NumPy [2, 23].
* **Modelado y Aprendizaje Profundo (IA):** PyTorch, la familia de modelos YOLO (para tareas de clasificación, detección de objetos y segmentación) [2, 17, 18].
* **Backend y APIs:** FastAPI (para servicios asíncronos), bases de datos relacionales PostgreSQL y bases de datos en memoria Redis [2, 18].
* **Optimización y Despliegue en Edge AI:** ONNX, TensorRT y despliegue físico en ordenadores embebidos industriales NVIDIA Jetson [2, 18].
* **Comunicaciones de Planta:** Protocolos de mensajería ligera MQTT, estándares OPC-UA para interconexión robusta con PLCs y protocolo clásico Modbus [2, 19].
* **Inteligencia Artificial Local y Modelos de Lenguaje:** Ollama para la ejecución de LLMs locales y arquitecturas de Generación Aumentada por Recuperación (RAG) multimediales [2, 19, 20].
* **Contenedores y Escala:** Docker y Docker Compose para modularización y empaquetamiento distribuido de los servicios de visión [2, 20].

---

## 4. ARQUITECTURA DETALLADA DEL PROYECTO "INDUSTRIAL-VISION-LAB" [6, 22]

El proyecto de desarrollo práctico **`industrial-vision-lab`** está diseñado bajo una arquitectura modular y orientada a objetos [22]. Se compone de capas de servicios independientes y reutilizables que desacoplan las tareas de entrada de datos, el almacenamiento físico y la interfaz gráfica de usuario [24, 25]:

### Estructura de Directorios del Repositorio [6]:
```
industrial-vision-lab/
├── apps/
│   ├── test_camera.py
│   └── camera_info.py
├── services/
│   ├── camera_service.py (y archivos del paquete de servicios)
│   ├── render_service.py
│   └── __init__.py
├── datasets/
├── models/
├── docs/
├── experiments/
├── scripts/
├── README.md
├── .gitignore
└── .venv/
```

### Descripción de los Componentes y Servicios [24, 25, 32]:

1. **`CameraService` (`services/camera_service.py`):**
   Encapsula por completo el ciclo de vida de adquisición del hardware de cámara a través de `cv2.VideoCapture` [24]. Contiene un robusto mecanismo de tolerancia a fallos que, si falla el puerto físico principal asignado a la cámara, escanea de forma cíclica los índices de puerto del sistema (del 0 al 4) para intentar reconectar automáticamente el dispositivo [24, 32]. En caso de una caída total irreversible de conexión, levanta una excepción personalizada de bajo nivel denominada `CameraConnectionError` [24].
   Asimismo, expone métodos utilitarios de manipulación de imagen y extracción de metadatos [24, 32]:
   * `roi_matrix`: Cálculo y obtención de la matriz correspondiente a la región recortada en planta [32].
   * `roi_to_gray`: Conversión espacial del frame a escala de grises [24, 32].
   * `noise_filter`: Reducción del ruido de alta frecuencia mediante la aplicación de un filtro de mediana [24, 32].
   * `threshold_roi` y `adaptive_threshold_roi`: Procesos de umbralización fija y binarización adaptativa gaussiana [24, 32].
   * `morph_clean`: Operaciones morfológicas de Apertura y Cierre (Opening y Closing) para la eliminación de imperfecciones o píxeles parásitos [24, 32].
   * `detect_edges`: Detección clásica de bordes mediante algoritmo de Canny [24, 32].
   * `find_and_filter_contours`: Búsqueda de contornos cerrados y filtrado selectivo según su área superficial en píxeles [24, 32].
   * `bounding_box` y `area_of_contour`: Extracción geométrica de las cajas envolventes y superficies dimensionales del objeto detectado [32].
   * `show_roi` y `release`: Métodos originales para habilitar ventanas de depuración rápidas y liberación segura de los recursos del sensor físico [32]. *Nota de aplicación:* con la regla de oro de renderizado, las ventanas de depuración dejaron de usarse en el flujo de producción, concentrándose la visualización en un único `cv2.imshow` al final del ciclo [32].

2. **`StorageService` (`services/storage_service.py`):**
   Gestiona de manera centralizada toda la persistencia de datos en disco duro local de la estación de trabajo, impidiendo que los scripts lógicos manejen rutas directamente [25].
   * `prepare_storage`: Garantiza la existencia del directorio de persistencia mediante `os.makedirs(..., exist_ok=True)` [32]. Es una inicialización explícita que el orquestador invoca una sola vez en el bloque de arranque, fuera del bucle de frames [32].
   * `save_frame`: Realiza el volcado físico de las capturas en formato de imagen comprimido JPG dentro de la carpeta local de datasets [25, 32]. Construye la ruta con `os.path.join` y comprueba el valor de retorno booleano de `cv2.imwrite`, registrando un `logger.error` si la escritura falla [32].
   * `registrar_metricas`: Escritura síncrona de datos de control de producción en el reporte histórico `reporte_produccion.csv` [25, 32]. Recibe exclusivamente tipos primitivos (`str`, `int`, `float | None`) y delega la serialización en `csv.writer` con `newline=""` y `encoding="utf-8"`, evitando construir las líneas a mano [32]. Los valores `None` se escriben como campo vacío y la cabecera solo se escribe si el archivo no existe [32].
   * `save_log`: Método reservado y diseñado para la persistencia centralizada de logs adicionales de ejecución del sistema [32]. Su implementación sigue pendiente, con un debate abierto sobre el posible solapamiento con `logging`/`FileHandler` [32].

3. **`InspectionService` (`services/inspection.py`):**
   Contiene las reglas de análisis de control de calidad sobre las piezas detectadas [32]. Expone el método `calculate_aspect_ratio` que obtiene las proporciones del bounding box de un contorno, y el método `is_valid_shape` que califica si la geometría del objeto se encuentra dentro de las tolerancias válidas definidas para la pieza de fabricación [32].

4. **`TrackingService` (`services/tracking.py`):**
   Implementa un algoritmo de seguimiento de centroides de piezas combinando su máquina de estados lógica [30, 32]. Su función principal consiste en registrar de forma única cada pieza que cruce una línea virtual de activación definida espacialmente dentro del frame, acumulando el contador histórico general sin incurrir en duplicaciones de contaje de una misma pieza a lo largo de múltiples frames continuos [30, 32].

5. **`RenderService` (`services/render_service.py`):**
   Encapsula toda la lógica de dibujado HMI, separando el cálculo del estado de las piezas de su representación visual [31, 32]. Define el dataclass `RenderablePiece` (`contour: np.ndarray`, `is_ok: bool`) como contrato de transporte entre el orquestador y la capa de pintado [31, 32].
   * `draw_roi`: Dibuja el recuadro de la Región de Interés sobre el frame completo [31, 32].
   * `draw_hud`: Superpone los contadores de piezas OK/NOK, el umbral de área y los objetos rastreados, apoyándose en el helper privado `_text_overlay` [31, 32].
   * `trace_objects`: Recorre la lista de `RenderablePiece`, elige el color según `is_ok` y dibuja contorno, bounding box y etiqueta semántica [31, 32].
   * `draw_line`: Traza la línea virtual de activación del tracking [31, 32].
   La paleta (colores y grosor de trazo) es configurable por constructor con valores por defecto, y el `__init__` no realiza I/O, no abre ventanas ni ejecuta bucles (constructor limpio) [31, 32]. El renderer no conoce la ROI (Opción A): recibe coordenadas globales del frame y el offset ROI→frame se aplica en el orquestador [31, 32].

6. **`apps/camera_info.py` (Script de Aplicación Principal):**
   Constituye el núcleo lógico de ejecución cíclica continua (`while True`) del sistema de visión artificial [25, 32]. Es la capa de coordinación encargada de instanciar y conectar de manera síncrona las capas de servicios independientes (`CameraService`, `StorageService`, `InspectionService`, `TrackingService` y `RenderService`) [25, 32]. En su bloque de arranque invoca una sola vez `storage.prepare_storage()`, garantizando el directorio de datos antes de entrar en el bucle [32]. Se encarga de procesar las matrices en memoria, calcular el estado semántico de cada pieza (centroide, área, aspect ratio, `is_ok`), actualizar los contadores y construir la lista de `RenderablePiece`; ya no decide colores ni textos [31, 32]. El dibujado se delega íntegramente en `RenderService`, quedando en el orquestador un único `cv2.imshow` al final del ciclo [31, 32]. Asimismo, monitoriza el tiempo del sistema para coordinar la frecuencia de persistencia de métricas [25, 32].

7. **`apps/test_camera.py` (Script de Verificación Rápida):**
   Un script mínimo de comprobación cuya única tarea es abrir una conexión directa con el índice de cámara especificado, desplegar el vídeo nativo en crudo en una ventana flotante básica y controlar la salida limpia del hilo tras la lectura del teclado con la tecla 'Q' [7, 32].

---

## 5. REGLAS INDUSTRIALES DE DISEÑO Y PARÁMETROS DEL SISTEMA

El desarrollo del software se rige bajo estrictos principios físicos y metodologías de programación característicos del control de procesos automatizados de planta [22, 26]:

* **Tolerancia del Aspect Ratio:** El sistema de inspección de forma discrimina piezas defectuosas o aplastadas evaluando la Relación de Aspecto (Aspect Ratio, $w/h$) del objeto detectado [30]. Se establece un rango de tolerancia industrial estricto de **0.8 a 1.2** [30]. Si la relación geométrica escapa de estos límites, el objeto es automáticamente calificado como pieza defectuosa (NOK) [30].
* **Ciclo de Persistencia de Producción:** El script de aplicación principal monitoriza los ciclos y vuelca los datos al histórico de producción síncrona en CSV exactamente **cada 30 frames** [25, 32]. Esto previene sobrecargar de peticiones de Entrada/Salida síncronas al procesador y disco en cada iteración individual de imagen, optimizando el rendimiento de la CPU del sistema [25].
* **Regla de Oro de Renderizado Industrial:** Primero se ejecutan todas las operaciones matemáticas y de lógica de negocio sobre las matrices de NumPy en memoria y, posteriormente, se dibujan todas las anotaciones HMI, rectángulos de ROI, bounding boxes de piezas y textos informativos en el búfer local [25, 27]. Solo al concluir todas las operaciones del frame, se llama una única vez en el ciclo al método `cv2.imshow` para renderizar visualmente el resultado, eliminando por completo cualquier tipo de latencia visual o "pintado fantasma" parpadeante [25, 27].
* **Nota de aplicación:** Esta regla se materializó reduciendo tres ventanas `cv2.imshow` simultáneas (`ROI Edge Detection`, `ROI` y `Camera Info`) a un único `cv2.imshow("Camera Info", frame)` al final del ciclo, y trasladando el dibujado de la matriz ROI al frame completo mediante el offset (roi_x, roi_y) [32]. Posteriormente, todo el dibujado se extrajo a `RenderService`, de modo que el orquestador solo invoca al renderer y conserva un único `cv2.imshow` [31, 32].
* **Regla del Constructor de Clase:** El método constructor (`__init__`) de un servicio o componente debe limitarse estrictamente a tareas de inicialización de atributos de memoria, parametrización inicial de clases y almacenamiento de objetos de configuración [10]. Bajo ningún concepto un constructor debe abrir interfaces gráficas, iniciar flujos de adquisición continuos o invocar bucles de control infinitos `while True`, ya que esto viola el aislamiento de instanciación e impide probar o instanciar el servicio con seguridad [10].
* **Regla de Preparación Explícita del Almacenamiento:** La existencia del directorio de datos se garantiza con una inicialización explícita (`StorageService.prepare_storage()` con `os.makedirs(..., exist_ok=True)`) ejecutada una sola vez en el bloque de arranque, nunca dentro del `while` de captura [32]. La preparación se mantiene como método del servicio responsable de la persistencia, sin crear clases auxiliares innecesarias (evitar la sobre-descomposición) [32].
* **Regla de Geometría Derivada de la Configuración:** Las anotaciones HMI deben derivarse de la geometría configurada (por ejemplo, `roi_x` y `roi_x + 300` para la línea de tracking) en lugar de usar coordenadas cableadas, de modo que un cambio de ROI no deje elementos desalineados [32].
* **Regla de Comprobación de Retornos de E/S:** Toda operación de escritura en disco debe verificar su resultado (`cv2.imwrite` devuelve un booleano) y registrar el fallo con `logger.error`; un fallo silencioso de persistencia es inaceptable en producción [32].

---

## 6. PROBLEMAS TÉCNICOS DETECTADOS Y SOLUCIONES DE ARQUITECTURA [7, 8, 9]

Durante el desarrollo del laboratorio de software `industrial-vision-lab`, se presentaron diversos errores que sirvieron como importantes hitos de aprendizaje en la estructuración de proyectos de Python [6, 7]:

### A) VSCode no detectaba la instalación de la biblioteca OpenCV
* **Causa:** El editor VS Code estaba haciendo uso del intérprete global de Python del sistema operativo en lugar de apuntar de forma explícita al intérprete del entorno virtual local (`.venv`) donde OpenCV había sido compilado e instalado [7].
* **Solución:** Seleccionar de manera manual el intérprete de Python correspondiente al directorio `.venv` local en la barra de configuración e intérpretes del editor VS Code [7].

### B) Error al realizar confirmaciones de versión con Git ("cannot run vi")
* **Causa:** Git intentaba invocar de manera predeterminada el editor de línea de comandos clásico `vi` en la terminal para que el usuario redactara de forma asíncrona el mensaje correspondiente al commit [8]. Debido a configuraciones de terminal o entorno, el ejecutable no respondía [8].
* **Solución:** Reconfigurar el editor de texto global de Git para redirigirlo directamente hacia VS Code, utilizando el comando global: `git config --global core.editor "code --wait"` [8]. Esto provoca que se abra una pestaña dedicada en el editor y Git permanezca en espera síncrona hasta que la pestaña del mensaje sea cerrada [8].

### C) Excepción "ModuleNotFoundError: No module named 'services'"
* **Causa:** El script se ejecutaba mediante el comando directo de consola `python apps/camera_info.py` estando posicionados dentro de la raíz del proyecto [8, 9]. Python tomaba automáticamente la carpeta `apps/` como el directorio raíz de búsqueda del sistema (el primer elemento en `sys.path`), lo que le impedía localizar e importar el paquete de software de `services/` ubicado en el nivel superior del proyecto [9].
* **Solución:** Asegurar la correcta resolución mediante la colocación de archivos de inicialización vacíos `__init__.py` tanto en el directorio `apps/` como en el de `services/` [9]. Posteriormente, ejecutar la aplicación principal desde el directorio raíz del repositorio empleando la llamada estructurada como módulo: `python -m apps.camera_info` [9].

### D) Múltiples ventanas de renderizado simultáneas (violación de la regla de oro)
* **Causa:** La aplicación desplegaba simultáneamente tres ventanas `cv2.imshow` activas —`ROI Edge Detection`, `ROI` (vía `show_roi`) y `Camera Info`—, violando la regla de oro de renderizado y generando latencia y ventanas de depuración innecesarias en el flujo de producción [32].
* **Solución:** Eliminar las ventanas de depuración y concentrar el renderizado en un único `cv2.imshow("Camera Info", frame)` al final del ciclo, trasladando el dibujado de la matriz ROI recortada al frame completo mediante el offset (roi_x, roi_y) con broadcasting de NumPy [32].

### E) Lógica de dibujado acoplada al orquestador
* **Causa:** El bucle principal mezclaba cálculo de negocio con decisiones de presentación: elegía colores, componía textos y ejecutaba llamadas directas a `cv2.rectangle`, `cv2.putText`, `cv2.drawContours` y `cv2.line` [31, 32]. Esto dificultaba el testing, la reutilización de la HMI y una futura separación en hilos de captura y renderizado [31, 32].
* **Solución:** Extraer todo el pintado a `RenderService`, con `RenderablePiece` como contrato de datos (`contour`, `is_ok`) y una paleta configurable por constructor [31, 32]. El orquestador pasa a calcular únicamente estado semántico y geometría, aplica el offset ROI→frame y delega el dibujado; el renderer desconoce la ROI (Opción A) y el único `cv2.imshow` permanece al final del ciclo [31, 32].

### F) Persistencia frágil: serialización manual, directorio no garantizado y fallo silencioso de escritura
* **Causa:** `registrar_metricas` recibía texto ya formateado y construía las líneas del CSV a mano; el directorio `datasets/` se creaba externamente con `mkdir -p datasets`; y `save_frame` no comprobaba el booleano devuelto por `cv2.imwrite`, por lo que un fallo de disco pasaba inadvertido [32].
* **Solución:** `registrar_metricas` acepta solo primitivos (`str`/`int`/`float | None`) y serializa con `csv.writer` (`newline=""`, `encoding="utf-8"`), escribiendo `None` como campo vacío y la cabecera solo si el archivo no existe; `prepare_storage()` garantiza el directorio con `os.makedirs(..., exist_ok=True)` y se invoca una vez en el arranque, fuera del `while`; `save_frame` usa `os.path.join` y registra con `logger.error` el fallo de `cv2.imwrite` [32].

### G) Código muerto y constantes mágicas en la HMI
* **Causa:** Tras el desacoplamiento del punto 6.3 quedaron variables calculadas y no usadas (`text_cnt_*`, `ar = None`, `threshold_roi`), líneas comentadas y coordenadas cableadas 200/500 en `draw_line`, lo que rompía la coherencia con la geometría configurada de la ROI [32].
* **Solución:** Eliminar el código muerto y derivar la línea virtual de tracking de `roi_x` y `roi_x + 300` [32]. La preparación del directorio se resolvió como método `prepare_storage()` del propio `StorageService`, descartando la clase auxiliar `PrepareStorage` para no sobre-descomponer la arquitectura [32].
