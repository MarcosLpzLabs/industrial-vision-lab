import cv2
import logging
import numpy

# inicializar el logger específico para este archivo
logger = logging.getLogger(__name__)


class CameraConectionError(Exception):
    """Excepción personalizada para errores de conexión de la cámara."""
    pass
class CameraService:
    def __init__(self, camera=0, max_index=4):
        super().__init__()
        self.camera_index = camera
        self.camera = cv2.VideoCapture(camera)

        if not self.camera.isOpened():
            self.camera.release()
            for idx in range(0, max_index + 1):
                if idx == camera:
                    continue
                self.camera = cv2.VideoCapture(idx)
                if self.camera.isOpened():
                    self.camera_index = idx
                    logger.info(f"Cámara abierta en índice {idx}")
                    break
                self.camera.release()

        if not self.camera.isOpened():
            raise CameraConectionError(f"No se puede abrir ninguna cámara. Intentados índices 0-{max_index}")
            '''raise RuntimeError(
                f"No se puede abrir ninguna cámara. Intentados índices 0-{max_index}"
            )'''

        self.text_fps = ""
        self.ret = False
        self.frame = 0

    def mostrar_fps(self):
        self.fps = self.camera.get(cv2.CAP_PROP_FPS)
        if self.fps <= 0:
            self.text_fps = "no disponible"
        else:
            self.text_fps = self.fps
        print("FPS: ", self.text_fps)

    def capturar_frame(self):
        if not self.camera.isOpened():
            logging.error(f"Error: no se puede abrir la cámara en el índice {self.camera_index}")
            return False, None
        self.ret, self.frame = self.camera.read()

        #temporal
        #frame_hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        #print("Píxel (0,0) en HSV:", frame_hsv[0, 0])
        if not self.ret:
            logging.error("Error: no se pudo leer el frame")
            return False, None

        self.mostrar_fps()

        info_text = f"OpenCV {cv2.__version__} | FPS {self.text_fps}"
        cv2.putText(
            self.frame,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )
        return self.ret, self.frame
    
    
    def roi_matrix(self, x_inicio, y_inicio, x_fin, y_fin):
        # Usamos directamente self.frame, que ya es la matriz real leída por el servicio
        if not self.ret or not isinstance(self.frame, numpy.ndarray):
            logging.warning("No hay un frame válido disponible para recortar la ROI.")
            return None

        # Asegurarse de que las coordenadas estén dentro de los límites del frame
        x = max(0, min(x_inicio, self.frame.shape[1] - 1))
        y = max(0, min(y_inicio, self.frame.shape[0] - 1))
        width = max(1, min(x_fin - x, self.frame.shape[1] - x))
        height = max(1, min(y_fin - y, self.frame.shape[0] - y))

        roi = self.frame[y:y + height, x:x + width]
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
            
            #cv2.imshow("ROI Morph Cleaned", cleaned)
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

