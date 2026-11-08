import cv2
import logging
from dataclasses import dataclass
import numpy as np

# inicializar el logger específico para este archivo
logger = logging.getLogger(__name__)

@dataclass
class RenderablePiece:
    contour: np.ndarray
    is_ok: bool

class RenderService:
    def __init__(self, grosor_trazo=2, color_roi=(255, 0, 0), color_ok=(0, 255, 0), color_nok=(0, 0, 255)
                , color_tracking=(255, 255, 0), color_umbral = (255,0,255), color_line=(0, 255, 255)):
        self.color_roi = color_roi
        self.grosor_trazo = grosor_trazo
        self.color_ok = color_ok
        self.color_nok = color_nok
        self.color_tracking = color_tracking
        self.color_umbral = color_umbral
        self.color_line = color_line


    def draw_roi(self,frame, roi_x, roi_y, roi_w, roi_h):
        # Dibujamos el rectángulo en el frame original para el operario
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + roi_w, roi_y + roi_h), self.color_roi, self.grosor_trazo ) # type: ignore
        

    def draw_hud(self,frame,umbral,ok,nok,tracking):
        umbral_area_text = f"Umbral Area: {umbral}"
        self._text_overlay(frame, umbral_area_text, (10, 60), self.color_umbral)

        text_cnt_nok = f"Piezas NOK: {nok}"
        self._text_overlay(frame, text_cnt_nok, (10, 90), self.color_nok)

        text_cnt_ok = f"Piezas OK: {ok}"
        self._text_overlay(frame, text_cnt_ok, (10, 120), self.color_ok)
        
        text_cnt_tracking = f"Objetos Rastreados: {tracking}"
        self._text_overlay(frame, text_cnt_tracking, (10, 150), self.color_tracking)



    def _text_overlay(self,frame,text, position : tuple,color,font_scale=0.8, thickness=2):
        cv2.putText(frame, text, position, cv2.FONT_HERSHEY_SIMPLEX, font_scale, color, thickness, cv2.LINE_AA)

    def trace_objects(self,frame,pieces): #pieces --> Dataclass
        for piece in pieces:
            color = self.color_ok if piece.is_ok else self.color_nok
            cv2.drawContours(frame,[piece.contour], -1, color, self.grosor_trazo) # type: ignore

            x,y,w,h = cv2.boundingRect(piece.contour)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, self.grosor_trazo) # type: ignore
            
            self._text_overlay(frame, 
                            "Objeto Ok" if piece.is_ok else "ALERTA: Objeto NOK",
                            (x, y - 5),
                            color,
                            font_scale=0.5,
                            thickness=1)
            
    def draw_line(self, frame, pt1: tuple, pt2: tuple):
        cv2.line(frame, pt1, pt2, self.color_line, self.grosor_trazo)


