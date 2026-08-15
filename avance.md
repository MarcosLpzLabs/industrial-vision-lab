# INFORME DE AVANCE Y CONOCIMIENTOS ADQUIRIDOS — PROYECTO INDUSTRIAL-VISION-LAB [32]

Este documento detalla el estado actual de aprendizaje, los conocimientos dominados, las áreas de fricción técnica y el grado de madurez del proyecto práctico de software desarrollado en el curso de visión artificial industrial [22, 32].

---

## 1. CALIFICACIÓN DE HERRAMIENTAS DE DESARROLLO

Se limita la puntuación del 1 al 10 de forma estricta a las tres herramientas de desarrollo base utilizadas a lo largo de la formación [3, 4, 5]:

### Python: 7/10 [4]
* **Conocimientos demostrados:** Implementación de clases bien estructuradas, modularización básica de código, aislamiento mediante entornos virtuales (`.venv`), buenas prácticas de programación y uso fluido de bibliotecas clave como OpenCV y NumPy [4, 6]. Nociones básicas de arquitecturas de Deep Learning con PyTorch y YOLO [4].
* **Aspectos pendientes de maduración:** Arquitectura avanzada de software, diseño formal de APIs robustas, testing profesional (`pytest`, cobertura y simulación de hardware mediante mocks), tipado avanzado y modularización a nivel de paquete profesional [4, 15, 16].

### Linux (CachyOS/Arch): 6/10 [3]
* **Conocimientos demostrados:** Uso nativo de CachyOS como sistema operativo principal de desarrollo, uso habitual e interactivo de la terminal de comandos, conocimiento de operaciones básicas de la consola, y experiencia básica con SSH y contenedores Docker sencillos [3, 23].
* **Aspectos pendientes de maduración:** Configuración profunda de servicios mediante systemd, visualización avanzada de logs de sistema con journalctl, administración y diagnóstico de redes (networking) en entornos industriales, despliegue automatizado de software y uso avanzado de contenedores Docker en arquitecturas complejas [4, 14, 20].

### Git y GitHub: 5/10 [5]
* **Conocimientos demostrados:** Comprensión de la diferencia conceptual entre Git (local) y GitHub (remoto) [5]. Dominio de comandos de flujo de trabajo básicos: `git add`, `git commit` (con configuración de editor global `code --wait`), `git push`, creación de ramas (branches), merges de código e interpretación de los estados del proyecto [5, 8]. Entendimiento profundo del concepto de que Git no almacena meros archivos, sino estados completos del proyecto en un árbol de directorios [5].
* **Aspectos pendientes de maduración:** Gestión avanzada de resolución de conflictos, Pull Requests en equipos y adopción del flujo de trabajo estructurado Git Flow [14].
* *Nota histórica de evolución:* Se registra un crecimiento significativo en el dominio de la herramienta, partiendo de un nivel estimado inicial de **3/10** hasta el actual de **5/10** [5].

---

## 2. CONOCIMIENTOS ADQUIRIDOS Y PUNTOS FUERTES

La formación ha permitido asimilar prácticas y conceptos esenciales de ingeniería de software orientada a entornos industriales de producción real [22]:

* **Arquitectura Limpia y Principios SOLID:** Comprensión rigurosa de la separación de responsabilidades y el aislamiento de la lógica de hardware de adquisición en servicios independientes [26]. Esto asegura que las capas de persistencia o procesamiento no dependan de la inicialización directa del dispositivo [11].
* **Matemática y Manipulación de Matrices (NumPy):** Comprensión avanzada del tratamiento de imágenes como arrays multidimensionales (`numpy.ndarray`) [23, 27]. Esto incluye operaciones de recorte espacial (recorte de Regiones de Interés - ROI) y aplicación de funciones de clampado o restricciones de seguridad para evitar desbordamientos de memoria al trabajar en los límites de los frames [27].
* **Pipeline de Procesamiento Digital de Imágenes (PDI) Clásico:** Estructuración y secuenciación lógica de algoritmos clásicos de visión de computador para el filtrado de ruido electrónico, binarización adaptativa gaussiana, limpieza mediante morfología matemática (operaciones de Opening y Closing), y detección de características geométricas basadas en análisis de contornos y bounding boxes [24, 27].
* **Sincronización de Flujos de Vídeo:** Dominio del flujo secuencial de renderizado gráfico de la HMI [27]. Se sigue estrictamente la directriz industrial de procesar y pintar la información exclusivamente sobre matrices en la memoria del sistema para, una sola vez al final del ciclo de frame, refrescar la pantalla mediante el backend gráfico con un único `cv2.imshow`, eliminando cualquier parpadeo ("pintados fantasmas") o latencia de dibujado [25, 27].

---

## 3. PUNTOS DE FRICCIÓN HISTÓRICOS (EN PROCESO DE ASIMILACIÓN)

Durante las fases de desarrollo práctico, se han identificado ciertos patrones de programación clásica o de automatización (PLCs/VBA) que entran en conflicto con la arquitectura de software avanzada en Python [2, 22, 28]:

* **Ciclo de Vida de Elementos de la UI en OpenCV:** Tendencia inicial a instanciar y asociar controles interactivos (como barras de desplazamiento o Trackbars) a ventanas lógicas del sistema que la GPU aún no ha inicializado y reservado en la memoria de visualización [28]. Este problema de acoplamiento se corrigió estableciendo un flujo de inicialización estricto usando `cv2.namedWindow` antes del arranque del bucle continuo [28].
* **Jerarquía y Ámbito de Variables Cíclicas:** Dificultades para definir correctamente el ciclo de vida de las variables de estado en bucles de captura secuenciales infinitos `while True` [28]. Existía una inclinación a declarar contadores instantáneos (que deben reiniciarse a cero en cada iteración del frame) fuera del bucle de ejecución, o bien a condicionar lecturas a bloques de ejecución espaciados en el tiempo (como el ciclo de guardado de históricos CSV cada 30 frames), provocando acumulaciones infinitas de datos o métricas que aparecían congeladas en la HMI [28].
* **Pureza de Datos en Capas de Persistencia:** Tendencia inicial a transmitir cadenas de caracteres ya formateadas para la UI, o estructuras complejas completas (como matrices de imagen `numpy.ndarray`), hacia la capa de base de datos o almacenamiento persistente [29]. Se ha trabajado en interiorizar que las capas de persistencia deben recibir únicamente tipos de datos primitivos de Python (enteros, floats, etc.) extraídos de la lógica de negocio pura, manteniendo el backend de almacenamiento desacoplado de la interfaz de usuario [29].

---

## 4. ESTADO DE MADUREZ DEL PROYECTO PRÁCTICO

El proyecto de desarrollo práctico **`industrial-vision-lab`** simula una celda de inspección automatizada en planta [6, 22]. El estado actual de sus componentes es el siguiente:

### Grado de Avance de Módulos Prácticos
* **Módulo 5 (HMI, Métricas y Persistencia de Producción): COMPLETADO AL 100%** [29, 33]. El sistema es sumamente robusto en la captura y procesamiento clásica, calcula métricas instantáneas limpias en cada ciclo de frame y genera un volcado síncrono estructurado y libre de corrupciones en el fichero CSV local [29].
* **Módulo 6 (Especialización Avanzada - Filtro de Forma, Conteo Histórico y Refactorización): EN PROCESO** [29, 30]. Se han estructurado y desarrollado las clases teóricas de servicios adicionales para la detección geométrica avanzada (`InspectionService`) y el conteo acumulativo (`TrackingService`), encontrándose actualmente pendientes de ser totalmente integrados y refactorizados dentro del script principal de la aplicación [32].

### Funcionalidades Implementadas en el Código [32]
1. **Adquisición de Vídeo Robusta:** Implementación de un ciclo de rescate automático que escanea de forma iterativa los puertos del sistema (del índice 0 al 4) en caso de fallo físico de la cámara principal, levantando excepciones personalizadas (`CameraConnectionError`) ante pérdidas totales de enlace [24, 32].
2. **Medición de Rendimiento Técnico:** Extracción y cálculo preciso de los FPS de captura, versión del motor de visión OpenCV y resolución del sensor de adquisición, superponiendo estos metadatos técnicos de forma elegante sobre el vídeo en tiempo real [7, 32].
3. **Filtro Espacial y ROI:** Definición y recorte en memoria de una Región de Interés (ROI) fija sobre la matriz principal para aislar la zona útil de inspección de la celda en planta [23, 32].
4. **Pipeline Clásico de PDI (Procesamiento Digital de Imágenes):** Conversión espacial a escala de grises, filtrado de ruido electrónico de cámara mediante filtros de mediana, binarización mediante umbralización fija y adaptativa gaussiana, limpieza morfológica (mediante operaciones de apertura y cierre) y detección de contornos estructurados por área mínima [24, 27, 32].
5. **Dibuixos y Elementos HMI:** Superposición en pantalla del recuadro de la ROI útil de inspección, coloreado de contornos detectados con sus respectivos cuadros delimitadores (bounding boxes) y visualización de contadores de piezas y estados (OK/NOK) [32].
6. **Métricas Geométricas de Aspect Ratio:** Desarrollo de lógica de filtrado basada en la relación de aspecto del bounding box (ancho/alto) con un rango de tolerancia industrial definido entre 0.8 y 1.2 para discriminar piezas deformadas [30, 32].
7. **Persistencia Síncrona Industrial:** Captura y guardado automático de volcados de frame en formato JPG dentro del directorio de base de datos (`datasets/`), y almacenamiento de métricas en el histórico `reporte_produccion.csv` con cabecera adaptativa automatizada [25, 32].
8. **Estructura del Paquete `services`:** Exportación unificada de servicios mediante el archivo `services/__init__.py`, empaquetando limpiamente `CameraService`, `StorageService`, `CameraConnectionError`, `InspectionService`, `TrackingService` y `TrackedObject` [32].

### Tareas de Refactorización y Mejoras Pendientes [32]
* **Integración del Servicio de Tracking:** Acoplar definitivamente `TrackingService` dentro del bucle de renderizado y control de `camera_info.py` para llevar a cabo el conteo de piezas histórico real mediante paso de centroides por una línea virtual de activación, eliminando la duplicación de contajes por frame [32].
* **Desacoplamiento Estricto de Binarización y Dibujado:** Migrar la lógica de procesamiento (binarización gaussiana y dibujo de textos de la interfaz) del script de aplicación `camera_info.py` hacia los servicios dedicados de procesamiento, preparando el backend de adquisición para futuros hilos de ejecución concurrentes (multihilo) [31, 32].
* **Pureza de Tipos de Persistencia:** Adecuar las firmas de llamada en `StorageService.registrar_metricas` para almacenar exclusivamente tipos primitivos puros de Python en lugar de strings ya formateados para la HMI [32].
* **Compleción del Almacenamiento Auxiliar:** Implementar la lógica del método `save_log` pendiente en el servicio de almacenamiento para el registro estructurado de eventos adicionales del sistema [32].
* **Control y Separación del Renderizado:** Estudiar alternativas para desacoplar por completo las responsabilidades de captura pura de frames de la capa de visualización interactiva y gestión de teclados de OpenCV (`cv2.waitKey`), garantizando la total separación de responsabilidades [32].
