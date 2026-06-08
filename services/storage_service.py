import cv2

class StorageService:
    def __init__(self, storage_path=""):
        self.storage_path = storage_path
        
    def save_frame(self,frame,filename):
        cv2.imwrite(f"{self.storage_path}/{filename}", frame)
        
    def save_log(self,log_data,filename):
        pass