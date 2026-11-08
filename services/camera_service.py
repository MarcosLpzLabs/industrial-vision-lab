import cv2
import logging
import numpy
import queue, threading, time
# inicializar el logger específico para este archivo
logger = logging.getLogger(__name__)


class CameraConectionError(Exception):
    """Excepción personalizada para errores de conexión de la cámara."""
    pass
class CameraService:
    def __init__(self, camera=0, max_index=4):
        super().__init__()
        self.camera = None 
        self.camera_index = camera
        self.buffer = queue.Queue(maxsize=1)  # Buffer para almacenar frames
        self._stop = threading.Event()  # Evento para detener el hilo de captura
        self._thread = None  # Hilo de captura
        self.max_index = max_index
        self.dropped_frames = 0  # Contador de frames descartados

    def start_capture(self):
        #comprobamos si la cámara está abierta, si no lo está, intentamos abrirla
        if self.camera is not None and self.camera.isOpened():
            logger.warning("La cámara ya está abierta")
            return

        self.camera = cv2.VideoCapture(self.camera_index)

        if not self.camera.isOpened():
            self.camera.release()
            for idx in range(0, self.max_index + 1):
                if idx == self.camera_index:
                    continue
                self.camera = cv2.VideoCapture(idx)
                if self.camera.isOpened():
                    self.camera_index = idx
                    logger.info(f"Cámara abierta en índice {idx}")
                    break
        

        if not self.camera.isOpened() :
            raise CameraConectionError(f"No se puede abrir ninguna cámara. Intentados índices 0-{self.max_index}")

        self._stop.clear()  # Aseguramos que el evento de parada esté limpio
        target = self._capture_loop
        self._thread = threading.Thread(target=target, daemon=True)
        self._thread.start()

    def _capture_loop(self):
        while not self._stop.is_set(): #mientras el evento de parada no esté activado
            ret, frame = self._capturar_frame() #leer la cámara
            if not ret:
                logger.error("Error: no se pudo leer el frame en el bucle de captura")
                break
            try:
                self.buffer.put_nowait(frame)  # Intentamos poner el frame en el buffer
            except queue.Full:
                try:
                    self.buffer.get_nowait()  # Sacamos el frame más viejo para hacer espacio
                    self.dropped_frames += 1  # Incrementamos el contador de frames descartados
                    self.buffer.put_nowait(frame)  # Intentamos poner el frame de nuevo
                except queue.Empty:
                    self.buffer.put_nowait(frame)  # Si no hay nada, lo ponemos de nuevo


    def _capturar_frame(self):
        if not self.camera.isOpened():
            logger.error(f"Error: no se puede abrir la cámara en el índice {self.camera_index}")
            return False, None
        ret, frame = self.camera.read()

        if not ret:
            logger.error("Error: no se pudo leer el frame")
            return False, None
        return ret, frame
    

    def latest_frame(self,timeout=0.1):
        try:
            frame = self.buffer.get(timeout=timeout)  # Intentamos obtener el frame más reciente
            return frame
        except queue.Empty:
            #no hacemos logger, con un timeout de 0.1s serían demasiados registros
            return None
            
    def roi_matrix(self,frame, x_inicio, y_inicio, x_fin, y_fin):
        if not isinstance(frame, numpy.ndarray):
            logger.warning("No hay un frame válido disponible para recortar la ROI.")
            return None

        # Asegurarse de que las coordenadas estén dentro de los límites del frame
        x = max(0, min(x_inicio, frame.shape[1] - 1))
        y = max(0, min(y_inicio, frame.shape[0] - 1))
        width = max(1, min(x_fin - x, frame.shape[1] - x))
        height = max(1, min(y_fin - y, frame.shape[0] - y))

        roi = frame[y:y + height, x:x + width]
        return roi
    
    def show_roi(self, roi):
        # Este método ahora solo tiene UNA responsabilidad: mostrar lo que le mandes
        if roi is not None:
            cv2.imshow("ROI", roi)
    def roi_to_gray(self, roi):
        """Convierte la ROI a escala de grises UNA sola vez."""
        if roi is not None:
            return cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        return None

    def noise_filter(self, grey_roi):
        """Aplica filtros de suavizado para eliminar el ruido electrónico de la ROI."""
        if grey_roi is not None:
            # Aplicar un filtro de mediana para reducir el ruido
            filtered_roi = cv2.medianBlur(grey_roi, 5)
            #cv2.imshow("ROI Noise Filtered", filtered_roi)
            return filtered_roi
        return None

    def threshold_roi(self, grey_roi):
        if grey_roi is not None:
            _, thresh_roi = cv2.threshold(grey_roi, 127, 255, cv2.THRESH_BINARY)
            #cv2.imshow("ROI Threshold", thresh_roi)
            return thresh_roi
        return None

    def adaptive_threshold_roi(self, grey_roi):
        if grey_roi is not None:
            adaptative_roi = cv2.adaptiveThreshold(grey_roi, 255, 
                                                cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                                cv2.THRESH_BINARY, 
                                                11, # Tamaño del bloque de píxeles vecinos para calcular la media
                                                2 # Constante que se resta a la media
                                                )
            #cv2.imshow("ROI Adaptative Threshold", adaptative_roi)
            return adaptative_roi
        return None
    

    def morph_clean(self, binary_roi):
        if binary_roi is not None:
            # 1. Definimos un kernel rectangular de 3x3 (nuestro margen de vecindad)
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
            
            # 2. Aplicamos un 'Opening' para eliminar cualquier mota de ruido residual exterior
            cleaned = cv2.morphologyEx(binary_roi, cv2.MORPH_OPEN, kernel)
            
            # 3. Aplicamos un 'Closing' por si han quedado poros abiertos dentro del objeto
            cleaned = cv2.morphologyEx(cleaned, cv2.MORPH_CLOSE, kernel)
            return cleaned
        return None
    
    def detect_edges(self,image):
        """Detecta los contornos de la pieza usando el algoritmo de Canny."""
        if image is not None:
            # cv2.Canny(imagen, umbral_bajo, umbral_alto)
            # Como nuestra imagen ya es binaria (0 o 255), los umbrales pueden ser drásticos
            edges = cv2.Canny(image, 50, 150)
            #cv2.imshow("ROI Edges (Canny)", edges)
            return edges
        return None



    def find_and_filter_contours(self, edges_image, min_area=500, max_area=50000):
        """Encuentra los contornos en la imagen de bordes y los filtra por tamaño."""
        if edges_image is not None:
            # cv2.findContours necesita: imagen, modo de recuperación, método de aproximación
            # RETR_EXTERNAL solo busca los contornos exteriores (ignora agujeros internos por ahora)
            # CHAIN_APPROX_SIMPLE comprime las líneas rectas para ahorrar memoria
            contours, _ = cv2.findContours(edges_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            valid_contours = []
            for cnt in contours:
                area = cv2.contourArea(cnt)
                # Filtramos por umbral de área para evitar falsos positivos (ruido residual)
                if min_area <= area <= max_area:
                    valid_contours.append(cnt)
            
            return valid_contours
        return []

    def bounding_box(self, contour):
        """Calcula el rectángulo delimitador de un contorno dado."""
        if contour is not None:
            x, y, w, h = cv2.boundingRect(contour)
            return (x, y, w, h)
        return None
    
    def area_of_contour(self, contour):
        """Calcula el área de un contorno dado."""
        if contour is not None:
            return cv2.contourArea(contour)
        return 0

    def release(self):
        self.camera.release()   
        cv2.destroyAllWindows()

    def callback_function(self, frame):
        pass #void function, can be implemented later if needed

