from services import CameraService, StorageService
import cv2
from datetime import datetime
if __name__ == "__main__":
    cnt = 30
    try:
        #los servicios siempre se instancian fuera del loop principal para evitar problemas de rendimiento  
        servicio = CameraService()
        storage = StorageService(f"datasets/")
    except RuntimeError as exc:
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
            storage.save_frame(f"frame_{sufix}.jpg", frame)
            print("Frame guardado en storage.")
            cnt = 30  # Reset the counter
        
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    servicio.release()
    

    





