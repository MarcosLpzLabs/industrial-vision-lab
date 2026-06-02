import cv2


def main() -> None:
    print("Versión de OpenCV",cv2.__version__)

    cap = cv2.VideoCapture(0)  # type: ignore[attr-defined]
    if not cap.isOpened():
        print("Error: no se puede abrir la cámara")
        return

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        fps_text = "no disponible"
    else:
        fps_text = fps

    print("Resolución: ", width, "x", height)
    print("FPS: ", fps_text)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: no se pudo leer el frame")
            break

        info_text = f"OpenCV {cv2.__version__} | {width}x{height} | FPS {fps_text}"
        cv2.putText(
            frame,
            info_text,
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2,
            cv2.LINE_AA,
        )

        cv2.imshow("Camera Info", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

