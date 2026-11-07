import cv2
import numpy as np
import logging

logger = logging.getLogger(__name__)


class InspectionService:
    def __init__(self, min_aspect_ratio: float = 0.8, max_aspect_ratio: float = 1.2):
        self.min_ar = min_aspect_ratio
        self.max_ar = max_aspect_ratio

    def calculate_aspect_ratio(self, contour: np.ndarray) -> float | None:
        """
        Calcula la relación de aspecto (w / h) de un contorno dado.
        Retorna float si el cálculo es exitoso, o None si la altura es cero.
        """
        x, y, w, h = cv2.boundingRect(contour)
        
        try:
            # Forzamos que la división mantenga consistencia de float
            return float(w / h)
        except ZeroDivisionError:
            logger.error("No se puede calcular el aspect ratio: la altura (h) del bounding box es 0.")
            return None

    def is_valid_shape(self, aspect_ratio: float | None) -> bool:
        """
        Determina si el aspect ratio calculado entra dentro del rango de tolerancia.
        Rechaza automáticamente valores nulos (None).
        """
        if aspect_ratio is None:
            return False
            
        return self.min_ar <= aspect_ratio <= self.max_ar