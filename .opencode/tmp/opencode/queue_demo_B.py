import queue, threading, time

buffer = queue.Queue(maxsize=1)

def sensor():
    perdido = 0

    for i in range(50):
        try:
            buffer.put_nowait(i)        # vemos que saca queue.Full si está lleno
        except queue.Full:
            try:
                buffer.get_nowait()  # sacamos el dato más viejo para hacer espacio
                buffer.put_nowait(i)  # intentamos poner el dato de nuevo
            except queue.Empty:
                buffer.put_nowait(i)# si no hay nada, lo ponemos de nuevo
            else:
                perdido += 1
            
        time.sleep(0.1)
    print("cantidad perdidos:", perdido)
    buffer.put(None)         # centinela: "no habrá más datos"

hilo = threading.Thread(target=sensor, daemon=True)
inicio = time.time()
hilo.start()

while True:
    dato = buffer.get()      # solución al queue full --> Rompe 
    if dato is None:
        break
    print("consumido:", dato)
    time.sleep(0.5)
final = time.time() - inicio
print("Tiempo total de ejecución:", final)
hilo.join()                  # esperar a que el hilo termine
