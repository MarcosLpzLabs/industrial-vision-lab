import queue, threading, time

buffer = queue.Queue(maxsize=1)

def sensor():
    for i in range(50):
        buffer.put(i)        # si está lleno, BLOQUEA al productor
        time.sleep(0.1)
    buffer.put(None)         # centinela: "no habrá más datos"

hilo = threading.Thread(target=sensor, daemon=True)
inicio = time.time()
hilo.start()

while True:
    dato = buffer.get()      # si está vacío, BLOQUEA al consumidor
    if dato is None:
        break
    print("consumido:", dato)
    time.sleep(0.5) # vuelve esto lento de más pero saca todos los numeros

final = time.time() - inicio
print("Tiempo total de ejecución:", final)
hilo.join()                  # esperar a que el hilo termine 