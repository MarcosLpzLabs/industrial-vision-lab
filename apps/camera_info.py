from services import CameraService, StorageService, CameraConectionError
import cv2
from datetime import datetime
import logging



if __name__ == "__main__":

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(),                      # Para que se siga viendo en la terminal
            logging.FileHandler("datasets/app_vision.log") # ¡Para que se guarde en un archivo de texto!
        ]
    )
    cnt = 30
    try:
        #los servicios siempre se instancian fuera del loop principal para evitar problemas de rendimiento  
        servicio = CameraService()
        storage = StorageService(f"datasets/")


    except CameraConectionError as exc:
        logging.error(f"Error de conexión de la cámara: {exc}")
        raise SystemExit(1)

    #print(f"Cámara abierta en índice {servicio.camera_index}")
    while True:
        ret, frame = servicio.capturar_frame()
        if not ret:
            print("Error: no se pudo leer el frame")
            break
        # 1. Extraemos la ROI usando el nuevo método limpio (sin pasarle el frame)
        roi = servicio.roi_matrix(200, 100, 500, 350)

        # 2. Dibujamos el rectángulo en el frame original para el operario
        cv2.rectangle(frame, (200, 100), (500, 350), (255, 0, 0), 2) #type: ignore

        
        if roi is not None:
            servicio.show_roi(roi)
            #pasamos la ROI a escala de grises
            grey_roi = servicio.roi_to_gray(roi)
            #threshold
            servicio.threshold_roi(grey_roi)
            #adaptive threshold
            servicio.adaptive_threshold_roi(grey_roi)
        # 3. Mostramos las ventanas
        cv2.imshow("Camera Info", frame) # type: ignore

        cnt -= 1
        if cnt == 0:
            sufix = datetime.now().strftime("%Y%m%d_%H%M%S")
            print("Guardando frame en storage...")
            storage.save_frame(frame, f"frame_{sufix}.jpg")
            print("Frame guardado en storage.")
            cnt = 30  # Reset the counter
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    servicio.release()
    

    





