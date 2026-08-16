from services import CameraService, StorageService, CameraConectionError, InspectionService, TrackingService
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
    roi_x = 200
    roi_y = 100
    ar = None

    piezas_ok_en_frame = 0
    piezas_nok_en_frame = 0
    total_tracking_count = 0
    text_cnt_ok = f"Piezas OK: {piezas_ok_en_frame}"
    text_cnt_nok = f"Piezas NOK: {piezas_nok_en_frame}"
    text_cnt_tracking = f"Objetos Rastreados: {total_tracking_count}"
    
    try:
        # Los servicios siempre se instancian fuera del loop principal para evitar problemas de rendimiento  
        servicio = CameraService()
        storage = StorageService(f"datasets/")
        inspection = InspectionService() # defect InspectionService(0.8,1.2)
        tracking = TrackingService(line_y=225) # defect TrackingService(max_distance=50, max_disappeared=5)
        cv2.namedWindow("Camera Info")
        cv2.createTrackbar("Umbral Area", "Camera Info", 5000, 10000, servicio.callback_function) 

    except CameraConectionError as exc:
        logging.error(f"Error de conexión de la cámara: {exc}")
        raise SystemExit(1)

    while True:
        ret, frame = servicio.capturar_frame()
        if not ret:
            print("Error: no se pudo leer el frame")
            break
        
        # Reset de contadores de piezas por frame
        piezas_ok_en_frame = 0
        piezas_nok_en_frame = 0
        centroid_list = []
        

        ar_in_frame = []
        mean_ar = None
        worst_ar = None

        # 1. Extraemos la ROI usando el nuevo método limpio (sin pasarle el frame)
        roi = servicio.roi_matrix(roi_x, roi_y, roi_x + 300, roi_y + 250)

        # 2. Dibujamos el rectángulo en el frame original para el operario
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + 300, roi_y + 250), (255, 0, 0), 2) # type: ignore

        # 3. Obtenemos el valor del umbral de área desde el trackbar
        umbral_area = cv2.getTrackbarPos("Umbral Area", "Camera Info") # type: ignore type-> int
        area_text = f"Umbral Area: {umbral_area}"
        cv2.putText(frame, area_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA) # type: ignore

        if roi is not None:
            # Pasamos la ROI a escala de grises
            grey_roi = servicio.roi_to_gray(roi)

            # Noise filter
            filtered_roi = servicio.noise_filter(grey_roi)

            # Threshold
            threshold_roi = servicio.threshold_roi(filtered_roi)

            # Adaptive threshold
            adaptative_roi = servicio.adaptive_threshold_roi(filtered_roi)

            # Morph clean
            morph_cleaned = servicio.morph_clean(adaptative_roi)

            # Edge detection
            edges = servicio.detect_edges(morph_cleaned)
            cv2.imshow("ROI Edge Detection", edges) # type: ignore

            # Buscamos los contornos válidos dentro de la ROI
            valid_contours = servicio.find_and_filter_contours(edges, min_area=400)
            
            if len(valid_contours) > 0:
                cv2.drawContours(roi, valid_contours, -1, (0, 255, 0), 2)

                # Cálculo del bounding box de cada contorno válido y dibujamos un rectángulo alrededor de cada uno
                for contour in valid_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    M = cv2.moments(contour)
                    if M["m00"] != 0:
                        cx = int(M["m10"] / M["m00"])
                        cy = int(M["m01"] / M["m00"])
                        global_cx = roi_x + cx
                        global_cy = roi_y + cy
                        centroid_list.append((global_cx, global_cy))
                    
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    
                    # Cálculo del área de cada contorno válido
                    area = cv2.contourArea(contour)

                    ar = inspection.calculate_aspect_ratio(contour)
                    if ar is not None:
                        ar_in_frame.append(ar)

                        # LÓGICA WORST CASE: El que tenga mayor desviación absoluta respecto a 1.0
                        if abs(ar - 1.0) > abs(worst_ar - 1.0 if worst_ar is not None else 0):
                            worst_ar = ar

                    is_valid_ar = inspection.is_valid_shape(ar)

                    if area < umbral_area or not is_valid_ar:
                        text_color = (0, 0, 255)  # Rojo para áreas pequeñas o deformadas
                        text_warning = "ALERTA: Objeto NOK"
                        piezas_nok_en_frame += 1
                    else:
                        text_color = (0, 255, 0)  # Verde para piezas correctas
                        text_warning = "Objeto OK"
                        piezas_ok_en_frame += 1 
                        
                    
                    cv2.putText(roi, 
                                text_warning, 
                                (x, y-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, 
                                text_color, 
                                1)
                
                servicio.show_roi(roi) 
            total_tracking_count = tracking.update(centroid_list)

        # Actualizamos las cadenas de texto con los totales reales del frame procesado
        text_cnt_ok = f"Piezas OK: {piezas_ok_en_frame}"
        text_cnt_nok = f"Piezas NOK: {piezas_nok_en_frame}"
        text_cnt_tracking = f"Objetos Rastreados: {total_tracking_count}"
        # Pintamos los textos siempre actualizados en el panel principal
        cv2.putText(frame, text_cnt_nok, (10, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2, cv2.LINE_AA) # type: ignore
        cv2.putText(frame, text_cnt_ok, (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2, cv2.LINE_AA) # type: ignore
        cv2.putText(frame, text_cnt_tracking, (10, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2, cv2.LINE_AA) # type: ignore
        cv2.line(frame, (200, tracking.line_y), (500, tracking.line_y), (255, 255, 0), 2) # type: ignore
        # 5. Mostramos las ventanas
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

    servicio.release()