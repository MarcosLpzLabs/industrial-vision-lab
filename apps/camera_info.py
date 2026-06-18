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
    roi_x = 200
    roi_y = 100

    piezas_ok_en_frame = 0
    piezas_nok_en_frame = 0
    text_cnt_ok = f"Piezas OK: {piezas_ok_en_frame}"
    text_cnt_nok = f"Piezas NOK: {piezas_nok_en_frame}"
    
    try:
        #los servicios siempre se instancian fuera del loop principal para evitar problemas de rendimiento  
        servicio = CameraService()
        storage = StorageService(f"datasets/")
        cv2.namedWindow("Camera Info")
        cv2.createTrackbar("Umbral Area", "Camera Info", 5000,10000, servicio.callback_function) 


        


    except CameraConectionError as exc:
        logging.error(f"Error de conexión de la cámara: {exc}")
        raise SystemExit(1)

    #print(f"Cámara abierta en índice {servicio.camera_index}")
    while True:
        ret, frame = servicio.capturar_frame()
        if not ret:
            print("Error: no se pudo leer el frame")
            break
        
        #reset de contadores de piezas por frame
        piezas_ok_en_frame = 0
        piezas_nok_en_frame = 0
        text_cnt_ok = f"Piezas OK: {piezas_ok_en_frame}"
        text_cnt_nok = f"Piezas NOK: {piezas_nok_en_frame}"
        
        # 1. Extraemos la ROI usando el nuevo método limpio (sin pasarle el frame)
        roi = servicio.roi_matrix(roi_x, roi_y, roi_x + 300, roi_y + 250)

        

        # 2. Dibujamos el rectángulo en el frame original para el operario
        cv2.rectangle(frame, (roi_x, roi_y), (roi_x + 300, roi_y + 250), (255, 0, 0), 2) #type: ignore

        # 3. Obtenemos el valor del umbral de área desde el trackbar
        umbral_area = cv2.getTrackbarPos("Umbral Area", "Camera Info") #type: ignore
        area_text = f"Umbral Area: {umbral_area}"
        cv2.putText(frame, area_text, (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA) #type: ignore


        

        
        if roi is not None:
            #servicio.show_roi(roi)
            #pasamos la ROI a escala de grises
            grey_roi = servicio.roi_to_gray(roi)
            #cv2.imshow("ROI Grayscale", grey_roi) #type: ignore

            #noise filter
            filtered_roi = servicio.noise_filter(grey_roi)
            #cv2.imshow("ROI Noise Filtered", filtered_roi) #type: ignore

            #threshold
            threshold_roi = servicio.threshold_roi(filtered_roi)
            #cv2.imshow("ROI Threshold", threshold_roi) #type: ignore

            #adaptive threshold
            adaptative_roi = servicio.adaptive_threshold_roi(filtered_roi)
            #cv2.imshow("ROI Adaptative Threshold", adaptative_roi) #type: ignore

            #morph clean
            morph_cleaned = servicio.morph_clean(adaptative_roi)
            #cv2.imshow("ROI Morph Cleaned", morph_cleaned) #type: ignore

            #edge detection
            edges = servicio.detect_edges(morph_cleaned)
            cv2.imshow("ROI Edge Detection", edges) #type: ignore

            # 1. Buscamos los contornos válidos dentro de la ROI
            valid_contours = servicio.find_and_filter_contours(edges, min_area=400)
            
            # 2. Dibujamos los contornos encontrados sobre la ROI a color para verlos en tiempo real
            # cv2.drawContours(imagen, lista_contornos, indice_contorno (-1 para todos), color, grosor)
            if len(valid_contours) > 0:
                cv2.drawContours(roi, valid_contours, -1, (0, 255, 0), 2)
                # Volvemos a mostrar la ventana ROI a color actualizada con los contornos pintados
                #servicio.show_roi(roi)

                #calculo del bounding box de cada contorno válido y dibujamos un rectángulo alrededor de cada uno
                for contour in valid_contours:
                    x, y, w, h = cv2.boundingRect(contour)
                    cv2.rectangle(roi, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    # Mostramos la ROI con los bounding boxes dibujados
                    
                    #calculo del area de cada contorno válido y mostramos el valor en la ventana de la ROI
                    area = cv2.contourArea(contour)
                    if area < umbral_area:
                        text_color = (0, 0, 255)  # Rojo para áreas pequeñas
                        text_warning = "ALERTA: Objeto pequeño"
                        piezas_nok_en_frame += 1
                        text_cnt_nok = f"Piezas NOK: {piezas_nok_en_frame}"
                        
                    else:
                        text_color = (0, 255, 0)  # Verde para áreas grandes
                        text_warning = "Objeto OK"
                        piezas_ok_en_frame += 1 
                        text_cnt_ok = f"Piezas OK: {piezas_ok_en_frame}"
                        
                    global_x = roi_x + x
                    global_y = roi_y + y
                    
                    cv2.putText(roi, 
                                text_warning, 
                                (x, y-5), 
                                cv2.FONT_HERSHEY_SIMPLEX, 
                                0.5, 
                                text_color, 
                                1)
                cv2.putText(frame, #type: ignore
                            text_cnt_nok,
                            (10, 90), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, 
                            (0, 0, 255), 
                            2, 
                            cv2.LINE_AA
                            ) #type: ignore
                cv2.putText(frame, #type: ignore
                            text_cnt_ok, 
                            (10, 120), 
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            0.8, 
                            (0, 255, 0), 
                            2, 
                            cv2.LINE_AA
                            ) #type: ignore
                servicio.show_roi(roi) 


        # 5. Mostramos las ventanas
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

