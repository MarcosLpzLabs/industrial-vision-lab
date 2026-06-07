from services import CameraService
import cv2
if __name__ == "__main__":
    try:
        servicio = CameraService()
    except RuntimeError as exc:
        print(exc)
        raise SystemExit(1)

    print(f"Cámara abierta en índice {servicio.camera_index}")
    while True:
        ret, frame = servicio.capturar_frame()
        if not ret:
            print("Error: no se pudo leer el frame")
            break
        else:
            cv2.imshow("Camera Info", frame) # type: ignore
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    servicio.release()
    

    





