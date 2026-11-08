from services import CameraService, StorageService, CameraConectionError, InspectionService, TrackingService, RenderService,RenderablePiece
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
            logging.FileHandler("datasets/app_vision.log") # Para que se guarde en un archivo de texto
        ]
    )
    cnt = 30
    roi_x = 200
    roi_y = 100

    piezas_ok_en_frame = 0
    piezas_nok_en_frame = 0
    total_tracking_count = 0
    intentos_fallados = 0
    
    try:
        # Los servicios siempre se instancian fuera del loop principal para evitar problemas de rendimiento  
        camera = CameraService()
        camera.start_capture()
        storage = StorageService(f"datasets/")
        storage.prepare_storage() # Preparamos el directorio de almacenamiento
        inspection = InspectionService() # defect InspectionService(0.8,1.2)
        tracking = TrackingService(line_y=225) # defect TrackingService(max_distance=50, max_disappeared=5)
        render = RenderService() #ahora mismo coge valores por defecto, pero se puede pasar parámetros para cambiar colores y grosor de trazo
        cv2.namedWindow("Camera Info")
        cv2.createTrackbar("Umbral Area", "Camera Info", 5000, 10000, camera.callback_function)

    except CameraConectionError as exc:
        logging.error(f"Error de conexión de la cámara: {exc}")
        raise SystemExit(1)

    while True:
        frame = camera.latest_frame(timeout=0.1)  # Intentamos obtener el frame más reciente con un timeout de 0.1s
        if frame is None:
            intentos_fallados += 1
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
            # si se supera umbral de 30 fallos (timeout de 0.1s cada uno) se cierra limpio
            if intentos_fallados >= 30:
                logging.error("Error: No se pudo obtener un frame de la cámara después de 30 intentos fallidos.")
                break
            continue  # Si no se obtiene un frame, continuamos con el siguiente ciclo del bucle sin procesar nada más
    
        intentos_fallados = 0  # Reset del contador de intentos fallidos si se obtiene un frame

        # Reset de contadores de piezas por frame
        piezas_ok_en_frame = 0
        piezas_nok_en_frame = 0
        centroid_list = []
        piezas = []
        

        ar_in_frame = []
        mean_ar = None
        worst_ar = None

        # 1. Extraemos la ROI usando el nuevo método limpio 
        roi = camera.roi_matrix(frame,roi_x, roi_y, roi_x + 300, roi_y + 250)

        # 2. Dibujamos el rectángulo en el frame original para el operario
        render.draw_roi(frame, roi_x, roi_y, 300, 250)

        # 3. Obtenemos el valor del umbral de área desde el trackbar
        umbral_area = cv2.getTrackbarPos("Umbral Area", "Camera Info") # type: ignore type-> int

        if roi is not None:
            # Pasamos la ROI a escala de grises
            grey_roi = camera.roi_to_gray(roi)

            # Noise filter
            filtered_roi = camera.noise_filter(grey_roi)

            # Adaptive threshold
            adaptative_roi = camera.adaptive_threshold_roi(filtered_roi)

            # Morph clean
            morph_cleaned = camera.morph_clean(adaptative_roi)

            # Edge detection
            edges = camera.detect_edges(morph_cleaned)

            # Buscamos los contornos válidos dentro de la ROI
            valid_contours = camera.find_and_filter_contours(edges, min_area=400)

            contorno_desplazado = [contorno + [roi_x, roi_y] for contorno in valid_contours]# Desplazamos el contorno a las coordenadas globales del frame
            
            if len(valid_contours) > 0:
                
                # "Evaluamos cada contorno: centroide, área, aspect ratio y estado OK/NOK
                for contorno in contorno_desplazado:
                    M = cv2.moments(contorno)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        centroid_list.append((cx, cy))
                    
                    # Cálculo del área de cada contorno válido
                    area = cv2.contourArea(contorno) # type: ignore

                    ar = inspection.calculate_aspect_ratio(contorno)
                    if ar is not None:
                        ar_in_frame.append(ar)

                        # LÓGICA WORST CASE: El que tenga mayor desviación absoluta respecto a 1.0
                        if abs(ar - 1.0) > abs(worst_ar - 1.0 if worst_ar is not None else 0):
                            worst_ar = ar

                    is_valid_ar = inspection.is_valid_shape(ar)

                    is_ok = (area >= umbral_area) and is_valid_ar
                    if is_ok:
                        piezas_ok_en_frame += 1
                    else:
                        piezas_nok_en_frame += 1
                        
                    piezas.append(RenderablePiece(contour=contorno, is_ok=is_ok))

                #pintamos los contornos y rectángulos de las piezas detectadas en el frame original
                render.trace_objects(frame, piezas)  # Llamamos al método trace_objects del camera de renderizado

            total_tracking_count = tracking.update(centroid_list)
        
        render.draw_hud(frame, umbral_area, piezas_ok_en_frame, piezas_nok_en_frame, total_tracking_count)

        render.draw_line(frame,(roi_x,tracking.line_y),(roi_x + 300,tracking.line_y))

        # 5. Mostramos la ventana
        cv2.imshow("Camera Info", frame) # type: ignore

        cnt -= 1

        # Si se detectaron piezas, calculamos el promedio matemático del frame
        if ar_in_frame:
            mean_ar = sum(ar_in_frame) / len(ar_in_frame)
        else:
            mean_ar = None  # No hay piezas, por lo que no hay promedio de relación de aspecto
            worst_ar = None  # No hay piezas, por lo que no hay peor relación de aspecto

        if cnt == 0:
            sufix = datetime.now().strftime("%Y%m%d_%H%M%S")
            print("Guardando frame en storage...")
            file_name = f"frame_{sufix}.jpg"
            storage.save_frame(frame, file_name)

            print("Guardando métricas...")
            storage.registrar_metricas(nombre_frame=file_name,
                                    umbral=umbral_area,
                                    ok=piezas_ok_en_frame,
                                    nok=piezas_nok_en_frame,
                                    aspect_ratio=round(mean_ar, 2) if mean_ar is not None else None,
                                    worst_ar=round(worst_ar, 2) if worst_ar is not None else None)

            print("Frame guardado en storage.")
            cnt = 30  # Reset the counter
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()