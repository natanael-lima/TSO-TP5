"""
UNJu - Facultad de Ingeniería
Teoría de Sistemas Operativos (TSO) - Ciclo Lectivo 2026
Cátedra: Ing. María Fernanda Vázquez - JTP: Ing. Fabio D. Argañaraz

Ejercicio Práctico N° 2: El Problema del Oso y las Abejas
Bibliografía de Referencia:
- Silberschatz: Cap. 6.6 (Problemas clásicos de sincronización)
- Stallings: Cap. 5.4 (Sincronización con semáforos)
"""

import sys
import threading
import time
import random

# Configuración UTF-8 para consola Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

M = 10                  # Capacidad del tarro de miel
NUM_ABEJAS = 5          # Número de abejas obreras
tarro_miel = 0          # Variable compartida
simulacion_activa = True

mutex = threading.Lock()
sem_oso = threading.Semaphore(0)
sem_tarro_disponible = threading.Semaphore(1)

def abeja(id_abeja):
    global tarro_miel, simulacion_activa
    while simulacion_activa:
        time.sleep(random.uniform(0.05, 0.2))
        
        # TODO: Sincronizar el acceso al tarro de miel:
        # 1. Esperar a que el tarro esté disponible.
        sem_tarro_disponible.acquire()
        # 2. Entrar en exclusión mutua con el tarro.
        with mutex:
            if not simulacion_activa:
                sem_tarro_disponible.release()
                break
            
            # 3. Depositar una porción de miel
            tarro_miel += 1
            print(f"[Abeja {id_abeja}] Depositó miel. Total: {tarro_miel}/{M}")
            
            # 4. Si el tarro se llenó, despertar al oso
            if tarro_miel == M:
                sem_oso.release()
            else:
            
                sem_tarro_disponible.release()
        
        pass

def oso(max_tarros=2):
    global tarro_miel, simulacion_activa
    tarros_comidos = 0
    while tarros_comidos < max_tarros and simulacion_activa:
        # =====================================================================
        # TODO PARA EL ESTUDIANTE:
        # 1. Esperar pasivamente (bloqueado) hasta que una abeja señale que el tarro está lleno:
        sem_oso.acquire()
        with mutex:
            print(f"🐻 [OSO] ¡Olla llena! Comiendo miel (Tarro {tarros_comidos+1})...")
            # 2. Vaciar el tarro de miel
            tarro_miel = 0
            # 3. Incrementar el contador de tarros consumidos
            tarros_comidos += 1
            
        # 4. Avisar a las abejas que el tarro está vacío y disponible de nuevo
        sem_tarro_disponible.release()
        time.sleep(0.05)
        
    simulacion_activa = False
    # Liberaciones de seguridad para destrabar hilos dormidos al terminar
    for _ in range(NUM_ABEJAS + 5):
        try:
            sem_tarro_disponible.release()
        except ValueError:
            pass

if __name__ == "__main__":
    print("=" * 60)
    print(" Iniciando Simulación: El Oso y las Abejas (UNJu FI)")
    print("=" * 60)
 
    t_oso = threading.Thread(target=oso, args=(2,), name="Oso")
    t_oso.start()
    

    abejas = []
    for i in range(1, NUM_ABEJAS + 1):
        t_abeja = threading.Thread(target=abeja, args=(i,), name=f"Abeja-{i}")
        abejas.append(t_abeja)
        t_abeja.start()
        

    t_oso.join()
    for t in abejas:
        t.join()
    print("Simulación del Oso y las Abejas finalizada con éxito.")
    pass

