import numpy as np
import time
from pymycobot.mycobot import MyCobot

def dh_transform(a, d, alpha_deg, theta_deg):
    theta_rad = np.radians(theta_deg)
    alpha_rad = np.radians(alpha_deg)
    ct = np.cos(theta_rad)
    st = np.sin(theta_rad)
    ca = np.cos(alpha_rad)
    sa = np.sin(alpha_rad)
    return np.array([
        [ct, -st*ca,  st*sa, a*ct],
        [st,  ct*ca, -ct*sa, a*st],
        [0,      sa,     ca,    d],
        [0,       0,      0,    1]
    ])

# DEFINIR CONFIGURACIÓN DE PRUEBA 
angulos_prueba = [0, 0, 0, 0, 0, 0] 

dh_base = [
    (0,     131.56,   90),   
    (110.4,   0,       0),   
    (96,      0,       0),   
    (0,      66.39,  -90),   
    (0,      73.18,   90),   
    (0,      48.6,     0)    
]


T_total = np.eye(4)
for i in range(6):
    a, d, alpha = dh_base[i]
    theta = angulos_prueba[i]
    T_total = T_total @ dh_transform(a, d, alpha, theta)

pos_calculada = T_total[:3, 3]
print(f"Modelo DH calculado: x={pos_calculada[0]:.2f} mm, y={pos_calculada[1]:.2f} mm, z={pos_calculada[2]:.2f} mm")
----------------------------------------------------------------------------------------------
# Conectar al robot real
mc = MyCobot('/dev/ttyUSB0', 1000000)
mc.power_on()
time.sleep(1)

print("Moviendo el brazo robótico real")
mc.send_angles(angulos_prueba, 30) 

time.sleep(5) 
print("Movimiento terminado.")
---------------------------------------------------


# Leer coordenadas del robot real una vez detenido
coords = mc.get_coords()
if coords:
    pos_real = np.array(coords[:3])
    print(f"Robot real API: x={pos_real[0]:.2f} mm, y={pos_real[1]:.2f} mm, z={pos_real[2]:.2f} mm")
    
    # Calculo de diferencias reales
    diff = pos_calculada - pos_real
    print("\n=== DIFERENCIA REAL MEDIDA ===")
    print(f"Δx = {abs(diff[0]):.2f} mm")
    print(f"Δy = {abs(diff[1]):.2f} mm")
    print(f"Δz = {abs(diff[2]):.2f} mm")
else:
    print("Error: El API no leyó las coordenadas. Ejecuta esta celda de nuevo.")
    
--------------------------------------------------------------------------------------------------------
    
