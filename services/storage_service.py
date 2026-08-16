import cv2
import os
from datetime import datetime
class StorageService:
    def __init__(self, storage_path=""):
        self.storage_path = storage_path
        
    def save_frame(self,frame,filename):
        cv2.imwrite(f"{self.storage_path}/{filename}", frame)
        
    def save_log(self,log_data,filename):
        pass

    def registrar_metricas(self,nombre_frame:str,umbral:int,ok:int,nok:int,aspect_ratio:float | None,worst_ar:float | None ):
        '''registra las métricas del frame actual en un CSV con el histórico'''
        
        archivo_csv =os.path.join(self.storage_path,"reporte_produccion.csv")
        existe_archivo = os.path.exists(archivo_csv)

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        #se abre archivo en modo a (append) para añadir lineas al final sin borrar el registro
        with open(archivo_csv,mode="a",encoding="utf-8") as f:
            # si el archivo es nuevo, escribimos primero la cabecera
            if not existe_archivo:
                f.write("timestamp,nombre_frame,umbral,aspect_ratio,ok,nok,worst_ar\n")
            #escribir la fila de datos
            f.write(f"{timestamp},{nombre_frame},{umbral},{aspect_ratio if aspect_ratio is not None else ''},{ok},{nok},{worst_ar if worst_ar is not None else ''}\n")