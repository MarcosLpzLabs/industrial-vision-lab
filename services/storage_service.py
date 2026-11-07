import cv2
import os
import csv
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class StorageService:
    def __init__(self, storage_path=""):
        self.storage_path = storage_path

    def prepare_storage(self):
        os.makedirs(self.storage_path,exist_ok = True)

        
    def save_frame(self,frame,filename):
        path = os.path.join(self.storage_path, filename)
        ok = cv2.imwrite(path, frame)
        if not ok:
            logger.error(f"No se pudo guardar el frame en {path}")
        

    def registrar_metricas(self,nombre_frame:str,umbral:int,ok:int,nok:int,aspect_ratio:float | None,worst_ar:float | None ):
        '''registra las métricas del frame actual en un CSV con el histórico'''
        
        archivo_csv =os.path.join(self.storage_path,"reporte_produccion.csv")
        existe_archivo = os.path.exists(archivo_csv)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #se abre archivo en modo a (append) para añadir lineas al final sin borrar el registro
        with open(archivo_csv,mode="a",newline='',encoding="utf-8") as f:
            writer = csv.writer(f)
            # si el archivo es nuevo, escribimos primero la cabecera
            if not existe_archivo:
                writer.writerow(["timestamp","nombre_frame","umbral","aspect_ratio","ok","nok","worst_ar"])
            writer.writerow([timestamp,nombre_frame,umbral,aspect_ratio,ok,nok,worst_ar])