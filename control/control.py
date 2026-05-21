import time
from pymycobot import MyCobot

# Conexión al robot
# Ajusta el puerto '/dev/ttyUSB0' según tu PC (puede ser COM3 en Windows)
mc = MyCobot('/dev/ttyUSB0', 1000000)
mc.power_on()
time.sleep(0.5)

# Funciones seguras con reintentos
def safe_send_angles(mc, pose, speed, retries=3):
    for i in range(retries):
        try:
            mc.send_angles(pose, speed)
            time.sleep(2)
            return True
        except Exception as e:
            print(f"Intento {i+1} fallido: {e}")
    print("Error crítico: no se pudo enviar la pose")
    return False

def safe_set_gripper(mc, value, speed, retries=3):
    for i in range(retries):
        try:
            mc.set_gripper_value(value, speed)
            time.sleep(1)
            return True
        except Exception as e:
            print(f"Intento {i+1} fallido: {e}")
    print("Error crítico: no se pudo mover el gripper")
    return False

# Definir las poses clave
init_pose = [0.61, -0.43, -0.43, -1.66, 0.7, -44.2] # Pose inicial (reset seguro)
watch_pose = [10.63, -38.93, -49.13, -2.54, 0.7, -51.59] # Pose de observación (arriba del cubo)
pick_pose = [10.81, -52.11, -49.13, -2.28, 0.79, -50.97] # Pose de agarre (bajar hasta el cubo)
safe_pose = [10.63, -51.5, -9.58, -2.46, 0.35, -50.36]
# Pose intermedia segura (subir antes de mover)
place_pose = [87.62, -54.05, -43.41, 0.52, -4.04, -47.37]
# Pose de depósito (donde sueltas el cubo)


# Función de ciclo completo con manejo de errores
def run_cycle(mc):
    print("Iniciando ciclo...")
    safe_send_angles(mc, init_pose, 30)
    safe_send_angles(mc, watch_pose, 30)
    safe_send_angles(mc, pick_pose, 30)
    safe_set_gripper(mc, 0, 80)      # Cerrar gripper
    safe_send_angles(mc, safe_pose, 30)
    safe_send_angles(mc, place_pose, 30)
    safe_set_gripper(mc, 100, 80)    # Abrir gripper
    print("Ciclo completado.")

# Ejecutar 5 ciclos seguidos
for i in range(5):
    print(f"Ejecutando ciclo {i+1}")
    run_cycle(mc)
