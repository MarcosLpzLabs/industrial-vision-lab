import math
import logging

logger = logging.getLogger("services.tracking")

class TrackedObject:
    def __init__(self, obj_id, centroid):
        self.id = obj_id
        self.centroid = centroid  # Tupla (cx, cy)
        self.counted = False      # Estado del conteo
        self.frames_disappeared = 0 # Para limpiar si se pierde la pieza

    

class TrackingService:
    def __init__(self, line_y: int, max_distance: int = 50, max_disappeared: int = 5):
        self.line_y = line_y
        self.max_distance = max_distance
        self.max_disappeared = max_disappeared
        
        self.next_id = 0
        self.tracked_objects = {} # Dict de {id: TrackedObject}
        self.total_count = 0      # Contador histórico acumulado

    def get_active_objects(self):
        return_list = []
        for obj in self.tracked_objects.values():
            # Creamos un diccionario nuevo y único para esta pieza en este frame
            obj_dict = {
                "id": obj.id,
                "centroid": obj.centroid,
                "counted": obj.counted
            }
            return_list.append(obj_dict)
            
        return return_list


    def update(self, current_centroids: list) -> int:
        """
        Recibe los centroides del frame actual [(cx, cy), (cx, cy)...]
        Actualiza los estados de tracking y devuelve el contador histórico global.
        """


        # 1. Emparejamiento por proximidad Euclídea
        # Mapeamos los IDs actuales con los nuevos centroides
        updated_objects = {}
        used_current_indices = set()

        # Intentar emparejar los objetos existentes con los más cercanos actuales
        for obj_id, obj in self.tracked_objects.items():
            min_dist = float("inf") # infinito positivo, se usa para comparar, nunca un valor va a ser mayor que infinito
            best_idx = None

            for idx, centroid in enumerate(current_centroids):
                if idx in used_current_indices:
                    continue
                
                # Distancia euclídea clásica de ingeniería
                dist = math.hypot(centroid[0] - obj.centroid[0], centroid[1] - obj.centroid[1])
                
                if dist < min_dist and dist < self.max_distance:
                    min_dist = dist
                    best_idx = idx

            if best_idx is not None:
                # Comprobar si ha cruzado la línea virtual antes de actualizar coordenadas
                new_centroid = current_centroids[best_idx]
                self._check_line_crossing(obj, new_centroid)
                
                # Actualizar el objeto con los datos del nuevo frame
                obj.centroid = new_centroid
                obj.frames_disappeared = 0
                updated_objects[obj_id] = obj
                used_current_indices.add(best_idx)
            else:
                # El objeto no se encontró en este frame
                obj.frames_disappeared += 1
                if obj.frames_disappeared <= self.max_disappeared:
                    updated_objects[obj_id] = obj
                else:
                    logger.info(f"Objeto ID {obj_id} fuera de la ROI. Eliminado del tracking.")

        # 2. Registrar los centroides que sobraron como nuevos objetos
        # Ahora añadimos las nuevas detecciones directamente a `updated_objects`
        # para que sobrevivan cuando reasignemos `self.tracked_objects`.
        for idx, centroid in enumerate(current_centroids):
            if idx not in used_current_indices:
                self._register_object(centroid, updated_objects)

        self.tracked_objects = updated_objects
        return self.total_count

    def _register_object(self, centroid, container=None):
        """Registra un nuevo objeto.

        Si se pasa `container`, el nuevo objeto se añadirá ahí en lugar de
        directamente en `self.tracked_objects`. Devuelve el objeto creado.
        """
        obj = TrackedObject(self.next_id, centroid)
        if container is None:
            # comportamiento por compatibilidad: añadir al dict principal
            self.tracked_objects[self.next_id] = obj
        else:
            container[self.next_id] = obj

        logger.debug(f"Nuevo objeto detectado en planta. ID asignado: {self.next_id}")
        self.next_id += 1
        return obj

    def _check_line_crossing(self, obj: TrackedObject, new_centroid: tuple):
        # Condición: El centroide anterior estaba arriba (y < line) y el nuevo abajo (y >= line)
        # Nota: En OpenCV, la Y crece hacia abajo de la pantalla
        if not obj.counted:
            if obj.centroid[1] < self.line_y <= new_centroid[1]:
                obj.counted = True
                self.total_count += 1
                logger.info(f"¡PIEZA CONTADA! ID {obj.id} cruzó la línea virtual. Total histórico: {self.total_count}")