import cv2
import logging



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
                    logging.info(f"Cámara abierta en índice {idx}")
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
    def release(self):
        self.camera.release()   
        cv2.destroyAllWindows()


