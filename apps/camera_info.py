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
        print(exc)
        raise SystemExit(1)

    #print(f"Cámara abierta en índice {servicio.camera_index}")
    while True:
        ret, frame = servicio.capturar_frame()
        if not ret:
            print("Error: no se pudo leer el frame")
            break

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
    

    





